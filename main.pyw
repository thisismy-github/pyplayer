r'''  >>> thisismygithub - 10/31/21 <<<
    ____        ____  __
   / __ \__  __/ __ \/ /___ ___  _____  _____
  / /_/ / / / / /_/ / / __ `/ / / / _ \/ ___/
 / ____/ /_/ / ____/ / /_/ / /_/ /  __/ /
/_/    \__, /_/   /_/\__,_/\__, /\___/_/
      /____/              /____/

      >>> thisismygithub - 10/31/21 <<<

icon sources/inspirations https://www.pinclipart.com/maxpin/hxThoo/ + https://www.hiclipart.com/free-transparent-background-png-clipart-vuclz
https://youtu.be/P1qMAupb2_Y?t=2461 VLC devs talk about Qt problems -> making two windows actually behave as one?
TODO: update boilerplate code with last_window_size/pos changes
TODO: need a way to deal with VLC registry edits
TODO: move show_color_picker and other browse dialogs + indeterminate_progress decorator + setCursor(app) and resetCursor(app) to qthelpers/util?
TODO: better/more fleshed-out themes
TODO: can't change themes while minimized to system tray (warn with tray icon?)
TODO: live-themes advanced option? (button that auto-refreshes themes every half-second for theme developers)
TODO: make more "modern" looking icon like VLC's ios app icon?
TODO: event_manager -> "no signature found for builtin <built-in method emit of PyQt5.QtCore.pyqtBoundSignal object"
TODO: getting the padding of the QSlider groove
TODO: better/more fleshed out sliderVolume (dedicated subclass?)
TODO: cropping finally finished. potential improvements:
        - ctrl-drag for square crops (not finished right now, especially near edges)
        - draw text on the QFrames, not on player (requires own paintEvent, ideally)
        - use alternate ffmpeg cropping format (in_w:in_h, etc.) for certain scenarios
        - delete crop stuff after turning crop mode off
        - get rid of self.selection in favor of using crop_frames[0] and crop_frames[2] (left/right)?
        - arrow keys/spinboxes for precise movement/cropping over the factored points (a new use for defactor_point())
        - https://stackoverflow.com/questions/24831484/how-to-align-qpainter-drawtext-around-a-point-not-a-rectangle
        - use QDockWidgets instead of frames
TODO: find interesting use for QtWidgets.QGraphicsScene()? (used in old widgets/main.py files for early crop tests)
TODO: 47.58fps video NOT behaving well (progress bar is too fast -> 1.25 seconds ahead per minute)
TODO: improved or improvised status bar? -> half-width and/or custom widgets for things like playback speed, etc.
TODO: centralwidget's layout column stretch should be a customizable option
TODO: streamlined way to trim and concat multiple sections of a single video (or just a timeline)
TODO: what are media_lists? https://stackoverflow.com/questions/28440708/python-vlc-binding-playing-a-playlist
TODO: add alternate log signal for logging.error messages, like "FAILED:"
        - log_slot is bad anyways since it disguises the actual origin of a log message
TODO: decrease max heights of progress slider/side timestamps or is 20 pixels a good middleground?
TODO: vlc-style playlists + playlist menu?
TODO: vlc dvd/network/capture device MRLs? easy to integrate? (dvd:///C:/Windows/system32/, screen://)
TODO: vlc VLsub (very cool subtitle search-utility) -> opensubtitles.org
TODO: vlc Media Information window with editable metadata + codec information?  <- get/set/save_meta
TODO: vlc.py stuff to check out
        - get_delay/set_delay (audio delays)
        - audio_get_channel/audio_set_channel
        - !!! get_stats (decoded frame count? video -> displayed frames -> ???)
        - VideoAdjustOption enum (hue/brightness/whatnot)
        - AudioEqualizer class
        - all_slave, but for un-saved audio tracks
        - video_get_track_description <- Get the description of available video tracks.
        - audio_get_track_description <- Get the description of available audio tracks.
        - get_full_title_descriptions <- Get the full description of available titles.
        - BROKEN? -> get_full_chapter_descriptions(i_chapters_of_title) <- Get full description of available chapters. @param index of title to query for chapters (uses current title if set to -1)
TODO: make use of .nfo files to expand auto-opening abilities for subtitles -> look at language + subtitle filename/format and find it
        - VLC already auto-opens subtitle files if they contain the media file's name anywhere in their own name
        - maybe check if media file has metadata and compare it against all non-matching .nfo files
TODO: tab-order no longer exists due to setting everything to ClickFocus (worthwhile sacrifice?)
        - previousInFocusChain and NextInFocusChain might be usable for best of both worlds
TODO: upload-to-imgur button? NOTE: requires client-id and requests Session. perhaps a secret advanced option
        - "plugin" support could be just loading python files before showing GUI -> add imgurbot + IRS support
TODO: use "rotate" metadata to have a live preview of rotations (might cause too many issues)? (or use QMediaPlayer and rotate manually)
        - VLC has a way to rotate videos natively (this may be involving either callbacks (hard) or filters (easy?))
TODO: custom rotate angle option (possibly difficult, ffmpeg has bizarre syntax for it)
TODO: more secure way of locking videos during editing? like with an actual file lock (QtCore.QLockFile)
optimization: identify the length of time required for each part of the startup process
optimization: quick-snapshot, snapshot... too many QActions and lambdas?
optimization: use direct libvlc functions
optimization: remove translate flags from .ui file? maybe not a good idea
TODO: use qtawesome icons/fonts? https://pypi.org/project/QtAwesome/ <- qta-browser
TODO: enhanced playback speed option (context menu/menubar)?
TODO: playlists + shuffle (including a smart shuffle that plays playlist to completion without repeats)
TODO: playing online media like VLC
TODO: implement VLC's taskbar button preview where it lets you play/pause from it https://docs.microsoft.com/en-us/dotnet/api/system.windows.shell.thumbbuttoninfo?view=windowsdesktop-6.0
TODO: video_set_aspect_ratio and video_set_scale (this is for "zooming")
TODO: improve recent videos list to be more like IR-suite's?
TODO: add setting to make total duration label show the remaining time instead
TODO: add settings for trim graphics?
TODO: more fullscreen settings? (alternate animation -> raise/lower instead of fade, separate idle timer, etc.)
TODO: finish marquee settings: drop shadow (VLC can control this, but I have no idea how), Color
        - fade durations aren't working very well, I was forced to put arbitrary limits on the settings
TODO: vlc settings to add
        - video/audio dependent raise/focus settings
        - settings for allowing multiple instances
        - "enable time-stretching audio" -> fixes audio pitch changing with playback speed
        - --start-paused, --no-start-paused
TODO: gstreamer | ffpyplayer https://matham.github.io/ffpyplayer/player.html
TODO: alternate progress method where we measure how many seconds are left -> how many frames are left -> we know where to set progress bar...?
      Example: 2 minute video at 10fps = 1200 frames. 30 seconds left = 300 frames left = set progress bar 300 frames from end
TODO: https://wiki.videolan.org/Documentation:Modules/alphamask/
TODO: WA_PaintUnclipped https://doc.qt.io/qt-5/qt.html#WidgetAttribute-enum
TODO: app.primaryScreenChanged.connect()
TODO: is there a way to add/modify libvlc options like "--gain" post-launch? media.add_option() is very limited
TODO: make logo in about window link somewhere
TODO: "add subtitle file" but for video/audio tracks? (audio tracks supported, but VLC chooses not to use this)
TODO: ram usage
        - !!! if it fails, update checking adds 15mb of ram that never goes away (~42mb before -> 57mb after)
        - if it doesn't fail, update checking still adds around 6mb on average
        - QWIDGETMAX is locked behind a pointless 4mb ram library
        - transition to lazy loading instead of loading everything all at once (about/cat dialogs finished)
        - themes take up nearly 2mb of ram (is loading the logo the biggest issue? only 14kb size)
        - removing 90% of qthelpers reduced ram by ~0.5mb (not worth it or even realistic)
TODO: editing feature changes:
        - "replace/add audio" -> add prompt to change volume of incoming file (make these into menus with 2 actions? one that shows a prompt and one that doesn't)
        - "add audio" -> option to literally add it as an audio track (with ffmpeg, not libvlc/add_slave)
        - adding audio to gifs
        - converting mp4 to gif
        - improve filter/name hints, especially for things like remove_track
        - add "compress" option
        - add "speed" option (this is already implemented for audio files through the resize function)
        - implement more image edits?
TODO: formats that still don't trim correctly after save() rewrite: 3gp, ogv, mpg (used to trim inaccurately, now doesn't trim at all)
        - trimming likely needs to not use libx264 and aac for every format


TODO: HIGH PRIORITY:
lazy concatenate dialog seems to have a memory leak (it does not free up QVideoList's memory after deletion)

TODO: MEDIUM PRIORITY:
DPI/scaling support
ffmpeg audio replacement/addition sometimes cuts out the audio 1 second short. keyframe related? corrupted streams (not vlc-specific)?
further polish cropping
increase stability/add re-encoding ability to concatenation (currently fails/corrupts if you combine different formats/corrupted streams)
confirm/increase stability for videos > 60fps (not yet tested)
implement "compress" and "speed" edits for videos
trimming-support for more obscure formats
implement filetype associations
high-precision progress bar has been neglected and is now consistently a little too fast
far greater UI customization

TODO: LOW PRIORITY:
replace VLC with QMediaPlayer (maybe)
support chaining more edits together at once
massively improve robust-ness of editing features -> filters/hints/prompts/errors/formats need to be MUCH more consistent
implement the "concatenate" edit for audio-only files
further reduce RAM usage
"Restore Defaults" button in settings window
see update change logs before installing
add way to distinguish base and forked repos
ability to skip updates
figure out the smallest feasible ffmpeg executable we can without sacrificing major edit features (ffmpeg.dll?)
create "lite" version on github that doesn't include ffmpeg or vlc files?
ability to continue playing media while minimized to system tray
enhance fading by adding ability to hold fade
forwards/backwards buttons currently only work when pressed over the player
ability to limit combination-edits (adding/replacing audio) to the shortest input (this exists in ffmpeg but breaks often)
do the math to chain audio-resizes together to get around ffmpeg atempo 0.5-2.0 limitation (can be chained in single command)


KNOWN ISSUES:
    Non-serious:
        dragging video onto taskbar button does nothing
        cursor idle timeout applies to music and images (good thing?)
    Likely unfixable:
        holding X on window/dialogs pauses progress bar but does not restore progress afterwards (likely requires custom titlebar)
    Low priority:
        using scrollwheel on the minute-spinBox increases/decreases by slightly more than a minute when not paused (around 63 seconds)
        manually entering single %'s in config file for path names somehow ignores all nested folders
        progress bar slows down when window isn't focused
        frame-seeking near the very end of a video rarely works (set_time() vs set_position() makes no difference)          <- use player.next_frame()?
        partially corrupt videos have unusual behavior when frame-seeking corrupted parts <- use player.next_frame()?
        frame-seeking only a handful of frames after a video finishes and trying to play again sometimes causes brief freeze
        player becomes slightly less responsive after repeatedly minimizing to system tray (noticable fraction-of-a-second delay when navigating)
        resizing videos doesn't actually stretch them? or... it does? very strange behavior with phantom black bars that differ from player to player
        rarely, concatenated videos will have a completely blank frame between clips, causing the theme background to appear for 1 frame
        abnormally long delay opening first video after opening extremely large video (longer delay than in VLC) -> delay occurs at player.set_media
    Medium priority:
        output-name lineEdit's placeholder text becomes invisible after setting a theme and then changing focus
        resizing an audio file rarely stalls forever with no error (works upon retry)
        rotating/flipping video rarely fails for no reason (works upon retry)
        videos with replace/added audio tracks longer than the video themselves do NOT concatenate correctly (audio track freaks ffmpeg out)
        concatenting sometimes freezes an explorer window if drag/dropping from it into the concatenation dialog
        repeatedly going into fullscreen on a higher DPI/scaled monitor results ruins the controls (general DPI/scaling support is high priority)
    Moderately high priority:
        spamming the cycle buttons will eventually crash to desktop with no error
        volume gain suddenly changes after extended use
        .3gp, .ogv, and .mpg files do not trim correctly
    Cannot reproduce consistently:
        player's current visible frame doesn't change when navigating (<- and ->) after video finishes until it's unpaused (used to never happen)
        scrubbing slider and sharply moving mouse out of window while releasing causes video to not unpause until scrubbed again (rare)
        clicking on the progress bar will update the video without moving the progress bar (very rare, may be bottlenecking issue)
        fullscreen mode becomes partially unresponsive -> no idle timer, no passthrough on dockControls (very rare, may be bottlenecking issue)
        system tray icon suddenly crashes -> "OSError: exception: access violation writing 0x0000000000000007" (extremely rare, unknown cause)
'''

import config
import widgets
import qtstart
import constants
import qthelpers
from util import ffmpeg, ffmpeg_async, add_path_suffix, get_unique_path, get_hms, get_aspect_ratio, get_PIL_Image, sanitize, scale, file_is_hidden
from bin.window_pyplayer import Ui_MainWindow
from bin.window_settings import Ui_settingsDialog

import os
import gc
import sys
import math
import json
import random
import logging
import subprocess
from time import sleep, localtime, mktime, strftime, strptime
from time import time as get_time                       # from time import time -> time() errors out
from threading import Thread
from traceback import format_exc
from contextlib import contextmanager

import filetype                                         # 0.4mb ram
from vlc import State, VideoMarqueeOption
from tinytag import TinyTag

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets as QtW
from PyQt5.QtCore import Qt
#from PyQt5.Qt import QWIDGETSIZE_MAX                   # PyQt5.Qt adds FOUR MB of ram usage, used in set_fullscreen
WindowStateChange = QtCore.QEvent.WindowStateChange     # important alias, but can't be defined in __name__=='__main__'


# keyboard event:     ['device', 'event_type', 'is_keypad', 'modifiers', 'name', 'scan_code', 'time', 'to_json' -> {"event_type": "up", "scan_code": 77, "name": "right", "time": 1636583589.5201082, "is_keypad": false}]
# Qt keyReleaseEvent: ['accept', 'count', 'ignore', 'isAccepted', 'isAutoRepeat', 'key', 'matches', 'modifiers', 'nativeModifiers', 'nativeScanCode', 'nativeVirtualKey', 'registerEventType', 'setAccepted', 'setTimestamp', 'spontaneous', 'text', 'timestamp', 'type']
# Qt wheelEvent:      ['accept', 'angleDelta', 'buttons', 'globalPos', 'globalPosF', 'globalPosition', 'globalX', 'globalY', 'ignore', 'inverted', 'isAccepted', 'modifiers', 'phase', 'pixelDelta', 'pos', 'posF', 'position', 'registerEventType', 'setAccepted', 'setTimestamp', 'source', 'spontaneous', 'timestamp', 'type', 'x', 'y']
# Qt mousePressEvent: ['accept', 'button' (CORRECT), 'buttons' (WRONG), 'flags', 'globalPos', 'globalX', 'globalY', 'ignore', 'isAccepted', 'localPos', 'modifiers', 'pos', 'registerEventType', 'screenPos', 'setAccepted', 'setTimestamp', 'source', 'spontaneous', 'timestamp', 'type', 'windowPos', 'x', 'y'] windowPos, x, y -> -> actual pos inside WIDGET
# Qt mouseMoveEvent:  ['accept', 'button', 'buttons', 'flags', 'globalPos', 'globalX', 'globalY', 'ignore', 'isAccepted', 'localPos', 'modifiers', 'pos', 'registerEventType', 'screenPos', 'setAccepted', 'setTimestamp', 'source', 'spontaneous', 'timestamp', 'type', 'windowPos', 'x', 'y']
# Qt dropEvent:       ['accept', 'acceptProposedAction', 'dropAction', 'ignore', 'isAccepted', 'keyboardModifiers', 'mimeData', 'mouseButtons', 'pos', 'posF', 'possibleActions', 'proposedAction', 'registerEventType', 'setAccepted', 'setDropAction', 'source', 'spontaneous', 'type']
# QSize:              ['boundedTo', 'expandedTo', 'grownBy', 'height', 'isEmpty', 'isNull', 'isValid', 'scale', 'scaled', 'setHeight', 'setWidth', 'shrunkBy', 'transpose', 'transposed', 'width']]
# QCursor:            ['bitmap', 'hotSpot', 'mask', 'pixmap', 'pos', 'setPos', 'setShape', 'shape', 'swap']
# QScreen:            [https://doc.qt.io/qt-5/qscreen.html -> size, availableSize, refreshRate, name, physicalSize, orientation (0 default, 2 landscape), primaryOrientation, nativeOrientation]
# -->                 app.screens(), app.primaryScreen(), app.primaryScreenChanged.connect()
# Qt.KeyboardModifiers | QApplication.keyboardModifiers() | QApplication.queryKeyboardModifiers()
# QColor F suffix is Float -> values are represented from 0-1. (getRgb() becomes getRgbF())
# QWidget.saveGeometry() | QWidget.restoreGeometry()
# self.childAt(x, y) | self.underMouse() -> bool
# NOTE: QtWidgets.QToolTip.hideText/showText/setPalette/setFont (showText is laggy)
# NOTE: app.setQuitOnLastWindowClosed(False) -> app.quit() (app.aboutToQuit.connect)
# NOTE: QWinTaskbarButton/QWinTaskbarProgress (obsolete) -> https://doc.qt.io/qt-5/qwintaskbarbutton.html
# NOTE: Plugins (QPluginLoader/QLibrary): Felgo (really good), QSkinny (lightweight), Advanced Docking System (laggy but pure Qt)
#                                         Qt Pdf Viewer Library, CircularSlider (QML), GitQlient, All KDE Community plugins
# NOTE: Useful: QReadWriteLock/QLockFile, QStorageInfo, QStandardPaths, QFileSystemWatcher, QMimeData (for dragging)
# NOTE: Potentially useful: QMutex, QLocale, QStateMachine(?), QShow/HideEvent, QFileSystemWatcher, QPdfDocument (paid?)
# NOTE: Interesting: QFileselector, QCamera, QEventLoop[Locker], QWinEventNotifier, QColorTransform(??), QSharedMemory (inter-process)
# NOTE: Interesting but useless in Python: QSaveFile, QRandomGenerator, QTemporaryDir/File, QJsonObject


# -----------------------------
# Additional utility functions
# -----------------------------
def get_audio_duration(file: str) -> float:
    ''' Lightweight way of getting the duration of an audio `file`.
        Used for instances where we need ONLY the duration. '''
    try:
        try:                                                    # https://pypi.org/project/tinytag/0.18.0/
            return TinyTag.get(file, tags=False).duration
        except:                                                 # TinyTag is lightweight but cannot handle everything
            import music_tag                                    # only import music_tag if we absolutely need to
            return music_tag.load_file(file)['#length'].value
    except:                                                     # this is to handle things that wrongly report as audio, like .ogv files
        log_on_statusbar('(?) File could not be read as an audio file (not recognized by TinyTag or music_tag)')
        return 0.0


@contextmanager
def get_image_data(path: str, extension: str = None):
    # TODO I don't need this anymore and should probably avoid using it at all.
    try:
        if exists(path): image_data = get_PIL_Image().open(path, formats=(extension,) if extension else None)
        else: image_data = get_PIL_Image().fromqpixmap(image_player.art)
        yield image_data
    finally:
        try: image_data.close()
        except: logging.warning('(?) Image pointer could not be closed (it likely was never open in the first place).')


@contextmanager
def get_PIL_safe_path(original_path: str, final_path: str):
    # TODO Like the above, this is a holdover from when I was reworking
    #      operation ordering/chaining for 0.6.0 and is not actually needed
    #      anymore, save for one spot where I was too lazy to implement Pillow.
    try:
        temp_path = ''
        if splitext_media(final_path, constants.IMAGE_EXTENSIONS)[-1] == '':
            good_ext = splitext_media(original_path, constants.IMAGE_EXTENSIONS)[-1]
            if good_ext == '': good_ext = '.png'
            temp_path = final_path + good_ext
            yield temp_path
        else:
            yield final_path
    finally:
        if temp_path != '':
            print('\n\nDO THEY EXIST? (literally impossible for them not to):', exists(temp_path), exists(final_path))
            try: os.replace(temp_path, final_path)
            except: logging.warning('(!) FAILED TO RENAME TEMPORARY IMAGE PATH' + format_exc())


def splitext_media(path: str, valid_extensions: tuple = constants.ALL_MEDIA_EXTENSIONS, strict: bool = True) -> tuple:
    base, ext = os.path.splitext(path)
    ext = ext.lower()
    if not ext: return path, ''
    if ext not in valid_extensions:
        if strict or len(ext) > 6: return base, ''
        has_letters = False
        for c in ext[1:]:
            if c.isalpha(): has_letters = True
            elif not c.isdigit(): return base, ''
        if not has_letters: return base, ''
    return base, ext


#def correct_misaligned_formats(audio, video) -> str:                # this barely works
#    _, vext = os.path.splitext(video)
#    abase, aext = os.path.splitext(audio)
#    if vext != aext and not (vext == '.mp4' and aext == '.mp3'):    # audio is not the same format as video
#        new_audio = f'{abase}{vext}'                                # create new audio filename
#        logging.info(f'Formats misaligned between audio "{audio}" and video "{video}". Correcting audio to "{new_audio}"')
#        ffmpeg(None, f'-i "{audio}" "{new_audio}"')                 # convert audio to video's format
#        audio = new_audio                                           # replace bad audio filename
#    else: logging.info(f'Formats aligned between audio "{audio}" and video "{video}".')
#    return audio


#def indeterminate_progress(func):      # originally used for _save()
#    ''' Cute and pointless decorator for toggling the progress bar inside our status bar without doing it the conventional ways
#        (adding save_progress_bar.hide() to every return line or wrapping all of _save() in a try-except-finally statement). '''
#    def wrapper(gui, *args, **kwargs):
#        gui.save_progress_bar.show()
#        return_value = func(gui, *args, **kwargs)
#        gui.save_progress_bar.hide()
#        return return_value
#    return wrapper


