''' Various custom widgets for achieving complex behavior such as
    the media progress slider, the concatenation dialog's list
    items, draggable frames, advanced hotkey widgets, and more.

    thisismy-github '''

from __future__ import annotations

from PyQt5 import QtGui, QtCore, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets as QtW

import qtstart
import constants
import qthelpers
from constants import SetProgressContext
from util import ffmpeg, ffmpeg_async, get_hms, get_PIL_Image, get_unique_path

import os
import time
import math
import logging

import vlc
from colour import Color
from threading import Thread
from traceback import format_exc
from vlc import State

# TODO: I absolutely cannot decide what should be camelCase and what should be underscores. It's becoming an issue.
# media_player: ['_as_parameter_', '_instance', 'add_slave', 'audio_get_channel', 'audio_get_delay', 'audio_get_mute', 'audio_get_track', 'audio_get_track_count', 'audio_get_track_description', 'audio_get_volume', 'audio_output_device_enum', 'audio_output_device_get', 'audio_output_device_set', 'audio_output_set', 'audio_set_callbacks', 'audio_set_channel', 'audio_set_delay', 'audio_set_format', 'audio_set_format_callbacks', 'audio_set_mute', 'audio_set_track', 'audio_set_volume', 'audio_set_volume_callback', 'audio_toggle_mute', 'can_pause', 'event_manager', 'from_param', 'get_agl', 'get_chapter', 'get_chapter_count', 'get_chapter_count_for_title', 'get_fps', 'get_full_chapter_descriptions', 'get_full_title_descriptions', 'get_fullscreen', 'get_hwnd', 'get_instance', 'get_length', 'get_media', 'get_nsobject', 'get_position', 'get_rate', 'get_role', 'get_state', 'get_time', 'get_title', 'get_title_count', 'get_xwindow', 'has_vout', 'is_playing', 'is_seekable', 'navigate', 'next_chapter', 'next_frame', 'pause', 'play', 'previous_chapter', 'program_scrambled', 'release', 'retain', 'set_agl', 'set_android_context', 'set_chapter', 'set_equalizer', 'set_evas_object', 'set_fullscreen', 'set_hwnd', 'set_media', 'set_mrl', 'set_nsobject', 'set_pause', 'set_position', 'set_rate', 'set_renderer', 'set_role', 'set_time', 'set_title', 'set_video_title_display', 'set_xwindow', 'stop', 'toggle_fullscreen', 'toggle_teletext', 'video_get_adjust_float', 'video_get_adjust_int', 'video_get_aspect_ratio', 'video_get_chapter_description', 'video_get_crop_geometry', 'video_get_cursor', 'video_get_height', 'video_get_logo_int', 'video_get_marquee_int', 'video_get_marquee_string', 'video_get_scale', 'video_get_size', 'video_get_spu', 'video_get_spu_count', 'video_get_spu_delay', 'video_get_spu_description', 'video_get_teletext', 'video_get_title_description', 'video_get_track', 'video_get_track_count', 'video_get_track_description', 'video_get_width', 'video_set_adjust_float', 'video_set_adjust_int', 'video_set_aspect_ratio', 'video_set_callbacks', 'video_set_crop_geometry', 'video_set_deinterlace', 'video_set_format', 'video_set_format_callbacks', 'video_set_key_input', 'video_set_logo_int', 'video_set_logo_string', 'video_set_marquee_int', 'video_set_marquee_string', 'video_set_mouse_input', 'video_set_scale', 'video_set_spu', 'video_set_spu_delay', 'video_set_subtitle_file', 'video_set_teletext', 'video_set_track', 'video_take_snapshot', 'video_update_viewpoint', 'will_play']
# media: ['_as_parameter_', '_instance', 'add_option', 'add_option_flag', 'add_options', 'duplicate', 'event_manager', 'from_param', 'get_duration', 'get_instance', 'get_meta', 'get_mrl', 'get_parsed_status', 'get_state', 'get_stats', 'get_tracks_info', 'get_type', 'get_user_data', 'is_parsed', 'parse', 'parse_async', 'parse_stop', 'parse_with_options', 'player_new_from_media', 'release', 'retain', 'save_meta', 'set_meta', 'set_user_data', 'slaves_add', 'slaves_clear', 'slaves_get', 'subitems', 'tracks_get']


# ------------------------------------------
# Logger
# ------------------------------------------
logger = logging.getLogger('widgets.py')


# ------------------------------------------
# Aliases (set in main.pyw)
# ------------------------------------------
gui: QtW.QMainWindow = None
app = QtW.qApp
cfg = None
settings = None
ZOOM_DYNAMIC_FIT = 0
ZOOM_NO_SCALING  = 1
ZOOM_FIT         = 2
ZOOM_FILL        = 3


# ------------------------------------------
# Core Widgets
# ------------------------------------------
class PyPlayerBackend:

    __name__ = 'Undefined'
    SUPPORTS_PARSING = False                                # Can this player parse and return critical media info (fps, duration, etc.)?
    SUPPORTS_VIDEO_TRACK_MANIPULATION = False               # Can this player return video track info AND set video tracks?
    SUPPORTS_AUDIO_TRACK_MANIPULATION = False               # Can this player return audio track info AND set audio tracks?
    SUPPORTS_SUBTITLE_TRACK_MANIPULATION = False            # Can this player return subtitle track info AND set subtitle tracks?
    SUPPORTS_AUTOMATIC_SUBTITLE_ENABLING = False            # Does this player auto-enable subtitle tracks when present?
    ENABLE_AUTOMATIC_TRACK_RESTORATION = True               # Should PyPlayer restore its saved tracks/delays when opening/restoring? NOTE: Avoid this if possible!!
    ENABLE_AUTOMATIC_TRACK_RESET = True                     # Should PyPlayer reset its saved tracks/delays to None when opening new files?

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.enabled = False
        self.menu: QtW.QMenu = None

        self.last_file = ''
        self.file_being_opened = ''
        self.open_cleanup_queued = False

        self.text = None
        self.last_text = None
        self._text_position = 5
        self._text_height_percent = 0.05
        self._text_x_percent = 0.016
        self._text_y_percent = 0.016
        self._text_opacity = 255

    # ---

    def __getattr__(self, name: str):
        ''' Allows access to undefined player-specific properties.
            This is mainly intended for testing purposes. '''
        logger.info(f'Attempting to access undefined player-specific property `player.{name}`')
        return getattr(self._player, name)

    # ---

    def enable(self) -> bool:
        ''' Called upon enabling the backend. When starting PyPlayer, this is
            called immediately after `gui.setup()` and loading the config, but
            before showing the window. '''
        self.enabled = True
        self.open_cleanup_queued = False
        return True

    def disable(self, wait: bool = True):
        ''' Called upon disabling the backend. Stop playing, set `self.enabled`
            to False, perform cleanup, disconnect signals, and end all threads.
            NOTE: If `wait` is False, do not wait for cleanup unless absolutely
            necessary. Instead, have `self.enable()` wait for unfinished cleanup
            before re-enabling. '''
        self.enabled = False
        self.open_cleanup_queued = False
        self.stop()

    def show(self):
        pass

    # ---

    def on_show(self, event: QtGui.QShowEvent):
        ''' Called in `gui.showEvent()`, before the window's
            state has been fully restored/validated. '''
        self.show()

    def on_resize(self, event: QtGui.QResizeEvent):
        ''' Called at the end of `QVideoPlayer.resizeEvent()`. '''
        pass

    def on_fullscreen(self, fullscreen: bool):
        ''' Called at the end of `gui.set_fullscreen()`, just before calling
            `gui.showFullScreen()`/`gui.showMaximized()`/`gui.showNormal()`. '''
        pass

    def on_parse(self, file: str, base_mime: str, mime: str, extension: str):
        ''' Called at the end of `gui.parse_media_file()`. All probe-related
            properties will be up-to-date when this event fires. Rarely, `mime`
            may mutate - `base_mime` is what `file` was initially parsed as.
            NOTE: This event MUST emit `gui._open_cleanup_signal` in some way.
            If you do not emit it directly, set `self.open_cleanup_queued` to
            True until the cleanup signal is emitted so PyPlayer understands
            that it's waiting for cleanup.
            NOTE: This event fires even if FFprobe finishes first, and the UI
            will begin updating immediately afterwards. If you wish to override
            probe properties, you must decide between waiting for the player
            to finish parsing or using `self.on_open_cleanup()` instead. '''
        gui._open_cleanup_signal.emit()

    def on_open_cleanup(self):
        ''' Called at the end of `gui._open_cleanup_slot()`. All opening-related
            properties (aside from `gui.open_in_progress`) will be up-to-date
            when this even fires. '''
        pass

    def on_restart(self):
        ''' Called in `gui.restart()`, immediately after confirming the restart
            is valid. `gui.restarted` will be False. After this event, the UI
            be updated and the player will be force-paused. This event should
            do any extraneous cleanup that must be urgently completed to ensure
            finished media is immediately/seamlessly ready to play again. '''
        gui.update_progress_signal.emit(gui.frame_count)    # ensure UI snaps to final frame

    # ---

    def play(self, file: str, will_restore: bool = False) -> bool:
        ''' Opens the provided `file`, and begins *asynchronously* parsing
            the media if supported by the player. `will_restore` will be
            True if we're intending to set the progress to an arbitrary value
            immediately afterwards (e.g. after a renaming or restart). '''
        raise NotImplementedError()

    def pause(self):
        ''' Toggles the pause state. '''
        raise NotImplementedError()

    def stop(self):
        ''' Stops the player, releasing any locks. '''
        raise NotImplementedError()

    def loop(self):
        ''' Loops the player back to `gui.minimum` after the media *completes*.
            This is not called when there is an ending marker. '''
        self.set_and_update_progress(gui.minimum, SetProgressContext.RESET_TO_MIN)
        return gui.force_pause(False)

    def snapshot(self, path: str, frame: int, width: int, height: int):
        ''' Saves the desired `frame` to `path`, resized to `width`x`height`.
            NOTE: Do not return until the snapshot is complete and saved.
            NOTE: You should probably override this. FFmpeg sucks. '''
        w = width or -1                                     # -1 uses aspect ratio in ffmpeg
        h = height or -1                                    # using `-ss` is faster but even less accurate
        ffmpeg(f'-i "{gui.video}" -frames:v 1 -vf "select=\'eq(n\\,{frame})\', scale={w}:{h}" "{path}"')

    # ---

    def set_pause(self, paused: bool):
        ''' Sets the pause state to `paused`. '''
        raise NotImplementedError()

    def get_mute(self) -> bool:
        ''' Returns the mute state. '''
        raise NotImplementedError()

    def set_mute(self, muted: bool):
        ''' Sets the mute state to `muted`. '''
        raise NotImplementedError()

    def get_volume(self) -> int:
        ''' Returns the volume between 0-100. '''
        raise NotImplementedError()

    def set_volume(self, volume: int):
        ''' Sets the `volume` between 0-100 (or above). '''
        raise NotImplementedError()

    def get_playback_rate(self) -> float:
        ''' Returns the playback rate relative to 1.0. '''
        return 1.0

    def set_playback_rate(self, rate: float):
        ''' Sets the playback `rate` relative to 1.0. '''
        self.show_text('Playback speed is not supported by the selected player.')

    def get_position(self) -> float:
        ''' Returns the media's progress as a value between 0.0-1.0. '''
        raise NotImplementedError()

    def set_position(self, percent: float):
        ''' Sets media progress to a `percent` between 0.0-1.0. '''
        raise NotImplementedError()

    def set_frame(self, frame: int):
        ''' Called while frame-seeking (or entering an exact frame).
            Use this if you have anything special you'd like to do
            (e.g. libVLC's `next_frame()`). '''
        self.set_and_update_progress(frame)

    def set_and_update_progress(self, frame: int = 0, context: int = SetProgressContext.NONE):
        ''' Sets player position to `frame` and updates the UI accordingly.
            `context` is useful if you need to do additional work depending
            on the specific reason we're manually setting the position.
            NOTE: Don't forget to update GIF progress.
            NOTE: This method should update the player's non-GIF progress
            ASAP, so the player feels "snappier" on the user's end. '''
        self.set_position(frame / gui.frame_count)
        gui.update_progress(frame)
        gui.gifPlayer.gif.jumpToFrame(frame)

    # ---

    def get_state(self) -> int:                             # TODO
        return State.NothingSpecial

    def can_restart(self) -> bool:
        ''' Called at the start of `gui.restart()`.
            Returns False if a restart should be skipped. '''
        return True

    def is_parsed(self) -> bool:
        ''' Returns True if the player has finished its own
            parsing of the current media, independent of FFprobe. '''
        return False

    def is_playing(self) -> bool:
        ''' Semi-convenience method. Returns True if
            we are actively playing unpaused media. '''
        raise NotImplementedError()

    def get_fps(self) -> float:
        ''' Returns the frame rate of the current
            media if possible, otherwise 0.0. '''
        return 0.0

    def get_duration(self) -> float:
        ''' Returns the duration (in seconds) of the
            current media if possible, otherwise 0.0. '''
        return 0.0

    def get_dimensions(self) -> tuple[int, int]:
        ''' Returns the dimensions of the current media as a tuple if possible,
            otherwise `(0, 0)`. This method may raise an exception. '''
        return 0, 0

    # ---

    def get_audio_delay(self) -> int:
        return 0

    def set_audio_delay(self, msec: int):
        self.show_text('Audio delays are not supported by the selected player.')

    def get_subtitle_delay(self) -> int:
        return 0

    def set_subtitle_delay(self, msec: int):
        self.show_text('Subtitle delays are not supported by the selected player.')

    def get_video_track(self) -> int:
        return -1

    def get_audio_track(self) -> int:
        return -1

    def get_subtitle_track(self) -> int:
        return -1

    def get_video_tracks(self, raw: bool = False) -> tuple[int, str]:
        ''' Generator that yields each video track's ID and title as a
            tuple. If `raw` is True, the title should be yielded as-is. '''
        yield -1, 'The selected player does not support tracks'

    def get_audio_tracks(self, raw: bool = False) -> tuple[int, str]:
        ''' Generator that yields each audio track's ID and title as a
            tuple. If `raw` is True, the title should be yielded as-is. '''
        yield -1, 'The selected player does not support tracks'

    def get_subtitle_tracks(self, raw: bool = False) -> tuple[int, str]:
        ''' Generator that yields each subtitle track's ID and title as a
            tuple. If `raw` is True, the title should be yielded as-is. '''
        yield -1, 'The selected player does not support tracks'

    def get_video_track_count(self) -> int:
        return 1

    def get_audio_track_count(self) -> int:
        return 1

    def get_subtitle_track_count(self) -> int:
        return 1

    def set_video_track(self, index: int):
        self.show_text('Track manipulation is not supported by the selected player.')

    def set_audio_track(self, index: int):
        self.show_text('Track manipulation is not supported by the selected player.')

    def set_subtitle_track(self, index: int):
        self.show_text('Track manipulation is not supported by the selected player.')

    def add_audio_track(self, url: str, enable: bool = False) -> bool:
        self.show_text('Dynamically adding audio tracks is not supported by the selected player.')

    def add_subtitle_track(self, url: str, enable: bool = False) -> bool:
        self.show_text('Dynamically adding subtitle tracks is not supported by the selected player.')

    # ---

    def show_text(self, text: str, timeout: int = 350, position: int = None):
        ''' Displays marquee `text` (overlaying the player),
            overriding the default `position` if desired. '''
        if not settings.groupText.isChecked(): return       # marquees are completely disabled -> return
        gui.statusbar.showMessage(text.replace('%%', '%'), max(timeout, 1000))

    def set_text_position(self, button: QtW.QRadioButton):
        ''' Sets marquee text's position to one of 9 pre-defined values
            represented by a `button` on the settings dialog. Use
            `int(button.objectName()[17:])` to get a number between
            1-9 representing top-left to bottom-right. '''
        self._text_position = int(button.objectName()[17:])

    def set_text_height(self, percent: int):
        ''' Sets marquee text's size (specifically its height) to a `percent`
            between 0-100 that is relative to the current media. '''
        self._text_height_percent = percent / 100

    def set_text_x(self, percent: float):
        ''' Sets marquee text's x-offset from the nearest edge to a `percent`
            between 0-100 that is relative to the current media. '''
        self._text_x_percent = percent / 100

    def set_text_y(self, percent: float):
        ''' Sets marquee text's y-offset to a `percent` between
            0-100 that is relative to the current media. '''
        self._text_y_percent = percent / 100

    def set_text_opacity(self, percent: int):
        ''' Sets marquee text's max opacity to a `percent` between 0-100. '''
        self._text_opacity = round(255 * (percent / 100))

    # ---

    def __repr__(self) -> str:
        return self.__name__