# ---------------------
# Main GUI
# ---------------------
class GUI_Instance(QtW.QMainWindow, Ui_MainWindow):
    _open_signal = QtCore.pyqtSignal()                  # NOTE: Custom signals MUST be class variables
    _save_open_signal = QtCore.pyqtSignal(str, bool)    # str -> file, bool -> remembering previous file
    fast_start_open_signal = QtCore.pyqtSignal(str)
    restart_signal = QtCore.pyqtSignal()
    force_pause_signal = QtCore.pyqtSignal(bool)
    show_ffmpeg_warning_signal = QtCore.pyqtSignal(QtW.QWidget)
    show_trim_dialog_signal = QtCore.pyqtSignal()
    update_progress_signal = QtCore.pyqtSignal(float)
    refresh_title_signal = QtCore.pyqtSignal()
    log_on_statusbar_signal = QtCore.pyqtSignal(str)
    set_save_progress_visible_signal = QtCore.pyqtSignal(bool)
    set_save_progress_max_signal = QtCore.pyqtSignal(int)
    set_save_progress_current_signal = QtCore.pyqtSignal(int)
    set_save_progress_format_signal = QtCore.pyqtSignal(str)
    disable_crop_mode_signal = QtCore.pyqtSignal(bool)
    handle_updates_signal = QtCore.pyqtSignal(bool)
    _handle_updates_signal = QtCore.pyqtSignal(dict, dict)

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.setupUi(self)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # this allows easier clicking off of lineEdits
        self.save_progress_bar = QtW.QProgressBar(self.statusbar)
        self.dialog_settings = qthelpers.getDialogFromUiClass(Ui_settingsDialog)
        self.dialog_settings.setWindowFlags(Qt.WindowStaysOnTopHint)
        if constants.PLATFORM != 'Windows':              # settings dialog was designed around Windows UI
            self.dialog_settings.resize(self.dialog_settings.tabWidget.sizeHint().width(),
                                        self.dialog_settings.height())
        self.icons = {
            'window':            QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}logo.ico'),
            'loop':              QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}loop.png'),
            'autoplay':          QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}autoplay.png'),
            'autoplay_backward': QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}autoplay_backward.png'),
            'autoplay_shuffle':  QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}autoplay_shuffle.png'),
            'reverse_vertical':  QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}reverse_vertical.png'),
            'cycle_forward':     QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}cycle_forward.png'),
            'cycle_backward':    QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}cycle_backward.png'),
        }
        self.setWindowIcon(self.icons['window'])
        app.setWindowIcon(self.icons['window'])


    def setup(self):
        self.first_video_fully_loaded = False
        self.closed = False
        self.restarted = False
        self.is_paused = False
        self.close_cancel_selected = False
        self.checking_for_updates = False
        self.frame_override: int = -1
        self.open_queued = False
        self.swap_slider_styles_queued = False
        self.lock_progress_updates = False
        self.lock_spin_updates = False
        self.timer_id_resize_snap: int = None
        self.close_was_spontaneous = False
        self.was_maximized = False
        self.was_paused = False
        self.lock_fullscreen_ui = False
        self.crop_restore_state = {}
        self.ignore_next_alt = False
        self.skip_next_vlc_progress_desync_check = False

        self.last_window_size: QtCore.QSize = None
        self.last_window_pos: QtCore.QPoint = None
        self.last_move_time = 0.0
        self.last_cycle_was_forward = True
        self.last_cycle_index: int = None

        self.video = ''
        self.video_basename = ''
        self.video_original_path = ''
        self.locked_video: str = None
        self.recent_files = []
        self.mime_type = 'image'    # defaults to 'image' since self.pause() is disabled for 'image' mime_types
        self.extension = '?'
        self.is_gif = False
        self.is_static_image = True
        self.clipboard_image_buffer = None
        #self.PIL_image = None       # TODO: store images in memory for quick copying?

        self.fractional_frame = 0.0
        self.delay = self.duration = 0
        self.frame_count = self.frame_rate = self.frame_rate_rounded = self.current_time = self.minimum = self.maximum = 1
        self.vwidth = self.vheight = 1000
        self.vsize = QtCore.QSize(1000, 1000)
        #self.resolution_label = '0x0'
        self.ratio = '0:0'
        self.size_label = '0.00mb'  # NOTE: do NOT use `self.size` - this is reserved for Qt

        self.last_amplify_audio_value = 100
        self.current_file_is_autoplay = False
        self.shuffle_folder = ''
        self.shuffle_ignore_order = []
        self.shuffle_ignore_unique = set()
        self.marked_for_deletion = set()
        self.shortcuts: dict = None
        #self.shortcut_bandaid_fix = False
        self.operations = {}
        self.volume_boost = 1
        self.playback_speed = 1.0

        # misc setup
        self.increment_volume = lambda inc: set_volume_slider(get_volume_slider() + inc)
        self.is_trim_mode = lambda: self.trim_mode_action_group.checkedAction() in (self.actionTrimAuto, self.actionTrimPrecise)
        self.statusbar.addPermanentWidget(self.save_progress_bar)            # TODO could QWIDGETMAXSIZE be used to span the widget across the entire statusbar?
        self.menuRecent.setToolTipsVisible(True)
        self.menuAudio.insertMenu(self.actionAmplifyVolume, self.menuTrimMode)
        self.menuAudio.addAction(self.actionResize)
        self.player = self.vlc.player                                        # NOTE: this is a secondary alias for other files to use
        self.sliderProgress.update_parent_progress = self.set_and_update_progress
        self.sliderVolume.keyPressEvent = self.keyPressEvent                 # pass sliderVolume key presses directly to GUI_Instance
        self.sliderVolume.keyReleaseEvent = self.keyReleaseEvent
        self.sliderProgress.dragEnterEvent = self.vlc.dragEnterEvent         # reuse player's drag-and-drop code for slider
        self.sliderProgress.dropEvent = self.vlc.dropEvent
        self.frameAdvancedControls.setDragTarget(self)
        self.dockControls.setTitleBarWidget(QtW.QWidget(self.dockControls))  # disables QDockWidget's unique titlebar
        self.dockControls.leaveEvent = self.leaveEvent                       # ensures leaving dockControls hides cursor/controls in fullscreen
        self.dockControls.resizeEvent = self.dockControlsResizeEvent         # ensures dockControls correctly hides/shows widgets in fullscreen
        self.dockControls.keyPressEvent = self.keyPressEvent                 # pass dockControls key presses directly to GUI_Instance
        self.dockControls.keyReleaseEvent = self.keyReleaseEvent
        self.lineOutput.setIgnoreAll(False)

        for spin in (self.spinHour, self.spinMinute, self.spinSecond, self.spinFrame):
            spin.setProxyWidget(self)

        self.save_progress_bar.setMaximum(0)
        self.save_progress_bar.setMaximumHeight(16)
        self.save_progress_bar.setFormat('Saving (%p%)')                     # TODO add "(%v/%m frames)"?
        self.save_progress_bar.setAlignment(Qt.AlignCenter)
        self.save_progress_bar.setSizePolicy(QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Expanding)
        self.save_progress_bar.hide()

        self.frameCropInfo.setVisible(False)                                # ensure crop info panel is hidden on startup

        self.frameProgress.contextMenuEvent = self.frameProgressContextMenuEvent
        self.buttonPause.contextMenuEvent = self.pauseButtonContextMenuEvent
        self.buttonTrimStart.contextMenuEvent = self.trimButtonContextMenuEvent
        self.buttonTrimEnd.contextMenuEvent = self.trimButtonContextMenuEvent
        self.buttonExploreMediaPath.contextMenuEvent = self.openMediaLocationButtonContextMenuEvent
        self.buttonMarkDeleted.contextMenuEvent = self.buttonMarkDeletedContextMenuEvent
        self.buttonSnapshot.contextMenuEvent = self.buttonSnapshotContextMenuEvent
        self.buttonAutoplay.contextMenuEvent = self.buttonAutoplayContextMenuEvent
        self.menuRecent.contextMenuEvent = self.menuRecentContextMenuEvent

        self.buttonLoop.setIcon(self.icons['loop'])
        self.buttonNext.setIcon(self.icons['cycle_forward'])
        self.buttonPrevious.setIcon(self.icons['cycle_backward'])

        # all possible snapshot button actions and tooltips
        self.snapshot_actions = (
            (self.snapshot,                                                          'Takes and saves a snapshot immediately using your presets.'),
            (lambda: self.snapshot(mode='full'),                                     'Opens size/quality, and save dialogs for your snapshot.'),
            (lambda: self.copy_image(extended=False),                                'Copy the current frame data directly to your clipboard.'),
            (lambda: self.copy_image(extended=True),                                 'Copy the current frame data using a custom size and quality.'),
            (lambda: self.snapshot(mode='undo'),                                     'Delete the most recently saved snapshot.'),
            (lambda: self.snapshot(mode='open'),                                     'Opens the last snapshot in PyPlayer.'),
            (lambda: self.snapshot(mode='view'),                                     'Opens the last snapshot in your default program.'),
            (lambda: self.explore(config.cfg.last_snapshot_path, 'Last snapshot'),   'Open the last snapshot in explorer.'),
            (lambda: self.copy(config.cfg.last_snapshot_path, 'Last snapshot'),      'Copy the last snapshot\'s path to your clipboard.'),
            (lambda: self.copy_file(config.cfg.last_snapshot_path),                  'Copy the last snapshot\'s file to your clipboard.'),
            (lambda: self.copy_file(config.cfg.last_snapshot_path, cut=True),        'Cut the last snapshot\'s file to your clipboard.'),
            (lambda: self.copy_image(config.cfg.last_snapshot_path, extended=False), 'Copy the last snapshot\'s image data to your clipboard.'),
        )

        Thread(target=self.update_slider_thread, daemon=True).start()


    def fast_start_open(self, cmdpath):
        ''' Slot for handling cmd-files from the fast-start interface in a thread-safe manner. '''
        try:
            with open(cmdpath, 'rb') as txt:            # paths are encoded, to support special characters
                command = txt.readline().decode().strip()
                if command == 'EXIT':
                    logging.info('(FS) External request to close recieved (likely an update pending). Exiting.')
                    try: os.remove(cmdpath)             # pre-emptively remove cmdpath before closing, if possible
                    except: pass
                    qtstart.exit(self)
                else:
                    self.open(command, focus_window=settings.checkFocusDoubleClick.isChecked())
                    logging.info(f'(FS) Fast-start for {command} recieved and handled.')
        finally: self.fast_start_in_progress = False    # resume fast-start interface


    def fast_start_interface_thread(self):
        ''' Simple interface for detecting and reading cmd.txt files. Used for instantly playing new media upon double-click
            if we're already open (cmd.txt contains the path to the media) or closing in preparation for an update (cmd.txt
            contains the word "EXIT"). NOTE: Also used to auto-correct high-precision progress sliders, once every 5 seconds. '''
        cmdpath = f'{constants.TEMP_DIR}{sep}cmd.{os.getpid()}.txt'           # the cmd.txt file with our PID to look for
        checks_per_second = 10                                                # how many times per second we'll check for our cmd file
        check_delay = round(1 / checks_per_second, 2)
        total_checks = 5 * checks_per_second
        try: os.makedirs(os.path.dirname(cmdpath))
        except: pass
        try: os.remove(cmdpath)
        except: pass
        logging.info(f'Fast-start connection established. Will listen for commands at {cmdpath}.')

        while not self.closed:
            for _ in range(total_checks):                                     # run fast-start interface for 5 seconds at a time
                if self.closed: break
                try:
                    if exists(cmdpath):
                        self.fast_start_in_progress = True
                        self.fast_start_open_signal.emit(cmdpath)
                        logging.info(f'(FS) CMD-file detected: {cmdpath}')
                        while self.fast_start_in_progress and not self.closed: sleep(0.05)
                        os.remove(cmdpath)                                    # delete cmd.txt if possible
                except: log_on_statusbar(f'(!) FAST-START INTERFACE FAILED: {format_exc()}')
                finally: sleep(check_delay)

            # once every 5 seconds, check to make sure high-precision progress slider is maintaining accuracy
            if player.is_playing() and not self.lock_progress_updates and settings.checkHighPrecisionProgress.isChecked():
                if self.skip_next_vlc_progress_desync_check:                  # NOTE: this is used for the audio-pitch-fix-hack while navigating
                    self.skip_next_vlc_progress_desync_check = False
                    continue
                vlc_frame = player.get_position() * self.frame_count          # get the frame VLC thinks it is
                next_frame = get_progess_slider() + 1 * self.playback_speed
                if abs(next_frame - vlc_frame) > self.frame_rate * 2:         # if our frame is way, WAY off (2+ seconds)...
                    true_frame = vlc_frame + (self.frame_rate * 0.3)          # ...reset to VLC's frame, +0.3 secs (VLC is usually 0.3-0.6 behind)
                    self.frame_override = true_frame
                    log_on_statusbar('Warning: high-precision slider was desynced by >2 seconds. Corrected.')


    # ---------------------
    # >>> EVENTS <<<
    # ---------------------
    def event(self, event: QtCore.QEvent) -> bool:
        ''' A global event callback. Used to detect windowStateChange events,
            so we can save/remember the maximized state when necessary. '''
        if event.type() == WindowStateChange:        # alias used for speed
            if not (self.windowState() & Qt.WindowMinimized or self.windowState() & Qt.WindowFullScreen):
                self.was_maximized = bool(self.windowState() & Qt.WindowMaximized)
        return super().event(event)


    def closeEvent(self, event: QtGui.QCloseEvent):  # 'spontaneous' -> X-button pressed, likely not exiting for real
        self.close_cancel_selected = False           # referenced in qtstart.exit()
        self.close_was_spontaneous = event.spontaneous()
        logging.info(f'Closing (spontaneous={event.spontaneous()}).')

        # if user doesn't want to minimize to tray, just exit immediately
        minimize_to_tray = settings.groupTray.isChecked() and settings.checkTrayClose.isChecked()
        force_close = (event.spontaneous() and not minimize_to_tray) or self.tray_icon is None

        if self.marked_for_deletion:
            logging.info(f'The following files are still marked for deletion, opening prompt: {self.marked_for_deletion}')
            choice = self.show_delete_prompt(exiting=force_close or not event.spontaneous())
            if choice == QtW.QMessageBox.Cancel:     # cancel selected, don't close
                self.close_cancel_selected = True    # required in case .close() was called from qtstart.exit()
                logging.info('Close canceled.')
                return event.ignore()

        #set_and_update_progress(0)
        self.stop()                                  # stop player
        settings.close()                             # close settings dialog
        self.dockControls.setFloating(False)         # hide fullscreen UI if needed
        logging.info('Player has been stopped.')

        if force_close:
            qtstart.exit(self)
        else:
            if not cfg.minimizedtotraywarningignored:
                if event.spontaneous():              # only show message if closeEvent was called by OS (i.e. X button pressed)
                    self.tray_icon.showMessage('PyPlayer', 'Minimized to system tray')  # this emits messageClicked signal
                cfg.minimizedtotraywarningignored = True
            if settings.checkFirstFileTrayReset.isChecked():
                self.first_video_fully_loaded = False
            gc.collect(generation=2)
        return event.accept()


    def hideEvent(self, event: QtGui.QHideEvent):    # 'spontaneous' -> native minimize button pressed
        if event.spontaneous():
            if settings.checkMinimizePause.isChecked():
                self.was_paused = self.is_paused
                self.force_pause(True)
            elif settings.groupTray.isChecked() and settings.checkTrayMinimize.isChecked():
                self.close()                         # TODO these do not work with each other yet
        return super().hideEvent(event)


    def showEvent(self, event: QtGui.QShowEvent):    # 'spontaneous' -> restored by OS (e.g. clicked on taskbar icon)
        super().showEvent(event)

        # refresh VLC instance's winId
        if constants.PLATFORM == 'Windows': player.set_hwnd(self.vlc.winId())              # Windows
        elif constants.PLATFORM == 'Darwin': player.set_nsobject(int(self.vlc.winId()))    # MacOS
        else: player.set_xwindow(self.vlc.winId())                                         # Linux (sometimes)

        # strangely, closing/reopening the window applies an alignment to our QVideoPlayer/QWidget (very bad)
        self.gridLayout.setAlignment(self.vlc, Qt.Alignment())          # reset alignment to nothing

        if event.spontaneous():
            if not self.was_paused and settings.checkMinimizePause.isChecked() and settings.checkMinimizeRestore.isChecked():
                self.force_pause(False)
        if self.isFullScreen(): self.set_fullscreen(True)               # restore fullscreen UI
        gc.collect(generation=2)


    def enterEvent(self, event: QtGui.QEnterEvent):
        self.lock_fullscreen_ui = False or (not player.is_playing() and not self.is_paused)
        return super().enterEvent(event)


    def leaveEvent(self, event: QtCore.QEvent):
        pos = self.mapFromGlobal(QtGui.QCursor().pos())
        self.lock_fullscreen_ui = self.rect().contains(pos) or (not player.is_playing() and not self.is_paused)
        if not self.lock_fullscreen_ui: self.vlc.last_move_time = 1
        return super().leaveEvent(event)


    def moveEvent(self, event: QtGui.QMoveEvent):
        if not self.isMaximized() and not self.isFullScreen():          # don't save position if we're currently maximized/fullscreen
            self.last_window_pos = event.oldPos()
            if self.timer_id_resize_snap is None or app.mouseButtons() != Qt.LeftButton:
                self.last_move_time = get_time()                        # don't save move time if we're actually resizing


    def resizeEvent(self, event: QtGui.QResizeEvent):
        if not self.isMaximized() and not self.isFullScreen():          # don't save size if we're currently maximized/fullscreen
            self.last_window_size = event.oldSize()


    def dockControlsResizeEvent(self, event: QtGui.QResizeEvent):
        ''' Makes UI controls more compact as the size of the controls shrinks. '''
        width = event.size().width()
        self.frameQuickChecks.setVisible((not self.actionCrop.isChecked() and width >= 568) or width >= 800)
        self.frameCropInfo.setVisible(self.actionCrop.isChecked() and width >= 621)
        self.lineOutput.setMinimumWidth(10 if width <= 380 else 120)    # reduce output lineEdit (but retain usability)
        self.advancedControlsLine.setVisible(width >= 357)              # hide aesthetic line-separator
        self.hlayoutQuickButtons.setSpacing(2 if width <= 394 else 6)   # reduce spacing between buttons
        self.buttonTrimStart.setMinimumWidth(32 if width <= 347 else 44)

        # hide or restore trim/toolbar buttons
        primary_visible = width > 335
        seconary_visible = width > 394
        self.buttonTrimStart.setVisible(primary_visible)
        self.buttonTrimEnd.setVisible(primary_visible)
        self.buttonMarkDeleted.setVisible(seconary_visible)
        self.buttonSnapshot.setVisible(seconary_visible)
        self.buttonExploreMediaPath.setVisible(seconary_visible)
        self.spinHour.setVisible(primary_visible)

        if primary_visible:
            self.spinFrame.setPrefix(f'{self.frame_rate_rounded} FPS: ')
            self.spinFrame.setMinimumSize(98, 0)
        else:
            self.spinFrame.setPrefix('')
            self.spinFrame.setMinimumSize(0, 0)


    def timerEvent(self, event: QtCore.QTimerEvent):
        ''' The base timeout event, used for adjusting the window's aspect
            ratio after a resize. Started by QVideoPlayer.resizeEvent(). '''
        if self.timer_id_resize_snap is not None and app.mouseButtons() != Qt.LeftButton:
            self.timer_id_resize_snap = self.killTimer(self.timer_id_resize_snap)
            if get_time() - self.last_move_time < 1: return super().timerEvent(event)

            # get keyboard modifiers -> shift shinks, ctrl inverts current media type's behavior
            mod = app.queryKeyboardModifiers()
            shrink = mod & Qt.ShiftModifier
            reverse_behavior = mod & Qt.ControlModifier

            # determine desired behavior for current media type, then invert if necessary
            checked = settings.checkSnapOnResize.checkState() and self.is_snap_mode_enabled()
            if (checked and reverse_behavior) or (not checked and not reverse_behavior): return

            force_instant_resize = checked == 0
            self.snap_to_player_size(shrink=shrink, force_instant_resize=force_instant_resize)
        if event: return super().timerEvent(event)


    def timerFullScreenMediaEndedEvent(self):
        ''' A timeout event separate from timerEvent as integrating it there caused timing-related
            crashes. Checks every 500 milliseconds if we've left fullscreen mode, resumed playback,
            or lost the fullscreen UI-lock already before allowing the fullscreen UI to fade again. '''
        if not self.restarted or not self.isFullScreen() or not self.lock_fullscreen_ui:
            self.lock_fullscreen_ui = False
            self.timer_fullscreen_media_ended.stop()    # kill timer


    def wheelEvent(self, event: QtGui.QWheelEvent):
        add = event.angleDelta().y() > 0
        mod = event.modifiers()                         # just modifiers instead of keyboardModifiers here for some reason
        if mod & Qt.ControlModifier:                    # TODO add more scrolling modifiers and show options like drag/drop does
            self.set_playback_speed(player.get_rate() + (0.1 if add else -0.1))
            refresh_title()
        else: self.increment_volume(get_volume_scroll_increment() if add else -get_volume_scroll_increment())
        event.accept()


    def keyPressEvent(self, event: QtGui.QKeyEvent):    # NOTE: the arrow keys seemingly do not get caught here
        #print(self.shortcut_bandaid_fix)
        key = event.key()
        mod = event.modifiers()

        # if a lineEdit has focus, ignore keypresses except for esc, which can be used to clear focus. spinboxes use QSpinBoxPassthrough
        editable = (self.lineOutput, self.lineCurrentTime)
        if any(w.hasFocus() for w in editable):
            if key == 16777216:                         # esc (clear focus)
                for widget in editable:                 # TODO there is a faster way to do this (by getting the current focus)
                    widget.clearFocus()
            return

        # this is a fix for QShortcuts not working in QSpinBoxPassthrough. it may or may not be changed in the future
        # https://stackoverflow.com/questions/10383418/qkeysequence-to-qkeyevent
        #if True:                   # TODO like in widgets.py, this had "and text" on it. why?
        sequence = QtGui.QKeySequence(event.modifiers() | event.key())
        for primary, secondary in self.shortcuts.values():
            if primary.key() == sequence or secondary.key() == sequence:
                primary.activated.emit()
                break
        #self.shortcut_bandaid_fix = False

        # if AltModifier is True but we aren't pressing alt, ignore next alt release
        if key != 16777251 and mod & Qt.AltModifier: self.ignore_next_alt = True

        # numbers 0-9
        if 48 <= key <= 57:
            jump_progress = False
            play_recent = False

            if not self.first_video_fully_loaded and settings.checkNumKeysRecentFilesOnLaunch.isChecked():
                play_recent = True
            else:
                #modifiers = {0: Qt.ControlModifier, 1: Qt.AltModifier}
                #modifier = modifiers[s.comboNumKeysSecondaryModifier.currentIndex()]
                if mod & Qt.ControlModifier:
                    secondary = settings.comboNumKeysSecondary.currentIndex()
                    jump_progress = secondary == 1
                    play_recent = secondary == 2
                else:
                    primary = settings.comboNumKeysPrimary.currentIndex()
                    jump_progress = primary == 1
                    play_recent = primary == 2

            if jump_progress:
                if self.mime_type == 'audio' and not self.is_paused:        # HACK: "replay" audio file to correct VLC's pitch-shifting bug
                    self.skip_next_vlc_progress_desync_check = True
                    play(self.video)
                set_and_update_progress(int(self.frame_count / 10 * (key - 48)))
            elif play_recent:
                if not self.recent_files: return show_on_statusbar('No recent files available.')
                if key == 48:
                    if settings.checkNumKeys0PlaysLeastRecentFile.isChecked(): index = 0
                    else: index = -10
                elif key == 49 and settings.checkNumKeys1SkipsActiveFiles.isChecked() and self.recent_files[-1] == self.video:
                    index = -2
                else: index = -(key - 48)
                path = self.recent_files[max(index, -len(self.recent_files))]
                self.open_recent_file(path, update=settings.checkNumKeysUpdateRecentFiles.isChecked())

        # handle individual keys. TODO: change these to their enums? (70 -> Qt.Key.Key_F)
        elif key == 16777216 and self.actionFullscreen.isChecked():         # esc (fullscreen only)
            self.actionFullscreen.trigger()

        # emulate menubar shortcuts when menubar is not visible (which disables shortcuts for some reason)
        elif not self.menubar.isVisible():
            if mod & Qt.ControlModifier:
                if key == 79: self.actionOpen.trigger()                     # ctrl + o (open)
                elif key == 83:
                    if mod & Qt.ShiftModifier: self.actionSaveAs.trigger()  # ctrl + shift + s (save as)
                    else: self.actionSave.trigger()                         # ctrl + s (save)
            elif mod & Qt.AltModifier:
                if key == 81: self.actionExit.trigger()                     # alt + q (exit)
        logging.debug(f'PRESSED key={key} mod={int(mod)} text="{event.text()}"')


    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        editable = (self.lineOutput, self.lineCurrentTime, self.spinHour, self.spinMinute, self.spinSecond, self.spinFrame)
        if any(w.hasFocus() for w in editable): return  # TODO

        key = event.key()
        if key != 16777251:                             # AltModifier is True but we aren't releasing alt, ignore next alt release
            if event.modifiers() & Qt.AltModifier:
                self.ignore_next_alt = True
        else:                                           # alt (ignore while dragging files or pressing other keys)
            if self.ignore_next_alt:
                self.ignore_next_alt = False
            elif not self.vlc.dragdrop_in_progress:
                self.actionShowMenuBar.trigger()
        logging.debug(f'RELEASED key={key} text="{event.text()}"')


    def contextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles creating the context menu (right-click) for the main window. '''
        context = QtW.QMenu(self)

        # add crop/zoom toggle if in crop mode or we're zoomed in
        if self.actionCrop.isChecked():
            context.addAction(self.actionCrop)
        elif image_player.zoomed:
            action_disable_zoom = QtW.QAction('&Zoomed')
            action_disable_zoom.setCheckable(True)
            action_disable_zoom.setChecked(True)
            action_disable_zoom.triggered.connect(image_player.disableZoom)
            context.addAction(action_disable_zoom)

        # add bilinear filtering toggle if showing image/gif/cover art
        # NOTE: bilinear filtering is not yet supported for animated GIFs (part of larger project)
        if image_player.pixmap():
            action_toggle_filtering = QtW.QAction('Bilinear &filtering')
            action_toggle_filtering.setCheckable(True)
            action_toggle_filtering.setChecked(settings.checkScaleFiltering.isChecked())
            action_toggle_filtering.triggered.connect(settings.checkScaleFiltering.setChecked)

            context.addAction(action_toggle_filtering)
            context.addSeparator()

        # add separator if we've added one of the above optionnal actions
        if context.actions():
            context.addSeparator()

        # main shortcut actions (only show copy image action if there's something to copy)
        context.addAction(self.actionStop)
        context.addAction(self.actionSettings)
        if self.mime_type != 'audio' or image_player.pixmap():
            context.addAction(self.refresh_copy_image_action())

        # add all menubar menus
        context.addSeparator()
        context.addMenu(self.menuFile)
        context.addMenu(self.menuEdit)
        context.addMenu(self.menuVideo)
        context.addMenu(self.menuAudio)
        context.addMenu(self.menuWindow)
        context.addMenu(self.menuHelp)

        # add labels with info about the current media, then show context menu
        if self.video: self.add_info_actions(context)
        context.exec(event.globalPos())


    def frameProgressContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        precision_action = QtW.QAction(settings.checkHighPrecisionProgress.text())
        precision_action.setCheckable(True)
        precision_action.setChecked(settings.checkHighPrecisionProgress.isChecked())
        precision_action.setToolTip(settings.checkHighPrecisionProgress.toolTip())
        precision_action.toggled.connect(settings.checkHighPrecisionProgress.setChecked)

        context = QtW.QMenu(self)
        context.setToolTipsVisible(True)
        context.addAction(precision_action)
        context.exec(event.globalPos())


    def pauseButtonContextMenuEvent(self, event: QtGui.QContextMenuEvent):  # should these use QWidget.actions() instead of contextMenuEvent?
        ''' Handles the context (right-click) menu for the pause button. '''
        context = QtW.QMenu(self)
        context.addAction(self.actionStop)
        context.addAction('Restart', set_and_update_progress)               # TODO this might have timing issues with update_thread
        context.exec(event.globalPos())


    def trimButtonContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles the context (right-click) menu for the start/end
            trim buttons. Includes the fade-mode menu, actions for
            instantly setting new start/end positions, and disabled
            actions displaying information about the current trim. '''
        is_trim_mode = self.is_trim_mode()
        show_length_label = is_trim_mode and self.minimum or self.maximum != self.frame_count

        # create disabled action for displaying start time
        verb = 'Start' if is_trim_mode else 'Fade to'
        if self.minimum:
            h, m, s, ms = get_hms(self.minimum / self.frame_rate)
            if self.duration < 3600: start_label_action = QtW.QAction(f'{verb} {m}:{s:02}.{ms:02} (frame {self.minimum})')
            else: start_label_action = QtW.QAction(f'{verb} {h}:{m:02}:{s:02} (frame {self.minimum})')
        else: start_label_action = QtW.QAction(f'{verb}: Disabled')
        start_label_action.setEnabled(False)

        # create disabled action for displaying end time
        verb = 'End' if is_trim_mode else 'Fade from'
        if self.maximum != self.frame_count:
            h, m, s, ms = get_hms(self.maximum / self.frame_rate)
            if self.duration < 3600: end_label_action = QtW.QAction(f'{verb}: {m}:{s:02}.{ms:02} (frame {self.maximum})')
            else: end_label_action = QtW.QAction(f'{verb}: {h}:{m:02}:{s:02} (frame {self.maximum})')
        else: end_label_action = QtW.QAction(f'{verb}: Disabled')
        end_label_action.setEnabled(False)

        # create disabled action for displaying trim length, if applicable
        if show_length_label:
            frames = self.maximum - self.minimum
            seconds = frames / self.frame_rate
            h, m, s, ms = get_hms(seconds)
            if seconds < 3600: length_label_action = QtW.QAction(f'Length: {m}:{s:02}.{ms:02} ({frames} frames)')
            else: length_label_action = QtW.QAction(f'Length: {h}:{m:02}:{s:02} ({frames} frames)')
            length_label_action.setEnabled(False)

        # actions for force-setting start/end times (disabled when no/useless media is playing)
        set_start_action = QtW.QAction('Set &start to current position', self)
        set_start_action.triggered.connect(lambda: self.set_trim_start(force=True))
        set_end_action = QtW.QAction('Set &end to current position', self)
        set_end_action.triggered.connect(lambda: self.set_trim_end(force=True))
        if not self.video or self.is_static_image:
            set_start_action.setEnabled(False)
            set_end_action.setEnabled(False)

        # create context menu
        context = QtW.QMenu(self)
        context.addAction(set_start_action)
        context.addAction(set_end_action)
        context.addSeparator()
        context.addMenu(self.menuTrimMode)
        context.addSeparator()
        context.addAction(start_label_action)
        context.addAction(end_label_action)
        if show_length_label: context.addAction(length_label_action)
        context.exec(event.globalPos())


    def openMediaLocationButtonContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles the context (right-click) menu for the open media location button. '''
        if not self.video: return       # do not render context menu if no media is playing
        context = QtW.QMenu(self)
        context.addAction(self.actionExploreMediaPath)
        context.addAction(self.actionCopyMediaPath)
        context.addAction(self.actionCopyFile)
        context.addAction(self.actionCutFile)
        if image_player.pixmap():       # add "Copy image" action if we're viewing an image
            context.addAction(self.refresh_copy_image_action())

        self.add_info_actions(context)
        context.exec(event.globalPos())


    def buttonMarkDeletedContextMenuEvent(self, event: QtGui.QContextMenuEvent):    # should these use QWidget.actions() instead of contextMenuEvent?
        ''' Handles the context (right-click) menu for buttonMarkDeleted. '''
        context = QtW.QMenu(self)
        context.setToolTipsVisible(True)
        context.addAction(self.actionMarkDeleted)
        context.addAction(self.actionClearMarked)
        context.addAction(self.actionShowDeletePrompt)
        context.addSeparator()
        context.addAction(self.actionDeleteImmediately)
        context.exec(event.globalPos())


    def buttonSnapshotContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles the context (right-click) menu for the snapshot button.
            Side note: PyQt does NOT like it if you do QMenu.exec() in a
            lambda. As soon as it returns, you get: `TypeError: invalid
            argument to sipBadCatcherResult()`. And it's uncatchable. '''
        context = QtW.QMenu(self)
        for index, action in enumerate(self.menuSnapshots.actions()):
            if index == 2 and image_player.pixmap():
                context.addAction(self.refresh_copy_image_action())
            context.addAction(action)
        context.exec(event.globalPos())


    def buttonAutoplayContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        context = QtW.QMenu(self)
        context.addActions(self.menuAutoplay.actions()[1:])
        context.exec(event.globalPos())


    def menuRecentContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles the context (right-click) menus for individual recent files. '''
        action = self.menuRecent.actionAt(event.pos())
        if action is self.actionClearRecent or not action: return
        path = action.toolTip()
        context = QtW.QMenu(self)

        explore_action = QtW.QAction('M&edia location')
        explore_action.triggered.connect(lambda: self.explore(path))
        copy_action = QtW.QAction('&Copy media path')
        copy_action.triggered.connect(lambda: self.copy(path))
        remove_action = QtW.QAction('&Remove from recent files')
        remove_action.triggered.connect(lambda: (self.recent_files.remove(path), self.refresh_recent_menu()))
        move_to_top_action = QtW.QAction('&Move to top')
        move_to_top_action.triggered.connect(lambda: self.open_recent_file(path, update=True, open=False))
        open_update_action = QtW.QAction('&Open and move to top')
        open_update_action.triggered.connect(lambda: self.open_recent_file(path, update=True))
        open_no_update_action = QtW.QAction('&Open without moving to top')
        open_no_update_action.triggered.connect(lambda: self.open_recent_file(path, update=False))

        context.addAction(remove_action)
        context.addSeparator()
        context.addAction(explore_action)
        context.addAction(copy_action)
        context.addSeparator()
        context.addAction(move_to_top_action)
        context.addAction(open_update_action)
        context.addAction(open_no_update_action)
        context.exec(event.globalPos())


    # ---------------------
    # >>> THEMES <<<
    # ---------------------
    def load_themes(self):
        logging.info('Loading themes...')
        self.themes = []
        for filename in os.listdir(constants.THEME_DIR):
            if filename[-4:] in ('.qss', '.css', '.txt'):   # this isn't the best way to parse css, but it works well enough
                getting_theme_data = False
                theme = {                                   # default theme properties
                    'name': 'Unnamed Theme',
                    'description': 'Please add a "Theme {}" section to your stylesheet with name, description, and version strings specified.',
                    'version': '0',
                    'stylesheet': '',
                    'special_widgets': None
                }

                theme_info_lines = []
                with open(f'{constants.THEME_DIR}{sep}{filename}') as theme_file:
                    theme['stylesheet'] = theme_file.read()
                    for line in theme['stylesheet'].split('\n'):
                        line = line.strip()
                        if getting_theme_data:
                            if line[-1] == '}':             # TODO assert theme properties? also this breaks if multiple {}'s are on one line
                                break
                            theme_info_lines.append(line)
                        if line.split()[0].rstrip('{') == 'Theme':
                            getting_theme_data = True

                    theme_info = (text.strip() for text in ' '.join(theme_info_lines).split(';') if text)
                    for info in theme_info:
                        parts = info.split(':')
                        key, value = parts[0].strip().lower(), ':'.join(parts[1:]).strip().strip('"').strip("'")    # strip whitespace/quotes and cleanup key-value pair
                        theme[key] = value                  # replace theme properties with info retrieved from top of theme file
                    self.themes.append(theme)


    def refresh_theme_combo(self, *args, restore_theme=True, set_theme=None):   # *args to capture unused signal args
        self.load_themes()
        comboThemes = settings.comboThemes
        old_theme = comboThemes.currentText()               # save current theme's name
        for _ in range(comboThemes.count()): comboThemes.removeItem(1)
        for theme in self.themes:
            try:
                name = theme.get('name', None)
                if name: comboThemes.addItem(name)
            except: logging.warning(f'Could not add theme {name} to theme combo: {format_exc()}')
        if set_theme: comboThemes.setCurrentText(set_theme)
        elif restore_theme: comboThemes.setCurrentText(old_theme)               # attempt to restore theme based on previous theme's name
        return old_theme


    def get_theme(self, theme_name):
        if theme_name == 'none' or theme_name == '': return None
        for theme in self.themes:
            try:
                if theme_name.lower() == theme['name'].lower():
                    return theme
            except: pass


    def set_theme(self, theme_name):
        theme = self.get_theme(theme_name)
        logging.info(f'Setting theme to {theme.get("name") if theme else None}')
        old_theme = self.get_theme(config.cfg.theme)        # config.cfg must be used because this is called before cfg is returned from config.py

        # undo the QToolTip workaround mentioned below
        if old_theme is not None and old_theme['special_widgets']:
            for widget in old_theme['special_widgets']:
                widget.setStyleSheet('')

        if theme is None:
            self.setStyleSheet('')
            settings.comboThemes.setToolTip('No theme is currently selected.')
            config.cfg.theme = 'None'
        else:
            try:
                stylesheet = theme['stylesheet']
                self.setStyleSheet(stylesheet)
                settings.comboThemes.setToolTip(theme['description'])
                config.cfg.theme = theme['name']

                # Workaround for QToolTip's not supporting widget identifiers
                qtooltip_index = stylesheet.find('QToolTip#')
                special_widgets = []
                while qtooltip_index != -1:
                    for index, c in enumerate(stylesheet[qtooltip_index:]):
                        if c in (' ', ',', '{'):
                            widget_name = stylesheet[qtooltip_index + 9:qtooltip_index + index]
                            break
                    widget = self.findChild(QtW.QWidget, widget_name)
                    if widget is not None:
                        tooltip_stylesheet = stylesheet[stylesheet.find('{', qtooltip_index):stylesheet.find('}', qtooltip_index) + 1]
                        widget.setStyleSheet(f'QToolTip {tooltip_stylesheet}')
                        special_widgets.append(widget)
                    qtooltip_index = stylesheet.find('QToolTip#', qtooltip_index + 1)
                if special_widgets: theme['special_widgets'] = special_widgets
            except Exception as error: logging.warning(f'Theme \'{theme["name"]}\' failed to load with the following error - {type(error)}: {error}.')

        # adjust UI spacing to match theme
        opt = QtW.QStyleOptionSlider()
        self.sliderProgress.initStyleOption(opt)
        groove_rect = self.sliderProgress.style().subControlRect(QtW.QStyle.CC_Slider, opt, QtW.QStyle.SC_SliderGroove, self.sliderProgress)
        handle_rect = self.sliderProgress.style().subControlRect(QtW.QStyle.CC_Slider, opt, QtW.QStyle.SC_SliderHandle, self.sliderProgress)
        self.frameProgress.setMaximumHeight(max(16, groove_rect.height() + 6, handle_rect.height() + 6))    # frameProgress needs +4 pixels, and +2 pixels of padding


    # -------------------------------
    # >>> BASIC VIDEO OPERATIONS <<<
    # -------------------------------
    def shuffle_media(self, folder: str = None):
        if folder is None:                                  # no folder provided, shuffle within current folder
            base_file = self.video
            current_dir, current_basename = os.path.split(base_file)
        else:
            base_file = ''
            current_dir = folder
            current_basename = ''

        # i was surprised to find that shuffling the strings directly is *very* slightly...
        # ...faster than making a list of indexes and shuffling/using that instead
        files = os.listdir(current_dir)
        random.shuffle(files)

        # aliases for the loop
        update_recent_list = settings.checkAutoplayShuffleAddToRecents.isChecked()
        skip_marked = self.checkSkipMarked.isChecked()
        marked = self.marked_for_deletion
        locked_video_path = self.locked_video
        open = self.open
        ignore = self.shuffle_ignore_unique
        ignore_order = self.shuffle_ignore_order

        # define valid mime types (no autoplay for images or gifs (yet?))
        if settings.checkAutoplaySameMime.isChecked() and self.mime_type != 'image':
            valid_mime_types = (self.mime_type,)
        else:
            valid_mime_types = ('video', 'audio')

        # if we've switched folders, update shuffle folder and clear ignore list
        if self.shuffle_folder != current_dir:
            self.shuffle_folder = current_dir
            ignore.clear()
            ignore_order.clear()

        logging.info(f'Shuffling inside {current_dir} ({len(ignore)}/{len(files)} files to ignore)...')

        # add the current file to the ignore list rather than the next file we play
        # this way, we ensure the current file is always ignored but the next...
        # ...file has a chance to be replayed if we manually cycle off of it
        if current_basename and current_basename not in ignore:
            ignore.add(current_basename)
            ignore_order.append(current_basename)

        start = get_time()
        for filename in files:
            file = f'{current_dir}{sep}{filename}'

            # get mime type of file to verify this is actually playable and skip the extra setup done in open()
            try:
                mime, extension = filetype.match(file).mime.split('/')
                if mime not in valid_mime_types: continue
            except: continue

            # check for reasons we might skip a playable file (from most to least likely)
            # NOTE: we don't skip just-edited clips like in `cycle_media` (for performance)
            if filename in ignore: continue
            if file_is_hidden(file): continue
            if skip_marked and file in marked: continue
            if filename == current_basename: continue
            if file == locked_video_path: continue

            # if file gets opened, check the size of our ignore list and return the file
            if open(file, _from_cycle=True, _from_autoplay=True,
                    update_recent_list=update_recent_list, mime=mime, extension=extension) != -1:
                logging.info(f'Shuffled to new file after {get_time() - start:.3f} seconds.')
                max_ignore_length = settings.spinAutoplayMaxFiles.value()
                if len(ignore) > max_ignore_length:
                    logging.info('Shuffling ignore list at max capacity. Removing oldest file(s)...')
                    difference = len(ignore_order) - max_ignore_length
                    for file in ignore_order[:difference]:
                        ignore.remove(file)
                    self.shuffle_ignore_order = ignore_order[difference:]                   # don't assign to alias here!!
                return file

        # nothing played - unmark autoplay flag
        self.current_file_is_autoplay = False

        # ignore list has multiple files - we ran out of files to play. clear it and shuffle again
        if len(ignore) > 1:
            logging.info('All files played. Clearing shuffle ignore list and reshuffling...')
            ignore.clear()
            ignore_order.clear()
            return self.shuffle_media(folder)

        # nothing could be or has been played - show appropriate log message on statusbar
        return log_on_statusbar('This is the only playable video in this folder.')


    def cycle_media(
        self,
        *args,
        next: bool = True,
        ignore: tuple = tuple(),
        update_recent_list: bool = True,
        autoplay: bool = False,
        index_override: int = 0
    ):                                              # *args to capture unused signal args
        ''' Cycles through the current media's folder and looks for the `next`
            or previous openable, non-hidden file that isn't in the `ignore`
            list. If there are no other openable files, nothing happens.
            Otherwise, the new file is opened and returned.

            TODO: This needs a lot of work.
                - implement OS-specific sorting alorithms
                - is there a faster (safe) way of getting our current index in a folder?
                - when `current_media` is missing, we should insert into `files`, resort, and get index that way
                - is there EVER a scenario where an `index_offset` of 1 results in a wrongly skipped video? '''
        original_video_path = self.video_original_path
        current_video_path = self.video
        base_file = original_video_path if settings.checkCycleRememberOriginalPath.checkState() else current_video_path
        self.last_cycle_was_forward = next

        # update autoplay icon if needed
        if self.actionAutoplayDirectionDynamic.isChecked() and not self.actionAutoplayShuffle.isChecked():
            if next: self.buttonAutoplay.setIcon(self.icons['autoplay'])
            else: self.buttonAutoplay.setIcon(self.icons['autoplay_backward'])

        if not current_video_path: return show_on_statusbar('No media is playing.', 10000)  # TODO remember last media's folder between sessions?
        logging.info(f'Getting {"next" if next else "previous"} media file...')

        current_dir, current_basename = os.path.split(base_file)
        files = os.listdir(current_dir)
        if len(files) == 1: return log_on_statusbar('This is the only file in this folder.')

        # get current position in folder so we know where to start from
        if current_basename in files: current_index = files.index(current_basename)         # original path might not exist anymore
        elif self.last_cycle_index is not None: current_index = self.last_cycle_index
        else:           # video was moved/renamed and never cycled, use human sorting to roughly determine where to start from
            import re   # https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
            test = lambda char: int(char) if char.isdigit() else char                       # NOTE: Most OS's do not actually use pure human sorting
            human_sort = lambda string: [test(c) for c in re.split(r'(\d+)', os.path.splitext(string)[0])]
            restored_files = files.copy()
            restored_files.append(current_basename)
            restored_files.sort(key=human_sort)
            current_index = max(0, min(len(files), restored_files.index(current_basename)) - 1)

        # TODO do we need to apply index_offset to the end points too?
        # TODO these numbers are wrong. all of them. they have to be
        #if next: file_range = range(current_index + 1, len(files) + current_index + 1)
        #else: file_range = range(current_index - 1, current_index - len(files) - 1, -1)
        #if next: file_range = range(current_index + index_offset, len(files) + current_index + 1)
        #else: file_range = range(current_index - index_offset, current_index - len(files) - 1, -1)
        # TODO i give up. just eat the performance hit from the extra file/checks we have to go through
        if next: file_range = range(current_index, len(files) + current_index + 1)
        else: file_range = range(current_index, current_index - len(files) - 1, -1)

        # aliases for the loop
        skip_marked = self.checkSkipMarked.isChecked()
        marked = self.marked_for_deletion
        locked_video_path = self.locked_video
        open = self.open

        if autoplay:                                # no autoplay for images or gifs (yet?)
            if settings.checkAutoplaySameMime.isChecked(): valid_mime_types = (self.mime_type,)
            else: valid_mime_types = ('video', 'audio')
        else: valid_mime_types = ('video', 'image', 'audio')

        skipped_old_video = False
        start = get_time()
        for new_index in file_range:
            new_index = new_index % len(files)

            file = f'{current_dir}{sep}{files[new_index]}'
            #logging.debug(f'Checking {file} at index #{new_index}')

            # get mime type of file to verify this is actually playable and skip the extra setup done in open()
            try:
                mime, extension = filetype.match(file).mime.split('/')
                if mime not in valid_mime_types: continue
            except: continue

            # check for reasons we might skip a playable file (from most to least likely)
            if file_is_hidden(file): continue
            if file in ignore: continue
            if skip_marked and file in marked: continue
            #if index_offset == 0 and (file == original_video_path or file == current_video_path): continue
            if file == original_video_path:
                skipped_old_video = original_video_path != current_video_path
                continue
            if file == current_video_path: continue
            if file == locked_video_path: continue

            # attempt to play file -> -1 is returned if file can't be opened
            # if the new video opens successfully, stop
            if open(file, _from_cycle=True, _from_autoplay=autoplay,
                    update_recent_list=update_recent_list, mime=mime, extension=extension) != -1:
                logging.info(f'Cycled files after {get_time() - start:.3f} seconds.')
                self.last_cycle_index = new_index
                return file

        # nothing played - unmark autoplay flag and show appropriate log message on statusbar
        if autoplay: self.current_file_is_autoplay = False
        if not skipped_old_video: log = 'This is the only playable media file in this folder.'
        else: log = 'This and the file you just edited are the only playable media files in this folder.'
        return log_on_statusbar(log)


    def cycle_recent_files(self, forward: bool = True):
        # NOTE: recent_files is least recent to most recent -> index 0 is the LEAST recent
        if self.video not in self.recent_files:     # default to latest file if no valid file is loaded
            current_index = len(self.recent_files)
        else: current_index = self.recent_files.index(self.video)
        new_index = current_index + (1 if forward else -1)
        if 0 <= new_index <= len(self.recent_files) - 1:
            path = self.recent_files[new_index]
            self.open_recent_file(path, update=False)


    def open_recent_file(self, path: str, update: bool, open: bool = True):
        try:
            recent_files = self.recent_files
            if path == self.locked_video:           # recent file is locked (it's actively being edited)
                log_on_statusbar(f'Recent file {path} is currently being worked on.')
            elif os.path.isfile(path):
                if open:
                    if self.open(path, update_recent_list=update) != -1:
                        log_on_statusbar(f'Opened recent file #{len(recent_files) - recent_files.index(path)}: {path}')
                    else:
                        log_on_statusbar(f'Recent file {path} could not be opened.')
                        recent_files.remove(path)
                else:                               # don't open, just move file to top
                    recent_files.append(recent_files.pop(recent_files.index(path)))
            else:
                log_on_statusbar(f'Recent file {path} no longer exists.')
                recent_files.remove(path)
        except ValueError: pass                     # ValueError -> path was not actually in recent_files
        finally: self.refresh_recent_menu()


    def open_folder(self, folder: str, mod: int = 0, focus_window: bool = True):
        try:
            if mod & Qt.AltModifier:                # alt (use shuffle mode to play video but disable autoplay)
                self.actionAutoplay.setChecked(False)
                self.shuffle_media(folder)
            elif mod & Qt.ShiftModifier:            # shift (play folder with autoplay in shuffle mode)
                self.actionAutoplay.setChecked(True)
                self.actionAutoplayShuffle.setChecked(not self.actionAutoplayShuffle.isChecked())
                self.shuffle_media(folder)
            else:
                #skip_marked = self.checkSkipMarked.isChecked()
                #marked = self.marked_for_deletion  # TODO should we?
                locked_video_path = self.locked_video
                open = self.open

                start = get_time()
                for filename in os.listdir(folder):
                    file = f'{folder}{sep}{filename}'

                    # get mime type of file to verify this is actually playable and skip the extra setup done in open()
                    try: mime, extension = filetype.match(file).mime.split('/')
                    except: continue

                    if file_is_hidden(file): continue
                    if file == locked_video_path: continue
                    #if skip_marked and file in marked: continue

                    if open(file, _from_cycle=True, mime=mime, extension=extension) != -1:
                        logging.info(f'Found playable file in folder after {get_time() - start:.3f} seconds.')
                        enabled = not (mod & Qt.ControlModifier)
                        verb = 'enabled' if enabled else 'disabled'
                        self.actionAutoplay.setChecked(enabled)
                        self.refresh_autoplay_button()
                        log_on_statusbar(f'Opened {filename} from folder {file} and {verb} Autoplay.')
                        return -1

                log_on_statusbar(f'No files in {folder} were playable.')
                return -1
        except: log_on_statusbar(f'(!) Failed while checking folder "{folder}" for openable media: {format_exc()}')
        finally: self.refresh_autoplay_button()


    def open_lastdir(self):
        qthelpers.openPath(cfg.lastdir)


    def explore(self, path: str = None, noun: str = 'Recent file'):
        ''' Opens `path` (or self.video if not provided) in the default file
            explorer, with `path` pre-selected if possible. `noun` controls
            how `path` is described in any log messages.'''
        if not path: path = self.video if self.video else cfg.lastdir
        if not exists(path):
            if path in self.recent_files:
                self.recent_files.remove(path)
            return log_on_statusbar(f'{noun} "{path}" no longer exists.')
        else: qthelpers.openPath(path, explore=True)


    def copy(self, path: str = None, noun: str = 'Recent file'):
        ''' Copies `path` (or self.video if not provided) to the clipboard,
            with backslashes escaped (if desired) and surrounded by quotes.
            `noun` controls how `path` is described in any log messages. '''
        if not path: path = self.video if self.video else cfg.lastdir
        if not exists(path):
            if path in self.recent_files:
                self.recent_files.remove(path)
            return log_on_statusbar(f'{noun} "{path}" no longer exists.')
        else:
            if settings.checkCopyEscapeBackslashes.isChecked():
                sep = '\\'
                escaped_sep = r'\\'
                app.clipboard().setText(f'"{path.replace(sep, escaped_sep)}"')
            else: app.clipboard().setText(f'"{path}"')


    def copy_file(self, path: str = None, cut: bool = False):
        if not path:
            if not self.video: return
            path = self.video
        if not exists(path): return log_on_statusbar(f'File "{path}" no longer exists.')
        mime = QtCore.QMimeData()
        mime.setUrls((QtCore.QUrl.fromLocalFile(path),))

        # https://stackoverflow.com/questions/47443545/cut-and-paste-clipboard-exchange-between-qt-application-and-windows-explorer
        # this is total nonsense and I have no idea why this works
        if cut:
            if constants.PLATFORM == 'Windows':
                data = QtCore.QByteArray()
                stream = QtCore.QDataStream(data, QtCore.QIODevice.WriteOnly)
                magic = QtCore.QByteArray()         # you HAVE to do these two lines
                stream << magic                     # we are bitshifting literally nothing into the data stream
                mime.setData('Preferred DropEffect', data)
                if path == self.video: self.stop()  # stop player if necessary so we can actually paste the file somewhere
            else:                                   # TODO crossplatform linux/mac support
                return show_on_statusbar('Cutting files is limited to Windows for now.')
            log_on_statusbar(f'File "{os.path.basename(path)}" cut to clipboard.')
        else:
            log_on_statusbar(f'File "{os.path.basename(path)}" copied to clipboard.')
        app.clipboard().setMimeData(mime)


    # https://stackoverflow.com/questions/34322132/copy-image-to-clipboard
    # https://stackoverflow.com/questions/34697559/pil-image-to-qpixmap-conversion-issue/75498151#75498151
    def copy_image(self, path: str = None, extended: bool = None):
        ''' Copies the currently open image to the clipboard. Uses `PIL` to
            crop image if crop mode is enabled. Cropped images are saved to
            a buffer as QImage does not save a copy of its own data (???),
            so as soon as it's out of scope in Python, everything crashes.

            If `extended` is True, a size/quality dialog will be shown.
            TODO: This is pretty messy. I rewrote `snapshot()` to reduce the
            amount of duplicate code, but it could still be a lot simpler. '''
        try:
            mime = self.mime_type
            if not path:
                if not self.video: return
                path = self.video
            if not exists(path) and not (mime == 'image' and path == self.video):
                return log_on_statusbar(f'Image "{path}" no longer exists.')
            if mime == 'audio' and not image_player.pixmap():
                return log_on_statusbar('You can only snapshot audio with cover art.')

            # I don't know how to jpeg-ify image data without saving/reopening so we need this to delete the excess file
            delete_path_anyway = False
            width = 0
            height = 0
            quality = 100
            temp_string = ''

            # verify `extended` and check whether we need to take a snapshot or not
            if extended is None:
                modifiers_pressed = bool(app.keyboardModifiers())
                inverted = settings.checkCopyPrimaryUsesDialog.isChecked()
                extended = (modifiers_pressed and not inverted) or (not modifiers_pressed and inverted)
            snapshot_needed = path == self.video and (mime == 'video' or mime == 'audio')

            # if we're watching a video or audio with cover art, snapshot the frame/cover art first
            if snapshot_needed:
                path = self.snapshot(mode='full' if extended else 'quick', is_temp=True)
                if path is None: return             # dialog canceled (finally-statement ensures we unpause if needed)
                temp_string = ' Temporary snapshot file has been deleted.'
            elif extended:
                if self.is_gif: image_player.gif.setPaused(True)
                else: player.set_pause(True)
                width, height, quality = self.show_size_dialog(snapshot=True)
                if width is None: return            # dialog canceled (finally-statement ensures we unpause if needed)

            log_on_statusbar('Copying image data to clipboard...')
            if not self.actionCrop.isChecked():     # no crop - copy entire image/frame
                if extended:
                    try:    # if path still equals self.video, that means it wasn't snapshotted -> must be image
                        if path == self.video: image = get_PIL_Image().fromqpixmap(image_player.pixmap())
                        else: image = get_PIL_Image().open(path)
                        if width or height: image = image.resize((width, height))
                        if quality < 100:
                            delete_path_anyway = True
                            path = self.convert_snapshot_to_jpeg(None, image, quality)
                            image = get_PIL_Image().open(path)

                        # put resized/jpeg-ified image data onto clipboard
                        self.clipboard_image_buffer = image.toqimage()
                        app.clipboard().setImage(self.clipboard_image_buffer)

                    except: return log_on_statusbar(f'(!) Image copying failed: {format_exc()}')
                    finally: image.close()
                else:
                    if path == self.video:          # if a snapshot was needed earlier, this will never be True
                        if self.is_gif: app.clipboard().setImage(image_player.gif.currentImage())         # setImage is faster
                        else: app.clipboard().setPixmap(image_player.pixmap())
                    else: app.clipboard().setImage(QtGui.QImage(path))
                log_on_statusbar(f'Image data for "{os.path.basename(path)}" copied to clipboard.{temp_string}')
            else:                                   # crop image/frame and copy crop region
                try:    # no with-statement here just in case Pillow doesn't close `image` when it gets reassigned
                    if path == self.video: image = get_PIL_Image().fromqpixmap(image_player.pixmap())
                    else: image = get_PIL_Image().open(path)

                    # calculate factors between media's native resolution and actual desired snapshot resolution
                    if not snapshot_needed:                         # snapshot() already cropped the snapshot for us
                        if width or height:                         # custom width and/or height is set
                            if width:
                                x_factor = self.vwidth / width
                                if not height: y_factor = x_factor  # width is set but height isn't -> match factors
                            if height:
                                y_factor = self.vheight / height
                                if not width: x_factor = y_factor   # height is set but width isn't -> match factors
                            image = image.resize((width, height))   # resize image
                        else:                                       # neither is set -> use 1 to avoid division by 0
                            x_factor = 1
                            y_factor = 1

                        # use factors to crop snapshot relative to the snapshot's actual resolution for an accurate crop
                        lfp = self.vlc.last_factored_points
                        image = image.crop((round(lfp[0].x() / x_factor), round(lfp[0].y() / y_factor),   # left/top/right/bottom (crop takes a tuple)
                                            round(lfp[3].x() / x_factor), round(lfp[3].y() / y_factor)))  # round QPointFs

                        # convert image data to jpeg if quality below 100 is requested
                        if quality < 100:
                            delete_path_anyway = True
                            path = self.convert_snapshot_to_jpeg(None, image, quality)
                            image = get_PIL_Image().open(path)

                    # put resized/cropped/jpeg-ified image data onto clipboard
                    self.clipboard_image_buffer = image.toqimage()
                    app.clipboard().setImage(self.clipboard_image_buffer)

                except: return log_on_statusbar(f'(!) Image copying failed: {format_exc()}')
                finally: image.close()
                log_on_statusbar(f'Cropped image data for "{os.path.basename(path)}" copied to clipboard.{temp_string}')

            if snapshot_needed or delete_path_anyway:
                logging.info(f'Deleting temporary snapshot at path {path}')
                try: os.remove(path)
                except: logging.warning('(!) FAILED TO DELETE TEMPORARY SNAPSHOT')
        except: log_on_statusbar(f'(!) Image copying failed: {format_exc()}')
        finally:                                    # restore pause-state before leaving
            if self.is_gif: image_player.gif.setPaused(self.is_paused)
            else: player.set_pause(self.is_paused)


    def parse_media_file(self, file, probe_file=None, mime='video', extension=None, data=None):
        ''' Parses a media file for relevant metadata and emits _open_signal.
            This *could* be simpler, but it still needs to be fast.
            The following properties should be set by this function:
                - self.mime_type
                - self.extension
                - self.video
                    - self.duration             (media duration in seconds)
                    - self.frame_count          (number of frames)
                    - self.frame_rate           (frames per second)
                    - self.frame_rate_rounded   (rounded frame rate, for UI purposes)
                    - self.delay                (delay between frames in seconds)
                    - self.vwidth               (media width)
                    - self.vheight              (media height)
                    - self.ratio                (aspect ratio, as a string) '''
        try:
            base_mime = mime
            if mime == 'video':
                if probe_file or data:
                    if data or self.vlc.media.get_parsed_status() != 4 or player.get_fps() == 0 or player.get_length() == 0 or player.video_get_size() == (0, 0):
                        start = get_time()
                        if data is None:            # VLC not finished, no data provided, but probe file is being generated
                            while not exists(probe_file): pass
                            with open(probe_file) as probe:
                                while data is None:
                                    try: data = json.load(probe)
                                    except:
                                        if self.vlc.media.get_parsed_status() == 4 and player.get_fps() != 0 and player.get_length() != 0 and player.video_get_size() != (0, 0):
                                            logging.info(f'VLC finished parsing while waiting for FFprobe ({get_time() - start:.4f} seconds).')
                                            break
                                        if get_time() - start > 5:
                                            logging.error('Media probe did not finish after 5 seconds.')
                                            return -1
                                        probe.seek(0)

                        if data:                    # double check if data was actually acquired
                            logging.info(f'FFprobe needed an additional {get_time() - start:.4f} seconds to parse.')
                            #logging.debug(f'FFprobe for {file}:\n{data}')
                            for stream in data['streams']:
                                if stream['codec_type'] == 'video' and stream['avg_frame_rate'] != '0/0':
                                    fps_parts = stream['avg_frame_rate'].split('/')
                                    fps = int(fps_parts[0]) / int(fps_parts[1])
                                    duration = float(data['format']['duration'])

                                    self.duration = duration
                                    self.frame_count = math.ceil(duration * fps)    # NOTE: nb_frames is unreliable for partially corrupt videos
                                    self.frame_rate = fps
                                    self.frame_rate_rounded = round(fps)
                                    self.delay = 1 / fps

                                    self.vwidth = int(stream['width'])
                                    self.vheight = int(stream['height'])
                                    self.ratio = stream.get('display_aspect_ratio', get_aspect_ratio(self.vwidth, self.vheight))
                                    break
                            else: mime = 'audio'    # the rare for-else-loop ("else" only happens if we don't break). audio streams usually report 0/0
                            logging.info('FFprobe parsed faster than VLC.')

                # still no FFprobe probe data, we MUST wait for VLC to finish (if it ever does)
                if data is None:
                    if self.vlc.media.get_parsed_status() != 4 or player.get_fps() == 0 or player.get_length() == 0 or player.video_get_size() == (0, 0):
                        start = get_time()          # get_parsed_status() == 4 means parsing is apparently done, but values are often not accessible immediately
                        while self.vlc.media.get_parsed_status() != 4 or player.get_fps() == 0 or player.get_length() == 0 or player.video_get_size() == (0, 0):
                            if get_time() - start > 15:
                                logging.error('FFprobe is disabled and VLC did not finish parsing after 15 seconds.')
                                return -1
                        logging.info(f'VLC needed an additional {get_time() - start:.4f} seconds to parse.')
                    elif probe_file: logging.info('VLC did not need additional time to parse.')
                    fps = round(player.get_fps(), 1)        # TODO: self.vlc.media.get_tracks() might be more accurate, but I can't get it to work
                    duration = round(player.get_length() / 1000, 4)
                    self.duration = duration
                    self.frame_count = int(duration * fps)
                    self.frame_rate = fps
                    self.frame_rate_rounded = round(fps)
                    self.delay = 1 / fps
                    self.vwidth, self.vheight = player.video_get_size()
                    self.ratio = get_aspect_ratio(self.vwidth, self.vheight)
                    logging.info('VLC parsed faster than FFprobe.')

            if mime == 'audio':
                if data:
                    for stream in data['streams']:
                        if stream['codec_type'] == 'video' and stream['avg_frame_rate'] == '0/0':
                            data = None             # audio file has 0fps video stream -> most likely cover art
                            break                   # set data back to None and break so we can extract the cover art
                    else:                           # the rare for-else-loop (else only happens if we don't break)
                        duration = float(data['format']['duration'])
                    self.vwidth, self.vheight = 16, 9

                if data is None:                    # no data provided OR art detected, use TinyTag (fallback to music_tag if necessary)
                    try:                            # we need to avoid parsing probe file anyway, since we need to check for cover art
                        try:
                            tag = TinyTag.get(file, image=True)     # https://pypi.org/project/tinytag/0.18.0/
                            cover_art = tag.get_image()
                            if cover_art and settings.checkShowCoverArt.isChecked():
                                play_image(cover_art)               # cover art is bytes -> set to image_player's QPixmap, open QPixmap with PIL
                                size = image_player.art.size()
                                self.vwidth = size.width()
                                self.vheight = size.height()
                            else:
                                self.vwidth = 16
                                self.vheight = 9
                            duration = tag.duration
                        except:                                     # TinyTag is lightweight but cannot handle everything
                            import music_tag                        # only import music_tag if we absolutely need to
                            tag = music_tag.load_file(file)
                            if 'artwork' in tag and settings.checkShowCoverArt.isChecked():
                                art = tag['artwork'].first
                                play_image(art.data)                # art.data is bytes -> set to image_player's QPixmap
                                self.vwidth = art.width             # music_tag directly reports width/height of artwork
                                self.vheight = art.height
                            else:
                                self.vwidth = 16
                                self.vheight = 9
                            duration = tag['#length'].value
                        #image_player.art.save(os.path.join(constants.TEMP_DIR, f'{os.path.basename(file)}_{getctime(file)}.png'))
                    except:                                         # this is to handle things that wrongly report as audio, like .ogv files
                        logging.info(f'Invalid audio file detected, parsing as a video file... {format_exc()}')
                        if probe_file:
                            start = get_time()
                            while not exists(probe_file): pass
                            with open(probe_file) as probe:
                                while data is None:
                                    try: data = json.load(probe)
                                    except: probe.seek(0)
                                    if get_time() - start > 5:
                                        logging.error('Media probe did not finish after 5 seconds.')
                                        return -1
                        return self.parse_media_file(file, probe_file, mime='video', extension=extension, data=data)
                self.duration = duration
                self.frame_count = round(duration * 20)
                self.frame_rate = 20                # TODO we only set to 20 to not deal with laggy hover-fades
                self.frame_rate_rounded = 20
                self.delay = 0.05
                self.ratio = get_aspect_ratio(self.vwidth, self.vheight)

            elif mime == 'image':
                if extension == 'gif' and image_player.gif.frameCount() > 1:
                    self.frame_count = image_player.gif.frameCount()
                    if data:                        # use probe data if available but it's not necessary
                        for stream in data['streams']:
                            if stream['codec_type'] == 'video' and stream['avg_frame_rate'] != '0/0':
                                fps_parts = stream['avg_frame_rate'].split('/')
                                fps = int(fps_parts[0]) / int(fps_parts[1])
                                duration = float(data['format']['duration'])
                        self.duration = duration
                        self.frame_rate = fps
                        self.frame_rate_rounded = round(fps)
                        self.delay = 1 / fps
                        self.vwidth = int(stream['width'])
                        self.vheight = int(stream['height'])
                    else:
                        self.delay = image_player.gif.nextFrameDelay() / 1000
                        self.duration = self.frame_count * self.delay
                        self.frame_rate = 1 / self.delay
                        self.frame_rate_rounded = round(self.frame_rate)
                        self.vwidth = image_player.gifSize.width()
                        self.vheight = image_player.gifSize.height()
                    self.ratio = get_aspect_ratio(self.vwidth, self.vheight)
                else:   # TODO: other formats have EXIF data but .getexif() is slow for images without EXIF data (except for jpegs)
                    if extension == 'jpeg':                         # use PIL to get EXIF data from jpegs
                        with get_PIL_Image().open(file) as image:   # opening with PIL is fast if we don't do any operations
                            orientation = image.getexif().get(0x0112)
                            if orientation:
                                if   orientation == 3: angle = 180
                                elif orientation == 6: angle = 90   # actually represents 270 counter-clockwise
                                elif orientation == 8: angle = 270  # actually represents 90 counter-clockwise
                                else: angle = 0
                                if angle: image_player.art = image_player.art.transformed(QtGui.QTransform().rotate(angle))
                            try: self.vwidth, self.vheight = image.size
                            except AttributeError:
                                self.vwidth = image_player.art.width()
                                self.vheight = image_player.art.height()
                    else:
                        self.vwidth = image_player.art.width()
                        self.vheight = image_player.art.height()
                    self.duration = 0.0000001       # low duration to avoid errors but still show up as 0 on the UI
                    self.frame_count = 1
                    self.frame_rate = 1
                    self.frame_rate_rounded = 1
                    self.delay = 0.2                # run update_slider_thread only 5 times/second
                    self.ratio = get_aspect_ratio(self.vwidth, self.vheight)

            assert self.duration != 0, f'File \'{file}\' appears to be corrupted or an invalid format and cannot be opened (invalid duration).'
        except:
            logging.error(f'(!) Parsing failure: {format_exc()}')
            return -1

        # extra setup. frame_rate_rounded, ratio, and delay could all be set here, but it would be slower overall
        self.video = file                           # set media AFTER opening but BEFORE _open_signal
        self.mime_type = mime
        if base_mime == 'image':
            self._open_signal.emit()                # manually emit _open_signal for images/gifs (slider thread will be idle)
            is_gif = extension == 'gif' and self.frame_count > 1
            self.is_gif = is_gif                    # do not treat single-frame GIFs as actual GIFs (static images have more features)
            self.is_static_image = not is_gif
        else:
            self.open_queued = True
            self.frame_override = 0                 # set frame_override to trigger open_queue in update_slider_thread
            self.is_gif = False
            self.is_static_image = False
        self.extension = extension
        #self.resolution_label = f'{self.vwidth:.0f}x{self.vheight:.0f}'
        if mime != 'audio': self.vlc.find_true_borders()


    def open(self, file=None, focus_window=True, update_recent_list=True, remember_old_file=False,
             mime=None, extension=None, _from_cycle=False, _from_autoplay=False):
        ''' Current iteration: IV '''
        try:
            # validate `file`. open file-dialog if needed, check if it's a folder, check if it's locked, etc.
            # (if called from sort of auto-cycling function, we can assume this stuff is already sorted out)
            if not _from_cycle:
                if not file: file, cfg.lastdir = qthelpers.browseForFile(cfg.lastdir, 'Select media file to open')
                if not file: return -1

                file = abspath(file)
                if os.path.isdir(file): return self.open_folder(file, focus_window=focus_window)
                if file == self.locked_video:               # if file is locked and we didn't cycle here, show a warning message
                    show_on_statusbar(f'File {file} is currently being worked on.')
                    return -1
            elif file == self.locked_video: return -1       # if file is locked and we're cycling, just return immediately

            # get stats and size of media
            start = get_time()
            stat = os.stat(file)
            filesize = stat.st_size
            basename = file[file.rfind(sep) + 1:]           # shorthand for os.path.basename NOTE: safe when `file` is provided automatically

        # --- Probing file and determining mime type ---
            # probe file with FFprobe if possible. if file has already been probed, reuse old probe. otherwise, save output to txt file
            # probing calls Popen through a Thread (faster than calling Popen itself or using Thread on a middle-ground function)
            probe_data = None
            if FFPROBE:                                     # generate probe file's path and check if it already exists
                probe_file = f'{constants.PROBE_DIR}{sep}{basename}_{stat.st_ctime}_{filesize}.txt'
                if exists(probe_file):                      # probe file already exists
                    try:
                        f = open(probe_file, 'r')
                        probe_data = json.load(f)
                        f.close()
                    except:
                        f.close()
                        try: os.remove(probe_file)
                        except: logging.warning('(!) FAILED TO DELETE POTENTIALLY INVALID PROBE FILE: ' + probe_file)
                        Thread(target=subprocess.Popen, args=(f'"{FFPROBE}" -show_format -show_streams -of json "{file}" > "{probe_file}"',), kwargs=dict(shell=True)).start()
                        logging.info('(?) Deleted potentially invalid probe file: ' + format_exc())
                else: Thread(target=subprocess.Popen, args=(f'"{FFPROBE}" -show_format -show_streams -of json "{file}" > "{probe_file}"',), kwargs=dict(shell=True)).start()
            else: probe_file = None                         # no FFprobe -> no probe file (even if one exists already)

            # get mime type of file (if called from cycle, then this part was worked out beforehand)
            if mime is None:
                try:
                    filetype_data = filetype.match(file)    # 'EXTENSION', 'MIME', 'extension', 'mime'
                    mime, extension = filetype_data.mime.split('/')
                    if mime not in ('video', 'image', 'audio'):
                        log_on_statusbar(f'File \'{file}\' appears to be corrupted or an invalid format and cannot be opened (invalid mime type).')
                        return -1
                except:
                    if not exists(file): log_on_statusbar(f'File \'{file}\' does not exist.')
                    else: log_on_statusbar(f'File \'{file}\' appears to be corrupted or an invalid format and cannot be opened (failed to determine mime type).')
                    logging.warning(format_exc())
                    return -1                               # ^^^ .match() errors out in rare circumstances ^^^

        # --- Restoring window ---
            # restore window from tray if hidden, otherwise there's a risk for unusual VLC output
            if not self.isVisible():                        # we need to do this even if focus_window is True
                was_minimzed_to_tray = True
                if self.isMaximized():
                    self.resize(self.last_window_size)      # restore size/pos or maximized windows will forget...
                    self.move(self.last_window_pos)         # ...their original geometry when you unmaximize them
                self.showMinimized()                        # minimize for now, we'll check if we need to focus later
            else: was_minimzed_to_tray = False

        # --- Playing media ---
            # attempt to play media
            player.stop()                                   # player must be stopped for images/gifs and to reduce delays on almost-finished media
            if mime == 'image': play_image(file, gif=extension == 'gif')
            elif not play(file): return -1                  # immediately attempt to play media once we know it might be valid
            else: play_image(None)                          # clear gifPlayer if vlc successfully played media

        # --- Parsing metadata and setting up UI/recent files list ---
            # parse non-video files and show/log file on statusbar
            parsed = False                                  # keep track of parse so we can avoid re-parsing it later if it ends up being a video
            if mime != 'video':                             # parse metadata early if it isn't a video
                if self.parse_media_file(file, probe_file, mime, extension, probe_data) == -1:
                    log_on_statusbar(f'File \'{file}\' appears to be corrupted or an invalid format and cannot be opened (non-video parsing failed).')
                    return -1
                parsed = True

            logging.info('--- OPENING FILE ---')
            log_on_statusbar(f'Opening file ({mime}/{extension}): {file}')

            # misc cleanup/setup for new media
            self.operations = {}
            self.sliderProgress.setEnabled(mime != 'image' or (extension == 'gif' and image_player.gif.frameCount() > 1))
            self.buttonTrimStart.setChecked(False)                                              # ^ static images/GIFs have odd but harmless behavior
            self.buttonTrimEnd.setChecked(False)

            # set basename (w/o extension) as default output text,
            # full basename as placeholder text, and update tooltip
            self.lineOutput.setText(splitext_media(basename)[0])
            self.lineOutput.setPlaceholderText(basename)
            self.lineOutput.setToolTip(f'{file}\n---\nEnter a new name and press enter to rename this file.')

            # update delete-action's QToolButton
            is_marked = file in self.marked_for_deletion
            self.actionMarkDeleted.setChecked(is_marked)
            self.buttonMarkDeleted.setChecked(is_marked)

            # reset cropped mode if needed
            if self.actionCrop.isChecked(): self.disable_crop_mode()                            # set_crop_mode auto-returns if mime_type is 'audio'

            # set size label for context menus and titlebar
            if filesize < 1048576:
                self.size_label = f'{filesize / 1024:.0f}kb'
            elif filesize < 1073741824:
                self.size_label = f'{filesize / 1048576:.2f}mb'
            else:
                self.size_label = f'{filesize / 1073741824:.2f}gb'

            # extra setup before we absolutely must wait for the media to finish parsing
            self.is_paused = False                  # force_pause could be used here, but it is slightly more efficient this way
            set_pause_button_text('𝗜𝗜')
            self.restarted = False
            #if not self.first_video_fully_loaded: self.set_volume(get_volume_slider())         # force volume to quickly correct gain issue
            self.lineOutput.clearFocus()            # clear focus from output line so it doesn't interfere with keyboard shortcuts
            self.current_file_is_autoplay = _from_autoplay

            # focus window. if disabled but window is minimized, check for special focus settings. ignore Autoplay focus if desired.
            if not self.isActiveWindow() and not (_from_cycle and settings.checkAutoplayIgnoreFocus.isChecked()):
                if not focus_window:
                    if self.isMinimized():
                        if was_minimzed_to_tray:    # check appropriate setting based on our original minimize state
                            if settings.checkFocusMinimizedToTray.isChecked(): focus_window = True
                        elif settings.checkFocusMinimized.isChecked(): focus_window = True
                if focus_window: qthelpers.showWindow(self)

            # if presumed to be a video -> finish VLC's parsing (done as late as possible to minimize downtime)
            if mime == 'video' and not parsed:
                if self.parse_media_file(file, probe_file, mime, extension, probe_data) == -1:  # parse metadata from VLC
                    log_on_statusbar(f'File \'{file}\' appears to be corrupted or an invalid format and cannot be opened (video parsing failed).')
                    return -1

                # update marquee size and offset relative to video's dimensions
                vlc = self.vlc
                set_marquee_int = player.video_set_marquee_int
                set_marquee_int(VideoMarqueeOption.Size, int(self.vheight * vlc.text_height_percent))
                set_marquee_int(VideoMarqueeOption.X, int(self.vheight * vlc.text_x_percent))
                set_marquee_int(VideoMarqueeOption.Y, int(self.vheight * vlc.text_y_percent))

            if not remember_old_file or not self.video_original_path: self.video_original_path = file

            # update recent media list
            if update_recent_list:
                recent_files = self.recent_files
                if file in recent_files:                                # move pre-existing recent file to front
                    recent_files.append(recent_files.pop(recent_files.index(file)))
                else:
                    recent_files.append(file)
                    max_len = settings.spinRecentFiles.value()
                    self.recent_files = recent_files[-max_len:]         # do NOT assign to the alias here

            # update UI with new media's duration
            h, m, s, ms = get_hms(self.duration)
            self.labelMaxTime.setText(f'{m:02}:{s:02}.{ms:02}' if self.duration < 3600 else f'{h}:{m:02}:{s:02}')
            self.spinHour.setEnabled(h != 0)                            # always leave spinSecond enabled
            self.spinMinute.setEnabled(m != 0)
            if self.width() <= 335: prefix = ''
            else: prefix = f'{self.frame_rate_rounded} FPS: '
            self.spinFrame.setPrefix(prefix)
            self.spinFrame.setMaximum(self.frame_count)
            self.spinFrame.setToolTip(str(self.frame_rate))

            # refresh title and log opening time
            refresh_title()
            logging.info(f'Initial media opening completed after {get_time() - start:.4f} seconds.')

        except: log_on_statusbar(f'(!) OPEN FAILED: {format_exc()}')


    def _open_slot(self):
        ''' NOTE: Not intended to be called manually. A slot for _open_signal which handles updating the progress slider's attributes.
            This is done here so that the progress bar updates in a uniform and quick manner as update_slider_thread must be used to
            reset the progress regardless, or we'll experience timing issues that cause newly opened media to play from the frame
            the previous media left off at. Putting ALL of open() in this slot, however, results in a noticable delay when opening
            media. Non-essential actions such as displaying a marquee are handled here as well. '''
        try:
            sliderProgress = self.sliderProgress

            sliderProgress.setMaximum(self.frame_count)
            update_progress(0)
            self.minimum = sliderProgress.minimum()
            self.maximum = sliderProgress.maximum()
            sliderProgress.setTickInterval(self.frame_rate_rounded * (1 if self.duration < 3600 else 60))       # place one tick per second/minute (default theme)
            sliderProgress.setPageStep(int(self.frame_count / 10))

            self.vsize.setWidth(self.vwidth)
            self.vsize.setHeight(self.vheight)
            if self.is_snap_mode_enabled():
                resize_on_open_state = settings.checkResizeOnOpen.checkState()
                snap_on_open_state = settings.checkSnapOnOpen.checkState()
                if resize_on_open_state and not (resize_on_open_state == 1 and self.first_video_fully_loaded):  # 1 -> only resize first video opened
                    self.snap_to_native_size()
                elif snap_on_open_state and not (snap_on_open_state == 1 and self.first_video_fully_loaded):
                    self.snap_to_player_size(force_instant_resize=True)
                elif settings.checkClampOnOpen.isChecked():
                    qthelpers.clampToScreen(self)       # clamping enabled but snap/resize is disabled
            elif settings.checkClampOnOpen.isChecked():
                qthelpers.clampToScreen(self)           # clamping enabled but snap/resize is disabled for this media

            # refresh title, reset cursor, show media title on screen, and set default subtitles
            #refresh_title()
            self.unsetCursor()                          # in some situations, a busy cursor might appear and get "stuck" TODO does this actually fix it?
            if settings.checkTextOnOpen.isChecked():    # certain combinations of autoplay + settings can override this marquee
                if not (settings.checkAutoplayHideMarquee.isChecked() and self.current_file_is_autoplay):
                    show_on_player(os.path.basename(self.video), 1000)
            if not settings.checkAutoEnableSubtitles.isChecked():
                player.video_set_spu(-1)

            self.first_video_fully_loaded = True
            image_player.gif.setPaused(False)

            logging.info(f'Metadata: duration={self.duration}, fps={self.frame_rate} ({self.frame_rate_rounded}), frames={self.frame_count}, size={self.vwidth}x{self.vheight}, ratio={self.ratio}, delay={self.delay:.6f}')
            logging.info('--- OPENING COMPLETE ---\n')
            gc.collect(generation=2)                    # do manual garbage collection after opening (NOTE: this MIGHT be risky)
        except: logging.error(f'(!) OPEN-SLOT FAILED: {format_exc()}')


    def restart(self):
        ''' Restarts media after it is finished playing to circumvent a strange design choice in libvlc which renders
            finished media unusable. While simple now, it took a LOT of experimentation, refactoring, and 5 iterations
            to reach this point. Called automatically as a callback through the MediaPlayerEndReached event <widgets.py>.
            If --play-and-exit is specified, program exits. '''
        try:
            logging.info('Restarting VLC media (Restart V)')

            # if we want to loop, reload video, reset UI, and return immediately
            if self.actionLoop.isChecked():
                play(self.video)
                # TODO just in case doing `set_and_update_progress` causes hitches or delays, we're...
                # ...doing an if-statement instead to ensure normal loops are slightly more seamless
                #return set_and_update_progress(self.minimum)           # <- simpler, possibly hitch-causing version
                if self.buttonTrimStart.isChecked(): return update_progress(0)
                else: return set_and_update_progress(self.minimum)

            # if we want autoplay/shuffle, don't reload -> switch immediately
            if self.actionAutoplay.isChecked():
                update_progress(0)                  # required due to the audio issue side-effect? (1st video file after audio file ends instantly)
                if self.actionAutoplayShuffle.isChecked(): return self.shuffle_media()
                if self.actionAutoplayDirectionDynamic.isChecked(): next = self.last_cycle_was_forward
                else: next = self.actionAutoplayDirectionForwards.isChecked()
                return self.cycle_media(next=next, update_recent_list=settings.checkAutoplayAddToRecents.isChecked(), autoplay=True)

            # if we want to stop, don't reload -> stop the player and return immediately
            if settings.checkStopOnFinish.isChecked() and player.get_state() != State.Stopped:
                return self.stop()

            play(self.video)                                            # reload video in VLC
            frame = self.frame_count
            set_player_position((frame - 2) / frame)                    # reset VLC player position (-2 frames to ensure visual update)
            emit_update_progress_signal(frame)                          # ensure UI snaps to final frame
            self.restarted = True

            if qtstart.args.play_and_exit:          # force-close if requested. this is done here so as to slightly optimize normal restarts
                logging.info('Play-and-exit requested. Closing.')
                return qtstart.exit(self)

            while player.get_state() == State.Ended: sleep(0.005)       # wait for VLC to update the player state
            self.force_pause(True, '⟳')                                 # forcibly re-pause VLC
            if self.isFullScreen() and settings.checkFullScreenMediaFinishedLock.isChecked():
                self.lock_fullscreen_ui = True      # show UI to indicate we've restarted in fullscreen (marquee doesn't work -> player is stopped)
                self.timer_fullscreen_media_ended = QtCore.QTimer(self, interval=500, timeout=self.timerFullScreenMediaEndedEvent)
                self.timer_fullscreen_media_ended.start()
            else: show_on_player('')                                    # VLC will auto-show last marq text everytime it restarts
            self.first_video_fully_loaded = True                        # ensure this is True (it resets depending on settings)
        except: logging.error(f'(!) RESTART FAILED: {format_exc()}')


    def pause(self):
        ''' Pauses/unpauses the media. Handles updating GUI, cleaning
            up/restarting, clamping progress to current trim, displaying
            the pause state on-screen, wrapping around the progress bar. '''
        will_pause = False

        # images/gifs
        if self.mime_type == 'image':
            if self.is_gif:                         # check if gif's filename is correct. if not, restart the gif and restore position
                old_state = image_player.gif.state()
                was_paused = old_state != QtGui.QMovie.Running          # V .fileName() is formatted wrong -> fix with `abspath`
                if was_paused and abspath(image_player.gif.fileName()) != image_player.filename:
                    image_player.gif.setFileName(image_player.filename)
                    set_gif_position(get_progess_slider())
                image_player.gif.setPaused(not was_paused)
                will_pause = not was_paused
                frame = image_player.gif.currentFrameNumber()
            else: return                                                # just return if it's a static image

        # videos/audio
        else:
            frame = get_progess_slider()
            old_state = player.get_state()
            if old_state == State.Stopped:
                self.restart()
                set_and_update_progress(frame)

            if frame >= self.maximum or frame <= self.minimum:          # play media from beginning if media is over
                self.lock_progress_updates = True
                set_and_update_progress(self.minimum)
                self.lock_progress_updates = False
            player.pause()                                              # actually pause VLC player
            will_pause = True if old_state == State.Playing else False  # prevents most types of pause-bugs...?

        # update pause button and titlebar
        pause_text = '▶' if will_pause else '𝗜𝗜'                        # ▷ ▶ ⏵︎
        set_pause_button_text(pause_text)
        if settings.checkTextOnPause.isChecked(): show_on_player(pause_text)
        refresh_title()

        self.is_paused = will_pause
        self.restarted = False
        logging.debug(f'Pausing: is_paused={will_pause} old_state={old_state} frame={frame} maxframe={self.maximum}')
        return will_pause


    def force_pause(self, paused: bool, text=None):
        if self.is_gif: image_player.gif.setPaused(paused)
        else: player.set_pause(paused)
        self.is_paused = paused
        set_pause_button_text(text if text is not None else '▶' if paused else '𝗜𝗜')
        refresh_title()
        logging.debug(f'Force-pause: paused={paused} text={text}')
        return self.is_paused


    def stop(self):
        ''' A more robust way of stopping - stop
            the player while also force-pausing. '''
        player.stop()
        image_player.gif.setFileName('')
        self.force_pause(True)


    def navigate(self, forward: bool, seconds_spinbox: QtW.QSpinBox):   # slightly longer than it could be, but cleaner/more readable
        ''' Navigates `forward` or backwards through the current media by the
            value specified in `seconds_spinbox`.

            NOTE: `seconds` has been replaced by `seconds_spinbox` since the
            former was never explicitly used. '''

        # cycle images with basic navigation keys
        if self.is_static_image: return self.cycle_media(next=forward)

        # HACK: "replay" audio file to correct VLC's pitch-shifting bug
        # https://reddit.com/r/VLC/comments/i4m0by/pitch_changing_on_seek_only_some_audio_file_types/
        # https://reddit.com/r/VLC/comments/b0i9ff/music_seems_to_pitch_shift_all_over_the_place/
        if self.mime_type == 'audio' and not self.is_paused:
            self.skip_next_vlc_progress_desync_check = True
            play(self.video)

        old_frame = get_progess_slider()
        seconds = seconds_spinbox.value()

        # calculate and update to new frame as long as it's within our bounds
        if forward:                                 # media will wrap around cleanly if it goes below 0/above max frames
            if old_frame == self.frame_count and settings.checkNavigationWrap.isChecked(): new_frame = 0
            #else: new_frame = min(self.frame_count, old_frame + self.frame_rate_rounded * seconds)
            else: new_frame = min(self.maximum, old_frame + self.frame_rate_rounded * seconds)
        else:   # TODO use "<= 1" as workaround for bug that causes media sometimes to play 1 frame when wrapping?
            #if old_frame <= 1 and settings.checkNavigationWrap.isChecked(): new_frame = self.frame_count
            if old_frame == 0 and settings.checkNavigationWrap.isChecked(): new_frame = self.frame_count
            #else: new_frame = max(0, old_frame - self.frame_rate_rounded * seconds)
            else: new_frame = max(self.minimum, old_frame - self.frame_rate_rounded * seconds)

        # set progress to new frame
        #self.frame_override = new_frame            # ensure VLC progress doesn't override our navigation TODO is this needed?
        set_and_update_progress(new_frame)

        # auto-unpause after restart and show current position as a marquee, if desired
        if self.restarted and settings.checkNavigationUnpause.isChecked(): self.force_pause(False)
        if self.isFullScreen() and settings.checkTextOnFullScreenPosition.isChecked():
            h, m, s, _ = get_hms(self.current_time)
            current_text = f'{m:02}:{s:02}' if self.current_time < 3600 else f'{h}:{m:02}:{s:02}'
            max_text = self.labelMaxTime.text()[:-3] if self.duration < 3600 else self.labelMaxTime.text()
            show_on_player(f'{current_text}/{max_text}')
        logging.debug(f'Navigated {"forwards" if forward else "backwards"} {seconds} second(s), going from frame {old_frame} to {new_frame}')


    def rename(self, new_name: str = None):
        ''' Renames the current media to `new_name`. If `new_name` is blank,
            self.lineOutput is used. See `get_renamed_output` for details. '''
        old_name = self.video
        new_name, basename_no_ext, ext = self.get_renamed_output(new_name)
        if new_name is None: return                 # `get_renamed_output` failed to create a valid output path
        was_paused = self.is_paused
        self.stop()                                 # player must be stopped before we can rename
        try:
            try:
                os.renames(old_name, new_name)
                marquee(f'File renamed to {new_name}', 2500, marq_key='Save')
            except FileNotFoundError:               # images/gifs are cached so they can be altered behind the scenes
                if self.mime_type == 'image' and settings.checkRenameMissingImages.isChecked():
                    image_player.art.save(new_name)
                    log_on_statusbar(f'Original file no longer exists, so a copy was created at {new_name}.')
                else: return log_on_statusbar(f'Current file no longer exists at {old_name}.')
            except PermissionError:
                return log_on_statusbar(f'(!) Permission error while renaming: file is in use by another program ({old_name}).')
            except OSError as error:                # show specific message for OSError 17
                if 'disk drive' in str(error): return log_on_statusbar('Renaming across drives is not supported yet.')
                return log_on_statusbar(f'(!) OSError while renaming: {format_exc()}')
            except:
                return log_on_statusbar(f'(!) Failed to rename: {format_exc()}')

            # set output textbox to extension-less basename (same as in open())
            self.lineOutput.setText(basename_no_ext)
            self.lineOutput.setPlaceholderText(basename_no_ext + ext)
            self.lineOutput.setToolTip(f'{new_name}\n---\nEnter a new name and press enter to rename this file.')
            self.lineOutput.clearFocus()                            # clear focus so we can navigate/use hotkeys again

            self.video = new_name
            refresh_title()                                         # update titlebar
        except: log_on_statusbar(f'RENAME FAILED: {format_exc()}')

        # replay the media, then restore position and pause state (no need for full-scale open())
        frame = get_progess_slider()
        if self.is_gif:                                             # gifs
            image_player.gif.setFileName(new_name)                  # don't need to play new path - just update filename
            set_gif_position(frame)
            if not was_paused: self.force_pause_signal.emit(False)  # unpause gif if it wasn't paused before
            image_player.filename = new_name
        elif self.mime_type != 'image':                             # video/audio (static images don't need extra cleanup)
            play(self.video)                                        # use self.video in case the rename failed
            self.force_pause_signal.emit(was_paused)                # rename can be called from a thread -> use signal
            if not was_paused: self.frame_override = frame          # progress thread might get confused and reset to 0
            set_player_position(frame / self.frame_count)

        # update recent files's list with new name, if possible
        # NOTE: this is done after playing in case the recent files list is very large
        try:
            recent_files = self.recent_files
            index = recent_files.index(old_name)
            recent_files[index] = self.video                        # don't use `new_name` here in case we failed to rename
        except: pass


    def delete(self, files=None, cycle: bool = True):
        ''' Deletes (or recycles) a list of `files`. If `files` is a string,
            it becomes a single-length tuple. If `files` is None, `self.video`
            is used. If `self.video` is within `files`, all players are stopped,
            and the media is cycled if possible before deleting. '''
        if not files: files = (self.video,)
        elif isinstance(files, str): files = (files,)
        if self.video in files:
            if not cycle:
                self.stop()
            else:                                   # cycle media before deleting if current video is about to be deleted
                if self.is_gif: self.stop()         # image_player's QMovie must have its filename changed to unlock it
                old_file = self.video               # self.video will likely change after media is cycled
                new_file = self.cycle_media(next=self.last_cycle_was_forward, ignore=files)
                if new_file is None or new_file == old_file:
                    self.stop()                     # media wasn't cycled -> stop player and uncheck deletion button
                    self.actionMarkDeleted.setChecked(False)
                    self.buttonMarkDeleted.setChecked(False)
                    log_on_statusbar('There are no remaining files to play.')

        recycle = settings.checkRecycleBin.isChecked()
        verb = 'recycl' if recycle else 'delet'     # we're appending "ing" to these words
        if recycle: import send2trash
        logging.info(f'{verb.capitalize()}ing {len(files)} files...')

        for file in files:
            try:
                send2trash.send2trash(file) if recycle else os.remove(file)
                logging.info(f'File {file} {verb}ed successfully.')
            except Exception as error: log_on_statusbar(f'File could not be deleted: {file} - {error}')
            if not exists(file):                    # if file doesn't exist, unmark file (even if error occurred)
                if file in self.recent_files: self.recent_files.remove(file)
                if file in self.marked_for_deletion: self.marked_for_deletion.remove(file)


    def snapshot(self, *args, mode: str = 'quick', is_temp: bool = False):  # *args to capture unused signal args
        ''' Snapshot modes:
                'full' - Open a resizing dialog and save dialog
                'quick' - Take and save snapshot immediately using predefined settings
                'open'  - Open last snapshot within PyPlayer
                'view'  - Open last snapshot within user's default program (which might be PyPlayer)
                'undo'  - Delete the last snapshot

            libvlc_video_take_snapshot's docstring:
            "Take a snapshot of the current video window. If `i_width` AND `i_height` is 0, original
            size is used. If `i_width` XOR `i_height` is 0, original aspect-ratio is preserved."
            Returns: 0 on success, -1 if the video was not found.
            Parameters:
                `p_mi` - media player instance.
                `num` - number of video output (typically 0 for the first/only one).
                `psz_filepath` - the path of a file or a folder to save the snapshot into.
                `i_width` - the snapshot's width.
                `i_height` - the snapshot's height. '''
        frame = get_progess_slider()    # immediately get frame, regardless of whether we need it or not

        mime = self.mime_type
        video = self.video
        must_pause = settings.checkSnapshotPause.isChecked() or mode == 'full'
        if must_pause and not self.is_paused:
            if self.is_gif: image_player.gif.setPaused(True)
            else: player.set_pause(True)

        try:
            # handle `mode`
            if self.is_static_image and mode == 'quick' and not self.actionCrop.isChecked():
                mode = 'full'                                               # change quick-snapshots to full-snapshots for uncropped images

        # >>> open last snapshot (not in explorer) <<<
            if mode == 'open' or mode == 'view':
                if not cfg.last_snapshot_path: return show_on_statusbar('No snapshots have been taken yet.', 10000)
                if not exists(cfg.last_snapshot_path): return log_on_statusbar(f'Previous snapshot at {cfg.last_snapshot_path} no longer exists.')
                if mode == 'open': self.open(cfg.last_snapshot_path)        # open in pyplayer
                else: qthelpers.openPath(cfg.last_snapshot_path)            # open in default program
                return log_on_statusbar(f'Opening last snapshot at {cfg.last_snapshot_path}.')

        # >>> undo last snapshot (by deleting it) <<<
            elif mode == 'undo':
                if not cfg.last_snapshot_path: return show_on_statusbar('No snapshots have been taken yet.', 10000)
                if not exists(cfg.last_snapshot_path): return log_on_statusbar(f'Previous snapshot at {cfg.last_snapshot_path} no longer exists.')
                try:
                    os.remove(cfg.last_snapshot_path)
                    return log_on_statusbar(f'Deleted last snapshot at {cfg.last_snapshot_path}.')
                except: return log_on_statusbar(f'(!) Failed to delete last snapshot at "{cfg.last_snapshot_path}": {format_exc()}')

            elif not video: return show_on_statusbar('No media is playing.', 10000)
            elif mime == 'audio' and not image_player.pixmap(): return show_on_statusbar('You can only snapshot audio with cover art.', 10000)

        # >>> take new snapshot <<<
            is_gif = self.is_gif
            is_art = mime == 'audio'                            # if it's audio, we already know that it has cover art
            frame_count_str = str(self.frame_count)
            if mime == 'image' and settings.checkSnapshotGifPNG.isChecked(): format = 'PNG'
            else: format = settings.comboSnapshotFormat.currentText()

            # NOTE: art and gif snapshots use the default name format's placeholder text
            if is_art:
                frame = 1
                frame_count_str = '1'
                name_format = settings.lineSnapshotArtFormat.text().strip() or settings.lineSnapshotNameFormat.placeholderText()
            elif is_gif: name_format = settings.lineSnapshotGifFormat.text().strip() or settings.lineSnapshotNameFormat.placeholderText()
            else: name_format = settings.lineSnapshotNameFormat.text().strip() or settings.lineSnapshotNameFormat.placeholderText()

            video_basename_no_ext = splitext_media(os.path.basename(video), strict=False)[0]
            date_format = settings.lineSnapshotDateFormat.text().strip() or settings.lineSnapshotDateFormat.placeholderText()
            default_name = name_format.replace('?name', video_basename_no_ext) \
                                      .replace('?date', strftime(date_format, localtime())) \
                                      .replace('?framecount', frame_count_str) \
                                      .replace('?frame', str(frame).zfill(len(frame_count_str)))

            # get width, height, and jpeg quality of snapshot
            if mode == 'full':
                width, height, quality = self.show_size_dialog(snapshot=True)
                if width is None: return                        # dialog canceled (finally-statement ensures we unpause if needed)
            else:
                width = 0
                height = 0
                quality = settings.spinSnapshotJpegQuality.value()

            # check if we should convert to a jpeg when we're done. if not, change format to PNG
            use_jpeg = (not is_temp or (mode == 'full' and quality < 100)) and format[:4] == 'JPEG' and mime == 'video'
            if not use_jpeg: format = 'PNG'

            # generate output path for snapshot
            if is_temp:                                         # generate temporary path
                path = abspath(
                    get_unique_path(
                        f'{constants.TEMP_DIR}{sep}{default_name}.{"jpg" if format == "JPEG" else "png"}',
                        start=1,
                        key='?count',
                        strict=True
                    )
                )
            elif mode == 'quick':                               # generate pre-determined path
                dirname = os.path.expandvars(settings.lineDefaultSnapshotPath.text().strip() or os.path.dirname(default_name))
                try: os.makedirs(dirname)
                except FileExistsError: pass
                path = abspath(
                    get_unique_path(
                        os.path.join(dirname, default_name) + ('.jpg' if format == 'JPEG' else '.png'),
                        start=1,
                        key='?count',
                        strict=True
                    )
                )
            else:                                               # open save-file dialog
                use_snapshot_lastdir = settings.checkSnapshotRemember.isChecked()
                selected_filter = 'JPEG (*.jpg; *.jpeg; *.jpe; *.jfif; *.exif)' if format == 'JPEG' else ''
                base_path = os.path.join(cfg.last_snapshot_folder if use_snapshot_lastdir else cfg.lastdir, default_name)
                path = f'{base_path}{".png" if not selected_filter else ".jpg"}'
                path, format, lastdir = qthelpers.saveFile(lastdir=get_unique_path(path, key='?count', zeros=1, strict=True),
                                                            caption='Save snapshot as',
                                                            filter='PNG (*.png);;JPEG (*.jpg; *.jpeg; *.jpe; *.jfif; *.exif);;All files (*)',
                                                            selectedFilter=selected_filter,
                                                            returnFilter=True)
                if use_snapshot_lastdir: cfg.last_snapshot_folder = lastdir
                else: cfg.lastdir = lastdir
                if path is None: return
                path = abspath(path)
                # 'BMP (*.bmp; *.dib, *.rle);;TIFF (*.tiff; *.tif);;GIF (*.gif);;TGA (*.tga);;WebP (*.webp)'

            logging.info(f'psz_filepath={path}, i_width={width}, i_height={height}, quality={quality}')

            # take and save snapshot
            if is_gif:
                if width or height:                             # use "scale" ffmpeg filter for gifs
                    w = width if width else -1                  # -1 uses aspect ratio in ffmpeg (as opposed to 0 in VLC)
                    h = height if height else -1
                    ffmpeg(f'-i "{self.video}" -vf "select=\'eq(n\\,{frame})\', scale={w}:{h}" -vsync 0 "{path}"')
                else: ffmpeg(f'-i "{self.video}" -vf select=\'eq(n\\,{frame})\' -vsync 0 "{path}"')
            elif mime == 'video':
                player.video_take_snapshot(num=0, psz_filepath=path, i_width=width, i_height=height)
            else:
                if width or height:
                    w = width if width else height * (self.vwidth / self.vheight)
                    h = height if height else width * (self.vheight / self.vwidth)
                    image_player.art.scaled(w, h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation).save(path, quality=quality)
                else: image_player.art.save(path, quality=quality)

            # update config and log progress if it's not a temporary snapshot
            if not is_temp:
                cfg.last_snapshot_path = path
                cfg.last_snapshot_folder = os.path.dirname(path)
                log_on_statusbar(f'{"Cover art" if is_art else "GIF frame" if is_gif else "Snapshot"} saved to {path}')

            # crop final snapshot if desired, taking into account the custom width/height
            if self.actionCrop.isChecked():
                logging.info('Cropping previously saved snapshot...')

                # wait up to 1 second for snapshot file to be generated
                seconds_until_timeout = 1.0
                while not exists(path) and seconds_until_timeout > 0:
                    seconds_until_timeout -= 0.05
                    sleep(0.05)
                if seconds_until_timeout <= 0:
                    log_on_statusbar(f'(!) NORMAL/CUSTOM SNAPSHOT FAILED: No output file appeared after 1 second at {path}.')
                    return

                with get_PIL_Image().open(path) as image:
                    # calculate factors between media's native resolution and actual desired snapshot resolution
                    if width or height:                         # custom width and/or height is set
                        if width:
                            x_factor = self.vwidth / width
                            if not height: y_factor = x_factor  # width is set but height isn't -> match factors
                        if height:
                            y_factor = self.vheight / height
                            if not width: x_factor = y_factor   # height is set but width isn't -> match factors
                    else:                                       # neither is set -> use 1 to avoid division by 0
                        x_factor = 1
                        y_factor = 1

                    # use factors to crop snapshot relative to the snapshot's actual resolution for an accurate crop
                    lfp = self.vlc.last_factored_points
                    image = image.crop((round(lfp[0].x() / x_factor), round(lfp[0].y() / y_factor),   # left/top/right/bottom (crop takes a tuple)
                                        round(lfp[3].x() / x_factor), round(lfp[3].y() / y_factor)))  # round QPointFs

                    # VLC doesn't actually support jpeg snapshots -> convert manually
                    # https://www.geeksforgeeks.org/convert-png-to-jpg-using-python/
                    if use_jpeg: self.convert_snapshot_to_jpeg(path, image, quality)
                    else: image.save(path)
            elif use_jpeg: self.convert_snapshot_to_jpeg(path, quality=quality)

            # return snapshot path
            return path

        except: log_on_statusbar(f'(!) SNAPSHOT FAILED: {format_exc()}')
        finally:                                                    # restore pause-state before leaving
            if self.is_gif: image_player.gif.setPaused(self.is_paused)
            else: player.set_pause(self.is_paused)                  # NOTE: DON'T do both - QMovie will emit a "frameChanged" signal!!!


    def save_as(
        self,
        *args,
        noun='media',
        filter='MP4 files (*.mp4);;MP3 files (*.mp3);;WAV files (*.wav);;AAC files (*.aac);;All files (*)',
        valid_extensions=constants.ALL_MEDIA_EXTENSIONS,
        ext_hint=None,
        default_path=None,
        unique_default=True
    ):
        ''' Opens a file dialog with `filter` and the caption "Save `noun`
            as...", before saving to the user-selected path, if any.
            See `save()` for more details. '''
        video = self.video
        if not video: return show_on_statusbar('No media is playing.', 10000)

        try:
            if default_path is None:
                base, ext = splitext_media(video, valid_extensions)
                if ext: default_path = video
                else: default_path = base + ext_hint

            logging.info('Opening \'Save As...\' dialog.')
            file = self.browse_for_save_file(
                noun=noun,
                filter=filter,
                default_path=default_path,
                unique_default=unique_default
            )

            if file is None: return
            logging.info(f'Saving as \'{file}\'')
            self.save(dest=file)
        except: log_on_statusbar(f'(!) SAVE_AS FAILED: {format_exc()}')


    def save(
        self,
        *args,                                                                  # *args to capture unused signal args
        dest=None,
        ext_hint=None,
        noun='media',
        filter='MP4 files (*.mp4);;MP3 files (*.mp3);;WAV files (*.wav);;AAC files (*.aac);;All files (*)',
        valid_extensions=constants.ALL_MEDIA_EXTENSIONS,
        preferred_extensions=None
    ):
        ''' Checks for any edit operations, applies them to the current media,
            and saves the new file to `dest`. If `dest` is None, `save_as()`
            is called, passing in `filter`, and a list of `valid_extensions`.
            If `preferred_extensions` is specified, `save_as()` will default
            to an extension from this list if possible, even if the current
            extension is already valid. If `dest` has no extension, `ext_hint`
            will be used. If `ext_hint` is None, PyPlayer will guess the
            extension. NOTE: Saving occurs in a separate thread. '''

        video = self.video
        if not video: return show_on_statusbar('No media is playing.', 10000)

        operations = self.operations.copy()
        if self.actionCrop.isChecked(): operations['crop'] = True
        if self.buttonTrimStart.isChecked(): operations['trim start'] = True
        if self.buttonTrimEnd.isChecked(): operations['trim end'] = True

        old_base, old_ext = splitext_media(video)
        if not old_ext: old_ext = '.' + self.extension
        ext = ''

        # see if we haven't sufficiently edited the destination (no abspath specified, same basename (excluding the extension))
        if not dest: dest_was_not_modified = True                               # TODO i don't think this code actually matters anymore
        else:
            old_tail_base = os.path.split(old_base)[-1]
            new_base, new_ext = splitext_media(dest)
            dest_was_not_modified = old_tail_base == new_base

        # get output name
        if dest_was_not_modified:
            output_text, _, ext = self.get_renamed_output(valid_extensions=valid_extensions)
            if not output_text or output_text == video:                         # no name OR name is same as original video
                if settings.checkAlwaysSaveAs.isChecked():
                    return self.save_as(
                        noun=noun,
                        filter=filter,
                        valid_extensions=preferred_extensions or valid_extensions,
                        ext_hint=ext_hint or old_ext,                           # ^ pass preferred extensions if provided
                        unique_default=False
                    )
                elif operations:
                    dest = add_path_suffix(video, '_edited', unique=True)
            else:
                dest = output_text
                if not os.path.dirname(dest):                                   # output text is just a name w/ no directory
                    default_dir = settings.lineDefaultOutputPath.text().strip()
                    if not default_dir: default_dir = os.path.dirname(video)    # if no default path, use source video's path
                    dest = abspath(os.path.expandvars(os.path.join(default_dir, dest)))
                if not splitext_media(dest, valid_extensions)[-1]:              # append extension if needed
                    ext = ext_hint or old_ext
                    dest += ext                             # use extension hint if specified, otherwise just use source file's extension
            dirname, basename = os.path.split(dest)         # sanitize our custom destination (`sanitize` does not account for full paths)
            dest = os.path.join(dirname, sanitize(basename))

        # ensure output has valid extension included
        if not ext:
            if not splitext_media(dest, valid_extensions)[-1]:
                dest += ext_hint or old_ext
        logging.info(f'Destination extension is "{ext}"')

        # clean up destination one more time, just in case
        dest = abspath(dest)

        # no operations -> check if video was renamed and return without starting a new thread
        if not operations:
            if dest != video:                               # no operations, but name is changed
                logging.info(f'No operations detected, but a new name was specified. Renaming to {dest}')
                return self.rename(dest)                    # do a normal rename and return
            return marquee('No changes have been made.', log=False)

        # do actual saving in separate thread
        Thread(target=self._save, args=(dest, operations), daemon=True).start()


    def _save(self, dest: str = None, operations: dict = {}):
        ''' Do not call this directly. Use `save()` instead. Iteration: V '''
        start_time = get_time()

        # save copies of all critical properties that could potentially change while we're saving
        video = self.video.strip()
        mime = self.mime_type
        extension = self.extension
        is_gif = self.is_gif
        is_static_image = self.is_static_image
        minimum, maximum, frame_count, frame_rate, duration = self.minimum, self.maximum, self.frame_count, self.frame_rate, self.duration
        vwidth, vheight = self.vwidth, self.vheight

        audio_tracks = player.audio_get_track_count()

        replacing_original = dest == video                              # whether or not our new video has same name as original
        delete_after_save = self.checkDeleteOriginal.checkState()       # what will we do to the media file after saving? (0, 1, or 2)
        NO_DELETE =   0                                                 # checkState() values for delete_after_save
        MARK_DELETE = 1
        FULL_DELETE = 2

        op_replace_audio = operations.get('replace audio', None)        # path to audio track
        op_add_audio =     operations.get('add audio', None)            # path to audio track
        op_remove_track =  operations.get('remove track', None)         # track to remove
        op_amplify_audio = operations.get('amplify audio', None)        # new volume, from 0-1(+)
        op_resize =        operations.get('resize', None)
        op_rotate_video =  operations.get('rotate video', None)         # rotate angle -> 90/180/270
        op_trim_start =    operations.get('trim start', None)           # represents both trimming and fading
        op_trim_end =      operations.get('trim end', None)             # represents both trimming and fading
        op_crop =          operations.get('crop', None)

        # quick pre-operation checks
        if op_crop:
            if mime == 'audio':                                         # NOTE: this shouldn't be possible, but just in case
                log_on_statusbar('Crop mode on audio files is designed for cropping cover art.')
                del operations['crop']                                  # remove operation key
                op_crop = False
            crop_selection = tuple(self.vlc.factor_point(point) for point in self.vlc.selection)
            lfp = tuple(self.vlc.last_factored_points)
            crop_top =    min(crop_selection[0].y(), vheight - 1)
            crop_left =   min(crop_selection[0].x(), vwidth - 1)
            crop_right =  min(crop_selection[1].x(), vwidth)
            crop_bottom = min(crop_selection[2].y(), vheight)
            crop_width =  round(crop_right - crop_left)
            crop_height = round(crop_bottom - crop_top)
            if crop_width == vwidth and crop_height == vheight:         # not actually cropped -> disable crop mode and update our operations
                log_on_statusbar('Crop is the same size as the source media.')
                self.disable_crop_mode_signal.emit(False)               # False to make sure we don't log crop mode being disabled
                del operations['crop']                                  # remove operation key
                op_crop = False
        if op_trim_start or op_trim_end:
            if minimum == 0 and maximum == frame_count:
                log_on_statusbar('It\'s not really a "trim" if your trim is the entire duration of the file, is it?')
                del operations['trim start']                            # remove operation keys
                del operations['trim end']
                op_trim_start = False
                op_trim_end = False
            if is_static_image:                                         # NOTE: shouldn't be possible, but just in case
                log_on_statusbar('I don\'t know how you got this far, but you can\'t trim/fade a static image.')
                del operations['trim start']                            # remove operation keys
                del operations['trim end']
                op_trim_start = False
                op_trim_end = False

        # check if we still have work to do after the above checks
        if not operations: return logging.info('(?) Pre-operation checks failed, nothing left to do.')

        # ffmpeg is required after this point, so check that it's actually present, and because...
        # ...we're in a thread, we skip the warning and display it separately through a signal
        if not constants.verify_ffmpeg(self, warning=False, force_warning=False):
            self.show_ffmpeg_warning_signal.emit(self)
            return marquee('You don\'t have FFmpeg installed!')

        # log data and create some strings for temporary paths we'll be needing
        logging.info(f'Saving file to "{dest}"')
        intermediate_file = video   # the path to the file that will be receiving all changes between operations
        final_dest = dest           # save the original dest so we can rename our temporary dest back later
        dest = add_path_suffix(dest, '_temp', unique=True)              # add _temp to dest, in case dest is the same as our base video
        temp_paths = []
        logging.debug(f'temp-dest={dest}, video={video} delete_after_save={delete_after_save} operations={operations}')

        # stop player if we've reached this point. it's our last chance to do so safely (without theoretically disrupting the user)
        self.stop()

        # lock video from being played if we're replacing it OR it's being immediately deleted
        if replacing_original or delete_after_save == FULL_DELETE:
            self.locked_video = video
            logging.info(f'Video locked during edits: {video}')

            # ignore deletion setting if we're replacing the original file
            if replacing_original: delete_after_save = NO_DELETE

        # display indeterminant progress bar, set busy cursor, and update UI to frame 0
        self.set_save_progress_max_signal.emit(frame_count)             # set progress bar max to max possible frames
        self.setCursor(Qt.BusyCursor)
        emit_update_progress_signal(0)

    # --- Apply operations to media ---
        # NOTE: ABSOLUTELY EXTREMELY IMPORTANT!!! update any relevant properties such as...
        # ...vheight/vwidth, is_gif/is_static_image, etc. as SOON as an operation is done!!!
        # TODO: GIFs should probably use Pillow for their operations
        try:
            # static images are cached and can be deleted independant of pyplayer
            # if this happens, take the cached QPixmap and save it to a temporary file
            # we'll assume the user wants the original image to stay gone, so we'll delete the temporary file later
            if is_static_image and not exists(video):
                temp_image_path = add_path_suffix(video, '_tempimage', unique=True)
                temp_paths.append(temp_image_path)
                intermediate_file = temp_image_path
                with get_PIL_Image().fromqpixmap(image_player.art) as image:
                    image.save(temp_image_path)

            # trimming and fading (controlled using the same start/end points)
            # TODO: there are scenarios where cropping and/or resizing first is better
            #       - how should we handle reordering operations?
            if op_trim_start or op_trim_end:

                # trim -> https://trac.ffmpeg.org/wiki/Seeking TODO: -vf trim filter should be used in here
                if self.is_trim_mode():
                    self.set_save_progress_max_signal.emit(maximum - minimum)       # set progress bar to actual number of frames in final trim
                    trim_duration = (maximum - minimum) / frame_rate

                    cmd = '-i %in '
                    if minimum > 0:           cmd += f'-ss {minimum / frame_rate} '
                    if maximum < frame_count: cmd += f'-to {maximum / frame_rate} '

                    if is_gif:
                        log_on_statusbar('GIF trim requested.')
                        precise = False
                    else:
                        # see if we should use auto-precise mode regardless of user's preference
                        # (always use precise trimming for very short media or short clips on semi-short media)
                        if duration <= 10 or (duration <= 30 and trim_duration <= 5):
                            log_on_statusbar('Precise trim auto-detected (short trims on short media always use precise trimming).')
                            precise = True

                        # don't use auto-precise mode. either use preferred mode or show dialog for user to pick mode
                        else:
                            if self.actionTrimPickEveryTime.isChecked() or not cfg.trimmodeselected:
                                self.trim_mode_selection_canceled = False
                                cfg.trimmodeselected = False
                                self.show_trim_dialog_signal.emit()
                                while not cfg.trimmodeselected: sleep(0.2)
                                if self.trim_mode_selection_canceled:               # user hit X on the trim dialog
                                    return log_on_statusbar('Trim canceled.')

                            start_time = get_time()                                 # reset start_time to undo time spent waiting for dialog
                            precise = self.trim_mode_action_group.checkedAction() is self.actionTrimPrecise or self.extension in constants.SPECIAL_TRIM_EXTENSIONS
                            log_on_statusbar(f'{"Precise" if precise else "Imprecise"} trim requested{" (this is a time-consuming task)" if precise else ""}.')

                        cmd += ' -c:v ' + ('libx264 -c:a aac' if precise else 'copy -c:a copy -avoid_negative_ts make_zero -async 1')
                        #else: cmd_parameters = ' -c:v copy -c:a copy -avoid_negative_ts make_zero -af \'aresample=async=1\''
                        #cmd_parameters = f' -c:v {"libx264" if precise else "copy"} -c:a {"aac" if precise else "copy -avoid_negative_ts make_zero"} '

                    if not precise: intermediate_file = self.ffmpeg(intermediate_file, cmd, dest)
                    else: intermediate_file = self.ffmpeg(intermediate_file, cmd, dest, start_text='Seeking to start of trim...')
                    duration = trim_duration                                        # update duration
                    frame_count = maximum - minimum                                 # update frame count

                # fade (using trim buttons as fade points) -> https://dev.to/dak425/add-fade-in-and-fade-out-effects-with-ffmpeg-2bj7
                else:
                    log_on_statusbar('Fade requested (this is a time-consuming task).')     # TODO: ffmpeg fading is actually very versatile, this could be WAY more sophisticated
                    mode = {self.actionFadeBoth: 'both', self.actionFadeVideo: 'video', self.actionFadeAudio: 'audio'}[self.trim_mode_action_group.checkedAction()]
                    fade_cmd_parts = []
                    if mode == 'video' or mode == 'both':
                        fade_parts = []
                        if minimum > 0:
                            seconds = minimum / frame_rate
                            fade_parts.append(f'fade=t=in:st=0:d={seconds}')        # d defaults to ~1 second
                        if maximum < frame_count:
                            seconds = maximum / frame_rate
                            delta = duration - seconds - 0.1                        # TODO: 0.1 offset since sometimes fade out doesn't finish on time
                            fade_parts.append(f'fade=t=out:st={seconds}:d={delta}')
                        if fade_parts: fade_cmd_parts.append(f'-vf "{",".join(fade_parts)}{" -c:a copy" if mode != "both" else ""}"')
                    if mode == 'audio' or mode == 'both':
                        fade_parts = []
                        if minimum > 0:
                            seconds = minimum / frame_rate
                            fade_parts.append(f'afade=t=in:st=0:d={seconds}')       # d defaults to ~1 second
                        if maximum < frame_count:
                            seconds = maximum / frame_rate
                            delta = duration - seconds - 0.1                        # TODO: ditto. make sure these work
                            fade_parts.append(f'afade=t=out:st={seconds}:d={delta}')
                        if fade_parts: fade_cmd_parts.append(f'-af "{",".join(fade_parts)}{" -c:v copy" if mode != "both" and mime == "video" else ""}"')
                    if fade_cmd_parts: intermediate_file = self.ffmpeg(intermediate_file, f'-i %in {" ".join(fade_cmd_parts)}', dest)

            # crop -> https://video.stackexchange.com/questions/4563/how-can-i-crop-a-video-with-ffmpeg
            if op_crop:     # ffmpeg cropping is not 100% accurate, final dimensions may be off by ~1 pixel
                log_on_statusbar('Cropping...')                                     # -filter:v "crop=out_w:out_h:x:y"
                cmd = f'-i %in -filter:v "crop={crop_width}:{crop_height}:{round(crop_left)}:{round(crop_top)}"'
                if is_static_image:
                    with get_image_data(intermediate_file, extension) as image:
                        image = image.crop((round(lfp[0].x()), round(lfp[0].y()),   # left/top/right/bottom (crop takes a tuple)
                                            round(lfp[3].x()), round(lfp[3].y())))  # round QPointFs
                        image.save(dest, format=extension)                          # specify `format` in case `dest`'s extension is unexpected
                    intermediate_file = dest
                else:
                    intermediate_file = self.ffmpeg(
                        infile=intermediate_file,
                        cmd=f'-i %in -filter:v "crop={crop_width}:{crop_height}:{round(crop_left)}:{round(crop_top)}"',
                        outfile=dest
                    )
                vwidth = round(crop_width) - 1                                      # update dimensions
                vheight = round(crop_height) - 1

            # resize video/GIF/image, or change audio file's tempo
            # TODO: this is a relatively fast operation and SHOULD be done much sooner but that requires...
            # ...dynamic ordering of operations (see above) and adjusting `crop_selection`/`lfp` and I'm lazy
            if op_resize is not None:       # audio -> https://stackoverflow.com/questions/25635941/ffmpeg-modify-audio-length-size-stretch-or-shrink
                log_note = ' (this is a time-consuming task)' if mime == 'video' else ' (Note: this should be a VERY quick operation)' if mime == 'audio' else ''
                log_on_statusbar(f'{mime.capitalize()} resize requested{log_note}.')
                width, height = op_resize   # for audio, width is the percentage and height is None
                if mime == 'audio':
                    intermediate_file = self.ffmpeg(intermediate_file, f'-i %in -filter:a atempo="{width}"', dest)
                else:   # Pillow can't handle 0/-1 as a dimension -> scale right away
                    vwidth, vheight = scale(vwidth, vheight, width, height)         # update dimensions
                    if is_static_image:
                        with get_image_data(intermediate_file, extension) as image:
                            image = image.resize((vwidth, vheight))                 # resize image
                            image.save(dest, format=extension)
                    else:
                        # ffmpeg cannot resize to dimensions that aren't divisible by 2 (for some reason)
                        # using -1 will STILL error out if the dimensions IT CHOOSES aren't divisible by 2
                        # this can technically be fixed using -2 (https://stackoverflow.com/a/72589591)...
                        # ...but we need to scale the dimensions ourselves anyways so it doesn't matter
                        vwidth -= int(vwidth % 2 != 0)
                        vheight -= int(vheight % 2 != 0)
                        intermediate_file = self.ffmpeg(
                            infile=intermediate_file,
                            cmd=f'-i %in -vf "scale={vwidth}:{vheight}" -crf 28 -c:a copy',
                            outfile=dest
                        )

            # rotate video/GIF/image
            # TODO: this should use Pillow for images/GIFs but I'm lazy
            # NOTE: ^ `get_PIL_safe_path` only still exists because of this
            if op_rotate_video is not None:
                log_on_statusbar('Video rotation/flip requested (this is a time-consuming task).')
                cmd = f'-i %in -vf "{op_rotate_video}" -crf 28 -c:a copy'
                if is_static_image:
                    with get_PIL_safe_path(original_path=video, final_path=dest) as temp_path:
                        self.ffmpeg(intermediate_file, cmd, temp_path)
                        intermediate_file = dest
                else:
                    intermediate_file = self.ffmpeg(intermediate_file, cmd, dest)
                if op_rotate_video == 'transpose=clock' or op_rotate_video == 'transpose=cclock':
                    vwidth, vheight = vheight, vwidth                               # update dimensions

            # replace audio track
            if op_replace_audio is not None:
                log_on_statusbar('Audio replacement requested.')
                audio = op_replace_audio    # TODO -shortest (before output) results in audio cutting out ~1 second before end of video despite the audio being longer
                intermediate_file = self.ffmpeg(intermediate_file, f'-i %in -i "{audio}" -c:v copy -map 0:v:0 -map 1:a:0', dest)

            # add audio track - adding audio to images or GIFs will turn them into videos
            # https://superuser.com/questions/1041816/combine-one-image-one-audio-file-to-make-one-video-using-ffmpeg
            if op_add_audio is not None:    # TODO :duration=shortest (after amix=inputs=2) has same issue as above
                audio = op_add_audio
                if is_static_image:         # static images
                    log_on_statusbar('Adding audio to static image.')
                    is_static_image = False                     # mark that this is no longer an image
                    if vwidth % 2 != 0 or vheight % 2 != 0:     # static image dimensions must be divisible by 2... for some reason
                        try:
                            with get_image_data(intermediate_file, extension) as image:
                                logging.info(f'Image dimensions aren\'t divisible by 2, cropping a pixel from the top and/or left and saving to {intermediate_file}.')
                                left = int(vwidth % 2 != 0)
                                top = int(vheight % 2 != 0)
                                image = image.crop((left, top, vwidth, vheight))    # left/top/right/bottom (crop takes a tuple)
                                image.save(intermediate_file, format=extension)     # specify `format` in case `intermediate_file`'s extension is unexpected
                                vwidth -= left
                                vheight -= top
                        except:
                            return log_on_statusbar(f'(!) Failed to crop image that isn\'t divisible by 2: {format_exc()}')
                    self.set_save_progress_max_signal.emit(int(get_audio_duration(audio) * 25))
                    intermediate_file = self.ffmpeg(            # ffmpeg defaults to using ^ 25fps for this
                        infile=intermediate_file,
                        cmd=f'-loop 1 -i %in -i "{audio}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest',
                        outfile=dest
                    )
                elif is_gif:                # gifs
                    log_on_statusbar('Adding audio to animated GIF (final video duration may not exactly line up with audio).')
                    is_gif = False                              # mark that this is no longer a gif
                    self.set_save_progress_max_signal.emit(int(get_audio_duration(audio) * frame_rate))
                    intermediate_file = self.ffmpeg(
                        infile=intermediate_file,
                        cmd=f'-stream_loop -1 -i %in -i "{audio}" -filter_complex amix=inputs=1 -shortest',
                        outfile=dest
                    )
                else:                       # video/audio TODO: adding "-stream_loop -1" and "-shortest" sometimes cause endless videos because ffmpeg is garbage
                    log_on_statusbar('Additional audio track requested.')
                    the_important_part = '-map 0:v:0 -map 1:a:0 -c:v copy' if mime == 'video' and audio_tracks == 0 else '-filter_complex amix=inputs=2'
                    intermediate_file = self.ffmpeg(intermediate_file, f'-i %in -i "{audio}" {the_important_part}', dest)

            # remove all video or audio tracks (does not turn file into an image/GIF)
            if op_remove_track is not None:                     # NOTE: This can degrade audio quality slightly.
                log_on_statusbar(f'{op_remove_track}-track removal requested.')
                intermediate_file = self.ffmpeg(intermediate_file, f'-i %in {"-q:a 0 -map a" if op_remove_track == "Video" else "-c copy -an"}', dest)

            # amplify audio (TODO: do math to chain several of these together at once to circumvent the max volume limitation)
            if op_amplify_audio is not None:
                log_on_statusbar('Audio amplification requested.')
                intermediate_file = self.ffmpeg(intermediate_file, f'-i %in -filter:a "volume={op_amplify_audio}"', dest)

        # --- Post-edit cleanup & opening our newly edited media ---
            # clean up temp paths if we have any
            for path in temp_paths:
                if exists(path):
                    try:
                        logging.debug(f'Removing temporary edit-path: {path}')
                        os.remove(path)
                    except:
                        logging.warning('(!) Failed to remove temporary edit-path')

            # confirm our operations, clean up base video, and get final path
            if operations:                                      # double-check that we've actually done anything at all
                if not exists(dest):
                    return log_on_statusbar('(!) Media saved without error, but never actually appeared. Possibly an FFmpeg error.')
                if os.stat(dest).st_size == 0:
                    os.remove(dest)
                    return log_on_statusbar('(!) Media saved without error, but was completely empty. Possibly an FFmpeg error.')

                # handle deletion behavior
                if delete_after_save == FULL_DELETE: self.delete(video, cycle=False)
                elif delete_after_save == MARK_DELETE: self.marked_for_deletion.add(video)
                #elif replacing_original:                       # TODO add setting for this behavior
                #    temp_name = add_path_suffix(video, '_original', unique=True)
                #    os.rename(video, temp_name)
                #    video = temp_name

                # rename `dest` back to `final_dest`
                if self.video == final_dest: self.stop()        # stop player again if necessary
                if exists(final_dest): os.replace(dest, final_dest)
                else: os.rename(dest, final_dest)

                # only open edited video if user hasn't opened something else TODO make this a setting
                if self.video == video:
                    self._save_open_signal.emit(final_dest, settings.checkCycleRememberOriginalPath.checkState() == 2)
                    if is_gif:                                  # gifs will often just... pause themselves after an edit
                        self.force_pause_signal.emit(False)     # this is the only way i've found to fix it
                elif settings.checkTextOnSave.isChecked():
                    show_on_player(f'Changes saved to {final_dest}.')
                log_on_statusbar(f'Changes saved to {final_dest} after {get_time() - start_time:.1f} seconds.')
            else: return log_on_statusbar('No changes have been made.')
        except: log_on_statusbar(f'(!) SAVE FAILED: {format_exc()}')
        finally:                                                # NOTE: this order is intentional
            self.locked_video = None                            # unlock video if needed
            self.set_save_progress_visible_signal.emit(False)   # hide the progress bar no matter what
            self.unsetCursor()                                  # restore cursor no matter what
            self.setFocus(True)                                 # restore keyboard focus so we can use hotkeys again
            self.set_save_progress_max_signal.emit(0)           # reset progress bar values
            self.set_save_progress_current_signal.emit(0)


    def update_gif_progress(self, frame: int):
        ''' Updates animated GIF progress by manually looping
            the GIF when outside the designated trim markers. '''
        if self.is_gif:
            if self.minimum <= frame <= self.maximum: update_progress(frame)
            else: set_and_update_progress(self.minimum)


    def update_progress(self, frame: int):
        ''' Updates every section of the UI to reflect the
            current `frame`. Clamps playback to desired trims.
            Loops if necessary. Locks spinboxes while updating. '''
        if not self.minimum <= frame <= self.maximum:
            if not (self.sliderProgress.grabbing_clamp_minimum or self.sliderProgress.grabbing_clamp_maximum):
                frame = min(self.maximum, max(self.minimum, frame))

                # pause or loop media if we've reached the end of our desired trim
                if frame == self.maximum and self.buttonTrimEnd.isChecked():
                    if not self.actionLoop.isChecked(): self.force_pause(True)
                    else: return set_and_update_progress(self.minimum)

        current_time = round(self.duration * (frame / self.frame_count), 3)
        self.current_time = current_time
        h, m, s, ms = get_hms(current_time)

        set_progress_slider(frame)
        if not current_time_lineedit_has_focus():       # use cleaner format for time-strings on videos > 1 hour
            set_current_time_text(f'{m:02}:{s:02}.{ms:02}' if self.duration < 3600 else f'{h}:{m:02}:{s:02}')

        self.lock_spin_updates = True                   # lock spins from actually updating player so we don't get recursion
        set_hour_spin(h)
        set_minute_spin(m)
        set_second_spin(s)
        set_frame_spin(frame)
        self.lock_spin_updates = False                  # unlock spins so they can be edited by hand again


    def _update_progress_slot(self, frame: float):
        ''' A slot for update_progress_signal which updates our progress in a thread-safe manner and without slowing
            down update_slider_thread. Takes `frame` as a float in order to handle partial frames caused by
            non-1 playback speeds. Saves the partial frame for later use as updates use an integer frame. '''
        # TODO: fractional_frame might not work as well as I hope
        frame += self.fractional_frame                  # add previous partial frame to get true position
        int_frame = int(frame)
        update_progress(int_frame)                      # update with an integer frame
        self.fractional_frame = frame - int_frame       # save new partial frame for later use


    def set_and_update_progress(self, frame: int = 0):
        ''' Simultaneously sets VLC/gif player position and updates progress on GUI. '''
        #self.set_player_time(round(frame * (1000 / self.frame_rate)))
        set_player_position(frame / self.frame_count)
        update_progress(frame)
        set_gif_position(frame)


    def update_slider_thread(self):
        ''' Handles updating the progress bar. This includes both slider-types and swapping between them.
            frame_override can be set to override the next pending frame (circumventing timing-related
            bugs), and if used with open_queued, the file-opening process is completed and cleaned up.
            While not playing and/or not visible, resource-usage is kept to a minimum. '''
        logging.info('Slider-updating thread started.')

        # re-define global aliases -> having them as locals is even faster
        current_frame = self.sliderProgress.value
        player = self.vlc.player
        is_playing = player.is_playing
        get_rate = player.get_rate                      # TODO: get_rate() vs. self.playback_speed <- which is faster?
        set_progress_slider = self.sliderProgress.setValue
        emit_open_signal = self._open_signal.emit
        _emit_update_progress_signal = self.update_progress_signal.emit
        _sleep = sleep
        _get_time = get_time

        while not self.closed:
            # window is NOT visible, stay relatively idle and do not update
            while not self.isVisible() and not self.closed: _sleep(0.25)

            # window is visible, but nothing is actively playing
            while self.isVisible() and not is_playing() and not self.closed:
                self.sliderProgress.update()            # force QVideoSlider to keep painting (this refreshes the hover-timestamp)
                _sleep(0.025)                           # update at 40fps

            # TODO this is where we'll handle the first part of high-precision v2
            self.swap_slider_styles_queued = False      # reset queued slider-swap (or the slider won't update anymore after a swap)

            # high-precision option enabled -> fake a smooth slider based on media's frame rate (simulates what libvlc SHOULD have)
            if settings.checkHighPrecisionProgress.isChecked():     # NOTE: (fast_start_interface_thread checks for accuracy every 5 seconds)
                start = _get_time()
                while is_playing() and not self.lock_progress_updates and not self.swap_slider_styles_queued:   # playing, not locked, and not about to swap styles
                    # lock_progress_updates is not always reached fast enough, so we use open_queued to force this thread to override the current frame
                    if self.frame_override != -1:
                        if self.open_queued:
                            emit_open_signal()          # _open_signal uses self._open_slot()
                            set_progress_slider(0)      # risky -> force sliderProgress to 0 to fix very rare timing issue (not thread safe, might "freeze" GUI)
                        else:
                            _emit_update_progress_signal(self.frame_override)
                        self.frame_override = -1        # reset frame_override
                        self.open_queued = False        # reset open_queued
                    elif (next_frame := current_frame() + 1 * get_rate()) <= self.frame_count:      # do NOT update progress if we're at the end
                        _emit_update_progress_signal(next_frame)                                    # update_progress_signal -> _update_progress_slot

                    _sleep(0.0001)                      # sleep to force-update get_time()
                    #try: _sleep(self.delay - (_get_time() - start))
                    try: _sleep(self.delay - (_get_time() - start) - 0.0007)
                    except Exception as error: logging.warning(f'update_slider_thread bottleneck - {type(error)}: {error} -> delay={self.delay} execution-time={_get_time() - start}')
                    finally: start = _get_time()

            # high-precision option disabled -> use libvlc's native progress at 8fps and manually paint QVideoSlider at 40fps
            else:
                while is_playing() and not self.lock_progress_updates and not self.swap_slider_styles_queued:   # not playing, not locked, and not about to swap styles
                    # lock_progress_updates is not always reached fast enough, so we use open_queued to force this thread to override the current frame
                    if self.frame_override != -1:
                        if self.open_queued:
                            emit_open_signal()          # _open_signal uses self._open_slot()
                            set_progress_slider(0)      # risky -> force sliderProgress to 0 to fix very rare timing issue (not thread safe, might "freeze" GUI)
                        else:
                            _emit_update_progress_signal(self.frame_override)
                        self.frame_override = -1        # reset frame_override
                        self.open_queued = False        # reset open_queued
                    else:
                        for _ in range(5):              # force QVideoSlider to paint at 40fps (this refreshes the hover-timestamp)
                            self.sliderProgress.update()
                            _sleep(0.025)               # only update slider position at 8fps (every 0.125 seconds -> VLC updates every 0.2-0.35)
                        new_frame = player.get_position() * self.frame_count                        # convert VLC position to frame
                        if new_frame >= current_frame(): _emit_update_progress_signal(new_frame)    # make sure VLC didn't literally go backwards (pretty common)
                        #else: _emit_update_progress_signal(int(new_frame + (self.frame_rate / 5))) # simulate a non-backwards update TODO this actually makes it look worse
        return logging.info('Program closed. Ending update_slider thread.')


    def update_time_spins(self):
        ''' Handles the hour, minute, and second spinboxes. Calculates the next frame based on the new
            values, and updates the progress UI accordingly. If the new frame is after the end of the media,
            it's replaced with the current frame and the progress UI is reset to its previous state. '''
        if self.lock_spin_updates or self.lock_progress_updates: return                             # return if user is not manually setting the time spins
        self.lock_progress_updates = True               # lock progress updates to prevent recursion errors from multiple elements updating at once
        try:
            seconds = self.spinHour.value() * 3600
            seconds += self.spinMinute.value() * 60
            seconds += self.spinSecond.value()

            old_frame = self.spinFrame.value()
            excess_frames = old_frame % self.frame_rate
            new_frame = math.ceil((seconds * self.frame_rate) + excess_frames)  # ceil() to ensure we don't overshoot frame_count on the next frame
            if new_frame > self.frame_count: update_progress(old_frame)
            else: set_and_update_progress(new_frame)

            logging.debug(f'Manually updating time-spins: seconds={seconds} frame {old_frame} -> {new_frame} ({excess_frames} excess frame(s))')
        except: logging.error(f'(!) UPDATE_TIME_SPINS FAILED: {format_exc()}')
        finally: self.lock_progress_updates = False             # always release lock on progress updates


    def update_frame_spin(self, frame: int):
        ''' If media is paused, updates UI based on frame spinbox's new value. '''
        try:
            if self.is_paused and not self.lock_progress_updates:
                try:
                    self.lock_progress_updates = True           # lock progress updates to prevent recursion errors from multiple elements updating at once
                    set_and_update_progress(frame)
                    #player.next_frame()                        # NOTE: this unfortunately does not fix the issues with frame-seeking at the end of a file
                except: logging.warning(f'Abnormal error while locking/setting/updating progress: {format_exc()}')
                finally: self.lock_progress_updates = False     # always release lock on progress updates
        except: logging.warning(f'Abnormal error while updating frame-spins: {format_exc()}')


    def manually_update_current_time(self):
        text = self.lineCurrentTime.text().strip()
        if not text: return
        logging.info(f'Manually updating current time "label" to {text}')

        try:
            if '%' in text:
                percent = float(text.strip('%').strip()) / 100  # do regular strip() again in case spaces were placed between number and %
                frame = self.frame_count * percent
            else:
                seconds = 0
                parts = tuple(float(part) for part in text.split(':') if part)    # float() takes care of milliseconds at the end
                if len(parts) == 3:   seconds += (parts[0] * 3600) + (parts[1] * 60) + parts[2]
                elif len(parts) == 2: seconds += (parts[0] * 60) + parts[1]
                elif len(parts) == 1: seconds = parts[0]
                frame = int(seconds * self.frame_rate)          # int() instead of ceil() to ensure we don't go too far

            if self.minimum <= frame <= self.maximum:
                try:
                    self.lock_progress_updates = True
                    set_and_update_progress(frame)
                except: logging.warning(f'Abnormal error while locking/setting/updating progress: {format_exc()}')
                finally: self.lock_progress_updates = False
        except: pass                                            # ignore invalid inputs
        finally: self.lineCurrentTime.clearFocus()              # clear focus after update no matter what


    # ---------------------
    # >>> FFMPEG <<<
    # ---------------------
    def ffmpeg(
        self,
        infile: str,
        cmd: str,
        outfile: str = None,
        frame_rate_hint: float = None,
        start_text: str = 'Saving (%p%)',
        active_text: str = 'Saving (%p%)'
    ) -> str:
        start = get_time()

        # aliases, then show progress bar and set progress bar format text
        emit_progress_text = self.set_save_progress_format_signal.emit
        emit_progress_value = self.set_save_progress_current_signal.emit
        emit_progress_text(start_text)
        emit_progress_value(0)                                              # we must call this to actually show the progress bar
        self.set_save_progress_visible_signal.emit(True)

        # ensure an %out variable is in `cmd` so we have a spot to insert `outfile`
        if not outfile: outfile = infile
        if '%out' not in cmd: cmd += ' %out'                                # ensure %out is present
        logging.info(f'Performing FFmpeg operation (infile={infile} | outfile={outfile} | cmd={cmd})')

        # create temp file if infile and outfile are the same
        if infile == outfile:
            temp_path = add_path_suffix(infile, '_temp', unique=True)
            if infile == self.locked_video: self.locked_video = temp_path   # update locked video if needed TODO does this make sense...?
            os.renames(infile, temp_path)                                   # rename `out` to temp name
            logging.info(f'Renamed "{infile}" to temporary FFmpeg file "{temp_path}"')
        else: temp_path = infile

        # run final ffmpeg command, replacing %in and %out with their respective (quote-surrounded) paths
        try: process = ffmpeg_async(cmd.replace('%in', f'"{temp_path}"').replace('%out', f'"{outfile}"'))
        except: logging.error(f'(!) FFMPEG CALL FAILED: {format_exc()}')

        # update progress bar using the 'frame=???' progress line from ffmpeg's stout
        # https://stackoverflow.com/questions/67386981/ffmpeg-python-tracking-transcoding-process/67409107#67409107
        # TODO: 'total_size=', time spent, and operations remaining could also be shown (save_progress_bar.setFormat())
        frame_rate = max(1, frame_rate_hint or self.frame_rate)             # used when ffmpeg provides `out_time_ms` instead of `frame`
        use_backup_lines = True
        lines_read = 0

        while True:
            if process.poll() is not None: break

            # loop over stout until we get to the line(s) we want
            # doing it this way lets us sleep between loops without falling behind, saving a lot of resources
            while True:
                progress_text = process.stdout.readline().strip()
                lines_read += 1
                logging.debug(f'FFmpeg output line #{lines_read}: {progress_text}')
                if not progress_text:
                    logging.info('FFmpeg output a blank progress line to STDOUT, leaving progress loop...')
                    break

                # normal videos will have a "frame" progress string
                if progress_text[:6] == 'frame=':
                    use_backup_lines = False                                # if we're using frames, DON'T use "out_time_ms" (less accurate)
                    frame = int(progress_text[6:].strip())
                    max_frames = self.save_progress_bar.maximum()           # this might change late, so always check it
                    emit_progress_value(min(frame, max_frames))
                    emit_progress_text(active_text)                         # reset format in case we changed it temporarily
                    break

                # ffmpeg usually uses "out_time_ms" for audio files
                elif use_backup_lines and progress_text[:12] == 'out_time_ms=':
                    try:
                        seconds = int(progress_text.strip()[12:-6])
                        frame = seconds * frame_rate
                        max_frames = self.save_progress_bar.maximum()       # this might change late, so always check it
                        emit_progress_value(min(frame, max_frames))
                        emit_progress_text(active_text)                     # reset format in case we changed it temporarily
                        break
                    except ValueError: pass
            sleep(0.2)

        # terminate process just in case ffmpeg got locked up
        try: process.terminate()
        except: pass

        # cleanup temp file, if needed
        if temp_path != infile:
            if exists(infile):
                try: os.remove(temp_path)
                except: logging.warning(f'Temporary FFmpeg file {temp_path} could not be deleted')
            else:       # TODO I don't think this can ever actually happen, and it makes as little sense as the locked_video line up there
                if temp_path == self.locked_video: self.locked_video = infile
                os.renames(temp_path, infile)
                logging.info(f'Renamed temporary FFmpeg file "{temp_path}" back to "{infile}"')
        log_on_statusbar(f'FFmpeg operation succeeded after {get_time() - start:.1f} seconds.')
        return outfile


    def set_trim_start(self, *args, force=False):
        if not self.video: return self.buttonTrimStart.setChecked(False)
        if self.is_static_image: return self.buttonTrimStart.setChecked(False)
        if force: self.buttonTrimStart.setChecked(True)         # force-check trim button, typically used from context menu

        if self.buttonTrimStart.isChecked():
            desired_minimum = get_progess_slider()
            if desired_minimum >= self.maximum:
                self.buttonTrimStart.setChecked(False)
                return log_on_statusbar('You cannot set the start of your trim after the end of it.')
            self.minimum = desired_minimum

            h, m, s, ms = get_hms(self.current_time)  # use cleaner format for time-strings on videos > 1 hour
            if self.duration < 3600: self.buttonTrimStart.setText(f'{m}:{s:02}.{ms:02}')
            else: self.buttonTrimStart.setText(f'{h}:{m:02}:{s:02}')
            self.sliderProgress.clamp_minimum = True
        else:
            self.minimum = self.sliderProgress.minimum()
            self.buttonTrimStart.setText('Start' if self.is_trim_mode() else ' Fade to ')
            self.sliderProgress.clamp_minimum = False


    def set_trim_end(self, *args, force=False):
        if not self.video: return self.buttonTrimEnd.setChecked(False)
        if self.is_static_image: return self.buttonTrimEnd.setChecked(False)
        if force: self.buttonTrimEnd.setChecked(True)           # force-check trim button, typically used from context menu

        if self.buttonTrimEnd.isChecked():
            desired_maximum = get_progess_slider()
            if desired_maximum <= self.minimum:
                self.buttonTrimEnd.setChecked(False)
                return log_on_statusbar('You cannot set the end of your trim before the start of it.')
            self.maximum = desired_maximum

            h, m, s, ms = get_hms(self.current_time)            # use cleaner format for time-strings on videos > 1 hour
            if self.duration < 3600: self.buttonTrimEnd.setText(f'{m}:{s:02}.{ms:02}')
            else: self.buttonTrimEnd.setText(f'{h}:{m:02}:{s:02}')
            self.sliderProgress.clamp_maximum = True
        else:
            self.maximum = self.sliderProgress.maximum()
            self.buttonTrimEnd.setText('End' if self.is_trim_mode() else ' Fade from ')
            self.sliderProgress.clamp_maximum = False


    def set_trim_mode(self, action: QtW.QAction):
        cfg.trimmodeselected = True
        if action in (self.actionTrimAuto, self.actionTrimPrecise):
            self.buttonTrimStart.setText(self.buttonTrimStart.text().replace(' Fade to ', 'Start'))
            self.buttonTrimEnd.setText(self.buttonTrimEnd.text().replace(' Fade from ', 'End'))
            for button in (self.buttonTrimStart, self.buttonTrimEnd):
                button.setToolTip(constants.TRIM_BUTTON_TOOLTIP_BASE.replace('?mode', 'trim'))
        else:
            self.buttonTrimStart.setText(self.buttonTrimStart.text().replace('Start', ' Fade to '))
            self.buttonTrimEnd.setText(self.buttonTrimEnd.text().replace('End', ' Fade from '))
            for button in (self.buttonTrimStart, self.buttonTrimEnd):
                button.setToolTip(constants.TRIM_BUTTON_TOOLTIP_BASE.replace('?mode', 'fade'))


    def concatenate(self, action: QtW.QAction, files=None):                             # TODO this is old and needs to be unified with the other edit methods
        # https://stackoverflow.com/questions/7333232/how-to-concatenate-two-mp4-files-using-ffmpeg
        # https://stackoverflow.com/questions/31691943/ffmpeg-concat-produces-dts-out-of-order-errors
        if not constants.verify_ffmpeg(self, force_warning=True):
            return marquee('You don\'t have FFmpeg installed!')

        style = {self.actionCatNone: 0, self.actionCatAny: 1, self.actionCatBefore: 2, self.actionCatAfter: 3}[action]
        if self.mime_type != 'video' and style > 1:
            return show_on_statusbar('Concatenation is not implemented for audio and image files yet.', 10000)

        try:
            if style > 1 and not self.video: return show_on_statusbar('No video is playing.', 10000)        # for styles that assume a video is playing -> return
            logging.info(f'Preparing to concatenate videos with style={style} and files={files}')

            # create/setup dialog and connect signals
            from bin.window_cat import Ui_catDialog
            dialog = qthelpers.getDialogFromUiClass(Ui_catDialog, **self.get_popup_location())
            dialog.checkOpen.setChecked(cfg.concatenate.open)
            dialog.checkExplore.setChecked(cfg.concatenate.explore)
            dialog.checkDelete.setCheckState(self.checkDeleteOriginal.checkState())     # set dialog's delete setting to our current delete setting
            dialog.output.setText(self.lineOutput.text().strip())                       # set dialog's output text to our current output text
            dialog.reverse.setIcon(self.icons['reverse_vertical'])

            dialog.add.clicked.connect(dialog.videoList.add)
            dialog.delete.clicked.connect(dialog.videoList.remove)
            dialog.up.clicked.connect(dialog.videoList.move)
            dialog.down.clicked.connect(lambda: dialog.videoList.move(down=True))
            dialog.reverse.clicked.connect(dialog.videoList.reverse)
            dialog.browse.clicked.connect(lambda: self.browse_for_save_file(dialog.output, 'concatenated video'))
            dialog.videoList.itemDoubleClicked.connect(lambda item: self.open(item.toolTip(), focus_window=False))

            # getting videos
            if files is None:
                if style == 0: files = tuple()                      # style 0 -> no videos, no browser. we just want the dialog
                elif style == 1 and self.video: files = (self.video,)                    # style 1 and video playing -> open the dialog with current video already present
                else: files, cfg.lastdir = qthelpers.browseForFiles(cfg.lastdir,         # style 1-3 -> browse for videos first
                                                                    caption='Select media files to concatenate together',
                                                                    filter='All files (*)')
                if len(files) == 0 and style != 0: return           # cancel selected (and an empty dialog was not requested) -> return
            if style == 2: files.append(self.video)                 # add currently playing video to selected files
            elif style == 3: files.insert(0, self.video)
            files = tuple(file.strip() for file in files if file)

            # open concatenation dialog
            if not (len(files) == 2 and style > 1):                 # style 2-3 and exactly 2 files selected means we know the videos and their order -> skip dialog
                dialog.videoList.add(files=files)
                if dialog.exec() == QtW.QDialog.Rejected: return    # cancel selected on dialog -> return
                files = tuple(item.toolTip() for item in dialog.videoList)
                logging.info(f'Concatenation dialog files: {files}')
                if len(files) < 2: return log_on_statusbar('Not enough videos to concatenate.')             # user ended up with <2 videos in dialog and hit OK -> return
            elif not dialog.output.text(): self.browse_for_save_file(dialog.output, 'concatenated video')   # dialog skipped, but no output text on main window (set on dialog earlier)
            log_on_statusbar(f'Concatenating files: {files}')

            # preparing videos for concatenation
            intermediate_files = []
            for file in files:
                temp_filename = file.replace('.mp4', '.ts').replace('/', '.').replace('\\', '.')
                intermediate_file = f'{constants.TEMP_DIR}{sep}{temp_filename}'
                try: os.remove(intermediate_file)
                except: pass
                intermediate_files.append(intermediate_file)
                ffmpeg(f'-i "{file}" -c copy -bsf:v h264_mp4toannexb -f mpegts "{intermediate_file}"')

            # preparing output destination
            output = dialog.output.text().strip()
            if not output: output = add_path_suffix(files[0] if style < 2 else self.video, '_concatenated')      # no output name -> default to first file's name + "_concatenated"
            if not splitext_media(output)[-1]: output = f'{output}{splitext_media(files[0], strict=False)[-1]}'  # append appropriate extension if needed
            output = get_unique_path(output)
            dirname, basename = os.path.split(output)
            if not dirname:                                         # no output directory specified
                default_dir = settings.lineDefaultOutputPath.text().strip()
                dirname = default_dir if default_dir else os.path.dirname(files[0])
            output = os.path.join(dirname, sanitize(basename))      # `sanitize` does not account for full paths

            # actually concatentating videos
            if self.mime_type == 'audio': cmd = f'-i "concat:{"|".join(intermediate_files)}" -c copy "{output}"'
            else: cmd = f'-i "concat:{"|".join(intermediate_files)}" -c copy -video_track_timescale 100 -bsf:a aac_adtstoasc -movflags faststart -f mp4 -threads 1 "{output}"'
            ffmpeg(cmd)
            for intermediate_file in intermediate_files:
                try: os.remove(intermediate_file)
                except: pass

            if not exists(output): return log_on_statusbar('(!) Concatenation failed. No files have been altered.')
            log_on_statusbar(f'Concatenation saved to {output}.')

            if dialog.checkExplore.isChecked(): qthelpers.openPath(output, explore=True)
            if dialog.checkOpen.isChecked(): self.open(output)
            if dialog.checkDelete.checkState() == 1: self.marked_for_deletion.update(files)
            elif dialog.checkDelete.checkState() == 2: self.delete(files)
        except: logging.error(f'(!) CONCATENATION FAILED: {format_exc()}')
        finally:
            try:
                dialog.close()              # TODO: !!! memory leak?
                cfg.concatenate.open = dialog.checkOpen.isChecked()
                cfg.concatenate.explore = dialog.checkExplore.isChecked()
                dialog.videoList.clear()    # clearing list does not free up the memory it takes
                dialog.deleteLater()        # deleting the dialog does not free up the list's memory either (you cannot delete the list items either)
                del dialog
                gc.collect(generation=2)
            except: logging.warning(f'(!) Unexpected error while closing concatenation dialog: {format_exc()}')


    def resize_media(self):                 # https://ottverse.com/change-resolution-resize-scale-video-using-ffmpeg/ TODO this should probably have an advanced crf option
        ''' Resizes the dimensions of video files, and changes the length of audio files. '''
        if not self.video: return show_on_statusbar('No media is playing.', 10000)
        width, height = self.show_size_dialog()
        if width is None: return            # dialog canceled
        if width == 0: width = -1           # ffmpeg takes -1 as a default value, not 0
        if height == 0: height = -1         # ffmpeg takes -1 as a default value, not 0

        # check for unchanged size/duration
        if self.mime_type == 'audio':
            if round(width, 2) == 1:        # might get something like 1.0000331463797563
                return show_on_statusbar('New length cannot be the same as the old length.', 10000)
        elif (width <= 0 or width == self.vwidth) and (height <= 0 or height == self.vheight):
            return show_on_statusbar('New size cannot be the same as the old size.', 10000)

        self.operations['resize'] = (width, height)
        self.save(noun='resized media', filter='All files(*)')              # don't really need any hints


    def rotate_video(self, action: QtW.QAction):
        if not self.video: return show_on_statusbar('No video is playing.', 10000)
        if self.mime_type == 'audio': return show_on_statusbar('Well that would just be silly, wouldn\'t it?', 10000)
        rotation_presets = {
            self.actionRotate90:         'transpose=clock',
            self.actionRotate180:        'transpose=clock,transpose=clock',
            self.actionRotate270:        'transpose=cclock',
            self.actionFlipVertically:   'vflip',
            self.actionFlipHorizontally: 'hflip'
        }
        self.operations['rotate video'] = rotation_presets[action]
        self.save(noun='rotated video/image', filter='All files(*)')        # don't really need any hints


    # TODO: doing this on an audio file is somewhat unstable
    # TODO: add option to toggle "shortest" setting?
    def add_audio(self, *args, path: str = None, save: bool = True):
        if not self.video: return show_on_statusbar('No media is playing.', 10000)
        try:
            if path is None: path, cfg.lastdir = qthelpers.browseForFile(cfg.lastdir, caption='Select audio file to add')
            if not path: return                                             # cancel selected
            self.operations['add audio'] = path
            if self.mime_type == 'image':
                filter = 'MP4 files (*.mp4);;All files (*)'
                valid_extensions = constants.VIDEO_EXTENSIONS
            elif self.mime_type == 'audio':
                filter = 'MP3 files (*.mp3);;WAV files (*.wav);;AAC files (*.aac);;All files (*)'
                valid_extensions = constants.VIDEO_EXTENSIONS + constants.AUDIO_EXTENSIONS
            else:
                filter = 'MP4 files (*.mp4);;MP3 files (*.mp3);;WAV files (*.wav);;AAC files (*.aac);;All files (*)'
                valid_extensions = constants.VIDEO_EXTENSIONS + constants.AUDIO_EXTENSIONS
            if save:                                                        # amplify_audio may call this, so saving is optional
                self.save(
                    noun='media with additional audio track',
                    filter=filter,
                    ext_hint='.mp4',
                    valid_extensions=valid_extensions
                )
        except: log_on_statusbar(f'(!) ADD_AUDIO FAILED: {format_exc()}')


    def amplify_audio(self):                # https://stackoverflow.com/questions/81627/how-can-i-hide-delete-the-help-button-on-the-title-bar-of-a-qt-dialog
        if not self.video: return show_on_statusbar('No media is playing.', 10000)

        if self.mime_type == 'image' or (self.mime_type == 'video' and player.audio_get_track_count() == 0):
            show_on_statusbar('Add audio first, then you can amplify it.')
            self.add_audio(save=False)
            filter = 'MP4 files (*.mp4);;All files (*)'
            valid_extensions = constants.VIDEO_EXTENSIONS
        elif self.mime_type == 'audio':
            filter = 'MP3 files (*.mp3);;WAV files (*.wav);;AAC files (*.aac);;All files (*)'
            valid_extensions = constants.VIDEO_EXTENSIONS + constants.AUDIO_EXTENSIONS
        else:
            filter = 'MP4 files (*.mp4);;MP3 files (*.mp3);;WAV files (*.wav);;AAC files (*.aac);;All files (*)'
            valid_extensions = constants.VIDEO_EXTENSIONS + constants.AUDIO_EXTENSIONS

        dialog = qthelpers.getDialog(title='Amplify Audio', **self.get_popup_location(), fixedSize=(125, 105), flags=Qt.Tool)
        layout = QtW.QVBoxLayout(dialog)
        label = QtW.QLabel('Input desired volume \n(applies on save):', dialog)
        spin = QtW.QSpinBox(dialog)
        spin.setSuffix('%')
        spin.setMaximum(1000)
        spin.setValue(self.last_amplify_audio_value)
        for w in (label, spin): layout.addWidget(w)
        dialog.addButtons(layout, QtW.QDialogButtonBox.Cancel, QtW.QDialogButtonBox.Ok)

        def accept():
            self.last_amplify_audio_value = spin.value()                     # save value to re-display it next time
            self.operations['amplify audio'] = round(spin.value() / 100, 2)  # convert volume to 0-1 range
            self.save(
                noun='amplified video/audio',
                filter=filter,
                ext_hint='.mp4',
                valid_extensions=valid_extensions
            )

        dialog.accepted.connect(accept)
        dialog.exec()


    def replace_audio(self, *args, path=None):
        if not self.video: return show_on_statusbar('No media is playing.', 10000)
        if self.mime_type == 'audio': return show_on_statusbar('Well that would just be silly, wouldn\'t it?', 10000)
        if self.mime_type == 'image': return self.add_audio(path=path)
        try:
            if path is None: path, cfg.lastdir = qthelpers.browseForFile(cfg.lastdir, caption='Select audio file to replace audio track with')
            if not path: return                                             # cancel selected
            self.operations['replace audio'] = path
            self.save(
                noun='video with replaced audio track',
                filter='MP4 files (*.mp4);;All files (*)',
                ext_hint='.mp4',
                valid_extensions=constants.VIDEO_EXTENSIONS
            )
        except: log_on_statusbar(f'(!) REPLACE_AUDIO FAILED: {format_exc()}')


    def remove_track(self, *args, audio=True):     # https://superuser.com/questions/268985/remove-audio-from-video-file-with-ffmpeg
        if not self.video: return show_on_statusbar('No media is playing.', 10000)
        if self.mime_type == 'image': return show_on_statusbar('Well that would just be silly, wouldn\'t it?', 10000)
        if self.mime_type == 'audio': return show_on_statusbar('Track removal for audio files is not supported yet.', 10000)
        if player.audio_get_track_count() == 0:
            if audio: return show_on_statusbar('There are no audio tracks left to remove.', 10000)
            else: return show_on_statusbar('There are no audio tracks. If you want to remove the video too, you might as well just close your eyes.', 10000)

        if audio:
            filter = 'MP4 files (*.mp4);;All files (*)'
            valid_extensions = constants.VIDEO_EXTENSIONS
            preferred_extensions = None
        else:
            filter = 'MP4 files (*.mp4);;MP3 files (*.mp3);;WAV files (*.wav);;AAC files (*.aac);;All files (*)'
            valid_extensions = constants.VIDEO_EXTENSIONS + constants.AUDIO_EXTENSIONS
            preferred_extensions = constants.AUDIO_EXTENSIONS

        self.operations['remove track'] = 'Audio' if audio else 'Video'     # we need to capitalize these later so might as well just do it here
        self.save(
            noun=f'{self.operations["remove track"]}',
            filter=filter,
            ext_hint=None if audio else '.mp3',                             # give hint for extension
            valid_extensions=valid_extensions,
            preferred_extensions=preferred_extensions                       # tells a potential "save as" prompt which extensions should be default
        )


    # ---------------------
    # >>> PROMPTS <<<
    # ---------------------
    def browse_for_directory(self, lineEdit=None, noun=None, default_path=None):
        if default_path is None: default_path = cfg.lastdir
        caption = f'Select {noun} directory' if noun else 'Select directory'
        path, cfg.lastdir = qthelpers.browseForDirectory(default_path, caption=caption, lineEdit=lineEdit)
        if path is None: return
        return path


    def browse_for_save_file(self, lineEdit=None, noun=None, filter='All files (*)', default_path=None, unique_default=True):
        if default_path is None or not exists(os.path.dirname(default_path)):
            current_path = self.video or '*.*'
            if settings.checkSaveAsUseMediaFolder.isChecked(): default_path = current_path
            else: default_path = os.path.join(cfg.lastdir, os.path.basename(current_path))
        caption = f'Save {noun} as...' if noun else 'Save as...'
        default_is_dir = os.path.isdir(default_path)
        if unique_default and not default_is_dir: default_path = get_unique_path(default_path)
        kwarg = {'directory' if default_is_dir else 'lastdir': default_path}
        selected_filter = 'All files (*)'       # NOTE: this simply does nothing if this filter isn't available
        path, cfg.lastdir = qthelpers.saveFile(
            **kwarg,
            caption=caption,
            filter=filter,
            selectedFilter=selected_filter,
            lineEdit=lineEdit
        )
        if path is None: return
        return path


    def browse_for_subtitle_file(self, urls=None):
        if self.mime_type == 'image': show_on_statusbar('Well that would just be silly, wouldn\'t it?', 10000)
        if urls is None:
            urls, cfg.lastdir = qthelpers.browseForFiles(
                cfg.lastdir,
                caption='Select subtitle file(s) to add',
                filter='Subtitle Files (*.cdg *.idx *.srt *.sub *.utf *.ass *.ssa *.aqt *.jss *.psb *.it *.sami *smi *.txt *.smil *.stl *.usf *.dks *.pjs *.mpl2 *.mks *.vtt *.tt *.ttml *.dfxp *.scc);;All files (*)',
                url=True
            )
        for url in urls:
            url = url.url()
            if player.add_slave(0, url, settings.checkAutoEnableSubtitles.isChecked()) == 0:    # slaves can be subtitles (0) or audio (1). last arg = auto-select
                log_on_statusbar(f'Subtitle file {url} added and enabled.')                     # returns 0 on success
                if settings.checkTextOnSubtitleAdded.isChecked(): show_on_player('Subtitle file added and enabled')
            else:
                log_on_statusbar(f'Failed to add subtitle file {url} (VLC does not report specific errors for this).')
                if settings.checkTextOnSubtitleAdded.isChecked(): show_on_player('Failed to add subtitle file')


    def show_size_dialog(self, snapshot=False):
        dimensions = snapshot or self.mime_type != 'audio'
        vwidth, vheight, duration = self.vwidth, self.vheight, self.duration
        max_time_string = self.labelMaxTime.text()
        dialog = qthelpers.getDialog(title='Input desired ' + 'size' if dimensions else 'length',
                                     **self.get_popup_location(), fixedSize=(0, 0), flags=Qt.Tool)

        layout = QtW.QVBoxLayout(dialog)
        form = QtW.QFormLayout()
        label = QtW.QLabel(dialog)
        if dimensions: label.setText(constants.SIZE_DIALOG_DIMENSIONS_LABEL_BASE.replace('?resolution', f'{vwidth}x{vheight}'))
        else: label.setText('Enter a timestamp (hh:mm:ss.ms)\nor a percentage. Note: This is\ncurrently limited to 50-200%\nof the original audio\'s length.')
        label.setAlignment(Qt.AlignCenter)

        wline = QtW.QLineEdit('0' if dimensions else max_time_string, dialog)
        wbutton = QtW.QPushButton('Width:' if dimensions else 'Length:', dialog)
        wbutton.clicked.connect(lambda: wline.setText(str(int(vwidth)) if dimensions else max_time_string))
        if dimensions: wbutton.setToolTip(f'Reset width to native resolution ({vwidth:.0f} pixels).')
        else: wbutton.setToolTip(f'Reset length to native length ({max_time_string}).')

        if dimensions:
            hline = QtW.QLineEdit('0', dialog)
            hbutton = QtW.QPushButton('Height:', dialog)
            hbutton.clicked.connect(lambda: hline.setText(str(int(vheight))))
            hbutton.setToolTip(f'Reset height to native resolution ({vheight:.0f} pixels).')

            if snapshot:                        # add JPEG quality label/spinbox
                qlabel = QtW.QLabel('Quality:', dialog)
                qlabel.setMinimumWidth(50)
                qlabel.setAlignment(Qt.AlignCenter)
                qlabel.setToolTip('JPEG quality (0-100). Higher is better. Does not apply if saved as PNG format.')
                qspin = QtW.QSpinBox(dialog)
                qspin.setValue(settings.spinSnapshotJpegQuality.value())
                qspin.setMaximum(100)

            for w in (wbutton, hbutton): w.setMaximumWidth(50)
            for w in (wline, hline):
                w.setMaxLength(6)
                w.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('\\d*%')))    # https://stackoverflow.com/questions/13422995/set-qlineedit-to-accept-only-numbers
        else: wbutton.setMaximumWidth(50)

        wline.selectAll()                       # start with text in width lineEdit selected, for quicker editing
        form.addRow(label)
        form.addRow(wbutton, wline)
        if dimensions: form.addRow(hbutton, hline)
        if snapshot: form.addRow(qlabel, qspin)
        layout.addLayout(form)
        dialog.addButtons(layout, QtW.QDialogButtonBox.Cancel, QtW.QDialogButtonBox.Ok)

        def accept():
            if dimensions:                      # if sizes are percents, strip '%' and multiply w/h by percentages.
                width, height =   wline.text().strip(), hline.text().strip()
                if '%' in width:  width = round(vwidth * (float(width.strip('%').strip()) / 100))
                else:             width = int(width) if width else 0                    # blank lineEdit defaults to 0
                if '%' in height: height = round(vheight * (float(height.strip('%').strip()) / 100))
                else:             height = int(height) if height else 0                 # blank lineEdit defaults to 0
            else:                               # audio resize, check for timestamp-style string instead (hh:mm:ss.ms)
                width, height = wline.text().strip(), None
                if '%' in width: width = 1 / (float(width.strip('%').strip()) / 100)    # convert percentage to tempo-multiplier
                else:
                    seconds = 0
                    parts = tuple(float(part) for part in width.split(':') if part)     # float() takes care of milliseconds at the end
                    if len(parts) == 3:   seconds += (parts[0] * 3600) + (parts[1] * 60) + parts[2]
                    elif len(parts) == 2: seconds += (parts[0] * 60) + parts[1]
                    elif len(parts) == 1: seconds = parts[0]
                    width = duration / seconds  # actual length is not a percent, but a multiplier
                width = min(2, max(0.5, width))
            dialog.width = width
            dialog.height = height
            if snapshot: dialog.quality = qspin.value()

        # open resize dialog. if cancel is selected, return None
        dialog.accepted.connect(accept)
        if not dialog.exec(): return (None, None, None) if snapshot else (None, None)
        return (dialog.width, dialog.height, dialog.quality) if snapshot else (dialog.width, dialog.height)


    def show_about_dialog(self):                # lazy version of about dialog
        from bin.window_about import Ui_aboutDialog
        dialog_about = qthelpers.getDialogFromUiClass(Ui_aboutDialog, **self.get_popup_location(),
                                                      modal=True, deleteOnClose=True)
        dialog_about.labelLogo.setPixmap(QtGui.QPixmap(f'{constants.RESOURCE_DIR}{sep}logo_filled.png'))
        dialog_about.labelVersion.setText(dialog_about.labelVersion.text().replace('?version', constants.VERSION))

        settings_were_open = settings.isVisible()               # hide the always-on-top settings while we show popups
        if settings_were_open: settings.hide()
        dialog_about.adjustSize()                               # adjust size to match version string/OS fonts
        dialog_about.exec()                                     # don't bother setting a fixed size or using open()
        if settings_were_open: settings.show()                  # restore settings if they were originally open

        del dialog_about
        gc.collect(generation=2)


    def show_trim_dialog(self):
        ''' Opens dialog for selecting which trim mode to default to. Only
            meant to appear for new users that haven't adjusted their trim
            settings yet. Sets cfg.trimmodeselected to True. '''
        try:
            self.force_pause(True)
            dialog = qthelpers.getDialog(title='Choose default trim mode', **self.get_popup_location(),
                                         modal=True, deleteOnClose=True, flags=Qt.Tool)
            dialog.setMinimumSize(427, 220)
            dialog.resize(0, 0)

            label = QtW.QLabel(
                'Which trimming style would you prefer? You can change this '
                'setting in the future through the \'Video\' menu, or by '
                'right-clicking the \'Start\' and \'End\' buttons.\n\nNote: '
                'The end of a trim is always accurate for both trim types.')
            button_precise = QtW.QCommandLinkButton(
                'Precise trim',
                'Re-encode your trim. Slow, but accurate. '
                'Works on most formats.')
            button_auto = QtW.QCommandLinkButton(
                'Auto trim',
                'Instantly trim your clip by rounding back to the last '
                'keyframe and cutting from there. May result in brief '
                'corruption at the at the start of the trim. PyPlayer '
                'will use precise trims regardless in some situations. '
                'Not supported on all formats.')
            check_always_pick = QtW.QCheckBox('Always show this dialog')

            label.setAlignment(Qt.AlignCenter)
            label.setWordWrap(True)
            button_precise.setDefault(True)
            button_precise.clicked.connect(dialog.accept)
            button_precise.clicked.connect(lambda: dialog.select(button_precise))
            button_auto.clicked.connect(dialog.accept)
            button_auto.clicked.connect(lambda: dialog.select(button_auto))
            check_always_pick.setChecked(self.actionTrimPickEveryTime.isChecked())

            check_layout = QtW.QHBoxLayout()
            check_layout.addStretch(0)
            check_layout.addWidget(check_always_pick)
            check_layout.addStretch(0)
            layout = QtW.QVBoxLayout(dialog)
            layout.addWidget(label)
            layout.addLayout(check_layout)
            layout.addWidget(button_precise)
            layout.addWidget(button_auto)

            def accept():
                self.actionTrimPickEveryTime.setChecked(check_always_pick.isChecked())

            if constants.PLATFORM != 'Windows': dialog.adjustSize()
            dialog.accepted.connect(accept)
            if dialog.exec() == QtW.QDialog.Accepted:
                if dialog.choice == button_auto: self.actionTrimAuto.setChecked(True)
                else: self.actionTrimPrecise.setChecked(True)
            else: self.trim_mode_selection_canceled = True
        except: log_on_statusbar(f'(!) TRIM DIALOG ERROR: {format_exc()}')
        finally: cfg.trimmodeselected = True                        # set this to True no matter what (_save is waiting on this)


    def show_delete_prompt(self, *args, exiting: bool = False):     # *args to capture unused signal args
        ''' Creates and shows a dialog for deleting marked files. Dialog
            consists of a QGroupBox containing a QCheckBox for each file,
            with Yes/No/Cancel buttons at the bottom. '''
        marked_for_deletion = self.marked_for_deletion

        # remove missing files from list and check if any are left
        marked_for_deletion = [f for f in marked_for_deletion if exists(f)]
        if not marked_for_deletion: return log_on_statusbar('No media is marked for deletion.')
        logging.info('Opening deletion prompt...')
        try:
            dialog = qthelpers.getDialog(title='Confirm Deletion', icon='SP_DialogDiscardButton', **self.get_popup_location())
            recycle = settings.checkRecycleBin.isChecked()
            marked = []
            unmarked = []

            # layout at "fixed size" https://stackoverflow.com/questions/14980620/qt-layout-resize-to-minimum-after-widget-size-changes
            layout = QtW.QVBoxLayout(dialog)
            layout.setSizeConstraint(QtW.QLayout.SetFixedSize)

            # group box and its own layout
            group = QtW.QGroupBox(f'The following files will be {"recycled. Recycle?" if recycle else "permanently deleted. Delete?"}', dialog)
            group.setAlignment(Qt.AlignHCenter)
            groupLayout = QtW.QVBoxLayout(group)
            layout.addWidget(group)

            # footer label
            if not exiting:
                label = QtW.QLabel('Clicking "No" will remove unchecked files from your deletion list.')
                label.setAlignment(Qt.AlignCenter)
                layout.addWidget(label)

            # checkboxes for each file (key=splitext to ignore extensions when sorting)
            # TODO add setting related to sorting the files
            for file in sorted(marked_for_deletion, key=os.path.splitext):
                checkbox = QtW.QCheckBox(file, group)
                checkbox.setChecked(True)
                groupLayout.addWidget(checkbox)

            def finished(result):
                for check in group.children():
                    if isinstance(check, QtW.QCheckBox):
                        (marked if check.isChecked() else unmarked).append(check.text())

            dialog.addButtons(layout, QtW.QDialogButtonBox.Cancel, QtW.QDialogButtonBox.No, QtW.QDialogButtonBox.Yes)
            dialog.finished.connect(finished)
            dialog.exec()

            if dialog.choice == QtW.QDialogButtonBox.Yes:
                self.delete(marked)
            elif dialog.choice == QtW.QDialogButtonBox.No:
                for file in unmarked:
                    self.mark_for_deletion(False, file)

            logging.info(f'Deletion dialog choice: {dialog.choice}')
            return dialog.choice
        except: log_on_statusbar(f'(!) DELETION PROMPT FAILED: {format_exc()}')


    def show_color_picker(self):
        ''' Opens color-picking dialog, specifically for the hover-timestamp font color setting.
            Saves new color and adjusts the color of the color-picker's button through a stylesheet. '''
        # NOTE: F suffix is Float -> values are represented from 0-1 (e.g. getRgb() becomes getRgbF())
        try:                                            # TODO: add support for marquee colors
            picker = QtW.QColorDialog()
            #for index, default in enumerate(self.defaults): picker.setCustomColor(index, QtGui.QColor(*default))
            color = picker.getColor(initial=self.sliderProgress.hover_font_color, parent=self.dialog_settings, title='Picker? I hardly know her!')
            if not color.isValid(): return
            self.sliderProgress.hover_font_color = color

            color_string = str(color.getRgb())
            settings.buttonHoverFontColor.setToolTip(color_string)
            settings.buttonHoverFontColor.setStyleSheet('QPushButton {background-color: rgb' + color_string + ';border: 1px solid black;}')
        except: log_on_statusbar(f'OPEN_COLOR_PICKER FAILED: {format_exc()}')


    # -------------------------------
    # >>> UTILITY FUNCTIONS <<<
    # -------------------------------
    def _log_on_statusbar_slot(self, msg, timeout=20000):
        ''' Logs a `msg` while simultaneously displaying it
            on the status bar for `timeout` milliseconds. '''
        logging.info(msg)
        show_on_statusbar(msg, timeout)


    def marquee(self, text: str, timeout: int = 350, marq_key: str = '', log: bool = True):
        ''' Conditionally displays `text` as a marquee over the player if
            the associated setting at `marq_key` is checked. Alawys displayed
            on statusbar. Logs as well if `log` is True.

            Example: marq_key='Save' -> checkTextOnSave.isChecked()? '''
        if log: log_on_statusbar(text)
        else: show_on_statusbar(text, 10000)
        try:
            if settings.__dict__[f'checkTextOn{marq_key}'].isChecked():
                show_on_player(text, timeout)
        except:
            pass


    def handle_updates(self, _launch=False):
        ''' Handles validating/checking updates as well as updating the settings dialog. Updates
            are only validated on launch, and if 'update_report.txt' is present. Update checks only
            occur on launch if it has been spinUpdateFrequency days since the last check. The last
            check date is only saved down to the day so that checks on launch are more predictable. '''
        if self.checking_for_updates: return            # prevent spamming the "check for updates" button
        just_updated = False

        if _launch:
            settings.labelLastCheck.setText(f'Last check: {cfg.lastupdatecheck or "never"}')
            settings.labelCurrentVersion.setText(f'Current version: {constants.VERSION}')
            settings.labelGithub.setText(settings.labelGithub.text().replace('?url', f'{constants.REPOSITORY_URL}/releases/latest'))
            update_report = f'{constants.CWD}{sep}update_report.txt'
            if exists(update_report):
                import update
                update.validate_update(self, update_report)
                just_updated = True

        if not _launch or settings.checkAutoUpdateCheck.isChecked():
            try: last_check_time_seconds = mktime(strptime(cfg.lastupdatecheck, '%x'))  # string into seconds needs %x
            except: last_check_time_seconds = 0
            if not _launch or last_check_time_seconds + (86400 * settings.spinUpdateFrequency.value()) < get_time():
                if not just_updated: log_on_statusbar('Checking for updates...')
                self.checking_for_updates = True
                settings.buttonCheckForUpdates.setText('Checking for updates...')

                if constants.IS_COMPILED:               # if compiled, override cacert.pem path to get rid of pointless folder
                    import certifi.core
                    cacert_override_path = f'{constants.BIN_DIR}{sep}cacert.pem'
                    os.environ["REQUESTS_CA_BUNDLE"] = cacert_override_path
                    certifi.core.where = lambda: cacert_override_path

                import update
                Thread(target=update.check_for_update, args=(self, not just_updated, _launch)).start()

                cfg.lastupdatecheck = strftime('%#D', localtime())                      # seconds into string needs %D
                settings.labelLastCheck.setText(f'Last check: {cfg.lastupdatecheck}')


    def _handle_updates(self, results: dict, popup_kwargs: dict):
        ''' A slot for update.check_for_update which cleans up and handles the results of an update
            check, if any, in a thread-safe manner. `results` is a dict containing either 'failed'
            to represent that there was an unusual error that could still indicate a pending update
            (mismatched URL format on Github, for example), or 'latest_version_url'. `popup_kwargs`
            are the keyword-arguments needed to construct the relevant QMessageBox. '''
        try:
            logging.info(f'Cleaning up after update check. results={results}')
            settings_were_open = settings.isVisible()   # hide the always-on-top settings while we show popups
            if settings_were_open: settings.hide()
            if results:     # display relevant popups. if `results` is empty, skip the popups and only do cleanup
                if 'failed' in results: return qthelpers.getPopup(**popup_kwargs, **self.get_popup_location()).exec()

                # did not fail, and update is available. on windows -> auto-updater popup (TODO: cross-platform autoupdating)
                if constants.IS_COMPILED and constants.PLATFORM == 'Windows':
                    choice = qthelpers.getPopup(**popup_kwargs, **self.get_popup_location()).exec()
                    if choice == QtW.QMessageBox.Yes:
                        import update
                        name = constants.VERSION.split()[0]
                        latest_version_url = results['latest_version_url']
                        latest_version = latest_version_url.split('/')[-1].lstrip('v')

                        filename = f'{name}_{latest_version}.zip'
                        download_url = f'{latest_version_url.replace("/tag/", "/download/")}/{filename}'
                        download_path = f'{constants.TEMP_DIR}{sep}{filename}'
                        update.download_update(self, latest_version, download_url, download_path)
                else: return qthelpers.getPopup(**popup_kwargs, **self.get_popup_location()).exec()  # non-windows version of popup
        finally:
            self.checking_for_updates = False
            settings.buttonCheckForUpdates.setText('Check for updates')
            if settings_were_open: settings.show()      # restore settings if they were originally open


    def get_renamed_output(self, new_name: str = None, valid_extensions: tuple = constants.ALL_MEDIA_EXTENSIONS) -> tuple:
        ''' Returns `new_name` or `self.lineOutput` as a valid/sanitized/unique
            path, along with its extensionless basename and its extension (as
            determined by `valid_extensions`). If `new_name` ends up the same
            as `self.video`, `new_name` and `self.lineOutput` are both blank,
            or no media is playing, then three `None`'s are returned. '''
        output_text = self.lineOutput.text().strip()
        video = self.video
        if not video or (not new_name and not output_text):
            return None, None, None

        try:
            old_oscwd = os.getcwd()
            os.chdir(os.path.dirname(video))            # set os module's CWD to self.video's folder -> allows things like abspath, '.', and '..'

            # get absolute path, sanitize basename, then check for a valid extension
            path = abspath(new_name or output_text)
            dirname, basename = os.path.split(path)
            basename = sanitize(basename)
            new_name = abspath(os.path.join(dirname, basename))
            basename_no_ext, ext = splitext_media(basename, valid_extensions)

            # append valid extension if needed
            if not ext:
                ext = splitext_media(video)[-1]
                if not ext: ext = '.' + self.extension
                new_name = f'{new_name}{ext}'

            # make sure new name isn't the same as the old name
            if new_name == video:
                return None, None, None

            # TODO make the usage of `get_unique_path` a setting (use os.replace instead of renames)
            return get_unique_path(new_name), basename_no_ext, ext
        except:
            log_on_statusbar(f'(!) Could not get valid string from output textbox: {format_exc()}')
            return None, None, None
        finally:
            os.chdir(old_oscwd)                         # reset os module's CWD before returning


    def get_popup_location(self):
        ''' Returns keyword arguments as a dictionary for
            the center-parameters of popups and dialogs. '''
        index = settings.comboDialogPosition.currentIndex()
        if index: widget = None
        elif not constants.APP_RUNNING:                 # index is 0 but geometry isn't set yet, use cfg to get center of window
            x, y = cfg.pos
            w, h = cfg.size
            x += w / 2
            y += h / 2
            widget = (x, y)
        else: widget = self.vlc if self.vlc.height() >= 20 else self.frameGeometry()    # use VLC window if it's big enough
        return {'centerWidget': widget, 'centerScreen': index == 1, 'centerMouse': index == 2}


    def add_info_actions(self, context: QtW.QMenu):
        context.addSeparator()
        context.addAction(f'Size: {self.size_label}').setEnabled(False)
        context.addAction(f'Res: {self.vwidth:.0f}x{self.vheight:.0f}').setEnabled(False)
        context.addAction(f'Ratio: {self.ratio}').setEnabled(False)


    def swap_slider_styles(self):
        ''' Used to switch between high-precision and low-precision sliders in update_slider_thread. '''
        self.swap_slider_styles_queued = True


    def set_fullscreen(self, fullscreen: bool):
        ''' Toggles fullscreen-mode on and off. Saves window-state to self.was_maximized to
            remember if the window is maximized or not and restore the window accordingly. '''
        self.dockControls.setFloating(fullscreen)       # FramelessWindowHint and WindowStaysOnTopHint not needed
        if fullscreen:  # TODO: figure out why dockControls won't resize in fullscreen mode -> strange behavior when showing/hiding control-frames
            current_screen = app.screenAt(self.mapToGlobal(self.rect().center()))       # fullscreen destination is based on center of window
            screen_size = current_screen.size()
            screen_geometry = current_screen.geometry()

            width_factor = settings.spinFullScreenWidth.value() / 100
            width = int(screen_size.width() * width_factor)
            height = sum(frame.height() for frame in (self.frameProgress, self.frameAdvancedControls) if frame.isVisible())
            x = int(screen_geometry.right() - ((screen_size.width() + width) / 2))      # adjust x/y values for screen's actual global position
            y = screen_geometry.bottom() - height

            self.dockControls.resize(width, height)
            #self.dockControls.setFixedWidth(width)     # TODO this is bad for DPI/scale and doesn't even fully get rid of the horizontal separator cursors. bandaid fix
            self.dockControls.move(x, y)
            self.dockControls.setWindowOpacity(settings.spinFullScreenMaxOpacity.value() / 100)     # opacity only applies while floating

            # if we're already hovering over the pending dockControls rect OR the video already ended (and we're not paused) -> lock fullscreen controls
            self.lock_fullscreen_ui = (not player.is_playing() and not self.is_paused) or QtCore.QRect(x, y, width, height).contains(QtGui.QCursor().pos())

            self.statusbar.setVisible(False)
            self.menubar.setVisible(False)              # TODO should this be like set_crop_mode's version? this requires up to 2 alt-presses to open
            self.was_maximized = self.isMaximized()     # remember if we're maximized or not
            self.vlc.last_move_time = get_time()        # reset last_move_time, just in case we literally haven't moved the mouse yet
            return self.showFullScreen()                # FullScreen with a capital S
        else:
            self.statusbar.setVisible(self.actionShowStatusBar.isChecked())
            self.menubar.setVisible(self.actionShowMenuBar.isChecked())
            #self.dockControls.setFixedWidth(QWIDGETSIZE_MAX)
            if self.was_maximized: self.showMaximized()
            else: self.showNormal()


    def set_playback_speed(self, rate: float):
        ''' Sets, saves, and displays the playback speed/rate for the video. '''
        player.set_rate(rate)
        image_player.gif.setSpeed(rate * 100)
        self.playback_speed = rate
        if settings.checkTextOnSpeed.isChecked(): show_on_player(f'{rate:.2f}x', 1000)
        log_on_statusbar(f'Playback speed set to {rate:.2f}x')


    def set_volume(self, volume):
        try:
            volume = int(volume * self.volume_boost)
            player.audio_set_volume(volume)
            player.audio_set_mute(False)
            self.sliderVolume.setEnabled(True)
            self.sliderVolume.setToolTip(f'{volume}%')
            if settings.checkTextOnVolume.isChecked(): show_on_player(f'{volume}%%', 200)
            refresh_title()
        except:
            if self.first_video_fully_loaded:
                logging.error(format_exc())


    def toggle_mute(self):
        try:
            muted = not bool(player.audio_get_mute())   # returns 1 or 0
            player.audio_set_mute(muted)
            self.sliderVolume.setEnabled(not muted)     # disabled if muted, enabled if not muted
            self.sliderVolume.setToolTip('Muted (M)' if muted else f'Unmuted ({get_volume_slider()}%)')
            if settings.checkTextOnMute.isChecked(): show_on_player('Muted (M)' if muted else f'Unmuted ({get_volume_slider()}%%)')
        except: logging.error(format_exc())


    def set_advancedcontrols_visible(self, visible: bool):
        self.vlc.last_invalid_snap_state_time = get_time()
        self.actionShowAdvancedControls.setChecked(visible)
        self.frameAdvancedControls.setVisible(visible)


    def set_progressbar_visible(self, visible: bool):
        ''' Readjusts the advanced controls' margins based on whether
            or not the progress bar's frame is `visible`. '''
        self.vlc.last_invalid_snap_state_time = get_time()
        self.frameProgress.setVisible(visible)
        self.actionShowProgressBar.setChecked(visible)
        self.frameAdvancedControls.layout().setContentsMargins(0, 0 if visible else 3, 0, 0 if self.statusbar.isVisible() else 3)       # left/top/right/bottom


    def set_statusbar_visible(self, visible: bool):
        ''' Readjusts the advanced controls' margins based
            on whether or not the status bar is `visible`. '''
        self.vlc.last_invalid_snap_state_time = get_time()
        self.statusbar.setVisible(visible)
        self.actionShowStatusBar.setChecked(visible)
        self.frameAdvancedControls.layout().setContentsMargins(0, 0 if self.frameProgress.isVisible() else 3, 0, 0 if visible else 3)   # left/top/right/bottom


    def set_menubar_visible(self, visible: bool):
        ''' Resizes window to avoid size-snapping based on whether or not the
            menubar is `visible`. Does nothing if crop mode is active. '''
        if visible:
            self.vlc.last_invalid_snap_state_time = get_time()
            if self.actionCrop.isChecked():
                return self.actionShowMenuBar.setChecked(False)
        self.menubar.setVisible(visible)
        self.actionShowMenuBar.setChecked(visible)
        if not self.isMaximized() and not self.isFullScreen() and self.first_video_fully_loaded:    # do not resize until a video is loaded
            height = self.menubar.height()
            self.resize(self.width(), self.height() + (height if visible else -height))             # resize window to preserve player size


    def set_crop_mode(self, on):     # https://video.stackexchange.com/questions/4563/how-can-i-crop-a-video-with-ffmpeg
        try:
            mime = self.mime_type
            is_gif = self.is_gif
            if not self.video or (self.mime_type == 'audio' and not image_player.pixmap()):         # reset crop mode if there's nothing to crop
                return self.actionCrop.trigger() if on else None

            if not on:
                self.disable_crop_mode()
            else:
                vlc = self.vlc
                restore_state = self.crop_restore_state
                if self.menubar.isVisible():
                    self.set_menubar_visible(False)
                    restore_state['menubar_visible'] = True
                else: restore_state['menubar_visible'] = False

                if is_gif:
                    restore_state['scale_setting'] = settings.comboScaleGifs
                    restore_state['scale_updater'] = image_player._updateGifScale
                elif mime == 'image':
                    restore_state['scale_setting'] = settings.comboScaleImages
                    restore_state['scale_updater'] = image_player._updateImageScale
                elif mime == 'audio':
                    restore_state['scale_setting'] = settings.comboScaleArt
                    restore_state['scale_updater'] = image_player._updateArtScale

                if 'scale_updater' in restore_state:
                    restore_state['scale_updater'](1 if is_gif else 2, force=True)
                    image_player.disableZoom()

                log_on_statusbar('Crop mode enabled. Right-click or press C to exit.')
                vlc.find_true_borders()

                if not vlc.selection:
                    vlc.selection = [
                        QtCore.QPoint(vlc.true_left + 20,  vlc.true_top + 20),      # 0 top left
                        QtCore.QPoint(vlc.true_right - 20, vlc.true_top + 20),      # 1 top right
                        QtCore.QPoint(vlc.true_left + 20,  vlc.true_bottom - 20),   # 2 bottom left
                        QtCore.QPoint(vlc.true_right - 20, vlc.true_bottom - 20)    # 3 bottom right
                    ]
                    s = vlc.selection
                    vlc.last_factored_points = s.copy()
                    vlc.crop_rect = QtCore.QRect(s[0], s[3])

                    class P:
                        ''' Enum representing points of the crop rectangle in QVideoPlayer.selection. Used here
                            purely for readablity purposes, performance impact is not worth it in realtime. '''
                        __slots__ = ()
                        TOP_LEFT = 0
                        TOP_RIGHT = 1
                        BOTTOM_LEFT = 2
                        BOTTOM_RIGHT = 3

                    vlc.reference_example = {
                        P.TOP_LEFT:     {P.TOP_LEFT:     lambda x, y: (s[0].setX(min(x, s[3].x() - 10)), s[0].setY(min(y, s[3].y() - 10))),
                                         P.TOP_RIGHT:    lambda _, y:  s[1].setY(min(y, s[2].y() - 10)),
                                         P.BOTTOM_LEFT:  lambda x, _:  s[2].setX(min(x, s[1].x() - 10))},
                        P.TOP_RIGHT:    {P.TOP_LEFT:     lambda _, y:  s[0].setY(min(y, s[2].y() - 10)),
                                         P.TOP_RIGHT:    lambda x, y: (s[1].setX(max(x, s[2].x() + 10)), s[1].setY(min(y, s[2].y() - 10))),
                                         P.BOTTOM_RIGHT: lambda x, _:  s[3].setX(max(x, s[0].x() + 10))},
                        P.BOTTOM_LEFT:  {P.TOP_LEFT:     lambda x, _:  s[0].setX(min(x, s[1].x() - 10)),
                                         P.BOTTOM_LEFT:  lambda x, y: (s[2].setX(min(x, s[1].x() - 10)), s[2].setY(max(y, s[1].y() + 10))),
                                         P.BOTTOM_RIGHT: lambda _, y:  s[3].setY(max(y, s[0].y() + 10))},
                        P.BOTTOM_RIGHT: {P.TOP_RIGHT:    lambda x, _:  s[1].setX(max(x, s[0].x() + 10)),
                                         P.BOTTOM_LEFT:  lambda _, y:  s[2].setY(max(y, s[0].y() + 10)),
                                         P.BOTTOM_RIGHT: lambda x, y: (s[3].setX(max(x, s[0].x() + 10)), s[3].setY(max(y, s[0].y() + 10)))}
                    }
                    vlc.text_y_offsets = {P.TOP_LEFT: -8, P.TOP_RIGHT: -8, P.BOTTOM_LEFT: 14, P.BOTTOM_RIGHT: 14}
                    vlc.cursors = {
                        0: Qt.SizeFDiagCursor,
                        1: Qt.SizeBDiagCursor,
                        2: Qt.SizeBDiagCursor,
                        3: Qt.SizeFDiagCursor
                    }

                if not vlc.crop_frames:
                    vlc.crop_frames = (     # can't reuse crop_frames alias here since it is None
                        QtW.QFrame(self),   # 0 top
                        QtW.QFrame(self),   # 1 left
                        QtW.QFrame(self),   # 2 right
                        QtW.QFrame(self),   # 3 bottom
                    )

                    for view in vlc.crop_frames:
                        view.mousePressEvent = vlc.mousePressEvent
                        view.mouseMoveEvent = vlc.mouseMoveEvent
                        view.mouseReleaseEvent = vlc.mouseReleaseEvent
                        view.mouseDoubleClickEvent = vlc.mouseDoubleClickEvent
                        view.setVisible(True)
                        view.setMouseTracking(True)
                        view.setStyleSheet('background: rgba(0, 0, 0, 135)')        # TODO add setting here?
                else:
                    for view in vlc.crop_frames:
                        view.setVisible(True)

                width = self.width()
                vlc.update_crop_frames()                                            # update crop frames and factored points
                self.frameCropInfo.setVisible(width >= 621)                         # show crop info panel if there's space
                self.frameQuickChecks.setVisible(width >= 800)                      # hide checkmarks if there's no space
                while app.overrideCursor(): app.restoreOverrideCursor()             # reset cursor
        except: log_on_statusbar(f'(!) Failed to toggle crop mode: {format_exc()}')


    def disable_crop_mode(self, log: bool = True):
        for view in self.vlc.crop_frames:
            view.setVisible(False)
            view.setMouseTracking(False)
        image_player.update()                                                       # repaint gifPlayer to fix background
        self.vlc.setToolTip('')                                                     # clear crop-size tooltip
        self.vlc.dragging = None                                                    # clear crop-drag
        self.vlc.panning = False                                                    # clear crop-pan
        self.frameCropInfo.setVisible(False)                                        # hide crop info panel
        self.frameQuickChecks.setVisible(self.width() >= 568)                       # show checkmarks if there's space
        while app.overrideCursor(): app.restoreOverrideCursor()                     # reset cursor

        # uncheck action and restore menubar/scale state. NOTE: if you do this part...
        # ...first, there's a chance of seeing a flicker after a crop edit is saved
        self.actionCrop.setChecked(False)
        restore_state = self.crop_restore_state
        self.set_menubar_visible(restore_state['menubar_visible'])
        if 'scale_setting' in restore_state:
            current_value = restore_state['scale_setting'].currentIndex()
            restore_state['scale_updater'](current_value, force=True)
        restore_state.clear()
        if log: log_on_statusbar('Crop mode disabled.')


    def is_snap_mode_enabled(self):
        mime = self.mime_type
        if mime == 'audio': return image_player.pixmap() and settings.checkSnapArt.isChecked()
        elif mime == 'video': return settings.checkSnapVideos.isChecked()
        elif self.is_gif: return settings.checkSnapGifs.isChecked()
        else: return settings.checkSnapImages.isChecked()


    def snap_to_player_size(self, shrink=False, force_instant_resize=False):
        if self.video and not self.isMaximized() and not self.isFullScreen():
            vlc_size = self.vlc.size()
            expected_vlc_size = self.vsize.scaled(vlc_size, Qt.KeepAspectRatio)
            void_width = vlc_size.width() - expected_vlc_size.width()
            void_height = vlc_size.height() - expected_vlc_size.height()

            # default instant snap. normally this shrinks the window, but to mitigate this and have a more balanced...
            # ...resize, we snap twice - once to resize it bigger than needed, then again to shrink it back down
            if force_instant_resize or settings.checkSnapOnResize.checkState() == 2:
                if not shrink:      # to shrink the window, just skip this -> shrinking is the default behavior
                    ratio = self.vwidth / self.vheight
                    void = round((void_width if void_width else void_height) / 2)

                    # TODO +28 here or window gets smaller when switching between videos with different ratios
                    expected_vlc_size.scale(expected_vlc_size.width() + round(void * ratio), expected_vlc_size.height() + round(void / ratio) + 28, Qt.KeepAspectRatio)
                    true_height = expected_vlc_size.height() + self.height() - self.vlc.height()
                    if expected_vlc_size != vlc_size: self.resize(expected_vlc_size.width(), true_height)
                    return self.snap_to_player_size(shrink=True)    # snap again, but shrink this time

            # experimental animated snap (discovered by accident)
            else:
                expected_vlc_size.setWidth(expected_vlc_size.width() + round(void_width / 2))
                expected_vlc_size.setHeight(expected_vlc_size.height() + round(void_height / 2))

            # resize window if player size does not match the expected size (expected size = w/o black bars)
            true_height = expected_vlc_size.height() + self.height() - self.vlc.height()
            if expected_vlc_size != vlc_size: self.resize(expected_vlc_size.width(), true_height)

            # move and resize to fit within screen if necessary
            if settings.checkClampOnResize.isChecked():
                frame_size = self.frameGeometry().size()
                screen = qthelpers.getScreenForRect(self.geometry())
                screen_size = screen.availableSize()
                if frame_size.height() > screen_size.height() or frame_size.width() > screen_size.width():
                    self.resize(self.frameGeometry().size().boundedTo(screen_size))
                    self.snap_to_player_size(shrink=True)
                qthelpers.clampToScreen(self, screen=screen, resize=False)


    def snap_to_native_size(self):
        if not self.video: return
        excess_height = self.height() - self.vlc.height()
        self.resize(self.vwidth, self.vheight + excess_height)
        qthelpers.clampToScreen(self)


    def cycle_track(self, track_type: str):
        types = {'video':    (player.video_get_track_description, player.video_get_track_count, player.video_get_track),
                 'audio':    (player.audio_get_track_description, player.audio_get_track_count, player.audio_get_track),
                 'subtitle': (player.video_get_spu_description, player.video_get_spu_count,   player.video_get_spu)}
        get_description, get_count, get_track = types[track_type]

        track_count = get_count() - 1
        if track_count > 0:
            current_track = get_track()
            first_track_parameters = (-1, None, None)
            show_title = settings.checkTrackCycleShowTitle.isChecked()
            for true_index, (track_index, track_title) in enumerate(get_description()):
                track_title = str(track_title)[2:-1] if show_title else None
                if first_track_parameters[0] == -1 and track_index > -1:
                    first_track_parameters = (track_index, true_index, track_title)
                if track_index > current_track:                 # ^ mark the first valid track
                    self.set_track(track_type, track_index, true_index, track_title)
                    break

            # `else` is reached if we didn't break the for-loop (we ran out of tracks to cycle through)
            # loop back to either the first valid track or to "disabled", depending on user settings
            else:
                if settings.checkTrackCycleCantDisable.isChecked():
                    if first_track_parameters[0] != current_track:
                        self.set_track(track_type, *first_track_parameters)
                    else:                                       # display special message if there's nothing else to cycle to
                        marquee(f'No other {track_type} tracks available', marq_key='TrackChanged', log=False)
                else:
                    self.set_track(track_type, -1)
        else:
            marquee(f'No {track_type} tracks available', marq_key='TrackChanged', log=False)


    def set_track(self, track_type: str, track: int = -1, true_index: int = None, title: str = None):
        types = {'video':    (-1, player.video_set_track),      # -1 = disabled, 0 = track 1
                 'audio':    (0,  player.audio_set_track),      # -1 = disabled, 1 = track 1
                 'subtitle': (1,  player.video_set_spu)}        # -1 = disabled, 2 = track 1
        offset_from_1, _set_track = types[track_type]

        if isinstance(track, QtW.QAction):                      # `track` is actually a QAction
            true_index = int(track.toolTip())                   # true index is stored in the action's tooltip
            track = track.data()                                # track index is stored in the action's `data` property

        # actually set the track, then choose what number we're going to show in the marquee
        _set_track(track)
        track_index = true_index if true_index is not None else (track - offset_from_1)

        # check if `title` is actually unique and not something like "Track 1"
        if title is not None:
            parts = title.split()
            if len(parts) > 1 and parts[0].lower() == 'track':  # V detect things like 'Track "2"' or 'Track 2)'
                if parts[1].strip('"\'()[]{}<>;:-').isnumeric():
                    if len(parts) > 2:                          # V skip third "word" if it's just a hyphen or something
                        start = 2 if parts[2].strip('"\'()[]{}<>;:-') else 3
                        title = ' '.join(parts[start:])
                    else: title = None
                else: title = None

        # if `title` is (or has become) None, use generic marquee, i.e. "Audio track 2 enabled"
        # otherwise, use something like "Audio track 2 'Microphone' enabled"
        prefix = f'{track_type.capitalize().rstrip("s")} track {track_index}'
        if not title: title = f'{prefix} enabled'
        else: title = f'{prefix}  \'{title}\' enabled'

        if track != -1: marquee(title, marq_key='TrackChanged', log=False)
        else: marquee(f'{track_type.capitalize()} disabled', marq_key='TrackChanged', log=False)
        gc.collect(generation=2)


    def refresh_track_menu(self, menu: QtW.QMenu):
        menus = {self.menuVideoTracks: ('video',    player.video_get_track_description, player.video_get_track, player.video_get_track_count, 2, -1),
                 self.menuAudioTracks: ('audio',    player.audio_get_track_description, player.audio_get_track, player.audio_get_track_count, 1, 0),
                 self.menuSubtitles:   ('subtitle', player.video_get_spu_description, player.video_get_spu, player.video_get_spu_count, 1, 0)}
        string, get_description, get_track, get_count, count_offset, minimum_tracks = menus[menu]

        menu.clear()                                            # clear previous contents of menu
        if menu is self.menuSubtitles:
            menu.addAction(self.actionAddSubtitleFile)
            menu.addSeparator()

        # TODO
        #print(f'get_full_title_descriptions={list(player.get_full_title_descriptions())}')
        #print(f'get_full_chapter_descriptions={player.get_full_chapter_descriptions(-1)}')
        #import vlc as vlc2
        #track = list(self.vlc.media.tracks_get())[0]
        #print(f'track.audio={track.audio}')    # 'audio', 'codec', 'id', 'level', 'original_fourcc', 'profile', 'subtitle', 'type', 'video'
        #print(f'codec_description={vlc2.libvlc_media_get_codec_description(track.type, track.codec)}')

        track_count = get_count() - count_offset
        if track_count > minimum_tracks:
            current_track = get_track()
            action_group = QtW.QActionGroup(menu)
            action_group.triggered.connect(lambda *args: self.set_track(string, *args))

            for true_index, (track_index, track_title) in enumerate(get_description()):
                name_parts = track_title.decode().split()       # check if track number is in it's title -> add &-shortcut
                new_parts = []
                for index, part in enumerate(name_parts):
                    if part.isnumeric():                        # track number identified, add &-shortcut and stop
                        new_parts.append('&' + part)
                        new_parts.extend(name_parts[index + 1:])
                        break
                    else: new_parts.append(part)
                track_name = ' '.join(new_parts)

                # create and add action, storing its track index and true index in its `data` and tooltip
                action = QtW.QAction(track_name, action_group)  # get_spu_description includes pre-generated track titles with tags -> VLC uses the last...
                action.setData(track_index)                     # ...non-extension keyword separated by a period in the filename as the track's tag
                action.setToolTip(str(true_index))              # e.g. 'dawnofthedead.2004.ENG.srt' -> 'Track 1 - [ENG]'
                action.setCheckable(True)                       # originally I was doing all of that manually, while juggling the random inconsistent indexes
                if current_track == track_index:                # NOTE: one year later and I don't remember why I put these comments here ^
                    action.setChecked(True)
                menu.addAction(action)
        else:
            menu.addAction(f'No {string} tracks').setEnabled(False)


    def refresh_recent_menu(self):
        ''' Clears and refreshes the recent files submenu. '''
        self.menuRecent.clear()
        if len(self.recent_files) > 25:
            self.menuRecent.addAction(self.actionClearRecent)   # add separator and clear action at top for very long lists
            self.menuRecent.addSeparator()

        update = settings.checkRecentFilesReorderFromMenu.isChecked()
        get_open_lambda = lambda path: lambda: self.open_recent_file(path, update=update)
        get_basename = os.path.basename
        for index, file in enumerate(reversed(self.recent_files)):                      # reversed to show most recent first
            number = str(index + 1)
            action = QtW.QAction(f'{number[:-1]}&{number[-1]}. {get_basename(file)}', self.menuRecent)
            action.triggered.connect(get_open_lambda(file))     # workaround for python bug/oddity involving creating lambdas in iterables
            action.setToolTip(file)
            self.menuRecent.addAction(action)

        if len(self.recent_files) <= 25:
            self.menuRecent.addSeparator()
            self.menuRecent.addAction(self.actionClearRecent)   # add separator and clear action at bottom for shorter lists


    def _refresh_title_slot(self):                              # TODO this could theoretically be much faster, but is it worth it?
        ''' Updates the window's titlebar using various variables, based on
            `lineWindowTitleFormat`. This can be called directly, but you
            probably shouldn't. '''
        if self.video:
            path = self.video
            basepath, name = os.path.split(path)
            parent = f'{basepath.split(sep)[-1]}{sep}{name}'
            base, _ = splitext_media(name, strict=False)        # don't actually need ext, just the accurate basename

            mime = self.mime_type.capitalize()                  # capitalize first letter of mime type
            paused = '■' if get_progess_slider() == self.frame_count else '▷' if not self.is_paused else '𝗜𝗜'   # ▶
            h, m, s, _ = get_hms(self.duration)
            duration = f'{m}:{s:02}' if self.duration < 3600 else f'{h}:{m:02}:{s:02}'  # no milliseconds in window title
            if mime != 'Audio':                                 # remember, we just capitalized this
                fps = str(self.frame_rate_rounded)
                resolution = f'{self.vwidth:.0f}x{self.vheight:.0f}'
            elif image_player.pixmap():                         # show resolution of cover art
                fps = '0'
                resolution = f'{self.vwidth:.0f}x{self.vheight:.0f}'
            else:
                fps = '0'
                resolution = '0x0'
            ratio = self.ratio
        else:
            path = name = base = parent = 'No media is playing'
            mime = 'Unknown'
            paused = '■'    # ▁▂▃▄▅▇▉ ▊▋█ ❏ ?paused ?name (?duration | ?fpsfps)
            fps = '0'       # ?base | ?name | ?parent | ?path | ?ext | ?mime | ?paused | ?fps | ?duration | ?resolution | ?ratio | ?volume | ?speed | ?size
            duration = '--:--'
            resolution = '0x0'
            ratio = '0:0'

        title = settings.lineWindowTitleFormat.text()
        replace = {'?base': base, '?name': name, '?parent': parent, '?path': path, '?ext': self.extension.upper(), '?mime': mime,
                   '?paused': paused, '?fps': fps, '?duration': duration, '?resolution': resolution, '?ratio': ratio,
                   '?volume': str(get_volume_slider()), '?speed': f'{player.get_rate():.2f}', '?size': self.size_label}
        for var, val in replace.items(): title = title.replace(var, val)
        self.setWindowTitle(title.strip())


    def refresh_copy_image_action(self):
        mime = self.mime_type
        cropped = self.actionCrop.isChecked()
        if mime == 'audio': text = 'Copy cover art'
        elif mime == 'video' or self.is_gif: text = 'Copy cropped frame' if cropped else 'Copy frame'
        else: text = 'Copy cropped image' if cropped else 'Copy image'
        self.actionCopyImage.setText('&' + text)
        return self.actionCopyImage


    def refresh_shortcuts(self, last_edit: widgets.QKeySequenceFlexibleEdit = None):
        # get list of all keySequenceEdits
        all_key_sequence_edits = []
        for layout in qthelpers.formGetItemsInColumn(settings.formKeys, 1):
            for child in qthelpers.layoutGetItems(layout):
                all_key_sequence_edits.append(child)

        # check and swap any keySequenceEdits that have the same keySequence as the one we just set
        if last_edit is not None:
            name = last_edit.objectName()
            index = 0 if name[-1] != '_' else 1
            name = name.rstrip('_')
            new_key_sequence = last_edit.keySequence()
            if new_key_sequence:            # empty key sequence -> don't check for duplicates
                for other_edit in all_key_sequence_edits:
                    if other_edit.keySequence() == new_key_sequence and other_edit is not last_edit:
                        other_name = other_edit.objectName()
                        other_index = 0 if other_name[-1] != '_' else 1
                        other_name = other_name.rstrip('_')

                        old_shortcut_key = self.shortcuts[name][index].key()
                        other_edit.setKeySequence(old_shortcut_key)
                        self.shortcuts[other_name][other_index].setKey(old_shortcut_key)
            self.shortcuts[name][index].setKey(new_key_sequence)

        # check and clear any instance of two keySequenceEdits having the same keySequence (higher in the menu = higher priority)
        else:                               # this is meant for use at startup only -> clearing duplicates caused by manual config editing
            for edit in all_key_sequence_edits:
                name = edit.objectName()
                index = 0 if name[-1] != '_' else 1
                name = name.rstrip('_')
                for other_edit in all_key_sequence_edits:       # loop over every keySequenceEdit for every keySequenceEdit to compare all of them
                    if edit.keySequence() == other_edit.keySequence() and edit is not other_edit:
                        other_name = other_edit.objectName()
                        other_index = 0 if other_name[-1] != '_' else 1
                        other_name = other_name.rstrip('_')
                        other_edit.setKeySequence(0)
                        self.shortcuts[other_name][other_index].setKey(other_edit.keySequence())
                self.shortcuts[name][index].setKey(edit.keySequence())


    def refresh_autoplay_button(self):
        ''' Updates the autoplay button's icon and check-state. '''
        if self.actionAutoplayShuffle.isChecked(): icon = 'autoplay_shuffle'
        elif self.actionAutoplayDirectionForwards.isChecked(): icon = 'autoplay'
        elif self.actionAutoplayDirectionBackwards.isChecked(): icon = 'autoplay_backward'
        elif self.last_cycle_was_forward: icon = 'autoplay'
        else: icon = 'autoplay_backward'
        self.buttonAutoplay.setIcon(self.icons[icon])
        self.buttonAutoplay.setChecked(self.actionAutoplay.isChecked())


    def refresh_snapshot_button_controls(self):
        default = self.snapshot_actions[settings.comboSnapshotDefault.currentIndex()]
        shift   = self.snapshot_actions[settings.comboSnapshotShift.currentIndex()]
        ctrl    = self.snapshot_actions[settings.comboSnapshotCtrl.currentIndex()]
        alt     = self.snapshot_actions[settings.comboSnapshotAlt.currentIndex()]
        self.buttonSnapshot.setToolTip(
            constants.SNAPSHOT_TOOLTIP_BASE.replace('?click',      default[1])
                                           .replace('?shiftclick', shift[1])
                                           .replace('?ctrlclick',  ctrl[1])
                                           .replace('?altclick',   alt[1])
        )


    def handle_snapshot_button(self):
        mod = app.keyboardModifiers()
        if not mod:                    self.snapshot_actions[settings.comboSnapshotDefault.currentIndex()][0]()
        elif mod & Qt.ShiftModifier:   self.snapshot_actions[settings.comboSnapshotShift.currentIndex()][0]()
        elif mod & Qt.ControlModifier: self.snapshot_actions[settings.comboSnapshotCtrl.currentIndex()][0]()
        elif mod & Qt.AltModifier:     self.snapshot_actions[settings.comboSnapshotAlt.currentIndex()][0]()
        else:                          self.snapshot_actions[settings.comboSnapshotAlt.currentIndex()][0]()


    def page_step_slider(self, action):
        ''' Required because Qt genuinely doesn't emit any other signals for page steps. Values
            are clamped to the progress slider's minimum and maximum values, to prevent wrapping. '''
        slider = self.sliderProgress
        if action == 3:     # page step add
            new_frame = min(slider.maximum(), max(slider.minimum(), slider.value() + slider.pageStep()))
            set_and_update_progress(new_frame)
        elif action == 4:   # page step sub
            new_frame = min(slider.maximum(), max(slider.minimum(), slider.value() - slider.pageStep()))
            set_and_update_progress(new_frame)
        if self.restarted and settings.checkNavigationUnpause.isChecked():
            self.pause()    # auto-unpause after restart


    def mark_for_deletion(self, checked: bool = False, file=None, mode=None):
        ''' Marks a `file` for deletion if `checked` is `True`. Alternate
            behavior can be triggered if `mode` is set to "delete" or "prompt".
            If `mode` is `None`, it will automatically be set to "delete" if
            Ctrl is being held down, or "prompt" if shift is held down.

            `checked` and `file` are backwards to accomodate Qt passing the
            check-state first in its signals. '''

        if not self.video:
            if checked: self.actionMarkDeleted.trigger()
            return show_on_statusbar('No media is playing.', 10000)
        file = file or self.video

        if mode is None:
            mod = app.keyboardModifiers()
            if mod:
                if mod & Qt.ControlModifier: mode = 'delete'    # ctrl pressed -> immediately delete video
                elif mod & Qt.ShiftModifier: mode = 'prompt'    # shift pressed -> show deletion prompt
        else: mode = mode.lower()
        logging.info(f'Marking file {file} for deletion: {checked}. Mode: {mode}')

        if mode == 'delete': self.delete(file)
        elif mode == 'prompt': self.show_delete_prompt()
        elif checked and file: self.marked_for_deletion.add(file)
        elif not checked:
            try: self.marked_for_deletion.remove(file)
            except (ValueError, KeyError): pass
            except: log_on_statusbar(f'(!) MARK_FOR_DELETION FAILED: {format_exc()}')

        # ensure mark-button is in the correct state and update tooltip
        if file == self.video:
            self.actionMarkDeleted.setChecked(checked)
            self.buttonMarkDeleted.setChecked(checked)
        tooltip_count_string = f'{len(self.marked_for_deletion)} file{"s" if len(self.marked_for_deletion) != 1 else ""}'
        self.buttonMarkDeleted.setToolTip(constants.MARK_DELETED_TOOLTIP_BASE.replace('?count', tooltip_count_string))


    def clear_marked_for_deletion(self):
        self.marked_for_deletion.clear()
        self.actionMarkDeleted.setChecked(False)
        self.buttonMarkDeleted.setChecked(False)
        self.buttonMarkDeleted.setToolTip(constants.MARK_DELETED_TOOLTIP_BASE.replace('?count', '0'))


    # https://www.geeksforgeeks.org/convert-png-to-jpg-using-python/
    def convert_snapshot_to_jpeg(self, path: str = None, image_data=None, quality: int = None):
        # TODO update docstring
        ''' Saves image at `path` as a JPEG file with the desired quality in the settings
            dialog, using PIL. Assumes that `path` already ends in a valid file-extension. '''
        if quality is None:
            quality = settings.spinSnapshotJpegQuality.value()

        if image_data is None:
            with get_PIL_Image().open(path) as image:
                return self.convert_snapshot_to_jpeg(path, image, quality)

        if path is None:    # generate temp path
            #time = str(get_time()).replace(".", "")
            path = get_unique_path(f'{constants.TEMP_DIR}{sep}{get_time()}.jpg')

        image_data.convert('RGB')
        log_on_statusbar(f'Saving JPEG snapshot at {quality}% quality to {path}.')
        image_data.save(path, quality=quality)
        return path