class PlayerVLC(PyPlayerBackend):
    ''' TODO: vlc.Instance() arguments to check out:
        --align={0 (Center), 1 (Left), 2 (Right), 4 (Top), 8 (Bottom), 5 (Top-Left), 6 (Top-Right), 9 (Bottom-Left), 10 (Bottom-Right)}
        --audio-time-stretch, --no-audio-time-stretch   Enable time stretching audio (default enabled) <- disabled = pitch changes with playback speed
        --gain=<float [0.000000 .. 8.000000]>           Audio gain
        --volume-step=<float [1.000000 .. 256.000000]>  Audio output volume step
        --marq-marquee, --sub-source=marq '''

    __name__ = 'VLC'
    SUPPORTS_PARSING = True
    SUPPORTS_VIDEO_TRACK_MANIPULATION = True
    SUPPORTS_AUDIO_TRACK_MANIPULATION = True
    SUPPORTS_SUBTITLE_TRACK_MANIPULATION = True
    SUPPORTS_AUTOMATIC_SUBTITLE_ENABLING = True
    ENABLE_AUTOMATIC_TRACK_RESTORATION = False
    ENABLE_AUTOMATIC_TRACK_RESET = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._media: vlc.Media = None
        self._instance: vlc.Instance = None
        self._player: vlc.MediaPlayer = None
        self._event_manager = None

        self.opening = False
        self.ui_delay = 0.0
        self.is_pitch_sensitive_audio = False
        self.is_bad_with_vlc = False
        self.add_to_progress_offset = 0.0
        self.reset_progress_offset = False
        self.swap_slider_styles_queued = False

        self.text_fade_start_time = 0.0
        self.text_fade_end_time = 0.0
        self.text_fade_thread_open = False
        self.metronome_thread_open = False
        self.slider_thread_open = False

        self.context_offsets = {
            SetProgressContext.RESTORE:             None,
            SetProgressContext.RESTART:             0.0,
            SetProgressContext.RESET_TO_MIN:        None,   # `QVideoSlider.mouseReleaseEvent()` had this as 0.01
            SetProgressContext.RESET_TO_MAX:        None,   # `QVideoSlider.mouseReleaseEvent()` had this as 0.01
            SetProgressContext.NAVIGATION_RELATIVE: 0.1,
            SetProgressContext.NAVIGATION_EXACT:    0.075,  # `manually_update_current_time()` had this as 0.01
            SetProgressContext.SCRUB:               None
        }


    def enable(self) -> bool:
        while self.metronome_thread_open or self.slider_thread_open or self.text_fade_thread_open:
            time.sleep(0.02)
        super().enable()

        # setup VLC instance
        logger.info(f'VLC arguments: {qtstart.args.vlc}')
        self._instance = vlc.Instance(qtstart.args.vlc)     # VLC arguments can be passed through the --vlc argument
        player = self._player = self._instance.media_player_new()
        event_manager = self._event_manager = player.event_manager()

        # NOTE: cannot use .emit as a callback
        event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, lambda event: gui.restart_signal.emit())
        event_manager.event_attach(vlc.EventType.MediaPlayerOpening, lambda event: setattr(self, 'opening', True))
        event_manager.event_attach(vlc.EventType.MediaPlayerPlaying, self._on_play)

        self.get_playback_rate = player.get_rate
        self.set_playback_rate = player.set_rate
        self.get_position = player.get_position
        self.set_position = player.set_position
        self.get_volume = player.audio_get_volume
        self.set_volume = player.audio_set_volume
        self.get_mute = player.audio_get_mute
        self.set_mute = player.audio_set_mute
        self.pause = player.pause
        self.set_pause = player.set_pause
        self.stop = player.stop
        self.snapshot = lambda path, frame, w, h: player.video_take_snapshot(0, psz_filepath=path, i_width=w, i_height=h)
        self.get_state = player.get_state
        self.is_playing = player.is_playing
        self.get_fps = player.get_fps                       # TODO: self.vlc.media.get_tracks() might be more accurate, but I can't get it to work
        self.get_duration = lambda: player.get_length() / 1000
        self.get_dimensions = player.video_get_size         # ↓ VLC uses microseconds for delays for some reason
        self.get_audio_delay = lambda: player.audio_get_delay() / 1000
        self.set_audio_delay = lambda msec: player.audio_set_delay(msec * 1000)
        self.get_subtitle_delay = lambda: player.video_get_spu_delay() / 1000
        self.set_subtitle_delay = lambda msec: player.video_set_spu_delay(msec * 1000)
        self.get_audio_track = player.audio_get_track
        self.get_video_track = player.video_get_track
        self.get_subtitle_track = player.video_get_spu
        self.get_audio_tracks = lambda raw = False: self._get_tracks(player.audio_get_track_description, raw)
        self.get_video_tracks = lambda raw = False: self._get_tracks(player.video_get_track_description, raw)
        self.get_subtitle_tracks = lambda raw = False: self._get_tracks(player.video_get_spu_description, raw)
        self.get_audio_track_count = lambda: player.audio_get_track_count() - 1
        self.get_video_track_count = lambda: player.video_get_track_count() - 1
        self.get_subtitle_track_count = lambda: player.video_get_spu_count() - 1
        self.set_audio_track = player.audio_set_track
        self.set_video_track = player.video_set_track
        self.set_subtitle_track = player.video_set_spu

        player.stop()                                       # stopping the player at any point fixes the audio-cutoff bug
        player.video_set_key_input(False)                   # pass VLC key events to widget
        player.video_set_mouse_input(False)                 # pass VLC mouse events to widget
        player.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, 1)

        # manually refresh text-related settings
        self.set_text_height(settings.spinTextHeight.value())
        self.set_text_x(settings.spinTextX.value())
        self.set_text_y(settings.spinTextY.value())

        # start slider-related threads (these are safe to do before showing window)
        self.swap_slider_styles_queued = False
        self.metronome_thread_open = False
        self.slider_thread_open = False
        Thread(target=self.update_slider_thread, daemon=True).start()
        Thread(target=self.high_precision_slider_accuracy_thread, daemon=True).start()
        return True


    def disable(self, wait: bool = True):                   # TODO do we need `gui.frame_override` in here for smooth transitions?
        super().disable()
        self.text_fade_thread_open = False
        self.open_cleanup_queued = False
        if wait:
            while self.metronome_thread_open or self.slider_thread_open:
                time.sleep(0.02)
            self._media = None
            self._instance = None
            self._player = None
            self._event_manager = None


    def show(self):
        if constants.IS_WINDOWS: self._player.set_hwnd(self.parent.winId())
        elif constants.IS_MAC:   self._player.set_nsobject(int(self.parent.winId()))
        else:                    self._player.set_xwindow(self.parent.winId())


    def _on_play(self, event: vlc.Event):
        ''' VLC event. '''
        if self.opening:
            self.opening = False

            # HACK: for some files, VLC will always default to the wrong audio track (NO idea...
            # ...why, nothing unusal in any media-parsing tool i've used and no other player...
            # ...does it) -> when opening a new file, immediately set all tracks to track 1
            if self.last_file != self.file_being_opened:
                self.last_file = self.file_being_opened
                gui.last_video_track = 1
                gui.last_audio_track = 1
                gui.last_subtitle_track = 1 if settings.checkAutoEnableSubtitles.isChecked() else -1
                gui.last_audio_delay = 0
                gui.last_subtitle_delay = 0
            gui.tracks_were_changed = True
            gui.restore_tracks()


    def on_parse(self, file: str, base_mime: str, mime: str, extension: str):
        if base_mime == 'image':
            gui._open_cleanup_signal.emit()                 # manually emit _open_cleanup_signal for images/gifs (slider thread will be idle)
            self.is_pitch_sensitive_audio = False
            self.is_bad_with_vlc = False
        else:
            self.open_cleanup_queued = True                 # `open_cleanup_queued` + `open_in_progress` and `frame_override` work...
            gui.frame_override = 0                          # ...together to halt `update_slider_thread()` and trigger cleanup safely

            # TODO: we should really be tracking the codec instead of the container here
            # TODO: can this be fixed with a different demuxer or something? (what we COULD have done to fix pitch-shifting)
            if extension == 'ogg':                          # TODO: flesh out a list of unresponsive media types
                self.is_bad_with_vlc = True
                self.is_pitch_sensitive_audio = False
            else:
                self.is_bad_with_vlc = False
                self.is_pitch_sensitive_audio = mime == 'audio'

            # update marquee size and offset relative to video's dimensions
            if mime == 'video':
                height = gui.vheight
                set_marquee_int = self._player.video_set_marquee_int
                set_marquee_int(vlc.VideoMarqueeOption.Size, int(height * self._text_height_percent))
                set_marquee_int(vlc.VideoMarqueeOption.X,    int(height * self._text_x_percent))
                set_marquee_int(vlc.VideoMarqueeOption.Y,    int(height * self._text_y_percent))


    def on_open_cleanup(self):
        # warn users that the current media will not scrub/navigate very well
        # TODO: what else needs to be here (and set as not `self.is_pitch_sensitive_audio`)?
        if self.is_bad_with_vlc:
            gui.statusbar.showMessage(f'Note: Files of this mime type/encoding ({gui.mime_type}/{gui.extension}) may be laggy or unresponsive while scrubbing/navigating on some systems (libVLC issue).')


    def on_restart(self):
        self.play(gui.video)
        frame = gui.frame_count
        self.set_position((frame - 2) / frame)              # reset position (-2 frames to ensure visual update for VLC)
        gui.update_progress_signal.emit(frame)              # ensure UI snaps to final frame
        while self.get_state() == State.Ended:              # wait for VLC to update the player's state
            time.sleep(0.005)


    def play(self, file: str, will_restore: bool = False, _error: bool = False) -> bool:
        ''' Open, parse, and play a `file` in libVLC, returning True if
            successful. If `file` cannot be played, the currently opened file
            is reopened if possible. NOTE: Parsing is started asynchronously.
            This function returns immediately upon playing the file. '''
        try:
            self._media = self._instance.media_new(file)    # combines media_new_path (local files) and media_new_location (urls)
            self._player.set_media(self._media)             # TODO: this line has a HUGE delay when opening first file after opening extremely large video
            #self._player.set_mrl(self.media.get_mrl())     # not needed? https://www.olivieraubert.net/vlc/python-ctypes/doc/vlc.MediaPlayer-class.html#set_mrl
            self._player.play()

            # NOTE: parsing normally is still relatively fast, but libVLC is not as effective/compatible as FFprobe
            #       additionally, reading an already-created probe file is MUCH faster (relatively) than parsing with libVLC
            self._media.parse_with_options(0x0, 0)          # https://www.olivieraubert.net/vlc/python-ctypes/doc/vlc.Media-class.html#parse_with_options
            self.file_being_opened = file
            return True
        except:
            logger.warning(f'VLC failed to play file {file}: {format_exc()}')
            if not _error and file != gui.video:            # `_error` ensures we only attempt to play previous video once
                if not gui.video: self._player.stop()       # no previous video to play, so just stop playing
                else: self.play(gui.video, _error=True)     # attempt to play previous working video
            return False


    def loop(self):
        self.play(gui.video)
        # TODO just in case doing `set_and_update_progress` causes hitches or delays, we're...
        # ...doing an if-statement instead to ensure normal loops are slightly more seamless
        #set_and_update_progress(self.minimum)              # <- DOES this cause hitches?
        if self.buttonTrimStart.isChecked():
            return gui.update_progress(0)
        return self.set_and_update_progress(gui.minimum, SetProgressContext.RESET_TO_MIN)


    def can_restart(self) -> bool:
        # HACK: sometimes VLC will double-restart -> replay/restore position ASAP
        if gui.restarted:
            logging.info('Double-restart detected. Ignoring...')
            gui.restarted = False                           # set this so we don't get trapped in an infinite restart-loop
            return gui.restore(gui.sliderProgress.value())

        # reset frame_override in case it's set
        gui.frame_override = -1

        # HACK: skip this restart if needed and restore actual progress
        if gui.ignore_imminent_restart:
            gui.ignore_imminent_restart = False
            gui.restarted = True
            return gui.restore(gui.sliderProgress.value())

        # we're good to go. continue with restart
        return True


    def is_parsed(self) -> bool:
        _player = self._player
        return (
            self._media.get_parsed_status() == 4
            and _player.get_fps() != 0
            and _player.get_length() != 0
            and _player.video_get_size() != (0, 0)
        )


    def set_playback_rate(self, rate: float):
        self._player.set_playback_rate(rate)
        if rate == 1.0 or gui.playback_rate == 1.0:         # TODO: for now, lets just force the VLC-progress for non-standard speeds
            self.reset_progress_offset = True
            self.swap_slider_styles_queued = True


    def set_and_update_progress(self, frame: int = 0, context: int = SetProgressContext.NONE):
        ''' Simultaneously sets VLC/gif player position to `frame`, avoids the
            pitch-shift-bug for unpaused audio, and adjusts the high-precision
            progress offset by `offset` seconds (if provided) to account for
            VLC buffering. `offset` is ignored if `self.is_paused` is True. '''

        # don't touch progress if we're currently opening a file
        if gui.open_in_progress:
            return

        offset = self.context_offsets.get(context, None)
        if offset is None:
            return super().set_and_update_progress(frame, context)

        is_paused = gui.is_paused
        is_pitch_sensitive_audio = self.is_pitch_sensitive_audio

        # HACK: "replay" audio file to correct VLC's pitch-shifting bug
        # https://reddit.com/r/VLC/comments/i4m0by/pitch_changing_on_seek_only_some_audio_file_types/
        # https://reddit.com/r/VLC/comments/b0i9ff/music_seems_to_pitch_shift_all_over_the_place/
        if is_pitch_sensitive_audio and not is_paused:
            self._player.set_media(self._media)
            self._player.play()

        #self.set_player_time(round(frame * (1000 / gui.frame_rate)))
        self.set_position(frame / gui.frame_count)
        gui.update_progress(frame)                          # necessary while paused and for a snappier visual update
        gui.gifPlayer.gif.jumpToFrame(frame)

        # NOTE: setting `frame_override` here on videos can cause high-precision progress...
        # ...to desync by a few frames, but prevents extremely rare timing issues that...
        # ...stop the slider from updating to its new position. is this trade-off worth it?
        # NOTE: `frame_override` sets `add_to_progress_offset` to 0.1 if it's 0
        #       -> add 0.001 to `offset` to ensure it doesn't get ignored
        if settings.checkHighPrecisionProgress.isChecked() and not is_pitch_sensitive_audio:
            self.add_to_progress_offset = -0.075 if is_paused else offset + 0.001
        gui.frame_override = frame                          # ^ set offset BEHIND current time while paused. i don't understand why, but it helps


    def _get_tracks(self, get_description, raw: bool = False) -> tuple[int, str]:
        if raw:
            for id, title in get_description():
                yield id, title.decode()

        # VLC may add tags to track titles, like "Track 1 - [English]" -> try to detect and remove these
        else:
            for id, title in get_description():
                fake_tags = []
                parts = title.decode().split(' - ')
                title = parts[0]
                for tag in reversed(parts[1:]):
                    if fake_tags:                           # if we found a non-tag, don't look for tags before it in...
                        fake_tags.append(tag)               # ...the title, e.g. "Track 1 - [Don't Detect Me] - Yippee"
                        continue
                    tag = tag.strip()
                    if tag[0] != '[' or tag[-1] != ']':
                        fake_tags.append(tag)
                if fake_tags:                               # reapply all valid nontags
                    title = f'{title} - {" - ".join(reversed(fake_tags))}'
                yield id, title


    def add_audio_track(self, url: str, enable: bool = False) -> bool:
        if self._player.add_slave(1, url, enable) == 0:     # slaves can be subtitles (0) or audio (1)
            gui.log_on_statusbar_signal.emit(f'Audio file {url} added and enabled.')
            if settings.checkTextOnSubtitleAdded.isChecked():
                self.show_text('Audio file added and enabled')
            return True
        else:                                               # returns 0 on success
            gui.log_on_statusbar_signal.emit(f'Failed to add audio file {url} (VLC does not report specific errors for this).')
            if settings.checkTextOnSubtitleAdded.isChecked():
                self.show_text('Failed to add audio file')


    def add_subtitle_track(self, url: str, enable: bool = False) -> bool:
        if self._player.add_slave(0, url, enable) == 0:     # slaves can be subtitles (0) or audio (1)
            gui.log_on_statusbar_signal.emit(f'Subtitle file {url} added and enabled.')
            if settings.checkTextOnSubtitleAdded.isChecked():
                self.show_text('Subtitle file added and enabled')
            return True
        else:                                               # returns 0 on success
            gui.log_on_statusbar_signal.emit(f'Failed to add subtitle file {url} (VLC does not report specific errors for this).')
            if settings.checkTextOnSubtitleAdded.isChecked():
                self.show_text('Failed to add subtitle file')


    def set_text_position(self, button: QtW.QRadioButton):
        self._text_position = (                             # libVLC uses wacky position values, so map them accordingly
            5, 4, 6,
            1, 0, 2,
            9, 8, 10
        )[int(button.objectName()[17:]) - 1]
        self._player.video_set_marquee_int(vlc.VideoMarqueeOption.Position, self._text_position)


    def set_text_height(self, percent: int):
        self._text_height_percent = percent / 100
        new_size = int(gui.vheight * self._text_height_percent)
        self._player.video_set_marquee_int(vlc.VideoMarqueeOption.Size, new_size)


    def set_text_x(self, percent: float):
        self._text_x_percent = percent / 100
        new_x = int(gui.vheight * self._text_x_percent)     # offset is relative to media's height for both X and Y
        self._player.video_set_marquee_int(vlc.VideoMarqueeOption.X, new_x)


    def set_text_y(self, percent: float):
        self._text_y_percent = percent / 100
        new_y = int(gui.vheight * self._text_y_percent)     # offset is relative to media's height for both X and Y
        self._player.video_set_marquee_int(vlc.VideoMarqueeOption.Y, new_y)


    def set_text_opacity(self, percent: int):
        self._text_opacity = round(255 * (percent / 100))


    def show_text(self, text: str, timeout: int = 350, position: int = None):
        ''' Displays marquee `text` on the player, for `timeout` milliseconds at
            `position`: 0 (Center), 1 (Left), 2 (Right), 4 (Top), 5 (Top-Left),
            6 (Top-Right), 8 (Bottom), 9 (Bottom-Left), 10 (Bottom-Right)

            TODO: marquees are supposed to be chainable -> https://wiki.videolan.org/Documentation:Modules/marq/
            NOTE: vlc.py claims "Marquee requires '--sub-source marq' in the Instance() call" <- not true?
            NOTE: VLC supports %-strings: https://wiki.videolan.org/Documentation:Format_String/
                  Escape isolated % characters with %%. Use VideoMarqueeOption.Refresh to auto-update text on
                  an interval. See the bottom of vlc.py for an example implementation of an on-screen clock. '''
        if not settings.groupText.isChecked(): return       # marquees are completely disabled -> return

        try:
            if position is None:                            # reuse last position if needed
                position = self._text_position
            self.text = (text, timeout, position)           # self.text is read by text_fade_thread
            unique_settings = self.text != self.last_text
            self.last_text = self.text                      # TODO: calling show_text very rapidly results in no fading (text still goes away on time, though)
            self.text_fade_start_time = time.time() + settings.spinTextFadeDelay.value()            # TODO this doesn't look right at low non-zero values (<0.5)
            self._player.video_set_marquee_int(vlc.VideoMarqueeOption.Opacity, self._text_opacity)  # reset opacity to default (repetitive but sometimes necessary)

            if (timeout == 0 and not unique_settings) or not gui.video:
                return                                      # avoid repetitive + pointless calls
            if unique_settings:                                                                     # avoid repetitive set_xyz() calls
                self._player.video_set_marquee_int(vlc.VideoMarqueeOption.Position, position)
                self._player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, text)            # set new text
            if not self.text_fade_thread_open:
                Thread(target=self.text_fade_thread, daemon=True).start()
                self.text_fade_thread_open = True
        except:
            logger.warning(f'(!) Unexpected error while showing text overlay: {format_exc()}')


    def text_fade_thread(self):
        while self.enabled:
            now = time.time()
            fade_time = self.text[1] / 1000                 # self.text[1] = timeout
            if now >= self.text_fade_start_time and fade_time != 0:
                if now <= self.text_fade_start_time + fade_time:
                    alpha = (self.text_fade_start_time + fade_time - now) * (self._text_opacity / fade_time)
                    self._player.video_set_marquee_int(vlc.VideoMarqueeOption.Opacity, round(alpha))
                    time.sleep(0.005)
                else:                                       # if we just finished fading, make sure no text is visible
                    #self._player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, '')
                    self._player.video_set_marquee_int(vlc.VideoMarqueeOption.Opacity, 0)
                    self.text_fade_start_time = 9999999999  # set start_time to extreme number to stop the loop
            else:                                           # sleep less frequently if we're going to fade soon
                time.sleep(0.5 if self.text_fade_start_time - now < 1 else 0.025)

        self.text_fade_thread_open = False
        return logging.info('VLC player disabled. Ending text_fade thread.')


    def high_precision_slider_accuracy_thread(self):
        ''' A thread for monitoring the accuracy of `self.update_slider_thread`
            compared to the real-world time it's been active. Once per second,
            the current UI frame is compared to how many actual seconds it's
            been since play was last started/resumed as well as the frame it
            started from to see how far we've deviated from reality. The inter-
            frame delay (`self.delay`) is then adjusted using `self.ui_delay`
            speed up or slow down the UI so that it lines up exactly right, one
            second from now.

            If the UI desyncs by more than one second from actual time or more
            than two seconds from libVLC's native progress, the UI is reset.

            Accuracy loop loops indefinitely until `self.reset_progress_offset`
            is set to True, then it breaks from the loop and resets its values.

            HACK: `self.add_to_progress_offset` is a float added to the initial
            starting time in order to account for microbuffering within libVLC
            (which is NOT reported or detectable anywhere, seemingly). A better
            solution is needed, but I'm not sure one exists. Even libVLC's media
            stats (read_bytes, displayed_pictures, etc.) are updated at the same
            awful, inconsistent rate that its native progress is updated, making
            them essentially useless. At the very least, most mid-high range
            systems "buffer" at the same speed (~0.05-0.1 seconds, is that also
            partially tied to libVLC's update system?). Only low-end systems
            will fall slightly behind (but (probably) never desync). '''

        play_started = 0.0
        frame_started = 0
        current_frame = 0
        vlc_frame = 0.0
        seconds_elapsed = 0.0
        frames_elapsed = 0.0
        frame_desync = 0.0
        time_desync = 0.0
        vlc_desync = 0.0

        # re-define global aliases -> having them as locals is even faster
        _gui = gui
        get_ui_frame = _gui.sliderProgress.value
        is_playing = self.is_playing
        _sleep = time.sleep
        _get_time = time.time

        check_interval = 1
        intercheck_count = 20
        delay_per_intercheck = check_interval / intercheck_count
        vlc_desync_counter_limit = 2                    # how many times in a row VLC must be desynced before we care

        while self.enabled:
            # stay relatively idle while minimized, nothing is active, or we're waiting for something
            while not _gui.isVisible() and self.enabled:                  _sleep(0.25)
            while _gui.isVisible() and not is_playing() and self.enabled: _sleep(0.02)
            while _gui.open_in_progress or _gui.frame_override != -1:     _sleep(0.01)

            start = _get_time()
            play_started = start + self.add_to_progress_offset
            frame_started = get_ui_frame()
            self.reset_progress_offset = False
            self.add_to_progress_offset = 0.0
            vlc_desync_limit = _gui.frame_rate * 2
            vlc_desync_counter = 0

            while is_playing() and not self.reset_progress_offset and not _gui.open_in_progress:
                seconds_elapsed = (_get_time() - play_started) * _gui.playback_rate
                frames_elapsed = seconds_elapsed * _gui.frame_rate
                current_frame = get_ui_frame()
                vlc_frame = self.get_position() * _gui.frame_count
                frame_desync = current_frame - frames_elapsed - frame_started
                time_desync = frame_desync / _gui.frame_rate
                absolute_time_desync = abs(time_desync)
                vlc_desync = current_frame - vlc_frame

                # if we're greater than 1 second off our expected time or 2 seconds off VLC's time...
                # ...something is wrong -> reset to just past VLC's frame (VLC is usually a bit behind)
                # NOTE: VLC can be deceptive - only listen to VLC if it's been desynced for a while
                vlc_is_desynced = vlc_frame > 0 and abs(vlc_desync) > vlc_desync_limit
                if vlc_is_desynced: vlc_desync_counter += 1
                else:               vlc_desync_counter = 0
                if absolute_time_desync >= 1 or vlc_desync_counter >= vlc_desync_counter_limit:
                    self.ui_delay = _gui.delay
                    true_frame = (self.get_position() * _gui.frame_count) + (_gui.frame_rate * 0.2)
                    logging.info(f'(?) High-precision progress desync: {time_desync:.2f} real seconds, {vlc_desync:.2f} VLC frames. Changing frame from {current_frame} to {true_frame}.')

                    # double-check our conditions in case of extremely unlucky timing
                    if not is_playing() or self.reset_progress_offset or _gui.open_in_progress:
                        break

                    # if frame_override is already set, it will be resetting for us anyways
                    # don't break - just let things run their course
                    if _gui.frame_override == -1:
                        _gui.frame_override = int(true_frame)

                # otherwise, adjust delay accordingly to stay on track
                else:
                    if time_desync >= 0: self.ui_delay = _gui.delay * (1 + absolute_time_desync)    # we're ahead (need to slow down)
                    else:                self.ui_delay = _gui.delay / (1 + absolute_time_desync)    # we're behind (need to speed up)

                # TODO: have setting or debug command line argument that actually logs these every second?
                #logging.debug(f'VLC\'s frame: {vlc_frame:.1f}, Our frame: {current_frame} (difference of {vlc_desync:.1f} frames, or {vlc_desync / _gui.frame_rate:.2f} seconds)')
                #logging.debug(f'New delay: {self.ui_delay} (delta_frames={delta_frames:.1f}, delta_seconds={delta_seconds:2f})')

                # wait for next check, but account for the time it took to actually run through the loop
                time_elapsed = 0.0
                while time_elapsed < check_interval:
                    if not is_playing() or self.reset_progress_offset or _gui.open_in_progress:
                        break
                    _sleep(delay_per_intercheck)
                    time_elapsed = _get_time() - start
                start = _get_time()

        # all loops broken, player backend disabled
        self.metronome_thread_open = False
        return logging.info('VLC player disabled. Ending high_precision_slider_accuracy thread.')


    def update_slider_thread(self):
        ''' Handles updating the progress bar. This includes both slider-types
            and swapping between them. Set `_gui.frame_override` to override the
            next pending frame (preventing timing-related bugs). If set while
            `_gui.open_in_progress` is True, this thread halts before signalling
            `_gui._open_cleanup_slot()` once `self.open_cleanup_queued` is True,
            then halts again until the opening process is fully complete. While
            not playing, the slider is manually updated at 20fps to keep
            animations working smoothly without draining resources.
            While minimized, resource-usage is kept to a minimum. '''

        logging.info('Slider-updating thread started.')

        # re-define global aliases -> having them as locals is even faster
        _gui = gui
        get_ui_frame = _gui.sliderProgress.value
        repaint_slider = _gui.sliderProgress.update
        is_playing = self.is_playing
        is_high_precision = _gui.dialog_settings.checkHighPrecisionProgress.isChecked
        emit_open_cleanup_signal = _gui._open_cleanup_signal.emit
        _emit_update_progress_signal = _gui.update_progress_signal.emit
        _sleep = time.sleep
        _get_time = time.time

        # set the minimum fps the slider MUST update at to ensure...
        # ...animations tied to the slider continue to work (smoothly)
        # NOTE: this number must match the `fps` variable that...
        #       ...appears twice in `QVideoSlider.paintEvent()`
        min_fps = 20                                    # TODO this is applied even for non-fullscreen images
        min_fps_delay = 1 / min_fps

        while self.enabled:
            # window is NOT visible, stay relatively idle and do not update
            while not _gui.isVisible() and self.enabled:
                _sleep(0.25)

            # window is visible, but nothing is actively playing (NOTE: `is_playing()` will be False for images)
            while _gui.isVisible() and not is_playing() and self.enabled:
                repaint_slider()                        # force `QVideoSlider` to keep painting
                _sleep(min_fps_delay)                   # update at `min_fps`

            # reset queued slider-swap (or the slider won't update anymore after a swap)
            self.swap_slider_styles_queued = False

            # high-precision option enabled -> fake a smooth slider based on media's frame rate (simulates what libvlc SHOULD have)
            # TODO: for now, lets just force the VLC-progress for non-standard speeds
            if is_high_precision() and _gui.playback_rate == 1.0:
                start = _get_time()
                now = start
                min_fps_delay_threshold_factor = 2      # if we're too close to `min_fps_delay`, split up sleep this many times
                min_fps_delay_threshold = min_fps_delay * min_fps_delay_threshold_factor

                # playing, not buffering, not locked, and not about to swap styles
                while is_playing() and not _gui.lock_progress_updates and not self.swap_slider_styles_queued:
                    if _gui.frame_override != -1:
                        if _gui.open_in_progress:       # opening -> wait for signal to start cleanup
                            while _gui.open_in_progress and not self.open_cleanup_queued:
                                _sleep(0.01)
                            emit_open_cleanup_signal()  # _open_cleanup_signal uses _gui._open_cleanup_slot()
                            self.open_cleanup_queued = False
                            while _gui.open_in_progress and not self.open_cleanup_queued:
                                _sleep(0.01)            # wait for media opening to finish
                        else:
                            _emit_update_progress_signal(_gui.frame_override)
                        _gui.frame_override = -1        # reset frame_override

                        # force high-precision progress bar to reset its starting offset
                        if not self.add_to_progress_offset:
                            self.add_to_progress_offset = 0.1
                        self.reset_progress_offset = True

                    # (TODO: unfinished) no frame override -> increment `playback_rate` frames forward (i.e. at 1x speed -> 1 frame)
                    #elif (next_frame := get_ui_frame() + _gui.playback_rate) <= _gui.frame_count:   # do NOT update progress if we're at the end
                    elif (next_frame := get_ui_frame() + 1) <= _gui.frame_count:            # do NOT update progress if we're at the end
                        _emit_update_progress_signal(next_frame)                            # update_progress_signal -> _update_progress_slot

                    # low FPS media confuses the accuracy thread when switching media
                    # -> always update/repaint high-precision slider at >= `min_fps`
                    if _gui.frame_rate < min_fps:
                        try:
                            _sleep(0.0001)              # sleep to force-update get_time()
                            now = _get_time()
                            execution_time = now - start
                            time_elapsed = execution_time
                            while time_elapsed < self.ui_delay:
                                to_sleep = self.ui_delay - time_elapsed

                                # if we're too close to `min_delay`, split up sleep calls
                                # otherwise, sleep for whichever delay is smaller
                                if to_sleep > min_fps_delay:
                                    if to_sleep < min_fps_delay_threshold:
                                        _sleep(to_sleep / min_fps_delay_threshold_factor)
                                    else:
                                        _sleep(min_fps_delay)
                                else:
                                    _sleep(to_sleep)

                                # manually repaint slider to keep animations running smoothly
                                repaint_slider()

                                # check our conditions while we're awaiting the next frame
                                if not is_playing() or _gui.lock_progress_updates or self.swap_slider_styles_queued or _gui.frame_override != -1:
                                    break

                                now = _get_time()
                                time_elapsed = now - start
                        except Exception as error:
                            logging.warning(f'update_slider_thread bottleneck - {type(error)}: {error} -> delay={self.ui_delay} execution-time={_get_time() - start}')
                        finally:
                            start = now

                    # for normal FPS media, just sleep normally, accounting for the loop's execution time
                    else:
                        try:
                            _sleep(0.0001)              # sleep to force-update get_time()
                            _sleep(self.ui_delay - (_get_time() - start))
                        except Exception as error:
                            logging.warning(f'update_slider_thread bottleneck - {type(error)}: {error} -> delay={self.ui_delay} execution-time={_get_time() - start}')
                        finally:
                            start = _get_time()

            # high-precision option disabled -> use libvlc's native progress and manually paint QVideoSlider
            else:
                vlc_offset = _gui.frame_rate * 0.15     # VLC's progress is usually a bit behind, so use this to make sure we stay somewhat lined up with reality

                # not playing, not locked, and not about to swap styles
                while is_playing() and not _gui.lock_progress_updates and not self.swap_slider_styles_queued:
                    if _gui.frame_override != -1:
                        if _gui.open_in_progress:       # opening -> wait for signal to start cleanup
                            while _gui.open_in_progress and not self.open_cleanup_queued:
                                _sleep(0.01)
                            emit_open_cleanup_signal()  # _open_cleanup_signal uses _gui._open_cleanup_slot()
                            self.open_cleanup_queued = False
                            while _gui.open_in_progress and not self.open_cleanup_queued:
                                _sleep(0.01)            # wait for media opening to finish
                        else:
                            _emit_update_progress_signal(_gui.frame_override)
                        _gui.frame_override = -1        # reset frame_override

                        # force high-precision progress bar to reset its starting offset
                        if not self.add_to_progress_offset:
                            self.add_to_progress_offset = 0.1
                        self.reset_progress_offset = True

                    # no frame override -> set slider to VLC's progress if VLC has actually updated
                    else:
                        new_frame = (self.get_position() * _gui.frame_count) + vlc_offset   # convert VLC position to frame
                        if new_frame >= get_ui_frame():         # if progress is updated (and didn't go backwards), update UI
                            _emit_update_progress_signal(new_frame)
                        #else:                          # if VLC literally went backwards (common) -> simulate a non-backwards update
                        #    interpolated_frame = int(new_frame + (_gui.frame_rate / 5))
                        #    _emit_update_progress_signal(interpolated_frame)               # TODO can this snowball and keep jumping forward forever?

                        # NOTE: for some reason, putting this as an `else` above...
                        # ...just... doesn't work. it repaints very inconsistently
                        repaint_slider()                # manually repaint slider for various animations to work
                        _sleep(min_fps_delay)           # update position at 15FPS (every ~0.0667 seconds -> libvlc updates every ~0.2-0.35 seconds)

        # all loops broken, player backend disabled
        self.slider_thread_open = False
        return logging.info('VLC player disabled. Ending update_slider thread.')




class PlayerQt(PyPlayerBackend):
    ''' Two years later, I finally came back to finish this. It's hard to forget.
        I don't forget. What were we talking about? 3/1/22 - 3/9/24. '''

    __name__ = 'Qt'
    SUPPORTS_PARSING = True
    SUPPORTS_VIDEO_TRACK_MANIPULATION = False
    SUPPORTS_AUDIO_TRACK_MANIPULATION = False
    SUPPORTS_SUBTITLE_TRACK_MANIPULATION = False
    SUPPORTS_AUTOMATIC_SUBTITLE_ENABLING = False
    ENABLE_AUTOMATIC_TRACK_RESTORATION = False          # False because we don't support tracks in the first place
    ENABLE_AUTOMATIC_TRACK_RESET = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._metadata_available = False
        self._media_status = QtMultimedia.QMediaPlayer.MediaStatus.NoMedia
        self._null_media = QtMultimedia.QMediaContent()

        self._player: QtMultimedia.QMediaPlayer = None
        self._video_widget: QtMultimediaWidgets.QVideoWidget = None
        self.player_and_widget_paired = False

        self._frame_timer = QtCore.QTimer()
        self._frame_timer.timeout.connect(self._on_timer)
        self.ignore_zero_progress = False
        self.lock_timer = False

        # TODO: add this to menu
        #for key in player.availableMetaData():
        #    try: print(key, player.metaData(key))
        #    except: print(format_exc())


    def enable(self) -> bool:
        super().enable()

        # TODO: should we be reusing this instead of creating new ones? no, right?
        player = self._player = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)

        self.get_playback_rate = player.playbackRate
        self.set_playback_rate = player.setPlaybackRate
        self.get_position = lambda: (player.position() / 1000) / gui.duration
        self.set_position = lambda pos: player.setPosition(int((pos * gui.duration) * 1000))
        self.get_volume = player.volume
        self.set_volume = player.setVolume
        self.get_mute = player.isMuted
        self.set_mute = player.setMuted
        self.pause = lambda: player.pause() if player.state() == QtMultimedia.QMediaPlayer.PlayingState else player.play()
        self.set_pause = lambda paused: player.pause() if paused else player.play()
        self.stop = lambda: player.setMedia(self._null_media)   # NOTE: `player.stop()` does not actually release file locks
        self.is_parsed = lambda: self._metadata_available       # minor optimization (isMetaDataAvailable() is slightly more involved)
        self.is_playing = lambda: player.state() == QtMultimedia.QMediaPlayer.PlayingState
        self.get_fps = lambda: player.metaData('VideoFrameRate') or 0.0
        self.get_duration = lambda: player.duration() / 1000

        # signals (NOTE: `positionChanged`/`setNotifyInterval()` is not used...
        # ...since we need to consistently repaint the slider regardless)
        player.error.connect(self._on_error)
        player.metaDataAvailableChanged.connect(lambda available: setattr(self, '_metadata_available', available))
        player.mediaStatusChanged.connect(self._on_media_status_changed)

        # create video surface to render our media onto (multiple choices here)
        video_widget = self._video_widget = QtMultimediaWidgets.QVideoWidget(self.parent)
        video_widget.setAspectRatioMode(Qt.KeepAspectRatio)     # TODO make IgnoreAspectRatio a player-specific setting

        # QVideoWidget defaults to looking like a flashbang
        p = QtGui.QPalette()
        p.setColor(QtGui.QPalette.Window, Qt.transparent)
        video_widget.setPalette(p)
        video_widget.setAttribute(Qt.WA_OpaquePaintEvent, True)

        # QVideoWidget really loves eating mouse events no matter how hard you try to stop it
        video_widget.setMouseTracking(True)
        video_widget.mousePressEvent = self.parent.mousePressEvent
        video_widget.mouseMoveEvent = self.parent.mouseMoveEvent
        video_widget.mouseReleaseEvent = self.parent.mouseReleaseEvent
        video_widget.mouseDoubleClickEvent = self.parent.mouseDoubleClickEvent
        video_widget.wheelEvent = self.parent.wheelEvent
        video_widget.enterEvent = self.parent.enterEvent
        video_widget.leaveEvent = self.parent.leaveEvent

        # start ui-updating timer
        if gui.mime_type == 'image':
            interval = 50 if gui.isFullScreen() else 200        # update at 5fps for images (or 20fps if we're fullscreen)
        else:
            interval = max(17, min(50, gui.delay * 1000))       # clamp interval to 17-50ms (~59-20fps)
        self._frame_timer.start(interval)
        return True


    def disable(self, wait: bool = True):
        super().disable()
        self.player_and_widget_paired = False
        self._frame_timer.stop()
        self._player.deleteLater()
        self._video_widget.deleteLater()


    def show(self):
        if not self.player_and_widget_paired:
            self._player.setVideoOutput(self._video_widget)
            if gui.mime_type == 'video':
                self._video_widget.show()
            else:
                self._video_widget.hide()
            self.player_and_widget_paired = True
        self._video_widget.resize(self.parent.size())


    def _on_timer(self):
        ''' Qt event. '''
        if not gui.is_paused and not self.lock_timer:
            frame = round((self._player.position() / 1000) * gui.frame_rate)
            if frame:                                       # sometimes Qt will try to reset UI to 0 when we don't want it to
                gui.update_progress(frame)
                self.ignore_zero_progress = False           # reset flag now that Qt is reporting the correct progress
            elif not self.ignore_zero_progress:             # only allow a `frame` of 0 if we're not ignoring it
                gui.update_progress(0)
        else:                                               # continue painting hover timestamp/fullscreen UI while paused
            gui.sliderProgress.update()


    def _on_error(self, error: QtMultimedia.QMediaPlayer.Error):
        ''' Qt event. '''
        logger.error(f'(!) PlayerQt reported an error: {error}')
        if error == QtMultimedia.QMediaPlayer.Error.FormatError:
            gui.log_on_statusbar_signal.emit('(!) You do not have the proper codecs install to correctly play this file.')


    def _on_media_status_changed(self, status: QtMultimedia.QMediaPlayer.MediaStatus):
        ''' Qt event. '''
        logger.debug(f'Media status changed to {status} (restarted={gui.restarted}, ui_frame={gui.sliderProgress.value()})')

        # HACK: QMediaPlayer likes to just... go longer than the video? like the frame it reports is often...
        # ...impossible, so to ensure that the frame doesn't visually change when we're restarting...
        # ...(QMediaPlayer resets to frame 0 on media finish), we set the progress to 200%
        # TODO: this unfortunately has HORRIBLE side effects when resizing. we can go over 100%...
        # ...progress, as long as it conforms to whatever fake frame Qt thinks the media can go...
        # ...to, but I have no idea how to determine this value
        if status == QtMultimedia.QMediaPlayer.MediaStatus.BufferedMedia and gui.restarted:
            self.set_and_update_progress(gui.frame_count * 2)
        elif status == QtMultimedia.QMediaPlayer.MediaStatus.EndOfMedia and not gui.is_paused and not gui.restarted:
            self._media_status = QtMultimedia.QMediaPlayer.MediaStatus.LoadingMedia
            gui.restart_signal.emit()
        else:
            self._media_status = status


    def on_resize(self, event: QtGui.QResizeEvent):
        self._video_widget.resize(event.size())
        #self._video_widget.resize(1920, 1080)              # TODO this can be used for video zooming


    def on_fullscreen(self, fullscreen: bool):
        if gui.mime_type == 'image':                        # use 20fps for images in fullscreen
            self._frame_timer.setInterval(50 if fullscreen else 200)


    def on_parse(self, file: str, base_mime: str, mime: str, extension: str):
        if mime == 'video':
            self._video_widget.show()
        else:
            self._video_widget.hide()

        if mime == 'image':
            self.lock_timer = True
            interval = 50 if gui.isFullScreen() else 200    # update at 5fps for images (or 20fps if we're fullscreen)
        else:
            self.lock_timer = False
            interval = max(17, min(50, gui.delay * 1000))   # clamp interval to 17-50ms (~59-20fps)

        gui._open_cleanup_signal.emit()
        self._frame_timer.setInterval(interval)
        logger.info(f'PlayerQt timer set to {interval:.2f}ms')


    def on_restart(self):
        ''' Called in `gui.restart()`, immediately after confirming the restart
            is valid. `gui.restarted` will be False. After this event, the UI
            be updated and the player will be force-paused. This event should
            do any extraneous cleanup that must be urgently completed to ensure
            finished media is immediately/seamlessly ready to play again. '''
        frame = gui.sliderProgress.value()
        #if frame == gui.frame_count:
        #    #frame = int((self._player.position() / 1000) * gui.frame_rate)
        #    frame = int((self._player.position() / 1000) * self._player.metaData('VideoFrameRate'))
        self.play(gui.video, will_restore=True)             # Qt will report the frame as 0 for a bit -> ignore this
        self.set_and_update_progress(frame, SetProgressContext.RESTART)


    def play(self, file: str, will_restore: bool = False, _error: bool = False):
        try:
            self.ignore_zero_progress = will_restore
            self._player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file)))
            self._player.play()
            self.file_being_opened = file
            return True
        except:
            logger.warning(f'QMediaPlayer failed to play video {file}: {format_exc()}')
            if not _error:                                  # `_error` ensures we only attempt to play previous video once
                if not gui.video: self._player.stop()       # no previous video to play, so just stop playing
                else: self.play(gui.video, _error=True)     # attempt to play previous working video
            return False


    def get_state(self):
        if self._media_status == QtMultimedia.QMediaPlayer.EndOfMedia:
            return State.Ended
        return {
            QtMultimedia.QMediaPlayer.PlayingState: State.Playing,
            QtMultimedia.QMediaPlayer.PausedState:  State.Paused,
            QtMultimedia.QMediaPlayer.StoppedState: State.Stopped,
        }.get(self._player.state(), State.Playing)


    def get_dimensions(self) -> tuple[int, int]:            # it's okay if we throw an exception here
        size: QtCore.QSize = self._player.metaData('Resolution') or self._video_player.sizeHint()
        return size.width(), size.height()


    def set_and_update_progress(self, frame: int = 0, context: int = SetProgressContext.NONE):
        # don't touch progress if we're currently opening a file
        if gui.open_in_progress:
            return

        if context == SetProgressContext.NAVIGATION_RELATIVE:
            self.lock_timer = True
            gui.update_progress(frame)
            self._player.setPosition(int((frame / gui.frame_rate) * 1000))
            self.lock_timer = False
        else:
            self._player.setPosition(int((frame / gui.frame_rate) * 1000))
            gui.update_progress(frame)
            if context == SetProgressContext.RESTORE:       # HACK: this helps fix flickering on the slider when switching from a...
                gui.frame_override = frame                  # ...player that uses `update_progress_signal`, but otherwise does nothing
        gui.gifPlayer.gif.jumpToFrame(frame)