#######################################
if __name__ == "__main__":
    if not constants.IS_COMPILED:
        import executable.hook                          # manually import launch-hook when running from script
        from PIL import Image                           # get_PIL_Image sometimes hangs on import when running from script
    try:
        logging.info(f'PyPlayer opened at {constants.SCRIPT_PATH} with executable {sys.executable}')
        logging.info('Creating QApplication and GUI...')
        app = widgets.app = QtW.QApplication(sys.argv)  # init qt
        gui = widgets.gui = GUI_Instance(app)           # init empty GUI instance
        gui.setup()                                     # setup gui's variables, widgets, and threads (0.3mb)

        # --------------------------------------------------------
        # Aliases for common/time-sensitive functions & variables
        # --------------------------------------------------------
        player = gui.vlc.player
        image_player = gui.gifPlayer
        play = gui.vlc.play
        play_image = gui.gifPlayer.play
        settings = gui.dialog_settings
        refresh_title = gui.refresh_title_signal.emit
        marquee = gui.marquee
        show_on_player = gui.vlc.show_text
        log_on_statusbar = gui.log_on_statusbar_signal.emit
        show_on_statusbar = gui.statusbar.showMessage
        update_progress = gui.update_progress
        set_and_update_progress = gui.set_and_update_progress
        emit_update_progress_signal = gui.update_progress_signal.emit
        set_volume_slider = gui.sliderVolume.setValue
        get_volume_slider = gui.sliderVolume.value
        get_volume_scroll_increment = settings.spinVolumeScroll.value
        get_progess_slider = gui.sliderProgress.value
        set_progress_slider = gui.sliderProgress.setValue
        set_pause_button_text = gui.buttonPause.setText
        set_hour_spin = gui.spinHour.setValue
        set_minute_spin = gui.spinMinute.setValue
        set_second_spin = gui.spinSecond.setValue
        set_frame_spin = gui.spinFrame.setValue
        set_player_position = player.set_position
        set_gif_position = image_player.gif.jumpToFrame
        set_current_time_text = gui.lineCurrentTime.setText
        current_time_lineedit_has_focus = gui.lineCurrentTime.hasFocus
        sep = os.sep
        exists = os.path.exists
        abspath = os.path.abspath

        qtstart.connect_widget_signals(gui)             # connect signals and slots
        cfg = widgets.cfg = config.loadConfig(gui)      # create and load config (uses constants.CONFIG_PATH)
        gui.refresh_theme_combo(set_theme=cfg.theme)    # load and set themes
        gui.refresh_autoplay_button()                   # set appropriate autoplay button icon
        if not qtstart.args.minimized: gui.show()       # show UI
        else:
            check_tray = settings.groupTray
            if not check_tray.isChecked():              # if tray icon is enabled, don't show UI at all
                gui.showMinimized()                     # otherwise, start with window minimized

        constants.verify_ffmpeg(gui)                    # confirm/look for valid ffmpeg path if needed
        FFPROBE = constants.verify_ffprobe(gui)         # confirm/look/return valid ffprobe path if needed
        widgets.settings = settings                     # set settings dialog as global object in widgets.py
        qtstart.after_show_setup(gui)                   # perform final bits of misc setup before showing UI

        with open(constants.PID_PATH, 'w'):             # create PID file
            gc.collect(generation=2)                    # final garbage collection before starting
            constants.APP_RUNNING = True
            logging.info(f'Starting GUI after {get_time() - constants.SCRIPT_START_TIME:.2f} seconds.')
            try: app.exec()
            except: logging.critical(f'(!) GUI FAILED TO EXECUTE: {format_exc()}')
            logging.info('Application execution has finished.')
        try: os.remove(constants.PID_PATH)
        except: logging.warning('(!) Failed to remove PID file:' + format_exc())
    except: logging.critical(f'(!) SCRIPT FAILED TO INITIALIZE: {format_exc()}')