class QVideoPlayer(QtW.QWidget):    # https://python-camelot.s3.amazonaws.com/gpl/release/pyqt/doc/advanced/development.html <- relevant?
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAttribute(Qt.WA_StyledBackground, True)     # https://stackoverflow.com/questions/7276330/qt-stylesheet-for-custom-widget
        self.setToolTipDuration(2000)
        self.setMouseTracking(True)                         # required for detecting idle movement
        self.setMinimumHeight(10)

        self.player = PyPlayerBackend(self)                 # NOTE: this is set purely so we can set global aliases in `main.pyw`
        self.players: dict[str, PyPlayerBackend] = {}

        self.idle_timeout_time = 0.0
        self.last_invalid_snap_state_time = 0.0
        self.dragdrop_in_progress = False
        self.dragdrop_last_modifiers = None
        self.dragdrop_subtitle_count = 0
        self.dragdrop_is_folder = False
        self.dragdrop_files = []

        self.dragging: int = None                           # NOTE: 0 is valid -> always check against None
        self.dragging_offset: QtCore.QPoint = None
        self.drag_axis_lock: int = None
        self.panning = False
        self.true_left = 100
        self.true_right = 250
        self.true_top = 100
        self.true_bottom = 250
        self.true_rect: QtCore.QRect = None

        self.selection: list[QtCore.QPoint] = None
        self.last_factored_points: list[QtCore.QPoint] = None
        self.crop_frames: list[QtW.QFrame] = None
        self.crop_rect: QtCore.QRect = None
        self.reference_example: dict[int, dict[int]] = None
        self.text_y_offsets: dict[int, int] = None
        self.cursors = {
            0: QtGui.QCursor(Qt.SizeFDiagCursor),
            1: QtGui.QCursor(Qt.SizeBDiagCursor),
            2: QtGui.QCursor(Qt.SizeBDiagCursor),
            3: QtGui.QCursor(Qt.SizeFDiagCursor)
        }


    def reset_dragdrop_status(self):
        ''' Quickly clears drag-and-drop related messages and properties. '''
        gui.statusbar.clearMessage()
        self.player.show_text('')
        self.dragdrop_last_modifiers = None
        self.dragdrop_in_progress = False


    # ---------------------
    # Cropping Utilities
    # ---------------------
    def get_crop_point_index_in_range(self, pos: QtCore.QPoint, _range: int = 30) -> int:
        ''' Returns the index of the closest crop-corner to `pos`,
            if any are within `_range` pixels, otherwise None. '''
        min_dist = 1000
        min_point = None
        for point in self.selection:
            #dist = abs(pos.x() - point.x()) + abs(pos.y() - point.y())     # TODO: verify that manhattanLength is actually better than this
            dist = (pos - point).manhattanLength()          # https://doc.qt.io/qt-5/qpoint.html#manhattanLength
            if dist < min_dist:
                min_dist = dist
                min_point = point
        return None if min_dist > _range else self.selection.index(min_point)


    def get_crop_edge_index_in_range(self, pos: QtCore.QPoint, _range: int = 15) -> int:
        ''' Returns the index of the closest crop-edge to `pos`, if
            any are within `_range` pixels, otherwise None. Indexes:
            Left: 0, Top: 1, Right: 2, Bottom: 3. '''
        s = self.selection
        for index in range(2):  # 0, 1
            if s[index].x() - _range <= pos.x() <= s[index].x() + _range and s[index].y() < pos.y() < s[(index + 2) % 4].y():
                return 0 if index == 0 else 2               # hovering over left edge if index == 0, else right edge
            elif s[index * 2].y() - _range <= pos.y() <= s[index * 2].y() + _range and s[index * 2].x() < pos.x() < s[(index * 2) + 1].x():
                return 1 if index == 0 else 3               # hovering over top edge if index == 0, else bottom edge
        return None


    def correct_points(self, changed_point_index: int):
        reference_point = self.selection[changed_point_index]
        x, y = reference_point.x(), reference_point.y()
        corrective_functions = self.reference_example[changed_point_index]
        for index, point in enumerate(self.selection):
            if index in corrective_functions:                                           # only 3/4 points are in each reference_example
                corrective_functions[index](x, y)                                       # run reference_example corrective function
                point.setX(min(self.true_right, max(self.true_left, point.x())))        # clamp each point to true borders
                point.setY(min(self.true_bottom, max(self.true_top, point.y())))        # true_bottom > true_top
                #self.selection[self.dragging].setX(min(self.true_right, max(self.true_left, point.x())))
                #self.selection[self.dragging].setY(min(self.true_bottom, max(self.true_top, point.y())))        # true_bottom > true_top
                #print('true borders (lrtb):', self.true_left, self.true_right, self.true_top, self.true_bottom, '| points:', point.x(), point.y(), f'| widget size: {self.width()}x{self.height()}')


    def factor_point(self, pos: QtCore.QPoint) -> QtCore.QPointF:
        ''' Converts a `QPoint` (`pos`) relative to `QVideoPlayer`'s viewport to
            a corresponding `QPointF` relative to the media's native resolution
            using the factor between the two. libVLC seemingly chooses to not
            expose these values, so we must calculate them manually. '''
        w = self.width()
        h = self.height()
        vw = gui.vwidth
        vh = gui.vheight
        ratio = vw / vh                     # native aspect ratio
        widget_ratio = w / h                # aspect ratio of QVideoPlayer
        if widget_ratio < ratio:            # video fills viewport width (there are black bars top/bottom)
            factor = vw / w
            void = ((h * factor) - vh) / 2  # calculate size of black bars
            x = pos.x() * factor
            y = (pos.y() * factor) - void   # account for black bars
            y = max(0, min(y, vh))          # I don't remember why this is needed
        else:                               # video fills viewport height (there are black bars left/right)
            factor = vh / h
            void = ((w * factor) - vw) / 2  # calculate size of black bars
            x = (pos.x() * factor) - void   # account for black bars
            y = pos.y() * factor
            x = max(0, min(x, vw))          # I don't remember why this is needed
        #print(f'factored pos ({pos.x()}, {pos.y()}) to ({x}, {y}) -> ratio={ratio} widget_ratio={widget_ratio} w={w} h={h} vw={vw} vh={vh} factor={factor} void={void}')
        return QtCore.QPointF(x, y)


    def defactor_point(self, pos: QtCore.QPointF) -> QtCore.QPoint:
        ''' The opposite of `self.factor_point()`: converts a `QPointF`
            (`pos`) relative to the media's native resolution to a
            corresponding `QPoint` relative to `QVideoPlayer`'s viewport. '''
        w = self.width()
        h = self.height()
        vw = gui.vwidth
        vh = gui.vheight
        ratio = vw / vh
        widget_ratio = w / h
        if widget_ratio < ratio:                            # video fills viewport width (there are black bars top/bottom)
            factor = vw / w
            void = ((h * factor) - vh) / 2                  # ((h - (w / video_ratio)) / 2)
            x = pos.x() / factor
            y = (pos.y() + void) / factor
            y = max(0, min(y, h))
        else:                                               # video fills viewport height (there are black bars left/right)
            factor = vh / h
            void = ((w * factor) - vw) / 2
            x = (pos.x() + void) / factor
            y = pos.y() / factor
            x = max(0, min(x, w))
        #print(f'de-factored pos ({pos.x()}, {pos.y()}) to ({x}, {y}) -> ratio={ratio} widget_ratio={widget_ratio} w={w} h={h} vw={vw} vh={vh} factor={factor} void={void}')
        return QtCore.QPoint(x, y)


    def find_true_borders(self):
        ''' Updates `self.true_rect` with a `QRect` containing the corners
            of the media's actual resolution within `QVideoPlayer`'s viewport.
            Also updates `self.true_{left/right/top/bottom}`. Similar to
            `self.factor_point()`/`self.defactor_point()`. I don't remember why,
            but a different calculation for the black bar was required here. '''
        w = self.width()
        h = self.height()

        # TODO which one is faster, vsize version or commented-out version? is having vsize JUST for this worth it?
        #vw = gui.vwidth
        #vh = gui.vheight
        #video_ratio = vw / vh                              # vh is never 0 (handled in gui.open())
        #widget_ratio = w / h
        #if widget_ratio < video_ratio:                     # video fills viewport width (there are black bars top/bottom)

        try:
            #if gui.gifPlayer._baseZoom == 1.0:
            #    expected_size = gui.vsize
            #    hvoid = (h - expected_size.height()) / 2
            #    wvoid = (w - expected_size.width()) / 2
            #    self.true_left =   int(wvoid)               # ensure potential error is outside bounds of actual video size
            #    self.true_right =  math.ceil(w - wvoid)     # ensure potential error is outside bounds of actual video size
            #    self.true_top =    int(hvoid)               # ensure potential error is outside bounds of actual video size
            #    self.true_bottom = math.ceil(h - hvoid)     # ensure potential error is outside bounds of actual video size
            #else:

            expected_size = gui.vsize.scaled(self.size(), Qt.KeepAspectRatio)
            if expected_size.height() < h:                  # video fills viewport width (there are black bars top/bottom)
                logger.debug('Video fills viewport width (there are black bars top/bottom)')
                #void = ((h - (w / video_ratio)) / 2)
                void = (h - expected_size.height()) / 2
                self.true_left =   0
                self.true_right =  w
                self.true_top =    int(void)                # ensure potential error is outside bounds of actual video size
                self.true_bottom = math.ceil(h - void)      # ensure potential error is outside bounds of actual video size
            else:                                           # video fills viewport height (there are black bars left/right)
                logger.debug('Video fills viewport height (there are black bars left/right)')
                #void = ((w - (h * video_ratio)) / 2)
                void = (w - expected_size.width()) / 2
                self.true_left =   int(void)                # ensure potential error is outside bounds of actual video size
                self.true_right =  math.ceil(w - void)      # ensure potential error is outside bounds of actual video size
                self.true_top =    0
                self.true_bottom = h

            logger.debug(f'void={void} w={w} h={h} expected_size={expected_size}')
            self.true_rect = QtCore.QRect(QtCore.QPoint(self.true_left, self.true_top), QtCore.QPoint(self.true_right, self.true_bottom))
        except:
            logger.debug(f'(!) find_true_borders failed: {format_exc()}')


    def update_crop_frames(self):
        ''' Updates the geometry for the four `QFrame`'s representing cropped
            out region. Updates the crop info panel accordingly. Saves current
            set of factored points for later use. '''
        selection = self.selection
        crop_top =    selection[0].y()                      # TODO make these @property?
        crop_left =   selection[0].x()
        crop_right =  selection[3].x()
        crop_bottom = selection[3].y()
        crop_height = crop_bottom - crop_top
        w = self.width()

        crop_frames = self.crop_frames
        crop_frames[0].setGeometry(0, 0, w, max(0, crop_top))                          # 0 top rectangle (full width)
        crop_frames[1].setGeometry(0, crop_top, crop_left, crop_height)                # 1 left rectangle
        crop_frames[2].setGeometry(crop_right, crop_top, w - crop_right, crop_height)  # 2 right rectangle
        crop_frames[3].setGeometry(0, crop_bottom, w, self.height() - crop_bottom)     # 3 bottom rectangle (full width)

        lfp = self.last_factored_points
        #if gui.gifPlayer._baseZoom == 1:
        #    lfp[0] = selection[0]
        #    lfp[1] = selection[1]
        #    lfp[2] = selection[2]
        #    lfp[3] = selection[3]
        #else:
        factor_point = self.factor_point
        lfp[0] = factor_point(selection[0])
        lfp[1] = factor_point(selection[1])
        lfp[2] = factor_point(selection[2])
        lfp[3] = factor_point(selection[3])

        # set crop info panel's strings
        gui.labelCropSize.setText(f'{lfp[1].x() - lfp[0].x():.0f}x{lfp[2].y() - lfp[0].y():.0f}')
        gui.labelCropTop.setText(f'T: {lfp[0].y():.0f}')
        gui.labelCropLeft.setText(f'L: {lfp[0].x():.0f}')
        gui.labelCropRight.setText(f'R: {lfp[3].x():.0f}')
        gui.labelCropBottom.setText(f'B: {lfp[3].y():.0f}')


    def refresh_crop_cursor(self, pos: QtCore.QPoint):
        ''' Updates the cursor to an appropriate resize/grab cursor
            based on its `pos` relative to the current crop region. '''
        cursor = app.overrideCursor()
        crop_point_index = self.get_crop_point_index_in_range(pos)
        edge_index = self.get_crop_edge_index_in_range(pos)
        if crop_point_index is not None:        # https://doc.qt.io/qt-5/qguiapplication.html#overrideCursor
            if cursor:     app.changeOverrideCursor(self.cursors[crop_point_index])
            else:          app.setOverrideCursor(self.cursors[crop_point_index])
        elif edge_index is not None:
            if edge_index % 2 == 0:
                if cursor: app.changeOverrideCursor(Qt.SizeHorCursor)
                else:      app.setOverrideCursor(Qt.SizeHorCursor)
            else:
                if cursor: app.changeOverrideCursor(Qt.SizeVerCursor)
                else:      app.setOverrideCursor(Qt.SizeVerCursor)
        elif self.crop_rect.contains(pos):
            if cursor:     app.changeOverrideCursor(Qt.SizeAllCursor)
            else:          app.setOverrideCursor(Qt.SizeAllCursor)
        elif cursor:
            app.restoreOverrideCursor()
            while app.overrideCursor():
                app.restoreOverrideCursor()


    # ---------------------
    # Events
    # ---------------------
    def paintEvent(self, event: QtGui.QPaintEvent):
        #super().paintEvent(event)                          # TODO this line isn't actually needed?
        if not gui.actionCrop.isChecked(): return           # nothing else to paint if we're not cropping

        s = self.selection
        white = QtGui.QColor(255, 255, 255)
        black = QtGui.QColor(0, 0, 0)

        p = QtGui.QPainter()
        p.begin(self)
        p.setPen(QtGui.QPen(white, 6, Qt.SolidLine))
        p.setBrush(white)
        p.setFont(QtGui.QFont('Segoe UI Light', 10))

        try:
            # draw thin border around video (+2 and -4 to account for size-6 pen)
            p.drawRect(s[0].x() + 2,
                       s[0].y() + 2,
                       s[1].x() - s[0].x() - 4,
                       s[2].y() - s[0].y() - 4)

            # draw handle and coordinates for each corner
            for index, point in enumerate(s):
                #p.drawRect(point.x() - 3, point.y() - 3, 5, 5)
                text = f'({self.last_factored_points[index].x():.0f}, {self.last_factored_points[index].y():.0f})'
                p.setPen(black)                                                              # set color to black
                p.drawText(point.x() + 1, point.y() + self.text_y_offsets[index] + 1, text)  # draw shadow first
                p.setPen(QtGui.QPen(white, 6, Qt.SolidLine))                                 # set color to white
                p.drawText(point.x(), point.y() + self.text_y_offsets[index], text)          # draw actual text over shadow
                p.drawPoint(point.x(), point.y())                                            # size-6 point to represent handles

        except: logger.warning(f'(!) Unexpected error while painting crop view from QVideoPlayer: {format_exc()}')
        finally: p.end()


    def resizeEvent(self, event: QtGui.QResizeEvent):
        ''' Recalculates borders and crop points while resizing if crop-mode
            is enabled. Also sets a timer for snapping the window to the
            current media's aspect ratio, as long as a timer isn't already
            active, snap-mode is enabled, we haven't recently altered the UI/
            maximized/fullscreened, and a file has already been loaded. '''
        if gui.actionCrop.isChecked():
            self.find_true_borders()
            #self.selection = [self.defactor_point(p) for p in self.last_factored_points]    # this should work but has bizarre side effects
            for index in range(4):
                self.correct_points(index)
            self.update_crop_frames()
        super().resizeEvent(event)

        # mark if we were recently fullscreen/maximized so we know not to snap-resize during the next few resizeEvents
        if gui.isMaximized() or gui.isFullScreen():
            self.last_invalid_snap_state_time = time.time()

        # set timer to resize window to fit player (if no file has been played yet, do not set timers on resize)
        # TODO: this does not work correctly on Linux!!! see `gui.timerEvent()` for more details
        elif (
            not gui.timer_id_resize_snap
            and time.time() - self.last_invalid_snap_state_time > 0.35
            and gui.first_video_fully_loaded
        ):
            gui.timer_id_resize_snap = gui.startTimer(200, Qt.CoarseTimer)

        self.player.on_resize(event)


    def mousePressEvent(self, event: QtGui.QMouseEvent):
        ''' Handles grabbing crop points/edges in crop-mode. Moves through the
            recent files list if the forwards/backwards buttons are pressed. '''
        try:
            if not gui.actionCrop.isChecked():                          # no crop -> check for back/forward buttons
                if event.button() == Qt.BackButton:      gui.cycle_recent_files(forward=False)
                elif event.button() == Qt.ForwardButton: gui.cycle_recent_files(forward=True)
                elif event.button() == Qt.MiddleButton:  gui.middle_click_player_actions[settings.comboPlayerMiddleClick.currentIndex()]()
                return  # TODO add back/forward functionality globally (not as easy as it sounds?)
            elif not event.button() == Qt.LeftButton:                   # ignore non-left-clicks in crop mode
                pos = self.mapFromGlobal(QtGui.QCursor.pos())
                return self.refresh_crop_cursor(pos)

            pos = self.mapFromGlobal(QtGui.QCursor.pos())               # mousePressEvent's event.pos() appears to return incorrect values...
            self.refresh_crop_cursor(pos)                               # ...in certain areas, leading to bad offsets and mismatched selections
            self.dragging = self.get_crop_point_index_in_range(pos)
            self.panning = False
            if self.dragging is not None:
                self.drag_axis_lock = None                              # reset axis lock before dragging corners
                self.dragging_offset = pos - self.selection[self.dragging]
            else:
                edge_index = self.get_crop_edge_index_in_range(pos)
                if edge_index is not None:
                    if edge_index % 2 == 0:
                        self.dragging = 0 if edge_index < 2 else 3
                        self.drag_axis_lock = 0
                    else:
                        self.dragging = 0 if edge_index < 2 else 3
                        self.drag_axis_lock = 1
                    self.dragging_offset = pos - self.selection[self.dragging]
                elif self.crop_rect.contains(pos):      # no corners/edges, but clicked inside crop rect -> panning
                    self.dragging = -1
                    self.drag_axis_lock = None          # reset axis lock before panning
                    self.dragging_offset = pos - self.selection[0]
                    if app.overrideCursor(): app.changeOverrideCursor(Qt.ClosedHandCursor)
                    else:                    app.setOverrideCursor(Qt.ClosedHandCursor)
            event.accept()
            self.update()
        except:
            logger.warning(f'(!) Unexpected error while clicking QVideoPlayer: {format_exc()}')
        return super().mousePressEvent(event)


    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        ''' Handles mouse movement over the player by resetting the idle timer
            if crop mode is disabled, or by allowing crop edges/corners (or the
            entire region) to be dragged around if crop mode is enabled. '''
        if not gui.actionCrop.isChecked():              # idle timeout is handled in QVideoSlider's paintEvent since it constantly updates
            if settings.checkHideIdleCursor.isChecked() and gui.video:
                self.idle_timeout_time = time.time() + settings.spinHideIdleCursorDuration.value()
            else:
                self.idle_timeout_time = 0.0            # 0 locks the cursor/UI
            return event.ignore()                       # only handle idle timeouts if we're not cropping

        # crop mode enabled -> lock UI and handle dragging and/or crop-cursor
        self.idle_timeout_time = 0.0
        try:
            pos = self.mapFromGlobal(event.globalPos())  # event.pos() does not work. I have no explanation.
            if self.dragging is None:
                self.refresh_crop_cursor(pos)

            elif event.buttons() == Qt.LeftButton:
                s = self.selection
                if self.drag_axis_lock is None: new_pos = pos - self.dragging_offset
                elif self.drag_axis_lock == 0:  new_pos = QtCore.QPoint((pos - self.dragging_offset).x(), s[self.dragging].y())  # x-axis only
                else:                           new_pos = QtCore.QPoint(s[self.dragging].x(), (pos - self.dragging_offset).y())  # y-axis only
                new_pos.setX(min(self.true_right, max(self.true_left, new_pos.x())))
                new_pos.setY(min(self.true_bottom, max(self.true_top, new_pos.y())))

                # we are panning the entire crop area
                if self.dragging == -1:
                    delta = new_pos - s[0]
                    for point in s:
                        point += delta

                    if not self.true_rect.contains(s[3]):
                        up =   QtCore.QPoint(0, 1)
                        left = QtCore.QPoint(1, 0)
                        while s[3].y() > self.true_bottom:
                            for point in s: point -= up
                        while s[3].x() > self.true_right:
                            for point in s: point -= left
                    self.panning = True                 # indicate that we're panning so we don't pause on release

                # we are dragging a corner/edge
                else:
                    # holding ctrl -> maintain square crop region
                    if app.keyboardModifiers() & Qt.ControlModifier:    # TODO this barely works, but it works. for now
                        self.dragging = 0                               # TODO bandaid fix so I don't have to finish all 4 points
                        new_x = new_pos.x()
                        anchor_index = (self.dragging + 1) % 4
                        anchor = s[anchor_index]
                        dragged = s[self.dragging]
                        if self.dragging % 2 == 0:
                            new_y = dragged.y() + (new_x - dragged.x())
                            dragged.setY(new_y)
                            height = s[(self.dragging + 2) % 4].y() - dragged.y()
                            anchor.setX(new_x + height)  # new_x - height is close to making indexes 1/3 work
                        else:
                            new_y = dragged.y() - (new_x - dragged.x())
                            dragged.setY(new_y)
                            height = s[(self.dragging + 2) % 4].y() - dragged.y()
                            anchor.setX(new_x - height)  # new_x - height is close to making indexes 1/3 work
                        ##dragged.setY(anchor.x() - dragged.x())
                        dragged.setX(new_x)
                        #dragged.setY(new_x)
                        #anchor.setX(anchor.x() - (anchor.x() - dragged.x()))
                        #height = s[(self.dragging + 2) % 4].y() - dragged.y()
                        #anchor.setX(new_x + height)    # new_x - height is close to making indexes 1/3 work
                        self.correct_points(self.dragging)
                        self.correct_points(anchor_index)
                    else:
                        s[self.dragging] = new_pos
                        self.correct_points(self.dragging)

                self.crop_rect.setTopLeft(s[0])
                self.crop_rect.setBottomRight(s[3])

                self.update_crop_frames()               # update crop frames and factored points
                self.repaint()                          # repaint QVideoPlayer (TODO: update() vs repaint() here)

        except TypeError: pass                          # self.dragging is None
        except: logger.warning(f'(!) Unexpected error while dragging crop points: {format_exc()}')
        #return super().mouseMoveEvent(event)           # TODO: required for mouseReleaseEvent to work properly?


    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        ''' Pauses media after clicking and releasing left-click over player,
            ignoring clicks that were dragged outside player. Releases dragged
            crop points/edges if needed, and resets cursor. '''

        # ensure we're actually over the player still and we're not panning/dragging a crop region
        if event.button() == Qt.LeftButton and self.rect().contains(event.pos()) and not self.panning:
            if (self.dragging is None and not gui.actionCrop.isChecked()) or self.dragging == -1:
                gui.pause()

        # right-click released -> prepare cursor/properties for context menu if necessary
        if event.button() == Qt.RightButton:
            # NOTE: this event happens before contextMenuEvent, which might not fire at all.
            # -> use a timer so contextMenuEvent has a chance to see the flag is set while...
            # ...guaranteeing the flag gets reset even if contextMenuEvent never fires
            if gui.ignore_next_right_click:             # not actually opening context menu
                def reset():
                    gui.ignore_next_right_click = False
                QtCore.QTimer.singleShot(50, Qt.CoarseTimer, reset)
            else:
                self.setCursor(Qt.ArrowCursor)          # HACK: reset base cursor as well to...
                self.unsetCursor()                      # ...fix obscure drag-and-drop cursor bugs
                while app.overrideCursor():
                    app.restoreOverrideCursor()

        # left-click released and we're not dragging the crop region/points/edges
        elif self.dragging is not None:                 # refresh crop cursor if we were just dragging
            self.refresh_crop_cursor(self.mapFromGlobal(event.globalPos()))

        #self.panning = False
        self.dragging = None                            # release crop-drag


    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        ''' Triggers user's desired double-click
            action after double-clicking the player. '''
        if event.button() == Qt.LeftButton:
            index = settings.comboPlayerDoubleClick.currentIndex()
            gui.double_click_player_actions[index]()


    def leaveEvent(self, event: QtCore.QEvent):
        ''' Automatically stop dragging, reset the cursor, and
            lock the cursor/UI when the mouse leaves the player. '''
        self.idle_timeout_time = 0.0                    # 0 locks the cursor/UI

        # HACK: set base cursors for the widgets above/below the player...
        # ...to fix various obscure cursor bugs related to drag-and-drop
        gui.dockControls.setCursor(Qt.ArrowCursor)      # (these are unset in their `enterEvent`s)
        gui.menubar.setCursor(Qt.ArrowCursor)

        # if cropping & the mouse is still over the player but NOT the controls (in fullscreen),...
        # ...don't reset cursor (the player AND each crop frame trigger their own `leaveEvent`'s)
        should_reset = True
        if gui.actionCrop.isChecked():
            mouse_pos = QtGui.QCursor().pos()
            if self.rect().contains(self.mapFromGlobal(mouse_pos)):
                control_pos = gui.dockControls.mapFromGlobal(mouse_pos)
                if not gui.dockControls.rect().contains(control_pos):
                    should_reset = False

        # we did not meet the specific scenario above
        if should_reset:
            while app.overrideCursor():                 # reset cursor to default
                app.restoreOverrideCursor()

        self.dragging = None                            # release crop-drag
        #print('setting panning to true', event.buttons())
        #self.panning = True  # TODO this is a bandaid fix. dragging/panning sometimes wrongly report as None and False, causing unexpected pauses in mouseReleaseEvent


    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        ''' Accepts a cursor-drag if files are being dragged.
            NOTE: Requires `self.setAcceptDrops(True)`. '''
        if event.mimeData().hasUrls(): event.accept()
        else: event.ignore()
        self.dragdrop_in_progress = True
        self.dragdrop_subtitle_count = 0
        self.dragdrop_is_folder = False

        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.dragdrop_files = files
        for file in files:
            if os.path.splitext(file)[-1] in constants.SUBTITLE_EXTENSIONS:
                self.dragdrop_subtitle_count += 1
            elif os.path.isdir(file):
                self.dragdrop_is_folder = True
                break

        return super().dragEnterEvent(event)            # run QWidget's built-in behavior


    def dragLeaveEvent(self, event: QtGui.QDragLeaveEvent):
        ''' Resets drag-and-drop status if user drags
            cursor off the window (to clear messages). '''
        self.reset_dragdrop_status()
        return super().dragLeaveEvent(event)


    def dragMoveEvent(self, event: QtGui.QDragMoveEvent):
        ''' Indicates on the statusbar and player (if possible) what the current
            button-combination will do once the drag-and-drop finishes. Keeps
            track of combination to avoid repeated statusbar/marquee calls. '''
        files = self.dragdrop_files

        if self.dragdrop_is_folder:
            mod = event.keyboardModifiers()
            if mod != self.dragdrop_last_modifiers:     # VVV alt OR ctrl+shift (play random file without autoplay)
                if mod & Qt.AltModifier or (mod & Qt.ControlModifier and mod & Qt.ShiftModifier):
                    msg = 'Drop to select random media from folder (without shuffle mode)'
                elif mod & Qt.ControlModifier:          # ctrl only (play random file with autoplay (in shuffle mode))
                    msg = 'Drop to select random media from folder (with shuffle mode)'
                elif mod & Qt.ShiftModifier:            # shift only (play first file without autoplay)
                    msg = 'Drop to select first media file in folder (without autoplay)'
                else:                                   # no modifiers (play first file with autoplay)
                    msg = 'Drop to autoplay folder contents, or hold ctrl/alt/shift for more options'
            gui.statusbar.showMessage(msg, 0)
            self.player.show_text(msg, timeout=0, position=0)
        elif self.dragdrop_subtitle_count:
            count = self.dragdrop_subtitle_count
            if count == len(files):
                if gui.video:
                    if count == 1: msg = 'Drop to add subtitle file'
                    else:          msg = 'Drop to add subtitle files'
                else:
                    msg = 'You cannot drop subtitle files by themselves if no media is playing.'
            else:
                if count == 1: msg = 'Drop to play media and add subtitle file'
                else:          msg = 'Drop to play media and add subtitle files'
            gui.statusbar.showMessage(msg, 0)
            self.player.show_text(msg, timeout=0, position=0)
        elif not gui.video:                             # no media playing, can't show marquee. don't bother with special options
            gui.statusbar.showMessage('Drop to play media, or hold ctrl/alt/shift while media is playing for additional options')
        else:
            mod = event.keyboardModifiers()
            if mod != self.dragdrop_last_modifiers:
                self.dragdrop_last_modifiers = mod
                if mod & Qt.ControlModifier:            # ctrl (concat before current)
                    if len(files) == 1: msg = 'Drop to concatenate 1 file before current media'
                    else:               msg = f'Drop to concatenate {len(files)} files before current media'
                elif mod & Qt.AltModifier:              # alt (concat after current)
                    if len(files) == 1: msg = 'Drop to concatenate 1 file after current media'
                    else:               msg = f'Drop to concatenate {len(files)} files after current media'
                elif mod & Qt.ShiftModifier:            # shift (add audio track)
                    if len(files) == 1: msg = 'Drop to add as audio track'
                    else:               msg = 'Drop to add first file as audio track'
                    if os.path.abspath(files[0]) == gui.video:
                        msg += ' (disabled due to identical file)'
                else:
                    msg = 'Drop to play media, or hold ctrl/alt/shift for more options'
                gui.statusbar.showMessage(msg, 0)
                self.player.show_text(msg, timeout=0, position=0)
        return super().dragMoveEvent(event)


    def dropEvent(self, event: QtGui.QDropEvent):       # attempt to open dropped files
        ''' Attempts to open dropped files as either media or subtitle tracks.
            Only uses the first dropped file for opening media or folders.

            Allows modifiers to alter the interaction used:
            - No modifiers -> Opens single media file/adds subtitle track(s).
            - Ctrl         -> Adds single media file as an audio track.
            - Shift        -> Concatenates media file(s) to the end of the current media.
            - Alt          -> Concatenates media file(s) to the start of the current media. '''

        # clear messages
        self.reset_dragdrop_status()

        # HACK: reset base cursor to help fix several cursor bugs
        self.setCursor(Qt.ArrowCursor)
        self.unsetCursor()

        files = self.dragdrop_files
        if gui.isFullScreen():  focus_window = settings.checkFocusOnDropFullscreen.isChecked()
        elif gui.isMaximized(): focus_window = settings.checkFocusOnDropMaximized.isChecked()
        else:                   focus_window = settings.checkFocusOnDropNormal.isChecked()

        def open_media_and_add_subtitles():
            for file in files:                          # open first valid media file, if any
                if os.path.splitext(file)[-1] not in constants.SUBTITLE_EXTENSIONS:
                    if gui.open(file, focus_window=focus_window) == 1:
                        break
            if gui.video and self.dragdrop_subtitle_count:
                for file in files:                      # re-loop and add all valid subtitle files (if ANY media is playing)
                    if os.path.splitext(file)[-1] in constants.SUBTITLE_EXTENSIONS:
                        gui.add_subtitle_files(file)

        if self.dragdrop_is_folder:
            gui.open_folder(files[0], event.keyboardModifiers(), focus_window=focus_window)
        elif gui.video:
            mod = event.keyboardModifiers()
            if mod & Qt.ControlModifier:                # ctrl (concat before current)
                gui.concatenate_signal.emit(gui.actionCatBeforeThis, files)
            elif mod & Qt.AltModifier:                  # alt (concat after current)
                gui.concatenate_signal.emit(gui.actionCatAfterThis, files)
            elif mod & Qt.ShiftModifier:                # shift (add audio track, one file at time currently)
                file = files[0]
                if os.path.abspath(file) != gui.video: gui.add_audio(path=file)
                else: gui.statusbar.showMessage('Cannot add file to itself as an audio track', 10000)
            else:                                       # no modifiers pressed, add first media file and any subtitle files
                open_media_and_add_subtitles()
        else:
            open_media_and_add_subtitles()              # no media playing -> ignore modifiers entirely

        if settings.checkRememberDropFolder.isChecked():                # update `cfg.lastdir` if desired
            cfg.lastdir = files[0] if os.path.isdir(files[0]) else os.path.dirname(files[0])
        return super().dropEvent(event)                 # run QWidget's built-in behavior




class QVideoPlayerLabel(QtW.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setMouseTracking(True)                     # needed so mouseMoveEvent works w/o clicking (needed for crop cursors)
        self.art = QtGui.QPixmap()
        self.gif = QtGui.QMovie()

        self._imageScale = 0                            # NOTE: scales are first set in qtstart.after_show_setup()
        self._artScale = 0
        self._gifScale = 0
        self._dragging = False
        self._draggingOffset = QtCore.QPoint()          # offset between cursor and image's real pos
        self.pixmapPos = QtCore.QPoint()                # local position of currently drawn QPixmap
        self.gifSize = QtCore.QSize()                   # gif's native size (not tracked by QMovie)
        self.gif.setCacheMode(QtGui.QMovie.CacheAll)    # required for jumpToFrame to work
        self.image = self.art                           # alias for self.art's QPixmap
        self.isCoverArt = False
        self.filename = None

        self.zoom = 1.0                                 # the true, current zoom level
        self._baseZoom = 1.0                            # base zoom level for the current window size based on zoom settings
        self._fitZoom = 1.0                             # the zoom required for fit mode, regardless of current zoom settings
        self._targetZoom = 1.0                          # the zoom level we're trying to reach while smooth-zooming
        self._smoothZoomTimerID = None                  # the ID for the smooth zoom timer, if any
        self._smoothZoomPos = QtCore.QPoint()           # the pos a smooth zoom should zoom in on
        self._smoothZoomFactor = 0.33                   # the "speed" at which a smooth zoom occurs
        self.zoomed = False                             # whether or not zoom-mode is enabled


    def play(self, file: str | bytes | None, interactable: bool = True, gif: bool = False, coverart: bool = False, autostart: bool = True):
        ''' Opens an image `file`, allowing image manipulation if `interactable`
            is True. Opens as a `QMovie` if `gif` is True (`QPixmap` otherwise),
            playing automatically if `autostart` is True. Sets `self.isCoverArt`
            to `coverart`. If `file` is None, the label is cleared and
            interaction is auto-disabled. '''

        # TODO: the `coverart` and `enabled` parameters used to be auto-determined based on whether or not `files`...
        # ...was bytes (if bytes, then it's cover art and we disable the widget). should we go back to that?
        self.gif.stop()
        self.filename = file
        self.zoomed = False
        if file is None:
            self.clear()
            self.gif.setFileName('')
            self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            return self.setEnabled(False)

        if gif:
            self.clear()
            self.gif.setFileName(file)
            if self.gif.frameCount() > 1:   # only treat GIF as animated if it has more than 1 frame
                try:                        # open gif in PIL to get its native size (fast)
                    with get_PIL_Image().open(file) as image:
                        size = image.size
                        self.gifSize.setWidth(size[0])
                        self.gifSize.setHeight(size[1])
                except:
                    self.gifSize = self.gif.frameRect().size()

                if self._gifScale == ZOOM_FIT:
                    self._resizeMovieFit()
                self.setMovie(self.gif)
                if autostart:
                    self.gif.start()
                logger.info('Animated GIF detected.')
            else:
                self.art.load(file)
                self.setPixmap(self.art)
                logger.info('Static GIF detected.')
        else:                               # static image. if `file` is bytes, it's cover art
            if isinstance(file, bytes):
                self.art.loadFromData(file)
            else:
                self.art.load(file)

            self.isCoverArt = coverart
            self.setPixmap(self.art)
            logger.info(f'Static image/cover art detected. (zoom={self.zoom})')

        self.disableZoom()
        self.setAttribute(Qt.WA_TransparentForMouseEvents, not interactable)
        self.setEnabled(interactable)


    def _updateImageScale(self, index: int, force: bool = False):
        ''' Updates the scaling mode for images (including
            single-frame GIFs, but excluding cover art). '''
        if not gui.actionCrop.isChecked() or force:
            logger.debug(f'Updating image scale to mode {index}')
            self._imageScale = index
            if self.pixmap():
                if not self.zoomed:
                    self._calculateBaseZoom()
                self.update()


    def _updateArtScale(self, index: int, force: bool = False):
        ''' Updates the scaling mode specifically for cover art. '''
        if not gui.actionCrop.isChecked() or force:
            logger.debug(f'Updating cover art scale to mode {index}')
            self._artScale = index
            if self.pixmap():
                if not self.zoomed:
                    self._calculateBaseZoom()
                self.update()


    def _updateGifScale(self, index: int, force: bool = False):
        ''' Updates the scaling mode for animated GIFs. '''
        if not gui.actionCrop.isChecked() or force:
            logger.debug(f'Updating gif scale to mode {index}')
            self._gifScale = index + 1      # FIXME: +1 is temporary until gifs properly support dynamic fit
            if self.movie():                # FIXME: ^^^ this is set manually in qtstart!!!!!
                if self.zoomed:             # FIXME: ^^^ it's also set in main.set_crop_mode!!!!
                    self.setZoom(self.zoom, force=True)
                else:
                    self._resetMovieSize()
                    self._calculateBaseZoom()


    def _updateSmoothZoomFactor(self, factor: int):
        ''' Updates the smooth zoom "speed" `factor / 100`. The `QSpinBox`
            is a percentage from 0-100 to make it easier to understand. '''
        self._smoothZoomFactor = factor / 100


    def _updatePreciseZoom(self, checked: bool):
        ''' Updates the "precise zoom" mode by swapping `pixmapPos`'s type
            between `QPoint` and `QPointF` to minimize errors. Precise zooming
            uses `QPointF`, normal zooming uses `QPoint`. '''
        if checked:
            if isinstance(self.pixmapPos, QtCore.QPoint):
                self.pixmapPos = QtCore.QPointF(self.pixmapPos)
        elif isinstance(self.pixmapPos, QtCore.QPointF):
            self.pixmapPos = self.pixmapPos.toPoint()


    def _resetMovieCache(self):
        ''' Stops and resets GIF to clear cached frames.
            Pause state is restored after reset. '''
        self.gif.stop()
        self.gif.setFileName(self.gif.fileName())
        self.gif.start()
        self.gif.setPaused(gui.is_paused)


    def _resetMovieSize(self):
        scale = self._gifScale
        self.setScaledContents(scale == ZOOM_FILL)
        if scale == ZOOM_NO_SCALING:
            self.gif.setScaledSize(QtCore.QSize(-1, -1))
        elif scale == ZOOM_FIT or self.width() < gui.vwidth or self.height() < gui.vheight:
            self._resizeMovieFit()
        elif scale == ZOOM_FILL:
            self.gif.setScaledSize(self.size())

        # TODO: the main issue with dynamic fit on gifs is that they start playing BEFORE we can actually see their true dimensions
        #       the fix appears to be something like loading the gif as a pixmap first, taking the dimensions, then playing as a gif
        #print('before', self.width(), self.height(), gui.vwidth, gui.vheight, self.gif.scaledSize().width(), self.gif.scaledSize().height())
        #if scale == ZOOM_FIT or self.width() < gui.vwidth or self.height() < gui.vheight: self._resizeMovieFit()
        #elif scale == ZOOM_FILL: self.gif.setScaledSize(self.size())
        #else: self.gif.setScaledSize(QtCore.QSize(-1, -1))
        self._resetMovieCache()


    def _resizeMovieFit(self):
        QtCore.QSize()
        self.gif.setScaledSize(self.gifSize.scaled(self.size(), Qt.KeepAspectRatio))


    def _calculateBaseZoom(self) -> float:
        ''' Calculates the default zoom level and minimum zoom level
            required to fit media within the current window size. '''

        # animated gif
        if self.movie():
            fitZoom = round(self.gif.scaledSize().width() / self.gifSize.width(), 4)
            scale = self._gifScale
            if scale == ZOOM_NO_SCALING:
                zoom = 1.0
            elif scale == ZOOM_FILL:
                w = self.width()
                h = self.height()
                vw = self.gifSize.width()
                vh = self.gifSize.height()
                ratio = vw / vh             # native gif aspect ratio
                widget_ratio = w / h        # aspect ratio of QVideoPlayerLabel
                if widget_ratio < ratio:    # gif is stretched vertically (there would be black bars top/bottom)
                    zoom = round(h / vh, 4)
                else:                       # gif is stretched horizontally (there would be black bars left/right)
                    zoom = round(w / vw, 4)
            else:                           # ZOOM_DYNAMIC_FIT (fit if media is smaller than window)
                zoom = fitZoom

        # image/cover art
        elif self.pixmap():
            fitSize = self.art.size().scaled(self.size(), Qt.KeepAspectRatio)
            fitZoom = round(fitSize.width() / self.art.width(), 4)

            scale = self._artScale if self.isCoverArt else self._imageScale
            if scale == ZOOM_FILL:
                w = self.width()
                h = self.height()
                vw = self.art.width()
                vh = self.art.height()
                ratio = vw / vh             # native image aspect ratio
                widget_ratio = w / h        # aspect ratio of QVideoPlayerLabel
                if widget_ratio < ratio:    # image is stretched vertically (there would be black bars top/bottom)
                    zoom = round(h / vh, 4)
                else:                       # image is stretched horizontally (there would be black bars left/right)
                    zoom = round(w / vw, 4)
            elif scale == ZOOM_FIT or self.width() < self.art.width() or self.height() < self.art.height():
                zoom = fitZoom
            else:                           # ZOOM_DYNAMIC_FIT (fit if image is smaller than window)
                zoom = 1.0

        # invalid mime-type, don't worry about zoom levels
        else:
            return 1.0

        self.zoom = self._baseZoom = self._targetZoom = zoom
        self._fitZoom = fitZoom
        return zoom


    def setZoom(
        self,
        zoom: float,
        pos: QtCore.QPoint = None,
        globalPos: QtCore.QPoint = None,
        force: bool = False,
        _smooth: bool = False
    ) -> float:

        is_gif = bool(self.movie())
        maxZoom = 100.0 if not is_gif else 20.0
        minZoomFactor = settings.spinZoomMinimumFactor.value()
        minZoom = self._baseZoom * minZoomFactor
        if settings.checkZoomForceMinimum.isChecked():
            minZoom = min(minZoomFactor, minZoom)

        if not _smooth:
            zoom = round(min(maxZoom, max(minZoom, zoom)), 4)
        if zoom == self.zoom and not force:
            if minZoomFactor == 1.0 and zoom == self._baseZoom and settings.checkZoomAutoDisable1x.isChecked():
                return self.disableZoom()   # _baseZoom == _targetZoom -> faster reset during smooth zoom (not worth it)
            return zoom

        willSmooth = not _smooth and settings.checkZoomSmooth.isChecked()
        if willSmooth:                      # about to start smoothing -> do first zoom-step now, start timer
            self._targetZoom = zoom
            if self._smoothZoomTimerID is None:
                zoom += (zoom - self.zoom) * self._smoothZoomFactor
                self._smoothZoomTimerID = self.startTimer(17, Qt.PreciseTimer)          # 17ms timer ~= 59fps

        if is_gif:
            if not willSmooth:
                if self._gifScale == ZOOM_FILL:
                    self.setScaledContents(False)
                    newSize = self.size().scaled(self.gifSize, Qt.KeepAspectRatio) * zoom
                else:
                    newSize = self.gifSize * zoom
                self.gif.setScaledSize(newSize)
                self._resetMovieCache()     # you can smooth zoom without freezing, but it's SLOWER than spam-resetting
        else:
            if globalPos:
                pos = self.mapFromGlobal(globalPos)
            if pos:
                if willSmooth:
                    self._smoothZoomPos = pos                   # set pos for smooth zoom to re-use
                elif settings.checkZoomPrecise.isChecked():
                    newSize = QtCore.QSizeF(self.art.size()) * zoom
                    oldSize = QtCore.QSizeF(self.art.size()) * self.zoom
                    oldPos = self.pixmapPos
                    xOffset = ((pos.x() - oldPos.x()) / oldSize.width()) * newSize.width()
                    yOffset = ((pos.y() - oldPos.y()) / oldSize.height()) * newSize.height()
                    self.pixmapPos = pos - QtCore.QPointF(xOffset, yOffset)
                    if not _smooth:                             # drag + zoom is bad unless it's a smooth zoom
                        self._draggingOffset = pos - self.pixmapPos
                else:
                    newSize = self.art.size() * zoom
                    oldSize = self.art.size() * self.zoom
                    oldPos = self.pixmapPos
                    xOffset = ((pos.x() - oldPos.x()) / oldSize.width()) * newSize.width()
                    yOffset = ((pos.y() - oldPos.y()) / oldSize.height()) * newSize.height()
                    self.pixmapPos = pos - QtCore.QPoint(xOffset, yOffset)
                    if not _smooth:                             # drag + zoom is bad unless it's a smooth zoom
                        self._draggingOffset = pos - self.pixmapPos

        if not willSmooth:
            self.zoom = zoom
        self.zoomed = True
        self.update()

        if not _smooth:
            logger.debug(f'QVideoPlayerLabel zoom set to {zoom} (pos={pos} | globalPos={globalPos})')
        return zoom


    def incrementZoom(
        self,
        increment: float,
        pos: QtCore.QPoint = None,
        globalPos: QtCore.QPoint = None,
        force: bool = False
    ) -> float:
        return self.setZoom(self.zoom + increment, pos, globalPos, force)


    def disableZoom(self) -> float:
        self.zoomed = False
        self.pixmapPos = self.rect().center() - self.art.rect().center()

        if self._smoothZoomTimerID: self._smoothZoomTimerID = self.killTimer(self._smoothZoomTimerID)
        if self.movie(): self._resetMovieSize()
        else: self.setScaledContents(False)

        self.update()
        return self._calculateBaseZoom()


    def pan(self, direction: QtCore.QPoint, mod: int = None):
        ''' Pans `self.pixmapPos` in `direction`, using `mod` modifiers. If
            `Shift` is held down, `direction` is transposed. If `Alt` is held
            down, `direction` is tripled. '''
        if mod is None:
            mod = app.keyboardModifiers()
        offset = direction

        # shift held -> scroll horizontally, alt held -> scroll 3x as far
        if mod & Qt.ShiftModifier:
            offset = offset.transposed()
        if mod & Qt.AltModifier:
            gui.ignore_next_alt = True
            offset = direction.transposed() * 3.0               # alt swaps horizontal/vertical scroll for some reason
        if settings.checkZoomPanInvertScroll.isChecked():
            offset *= -1

        self.pixmapPos += offset
        self.zoomed = True
        self.update()


    def mousePressEvent(self, event: QtGui.QMouseEvent):
        ''' Sets the offset between the cursor
            and our `QPixmap`'s local position. '''
        if event.button() == Qt.LeftButton and not gui.actionCrop.isChecked():
            self._draggingOffset = event.pos() - self.pixmapPos
        return super().mousePressEvent(event)                   # QLabel will pass event to underlying widgets (needed for cropping)


    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        ''' Handles mouse movement over the image player. Drags our `QPixmap` by
            adjusting its position based on the cursor's position relative to
            the offset we set in `mousePressEvent`, and resets the idle timer
            if crop mode is disabled. Otherwise, `QVideoPlayer.mouseMoveEvent()`
            is called to handle cropping. '''
        if not gui.actionCrop.isChecked():
            if event.buttons() == Qt.LeftButton:                # why doesn't `event.button()` work here?
                self.pixmapPos = event.pos() - self._draggingOffset
                self._dragging = True
                self.update()                                   # manually update
            if settings.checkHideIdleCursor.isChecked() and gui.video:
                gui.vlc.idle_timeout_time = time.time() + settings.spinHideIdleCursorDuration.value()
            else:
                gui.vlc.idle_timeout_time = 0.0                 # 0 locks the cursor/UI
        else:
            return super().mouseMoveEvent(event)                # QLabel will pass event to underlying widgets (needed for cropping)


    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        ''' Disables drag-mode on releasing a mouse button. If left-clicking
            and drag-mode was never enabled, then zoom-mode is disabled. '''
        if event.button() == Qt.LeftButton:
            if not (self.movie() or self._dragging):            # reset QVideoPlayerLabel's zoom if we click without dragging
                self.disableZoom()
        self._dragging = False
        return super().mouseReleaseEvent(event)                 # QLabel will pass event to underlying widgets (needed for cropping)


    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        if self.zoomed and event.button() == Qt.LeftButton: self.disableZoom()
        else: super().mouseDoubleClickEvent(event)


    def wheelEvent(self, event: QtGui.QWheelEvent):
        ''' Increments the zoom factor or pans `self.pixmapPos` depending
            on what modifiers and mouse buttons are held down. '''
        event.accept()                                          # accept event or QLabel will pass it through no matter what
        if gui.actionCrop.isChecked() or not gui.video: return

        # see if we want the secondary action and what our secondary action is
        mod = event.modifiers()
        secondary_pans = not settings.checkZoomPanByDefault.isChecked()
        if event.buttons() == Qt.RightButton:
            use_secondary = True
            gui.ignore_next_right_click = True
        else:
            use_secondary = mod & Qt.ControlModifier

        # pan the media around instead of zooming if desired
        if (use_secondary and secondary_pans) or (not use_secondary and not secondary_pans):
            return self.pan(event.angleDelta(), mod)

        # otherwise, calculate the factor with which to change our zoom
        add = event.angleDelta().y() > 0
        if mod & Qt.ShiftModifier:
            factor = settings.spinZoomIncrement3.value()    # shift -> #3
        elif mod & Qt.AltModifier:
            factor = settings.spinZoomIncrement2.value()    # alt -> #2
            add = event.angleDelta().x() > 0                # alt swaps horizontal/vertical scroll for some reason
            gui.ignore_next_alt = True
        else:
            factor = settings.spinZoomIncrement1.value()    # default -> #1

        # calculate and apply our new zoom level
        zoom = self._targetZoom if settings.checkZoomSmooth.isChecked() else self.zoom
        increment = (zoom / factor)
        self.setZoom(zoom + (increment if add else -increment), globalPos=QtGui.QCursor().pos())


    def resizeEvent(self, event: QtGui.QResizeEvent):
        ''' Scales the GIF/image/art while resizing, and calculates
            what zoom factor the new player size should start from. '''
        if self.hasScaledContents():
            return
        elif not self.zoomed:
            if self.pixmap():
                self._calculateBaseZoom()
            elif self.movie():
                if self._gifScale == ZOOM_FIT:
                    self._resizeMovieFit()
                self._resetMovieCache()
                self._calculateBaseZoom()
        elif self._gifScale == ZOOM_FILL:
            self.gif.setScaledSize(self.size().scaled(self.gifSize, Qt.KeepAspectRatio) * self.zoom)
            self._resetMovieCache()


    def timerEvent(self, event: QtCore.QTimerEvent):            # TODO why is zooming out so slow at lower smoothZoomFactors??
        if self._smoothZoomTimerID is not None:
            currentZoom = self.zoom
            if self._targetZoom == currentZoom:
                self._smoothZoomTimerID = self.killTimer(self._smoothZoomTimerID)
                self.setZoom(self._targetZoom, pos=self._smoothZoomPos, _smooth=True)
                #if self.movie(): self._resetMovieCache()       # only reset gif cache after smooth zoom is finished
            else:
                digits = 4 - (int(math.log10(self._targetZoom)) + 1)                        # smaller zoom, round to more digits
                newZoom = round(currentZoom + (self._targetZoom - currentZoom) * self._smoothZoomFactor, digits)
                if newZoom == currentZoom:
                    newZoom = self._targetZoom
                self.setZoom(newZoom, pos=self._smoothZoomPos, _smooth=True)
        return super().timerEvent(event)


    def paintEvent(self, event: QtGui.QPaintEvent):             # TODO very close to figuring out how to handle GIFs in here
        #if True:
        if self.pixmap():
            painter = QtGui.QPainter(self)
            if settings.checkScaleFiltering.isChecked():
                painter.setRenderHint(QtGui.QPainter.Antialiasing)
                painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
                transformMode = Qt.SmoothTransformation
            else:
                transformMode = Qt.FastTransformation

            # draw zoomed pixmap by using scale mode and the current zoom to generate new size
            scale = self._artScale if self.isCoverArt else self._imageScale
            #pixmap = self.art if self.pixmap() else self.gif.currentPixmap()
            pixmap = self.art
            if self.zoomed:
                zoom = self.zoom

                # at >1 zoom, drawing to QRect is MUCH faster and looks identical to art.scaled()
                try:
                    if zoom >= 1:
                        if settings.checkZoomPrecise.isChecked():
                            if scale != ZOOM_FILL: size = QtCore.QSizeF(pixmap.size())  # TODO V does this deform the image while zooming?
                            else:                  size = QtCore.QSizeF(self.size().scaled(pixmap.size(), Qt.KeepAspectRatio))
                            painter.drawPixmap(QtCore.QRectF(self.pixmapPos, size * zoom).toRect(), pixmap)
                        else:
                            if scale != ZOOM_FILL: size = pixmap.size()                 # TODO V ditto?
                            else:                  size = self.size().scaled(pixmap.size(), Qt.KeepAspectRatio)
                            painter.drawPixmap(QtCore.QRect(self.pixmapPos, size * zoom), pixmap)
                        #painter.scale(zoom, zoom)                                      # TODO painter.scale() vs. QRect() -> which is faster?
                        #painter.drawPixmap(self.pixmapPos / zoom, pixmap)

                    # at <1 zoom, art.scaled() looks MUCH better and the performance drop is negligible
                    else:
                        if scale == ZOOM_FILL:
                            size = self.size().scaled(pixmap.size(), Qt.KeepAspectRatio) * zoom
                            aspectRatioMode = Qt.IgnoreAspectRatio
                        else:
                            size = pixmap.size() * zoom
                            aspectRatioMode = Qt.KeepAspectRatio
                        painter.drawPixmap(self.pixmapPos, pixmap.scaled(size, aspectRatioMode, transformMode))
                except TypeError:
                    logger.warning(f'(!) QVideoPlayerLabel paintEvent failed due to mismatched pixmapPos type: {format_exc()}')

            # draw normal pixmap. NOTE: for fill-mode, drawing to a QRect NEVER looks identical (it's much worse)
            else:
                #scale = self._artScale if self.isCoverArt else self._imageScale
                if scale == ZOOM_NO_SCALING or (scale == ZOOM_DYNAMIC_FIT and self._baseZoom == 1):
                    self.pixmapPos = self.rect().center() - pixmap.rect().center()
                    painter.drawPixmap(self.pixmapPos, pixmap)
                elif scale == ZOOM_FIT or (scale == ZOOM_DYNAMIC_FIT and self._baseZoom != 1):
                    scaledPixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode)
                    self.pixmapPos = self.rect().center() - scaledPixmap.rect().center()
                    painter.drawPixmap(self.pixmapPos, scaledPixmap)
                elif scale == ZOOM_FILL:
                    self.pixmapPos = QtCore.QPoint()
                    painter.drawPixmap(0, 0, pixmap.scaled(self.size(), transformMode=transformMode))
        else:
            super().paintEvent(event)




class QVideoSlider(QtW.QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)                               # TODO is having stuff like this here better than in the .ui file?
        self.setMouseTracking(True)

        self.last_mouseover_time = 0
        self.last_mouseover_pos = None
        self.clamp_minimum = False                              # NOTE: essentially aliases for gui.buttonTrimXXX.isChecked()
        self.clamp_maximum = False
        self.grabbing_clamp_minimum = False
        self.grabbing_clamp_maximum = False
        self.scrubbing = False
        self.scrub_start_frame = 0

        self.hover_font_color: QtGui.QColor = None
        self.colors: list[Color] = None
        self.color_index = 0
        self.color_order = (Color('red'), Color('blue'), Color('lime'))
        self.last_color_change_time = 0


    # pass keystrokes through to parent
    def keyPressEvent(self, event: QtGui.QKeyEvent):   return gui.keyPressEvent(event)
    def keyReleaseEvent(self, event: QtGui.QKeyEvent): return gui.keyReleaseEvent(event)


    def setMaximum(self, maximum: int):
        ''' Sets the maximum slider value to `maximum - 1`. If 1 or less,
            the slider and its mouse events are automatically disabled. '''
        super().setMaximum(maximum - 1)
        self.setEnabled(maximum > 1)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, maximum < 2)


    def paintEvent(self, event: QtGui.QPaintEvent):
        ''' If enabled, paints a timestamp under the mouse corresponding with
            its position over the slider relative to the current media, and
            paints a rainbow effect around trim-boundaries, if present. '''
        super().paintEvent(event)                               # perform built-in paint immediately so we can paint on top

        # handle QVideoPlayer's fullscreen controls/idle cursor timeout
        try:
            now = time.time()
            vlc = gui.vlc
            idle_time = vlc.idle_timeout_time
            if not idle_time or idle_time > now or gui.restarted or (gui.player.get_state() == 5 and not gui.mime_type == 'image'):
                if vlc.underMouse() and not gui.actionCrop.isChecked():
                    cursor = app.overrideCursor()               # these if's may seem excessive, but it's literally...
                    if not cursor:                              # ...12x faster than actually setting the cursor
                        app.setOverrideCursor(QtCore.Qt.ArrowCursor)
                    elif cursor.shape() != QtCore.Qt.ArrowCursor:
                        app.changeOverrideCursor(QtCore.Qt.ArrowCursor)

                if gui.isFullScreen():
                    current_opacity = gui.dockControls.windowOpacity()
                    max_opacity = settings.spinFullScreenMaxOpacity.value() / 100
                    if current_opacity < max_opacity:
                        fps = 20
                        if gui.player.is_playing() and settings.checkHighPrecisionProgress.isChecked():
                            fps = max(fps, gui.frame_rate_rounded)

                        fade_time = settings.spinFullScreenFadeDuration.value() or 0.01
                        opacity_increment = max_opacity / (fade_time * fps)
                        gui.dockControls.setWindowOpacity(min(current_opacity + opacity_increment, max_opacity))

            else:
                if vlc.underMouse() and not gui.actionCrop.isChecked():
                    cursor = app.overrideCursor()
                    if not cursor:
                        app.setOverrideCursor(QtCore.Qt.BlankCursor)
                    elif cursor.shape() != QtCore.Qt.BlankCursor:
                        app.changeOverrideCursor(QtCore.Qt.BlankCursor)

                if gui.isFullScreen():
                    current_opacity = gui.dockControls.windowOpacity()
                    min_opacity = settings.spinFullScreenMinOpacity.value() / 100
                    if current_opacity > min_opacity:
                        fps = 20
                        if gui.player.is_playing() and settings.checkHighPrecisionProgress.isChecked():
                            fps = max(fps, gui.frame_rate_rounded)

                        max_opacity = settings.spinFullScreenMaxOpacity.value() / 100
                        fade_time = settings.spinFullScreenFadeDuration.value() or 0.01
                        opacity_increment = max_opacity / (fade_time * fps)
                        gui.dockControls.setWindowOpacity(max(current_opacity - opacity_increment, min_opacity))
        except:
            return

        p = QtGui.QPainter()
        p.begin(self)

        # trim start/end markers -> draw trim-boundaries
        if self.clamp_minimum or self.clamp_maximum:

            # pick current color to use for animated trim-boundaries
            if not self.colors:
                next_index = self.color_index + 1
                if next_index > len(self.color_order) - 1:
                    next_index = 0
                self.colors = list(self.color_order[next_index].range_to(self.color_order[self.color_index], int(gui.frame_rate * 4)))
                self.color_index = next_index
            if now > self.last_color_change_time + 0.05:    # update color at a MAX of 20fps
                color = QtGui.QColor(self.colors.pop().get_hex())
                self.last_color_change_time = now
            else:
                color = QtGui.QColor(self.colors[-1].get_hex())

            color.setAlpha(100)
            pen_thick = QtGui.QPen(color, 2)
            pen_thin = QtGui.QPen(QtGui.QColor(255, 255, 255), 1)
            #pen_thick.setCapStyle(Qt.RoundCap)
            p.setBrush(QtGui.QColor(0, 0, 0, 200))

            opt = QtW.QStyleOptionSlider()
            self.initStyleOption(opt)
            groove_rect = self.style().subControlRect(QtW.QStyle.CC_Slider, opt, QtW.QStyle.SC_SliderGroove, self)
            #print(groove_rect, groove_rect.left(), groove_rect.topLeft(), dir(groove_rect))

            # draw triangle markers for start/end and cover slider outside trim TODO: this is not efficient
            if self.clamp_minimum:
                x = self.rangeValueToPixelPos(gui.minimum)
                p.setPen(pen_thick)
                p.drawRoundedRect(groove_rect.left(), groove_rect.top(), x, groove_rect.height(), 2, 2)
                p.setPen(pen_thin)
                p.drawPolygon(QtGui.QPolygon([QtCore.QPoint(x, 2), QtCore.QPoint(x, self.height() - 2), QtCore.QPoint(x - 4, self.height() / 2)]))
            if self.clamp_maximum:
                x = self.rangeValueToPixelPos(gui.maximum)
                p.setPen(pen_thick)
                p.drawRoundedRect(x, groove_rect.top(), groove_rect.width() - x - 1, groove_rect.height(), 2, 2)
                p.setPen(pen_thin)
                p.drawPolygon(QtGui.QPolygon([QtCore.QPoint(x, 2), QtCore.QPoint(x, self.height() - 2), QtCore.QPoint(x + 4, self.height() / 2)]))

        #for marker in self.markers:    # an idea for a more general implementation with an arbitrary number of "markers"
        #    x = self.rangeValueToPixelPos(marker)
        #    #print(x)
        #    #p.drawImage(pos, 0, QtGui.QImage(r'C:\cs\python\videoeditor\bin\icon.ico'))
        #    p.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 1))
        #    p.setBrush(QtGui.QColor(255, 255, 255))
        #    #p.drawLine(x, 0, x, self.height())
        #    p.drawPolygon(QtGui.QPolygon([QtCore.QPoint(x, 0), QtCore.QPoint(x, self.height()), QtCore.QPoint(x + 4, self.height() / 2)]))

        # hover timestamps
        if settings.groupHover.isChecked():                 # ↓ 0.05 looks instant but avoids flickers
            fade_time = max(0.05, settings.spinHoverFadeDuration.value())
            if now <= self.last_mouseover_time + fade_time:
                if self.underMouse():                       # ↓ get position relative to widget
                    pos = self.mapFromGlobal(QtGui.QCursor().pos())
                    self.last_mouseover_time = now          # reset fade timer if we're still hovering
                    self.last_mouseover_pos = pos           # save last mouse position within slider
                else:
                    pos = self.last_mouseover_pos           # use last position if mouse is outside the slider

                frame = self.pixelPosToRangeValue(pos)
                h, m, s, _ = get_hms(round(gui.duration_rounded * (frame / gui.frame_count), 2))
                text = f'{m}:{s:02}' if gui.duration_rounded < 3600 else f'{h}:{m:02}:{s:02}'

                size = settings.spinHoverFontSize.value()   # TODO use currentFontChanged signals + more for performance? not needed?
                font = settings.comboHoverFont.currentFont()
                font.setPointSize(size)
                #font.setPixelSize(size)
                p.setFont(font)
                pos.setY(self.height() - (self.height() - size) / 2)

                # calculate fade-alpha from 0-255 based on time since we stopped hovering. default to 255 if fading is disabled
                # TODO: I sure used a lot of different methods for fading things. should these be more unified?
                alpha = (self.last_mouseover_time + fade_time - now) * (255 / fade_time) if fade_time != 0.05 else 255

                if settings.checkHoverShadow.isChecked():   # draw shadow first (as black, slightly offset text)
                    p.setPen(QtGui.QColor(0, 0, 0, alpha))  # set color to black
                    p.drawText(pos.x() + 1, pos.y() + 1, text)
                self.hover_font_color.setAlpha(alpha)
                p.setPen(self.hover_font_color)             # set color to white
                p.drawText(pos, text)                       # draw actual text over shadow

                # my idea for using tooltips for displaying the time. works, but qt's tooltips don't refresh fast enough
                #h, m, s, _ = get_hms(round(gui.duration_rounded * (frame / gui.frame_count), 2))
                #self.setToolTip(f'{h}:{m:02}:{s:02}' if h else f'{m}:{s:02}')
        p.end()


    def wheelEvent(self, event: QtGui.QWheelEvent):
        ''' Page-steps along the slider while scrolling. Horizontal sliders
            are increased by scrolling down or right, vertical sliders are
            increased by scrolling up or left. '''
        up = event.angleDelta().y() > 0 or event.angleDelta().x() > 0
        if self.orientation() == Qt.Vertical:
            up = not up

        if up: forward = settings.checkScrollUpForForwards.isChecked()
        else:  forward = not settings.checkScrollUpForForwards.isChecked()
        gui.page_step(step=settings.spinScrollProgress.value() / 100, forward=forward)
        event.accept()                                          # must accept event or it gets passed to the window


    def enterEvent(self, event: QtGui.QEnterEvent):
        ''' Marks the current time when mousing-over and forces a `paintEvent`
            to begin drawing hover-timestamps. Does not require
            `setMouseTracking(True)`, as `enterEvent` fires regardless. '''
        if gui.video:
            self.last_mouseover_time = time.time()              # save last mouseover time to use as a fade timer
            self.update()                                       # force-update to draw timestamp in self.paintEvent()
        return super().enterEvent(event)


    def mousePressEvent(self, event: QtGui.QMouseEvent):
        ''' Snaps the slider handle to the mouse cursor if left-clicked.
            Does not use the normal implementation to grab the handle,
            instead allowing it to move freely until the mouse is moved,
            ensuring a snappier experience when clicking the progress bar.
            Does not emit the `sliderPressed` signal. '''

        if event.button() == Qt.LeftButton:
            pos = event.pos()
            frame = self.pixelPosToRangeValue(pos)
            if gui.minimum < frame < gui.maximum:
                gui.player.set_and_update_progress(frame, SetProgressContext.NAVIGATION_EXACT)
            self.scrub_start_frame = frame

            # https://stackoverflow.com/questions/40100733/finding-if-a-qpolygon-contains-a-qpoint-not-giving-expected-results
            if self.clamp_minimum or self.clamp_maximum:        # ^ alternate solution by finding points inside QPolygons
                radius = 12                                     # 12 pixel radius for the handles
                self.grabbing_clamp_minimum = False
                self.grabbing_clamp_maximum = False
                if self.clamp_minimum:
                    min_pos = self.rangeValueToPixelPos(gui.minimum)
                    if min_pos - radius < pos.x() < min_pos + radius:
                        self.grabbing_clamp_minimum = True
                if self.clamp_maximum:
                    max_pos = self.rangeValueToPixelPos(gui.maximum)
                    if max_pos - radius < pos.x() < max_pos + radius:
                        self.grabbing_clamp_maximum = True
            #if abs(delta) > 0.025:                             # only change if difference between new/old positions is greater than 2.5%
            #    self.setValue(new_value)


    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        ''' If not dragging, this manually repaints the timestamp-hover effect
            while mousing over the progress bar. Otherwise, this re-implements
            scrubbing by grabbing the handle, pausing the player, and updating
            the player position. Does not emit the `sliderMoved` signal. '''

        # event.button() is always 0 for move events. yes, it's very stupid.
        if event.buttons() != Qt.LeftButton:                    # NOTE: requires `self.setMouseTracking(True)`
            self.update()

        # handle dragging
        else:
            frame = self.pixelPosToRangeValue(event.pos())      # get frame
            gui.player.set_pause(True)                          # pause player while scrubbing
            gui.gifPlayer.gif.setPaused(True)                   # pause GIF player while scrubbing
            if self.grabbing_clamp_maximum:
                gui.player.set_and_update_progress(frame, SetProgressContext.SCRUB)
                if self.grabbing_clamp_minimum:                 # grabbing both markers -> choose marker by which direction we drag
                    if frame > self.scrub_start_frame:
                        self.grabbing_clamp_minimum = False
                        gui.set_trim_end(True)
                    elif frame < self.scrub_start_frame:
                        self.grabbing_clamp_maximum = False
                        gui.set_trim_start(True)
                else:
                    gui.set_trim_end(True)
            elif self.grabbing_clamp_minimum:
                gui.player.set_and_update_progress(frame, SetProgressContext.SCRUB)
                gui.set_trim_start(True)
            else:                                               # not grabbing markers -> only update progress between markers
                gui.player.set_and_update_progress(min(gui.maximum, max(gui.minimum, frame)), SetProgressContext.SCRUB)
            self.last_mouseover_time = 0                        # reset last mouseover time to stop drawing timestamp immediately
            self.scrubbing = True                               # mark that we're scrubbing


    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        ''' Unpauses the player after scrubbing, unless it was paused
            originally. Does not emit the `sliderReleased` signal. '''

        just_restarted = False
        frame = self.pixelPosToRangeValue(event.pos())          # get frame
        if frame < gui.minimum:   gui.player.set_and_update_progress(gui.minimum, SetProgressContext.RESET_TO_MIN)
        elif frame > gui.maximum: gui.player.set_and_update_progress(gui.maximum, SetProgressContext.RESET_TO_MAX)
        elif self.scrubbing:
            if frame == gui.frame_count:
                just_restarted = True
                gui.restart()
            else:
                gui.player.set_and_update_progress(frame, SetProgressContext.NAVIGATION_EXACT)

        if not just_restarted:                                  # do not touch pause state if we manually restarted
            if gui.restarted:
                if settings.checkNavigationUnpause.isChecked():
                    gui.force_pause(False)                      # auto-unpause after restart
                    gui.restarted = False
            else:
                paused = False or gui.is_paused                 # stay paused if we were paused
                gui.player.set_pause(paused)
                gui.gifPlayer.gif.setPaused(paused)

        self.grabbing_clamp_minimum = False
        self.grabbing_clamp_maximum = False
        if self.underMouse():                                   # resume drawing timestamp after release
            self.last_mouseover_time = time.time()
        self.scrubbing = False


    def pixelPosToRangeValue(self, pos: QtCore.QPoint) -> int:  # https://stackoverflow.com/questions/52689047/moving-qslider-to-mouse-click-position
        ''' Auto-magically detects the correct value to set the handle
            to based on a given `pos`. Works with horizontal and vertical
            sliders, with or without stylesheets. '''
        try:
            opt = QtW.QStyleOptionSlider()
            self.initStyleOption(opt)

            groove_rect = self.style().subControlRect(QtW.QStyle.CC_Slider, opt, QtW.QStyle.SC_SliderGroove, self)
            handle_rect = self.style().subControlRect(QtW.QStyle.CC_Slider, opt, QtW.QStyle.SC_SliderHandle, self)
            try:
                raw_position = pos - handle_rect.center() + handle_rect.topLeft()
            except TypeError:                                   # event.pos() becomes None in rare, unknown circumstances
                pos = self.mapFromGlobal(QtGui.QCursor().pos())
                raw_position = pos - handle_rect.center() + handle_rect.topLeft()

            if self.orientation() == Qt.Horizontal:
                slider_min = groove_rect.x()
                slider_max = groove_rect.right() - handle_rect.width() + 1
                new_position = raw_position.x() - slider_min
            else:
                slider_min = groove_rect.y()
                slider_max = groove_rect.bottom() - handle_rect.height() + 1
                new_position = raw_position.y() - slider_min

            return QtW.QStyle.sliderValueFromPosition(
                self.minimum(),                                 # min
                self.maximum(),                                 # max
                new_position,                                   # position
                slider_max - slider_min,                        # span
                opt.upsideDown                                  # upsideDown
            )
        except:
            logger.warning(f'(!) Unexpected error in pixelPosToRangeValue - {format_exc()}')
            return 0                                            # return 0 as a failsafe


    def rangeValueToPixelPos(self, value: int) -> int:
        ''' Auto-magically detects the correct X/Y position to set the handle
            to based on a given `value`. Works with horizontal and vertical
            (...? see TODO below) sliders, with or without stylesheets. '''
        opt = QtW.QStyleOptionSlider()
        self.initStyleOption(opt)

        groove_rect = self.style().subControlRect(QtW.QStyle.CC_Slider, opt, QtW.QStyle.SC_SliderGroove, self)
        handle_rect = self.style().subControlRect(QtW.QStyle.CC_Slider, opt, QtW.QStyle.SC_SliderHandle, self)

        is_horizontal = self.orientation() == Qt.Horizontal
        if is_horizontal:
            slider_min = groove_rect.x()
            slider_max = groove_rect.right() - handle_rect.width() + 1
        else:
            slider_min = groove_rect.y()
            slider_max = groove_rect.bottom() - handle_rect.height() + 1

        raw_position = QtW.QStyle.sliderPositionFromValue(
            self.minimum(),                                     # min
            self.maximum(),                                     # max
            value,                                              # position
            slider_max - slider_min,                            # span
            opt.upsideDown                                      # upsideDown
        )

        # TODO test this on vertical
        if is_horizontal: return raw_position + handle_rect.center().x() - handle_rect.topLeft().x()
        else:             return raw_position + handle_rect.center().y() - handle_rect.topLeft().y()



# ------------------------------------------
# Concatenation Widgets
# ------------------------------------------
class QVideoListItemWidget(QtW.QWidget):                        # TODO this likely does not get garbage collected
    ''' An item representing a media file within a
        `QVideoList`, within the concatenation menu. '''
    def __init__(
        self,
        parent: QtW.QWidget,
        thumbnail_path: str,
        text: str,
        is_playing: bool
    ):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.layout = QtW.QHBoxLayout()                         # ^ required for dragging to work
        self.setLayout(self.layout)

        self.thumbnail = QtW.QLabel(self)
        self.thumbnail.setPixmap(QtGui.QPixmap(thumbnail_path))
        self.thumbnail.setAlignment(Qt.AlignCenter)

        # put outline around thumbnail if this item is currently playing
        if not is_playing:
            self.thumbnail.setStyleSheet('QLabel { padding: 4px; }')
        else:
            self.thumbnail.setStyleSheet(
                'QLabel { padding: 4px; background-color: '
                'qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,'
                'stop:0.573864 rgba(0,255,255,255),stop:1 rgba(0,0,119,255)); }'
            )

        self.label = QtW.QLabel(text, self)
        #self.label.setStyleSheet('QLabel { padding-left: 1px; }')
        #self.layout.addSpacerItem(QtW.QSpacerItem(2, 20, QtW.QSizePolicy.Fixed, QtW.QSizePolicy.Minimum))

        self.layout.addWidget(self.thumbnail)
        self.layout.addWidget(self.label)
        self.layout.addSpacerItem(QtW.QSpacerItem(40, 20, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum))
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(1, 0, 0, 0)




class QVideoList(QtW.QListWidget):                              # TODO this likely is not doing any garbage collection
    ''' A list of interactable media files represented by
        `QVideoListItemWidget`'s within the concatenation menu. '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)


    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):     # drag and drop requires self.setAcceptDrops(True)
        if event.mimeData().hasUrls(): event.accept()
        else: event.ignore()
        super().dragEnterEvent(event)                           # run QWidget's built-in behavior


    def dropEvent(self, event: QtGui.QDropEvent):
        ''' Handles adding externally dropped items to the list, and includes
            an ugly workaround for a Qt bug that creates duplicated and/or
            invisible items when dragging an item below itself without
            actually changing its final position. '''
        old_items = tuple(qthelpers.listGetAllItems(self))
        files = tuple(url.toLocalFile() for url in event.mimeData().urls())
        if files:
            self.add(files=files)

        # reset and force arrow cursor so it doesn't get erroneously hidden
        qthelpers.setCursor(Qt.ArrowCursor)

        # run QWidget's built-in behavior
        super().dropEvent(event)

        # if no files were dropped, assume we did an internal drag/drop -> fix Qt bug
        if not files:
            event.ignore()                                      # ignoring the event prevents original item from getting deleted
            for item in qthelpers.listGetAllItems(self):        # cycle through items and
                if item not in old_items:                       # look for "new" item that appeared
                    garbage = self.takeItem(self.row(item))     # delete corrupted item
                    del garbage


    def contextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Creates a context menu for the `QListWidgetItem` underneath
            the mouse, if any. This could alternatively be accomplished
            through the `itemClicked` signal. '''
        item = self.itemAt(event.pos())                         # get item under mouse to work with
        if not item: return                                     # no item under mouse, return
        path = item.toolTip()

        def play_and_refresh():
            gui.open(
                path,
                focus_window=False,
                flash_window=False,
                update_recent_list=path in gui.recent_files,
                update_raw_last_file=False
            )
            self.refresh_thumbnail_outlines()

        def set_output_part(*, filename: bool = True):
            output = self.parent().output
            old_path = output.text().strip()
            if filename:                                        # replace filename
                dirname = os.path.dirname(old_path)
                if dirname:
                    dirname += '/'
                output.setText(os.path.normpath(dirname + os.path.basename(path)))
            else:                                               # replace dirname
                filename = os.path.basename(old_path)
                new_path = os.path.normpath(f'{os.path.dirname(path)}/{filename}')
                if not filename:
                    new_path += os.sep
                output.setText(new_path)

        action1 = QtW.QAction('&Play')
        action1.triggered.connect(play_and_refresh)
        action2 = QtW.QAction('&Explore')
        action2.triggered.connect(lambda: qthelpers.openPath(path, explore=True))
        action3 = QtW.QAction('&Remove')
        action3.triggered.connect(lambda: qthelpers.listRemoveSelected(self))
        action4 = QtW.QAction('&Set as output (filename)')
        action4.triggered.connect(set_output_part)
        action5 = QtW.QAction('&Set as output (folder)')
        action5.triggered.connect(lambda: set_output_part(filename=False))
        action6 = QtW.QAction('&Set as output (full path)')
        action6.triggered.connect(lambda: self.parent().output.setText(path))

        context = QtW.QMenu(self)
        context.addActions((action1, action2, action3))
        context.addSeparator()
        context.addActions((action4, action5, action6))
        context.exec(event.globalPos())


    def add(self, *, files: str | tuple[str] = None, index: int = None):
        ''' Adds a list/tuple of `files` as `QVideoListItemWidget`'s. If `files`
            is a string, it will be interpreted as the sole element of a tuple.
            If `index` is specified, `files` will be inserted at that spot. '''
        if isinstance(files, str):
            files = (files,)
        elif files is None:
            files, cfg.lastdir = qthelpers.browseForFiles(
                lastdir=cfg.lastdir,
                caption='Select video to add',
                filter='MP4 files (*.mp4);;All files (*)'
            )

        # create QVideoListItemWidgets on top of QListWidgetItems for each file
        thumbnails_needed = []
        for file in files:
            if not file or not os.path.exists(file):
                continue

            file = os.path.abspath(file)
            basename = os.path.basename(file)
            thumbnail_name = get_unique_path(basename.replace('/', '.').replace('\\', '.'))
            thumbnail_path = os.path.join(constants.THUMBNAIL_DIR, f'{thumbnail_name}_thumbnail.jpg')
            last_modified = time.strftime('%#m/%#d/%y | %#I:%M:%S%p', time.localtime(os.path.getmtime(file))).lower()
            html = f'<html><head/><body><p style="line-height:0.5"><span style="font-family:Yu Gothic; font-size:12pt;">{basename}</span></p><p><span style="color:#676767;">{last_modified}</span></p></body></html>'
            item_widget = QVideoListItemWidget(
                parent=self,
                thumbnail_path=thumbnail_path,
                text=html,
                is_playing=file == gui.video
            )

            # create and setup QListWidgetItem as the base for our QVideoListItemWidget with our file and QLabel
            if index is None:
                item_base = QtW.QListWidgetItem(self)
            else:
                item_base = QtW.QListWidgetItem()
                self.insertItem(index, item_base)
            item_base.setToolTip(file)
            self.setItemWidget(item_base, item_widget)
            item_base.setSizeHint(QtCore.QSize(0, 64))          # default width/height is -1, but this is invalid. yeah.

            # check if thumbnail actually existed or not
            if not os.path.exists(thumbnail_path):              # check if thumbnail existed or not
                thumbnails_needed.append((file, thumbnail_path, item_widget))

        # ensure thumbnail folder exists, then create threads to generate thumbnails
        if not os.path.exists(constants.THUMBNAIL_DIR):
            os.makedirs(constants.THUMBNAIL_DIR)
        if thumbnails_needed:
            Thread(target=self.generate_thumbnails, args=thumbnails_needed, daemon=True).start()

        # refresh titlebar to show number of QVideoListItemWidgets
        self.refresh_title()


    def remove(self):
        ''' Removes all selected `QVideoListItemWidget`'s and updates title. '''
        qthelpers.listRemoveSelected(self)
        self.refresh_title()


    def generate_thumbnails(self, *thumbnail_args: tuple[str, str, QVideoListItemWidget], _delete: list = None):
        ''' Generates/saves thumbnails for an indeterminate number of tuples
            consisting of the vide to generate the thumbnail from, a path to
            save the thumbnail to, and the `QVideoListItemWidget` to apply the
            thumbnail to. Thumbnails are generated concurrently, but only 16
            at a time. `constants.FFMPEG` is assumed to be valid. '''

        logger.info(f'Getting thumbnails for {len(thumbnail_args)} file(s)')
        _thumbnail_args = thumbnail_args[:16]                    # only do 16 at a time
        excess = thumbnail_args[16:]
        stage1 = []
        stage2 = []
        to_delete = _delete or []

        # begin ffmpeg process for each file and immediately jump to the next file
        # generate thumbnail from 3 seconds into each file
        for file, thumbnail_path, item_widget in _thumbnail_args:
            temp_path = thumbnail_path.replace('_thumbnail', '_thumbnail_unscaled')
            stage1.append(
                (
                    temp_path,
                    thumbnail_path,
                    item_widget,
                    ffmpeg_async(f'-ss 3 -i "{file}" -vframes 1 "{temp_path}"')
                )                                                # ^ "-ss 3" gets a frame from 3 seconds in
            )

        # wait for each process and then repeat
        # this time we're resizing the thumbnails we just generated
        for temp_path, thumbnail_path, item_widget, process in stage1:
            process.communicate()
            if not os.path.exists(temp_path):                    # thumbnail won't generate if video is <3s long
                ffmpeg(f'-i "{file}" -vframes 1 "{temp_path}"')  # try again, getting the first frame instead
            stage2.append(
                (
                    temp_path,
                    thumbnail_path,
                    item_widget,
                    ffmpeg_async(f'-i "{temp_path}" -vf scale=-1:56 "{thumbnail_path}"')
                )
            )

        # wait once again and apply the thumbnail to its associated widget
        for temp_path, thumbnail_path, item_widget, process in stage2:
            process.communicate()
            item_widget.thumbnail.setPixmap(QtGui.QPixmap(thumbnail_path))
            to_delete.append(temp_path)

        # recursively generate 16 thumbnails at a time until finished
        if excess:
            return self.generate_thumbnails(*excess, _delete=to_delete)

        # delete all temporary files. keep trying for 1.5 seconds if necessary
        attempts = 3
        while to_delete and attempts > 0:
            for index in range(len(to_delete) - 1, -1, -1):
                try: os.remove(to_delete[index])
                except FileNotFoundError: pass
                except: continue
                to_delete.pop(index)
            attempts -= 1
            time.sleep(0.5)


    def refresh_thumbnail_outlines(self):
        for item in self:
            set_style = self.itemWidget(item).thumbnail.setStyleSheet
            if item.toolTip() != gui.video: set_style('QLabel { padding: 4px; }')
            else: set_style('QLabel { padding: 4px;background-color: qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0.573864 rgba(0,255,255,255),stop:1 rgba(0,0,119,255)); }')


    def refresh_title(self):
        ''' Refreshes parent's titlebar to mention the current file count. '''
        count = self.count()
        if count < 2: self.parent().setWindowTitle('Videos to concatenate')
        else:         self.parent().setWindowTitle(f'{count} videos to concatenate')


    def move(self, *, down: bool = False):
        ''' Moves all selected items up or `down`, while maintaining selection.
            Achieved by duplicating selected items and inserting them one index
            away, before deleting the original items. '''
        indexes = sorted(self.row(item) for item in self.selectedItems())
        for old_index in (reversed(indexes) if down else indexes):
            new_index = old_index + (1 if down else -1)
            new_index = min(self.count() - 1, max(0, new_index))
            if old_index != new_index:
                self.add(files=self.takeItem(old_index).toolTip(), index=new_index)
                self.item(new_index).setSelected(True)          # ^ same corrupted item bug affects moving items


    def reverse(self):
        ''' Reverses items in list by cloning list backwards, then
            deleting the original items. Preserves selection. '''
        count = self.count()
        selected_indexes = sorted(count - self.row(item) - 1 for item in self.selectedItems())
        for index in reversed(range(count)):
            self.add(files=self.item(index).toolTip())
            self.takeItem(index)
        for index in selected_indexes:
            self.item(index).setSelected(True)
        self.refresh_title()


    def __iter__(self):
        for i in range(self.count()):
            yield self.item(i)



# ------------------------------------------
# "Add text" Dialog Widgets
# ------------------------------------------
class QTextOverlayPreview(QtW.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overlays: list[QTextOverlay] = []
        self.selected: QTextOverlay = None                      # TODO ability to select multiple at once
        self.ratio: float = None
        self._draggingOffset: QtCore.QPoint = None
        self._dragging: bool = False


    #def overlayPosToPreviewPos(self, overlay: QTextOverlay) -> QtCore.QPointF:
    #    return overlay.pos * self.ratio


    def getOverlayInRange(self, pos: QtCore.QPoint, _range: int = 30) -> QTextOverlay:
        ''' Returns the index of the closest text overlay to `pos`,
            if any are within `_range` pixels, otherwise None. '''
        min_dist = 1000
        min_overlay = None
        for overlay in self.overlays:
            #font = overlay.font
            #font.setPointSize(overlay.size)

            overlay.font.setPointSize(overlay.size * self.ratio)
            local_pos = overlay.pos * self.ratio
            text_size = QtGui.QFontMetrics(overlay.font).size(0, overlay.text)
            text_rect = QtCore.QRect(local_pos.toPoint(), text_size)

            #text_size = QtGui.QFontMetrics(font).size(0, overlay.text)
            #bottom_right = QtCore.QPoint(local_pos.x() + text_size.width(), local_pos.y() + text_size.height())
            #if QtCore.QRect(local_pos.toPoint(), bottom_right).contains(pos):
            if text_rect.contains(pos):
                min_dist = 0
                min_overlay = overlay

            ##dist = abs(pos.x() - point.x()) + abs(pos.y() - point.y())     # TODO: verify that manhattanLength is actually better than this
            #dist = (pos - (overlay.pos * self.ratio)).manhattanLength()     # https://doc.qt.io/qt-5/qpoint.html#manhattanLength
            #print('DISTANCE', dist)
            #if dist < min_dist:
            #    min_dist = dist
            #    min_overlay = overlay
        return None if min_dist > _range else min_overlay


    def mousePressEvent(self, event: QtGui.QMouseEvent):
        try:
            if event.button() == Qt.LeftButton:
                parent = self.parent()
                overlay = self.getOverlayInRange(event.pos())
                print('OVERLAY IN RANGE?', overlay)

                if not self.selected.text.strip():
                    try: self.overlays.pop(self.overlays.index(self.selected))
                    except: pass

                if not overlay:
                    #overlay = QTextOverlay(parent.comboFont.currentFont(), parent.spinFontSize.value())
                    overlay = QTextOverlay(parent)
                    overlay.pos = QtCore.QPointF(event.pos()) / self.ratio
                    self.overlays.append(overlay)
                    parent.text.setFocus(True)

                if overlay is not self.selected:
                    self.selected = overlay
                    parent.text.setPlainText(overlay.text)
                    parent.comboFont.setCurrentFont(overlay.font)
                    parent.spinFontSize.setValue(overlay.size)
                    parent.spinBoxWidth.setValue(overlay.bgwidth)
                    parent.buttonColorFont.setStyleSheet('QPushButton {background-color: rgba' + str(overlay.color.getRgb()) + ';border: 1px solid black;}')
                    parent.buttonColorBox.setStyleSheet('QPushButton {background-color: rgba' + str(overlay.bgcolor.getRgb()) + ';border: 1px solid black;}')
                    parent.buttonColorShadow.setStyleSheet('QPushButton {background-color: rgba' + str(overlay.shadowcolor.getRgb()) + ';border: 1px solid black;}')
                    {
                        Qt.AlignLeft:    parent.buttonAlignLeft,
                        Qt.AlignHCenter: parent.buttonAlignCenter,
                        Qt.AlignRight:   parent.buttonAlignRight
                    }[overlay.alignment].setChecked(True)

                self._draggingOffset = event.pos() - (overlay.pos * self.ratio)
                self._dragging = True
                self.update()

        except:
            print('mousepress', format_exc())


    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        try:
            if event.buttons() == Qt.LeftButton and self._dragging:
                centered = False
                overlay = self.selected
                local_pos = event.pos() - self._draggingOffset

                # hold ctrl for free dragging
                if event.modifiers() & Qt.ControlModifier:
                    overlay.centered_horizontally = False
                    overlay.centered_vertically = False
                    overlay.pos = local_pos / self.ratio

                # otherwise, the text is snapped to an axis if close enough
                else:
                    #text_size = QtGui.QFontMetrics(overlay.font).size(0, overlay.text.strip('\n'))
                    text_size = QtGui.QFontMetrics(overlay.font).size(0, overlay.text)
                    text_pos_rect = QtCore.QRect(local_pos.toPoint(), text_size)
                    text_center = text_pos_rect.center()
                    horizontal_center = self.width() / 2
                    vertical_center = self.height() / 2

                    # check if we should snap to the horizontal center (locked x)
                    if abs(text_center.x() - horizontal_center) < 20:
                        text_pos_rect.moveCenter(QtCore.QPoint(horizontal_center, text_center.y()))
                        overlay.centered_horizontally = True
                        centered = True
                    else:
                        overlay.centered_horizontally = False

                    # check if we should snap to the vertical center (locked y)
                    if abs(text_center.y() - vertical_center) < 20:
                        text_pos_rect.moveCenter(QtCore.QPoint(text_pos_rect.center().x(), vertical_center))
                        overlay.centered_vertically = True
                        centered = True
                    else:
                        overlay.centered_vertically = False

                    # update text overlay position depending on if we snapped to a center or not
                    if centered:
                        overlay.pos = QtCore.QPointF(text_pos_rect.x(), text_pos_rect.y()) / self.ratio
                    else:
                        overlay.pos = local_pos / self.ratio
                self.update()                                   # manually update
        except: print('mousemove', format_exc())


    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        local_pos = self.selected.pos * self.ratio
        text_size = QtGui.QFontMetrics(self.selected.font).size(0, self.selected.text)
        text_pos_rect = QtCore.QRect(local_pos.toPoint(), text_size)
        if not self.rect().contains(text_pos_rect.center()):
            logging.info('Text overlay dragged out of the preview, deleting...')
            try: self.overlays.pop(self.overlays.index(self.selected))
            except: pass

        self._dragging = False
        self.update()                                           # manually update


    def paintEvent(self, event: QtGui.QPaintEvent):
        super().paintEvent(event)                               # perform built-in paint immediately so we can paint on top

        p = QtGui.QPainter()
        p.begin(self)
        try:
            for overlay in self.overlays:
                text = overlay.text.strip('\n')

                #size = settings.spinHoverFontSize.value()   # TODO use currentFontChanged signals + more for performance? not needed?
                #font = settings.comboHoverFont.currentFont()

                #font = overlay.family
                #font.setPointSize(overlay.size)
                #p.setFont(font)
                #color = overlay.color
                #color.setAlpha(overlay.alpha)
                #p.setPen(color)
                #overlay.font.setPointSize(overlay.size * self.ratio)
                #overlay.font.setPointSize(overlay.size * self.ratio)

                #if overlay.size % 2 == 0:
                #    overlay.font.setPointSize(overlay.size * self.ratio)
                #else:
                #    overlay.font.setPixelSize(overlay.size * self.ratio)

                # FFmpeg uses pixel size
                overlay.font.setPixelSize(overlay.size * self.ratio)

                #overlay.color.setAlpha(overlay.alpha)
                p.setFont(overlay.font)
                p.setPen(overlay.color)
                #p.setLine
                fm = p.fontMetrics()

                #color = QtGui.QColor(overlay.color)
                #color.setAlpha(overlay.alpha)
                #p.setPen(color)

                local_pos = overlay.pos * self.ratio
                text_size = fm.size(0, text)
                #text_pos_rect = QtCore.QRect(local_pos.toPoint(), text_size)
                text_pos_rect = QtCore.QRectF(local_pos, QtCore.QSizeF(text_size))
                print('DRAWING AT!!', local_pos, text_pos_rect.center().x(), self.width() / 2)

                ##local_pos.setY(self.height() - (self.height() - overlay.size) / 2)
                ##p.drawText(local_pos, text)
                ##text_width = QtGui.QFontMetrics(font).width(text)
                ##text_size = QtGui.QFontMetrics(font).size(0, text)
                #text_size = fm.size(0, text)
                ##bottom_right = QtCore.QPointF(local_pos.x() + text_size.width(), local_pos.y() + text_size.height())
                ##p.drawText(QtCore.QRect(local_pos, bottom_right), 0, text)
                ##bottom_right = QtCore.QPoint(local_pos.x() + text_size.width(), local_pos.y() + text_size.height())
                ##text_rect = QtCore.QRect(local_pos.toPoint(), bottom_right)
                #text_rect = QtCore.QRect(local_pos.toPoint(), text_size)

                #text_rect = fm.boundingRect(text)

                #text_boundary_rect = fm.tightBoundingRect(text)
                ##text_rect.setHeight(QtGui.QFontMetrics(overlay.font).ascent())
                #print('tight:', text_boundary_rect)

                #text_boundary_rect.translate(local_pos.toPoint())
                #text_pos_rect.adjust(text_boundary_rect.x(), text_boundary_rect.y(), 0, 0)
                #text_pos_rect.translate(-text_boundary_rect.x() // 2, text_boundary_rect.y() // 2)
                #text_boundary_rect.moveTo(local_pos.toPoint())

                ##x = QtCore.QPoint(local_pos.x() + text_boundary_rect.x(), local_pos.y() - text_boundary_rect.y())
                #x = QtCore.QPoint(local_pos.x() + text_boundary_rect.x(), local_pos.y() + fm.descent() + 1)
                #text_boundary_rect.moveTo(x)
                ##text_boundary_rect.translate(text_boundary_rect.x(), text_boundary_rect.y())

                # draw background first (or a simple outline and snap-lines if we're dragging)
                #if self._dragging and overlay is self.selected: p.drawRect(text_boundary_rect)
                #else: p.fillRect(text_boundary_rect, overlay.bgcolor)
                if self._dragging and overlay is self.selected:
                    p.drawRect(text_pos_rect)
                    if overlay.centered_horizontally:
                        p.drawLine(self.width() / 2, 0, self.width() / 2, self.height())
                    if overlay.centered_vertically:
                        p.drawLine(0, self.height() / 2, self.width(), self.height() / 2)
                else:
                    p.fillRect(text_pos_rect, overlay.bgcolor)

                # draw text over background (drop-shadow first)
                if overlay.shadowx or overlay.shadowy:
                    p.setPen(overlay.shadowcolor)
                    p.drawText(text_pos_rect.translated(overlay.shadowx, overlay.shadowy), overlay.alignment | Qt.AlignTop, text)
                    p.setPen(overlay.color)
                p.drawText(text_pos_rect, overlay.alignment | Qt.AlignTop, text)

                #richtext = text.replace('\n', '<br>')
                #richertext = f'<p style="line-height:0.8">{richtext}</p>'
                #p.drawStaticText(local_pos, QtGui.QStaticText(richertext))
                #td = QtGui.QTextDocument()
                #td.setHtml(text)
                #td.drawContents(p, text_pos_rect)
        except:
            print('TEXTADDPAINT', format_exc())
        finally:
            p.end()




class QTextOverlay:
    def __init__(self, dialog):
        self.text = ''
        self.pos = QtCore.QPointF(0.0, 0.0)
        self.font: QtGui.QFont = dialog.comboFont.currentFont()
        self.size: int = dialog.spinFontSize.value()
        self.color = self.get_color_from_stylesheet(dialog.buttonColorFont.styleSheet())
        self.bgcolor = self.get_color_from_stylesheet(dialog.buttonColorBox.styleSheet())
        self.bgwidth: int = dialog.spinBoxWidth.value()
        self.shadowcolor = self.get_color_from_stylesheet(dialog.buttonColorShadow.styleSheet())
        self.shadowx = dialog.spinShadowX.value()
        self.shadowy = dialog.spinShadowY.value()
        self.alignment: Qt.Alignment = {
            dialog.buttonAlignLeft:   Qt.AlignLeft,
            dialog.buttonAlignCenter: Qt.AlignHCenter,
            dialog.buttonAlignRight:  Qt.AlignRight
        }[dialog.buttonGroup.checkedButton()]
        self.centered_horizontally = False
        self.centered_vertically = False


    def get_color_from_stylesheet(self, stylesheet: str) -> QtGui.QColor:
        ''' Returns the first "rgba()" in a `stylesheet` as a `QColor`. '''
        start_index = stylesheet.find('rgba(') + 5
        end_index = stylesheet.find(');', start_index)
        rgba = stylesheet[start_index:end_index].replace(' ', '').split(',')
        return QtGui.QColor(*(int(v) for v in rgba))



# ------------------------------------------
# Utility Widgets
# ------------------------------------------
class QColorPickerButton(QtW.QPushButton):
    ''' A button representing a color that may be clicked to display and handle
        a color picker. Clicking and dragging the button will turn the mouse into
        an eyedropper tool, allowing users to select a color from their screen.
        Adjusts its stylesheet and tooltip to display the color it represents.
        Custom stylesheets & tooltips may be used as a base and are accessible/
        editable as properties.

        Emits a custom `colorChanged` signal upon successfully changing
        the color. Uses white text for dark colors. Scrolling over the button
        will adjust its color's alpha value, if the alpha channel is enabled.
        Middle-clicking the button will toggle the alpha (if enabled) between
        0 and the most recent non-0 value.

        NOTE: `parseStyleSheet()` must be manually called to initialize the
        button's color. The button's base stylesheet must include the button's
        `background-color` attribute (and it must be the first attribute of the
        first styled widget) before `parseStyleSheet()` may be called.

        NOTE: This class is designed around using `QColor.getRgb()` instead of
        `QColor.name()`, with stylesheets using "rgb(r,g,b)/rbga(r,g,b,a)"
        formatting instead of #RRGGBB/#AARRGGBB. '''

    colorChanged = QtCore.pyqtSignal(QtGui.QColor)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked.connect(self.showColorPicker)
        self.color: QtGui.QColor = None
        self.alphaEnabled = True
        self.storedAlpha = 150
        self.toolTipBase = ''
        self.styleSheetSuffix = ''
        self._timer: int = None
        self._dragging = False
        self._predragColor: QtGui.QColor = None
        self._parentCursor: Qt.CursorShape = None


    def setAlphaEnabled(self, enabled: bool):
        self.alphaEnabled = enabled


    def setStoredAlpha(self, alpha: int):
        self.storedAlpha = alpha


    def setToolTipBase(self, tooltip: str):
        self.toolTipBase = tooltip


    def parseStyleSheet(self):
        ''' Initialize this button's color by parsing its stylesheet. This may
            be called as many times as desired, but realisitically only needs
            to be done once. '''
        stylesheet = self.styleSheet()

        # Example: 'QPushButton { background-color: rgba(255,255,255,255); }'
        start = stylesheet.find('background-color: rgb') + 22
        if start == 21:
            return
        if stylesheet[start - 1] == 'a':
            start += 1
        end = stylesheet.find(')', start)
        self.styleSheetSuffix = stylesheet[end + 1:]            # strip ')' from start of suffix
        color = self.setColorString(stylesheet[start:end])
        self.storedAlpha = color.alpha() or self.storedAlpha


    def setColor(self, color: QtGui.QColor, enableAlpha: bool = None) -> str:
        ''' Sets `self.color` to `color`, updates the tooltip/stylesheet, emits
            a `self.colorChanged` signal, and returns the new string `color`
            represents. `self.alphaEnabled` will be updated if `enableAlpha`
            is provided. '''
        self.color = color

        # shortcut for toggling alpha channel
        if enableAlpha is not None:
            self.alphaEnabled = enableAlpha

        # if alpha is enabled, change stylesheet/tooltip accordingly
        if self.alphaEnabled:
            prefix = 'QPushButton{background-color:rgba'
            tooltip_suffix = '\nClick/drag for color picker.\nMiddle-click to toggle alpha.\nScroll to increment alpha.'
        else:
            prefix = 'QPushButton{background-color:rgb'
            tooltip_suffix = ''

        # get color string and update tooltip/stylesheet
        color_string = str(color.getRgb())
        self.setToolTip(f'{self.toolTipBase} {color_string}{tooltip_suffix}')

        # -> use white text if button is too dark - https://en.wikipedia.org/wiki/HSL_and_HSV
        if color.value() < 50 and color.alpha() > 100:
            self.setStyleSheet(f'{prefix}{color_string};color:white{self.styleSheetSuffix}')
        else:
            self.setStyleSheet(f'{prefix}{color_string}{self.styleSheetSuffix}')

        # emit signal and return the string version of the provided `color`
        self.colorChanged.emit(color)
        return color_string


    def setColorString(self, string: str) -> QtGui.QColor:
        ''' Converts `string` to a `QColor` if possible, assigns it
            to `self.color`, updates the tooltip/stylesheet, emits
            a `self.colorChanged` signal, and returns the new color.

            `string` should loosely follow the format of "r,g,b,a".
            `self.alphaEnabled` will be updated to match whether
            or not `color_string` included an alpha value. '''

        # strip opening/closing parenthesis and remove all spaces
        color_string = string.strip('()').replace(' ', '')
        color_parts = color_string.split(',')
        color = self.color = QtGui.QColor(*(int(v) for v in color_parts))

        if len(color_parts) == 4:
            self.alphaEnabled = True
            prefix = 'QPushButton{background-color:rgba'
            tooltip_suffix = '\nClick/drag for color picker.\nMiddle-click to toggle alpha.\nScroll to increment alpha.'
        else:
            self.alphaEnabled = False
            prefix = 'QPushButton{background-color:rgb'
            tooltip_suffix = ''

        self.setToolTip(f'{self.toolTipBase} ({color_string.replace(",", ", ")}){tooltip_suffix}')
        if color.value() < 50 and color.alpha() > 100:          # use white text if button is too dark
            self.setStyleSheet(f'{prefix}({color_string});color:white{self.styleSheetSuffix}')
        else:
            self.setStyleSheet(f'{prefix}({color_string}){self.styleSheetSuffix}')

        self.colorChanged.emit(color)
        return color


    def showColorPicker(self, initialColor: QtGui.QColor = None, alpha: bool = None) -> QtGui.QColor | None:
        ''' Shows Qt's native color picking dialog set to `self.color`
            by default and showing the alpha channel if `self.alphaEnabled`
            is True, with `initialColor` and `alpha` acting as overrides if
            provided (`alpha` will also update `self.alphaEnabled` on success).
            If a valid color is chosen, `self.setColor()` is called and the new
            color is returned. Otherwise, the starting color is returned. '''
        initialColor = initialColor or self.color
        alpha = self.alphaEnabled if alpha is None else alpha

        # NOTE: F suffix is Float -> values are represented from 0-1 (e.g. getRgb() becomes getRgbF())
        try:
            picker = QtW.QColorDialog()
            #for index, default in enumerate(self.defaults):
            #    picker.setCustomColor(index, QtGui.QColor(*default))

            # open color picker with appropriate arguments
            kwargs = dict(initial=initialColor, parent=self.parent(), title='Picker? I hardly know her!')
            if alpha: color = picker.getColor(**kwargs, options=QtW.QColorDialog.ShowAlphaChannel)
            else:     color = picker.getColor(**kwargs)

            # return the starting color if selected color is invalid
            if not color.isValid():
                return initialColor

            # update/return our selected color and update `self.alphaEnabled`
            self.alphaEnabled = alpha
            self.setColor(color)
            return color
        except:
            logger.warning(f'(!) OPEN_COLOR_PICKER FAILED: {format_exc()}')
            return initialColor


    def wheelEvent(self, event: QtGui.QWheelEvent):
        ''' Increments `self.color`'s alpha value if possible:
            5 by default, 15 if `Ctrl` is held, 1 if `Alt` is held. '''
        if not self.alphaEnabled:
            return

        mod = event.modifiers()
        if mod & Qt.AltModifier:
            self.color.setAlpha(self.color.alpha() + (1 if event.angleDelta().x() > 0 else -1))
        else:
            delta = 15 if mod & Qt.ControlModifier else 5
            self.color.setAlpha(self.color.alpha() + (delta if event.angleDelta().y() > 0 else -delta))
        self.setColor(self.color)


    def mousePressEvent(self, event: QtGui.QMouseEvent):
        ''' Toggles the current color's alpha between 0 and
            the most recent non-zero alpha on middle-click. '''
        if event.button() == Qt.MiddleButton and self.alphaEnabled:
            color = self.color
            alpha = color.alpha()
            if alpha:                       # only store/update alpha if it's non-zero
                self.storedAlpha = alpha
                color.setAlpha(0)
            else:
                color.setAlpha(self.storedAlpha)
            self.setColor(color)
        else:
            super().mousePressEvent(event)


    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        ''' Updates our color to whatever pixel on the screen the mouse is
            currently hovering over, if we're left-click dragging. If we're
            dragging but left-click isn't the sole button being held, the
            eyedropper is cancelled. Overrides the cursor to a precision
            cursor while color picking if we're not hovering over
            ourselves, otherwise a warning cursor is used. '''
        # there are many ways this can be done (like with timers), but just spamming it is honestly fine
        # NOTE: override-cursors must be used as a widget's normal cursor is not honored while dragging
        if event.buttons() == Qt.LeftButton:
            if self._dragging:
                if self.rect().contains(event.pos()):       # NOTE: self.underMouse() does not work...
                    if self.color != self._predragColor:    # ...here, even with `setMouseTracking(True)`
                        self.setColor(self._predragColor)
                    qthelpers.setCursor(Qt.ForbiddenCursor, conditionally=True)
                else:
                    new_color = qthelpers.getPixelColor(alpha=self.color.alpha())
                    if self.color != new_color:
                        self.setColor(new_color)
                    qthelpers.setCursor(Qt.CrossCursor, conditionally=True)
                return

            self._predragColor = self.color
            self._dragging = True

        # cancel if anything other than solely left-click is held while moving
        elif self._dragging:                                # NOTE: these clicks cannot be detected...
            self.setColor(self._predragColor)               # ...in `mousePressEvent`() while dragging
            qthelpers.resetCursor()
            self._dragging = False


    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        ''' Finalizes and disables the eyedropper (and its cursor) if it
            was active, cancelling it if we released over ourselves. '''
        if self._dragging and event.button() == Qt.LeftButton:
            # reset color if we released over the button (NOTE: self.underMouse() does not work here)
            # otherwise, get pixel again to ensure we have the true final color under our mouse
            if self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())):
                self.setColor(self._predragColor)
            else:
                self.setColor(qthelpers.getPixelColor(alpha=self.color.alpha()))

            self._dragging = False
            qthelpers.resetCursor()
        else:
            return super().mouseReleaseEvent(event)


    def keyPressEvent(self, event: QtGui.QKeyEvent):
        ''' Cancels the eyedropper if Esc is pressed. '''
        if self._dragging and event.key() == Qt.Key_Escape:
            self.setColor(self._predragColor)
            qthelpers.resetCursor()
            self._dragging = False
        else:
            return super().keyPressEvent(event)




class QKeySequenceFlexibleEdit(QtW.QKeySequenceEdit):
    ''' `QKeySequenceEdit` with support for ignorable sequences, limiting to a
        single sequence, custom edit delays, clearing focus/sequences with Esc,
        a clear button, and easy access to the underlying `QLineEdit`. '''
    def __init__(
        self,
        *args,
        singleSequence: bool = True,
        escClearsFocus: bool = True,
        escClearsSequence: bool = True,
        clearButton: bool = False,
        delay: int = 200,
        ignored: tuple = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._timerID = None
        self._editing = False
        self.lineEdit = self.children()[0]
        self.setClearButtonEnabled(clearButton)
        self.singleSequence = singleSequence
        self.escClearsFocus = escClearsFocus
        self.escClearsSequence = escClearsSequence
        self.editDelay = delay
        self.ignoredSequences = (           # like the other utility widgets, we manually set this here for simplicity
            QtGui.QKeySequence('Ctrl+O'),
            QtGui.QKeySequence('Ctrl+S'),
            QtGui.QKeySequence('Ctrl+Shift+S'),
            QtGui.QKeySequence('Alt+Q')
        )


    def setSingleSequence(self, enabled: bool): self.singleSequence = enabled
    def setEscClearsFocus(self, enabled: bool): self.escClearsFocus = enabled
    def setEscClearsSequence(self, enabled: bool): self.escClearsSequence = enabled
    def setEditDelay(self, delay: int): self.editDelay = delay
    def setIgnoredSequences(self, *args: QtGui.QKeySequence): self.ignoredSequences = args


    def setClearButtonEnabled(self, enabled: bool):
        ''' Toggles/connects the clear button for the underlying `QLineEdit`
            (`self.lineEdit`). When disabling, the `QAction` and `QToolButton`
            that make up the clear button are automatically discarded by Qt. '''
        self.lineEdit.setClearButtonEnabled(enabled)
        if enabled:
            self.lineEdit.children()[1].triggered.connect(self.clear)


    def clear(self):
        ''' Overrides clearing to manually emit `keySequenceChanged` and
            `editingFinished` signals (assuming it was not called as part of an
            editing timer), allowing clearing to actually trigger updates. '''
        super().clear()
        if self._timerID is None:           # timerID means a custom timer active
            self.keySequenceChanged.emit(self.keySequence())
            self.editingFinished.emit()


    def keyPressEvent(self, event: QtGui.QKeyEvent):
        ''' If `self.escClearsFocus` is set, focus is cleared and returned
            after Esc is pressed. If `self.singleSequence` is set, sequences
            are truncated to their last sequence, and ", ..." is stripped from
            the underlying `QLineEdit` (`self.lineEdit`). '''
        if event.key() == Qt.Key_Escape:                        # clear text/focus on Esc
            if self.escClearsSequence: self.clear()
            if self.escClearsFocus: return self.clearFocus()    # do NOT use event.ignore() here

        if self.singleSequence:             # single sequence only
            super().keyPressEvent(event)    # run built-in keyPressEvent first (this emits keySequenceChanged)
            if self.keySequence().count() > 1:
                self.setKeySequence(QtGui.QKeySequence(self.keySequence()[-1]))  # truncate sequence to last sequence
            return self.lineEdit.setText(self.keySequence().toString())          # strip ", ..." from underlying QLineEdit and return

        elif self.editDelay != 1000:        # not a single sequence, but a custom editing delay (reimplement timer behavior)
            if self._timerID is None:       # no timer running + not actively editing -> clear existing sequence for incoming sequence
                if not self._editing:
                    self.clear()
            else:                           # timer running + actively editing the sequence -> kill/reset timer (we're still editing)
                self._timerID = self.killTimer(self._timerID)
            self._editing = True            # mark that we're actively editing
        super().keyPressEvent(event)        # run built-in keyPressEvent last (this emits the first keySequenceChanged signal)


    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        ''' Clears the entire field if it contains an ignored sequence. If
            `self.singleSequence` is set, the `editingFinished` signal is
            emitted immediately and the normal timer is skipped. Otherwise,
            if a custom `self.editDelay` is set, then `QKeySequenceEdit`'s
            edit-finished-timer is reimplemented in `timerEvent`. '''
        if self.ignoredSequences and self.keySequence() in self.ignoredSequences:
            self.clear()

        if self.singleSequence:
            return self.editingFinished.emit()
        elif self.editDelay != 1000:
            self._editing = False
            if self._timerID is not None:
                self.killTimer(self._timerID)
            self._timerID = self.startTimer(self.editDelay, Qt.CoarseTimer)
        else:
            return super().keyReleaseEvent(event)


    def timerEvent(self, event: QtCore.QTimerEvent):
        ''' Finishes the reimplementation of `QKeySequenceEdit`'s
            edit-finished-timer for custom `self.editDelay` values.
            This doesn't fire if `self.singleSequence` is set. '''
        if self._timerID is not None:                           # timerID means a custom timer active
            self.keySequenceChanged.emit(self.keySequence())    # emit second keySequenceChanged signal
            self.editingFinished.emit()
            self._timerID = self.killTimer(self._timerID)       # kill timer and remove ID
            self.lineEdit.setText(self.keySequence().toString())
        return super().timerEvent(event)                        # ^ strip ", ..." from underlying QLineEdit


    def toString(
        self,
        format: QtGui.QKeySequence.SequenceFormat = QtGui.QKeySequence.SequenceFormat.PortableText
    ) -> str:
        ''' Returns the embedded key sequence as a string. '''
        return self.keySequence().toString(format)


    def __repr__(self) -> str:
        ''' Returns the embedded key sequence as a string. '''
        return self.keySequence().toString()




class QWidgetPassthrough(QtW.QWidget):
    ''' `QWidget` which passes desired keypresses to its parent. Specific
        characters can be ignored, and specific categories (such as letters,
        integers, and punctuation) can be toggled. The option to clear or
        optionally "pass" focus when Esc is pressed is also included. '''
    base = QtW.QWidget      # TODO semi-bandaid fix. without this, we can't access the correct keyPressEvent in subclasses(...?)

    # TODO make the getting/setting syntax fully Qt-like or make it fully normal
    def __init__(
        self,
        *args,
        proxy: QtW.QWidget = None,
        escClearsFocus: bool = True,
        passFocus: bool = True,
        alpha: bool = True,
        punctuation: bool = True,
        numeric: bool = False,
        ignored: tuple[int] = tuple(),
        **kwargs
    ):
        super().__init__(*args, **kwargs)   # normally these kwargs are True, False, False, False
        self.escClearsFocus = escClearsFocus
        self.passFocus = passFocus
        self.ignoreAlpha = alpha
        self.ignorePunctuation = punctuation
        self.ignoreNumeric = numeric
        self.ignoredKeys = ignored
        if proxy:
            self._proxyWidget = proxy
            self._proxyWidgetIsParent = False
        else:
            self._proxyWidget = self.parent()
            self._proxyWidgetIsParent = True

    def proxyWidget(self) -> QtW.QWidget:   # pointless, but consistent with Qt
        return self._proxyWidget

    def setProxyWidget(self, widget: QtW.QWidget):
        ''' Sets `self.proxyWidget` to `widget`, which will receive any
            keypresses from this widget that would otherwise be discarded.
            If `widget` is our parent, the parent will be tracked until this
            method is called again with a unique `widget`. '''
        self._proxyWidget = widget
        self._proxyWidgetIsParent = widget is self.parent()

    def setParent(self, parent: QtW.QWidget):
        ''' Captures setParent and sets `proxyWidget` to the new `parent`
            if our proxy widget and parent are expected to be linked. '''
        super().setParent(parent)
        if self._proxyWidgetIsParent:
            self._proxyWidget = parent

    def setIgnoreAll(self, ignore: bool):
        self.ignoreAlpha = ignore
        self.ignorePunctuation = ignore
        self.ignoreNumeric = ignore

    def setEscClearsFocus(self, enabled: bool): self.escClearsFocus = enabled
    def setPassFocus(self, enabled: bool): self.passFocus = enabled
    def setIgnoreAlpha(self, ignore: bool): self.ignoreAlpha = ignore
    def setIgnorePunctuation(self, ignore: bool): self.ignorePunctuation = ignore
    def setIgnoreNumeric(self, ignore: bool): self.ignoreNumeric = ignore
    def setIgnoredKeys(self, *args: int): self.ignoredKeys = args

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> QtGui.QKeyEvent:
        key = event.key()                   # V esc (clear/pass focus)
        if self.escClearsFocus and key == 16777216:
            if self.passFocus: return self._proxyWidget.setFocus()
            else: return self.clearFocus()
        text = event.text()
        if (
            key in self.ignoredKeys
            or (self.ignoreAlpha and text.isalpha())
            or (self.ignorePunctuation and text in '!"#$%&\'()*+, -./:;<=>?@[\\]^_`{|}~')
            or (self.ignoreNumeric and text.isnumeric())
        ):
            return self._proxyWidget.keyPressEvent(event)
        return self.base.keyPressEvent(self, event)




class QSpinBoxPassthrough(QtW.QSpinBox, QWidgetPassthrough): base = QtW.QSpinBox
class QDockWidgetPassthrough(QtW.QDockWidget, QWidgetPassthrough): base = QtW.QDockWidget
class QLineEditPassthrough(QtW.QLineEdit, QWidgetPassthrough): base = QtW.QLineEdit




class QDraggableWindowFrame(QtW.QFrame):
    ''' `QFrame` which moves a separate widget called `dragTarget` when dragging
        on empty spaces using `button` (if None, any button works). `dragTarget`
        is moved relative to this frame, and does not move while fullscreen or
        maximized. If no `dragTarget` is specified, `parent()` is used instead
        and persists through `setParent()` until a unique dragTarget is set. '''
    def __init__(
        self,
        *args,
        dragTarget: QtW.QWidget = None,
        button: int = Qt.LeftButton,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        if dragTarget:
            self._dragTarget = dragTarget
            self._dragTargetIsParent = False
        else:
            self._dragTarget = self.parent()
            self._dragTargetIsParent = True
        self._button = button
        self._validDrag = False
        self._draggingOffset: QtCore.QPoint = None

    def dragTarget(self) -> QtW.QWidget:    # pointless, but consistent with Qt
        return self._dragTarget

    def setDragTarget(self, widget: QtW.QWidget):
        ''' Manually sets `dragTarget`. The drag target is the
            `widget` that gets moved while dragging `self`. '''
        self._dragTarget = widget
        self._dragTargetIsParent = widget is self.parent()

    def button(self) -> int:                # pointless, but consistent with Qt
        return self._button

    def setButton(self, button: int):
        self._button = button

    def setParent(self, parent: QtW.QWidget):
        ''' Captures `QFrame.setParent()` and sets `parent` as our
            new `self._dragTarget` if our drag target and parent are
            expected to be linked (`self._dragTargetIsParent`). '''
        super().setParent(parent)
        if self._dragTargetIsParent:
            self._dragTarget = parent

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        ''' Confirms that a mouse press is valid for dragging and obtains the
            offset between the click and the top-left corner of our target.
            Ignores clicks while our target is fullscreened or maximized. This
            event does not fire if we've clicked one of our child widgets. '''
        valid_button = self._button is None or event.button() == self._button
        self._validDrag = not self._dragTarget.isFullScreen() and not self._dragTarget.isMaximized() and valid_button
        self._draggingOffset = event.globalPos() - self._dragTarget.pos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        ''' If valid, moves our target relative to our mouse's
            movement using the offset obtained in `mousePressEvent`. '''
        if not self._validDrag: return      # don't move dragTarget if we're dragging a child widget
        self._dragTarget.move(event.globalPos() - self._draggingOffset)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        self._validDrag = False



# ------------------------------------------
# Unfinished/Unused Widgets
# ------------------------------------------
''' Currently unfinished. Intended to "simplify" the cropping process as well as
    draw the cropping coordinates/border over the frames, instead of underneath. '''
#class QCropFrame(QtW.QFrame):
#    def __init__(self, parent, vlc, index, alpha, *args, **kwargs):
#        super().__init__(parent, *args, **kwargs)
#        self.vlc = vlc
#        self.index = index
#        self.mousePressEvent = vlc.mousePressEvent
#        self.mouseMoveEvent = vlc.mouseMoveEvent
#        self.mouseReleaseEvent = vlc.mouseReleaseEvent
#        self.mouseDoubleClickEvent = vlc.mouseDoubleClickEvent
#        self.setMouseTracking(True)
#        self.setVisible(True)
#        self.setStyleSheet(f'background: rgba(0, 0, 0, {alpha})')
#        #self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
#
#
#    def paintEvent(self, event: QtGui.QPaintEvent):
#        super().paintEvent(event)
#        p = QtGui.QPainter()
#        p.begin(self)
#
#        white = QtGui.QColor(255, 255, 255)
#        black = QtGui.QColor(0, 0, 0)
#
#        p.setPen(QtGui.QPen(white, 6, Qt.SolidLine))
#        p.setBrush(white)
#        p.setFont(QtGui.QFont('Segoe UI Light', 10))
#        print('mapping...', self.vlc.selection, self.mapFrom, self.vlc)
#        print(self.mapFrom(self.vlc, self.vlc.selection[0]))    # mapFrom crashes with no errors
#        s = tuple(self.mapFrom(self.vlc, point) for point in self.vlc.selection)
#        print(1, self.vlc.selection)
#        print(2, s)
#        try:
#            # draw thin border around video (+2 and -4 to account for size-6 pen)
#            p.drawRect(s[0].x() + 2,
#                       s[0].y() + 2,
#                       s[1].x() - s[0].x() - 4,
#                       s[2].y() - s[0].y() - 4)
#
#            # draw handle and coordinates for each corner
#            index = self.index
#            point = s[index]
#            fpoint = self.vlc.last_factored_points[index] = self.vlc.factor_point(point)
#            #p.drawRect(point.x() - 3, point.y() - 3, 5, 5)
#            text = f'({fpoint.x():.0f}, {fpoint.y():.0f})'
#            p.setPen(black)                                                                    # set color to black
#            p.drawText(point.x() + 1, point.y() + self.vlc.text_y_offsets[index] + 1, text)    # draw shadow first
#            p.setPen(QtGui.QPen(white, 6, Qt.SolidLine))                                # set color to white
#            p.drawText(point.x(), point.y() + self.vlc.text_y_offsets[index], text)            # draw actual text over shadow
#            p.drawPoint(point.x(), point.y())                                                  # size-6 point to represent handles
#        except: print(format_exc())
#        p.end()
