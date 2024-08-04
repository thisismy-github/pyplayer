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
TODO: need a way to deal with VLC registry edits
TODO: move browse dialogs + indeterminate_progress decorator to qthelpers/util?
TODO: better/more fleshed-out themes
TODO: can't change themes while minimized to system tray (warn with tray icon?)
TODO: live-themes option? (button that auto-refreshes themes every half-second for theme-editing)
TODO: make more "modern" looking icon like VLC's ios app icon?
TODO: event_manager -> "no signature found for builtin <built-in method emit of PyQt5.QtCore.pyqtBoundSignal object"
TODO: getting the padding of the QSlider groove
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
        - audio_get_channel/audio_set_channel
        - VideoAdjustOption enum (hue/brightness/whatnot)
        - AudioEqualizer class
        - all_slave, but for un-saved audio tracks
        - get_full_title_descriptions <- Get the full description of available titles.
        - BROKEN? -> get_full_chapter_descriptions(i_chapters_of_title) <- Get full description of available chapters. @param index of title to query for chapters (uses current title if set to -1)
TODO: make use of .nfo files to expand auto-opening abilities for subtitles -> look at language + subtitle filename/format and find it
        - VLC already auto-opens subtitle files if they contain the media file's name anywhere in their own name
        - maybe check if media file has metadata and compare it against all non-matching .nfo files
TODO: tab-order no longer exists due to setting everything to ClickFocus (worthwhile sacrifice?)
        - previousInFocusChain and NextInFocusChain might be usable for best of both worlds
TODO: upload-to-imgur button? NOTE: requires client-id and requests Session. perhaps a secret advanced option
        - "plugin" support could be just loading python files before showing GUI
TODO: use "rotate" metadata to have a live preview of rotations (might cause too many issues)? (or use QMediaPlayer and rotate manually)
        - VLC has a way to rotate videos natively (this may be involving either callbacks (hard) or filters (easy?))
TODO: custom rotate angle option (possibly difficult, ffmpeg has bizarre syntax for it)
TODO: more secure way of locking videos during editing? like with an actual file lock (QtCore.QLockFile)
optimization: identify the length of time required for each part of the startup process
optimization: are there too many QActions and lambdas?
optimization: use direct libvlc functions
optimization: remove translate flags from .ui file? maybe not a good idea
TODO: use qtawesome icons/fonts? https://pypi.org/project/QtAwesome/ <- qta-browser
TODO: enhanced playback speed option (context menu/menubar)?
TODO: playlists (adapt smart shuffle to them too)
TODO: playing online media like VLC
TODO: video_set_aspect_ratio and video_set_scale (this is for "zooming")
TODO: add setting to make total duration label show the remaining time instead
TODO: add settings for trim graphics?
TODO: more fullscreen settings? (alternate animation -> raise/lower instead of fade, separate idle timer, etc.)
TODO: finish marquee settings: drop shadow (VLC can control this, but I have no idea how), Color
        - fade durations aren't working very well, I was forced to put arbitrary limits on the settings
TODO: vlc settings to add
        - video/audio dependent raise/focus settings
        - settings for allowing multiple instances? (you can already sorta do this)
        - "enable time-stretching audio" -> fixes audio pitch changing with playback speed
        - --start-paused, --no-start-paused
TODO: gstreamer | ffpyplayer https://matham.github.io/ffpyplayer/player.html
TODO: https://wiki.videolan.org/Documentation:Modules/alphamask/
TODO: WA_PaintUnclipped https://doc.qt.io/qt-5/qt.html#WidgetAttribute-enum
TODO: app.primaryScreenChanged.connect()
TODO: is there a way to add/modify libvlc options like "--gain" post-launch? media.add_option() is very limited
TODO: make logo in about window clickable and link to somewhere
TODO: "add subtitle file" but for video/audio tracks? (audio tracks supported, but VLC chooses not to use this)
TODO: formats that still don't trim correctly after save() rewrite: 3gp, ogv, mpg (used to trim inaccurately, now doesn't trim at all)
        - trimming likely needs to not use libx264 and aac for every format
TODO: ram usage
        - !!! if it fails, update checking adds 15mb of ram that never goes away (~42mb before -> 57mb after)
        - if it doesn't fail, update checking still adds around 6mb on average
        - QWIDGETMAX is locked behind a pointless 4mb ram library
        - transition to lazy loading instead of loading everything all at once (about/cat dialogs finished)
        - themes take up nearly 2mb of ram (is loading the logo the biggest issue? only 14kb size)
TODO: editing feature changes:
        - text overlay (this would be awesome)
        - "replace/add audio" -> add prompt to change volume of incoming file (always? as separate action? while holding modifier?)
        - "add audio" -> option to literally add it as an audio track (with ffmpeg, not libvlc/add_slave)
        - converting mp4 to gif
        - add "compress" option
        - add "speed" option (this is already implemented for audio files through the resize function)
        - do math to chain audio-resizes to get around ffmpeg atempo 0.5-2.0 limitation (can be chained in single command)
        - implement more image edits?
        - ability to "hold" fades
TODO: should probe files be written/read as bytes? how much faster would that be?
        - `json.detect_encoding()` would still be needed for actually parsing the files into JSON


TODO: MEDIUM PRIORITY:
DPI/scaling support
further polish cropping
confirm/increase stability for videos > 60fps (not yet tested)
trimming-support for more obscure formats
implement filetype associations
system tray icon's menu is just blank on linux
high-precision progress bar on non-1x speeds

TODO: LOW PRIORITY:
resize-snapping does not work on linux
implement concatenation for audio files
further reduce RAM usage
"Restore Defaults" button in settings window
see update change logs before installing
add way to distinguish base and forked repos
ability to skip updates
far greater UI customization
figure out the smallest feasible ffmpeg executable we can use without sacrificing major edit features (ffmpeg.dll?)
ability to continue playing media while minimized to system tray
forwards/backwards buttons currently only work when pressed over the player
ability to limit combination-edits (adding/replacing audio) to the shortest input (this exists in ffmpeg but breaks often)
lazy concatenate dialog seems to have a memory leak (it does not free up QVideoList's memory after deletion)
dropping files over taskbar button doesn't work


KNOWN ISSUES:
    Likely unfixable:
        frame-seeking near the very end of a video rarely works (set_time()/set_position()/next_frame() make no difference)
        NOTE: ^ this was greatly improved (but not fully fixed) in libvlc 3.0.19
    Low priority:
        manually entering single %'s in config file for path names somehow ignores all nested folders
        partially corrupt videos have unusual behavior when frame-seeking corrupted parts <- use player.next_frame()?
        frame-seeking only a handful of frames after a video finishes and trying to play again sometimes causes brief freeze
        player becomes slightly less responsive after repeatedly minimizing to system tray (noticable fraction-of-a-second delay when navigating)
        resizing videos doesn't actually stretch them? or... it does? very strange behavior with phantom black bars that differ from player to player
        rarely, concatenated videos will have a literal missing frame between clips, causing PyPlayer's background to appear for 1 frame
        abnormally long delay opening first video after opening extremely large video (longer delay than in VLC) -> delay occurs at player.set_media
        output-name lineEdit's placeholder text becomes invisible after setting a theme and then changing focus
        libVLC does NOT like it when you disable the video track. lots of bugs
    Medium priority:
        resizing an audio file rarely stalls forever with no error (works upon retry) NOTE: might have been fixed with new `Edit` class
        rotating/flipping video rarely fails for no reason (works upon retry) NOTE: might have been fixed with new `Edit` class
        videos with replaced/added audio tracks longer than the video themselves do NOT concatenate correctly (audio track freaks ffmpeg out)
        repeatedly going into fullscreen on a higher DPI/scaled monitor results ruins the controls (general DPI/scaling support is high priority)
        audio replacement/addition sometimes cuts out audio 1 second short. keyframe related? corrupted streams (not vlc-specific)?
    Moderately high priority:
        .3gp, .ogv, and .mpg files do not trim correctly
    Cannot reproduce consistently:
        volume gain suddenly changes after extended use
        spamming the cycle buttons may rarely crash to desktop with no error NOTE: might have been fixed with 3/06/24 commit
        spamming the cycle buttons may rarely cause the UI to desync in a way that `high_precision_progress_thread()` seemingly can't detect
        player's current visible frame doesn't change when navigating (<- and ->) after video finishes until it's unpaused (used to never happen)
        scrubbing slider and sharply moving mouse out of window while releasing causes video to not unpause until scrubbed again (rare)
        clicking on the progress bar will update the video without moving the progress bar (very rare, may be bottlenecking issue)
        fullscreen mode becomes partially unresponsive -> no idle timer, no passthrough on dockControls (very rare, may be bottlenecking issue)
        system tray icon suddenly crashes -> "OSError: exception: access violation writing 0x0000000000000007" (extremely rare, unknown cause)
        random freeze and crash to desktop after otherwise successful ffmpeg operation (rare, never leaves any error)
        libvlc randomly jumps to a very, very low progress after otherwise successful navigation (very rare, unknown cause)
'''

from __future__ import annotations

import config
import widgets
import qtstart
import constants
import qthelpers
from constants import SetProgressContext
from bin.window_pyplayer import Ui_MainWindow
from bin.window_settings import Ui_settingsDialog
from util import (                                      # direct import time-sensitive utils for a very small optimization
    add_path_suffix, ffmpeg, ffmpeg_async, foreground_is_fullscreen, get_font_path,
    get_hms, get_PIL_Image, get_ratio_string, get_unique_path, get_verbose_timestamp,
    open_properties, remove_dict_value, remove_dict_values, sanitize, scale, setctime,
    suspend_process, kill_process, file_is_hidden
)

import os
import gc
import sys
import math
import glob
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
from vlc import State
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
# self.childAt(x, y) | self.underMouse() -> bool
# NOTE: QtWidgets.QToolTip.hideText/showText/setPalette/setFont (showText is laggy)
# NOTE: app.setQuitOnLastWindowClosed(False) -> app.quit() (app.aboutToQuit.connect)
# NOTE: Plugins (QPluginLoader/QLibrary): Felgo (really good), QSkinny (lightweight), Advanced Docking System (laggy but pure Qt)
#                                         Qt Pdf Viewer Library, CircularSlider (QML), GitQlient, All KDE Community plugins
# NOTE: Useful: QReadWriteLock/QLockFile, QStorageInfo, QStandardPaths, QFileSystemWatcher, QMimeData (for dragging)
# NOTE: Potentially useful: QMutex, QLocale, QStateMachine(?), QShow/HideEvent, QFileSystemWatcher, QPdfDocument (paid?)
# NOTE: Interesting: QFileselector, QCamera, QEventLoop[Locker], QWinEventNotifier, QColorTransform(??), QSharedMemory (inter-process)
# NOTE: Interesting but useless in Python: QSaveFile, QRandomGenerator, QTemporaryDir/File, QJsonObject


# -------------------------------------------
# Additional media-related utility functions
# -------------------------------------------
def probe_files(*files: str, refresh: bool = False, write: bool = True, retries: int = 0) -> dict[str, dict]:
    ''' Probes an indeterminant number of `files` and returns a dictionary of
        `{path: probe_dictionary}` pairs. All files are probed concurrently, but
        this function does not return until all probes are completed. Files that
        fail are simply not included.

        This function is similar to the probing process in `self.open()`
        (but is not used there for performance reasons) - by default, it will
        create/validate/reuse probe files. However, if `refresh` is True, a new
        probe will always be generated even if the probe file already exists.
        If `write` is False, any new probes will not be written to a file. '''

    try:
        logging.info(f'Manually probing files: {files} (refresh={refresh})')
        probes: dict[str, dict] = {}
        processes: list[tuple[str, str, subprocess.Popen]] = []

        is_windows = constants.IS_WINDOWS
        if not is_windows:
            import shlex                                # have to pass commands as list for linux/macos (stupid)
            cmd_parts = shlex.split(f'"{FFPROBE}" -show_format -show_streams -of json "output"')

        # begin probe-process for each file and immediately jump to the next file
        for file in files:
            if file in probes or not exists(file):
                continue

            stat = os.stat(file)
            probe_file = f'{constants.PROBE_DIR}{sep}{os.path.basename(file)}_{stat.st_mtime}_{stat.st_size}.txt'
            probe_exists = exists(probe_file)
            if probe_exists:
                if refresh:                             # NOTE: if `refresh` is True and `write` is False, existing...
                    try: os.remove(probe_file)          # ...probe files will be deleted without being replaced
                    except: logging.warning('(!) FAILED TO DELETE UNWANTED PROBE FILE: ' + format_exc())
                    probe_exists = False
                else:
                    with open(probe_file, 'r', encoding='utf-8') as probe:
                        try:
                            probe_data = parse_json(probe.read())
                            if not probe_data:
                                raise AssertionError('probe returned no data')
                            probes[file] = probe_data
                        except:
                            probe.close()
                            logging.info('(?) Deleting potentially invalid probe file: ' + probe_file)
                            try: os.remove(probe_file)
                            except: logging.warning('(!) FAILED TO DELETE POTENTIALLY INVALID PROBE FILE: ' + format_exc())
                            probe_exists = False

            if not probe_exists:
                if is_windows:
                    cmd = f'"{FFPROBE}" -show_format -show_streams -of json "{file}"'
                else:                                   # ^ do NOT use ">" here since we need to read stdout
                    cmd = cmd_parts[:]                  # copy list and replace final element with our destination
                    cmd[-1] = file                      # do NOT put quotes around this
                processes.append(
                    (
                        file,
                        probe_file,
                        subprocess.Popen(
                            cmd,
                            text=True,                  # decodes stdout into text rather than a byte stream
                            encoding='utf-8',           # use ffmpeg/ffprobe's encoding so `text=True` doesn't crash for paths w/ scary characters
                            errors='ignore',            # drop bad characters when there's an encoding error (which won't matter for our usecase)
                            stdout=subprocess.PIPE,     # don't use `shell=True` for the same reason as above
                            startupinfo=constants.STARTUPINFO
                        )                               # ^ hides the command prompt that appears w/o `shell=True`
                    )
                )

        # for any files that did not have pre-existing probe files, wait until...
        # ...their processes are complete and read output directly from the process
        for file, probe_file, process in processes:
            try:
                out, err = process.communicate()        # NOTE: this is where errors happen on filenames with the wrong encoding above
                probe_data = parse_json(out)
                if not probe_data:
                    raise AssertionError('probe returned no data')
                probes[file] = probe_data
                if write:                               # manually write probe to file
                    with open(probe_file, 'w', encoding='utf-8') as probe:
                        probe.write(out)                    # ^ DON'T use `errors='ignore'` here. if we somehow error out here, i'd rather know why
            except:
                logging.warning(f'(!) {file} could not be correctly parsed by FFprobe: {format_exc()}')
                show_on_statusbar(f'{file} could not be correctly parsed by FFprobe.')
        return probes

    # if we're low on RAM, wait one second and try again
    except OSError:                                     # "[WinError 1455] The paging file is too small for this operation to complete"
        logging.warning(f'(!) OSError while probing files: {format_exc()}')
        if retries:
            show_on_statusbar('(!) Not enough RAM to probe files. Trying again...')
            sleep(1)
            return probe_files(*files, refresh, write, retries - 1)
        else:
            show_on_statusbar('(!) Not enough RAM to probe files. Giving up.')
            return {}


def get_audio_duration(file: str) -> float:
    ''' Lightweight way of getting the duration of an audio `file`.
        Used for instances where we need ONLY the duration. '''
    try:
        try:                                            # https://pypi.org/project/tinytag/0.18.0/
            return TinyTag.get(file, tags=False).duration
        except:                                         # TinyTag is lightweight but cannot handle everything
            import music_tag                            # only import music_tag if we absolutely need to
            return music_tag.load_file(file)['#length'].value
    except:                                             # this is to handle things that wrongly report as audio, like .ogv files
        log_on_statusbar('(?) File could not be read as an audio file (not recognized by TinyTag or music_tag)')
        return 0.0


@contextmanager
def get_image_data(path: str, extension: str = None):
    # TODO I don't need this anymore and should probably avoid using it at all.
    try:
        if exists(path): image_data = get_PIL_Image().open(path, formats=(extension,) if extension else None)
        else:            image_data = get_PIL_Image().fromqpixmap(image_player.art)
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
            if good_ext == '':
                good_ext = '.png'
            temp_path = final_path + good_ext
            yield temp_path
        else:
            yield final_path
    finally:
        if temp_path != '':
            try: os.replace(temp_path, final_path)
            except: logging.warning('(!) FAILED TO RENAME TEMPORARY IMAGE PATH' + format_exc())


def splitext_media(
    path: str,
    valid_extensions: tuple[str] = constants.ALL_MEDIA_EXTENSIONS,
    invalid_extensions: tuple[str] = constants.ALL_MEDIA_EXTENSIONS,
    *,
    strict: bool = True,
    period: bool = True
) -> tuple[str, str]:
    ''' Split the extension from a `path` if the extension is within a
        list of `valid_extensions`. If not, the basename is returned with an
        empty extension. The extension will be lowercase. If `period` is True,
        the preceding period will be included (i.e. ".mp4"). If `strict` is
        False, an unknown extension can still be returned intact if:

        1. It is not within a list of `invalid_extensions`
        2. It is 6 characters or shorter
        3. It contains at least one letter
        4. It does not contain anything other than letters and numbers

        NOTE: `strict` must be provided as a keyword argument.

        NOTE: `valid_extensions` is evaluated first. `invalid_extensions` should
        rarely be changed, but may be passed as None/False/"" if desired. '''

    base, ext = os.path.splitext(path)
    ext = ext.lower()

    # if no ext to begin with, return immediately
    if not ext:
        return path, ''

    # if `strict` is False and ext is invalid, only return if ext is >6 characters
    if ext not in valid_extensions:
        if strict or len(ext) > 6 or ext in (invalid_extensions or tuple()):
            return base, ''

        # verify ext has at least one letter and no symbols
        has_letters = False
        for c in ext[1:]:
            if c.isalpha():
                has_letters = True
            elif not c.isdigit():
                return base, ''
        if not has_letters:
            return base, ''

    # return extension with or without preceding period (".mp4" vs "mp4")
    if period:
        return base, ext
    return base, ext[1:]


def close_handle(handle, delete: bool):                 # i know they're not really handles but whatever
    ''' Closes a file-object `handle` and attempts
        to `delete` its associated path. '''
    handle.close()
    if delete and exists(handle.name):
        try: os.remove(handle.name)
        except: logging.warning(f'(!) Failed to delete dummy file at final destination ({handle.name}): {format_exc()}')


#def correct_misaligned_formats(audio, video) -> str:    # this barely works
#    _, vext = os.path.splitext(video)
#    abase, aext = os.path.splitext(audio)
#    if vext != aext and not (vext == '.mp4' and aext == '.mp3'):
#        new_audio = f'{abase}{vext}'                    # create new audio filename if extensions don't match
#        logging.info(f'Formats misaligned between audio "{audio}" and video "{video}". Correcting audio to "{new_audio}"')
#        ffmpeg(None, f'-i "{audio}" "{new_audio}"')     # convert audio to video's format
#        audio = new_audio                               # replace bad audio filename
#    else: logging.info(f'Formats aligned between audio "{audio}" and video "{video}".')
#    return audio


# ---------------------
# Editing helper class
# ---------------------
class Edit:
    ''' A class for handling, executing, and tracking edits in progress. '''

    __slots__ = (
        'dest', 'temp_dest', 'process', '_is_paused', '_is_cancelled',
        '_threads', 'has_priority', 'frame_rate', 'frame_count',
        'audio_track_titles', 'operation_count', 'operations_started', 'frame',
        'value', 'text', 'percent_format', 'start_text', 'override_text'
    )

    def __init__(self, dest: str = ''):
        self.dest = dest
        self.temp_dest = ''
        self.process: subprocess.Popen = None
        self._is_paused = False
        self._is_cancelled = False
        self._threads = 0
        self.has_priority = False
        self.frame_rate = 0.0
        self.frame_count = 0
        self.audio_track_titles: list[str] = []
        self.operation_count = 1
        self.operations_started = 0
        self.frame = 0
        self.value = 0
        self.text = 'Saving'
        self.percent_format = '(%p%)'
        self.start_text = 'Saving'
        self.override_text = False


    @property
    def is_paused(self) -> bool:
        ''' Use `self.pause()` to safely alter this property. '''
        return self._is_paused


    @property
    def is_cancelled(self) -> bool:
        ''' Use `self.cancel()` to safely cancel. '''
        return self._is_cancelled


    def pause(self, paused: bool = None) -> bool:
        ''' Suspends or resumes the edit's FFmpeg process. If `paused` is
            not provided, the current pause-state is toggled instead. '''

        # if `paused` is not provided, just toggle our current pause state
        will_pause = (not self._is_paused) if paused is None else paused

        # NOTE: on Windows, suspending a process STACKS!!! i.e. if you suspend a process...
        # ...twice, you must resume it twice -> ONLY suspend if `self._is_paused` will change
        if will_pause != self._is_paused:
            self._is_paused = will_pause                # ↓ returns None if process hasn't terminated yet
            if self.process and self.process.poll() is None:
                suspend_process(self.process, suspend=will_pause)
                if self.has_priority:
                    self.set_progress_bar(value=self.value)

        return will_pause


    def cancel(self):
        ''' Cancels this edit by killing its current FFmpeg process.
            Resumes process first if it was previously suspended. '''
        self._is_cancelled = True
        if constants.IS_WINDOWS:                        # NOTE: don't have to actually unpause on Windows...
            self._is_paused = False                     # ...since we don't rely on stdout buffering
        else:
            self.pause(paused=False)


    def give_priority(self, update_others: bool = True, ignore_lock: bool = False, conditional: bool = False):
        ''' Refreshes progress bar/taskbar to this edit's values if we've been
            given priority over updating the progress bar. If `update_others`
            is True, all other edits in `gui.edits_in_progress` will set their
            `has_priority` property to False. This method returns immediately
            if `gui.lock_edit_priority` is True and `ignore_lock` is False,
            or if `conditional` is True and any other edit has priority. '''

        # return immediately if desired
        if gui.lock_edit_priority and not ignore_lock:
            return
        if conditional:
            for edit in gui.edits_in_progress:
                if edit.has_priority:
                    return

        # ensure priority is disabled on everything else
        if update_others:
            for edit in gui.edits_in_progress:
                edit.has_priority = False

        self.has_priority = True
        if self.frame == 0:                             # assume we haven't parsed any output yet
            gui.set_save_progress_value_and_format_signal.emit(0, self.start_text)
            refresh_title()
        else:
            self.set_progress_bar(value=self.value)
        gui.set_save_progress_max_signal.emit(100 if self.frame_count else 0)


    def get_progress_text(self, frame: int = 0, simple: bool = False) -> str:
        ''' Returns `self.text` surrounded by relevant information, e.g. "2
            edits in progress - Trimming [1/3] (25%)". Manually replaces %v/%m
            with `frame`/`self.frame_count`. If `self.frame_count` is 0, "?" is
            used instead. If `simple` is provided, a standardized format that
            ignores edit counts/percent formats/text overrides is returned. '''

        if simple:
            text = self.text
            percent_format = f'({self.value}%)'
        elif self.override_text:
            return self.text
        else:
            percent_format = self.percent_format
            save_count = len(gui.edits_in_progress)
            if save_count > 1:
                text = f'{save_count} edits in progress - {self.text}'
            else:
                text = self.text

        # handle operation count and pause symbol for this edit
        operation_count = self.operation_count
        if operation_count > 1:
            pause = '𝗜𝗜, ' if self._is_paused else ''
            text = f'{text} [{pause}{self.operations_started}/{operation_count}] {percent_format}'
        else:
            pause = ' [𝗜𝗜] ' if self._is_paused else ' '
            text = f'{text}{pause}{percent_format}'

        # return with `QProgressBar` variables manually replaced TODO: never used, no plans -> why even bother?
        return text.replace('%v', str(frame)).replace('%m', str(self.frame_count or '?'))


    def set_progress_bar(self, frame: int = None, value: int = None) -> int:
        ''' Sets the progress bar/taskbar button to `frame`/`Edit.frame_count`.
            Updates the progress bar's text and puts the average progress of all
            edits/operations in the titlebar. Returns the new percentage. '''
        if value is None:
            value = int((frame / max(1, self.frame_count)) * 100)
        self.value = value
        self.frame = frame or self.frame

        # update progress bar, taskbar, and titlebar with our current value/text
        if self.has_priority:
            gui.set_save_progress_value_and_format_signal.emit(value, self.get_progress_text(frame))
            if constants.IS_WINDOWS and settings.checkTaskbarProgressEdit.isChecked():
                gui.taskbar_progress.setValue(value)
            refresh_title()

        return value


    def ffmpeg(
        self,
        infile: str,
        cmd: str,
        outfile: str = None,
        text: str = None,
        start_text: str = None,
        percent_format: str = None,
        text_override: str = None,
        auto_map_tracks: bool = True,
        audio_track_titles: list[str] = None
    ) -> str:
        ''' Executes an FFmpeg `cmd` on `infile` and outputs to `outfile`,
            showing a progress bar on both the statusbar and the taskbar icon
            (on Windows) by parsing FFmpeg's output. "%in" and "%out" will be
            replaced within `cmd` if provided. "%out" will be appended to the
            end of `cmd` automatically if needed. If `auto_map_tracks` is True,
            "-map 0" will be inserted before "%out" if "-map" is not present.
            the appropriate metadata arguments for `audio_track_titles` (or
            `self.audio_track_titles`) will also be inserted.

            NOTE: `infile` and "%in" do not necessarily need to be included, but
            if you don't providing `infile`, you shouldn't provide "%in" either.
            NOTE: If `outfile` is not provided, `infile` is overwritten instead.
            If neither was provided, an exception is raised.
            NOTE: This method will only update the progress bar if this edit
            has priority. Priority may change mid-operation and is gained
            whenever `len(gui.edits_in_progress) == 1`.

            `Edit.frame_rate` is a hint for the progress bar as to what frame
            rate to use when normal frame-output from FFmpeg is not available
            (such as for audio files) and we must convert timestamp-output to
            frames instead. If not provided, `gui.frame_rate` is used.

            `Edit.frame_count` is the target value that is used to calculate
            our current progress percentage. If not provided and this operation
            has priority, the progress bar switches to an indeterminate bar.

            `text` specifies the main text that will appear on the progress bar
            (while this edit has priority), surrounded by relevant information
            such as how many other edits are in progress and how many operations
            this edit has left. `start_text` (if provided) overrides `text`
            until the first progress update is parsed, and `percent_format` is
            the suffix that will be added to the end of `text`. It does not have
            to be an actual percentage. `QProgressBar`'s format variables:
            - %p - percent complete
            - %v - raw current value (frame)
            - %m - raw max value (frame count, or "?" if frame count is 0).

            If `text_override` is provided (and this edit has priority), `text`,
            `percent_format`, and `start_text` are all ignored, no other
            information is added, and `Edit.override_text` is set to True.

            NOTE: Temporary paths will be locked/unlocked if `infile` is
            already locked when you call this method.
            NOTE: This method used to optionally handle locking/unlocking and
            cleanup, but these features have since been removed. Please handle
            these things before/after calling this method (see: `gui._save()`).

            Returns the actual final output path. '''

        start = get_time()
        locked_files = gui.locked_files
        edits_in_progress = gui.edits_in_progress
        had_priority = len(edits_in_progress) == 1
        is_windows = constants.IS_WINDOWS
        logging.info(f'Performing FFmpeg operation (infile={infile} | outfile={outfile} | cmd={cmd})')

        # set title/text-format-related properties based on parameters and existing values
        self.override_text = bool(text_override)
        self.start_text = start_text or text_override or self.get_progress_text()
        self.text = text_override or text or self.text
        self.audio_track_titles = audio_track_titles or self.audio_track_titles
        if percent_format is not None:
            self.percent_format = percent_format

        # prepare the progress bar/taskbar/titlebar if no other edits are active
        if had_priority:
            self.has_priority = True                                # ↓ must set value to actually show the progress bar
            gui.set_save_progress_value_and_format_signal.emit(0, self.start_text)
            gui.set_save_progress_max_signal.emit(100 if self.frame_count else 0)
            gui.set_save_progress_visible_signal.emit(True)
            if is_windows and settings.checkTaskbarProgressEdit.isChecked():
                gui.taskbar_progress.reset()
            refresh_title()

        # validate `infile` if it was provided
        if infile:
            assert exists(infile), f'`infile` "{infile}" does not exist.'
            if not outfile:
                outfile = infile
                logging.info(f'`outfile` not provided, setting to `infile`: {infile}')
        elif not outfile:
            raise AssertionError('Both `infile` and `outfile` are invalid. This FFmpeg command is impossible.')

        try:
            # create temp file if `infile` and `outfile` are the same (ffmpeg can't edit files in-place)
            editing_in_place = False
            if infile:
                if infile == outfile:                               # NOTE: this happens in `gui._save()` w/ multiple operations
                    editing_in_place = True
                    temp_infile = add_path_suffix(infile, '_temp', unique=True)
                    if infile in locked_files:                      # if `infile` is already locked, lock the temp...
                        locked_files.add(temp_infile)               # ...path too, regardless of our `lock` parameter
                    os.rename(infile, temp_infile)                  # rename `infile` to our temporary name
                    logging.info(f'Renamed "{infile}" to temporary FFmpeg file "{temp_infile}"')
                else:
                    temp_infile = infile
            else:                                                   # no infile provided at all, so no temp path either
                temp_infile = ''

            # replace %in and %out with their respective (quote-surrounded) paths
            if '%out' not in cmd:                                   # ensure %out is present so we have a spot to insert `outfile`
                cmd += ' %out'

            # insert `-map 0` so all tracks are "mapped" to the final output
            # TODO: ffprobe can't parse track titles (LOL), so we need mediainfo if we want...
            # ...to get them on the fly, especially for edits like concatenation. incredible.
            if auto_map_tracks and '-map ' not in cmd:
                out = cmd.find(' %out')
                if self.audio_track_titles:                         # ffmpeg drops the track titles, so insert garbage metadata arguments
                    titles = ' '.join(                              # ↓ replace empty titles with something generic, like "Track 2"
                        f'-metadata:s:a:{index} title="{title.strip() or f"Track {index + 1}"}"'
                        for index, title in enumerate(self.audio_track_titles)
                    )
                    cmd = f'{cmd[:out]} -map 0 {titles}{cmd[out:]}'
                else:
                    cmd = f'{cmd[:out]} -map 0{cmd[out:]}'

            # run final ffmpeg command
            try:
                self._threads = settings.spinFFmpegThreads.value() if settings.checkFFmpegThreadOverride.isChecked() else 0
                process: subprocess.Popen = ffmpeg_async(
                    cmd=cmd.replace('%in', f'"{temp_infile}"').replace('%out', f'"{outfile}"'),
                    priority=settings.comboFFmpegPriority.currentIndex(),
                    threads=self._threads
                )
            except:
                logging.error(f'(!) FFMPEG FAILED TO OPEN: {format_exc()}')
                raise                                               # raise anyway so cleanup can occur

            self.process = process
            self.temp_dest = outfile
            self.operations_started += 1

            # update progress bar using the 'frame=???' lines from ffmpeg's stdout until ffmpeg is finished
            # https://stackoverflow.com/questions/67386981/ffmpeg-python-tracking-transcoding-process/67409107#67409107
            # TODO: 'total_size=', time spent, and operations remaining could also be shown (save_progress_bar.setFormat())
            frame_rate = max(1, self.frame_rate or gui.frame_rate)  # used when ffmpeg provides `out_time_ms` instead of `frame`
            use_outtime = True
            last_frame = 0
            lines_read = 0
            lines_to_log = []
            while True:
                if process.poll() is not None:                      # returns None if process hasn't terminated yet
                    break

                # if we're paused, continue sleeping but refresh title every second if necessary
                while self._is_paused:
                    sleep(1.0)
                    if len(edits_in_progress) > 1 and self.has_priority:
                        refresh_title()

                # edit cancelled -> kill this thread's ffmpeg process and cleanup
                if self._is_cancelled:
                    raise AssertionError('Cancelled.')

                # check if this thread lost priority
                if had_priority and not self.has_priority:
                    had_priority = False

                # check if this thread was manually set to control the progress bar
                if not had_priority and self.has_priority:
                    had_priority = True
                    self.give_priority()

                # check if this thread should automatically start controlling the progress bar, then...
                # ...sleep before parsing output -> sleep longer (update less frequently) while not visible
                if self.has_priority:
                    sleep(0.5)
                elif len(edits_in_progress) == 1:                   # NOTE: this doesn't actually get reached anymore i think
                    logging.info('(?) Old auto-priority-update code reached. This probably shouldn\'t be possible.')
                    had_priority = True
                    self.give_priority()
                    sleep(0.5)
                else:
                    sleep(0.5)                                      # split non-priority sleep into two parts so users can...
                    if not self.has_priority:                       # ...switch priority w/o too much delay before updates resume
                        sleep(0.5)

                # seek to end of current stdout output then back again to calculate how much data...
                # ...we'll need to read (we have to do it this way to get around pipe buffering)
                if is_windows:
                    start_index = process.stdout.tell()
                    process.stdout.seek(0, 2)
                    end_index = process.stdout.tell()
                    try:
                        process.stdout.seek(start_index, 0)         # seeking back sometimes throws an error?
                        progress_lines = process.stdout.read(end_index - start_index).split('\n')
                    except OSError:
                        logging.warning(f'(!) Failed to seek backwards from index {end_index} to index {start_index} in FFmpeg\'s stdout pipe, retrying...')
                        continue
                    except:
                        logging.warning('(!) Unexpected error while seeking or reading from FFmpeg\'s stdout pipe: ' + format_exc())
                        progress_lines = []

                # can't seek in streams on linux -> call & measure readline()'s delay until it buffers
                # NOTE: this is WAY less efficient and updates noticably slower when sleeping for the same duration. too bad lol
                else:
                    progress_lines = []
                    while process.poll() is None:                   # ensure we don't try to read a new line if process already ended
                        line_read_start = get_time()
                        progress_lines.append(process.stdout.readline().strip())
                        if not progress_lines[-1] or get_time() - line_read_start > 0.05:
                            break

            # >>> parse ffmpeg output <<<
                # loop over new stdout output without waiting for buffer so we can read output in...
                # ...batches and sleep between loops without falling behind, saving a lot of resources
                new_frame = last_frame
                for progress_line in progress_lines:
                    lines_read += 1
                    lines_to_log.append(f'FFmpeg output line #{lines_read}: {progress_line}')
                    if not progress_line:
                        logging.info('FFmpeg output a blank progress line to STDOUT, leaving progress loop...')
                        break

                    # check for common errors
                    if progress_line[-6:] == 'failed':              # "malloc of size ___ failed"
                        if 'malloc of size' in progress_line:
                            raise AssertionError(progress_line)
                    elif 'do not match the corresponding output link' in progress_line:
                        raise AssertionError(progress_line)         # ^ concating videos with different dimensions

                    # normal videos will have a "frame=" progress string
                    if progress_line[:6] == 'frame=':
                        frame = min(int(progress_line[6:].strip()), self.frame_count)
                        if last_frame == frame and frame == 1:      # specific edits will constantly spit out "frame=1"...
                            use_outtime = True                      # ...for these scenarios, we should ignore frame output
                        else:
                            use_outtime = False                     # if we ARE using frames, don't use "out_time_ms" (less accurate)
                            new_frame = frame

                    # ffmpeg usually uses "out_time_ms" for audio files
                    elif use_outtime and progress_line[:12] == 'out_time_ms=':
                        try:
                            seconds = int(progress_line.strip()[12:-6])
                            new_frame = min(int(seconds * frame_rate), self.frame_count)
                        except ValueError:
                            pass

                # update progress bar to latest new frame (so we don't spam updates while parsing stdout)
                if new_frame != last_frame:
                    self.set_progress_bar(new_frame)
                last_frame = new_frame

                # batch-log all our newly read lines at once
                if lines_to_log:
                    progress_lines = '\n'.join(lines_to_log)
                    logging.info(f'New FFmpeg output from {self}:\n{progress_lines}')
                    lines_to_log.clear()

            # terminate process just in case ffmpeg got locked up at the end
            try: process.terminate()
            except: pass

            # cleanup temp file, if needed (editing in place means we had to rename `infile`)
            if editing_in_place:
                qthelpers.deleteTempPath(temp_infile)

            log_on_statusbar(f'FFmpeg operation succeeded after {get_verbose_timestamp(get_time() - start)}.')
            return outfile

        except Exception as error:
            if lines_to_log:
                progress_lines = '\n'.join(lines_to_log)
                logging.info(f'Final FFmpeg output leading up to error {self}:\n{progress_lines}')

            if str(error) == 'Cancelled.':
                log_on_statusbar('Cancelling...')
                logging.info(f'FFmpeg operation cancelled after {get_time() - start:.1f} seconds. Cleaning up...')
            else:
                log_on_statusbar(f'(!) FFmpeg operation failed after {get_verbose_timestamp(get_time() - start)}: {format_exc()}')

            # TODO: is there ever a scenario we DON'T want to kill ffmpeg here? doing this lets us delete `temp_infile`
            # TODO: add setting to NOT delete `temp_infile` on error? (here + `self._save()`)
            if self.process:
                kill_process(process)           # aggressively terminate ffmpeg process in case it's still running
            if editing_in_place:
                qthelpers.deleteTempPath(temp_infile, 'FFmpeg file')
            raise                               # raise exception anyway (we'll still go to the finally-statement)

        finally:
            if editing_in_place:                # always unlock our temporary path if necessary
                try:
                    locked_files.discard(temp_infile)
                except:
                    pass


class Undo:
    __slots__ = 'type', 'label', 'description', 'data'

    def __init__(self, type_: constants.UndoType, label: str, description: str, data: dict):
        self.type = type_
        self.label = label
        self.description = description
        self.data = data

        # TODO: add setting for max undos?
        if len(gui.undo_dict) > 50:
            for key in tuple(gui.undo_dict.items())[50:]:
                try: del gui.undo_dict[key]
                except: pass

    # TODO: should we do this here, in `gui.refresh_undo_menu`, or save lambdas as a property (`undo.action()`)?
    def execute(self):
        ''' Uses `self.data` to undo an action as defined by `self.type`.
            If successful, we remove ourselves from `gui.undo_dict`. '''
        try:
            if self.type == constants.UndoType.RENAME:
                if gui.undo_rename(self):
                    remove_dict_value(gui.undo_dict, self)
        except:
            log_on_statusbar(f'(!) Unexpected error while attempting undo: {format_exc()}')


# ---------------------
# Main GUI
# ---------------------
class GUI_Instance(QtW.QMainWindow, Ui_MainWindow):

    # Custom signals MUST be class variables
    # NOTE: avoid directly emitting signals prefixed with _ if possible
    _open_cleanup_signal = QtCore.pyqtSignal()
    _open_signal = QtCore.pyqtSignal(dict)
    _open_external_command_signal = QtCore.pyqtSignal(str)
    restart_signal = QtCore.pyqtSignal()
    force_pause_signal = QtCore.pyqtSignal(bool)
    restore_tracks_signal = QtCore.pyqtSignal(bool)
    concatenate_signal = QtCore.pyqtSignal(QtW.QAction, list)
    show_ffmpeg_warning_signal = QtCore.pyqtSignal(QtW.QWidget)
    show_trim_dialog_signal = QtCore.pyqtSignal()
    update_progress_signal = QtCore.pyqtSignal(int)
    refresh_title_signal = QtCore.pyqtSignal()
    set_save_progress_visible_signal = QtCore.pyqtSignal(bool)
    set_save_progress_max_signal = QtCore.pyqtSignal(int)
    set_save_progress_value_signal = QtCore.pyqtSignal(int)
    set_save_progress_format_signal = QtCore.pyqtSignal(str)
    set_save_progress_value_and_format_signal = QtCore.pyqtSignal(int, str)
    disable_crop_mode_signal = QtCore.pyqtSignal(bool)
    handle_updates_signal = QtCore.pyqtSignal(bool)
    _handle_updates_signal = QtCore.pyqtSignal(dict, dict)
    popup_signal = QtCore.pyqtSignal(dict)
    log_on_statusbar_signal = QtCore.pyqtSignal(str)

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.setupUi(self)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)             # this allows easier clicking off of lineEdits
        self.save_progress_bar = QtW.QProgressBar(self.statusbar)
        self.dialog_settings = qthelpers.getDialogFromUiClass(Ui_settingsDialog, flags=Qt.WindowStaysOnTopHint)
        if not constants.IS_WINDOWS:                                # settings dialog was designed around Windows UI
            self.dialog_settings.resize(self.dialog_settings.tabWidget.sizeHint().width() + 32,
                                        self.dialog_settings.height())
        self.icons = {
            'window':            QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}logo.ico'),
            'settings':          QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}settings.png'),
            'play':              QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}play.png'),
            'pause':             QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}pause.png'),
            'stop':              QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}stop.png'),
            'restart':           QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}restart.png'),
            'x':                 QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}x.png'),
            'loop':              QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}loop.png'),
            'autoplay':          QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}autoplay.png'),
            'autoplay_backward': QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}autoplay_backward.png'),
            'autoplay_shuffle':  QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}autoplay_shuffle.png'),
            'cycle_forward':     QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}cycle_forward.png'),
            'cycle_backward':    QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}cycle_backward.png'),
            'reverse_vertical':  QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}reverse_vertical.png'),
            'recent':            QtGui.QIcon(f'{constants.RESOURCE_DIR}{os.sep}recent.png'),
        }
        self.setWindowIcon(self.icons['window'])
        app.setWindowIcon(self.icons['window'])


    def setup(self):
        self.first_video_fully_loaded = False   # NOTE: this can reset! use `videos_opened` to !00% know if files were opened this session
        self.closed = False
        self.restarted = False
        self.is_paused = False
        self.close_cancel_selected = False
        self.checking_for_updates = False
        self.timer_id_resize_snap: int = None
        self.close_was_spontaneous = False
        self.was_maximized = False
        self.was_paused = False
        self.crop_restore_state = {}

        self.last_window_size: QtCore.QSize = None
        self.last_window_pos: QtCore.QPoint = None
        self.last_window_pos_non_zero: QtCore.QPoint = None
        self.last_move_time = 0.0
        self.last_cycle_was_forward = True
        self.last_cycle_index: int = None
        self.last_amplify_audio_value = 100
        self.last_resize_media_values: tuple[str, str] = ('50%', '50%')
        self.last_resize_media_base_size: tuple[int, int] = (-1, -1)
        self.last_concat_files: list[str] = []
        self.last_concat_output = ''
        self.last_video_track: int | None = None
        self.last_audio_track: int | None = None
        self.last_subtitle_track: int | None = None
        self.last_subtitle_delay: int | None = None
        self.last_audio_delay: int | None = None
        self.tracks_were_changed = False
        self.invert_next_move_event = False
        self.invert_next_resize_event = False
        self.ignore_next_fullscreen_move_event = False
        self.ignore_next_right_click = False
        self.ignore_next_alt = False
        self.ignore_imminent_restart = False

        self.video = ''
        self.video_original_path = ''
        self.locked_files: set[str] = set()
        self.videos_opened = 0                          # the actual number of files that have been opened this session
        self.last_video = ''                            # the actual last non-edited file played
        self.recent_files: list[str] = []               # the user-friendly list of recent files
        self.recent_edits: list[str] = []               # a list of recent edit output destinations
        self.recent_searches: dict[str, int] = {}       # recent searches in the output textbox and the last selected index for that search
        self.last_search_open_prompt = ''               # the last prompt used to open a file through search
        self.last_search_open_output = ''               # the text in the output textbox following our last search
        self.last_search_open_time = 1.0                # the last time we opened a file through search
        self.last_open_time = 0.0                       # the last time we COMPLETED opening a file (`end`)
        self.move_destinations: list[str] = []          # a list of destinations for the "Move to..." and "Open..." context menu actions
        self.undo_dict: dict[str, Undo] = {}            # filenames with actions that can be undone (renaming, moving, etc.) to undo actions they're associated with
        self.mime_type = 'image'                        # NOTE: defaults to 'image' so that pausing is disabled
        self.extension = 'mp4'                          # NOTE: should be lower and not include the period (i.e. "mp4", not ".MP4")
        self.extension_label = '?'                      # the string used on the titlebar to reprsent the extension
        self.is_gif = False
        self.is_static_image = True
        self.is_audio_with_cover_art = False            # NOTE: True if cover art is present in buffer, even if it's hidden
        self.is_audio_without_cover_art = False
        self.clipboard_image_buffer: bytes = None
        self.cover_art_buffer: bytes = None             # used to store cover art in memory in case we want to load but not display it
        #self.PIL_image = None                          # TODO: store images in memory for quick copying?

        self.delay = 0.0
        self.frame_count = 1                            # the frame count from 0, i.e. 8999 frames (never actually 0 though)
        self.frame_count_raw = 1                        # the actual frame count, i.e. 9000 frames (DON'T use for calculations)
        self.frame_rate = 1
        self.frame_rate_rounded = 1
        self.duration = 0.0
        self.duration_rounded = 0.0
        self.current_time = 1
        self.minimum = 1
        self.maximum = 1
        self.vwidth = 1000
        self.vheight = 1000
        self.vsize = QtCore.QSize(1000, 1000)
        #self.resolution_label = '0x0'
        self.ratio = '0:0'
        self.size_label = '0.00mb'                      # NOTE: do NOT use `self.size` - this is reserved for Qt
        self.stat: os.stat_result = None

        self.frame_override = -1
        self.lock_progress_updates = False
        self.lock_edit_priority = False

        self.open_in_progress = False
        self._open_main_in_progress = False
        self._open_cleanup_in_progress = False
        self.external_command_in_progress = False
        self.player_swap_in_progress = False
        self.edits_in_progress: list[Edit] = []

        self.current_file_is_autoplay = False
        self.shuffle_folder = ''
        self.shuffle_ignore_order = []
        self.shuffle_ignore_unique: set[str] = set()
        self.marked_for_deletion: set[str] = set()
        self.mark_for_deletion_held_down = False
        self.mark_for_deletion_held_down_state = False
        self.shortcuts: dict = None
        self.operations = {}
        self.save_remnants: dict[float, dict] = {}
        self.playback_rate = 1.0
        self.volume_boost = 1
        self.volume_startup_correction_needed = True

        # misc setup
        self.menuRecent.setToolTipsVisible(True)
        self.menuAudio.insertMenu(self.menuAudio.actions()[2], self.menuTrimMode)
        self.menuAudio.insertAction(self.menuAudio.actions()[-1], self.actionResize)
        self.dockControls.setTitleBarWidget(QtW.QWidget(self.dockControls))  # disables QDockWidget's unique titlebar
        self.lineOutput.setProxyWidget(self)                                 # pass output text box's non-essential key events to ourselves
        self.lineOutput.setIgnoredKeys(Qt.Key_Tab)                           # ignore tab presses, we're using them for something else
        self.lineOutput.setIgnoreAll(False)                                  # but DON'T ignore normal stuff (letters, numbers, punctuation)
        self.checkDeleteOriginal.setCheckState(1)                            # default to partially checked (can't be done in QtDesigner, lol)
        self.frameAdvancedControls.setDragTarget(self)
        self.frameCropInfo.setVisible(False)                                 # ensure crop info panel is hidden on startup
        self.dialog_settings.checkContextShowSubmenus.setCheckState(1)       # can't make checkboxes default to partially checked in Qt Designer :(
        for spin in (self.spinHour, self.spinMinute, self.spinSecond, self.spinFrame):
            spin.setProxyWidget(self)

        # setup progress bar embedded within the status bar
        self.statusbar.addPermanentWidget(self.save_progress_bar)            # TODO could QWIDGETMAXSIZE be used to span the widget across the entire statusbar?
        self.save_progress_bar.setMaximum(0)
        self.save_progress_bar.setMaximumHeight(16)
        self.save_progress_bar.setFormat('Saving (%p%)')                     # TODO add "(%v/%m frames)"?
        self.save_progress_bar.setAlignment(Qt.AlignCenter)
        self.save_progress_bar.setSizePolicy(QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Expanding)
        self.save_progress_bar.setCursor(Qt.PointingHandCursor)
        self.save_progress_bar.hide()

        # set custom one-off event handlers for various widgets
        self.sliderVolume.keyPressEvent = self.keyPressEvent                 # pass sliderVolume key presses directly to GUI_Instance
        self.sliderVolume.keyReleaseEvent = self.keyReleaseEvent
        self.sliderProgress.dragEnterEvent = self.vlc.dragEnterEvent         # reuse player's drag-and-drop code for slider
        self.sliderProgress.dropEvent = self.vlc.dropEvent
        self.dockControls.leaveEvent = self.leaveEvent                       # ensures leaving dockControls hides cursor/controls in fullscreen
        self.dockControls.resizeEvent = self.dockControlsResizeEvent         # ensures dockControls correctly hides/shows widgets in fullscreen
        self.dockControls.keyPressEvent = self.keyPressEvent                 # pass dockControls key presses directly to GUI_Instance
        self.dockControls.keyReleaseEvent = self.keyReleaseEvent
        self.dockControls.enterEvent = lambda e: self.dockControls.unsetCursor()
        self.menubar.enterEvent = lambda e: self.menubar.unsetCursor()

        self.buttonTrimStart.contextMenuEvent = self.trimButtonContextMenuEvent
        self.buttonTrimEnd.contextMenuEvent = self.trimButtonContextMenuEvent
        self.buttonExploreMediaPath.contextMenuEvent = self.buttonMediaLocationContextMenuEvent
        self.buttonMarkDeleted.contextMenuEvent = self.buttonMarkDeletedContextMenuEvent
        self.buttonSnapshot.contextMenuEvent = self.buttonSnapshotContextMenuEvent
        self.buttonAutoplay.contextMenuEvent = self.buttonAutoplayContextMenuEvent
        self.buttonNext.contextMenuEvent = self.cycleButtonContextMenuEvent
        self.buttonPrevious.contextMenuEvent = self.cycleButtonContextMenuEvent
        self.menuRecent.contextMenuEvent = self.menuRecentContextMenuEvent
        self.frameProgress.contextMenuEvent = self.frameProgressContextMenuEvent
        self.frameVolume.contextMenuEvent = self.frameVolumeContextMenuEvent
        self.frameVolume.mousePressEvent = self.frameVolumeMousePressEvent
        self.buttonPause.contextMenuEvent = self.buttonPauseContextMenuEvent
        self.buttonPause.mousePressEvent = self.buttonPauseMousePressEvent
        self.statusbar.contextMenuEvent = self.editProgressBarContextMenuEvent
        self.save_progress_bar.mouseReleaseEvent = self.editProgressBarMouseReleaseEvent

        # set default icons for various buttons
        self.buttonPause.setIcon(self.icons['pause'])
        self.buttonLoop.setIcon(self.icons['loop'])
        self.buttonNext.setIcon(self.icons['cycle_forward'])
        self.buttonPrevious.setIcon(self.icons['cycle_backward'])

        # secondary aliases (mostly for other files to use)
        self.player = self.vlc.player
        self.is_trim_mode = lambda: self.trim_mode_action_group.checkedAction() in (self.actionTrimAuto, self.actionTrimPrecise)

        # all possible snapshot button actions and tooltips, ordered by their appearance in the settings
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

        # all possible double-click actions, ordered by their appearance in the settings
        self.double_click_player_actions = (
            self.dialog_settings.exec,
            self.toggle_mute,
            self.actionFullscreen.trigger,
            self.toggle_maximized,
            lambda: self.set_playback_rate(1.0)
        )

        # all possible middle-click actions, ordered by their appearance in the settings
        self.middle_click_player_actions = (
            self.dialog_settings.exec,
            self.stop,
            self.toggle_mute,
            self.actionFullscreen.trigger,
            self.toggle_maximized,
            lambda: self.set_playback_rate(1.0)
        )

        # all possible tray middle-click actions, ordered by their appearance in the settings
        self.middle_click_tray_actions = (
            qtstart.exit,
            self.dialog_settings.exec,
            self.stop,
            self.toggle_mute,
        )

        # create all taskbar-extensions-related widgets for windows 7-11
        self.create_taskbar_controls()

        # HACK: if you switch players at least once, libVLC will no longer be able to...
        # ...track `QVideoPlayer.underMouse()` immediately after a menu is shown???????
        # -> monkeypatch `QMenu` itself to always correct this issue (simple and performant)
        def hideEvent(menu: QtW.QMenu, event: QtGui.QHideEvent):
            QtW.QMenu._hideEvent(menu, event)
            self.vlc.reset_undermouse_state()           # updates `underMouse()` and hides cursor if over player
        QtW.QMenu._hideEvent = QtW.QMenu.hideEvent      # save real hideEvent to separate property
        QtW.QMenu.hideEvent = hideEvent

        self.menuPlayer.addAction('Set player to VLC', lambda: self.set_player('VLC'))
        self.menuPlayer.addAction('Set player to Qt', lambda: self.set_player('Qt'))


    def external_command_interface_thread(
        self,
        cmdpath: str = None,
        once: bool = False,
        delete: bool = True,
        timeout: float = 0
    ):
        ''' Simple interface for detecting and reading cmd.txt files. Used for
            instantly playing new media upon double-click if we're already open
            (cmd.txt contains the path to the media) or closing in preparation
            for an update (cmd.txt contains the word "EXIT").

            NOTE: This can be started multiple times if, for whatever reason,
            you have alternative command files you want to watch for. Just pass
            a `cmdpath` parameter. If `once` is True, this thread will auto-exit
            after its first successful command. If `delete` is True, `cmdpath`
            will be deleted after reading. If `timeout` is greater than 0,
            this thread will auto-exit after `timeout` seconds. '''

        if cmdpath is None: cmdpath = f'{constants.TEMP_DIR}{sep}cmd.{os.getpid()}.txt'
        try: os.makedirs(os.path.dirname(cmdpath))
        except: pass
        try: os.remove(cmdpath)
        except: pass
        logging.info(f'Fast-start connection established. Will listen for commands at {cmdpath}.')
        use_timeout = timeout > 0

        while not self.closed:
            try:
                if exists(cmdpath):
                    self.external_command_in_progress = True
                    self._open_external_command_signal.emit(cmdpath)
                    logging.info(f'(CMD) Command file detected: {cmdpath}')
                    while self.external_command_in_progress and not self.closed:
                        sleep(0.05)
                    if delete:
                        os.remove(cmdpath)
                    if once:
                        break
            except:
                log_on_statusbar(f'(!) EXTERNAL COMMAND INTERFACE FAILED: {format_exc()}')
            finally:
                if use_timeout:
                    timeout -= 0.1
                    if timeout < 0:
                        break
                sleep(0.1)


    # ---------------------
    # >>> EVENTS <<<
    # ---------------------
    def event(self, event: QtCore.QEvent) -> bool:
        ''' A global event callback. Used to detect `windowStateChange` events,
            so we can save/remember the maximized state when necessary. '''
        if event.type() == WindowStateChange:           # alias used for speed
            if not (self.windowState() & Qt.WindowMinimized or self.windowState() & Qt.WindowFullScreen):
                self.was_maximized = bool(self.windowState() & Qt.WindowMaximized)
        return super().event(event)


    def closeEvent(self, event: QtGui.QCloseEvent):     # 'spontaneous' -> X-button pressed, likely not exiting for real
        self.close_cancel_selected = False              # referenced in qtstart.exit()
        self.close_was_spontaneous = event.spontaneous()
        logging.info(f'Closing (spontaneous={event.spontaneous()}).')

        # if user doesn't want to minimize to tray, just exit immediately
        minimize_to_tray = settings.groupTray.isChecked() and settings.checkTrayClose.isChecked()
        force_close = (event.spontaneous() and not minimize_to_tray) or self.tray_icon is None

        # show deletion prompt if we still have files to delete
        if self.marked_for_deletion:
            logging.info(f'The following files are still marked for deletion, opening prompt: {self.marked_for_deletion}')
            choice = self.show_delete_prompt(exiting=force_close or not event.spontaneous())
            if choice == QtW.QMessageBox.Cancel:        # cancel selected, don't close
                self.close_cancel_selected = True       # required in case .close() was called from qtstart.exit()
                logging.info('Close cancelled.')
                return event.ignore()

        # show popup if we still have edits in progress -> cancel all if accepted
        if self.edits_in_progress and (force_close or not event.spontaneous()):
            words = ('this', 'edit') if len(self.edits_in_progress) == 1 else ('these', 'edits')
            choice = qthelpers.getPopupOkCancel(
                title=f'{words[1].capitalize()} still in progress!',
                text=(f'You still have {len(self.edits_in_progress)} {words[1]} in progress.\n'
                      f'Exiting will cancel {words[0]} {words[1]}. Continue?'),
                **self.get_popup_location_kwargs()
            ).exec()
            if choice == QtW.QMessageBox.Cancel:
                self.close_cancel_selected = True       # required in case .close() was called from qtstart.exit()
                logging.info('Close cancelled.')
                return event.ignore()
            self.cancel_all(wait=True)

        self.stop()                                     # stop player
        settings.close()                                # close settings dialog
        self.dockControls.setFloating(False)            # hide fullscreen UI if needed
        logging.info('Player has been stopped.')

        if force_close:
            qtstart.exit(self)
        else:
            if not cfg.minimizedtotraywarningignored:
                if event.spontaneous():                 # only show message if closeEvent was called by OS (i.e. X button pressed)
                    self.tray_icon.showMessage('PyPlayer', 'Minimized to system tray')      # this emits messageClicked signal
                cfg.minimizedtotraywarningignored = True
            if settings.checkTrayResetFirstFileOnRestore.isChecked():
                self.first_video_fully_loaded = False
            gc.collect(generation=2)
        return event.accept()


    def hideEvent(self, event: QtGui.QHideEvent):       # 'spontaneous' -> native minimize button pressed
        if constants.IS_WINDOWS and settings.checkTaskbarIconPauseMinimized.isChecked():
            at_end = get_ui_frame() == self.frame_count
            self.taskbar.setOverlayIcon(self.icons['restart' if at_end else 'pause' if self.is_paused else 'play'])

        if event.spontaneous():
            if settings.checkMinimizePause.isChecked():
                self.was_paused = self.is_paused
                self.force_pause(True)
            elif settings.groupTray.isChecked() and settings.checkTrayMinimize.isChecked():
                self.close()                            # TODO these do not work with each other yet
        return super().hideEvent(event)


    def showEvent(self, event: QtGui.QShowEvent):       # 'spontaneous' -> restored by OS (e.g. clicked on taskbar icon)
        super().showEvent(event)

        # clear overlay icon on taskbar in Windows
        if constants.IS_WINDOWS and settings.checkTaskbarIconPauseMinimized.isChecked():
            self.taskbar.clearOverlayIcon()

        player.on_show(event)

        # strangely, closing/reopening the window applies an alignment to our QVideoPlayer/QWidget (very bad)
        self.gridLayout.setAlignment(self.vlc, Qt.Alignment())                  # reset alignment to nothing

        if event.spontaneous():
            if not self.was_paused and settings.checkMinimizePause.isChecked() and settings.checkMinimizeRestore.isChecked():
                self.force_pause(False)
        if self.isFullScreen():
            self.set_fullscreen(True)                   # restore fullscreen UI
        gc.collect(generation=2)


    def leaveEvent(self, event: QtCore.QEvent):
        ''' Handles moving the cursor off the window. In fullscreen, mousing
            over the controls while they're docked counts as leaving the window.
            If we've ACTUALLY left the window, we trigger the idle timeout so
            the docked controls fade out. '''
        if settings.checkHideIdleCursor.isChecked():
            pos = self.dockControls.mapFromGlobal(QtGui.QCursor.pos())
            if not self.dockControls.rect().contains(pos):
                self.vlc.idle_timeout_time = 1.0        # 0 locks the UI, so set it to 1
        return super().leaveEvent(event)


    def moveEvent(self, event: QtGui.QMoveEvent):
        ''' Handles moving the window. Remembers our last non-maximized,
            non-fullscreen position by setting `self.last_window_pos`. However,
            out `self.toggle_maximized` method causes weird/inverted behavior,
            so if we're "normal" but `self.invert_next_move_event` is True, we
            save our position anyway, and if we're "maximized/fullscreen", we
            set `self.invert_next_move_event` back to False without saving.

            Additionally, sometimes Qt likes to just report garbage numbers,
            such as (0,0) for the position or (-1,-1) for the size. As such,
            since `moveEvent` is evaluated first, we must also track the last
            non-zero position so we can see if the size is garbage as well,
            then retroactively fix it using `self.last_window_pos_non_zero`.

            This is all done because `QWidget.saveGeometry()` and
            `QWidget.restoreGeometry()` have too many edge cases I just can't
            figure out. Hopefully we can just get rid of this eventually. '''
        fullscreen = self.isFullScreen()
        if not self.isMaximized() and not fullscreen:                   # don't save position if we're maximized/fullscreen
            if self.invert_next_move_event:
                self.invert_next_move_event = False
            else:
                if not event.oldPos().isNull():                         # save non-zero position to two separate properties
                    self.last_window_pos_non_zero = event.oldPos()
                self.last_window_pos = event.oldPos()
            if self.timer_id_resize_snap is None or app.mouseButtons() != Qt.LeftButton:
                self.last_move_time = get_time()                        # don't save move time if we're actually resizing
        elif fullscreen:
            if self.ignore_next_fullscreen_move_event:                  # if the user is trying to move an already...
                self.ignore_next_fullscreen_move_event = False          # ...fullscreen window, leave fullscreen. window...
            else:                                                       # ...will be in the wrong place, but whatever
                self.actionFullscreen.trigger()
        elif self.invert_next_move_event:                               # set `last_window_size` here instead for inverted behavior
            if not event.oldPos().isNull():
                self.last_window_pos_non_zero = event.oldPos()
            self.last_window_pos = event.oldPos()


    def resizeEvent(self, event: QtGui.QResizeEvent):
        ''' Refer to `moveEvent` for why this is such a disaster. '''
        if not self.isMaximized() and not self.isFullScreen():          # don't save size if we're currently maximized/fullscreen
            if self.invert_next_resize_event:
                self.invert_next_resize_event = False
            elif event.oldSize().width() != -1:                         # ignore garbage size (-1, -1)
                self.last_window_size = event.oldSize()
            elif self.last_window_pos.isNull():                         # garbage size AND position - ignore size, revert position
                self.last_window_pos = self.last_window_pos_non_zero
        elif self.invert_next_resize_event:
            if event.oldSize().width() != -1:
                self.last_window_size = event.oldSize()
            elif self.last_window_pos.isNull():
                self.last_window_pos = self.last_window_pos_non_zero


    def timerEvent(self, event: QtCore.QTimerEvent):
        ''' The base timeout event, used for adjusting the window's aspect
            ratio after a resize. Started by `QVideoPlayer.resizeEvent()`. '''

        # TODO: on Linux, app.mouseButtons() never returns anything when we're clicking outside the window...
        # ...(i.e. the window's border), so the player just flails around inside the window until we let go
        if self.timer_id_resize_snap is not None and app.mouseButtons() != Qt.LeftButton:
            self.timer_id_resize_snap = self.killTimer(self.timer_id_resize_snap)

            # TODO: what is this for?? is it protecting against some super obscure edge-case? all...
            # ...it seems to do is cause problems on Linux when dragging from the left or top edge
            if get_time() - self.last_move_time < 1:    # of all the things to not be commented, it had to be this
                return super().timerEvent(event)

            # get keyboard modifiers -> shift shinks, ctrl inverts current media type's behavior
            mod = app.queryKeyboardModifiers()
            shrink = mod & Qt.ShiftModifier
            reverse_behavior = mod & Qt.ControlModifier

            # determine desired behavior for current media type, then invert if necessary
            checked = settings.checkSnapOnResize.checkState() and self.is_snap_mode_enabled()
            if (checked and reverse_behavior) or (not checked and not reverse_behavior):
                return

            force_instant_resize = checked == 0
            self.snap_to_player_size(shrink=shrink, force_instant_resize=force_instant_resize)

        if event:
            return super().timerEvent(event)


    def wheelEvent(self, event: QtGui.QWheelEvent):
        ''' Handles scrolling anywhere over the window (unless a child widget
            handles it first without passing it, like the progress slider).
            Increments the volume or playback rate, depending on what keyboard
            modifiers and mouse buttons are currently held down. '''
        up = event.angleDelta().y() > 0
        mod = event.modifiers()                         # just modifiers instead of keyboardModifiers here for some reason

        if mod & Qt.ControlModifier:
            inc = 0.05 if mod & Qt.ShiftModifier else 0.2
            self.set_playback_rate(inc if up else -inc, increment=True)
        else:
            if event.buttons() == Qt.RightButton:
                self.ignore_next_right_click = True     # reset-timer for this starts in `QVideoPlayer.mouseReleaseEvent`
                small = True
            else:
                small = mod & Qt.ShiftModifier
            inc = 1 if small else get_volume_scroll_increment()
            set_volume_slider(get_volume_slider() + (inc if up else -inc))

        refresh_title()
        event.accept()


    def keyPressEvent(self, event: QtGui.QKeyEvent):    # NOTE: the arrow keys seemingly do not get caught here
        key = event.key()
        mod = event.modifiers()

        # ignore keypresses if a lineEdit has focus (except for esc/tab). NOTE: spinboxes use QSpinBoxPassthrough
        for widget in (self.lineOutput, self.lineCurrentTime):
            if widget.hasFocus():
                if key == 16777216:                                     # esc (clear focus)
                    widget.clearFocus()
                elif key == 16777217 and widget is self.lineOutput:     # tab (show similar files next to output text box)
                    self.search_files(auto_popup=True)
                return

        # manually emit shortcuts if the main window isn't focused. `WidgetWithChildrenShortcut` (our...
        # ...shortcut context) usually doesn't need this, but some widgets like the frame spinbox don't...
        # ...work for some reason. NOTE: this doesn't solve the combobox parenting problem above
        # https://stackoverflow.com/questions/10383418/qkeysequence-to-qkeyevent
        if not self.hasFocus():
            sequence = QtGui.QKeySequence(event.modifiers() | event.key())
            for primary, secondary in self.shortcuts.values():
                if primary.key() == sequence or secondary.key() == sequence:
                    primary.activated.emit()
                    break

        # if AltModifier is True but we aren't pressing alt, ignore next alt release
        if key != 16777251 and mod & Qt.AltModifier:
            self.ignore_next_alt = True

        # numbers 0-9
        if 48 <= key <= 57:
            jump_progress = False
            play_recent = False

            if not self.first_video_fully_loaded and settings.checkNumKeysRecentFilesOnLaunch.isChecked():
                play_recent = True
            else:
                if mod & Qt.ControlModifier:
                    secondary = settings.comboNumKeysSecondary.currentIndex()
                    jump_progress = secondary == 1
                    play_recent = secondary == 2
                else:
                    primary = settings.comboNumKeysPrimary.currentIndex()
                    jump_progress = primary == 1
                    play_recent = primary == 2

            if jump_progress:                           # scale progress to current min/max frames
                new_frame = self.minimum + int((self.maximum - self.minimum) / 10 * (key - 48))
                set_and_update_progress(new_frame, SetProgressContext.NAVIGATION_EXACT)
                if self.restarted and settings.checkNavigationUnpause.isChecked():
                    self.force_pause(False)             # auto-unpause after restart if desired
                    self.restarted = False
            elif play_recent:
                if not self.recent_files:
                    return show_on_statusbar('No recent files available.')
                if key == 48:
                    if settings.checkNumKeys0PlaysLeastRecentFile.isChecked(): index = 0
                    else: index = -10
                elif key == 49 and settings.checkNumKeys1SkipsActiveFiles.isChecked() and self.recent_files[-1] == self.video:
                    index = -2
                else:
                    index = -(key - 48)
                path = self.recent_files[max(index, -len(self.recent_files))]
                self.open_recent_file(path, update=settings.checkNumKeysUpdateRecentFiles.isChecked())

        # handle individual keys. TODO: change these to their enums? (70 -> Qt.Key.Key_F)
        elif key == 16777216 and self.actionFullscreen.isChecked():         # esc (fullscreen only)
            self.actionFullscreen.trigger()

        # emulate menubar shortcuts when menubar is not visible (which disables shortcuts for some reason)
        elif not self.menubar.isVisible():
            if mod & Qt.ControlModifier:
                if key == 79:                                               # ctrl + o (open)
                    self.actionOpen.trigger()
                elif key == 83:
                    if mod & Qt.ShiftModifier: self.actionSaveAs.trigger()  # ctrl + shift + s (save as)
                    else:                      self.actionSave.trigger()    # ctrl + s (save)
                elif key == 16777223:                                       # ctrl + del (delete immediately)
                    self.actionDeleteImmediately.trigger()
            elif mod & Qt.AltModifier:
                if key == 81:                                               # alt + q (exit)
                    self.actionExit.trigger()

        # del (mark for deletion) - when we press del, save the mark state we just set and auto-apply it to every file...
        # ...we open afterwards until we've released del. this way we can hold del and cycle for quick marking/unmarking
        # NOTE: `actionMarkDeleted` uses "WidgetShortcut" context so its keypresses only get eaten if the menubar is focused
        if key == 16777223:                             # ignore del entirely if ctrl or alt modifiers are held
            if mod & Qt.ControlModifier or mod & Qt.AltModifier:
                self.mark_for_deletion_held_down = False
            else:
                if self.video and not self.mark_for_deletion_held_down:
                    self.mark_for_deletion_held_down_state = self.video not in self.marked_for_deletion
                    self.actionMarkDeleted.trigger()
                self.mark_for_deletion_held_down = not mod & Qt.ShiftModifier

        elif key == 16777239:                           # page down (pan image)
            if self.is_static_image or self.is_gif:
                image_player.pan(QtCore.QPoint(0, -500))
        elif key == 16777238:                           # page up (pan image)
            if self.is_static_image or self.is_gif:
                image_player.pan(QtCore.QPoint(0, 500))

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

        # confirm that we're actually releasing del -> `isAutoRepeat()` means this is an...
        # ...automatic key-repeat event sent by the OS and the key was not actually released
        if key == 16777223 and self.mark_for_deletion_held_down and not event.isAutoRepeat():
            self.mark_for_deletion_held_down = False    # update tooltip once we're done auto-setting
            self.refresh_marked_for_deletion_tooltip()  # NOTE: this means we'll double-update it sometimes but that's fine

        logging.debug(f'RELEASED key={key} text="{event.text()}"')


    def contextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles the context (right-click) menu for the main window. '''
        if self.ignore_next_right_click:                # NOTE: this resets on a timer even if we don't catch it here
            self.ignore_next_right_click = False
            return
        context = QtW.QMenu(self)

        # HACK: reset the player's base cursor (and then again after a short delay)...
        # ...to fix one of many obscure cursor bugs that can occur after drag-and-drops
        def reset():
            self.vlc.setCursor(Qt.ArrowCursor)
            self.vlc.unsetCursor()
        reset()
        QtCore.QTimer.singleShot(50, Qt.CoarseTimer, reset)

        # add crop/zoom toggle if in crop mode or we're zoomed in
        if self.actionCrop.isChecked():
            context.addAction(self.actionCrop)
        elif image_player.zoomed:
            action_disable_zoom = QtW.QAction('&Zoomed')
            action_disable_zoom.setCheckable(True)
            action_disable_zoom.setChecked(True)
            action_disable_zoom.triggered.connect(image_player.disableZoom)
            context.addAction(action_disable_zoom)

        # add cover art toggle if we have cover art in our buffer
        if self.is_audio_with_cover_art:                # True so long as the cover art is loaded (even while hidden)
            action_toggle_cover_art = context.addAction('Show cover art')
            action_toggle_cover_art.setCheckable(True)
            action_toggle_cover_art.setChecked(can_show_cover_art())
            action_toggle_cover_art.triggered.connect(settings.checkShowCoverArt.setChecked)

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
        if not self.is_audio_without_cover_art:
            self.refresh_copy_image_action()
            context.addAction(self.actionCopyImage)
        context.addAction(self.actionSettings)

        # add submenus if menubar isn't visible, we shift-click, or we always want them shown
        show_submenus = settings.checkContextShowSubmenus.checkState()
        always_show = show_submenus == 2
        dynamic_show = show_submenus == 1
        if always_show or event.modifiers() & Qt.ShiftModifier or (not self.menubar.isVisible() and dynamic_show):
            context.addSeparator()
            context.addMenu(self.menuFile)
            context.addMenu(self.menuEdit)
            context.addMenu(self.menuVideo)
            context.addMenu(self.menuAudio)
            context.addMenu(self.menuWindow)
            context.addMenu(self.menuPlayer)
            context.addMenu(self.menuHelp)

        # add labels with info about the current media, then show context menu
        if self.video:
            self.add_info_actions(context)
            context.addSeparator()                      # ↓ TODO: reuse the hotkey lambda here? does it matter?
            context.addAction('Properties', lambda: open_properties(self.video))
        context.exec(event.globalPos())


    # ---------------------
    # >>> CUSTOM EVENTS <<<
    # ---------------------
    def dockControlsResizeEvent(self, event: QtGui.QResizeEvent):
        ''' Makes UI controls more compact as their size shrinks. '''
        width = event.size().width()
        self.frameQuickChecks.setVisible((not self.actionCrop.isChecked() and width >= 568) or width >= 800)
        self.frameCropInfo.setVisible(self.actionCrop.isChecked() and width >= 621)
        self.lineOutput.setMinimumWidth(10 if width <= 380 else 120)                # reduce output lineEdit (but retain usability)
        self.advancedControlsLine.setVisible(width >= 357)                          # hide aesthetic line-separator
        self.glayoutQuickButtons.setHorizontalSpacing(2 if width <= 394 else 6)     # reduce spacing between buttons
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


    def frameProgressContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles the context (right-click) menu for the progress slider. '''
        precision_action = QtW.QAction(settings.checkHighPrecisionProgress.text())
        precision_action.setCheckable(True)
        precision_action.setChecked(settings.checkHighPrecisionProgress.isChecked())
        precision_action.setToolTip(settings.checkHighPrecisionProgress.toolTip())
        precision_action.toggled.connect(settings.checkHighPrecisionProgress.setChecked)

        context = QtW.QMenu(self)
        context.setToolTipsVisible(True)
        context.addAction(precision_action)
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
            if self.duration_rounded < 3600: start_label = f'{verb} {m}:{s:02}.{ms:02} (frame {self.minimum})'
            else:                            start_label = f'{verb} {h}:{m:02}:{s:02} (frame {self.minimum})'
        else:                                start_label = f'{verb}: Disabled'
        start_label_action = QtW.QAction(start_label)
        start_label_action.setEnabled(False)

        # create disabled action for displaying end time
        verb = 'End' if is_trim_mode else 'Fade from'
        if self.maximum != self.frame_count:
            h, m, s, ms = get_hms(self.maximum / self.frame_rate)
            if self.duration_rounded < 3600: end_label = f'{verb}: {m}:{s:02}.{ms:02} (frame {self.maximum})'
            else:                            end_label = f'{verb}: {h}:{m:02}:{s:02} (frame {self.maximum})'
        else:                                end_label = f'{verb}: Disabled'
        end_label_action = QtW.QAction(end_label)
        end_label_action.setEnabled(False)

        # create disabled action for displaying trim length, if applicable
        if show_length_label:
            frames = self.maximum - self.minimum
            seconds = frames / self.frame_rate
            h, m, s, ms = get_hms(seconds)
            if h: length_label = f'Length: {h}:{m:02}:{s:02} ({frames} frames)'
            else: length_label = f'Length: {m}:{s:02}.{ms:02} ({frames} frames)'
            length_label_action = QtW.QAction(length_label)
            length_label_action.setEnabled(False)

        # actions for force-setting start/end times (disabled when no/useless media is playing)
        set_start_action = QtW.QAction('Set &start to current position', self)
        set_start_action.triggered.connect(lambda: self.set_trim_start(enabled=True))
        set_end_action = QtW.QAction('Set &end to current position', self)
        set_end_action.triggered.connect(lambda: self.set_trim_end(enabled=True))
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
        if show_length_label:
            context.addAction(length_label_action)
        context.exec(event.globalPos())


    def buttonMediaLocationContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles the context (right-click)
            menu for the media location button. '''
        if not self.video: return                           # do not render context menu if no media is playing

        context = QtW.QMenu(self)
        context.addAction(self.actionExploreMediaPath)
        context.addAction(self.actionCopyMediaPath)
        context.addAction(self.actionCopyFile)
        context.addAction(self.actionCutFile)

        def menuMoveContextMenuEvent(menu: QtW.QMenu, event: QtGui.QContextMenuEvent):
            ''' Handles the context (right-click) menus for
                individual "Move to..." and "Open..." destinations. '''
            if action := menu.actionAt(event.pos()):
                context = QtW.QMenu(self)
                context.addAction('&Remove destination', lambda: self.move_destinations.remove(action.toolTip()))
                context.exec(event.globalPos())

        def move(folder: str):
            ''' Moves the current media to `folder`, retaining its basename.
                Warns on replacement or if `folder` is on a different drive. '''
            try:
                if not os.path.isdir(folder) and exists(folder):
                    folder = os.path.dirname(folder)        # if folder is actually a file, use ITS folder

                # TODO: show saveFile prompt like rename does when the path already exists
                new_name = os.path.join(folder, os.path.basename(self.video))
                self.rename(
                    new_name=new_name,
                    sanitize=False,
                    delete_source_dir=False,
                    warn_on_replace=True,
                    warn_on_drive=True
                )
            except:
                log_on_statusbar(f'(!) Move failed: {format_exc()}')

        def generate_menu(label: str) -> QtW.QMenu:
            menu = context.addMenu(label)
            menu.setToolTipsVisible(True)
            menu.contextMenuEvent = menuMoveContextMenuEvent
            return menu

        # create "Open" and "Move to" submenus for quickly sorting files
        context.addSeparator()
        open_menu = generate_menu('&Open...')
        move_menu = generate_menu('&Move to...')
        add_destination_action = QtW.QAction('&Add destination...')
        add_destination_action.triggered.connect(lambda: self.browse_for_directory(noun='destination'))

        # add all existing destinations to the top of each submenu
        # TODO: always `openPath`, or try opening in pyplayer first?
        # TODO: only add to `move_menu` if it's a folder, or move to the file's folder?
        for folder in self.move_destinations:
            label = os.path.basename(folder)                # ↓ 7/30/24 i JUST learned you can do this to fix lambdas in iterables
            open_menu.addAction(label, lambda f=folder: qthelpers.openPath(f)).setToolTip(folder)
            move_menu.addAction(label, lambda f=folder: move(f)).setToolTip(folder)

        # add a separator and an action for adding new destinations to each submenu
        for menu in (open_menu, move_menu):
            menu.addSeparator()
            menu.addAction(add_destination_action)

        # add labels with info about the current media, then show context menu
        self.add_info_actions(context)
        context.exec(event.globalPos())


    def buttonMarkDeletedContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles the context (right-click) menu for the deletion button. '''
        # TODO: doing this as a lambda in `self.setup()` crashes if you open and close the confirmation prompt????
        self.menuDelete.exec(event.globalPos())


    def buttonSnapshotContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles the context (right-click) menu for the snapshot button.
            Side note: PyQt does NOT like it if you do `QMenu.exec()` in a
            lambda. As soon as it returns, you get: `TypeError: invalid
            argument to sipBadCatcherResult()`. And it's uncatchable. '''
        context = QtW.QMenu(self)
        for index, action in enumerate(self.menuSnapshots.actions()):
            if index == 2 and not self.is_audio_without_cover_art:
                self.refresh_copy_image_action()            # add "Copy image" action if there's something to copy
                context.addAction(self.actionCopyImage)
            context.addAction(action)
        context.exec(event.globalPos())


    def buttonAutoplayContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles the context (right-click) menu for the autoplay button. '''
        context = QtW.QMenu(self)
        context.setToolTipsVisible(True)
        context.addActions(self.menuAutoplay.actions()[1:])
        context.exec(event.globalPos())


    def cycleButtonContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles the context (right-click) menu for the cycle buttons. '''
        mime = self.mime_type

        context = QtW.QMenu(self)                           # ↓ lambda to discard qt's signal parameter
        context.addAction('Open random file', lambda: self.shuffle_media())
        context.addAction('Open next file', self.cycle_media)
        context.addAction('Open previous file', lambda: self.cycle_media(next=False))
        context.addSeparator()
        context.addAction(f'Open random {mime} file', lambda: self.shuffle_media(valid_mime_types=(mime,)))
        context.addAction(f'Open next {mime} file', lambda: self.cycle_media(valid_mime_types=(mime,)))
        context.addAction(f'Open previous {mime} file', lambda: self.cycle_media(next=False, valid_mime_types=(mime,)))
        context.exec(event.globalPos())


    def menuRecentContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles the context (right-click)
            menus for individual recent files. '''
        action = self.menuRecent.actionAt(event.pos())
        if action is self.actionClearRecent or not action: return
        path = action.toolTip()

        context = QtW.QMenu(self)
        context.addAction('&Remove from recent files', lambda: (self.recent_files.remove(path), self.refresh_recent_menu()))
        context.addSeparator()
        context.addAction('M&edia location', lambda: self.explore(path))
        context.addAction('&Copy media path', lambda: self.copy(path))
        context.addSeparator()
        context.addAction('&Move to top', lambda: self.open_recent_file(path, update=True, open=False))
        context.addAction('&Open and move to top', lambda: self.open_recent_file(path, update=True))
        context.addAction('&Open without moving to top', lambda: self.open_recent_file(path, update=False))
        context.exec(event.globalPos())


    def frameVolumeContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles the context (right-click) menu for the volume slider's
            frame. A frame is used since the slider can be disabled.'''
        mute_action = QtW.QAction('Mute')
        mute_action.setCheckable(True)
        mute_action.setChecked(not self.sliderVolume.isEnabled())
        mute_action.toggled.connect(self.toggle_mute)

        next_boost = min(self.volume_boost + 0.5, 5)
        last_boost = min(self.volume_boost - 0.5, 5)
        inc_boost_action = QtW.QAction(f'Increase boost to {next_boost:.1f}x')
        inc_boost_action.triggered.connect(lambda: self.set_volume_boost(next_boost))
        dec_boost_action = QtW.QAction(f'Decrease boost to {last_boost:.1f}x')
        dec_boost_action.triggered.connect(lambda: self.set_volume_boost(last_boost))
        reset_boost_action = QtW.QAction('Reset boost')
        reset_boost_action.triggered.connect(self.set_volume_boost)

        context = QtW.QMenu(self)
        context.addAction(mute_action)
        context.addSeparator()
        context.addAction(inc_boost_action)
        context.addAction(dec_boost_action)
        context.addAction(reset_boost_action)
        context.exec(event.globalPos())


    def frameVolumeMousePressEvent(self, event: QtGui.QMouseEvent):
        ''' Handles clicking on the volume slider's frame. A frame is used
            since the slider can be disabled. Unmutes on left-click. '''
        if event.button() == Qt.LeftButton:
            self.set_mute(False)


    def buttonPauseContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles the context (right-click) menu for the pause button. '''
        # TODO should these redefined events use QWidget.actions() instead of contextMenuEvent?
        context = QtW.QMenu(self)
        context.addAction(self.actionStop)
        context.addAction('Restart', lambda: set_and_update_progress(0, SetProgressContext.RESET_TO_MIN))
        context.exec(event.globalPos())                     # ^ TODO this might have timing issues with update_thread


    def buttonPauseMousePressEvent(self, event: QtGui.QMouseEvent):
        ''' Handles clicking on the volume slider's frame. A frame is used
            since the slider can be disabled. Unmutes on left-click. '''
        if event.button() == Qt.MiddleButton: self.stop()
        else: QtW.QPushButton.mousePressEvent(self.buttonPause, event)


    def editProgressBarContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles the context (right-click) menu for the edit progress bar,
            allowing you to see, display, and cancel all active edits. '''
        context = QtW.QMenu(self)
        context.setToolTipsVisible(True)

        # add recent edits submenu + separator to top of menu if desired
        if settings.spinRecentEdits.value():
            menu_recent = QtW.QMenu('Recent edits', context)
            menu_recent.setToolTipsVisible(True)
            if self.recent_edits:
                menu_recent.triggered.connect(lambda action: self.open_recent_file(action.toolTip(), update=True, edits=True))
                for path in reversed(self.recent_edits):
                    menu_recent.addAction(os.path.basename(path)).setToolTip(path)
            else:
                menu_recent.addAction('No edits this session').setEnabled(False)
            context.addMenu(menu_recent)
            context.addSeparator()

        # return early if no edits are actually active
        total_edits = len(self.edits_in_progress)
        if not total_edits:
            context.addAction('No edits in progress').setEnabled(False)
            context.exec(event.globalPos())                 # NOTE: !!! EXTREMELY IMPORTANT -> do NOT return this directly...
            return                                          # ...or the `self.open()` actions above will crash??????

        # workarounds for python bug/oddity involving creating lambdas in iterables
        # (needed for the actions to actually remember which edit they belong to)
        get_cancel_lambda =   lambda edit: lambda: edit.cancel()
        get_pause_lambda =    lambda edit: lambda: edit.pause(paused=True)
        get_resume_lambda =   lambda edit: lambda: edit.pause(paused=False)
        get_priority_lambda = lambda edit: lambda: edit.give_priority()

        # this + the above workarounds (edit: now just the four) took like two hours to get working
        # NOTE: this loop could be much shorter, but this is way easier to read
        for edit in self.edits_in_progress:

            # set edit's menu title with text, operation count, and (operation) progress
            if total_edits > 1:
                submenu = QtW.QMenu(edit.get_progress_text(simple=True), context)
                context.addMenu(submenu)
            else:
                submenu = context                           # for just one edit, show the submenu directly

            # resume/pause selected edit
            if not edit._is_paused:
                action_suspend = submenu.addAction('Pause')
                action_suspend.triggered.connect(get_pause_lambda(edit))
            else:
                action_suspend = submenu.addAction('Resume')
                action_suspend.triggered.connect(get_resume_lambda(edit))

            # cancel selected edit
            action_cancel = submenu.addAction('Cancel')
            action_cancel.triggered.connect(get_cancel_lambda(edit))
            submenu.addSeparator()                          # show separator after suspend/cancel actions

            # give priority to selected edit (if possible)
            if total_edits > 1:
                action_priority = submenu.addAction('Display')
                if edit.has_priority:
                    action_priority.setEnabled(False)
                else:
                    action_priority.triggered.connect(get_priority_lambda(edit))

            # show dest's basename as disabled action so edits can be distinguished
            if edit.dest:
                action_outfile = submenu.addAction(os.path.basename(edit.dest))
                action_outfile.setEnabled(False)
                if edit.temp_dest == edit.dest:             # show full path(s) as tooltip
                    action_outfile.setToolTip(edit.dest)
                else:
                    action_outfile.setToolTip(f'Final destination:\t {edit.dest}\n'
                                              f'Temp destination:\t {edit.temp_dest}')

            # show "-threads" override if one was used
            if edit._threads:
                text = f'Using {edit._threads} thread{"s" if edit._threads != 1 else ""}'
                submenu.addAction(text).setEnabled(False)

        # add "Pause/Resume/Cancel all" actions, if appropriate
        if total_edits > 1:
            context.addSeparator()
            context.addAction('Pause all', lambda: self.pause_all(paused=True))
            context.addAction('Resume all', lambda: self.pause_all(paused=False))
            context.addAction('Cancel all', self.cancel_all)

        context.exec(event.globalPos())


    def editProgressBarMouseReleaseEvent(self, event: QtGui.QMouseEvent):
        ''' Handles clicking (and releasing) over the edit progress bar. Cycles
            which edit currently has priority on left-click, toggles pause-state
            for the current edit with priority on middle-click. '''
        if len(self.edits_in_progress) > 1 and event.button() == Qt.LeftButton:
            self.cycle_edit_priority()
        elif event.button() == Qt.MiddleButton:
            edit = self.get_edit_with_priority()
            edit.pause()


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
                with open(f'{constants.THEME_DIR}{sep}{filename}', 'r') as theme_file:
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


    def refresh_theme_combo(self, *, restore_theme: bool = True, set_theme: str = None):
        self.load_themes()                                  # ^ * to capture unused signal args
        comboThemes = settings.comboThemes
        old_theme = comboThemes.currentText()               # save current theme's name

        for _ in range(comboThemes.count()):
            comboThemes.removeItem(1)
        for theme in self.themes:
            try:
                name = theme.get('name', None)
                if name:
                    comboThemes.addItem(name)
            except:
                logging.warning(f'Could not add theme {name} to theme combo: {format_exc()}')

        if set_theme:       comboThemes.setCurrentText(set_theme)
        elif restore_theme: comboThemes.setCurrentText(old_theme)               # attempt to restore theme based on previous theme's name
        return old_theme


    def get_theme(self, theme_name: str) -> dict:
        ''' Returns the theme dictionary for the first theme called `theme_name`.
            If no matching theme is found, None is returned. '''
        if theme_name and theme_name != 'none':
            for theme in self.themes:
                try:
                    if theme_name.lower() == theme['name'].lower():
                        return theme
                except:
                    pass


    def set_theme(self, theme_name: str):
        ''' Gets and sets the current theme to the first theme with called
            `theme_name`. If not found, the "default" theme is used. '''
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
                if special_widgets:
                    theme['special_widgets'] = special_widgets
            except Exception as error:
                logging.warning(f'Theme \'{theme["name"]}\' failed to load with the following error - {type(error)}: {error}.')

        # adjust UI spacing to match theme
        opt = QtW.QStyleOptionSlider()
        self.sliderProgress.initStyleOption(opt)
        groove_rect = self.sliderProgress.style().subControlRect(QtW.QStyle.CC_Slider, opt, QtW.QStyle.SC_SliderGroove, self.sliderProgress)
        handle_rect = self.sliderProgress.style().subControlRect(QtW.QStyle.CC_Slider, opt, QtW.QStyle.SC_SliderHandle, self.sliderProgress)
        self.frameProgress.setMaximumHeight(max(16, groove_rect.height() + 6, handle_rect.height() + 6))    # frameProgress needs +4 pixels, and +2 pixels of padding


    def set_player(self, backend: str | widgets.PyPlayerBackend, _error: bool = False):
        ''' Sets player to `backend`, which can be the raw `PyPlayerBackend`
            class or its `__name__` property. Disables and waits on old player,
            updates global aliases, enables and shows (unless minimized) the new
            player, and restores media progress for non-images. The new player
            is cached if needed, and the config is immediately updated. '''
        global player, play, show_on_player, set_and_update_progress, set_player_position

        if self.player_swap_in_progress and not _error:
            return logging.info('Not changing player - player swap is already in progress.')
        self.player_swap_in_progress = True

        try:
            log_on_statusbar(f'Setting player to {backend} player...')
            app.processEvents()                     # process events so the log message appears on statusbar

            # get current UI frame and new player
            frame = get_ui_frame()
            was_paused = self.is_paused
            if isinstance(backend, str):
                new_player = self.vlc.players.get(backend) or getattr(widgets, f'Player{backend}')(self.vlc)
            else:
                new_player = self.vlc.players.get(backend.__name__) or backend(self.vlc)

            # disable old player if we had one
            try:
                if self.player.__name__ == 'Undefined':
                    raise
                old_player = self.player

                if new_player == old_player:
                    return show_on_statusbar(f'You\'re already using {backend} player.', 3000)
                if not FFPROBE and not new_player.SUPPORTS_PARSING:
                    if qthelpers.getPopupYesNo(     # warn user if they're about to be stuck between a rock and a hard place
                        title='You won\'t be able to open files!',
                        text='You have FFprobe disabled, but have also selected a\nplayer that cannot sufficiently parse media on its own.\n\nContinue?',
                        icon='warning',
                        **self.get_popup_location_kwargs()
                    ).exec() != QtW.QMessageBox.Yes:
                        return

                old_player.disable()
                new_player.last_file = old_player.last_file
            except:
                pass

            # update global aliases to reference our new player
            player = new_player
            play = new_player.play
            show_on_player = new_player.show_text
            set_and_update_progress = new_player.set_and_update_progress
            set_player_position = new_player.set_position

            # enable the new player and restore our original progress within it
            self.frame_override = -1                # reset frame_override in case last player was using it
            if not new_player.enable():
                raise
            if self.isVisible():                    # only show player if the window is visible
                new_player.show()

            # cache the new player and update properties/config accordingly
            self.vlc.players[new_player.__name__] = new_player
            self.vlc.player = new_player
            self.player = new_player
            config.cfg.player = new_player.__name__

            self.restore(frame, was_paused)
            log_on_statusbar(f'Player successfully set to {backend} player.')

        except:
            if _error:
                msg = f'(CRITICAL FAILURE) New player could not be set, and old player "{backend}" could not be restored! {format_exc()}'
                logging.critical(msg)
                show_on_statusbar(msg)
            else:
                log_on_statusbar(f'(!) New player "{backend}" could not be set: {format_exc()}')
                try:    self.set_player(old_player, _error=True)
                except: self.set_player('Qt', _error=True)
        finally:
            self.player_swap_in_progress = False


    # -------------------------------
    # >>> BASIC VIDEO OPERATIONS <<<
    # -------------------------------
    def shuffle_media(
        self,
        folder: str = None,
        autoplay: bool = False,                     # NOTE: this doesn't change the current autoplay state
        valid_mime_types: tuple[str] = None
    ) -> str:
        if folder is None:                          # no folder provided, shuffle within current folder
            if not self.video:                      # return if no folder provided and no media playing
                return show_on_statusbar('No media is playing.', 10000)
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
        is_hidden = file_is_hidden
        locked_files = self.locked_files
        open = self.open
        ignore = self.shuffle_ignore_unique
        ignore_order = self.shuffle_ignore_order

        # determine valid mime types. any mime goes if we're shuffling...
        # ...manually, but no autoplay-shuffling for images/gifs (yet?)
        if not valid_mime_types:
            if autoplay:
                same_mime = self.actionAutoplaySameMime.isChecked()
                if same_mime: valid_mime_types = (self.mime_type,)
                else:         valid_mime_types = ('video', 'audio')
            else:             valid_mime_types = ('video', 'audio', 'image')

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
                if mime not in valid_mime_types:
                    continue
            except:
                continue

            # check for reasons we might skip a playable file (from most to least likely)
            # NOTE: we don't skip just-edited clips like in `cycle_media` (for performance)
            if filename in ignore: continue
            if is_hidden(file): continue
            if skip_marked and file in marked: continue
            if filename == current_basename: continue
            if file in locked_files: continue

            # if file gets opened, check the size of our ignore list and return the file
            if open(file, _from_cycle=True, _from_autoplay=autoplay,
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

        # nothing played - unmark autoplay flag if we were trying to autoplay
        if autoplay:
            self.current_file_is_autoplay = False

        # ignore list has multiple files - we ran out of files to play. clear it and shuffle again
        if len(ignore) > 1:
            logging.info('All files played. Clearing shuffle ignore list and reshuffling...')
            ignore.clear()
            ignore_order.clear()
            return self.shuffle_media(
                folder=folder,
                autoplay=autoplay,
                valid_mime_types=valid_mime_types
            )

        # nothing could be or has been played - show appropriate log message on statusbar
        if len(valid_mime_types) == 3: log_on_statusbar('This is the only playable media file in this folder.')
        else: log_on_statusbar(f'This is the only playable {"/".join(valid_mime_types)} file in this folder.')


    def cycle_media(
        self,
        *,                                          # * to capture unused signal args
        next: bool = True,
        ignore: tuple[str] = tuple(),
        update_recent_list: bool = True,
        autoplay: bool = False,
        valid_mime_types: tuple[str] = None,
        index_override: int = 0
    ) -> str:
        ''' Cycles through the current media's folder and looks for the `next`
            or previous openable, non-hidden file that isn't in the `ignore`
            list. If there are no other openable files, nothing happens.
            Otherwise, the new file is opened and returned.

            TODO: This needs a lot of work.
                - implement OS-specific sorting alorithms
                - is there a faster (safe) way of getting our current index in a folder?
                - when `current_media` is missing, we should insert into `files`, resort, and get index that way
                - is there EVER a scenario where an `index_offset` of 1 results in a wrongly skipped video? '''

        # save copies of critical properties that could potentially change while we're saving
        original_video_path = self.video_original_path
        current_video_path = self.video
        base_file = original_video_path if settings.checkCycleRememberOriginalPath.checkState() else current_video_path

        # save the direction we're going
        self.last_cycle_was_forward = next

        # update autoplay icon if needed
        if self.actionAutoplayDirectionDynamic.isChecked() and not self.actionAutoplayShuffle.isChecked():
            if next: self.buttonAutoplay.setIcon(self.icons['autoplay'])
            else:    self.buttonAutoplay.setIcon(self.icons['autoplay_backward'])

        if not current_video_path: return show_on_statusbar('No media is playing.', 10000)  # TODO remember last media's folder between sessions?
        logging.info(f'Getting {"next" if next else "previous"} media file...')

        current_dir, current_basename = os.path.split(base_file)
        files = os.listdir(current_dir)
        if len(files) < 2:
            if len(files) == 1: return log_on_statusbar('This is the only file in this folder.')
            if len(files) == 0: return log_on_statusbar('There are no remaining files to play in this folder.')

        # get current position in folder so we know where to start from
        if current_basename in files:               # original path might not exist anymore
            current_index = files.index(current_basename)
        elif self.last_cycle_index is not None:
            current_index = self.last_cycle_index
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
        else:    file_range = range(current_index, current_index - len(files) - 1, -1)

        # aliases for the loop
        skip_marked = self.checkSkipMarked.isChecked()
        marked = self.marked_for_deletion
        is_hidden = file_is_hidden
        locked_files = self.locked_files
        open = self.open

        # determine valid mime types. any mime goes if we're cycling...
        # ...manually, but no autoplay-cycling for images/gifs (yet?)
        if not valid_mime_types:
            if autoplay:
                same_mime = self.actionAutoplaySameMime.isChecked()
                if same_mime: valid_mime_types = (self.mime_type,)
                else:         valid_mime_types = ('video', 'audio')
            else:             valid_mime_types = ('video', 'audio', 'image')

        skipped_old_video = False
        start = get_time()
        for new_index in file_range:
            new_index = new_index % len(files)      # `len(files)` is already confirmed to not be 0
            file = f'{current_dir}{sep}{files[new_index]}'
            #logging.debug(f'Checking {file} at index #{new_index}')

            # get mime type of file to verify this is actually playable and skip the extra setup done in open()
            try:
                mime, extension = filetype.match(file).mime.split('/')
                if mime not in valid_mime_types:
                    continue
            except:
                continue

            # check for reasons we might skip a playable file (from most to least likely)
            if is_hidden(file): continue
            if file in ignore: continue
            if skip_marked and file in marked: continue
            #if index_offset == 0 and (file == original_video_path or file == current_video_path): continue
            if file == original_video_path:
                skipped_old_video = original_video_path != current_video_path
                continue
            if file == current_video_path: continue
            if file in locked_files: continue

            # attempt to play file -> -1 is returned if file can't be opened
            # if the new video opens successfully, stop
            if open(file, _from_cycle=True, _from_autoplay=autoplay,
                    update_recent_list=update_recent_list, mime=mime, extension=extension) != -1:
                logging.info(f'Cycled files after {get_time() - start:.3f} seconds.')
                self.last_cycle_index = new_index
                return file

        # nothing played - unmark autoplay flag and show appropriate log message on statusbar
        if autoplay:
            self.current_file_is_autoplay = False
        if not skipped_old_video:
            if len(valid_mime_types) == 3: log_on_statusbar('This is the only playable media file in this folder.')
            else: log_on_statusbar(f'This is the only playable {"/".join(valid_mime_types)} file in this folder.')
        else: log_on_statusbar('This and the file you just edited are the only playable media files in this folder.')


    def cycle_recent_files(self, forward: bool = True):
        ''' Plays the next (older) recent file in `self.recent_files` if
            `forward`, else the last (newer) recent file. Position is relative
            to `self.video`'s spot within the recent files list. If not within
            the list, the most recent file is used. '''
        # default to latest (most recent) file if no valid file is loaded
        # NOTE: recent_files is least recent to most recent -> index 0 is the LEAST recent
        if self.video not in self.recent_files: current_index = len(self.recent_files)
        else: current_index = self.recent_files.index(self.video)

        new_index = current_index + (1 if forward else -1)
        if 0 <= new_index <= len(self.recent_files) - 1:
            path = self.recent_files[new_index]
            self.open_recent_file(path, update=False)


    def open_recent_file(self, path: str, update: bool, open: bool = True, edits: bool = False):
        ''' Opens `path` from `self.recent_files` (or `self.recent_edits` if
            `edits` is True) if it exists, even if it's not actually in the
            list. If `path` doesn't exist and IS in the list, it is removed.

            - `update` - Move `path` to the top of `self.recent_files`
                         (regardless of `edits`).
            - `open`   - Open `path`. If False, `path` is moved to the top of
                         its associated list (regardless of `update`). '''
        try:
            if edits:
                recents = self.recent_edits
                open = True
                noun = 'edit'
            else:
                recents = self.recent_files
                noun = 'file'

            if path in self.locked_files:           # recent file is locked (it's actively being edited)
                log_on_statusbar(f'Recent {noun} {path} is currently being worked on.')
            elif os.path.isfile(path):
                if open:
                    if self.open(path, update_recent_list=update) != -1:
                        log_on_statusbar(f'Opened recent file #{len(recents) - recents.index(path)}: {path}')
                    else:
                        log_on_statusbar(f'Recent file {path} could not be opened.')
                        recents.remove(path)
                else:                               # don't open, just move file to top
                    recents.append(recents.pop(recents.index(path)))
            else:
                log_on_statusbar(f'Recent {noun} {path} no longer exists.')
                recents.remove(path)
        except ValueError:                          # ValueError -> path was not actually in recent_files/edits
            pass
        finally:
            if not edits:
                self.refresh_recent_menu()


    def open_folder(self, folder: str, mod: int = 0, focus_window: bool = True) -> str:
        ''' Plays a file inside `folder`, returning the selected file, if any.
            The method of choosing a file and whether Autoplay/shuffle mode are
            altered depends on keyboard modifiers passed through `mod`, if any:

            - `Alt` OR `Ctrl + Shift`: Enable autoplay, disable shuffle mode.
                                       Plays the first valid file in the folder.
            - `Ctrl`:                  Enable autoplay, enable shuffle mode.
                                       Plays a random file in the folder.
            - `Shift`:                 Disables autoplay, ignore shuffle mode.
                                       Plays the first valid file in the folder.
            - No modifiers:            Enable autoplay, keep current shuffle
                                       mode setting (first file if disabled,
                                       random file if enabled).

            NOTE: `focus_window` may also be passed,
            but is ignored if shuffle mode is used. '''

        try:
            folder = abspath(folder)                # ensure `folder` uses a standardized format

            # no modifiers -> enable autoplay and keep current shuffle mode setting
            enable_autoplay = True
            enable_shuffle = self.actionAutoplayShuffle.isChecked()

            if (mod & Qt.ControlModifier and mod & Qt.ShiftModifier) or mod & Qt.AltModifier:
                enable_shuffle = False              # alt OR (ctrl+shift) -> autoplay, no shuffle
            elif mod & Qt.ControlModifier:
                enable_shuffle = True               # ctrl                -> autoplay, shuffle
            if mod & Qt.ShiftModifier:
                enable_autoplay = False             # shift               -> no autoplay (shuffle is irrelevant)

        # update autoplay and shuffle mode, then play a random file if shuffle mode is active
            self.actionAutoplay.setChecked(enable_autoplay)
            if enable_autoplay:                     # ↓ only update shuffle mode if we're using autoplay
                self.actionAutoplayShuffle.setChecked(enable_shuffle)
                if enable_shuffle:
                    file = self.shuffle_media(folder, autoplay=True)
                    if file is not None:
                        log_on_statusbar(f'Randomly opened {os.path.basename(file)} from folder {folder} (shuffle mode).')
                    return file

        # no autoplay OR no shuffle mode -> play first file in folder regardless of autoplay setting
            #skip_marked = self.checkSkipMarked.isChecked()
            #marked = self.marked_for_deletion      # TODO see below
            is_hidden = file_is_hidden
            locked_files = self.locked_files
            open = self.open

            start = get_time()
            for filename in os.listdir(folder):
                file = f'{folder}{sep}{filename}'

                # get mime type of file to verify this is actually playable and skip the extra setup done in open()
                try: mime, extension = filetype.match(file).mime.split('/')
                except: continue

                if is_hidden(file): continue
                if file in locked_files: continue
                #if skip_marked and file in marked: continue    # TODO should we do this here?

                if open(file, _from_cycle=True, mime=mime, extension=extension, focus_window=focus_window) != -1:
                    logging.info(f'Found playable file in folder after {get_time() - start:.3f} seconds.')
                    log_on_statusbar(f'Opened {filename} from folder {folder} ({"" if enable_autoplay else " no"} Autoplay).')
                    return file                     # mention new autoplay state in log message ^

            # if we haven't returned yet, we failed to play anything
            log_on_statusbar(f'No files in {folder} were playable.')

        except:
            log_on_statusbar(f'(!) Failed while checking folder "{folder}" for openable media: {format_exc()}')
        finally:
            self.refresh_autoplay_button()


    def open_probe_file(self, *, file: str = None, delete: bool = False, verbose: bool = True):
        ''' Opens `file`'s probe file, if it exists and FFprobe is enabled.
            If `file` is provided but doesn't exist, this method returns early.
            If `file` is not provided, `self.video` is used. If `delete` is
            True, the probe file is deleted instead of opened. If `verbose` is
            True, warnings are shown `file` or its probe file do not exist. '''
        if not FFPROBE:
            return show_on_statusbar('You don\'t have FFprobe enabled.')

        try:
            if file:
                try:
                    stat = os.stat(file)
                except:
                    if verbose:
                        show_on_statusbar('This media\'s probe file cannot be accessed as the media itself cannot be accessed.')
                    return
            elif self.video:
                file = self.video
                stat = self.stat
            else:
                return show_on_statusbar('No media is playing.')

            # generate probe file's path and verify that it exists
            basename = f'{os.path.basename(self.video)}_{stat.st_mtime}_{stat.st_size}.txt'
            path = f'{constants.PROBE_DIR}{sep}{basename}'
            if not exists(path):
                if verbose:
                    show_on_statusbar('This media\'s probe file no longer exists.')
                return

            # delete or open probe file
            if delete:
                try: os.remove(path)
                except: log_on_statusbar(f'Failed to delete probe file at {path}: {format_exc()}')
            else:
                qthelpers.openPath(path)
        except:
            log_on_statusbar(f'(!) Probe file opening/deletion failed: {format_exc()}')


    def add_subtitle_files(self, *files: str | QtCore.QUrl):
        ''' Adds an arbitrary number of `files` as subtitle tracks,
            if possible. `files` may be paths or `QUrl`s. '''
        urls = []
        for file in files:
            if isinstance(file, QtCore.QUrl):
                urls.append(file)
            else:
                urls.append(QtCore.QUrl.fromLocalFile(file))

        enable = settings.checkAutoEnableSubtitles.isChecked()
        for url in urls:
            if player.add_subtitle_track(url.url(), enable=enable) and enable:
                self.last_subtitle_track = player.get_subtitle_track_count()
                self.tracks_were_changed = True


    def discover_subtitle_files(self):
        ''' Detects and adds .srt subtitle files that start
            with `self.video`'s extensionless basename. '''
        dirname, basename = os.path.split(self.video)
        basename_no_ext = os.path.splitext(basename)[0]
        self.add_subtitle_files(*glob.glob(f'{dirname}{sep}{basename_no_ext}*.srt'))


    def search_files(
        self,
        prompt: str = '',
        folder: str = '',
        auto_glob: bool = True,
        auto_popup: bool = False
    ) -> list[str] | None:
        ''' Searches for `prompt` (or `self.lineOutput.text()`) relative to
            `folder` (or `self.video`'s folder). If `prompt` doesn't exist,
            `glob` is used to get results. If `auto_glob` is True, wildcards
            will be inserted into `prompt` before searching. If `auto_popup`
            is True, results are displayed under the output textbox in an
            interactive combobox (maximum of ~1000 results). Otherwise, the
            result list is returned. Automatically reuses previous prompts
            and selected indexes when appropriate. '''
        try:
            old_oscwd = os.getcwd()
            recent_searches = self.recent_searches

            # decide where to search relative to, including fallback if we haven't opened anything yet
            new_oscwd = folder or os.path.dirname(self.video)
            if not new_oscwd:
                if self.recent_files:                       # fallback to most recent file if we have one
                    show_on_statusbar('(Searching relative to most recent file\'s folder)', 20000)
                    new_oscwd = os.path.dirname(self.recent_files[-1])
                else:                                       # fallback to pyplayer's folder otherwise
                    show_on_statusbar('(Searching relative to installation folder)', 20000)
                    new_oscwd = constants.CWD
            os.chdir(new_oscwd)                             # this allows things like `abspath()`, '.', and '..'

            # get search prompt from output textbox.
            # get search text. if it's just the name of the media, check if we...
            # ...just did a search to get here and reuse our last search if so
            search = prompt or abspath(self.lineOutput.text().strip().strip('\'"') or '*')
            dirname, basename = os.path.split(search)
            if self.last_search_open_time == self.last_open_time and basename == self.last_search_open_output:
                search = self.last_search_open_prompt       # same opening time + output text hasn't changed = reuse last prompt

            if exists(search):                              # TODO: make this a setting?
                files = [search]
            else:
                if auto_glob:
                    if '*' in search or '?' in search:      # search is a glob -> use as-is, plus a * at the end
                        search += '*'
                    else:                                   # search is NOT a glob -> insert several *
                        basename_no_ext, ext = os.path.splitext(basename)
                        search = f'{dirname}{sep}*{basename_no_ext}*{ext}*'
                files = glob.glob(search)                   # execute search, add it to our recent searches, and default...
                recent_searches.setdefault(search, 0)       # ...the selected index to 0 if we haven't searched for it before

            # overlay hidden combobox over textbox, fill it with our results, and display its dropdown
            # NOTE: we SHOULD implement our own version with `QAbstractItemView` and stuff, but... lol
            if not files:
                show_on_statusbar('No results')
            elif len(files) == 1 and files[0] == self.video:
                show_on_statusbar('No results besides the currently open file')
            elif files:
                if not auto_popup:
                    return files                            # return files if we don't want a popup
                else:
                    def select(combo: QtW.QComboBox, text: str):
                        path = f'{dirname}{sep}{text}'
                        if path != self.video:              # don't use local alias here
                            self.open(file=path)            # ↓ save search, new output text, and timestamp
                            self.last_search_open_prompt = search
                            self.last_search_open_output = self.lineOutput.text()
                            self.last_search_open_time = self.last_open_time
                        if len(files) > 1:                  # do NOT reopen popup if there was only one file to pick
                            combo.showPopup()               # save search + our selected index (it's accurate here)
                            recent_searches[search] = combo.currentIndex()
                            if len(recent_searches) > 10:   # limit recent searches to the last 10
                                del recent_searches[recent_searches.keys()[0]]

                    # TODO: should we see if `self.video` is in `files` BEFORE truncating results?
                    old_index = recent_searches.get(search) or (files.index(self.video) if self.video in files else 0)

                    self.show_search_popup(
                        files,
                        widget=self.lineOutput,
                        item_labels=(f[len(dirname) + len(sep):] for f in files),
                        max_visible=9,                      # ^ strip folders from file labels inside combobox
                        selected_index=old_index,
                        on_select=select
                    )
        except:
            log_on_statusbar(f'(!) Failed to generate popup for similar files: {format_exc()}')
        finally:
            os.chdir(old_oscwd)                             # restore whatever folder `os` thinks we're in no matter what


    def explore(self, path: str = None, noun: str = 'Recent file'):
        ''' Opens `path` (or self.video if not provided) in the default file
            explorer, with `path` pre-selected if possible. `noun` controls
            how `path` is described in any log messages.'''
        if not path:
            path = self.video if self.video else cfg.lastdir
        if not exists(path):
            if path in self.recent_files:
                self.recent_files.remove(path)
            return log_on_statusbar(f'{noun} "{path}" no longer exists.')
        qthelpers.openPath(path, explore=True)


    def copy(self, path: str = None, noun: str = 'Recent file'):
        ''' Copies `path` (or self.video if not provided) to the clipboard,
            with backslashes escaped (if desired) and surrounded by quotes.
            `noun` controls how `path` is described in any log messages. '''
        if not path:
            path = self.video or cfg.lastdir
        if not exists(path):
            if path in self.recent_files:
                self.recent_files.remove(path)
            return log_on_statusbar(f'{noun} "{path}" no longer exists.')
        else:
            if settings.checkCopyEscapeBackslashes.isChecked():
                sep = '\\'
                escaped_sep = r'\\'
                app.clipboard().setText(f'"{path.replace(sep, escaped_sep)}"')
            else:
                app.clipboard().setText(f'"{path}"')


    def copy_file(self, path: str = None, cut: bool = False):
        ''' Copies the file at `path` to the clipboard. If `path` is not
            specified, `self.video` is used if possible. If `cut` is True, the
            file will be moved to its new destination rather than copied once
            pasted (currently Windows-only). '''
        if not path:
            if not self.video:
                return show_on_statusbar('No media is playing.')
            path = self.video
        if not exists(path):
            return log_on_statusbar(f'File "{path}" no longer exists.')

        mime = QtCore.QMimeData()
        mime.setUrls((QtCore.QUrl.fromLocalFile(path),))

        # https://stackoverflow.com/questions/47443545/cut-and-paste-clipboard-exchange-between-qt-application-and-windows-explorer
        # this is total nonsense and I have no idea why this works
        if cut:
            if constants.IS_WINDOWS:
                data = QtCore.QByteArray()
                stream = QtCore.QDataStream(data, QtCore.QIODevice.WriteOnly)
                magic = QtCore.QByteArray()         # you HAVE to do these two lines
                stream << magic                     # we are bitshifting literally nothing into the data stream
                mime.setData('Preferred DropEffect', data)
                if path == self.video:              # stop player if necessary so we can actually paste the file somewhere
                    self.stop()
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
                if not self.video:
                    return
                path = self.video
            if not exists(path) and not (mime == 'image' and path == self.video):
                return show_on_statusbar(f'Image "{path}" no longer exists.', 10000)
            if self.is_audio_without_cover_art:
                if not can_load_cover_art():
                    return show_on_statusbar('You have cover art detection disabled.', 10000)
                return show_on_statusbar('You can only snapshot audio with cover art.', 10000)

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
            # NOTE: if the cover art is loaded but hidden, `self.snapshot()` will still get it
            if snapshot_needed:
                path = self.snapshot(mode='full' if extended else 'quick', is_temp=True)
                if path is None:                    # dialog cancelled (finally-statement ensures we unpause if needed)
                    return
                temp_string = ' Temporary snapshot file has been deleted.'
            elif extended:
                if self.is_gif: image_player.gif.setPaused(True)
                else: player.set_pause(True)
                width, height, quality, _, _ = self.show_size_dialog(show_quality=True)
                if width is None:                   # dialog cancelled (finally-statement ensures we unpause if needed)
                    return

            log_on_statusbar('Copying image data to clipboard...')
            if not self.actionCrop.isChecked():     # no crop - copy entire image/frame
                if extended:
                    try:    # if `path` still equals `self.video`, that means it wasn't snapshotted -> must be an image
                        if path == self.video: image = get_PIL_Image().fromqpixmap(image_player.pixmap())
                        else:                  image = get_PIL_Image().open(path)
                        if width or height:
                            image = image.resize((width, height))
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
                        if self.is_gif: app.clipboard().setImage(image_player.gif.currentImage())         # `setImage()` is faster
                        else:           app.clipboard().setPixmap(image_player.pixmap())                  # <- doesn't matter how we access the...
                    else:               app.clipboard().setImage(QtGui.QImage(path))                      # ...pixmap here, it'll always be valid
                log_on_statusbar(f'Image data for "{os.path.basename(path)}" copied to clipboard.{temp_string}')
            else:                                   # crop image/frame and copy crop region
                try:    # no with-statement here just in case Pillow doesn't close `image` when it gets reassigned
                    if path == self.video: image = get_PIL_Image().fromqpixmap(image_player.pixmap())
                    else:                  image = get_PIL_Image().open(path)

                    # calculate factors between media's native resolution and actual desired snapshot resolution
                    if not snapshot_needed:                         # snapshot() already cropped the snapshot for us
                        if width or height:                         # custom width and/or height is set
                            if width:
                                x_factor = self.vwidth / width
                                if not height:                      # width is set but height isn't -> match factors
                                    y_factor = x_factor
                            if height:
                                y_factor = self.vheight / height
                                if not width:                       # height is set but width isn't -> match factors
                                    x_factor = y_factor
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
                qthelpers.deleteTempPath(path, 'snapshot')
        except:
            log_on_statusbar(f'(!) Image copying failed: {format_exc()}')
        finally:                                    # restore pause-state before leaving
            if self.is_gif: image_player.gif.setPaused(self.is_paused)
            else: player.set_pause(self.is_paused)


    def parse_media_file(
        self,
        file: str,
        probe_file: str = None,
        mime: str = 'video',
        extension: str = None,
        probe_data: dict = None
    ) -> int:
        ''' Parses a media `file` for relevant metadata and updates properties
            accordingly. Emits `self._open_cleanup_signal`. Returns 1 if
            successful, otherwise returns a string containing the reason for
            failure. This could be simpler, but it still needs to be fast.

            The following properties should be set by this function:
                - `self.mime_type`
                - `self.extension`
                - `self.video`                (the current media's path)
                - `self.duration`             (media duration in seconds)
                - `self.duration_rounded`     (duration rounded to 2 places)
                - `self.frame_count`          (number of frames starting from 0)
                - `self.frame_count_raw`      (number of frames starting from 1)
                - `self.frame_rate`           (frames per second)
                - `self.frame_rate_rounded`   (fps rounded to nearest int)
                - `self.delay`                (delay between frames in seconds)
                - `self.vwidth`               (media width)
                - `self.vheight`              (media height)
                - `self.ratio`                (aspect ratio, as a string) '''

        # remember our original mime in case we need to change it later
        base_mime = mime

        # >>> videos <<<
        try:
            if mime == 'video':
                if probe_file:                      # `probe_file` can be None if FFprobe is disabled
                    if probe_data or not player.is_parsed():
                        start = get_time()
                        if probe_data is None:      # VLC not finished, no data provided, but probe file is being generated
                            while not exists(probe_file):
                                sleep(0.01)
                            with open(probe_file, 'r', encoding='utf-8') as probe:
                                while probe_data is None:
                                    try:
                                        probe_data = parse_json(probe.read())
                                    except:
                                        if player.is_parsed():
                                            logging.info(f'VLC finished parsing while waiting for FFprobe ({get_time() - start:.4f} seconds).')
                                            break
                                        if get_time() - start > 5:
                                            logging.error('Media probe did not finish after 5 seconds.')
                                            raise AssertionError('video probing timed out')
                                        probe.seek(0)

                        if probe_data:              # double check if data was actually acquired
                            logging.info(f'FFprobe needed an additional {get_time() - start:.4f} seconds to parse.')
                            for stream in probe_data['streams']:
                                if stream['codec_type'] == 'video' and stream['avg_frame_rate'] != '0/0':
                                    fps_parts = stream['avg_frame_rate'].split('/')
                                    fps = int(fps_parts[0]) / int(fps_parts[1])
                                    duration = float(probe_data['format']['duration'])
                                    frame_count = math.ceil(duration * fps)     # NOTE: nb_frames is unreliable for partially corrupt videos

                                    self.duration = duration
                                    self.duration_rounded = round(duration, 2)
                                    self.frame_count_raw = frame_count
                                    self.frame_count = max(1, frame_count - 1)
                                    self.frame_rate = fps
                                    self.frame_rate_rounded = round(fps)
                                    self.delay = 1 / fps

                                    self.vwidth = int(stream['width'])
                                    self.vheight = int(stream['height'])
                                    self.ratio = stream.get('display_aspect_ratio', get_ratio_string(self.vwidth, self.vheight))
                                    break
                            else:                   # the rare for-else-loop ("else" only happens if we don't break)
                                mime = 'audio'      # audio streams usually report 0/0
                            logging.info('FFprobe parsed faster than player.')

                # still no FFprobe probe data, we MUST wait for player to finish (if it ever does)
                if probe_data is None:
                    if not player.is_parsed():
                        start = get_time()          # get_parsed_status() == 4 means parsing is apparently done, but values are often not accessible immediately
                        while not player.is_parsed():
                            if get_time() - start > 5:
                                logging.error('FFprobe is disabled and player did not finish parsing after 5 seconds.')
                                raise AssertionError('video parsing timed out')
                        logging.info(f'Player needed an additional {get_time() - start:.4f} seconds to parse.')
                    elif probe_file:
                        logging.info('Player did not need additional time to parse.')

                    fps = round(player.get_fps(), 1)
                    duration = round(player.get_duration(), 4)
                    frame_count = int(duration * fps)
                    self.duration = duration
                    self.duration_rounded = round(duration, 2)
                    self.frame_count_raw = frame_count
                    self.frame_count = max(1, frame_count - 1)
                    self.frame_rate = fps
                    self.frame_rate_rounded = round(fps)
                    self.delay = 1 / fps
                    self.vwidth, self.vheight = player.get_dimensions()
                    self.ratio = get_ratio_string(self.vwidth, self.vheight)
                    logging.info('VLC parsed faster than FFprobe.')
                elif probe_data == {}:
                    raise AssertionError('video probe returned no data')

        # >>> audio <<<
            if mime == 'audio':
                if probe_data:
                    for stream in probe_data['streams']:
                        if stream['codec_type'] == 'video' and stream['avg_frame_rate'] == '0/0':
                            probe_data = None       # audio file has 0fps video stream -> most likely cover art
                            break                   # set data back to None and break so we can extract the cover art
                    else:                           # the rare for-else-loop (else only happens if we don't break)
                        duration = float(probe_data['format']['duration'])
                    self.vwidth = 16
                    self.vheight = 9

                # no data provided OR art detected (see above), use `TinyTag` (fallback to `music_tag` if necessary)
                if probe_data is None:              # we need to avoid parsing probe file anyway, since we need to check for cover art
                    try:
                        try:                        # https://pypi.org/project/tinytag/0.18.0/
                            tag = TinyTag.get(file, image=can_load_cover_art())
                            art = self.cover_art_buffer = tag._image_data
                            duration = tag.duration                 # ^ this will be None if there's no image (or `image` was False)
                        except:
                            logging.info('`TinyTag` failed to identify audio, resorting to `music_tag`...')
                            import music_tag                        # only import `music_tag` if we absolutely need to
                            tag = music_tag.load_file(file)
                            if can_load_cover_art() and 'artwork' in tag:
                                art = self.cover_art_buffer = tag['artwork'].first.data
                            else:                                   # ^ NOTE: `.first` has its own width/height properties but this is cleaner
                                art = self.cover_art_buffer = None
                            duration = tag['#length'].value

                        # display cover art if it was loaded (NOTE: we can slightly optimize this...
                        # ...for `music_tag`, but that's a rare scenario and this is way cleaner)
                        if art and can_show_cover_art():
                            play_image(art, coverart=True, interactable=False)
                            size = image_player.art.size()
                            self.vwidth = size.width()
                            self.vheight = size.height()
                        else:
                            self.vwidth = 16        # NOTE: we don't need `else: play_image(None)` here because...
                            self.vheight = 9        # ...it is already cleared automatically just before parsing

                        # TODO worth saving the cover art to a temp file for future use?
                        #image_player.art.save(os.path.join(constants.TEMP_DIR, f'{os.path.basename(file)}_{getctime(file)}.png'))
                    except:                                         # this is to handle things that wrongly report as audio, like .ogv files
                        logging.info(f'Invalid audio file detected, parsing as a video file... {format_exc()}')
                        if probe_file:
                            start = get_time()
                            while not exists(probe_file):
                                sleep(0.01)
                            with open(probe_file, 'r', encoding='utf-8') as probe:
                                while probe_data is None:
                                    try:
                                        probe_data = parse_json(probe.read())
                                    except:
                                        if get_time() - start > 5:
                                            logging.error('Media probe did not finish after 5 seconds.')
                                            raise AssertionError('audio parsing timed out')
                                        probe.seek(0)
                        return self.parse_media_file(file, probe_file, mime='video', extension=extension, probe_data=probe_data)
                elif probe_data == {}:
                    raise AssertionError('audio probe returned no data')

                frame_count_raw = round(duration * 20)
                self.duration = duration
                self.duration_rounded = round(duration, 2)
                self.frame_count_raw = frame_count_raw
                self.frame_count = max(1, frame_count_raw - 1)
                self.frame_rate = 20                # TODO we only set to 20 to not deal with laggy hover-fades
                self.frame_rate_rounded = 20
                self.delay = 0.05
                self.ratio = get_ratio_string(self.vwidth, self.vheight)

        # >>> images <<<
            elif mime == 'image':
                if extension == 'gif' and image_player.gif.frameCount() > 1:
                    self.frame_count_raw = image_player.gif.frameCount()
                    self.frame_count = image_player.gif.frameCount() - 1
                    if probe_data:                  # use probe data if available but it's not necessary
                        for stream in probe_data['streams']:
                            if stream['codec_type'] == 'video' and stream['avg_frame_rate'] != '0/0':
                                fps_parts = stream['avg_frame_rate'].split('/')
                                fps = int(fps_parts[0]) / int(fps_parts[1])
                                duration = float(probe_data['format']['duration'])
                        self.duration = duration
                        self.duration_rounded = round(duration, 2)
                        self.frame_rate = fps
                        self.frame_rate_rounded = round(fps)
                        self.delay = 1 / fps
                        self.vwidth = int(stream['width'])
                        self.vheight = int(stream['height'])
                    else:
                        delay = image_player.gif.nextFrameDelay() / 1000
                        duration = self.frame_count_raw * delay
                        self.delay = delay
                        self.duration = duration
                        self.duration_rounded = round(duration, 2)
                        self.frame_rate = 1 / self.delay
                        self.frame_rate_rounded = round(self.frame_rate)
                        self.vwidth = image_player.gifSize.width()
                        self.vheight = image_player.gifSize.height()
                    self.ratio = get_ratio_string(self.vwidth, self.vheight)
                else:   # TODO: other formats have EXIF data but .getexif() is slow for images without EXIF data (except for jpegs)
                    if extension == 'jpeg':                         # use PIL to get EXIF data from jpegs
                        with get_PIL_Image().open(file) as image:   # opening with PIL is fast if we don't do any operations
                            orientation = image.getexif().get(0x0112)
                            if orientation:
                                if   orientation == 3: angle = 180
                                elif orientation == 6: angle = 90   # actually represents 270 counter-clockwise
                                elif orientation == 8: angle = 270  # actually represents 90 counter-clockwise
                                else:                  angle = 0
                                if angle:
                                    image_player.art = image_player.art.transformed(QtGui.QTransform().rotate(angle))
                            try:
                                self.vwidth, self.vheight = image.size
                            except AttributeError:
                                self.vwidth = image_player.art.width()
                                self.vheight = image_player.art.height()
                    else:
                        self.vwidth = image_player.art.width()
                        self.vheight = image_player.art.height()
                    self.duration = 0.0000001       # low duration to avoid errors but still show up as 0 on the UI
                    self.duration_rounded = 0.0
                    self.frame_count_raw = 1        # NOTE: these CANNOT be 0
                    self.frame_count = 1
                    self.frame_rate = 1
                    self.frame_rate_rounded = 1
                    self.delay = 0.2                # run `update_slider_thread()` only 5 times/second
                    self.ratio = get_ratio_string(self.vwidth, self.vheight)

            assert self.duration != 0, 'invalid duration'
        except AssertionError as error:
            logging.error(f'(!) Parsing failure: {format_exc()}')
            self._open_cleanup_in_progress = False  # ensure that this gets reset
            return str(error)
        except:
            logging.error(f'(!) Unexpected parsing failure: {format_exc()}')
            self._open_cleanup_in_progress = False
            return 'parsing failed for unknown reason - see log file'

    # >>> extra setup <<< (frame_rate_rounded, ratio, delay, etc. could be set down here, but it would be slower overall)
        # mark that cleanup is about to start - setting this here makes it impossible to leave `self.open()`...
        # ...with this being improperly set, avoiding scenarios where `self.open_in_progress` gets stuck on True
        self._open_cleanup_in_progress = True

        self.video = file                           # set media AFTER opening but BEFORE _open_cleanup_signal
        self.mime_type = mime
        self.extension = extension
        #self.resolution_label = f'{self.vwidth:.0f}x{self.vheight:.0f}'

    # >>> alias setup <<< (this could be optimized by doing it above, but i don't FEEL like it)
        if base_mime == 'image':
            # see if this is an animated or static image
            is_gif = extension == 'gif' and self.frame_count_raw > 1
            self.is_gif = is_gif                    # do not treat single-frame GIFs as actual GIFs (static images have more features)
            self.is_static_image = not is_gif

            # disable all audio/video-related bandaid properties
            self.is_audio_with_cover_art = False
            self.is_audio_without_cover_art = False

        else:
            self.is_gif = False
            self.is_static_image = False

            if mime == 'audio':
                has_cover_art = bool(self.cover_art_buffer)
                self.is_audio_with_cover_art = has_cover_art
                self.is_audio_without_cover_art = not has_cover_art
            else:
                self.is_audio_with_cover_art = False
                self.is_audio_without_cover_art = False

        # emit event for player backend
        player.on_parse(file, base_mime, mime, extension)
        return 1


    def open(
        self,
        file: str = None,
        focus_window: bool = None,
        flash_window: bool = True,
        pause_if_focus_rejected: bool = False,
        beep_if_focus_rejected: bool = False,
        update_recent_list: bool = True,
        update_raw_last_file: bool = True,
        update_original_video_path: bool = True,
        mime: str = None,
        extension: str = None,
        _from_cycle: bool = False,
        _from_autoplay: bool = False,
        _from_edit: bool = False
    ) -> int:
        ''' Opens, parses, and plays a media `file`. Returns -1 if unsuccessful.

            If `file` is None, a file-browsing dialog will be opened.
            If no `mime` or `extension` are provided, they will be detected
            automatically. If `focus_window` is None, the window will focus
            depending on its current state, the media type, and user settings.
            If the window remains unfocused, a notification sound will play if
            `beep_if_focus_rejected` is True and the player will start paused
            if `pause_if_focus_rejected` is True (does not apply to GIFs).

            - `update_recent_list` - updates `self.recent_files`
            - `update_raw_last_file` - updates `self.last_video`
            - `update_original_video_path` - updates `self.original_video_path`

            If `_from_cycle` is True, validity checks are skipped.
            `self.current_file_is_autoplay` is set to `_from_autoplay`.

            Current iteration: IV '''

        try:
            # validate `file`. open file-dialog if needed, check if it's a folder, check if it's locked, etc.
            # (if called from sort of auto-cycling function, we can assume this stuff is already sorted out)
            if not _from_cycle:
                if not file:
                    file, cfg.lastdir = qthelpers.browseForFile(
                        lastdir=cfg.lastdir,
                        caption='Select media file to open'
                    )
                if not file:
                    return -1
                file = abspath(file)                        # ensure `file` uses a standardized format

                if os.path.isdir(file):
                    file = self.open_folder(file, focus_window=focus_window)
                    return 1 if file else -1
                if file in self.locked_files:               # if file is locked and we didn't cycle here, show a warning message
                    show_on_statusbar(f'File {file} is currently being worked on.')
                    return -1

            # get stats and size of media
            start = get_time()
            stat = os.stat(file)
            filesize = stat.st_size
            basename = file[file.rfind(sep) + 1:]           # shorthand for os.path.basename NOTE: safe when `file` is provided automatically

        # --- Probing file and determining mime type ---
            # probe file with FFprobe if possible. if file has already been probed, reuse old probe. otherwise, save output to txt file
            # probing calls Popen through a Thread (faster than calling Popen itself or using Thread on a middle-ground function)
            if FFPROBE:                                     # generate probe file's path and check if it already exists
                probe_file = f'{constants.PROBE_DIR}{sep}{basename}_{stat.st_mtime}_{filesize}.txt'
                probe_exists = exists(probe_file)
                if probe_exists:                            # probe file already exists
                    with open(probe_file, 'r', encoding='utf-8') as probe:
                        try:
                            probe_data = parse_json(probe.read())
                            probe_process = None
                            if not probe_data:              # probe is literally just two braces with no data -> DON'T...
                                raise                       # ...give up. instead, raise error and try to re-probe it
                        except:
                            probe.close()
                            logging.info('(?) Deleting potentially invalid probe file: ' + probe_file)
                            try: os.remove(probe_file)
                            except: logging.warning('(!) FAILED TO DELETE POTENTIALLY INVALID PROBE FILE: ' + format_exc())
                            probe_exists = False

                if not probe_exists:
                    probe_data = None
                    probe_process = subprocess.Popen(
                        f'"{FFPROBE}" -show_format -show_streams -of json "{file}" > "{probe_file}"',
                        shell=True                          # needed so we can easily write the output to a file
                    )
            elif player.SUPPORTS_PARSING:
                probe_file = None                           # no FFprobe -> no probe file (even if one exists already)
                probe_data = None
                probe_process = None
            else:
                qthelpers.getPopup(
                    title='Welp.',
                    text='You have FFprobe disabled, but have also selected a\nplayer that cannot sufficiently parse media on its own.\n\nDo you see the issue?',
                    icon='warning',
                    **self.get_popup_location_kwargs()
                ).exec()
                raise AssertionError('FFprobe disabled and player does not support probing')

            # misc variables we can setup after probe has started
            old_file = self.video
            extension_label = ''
            mime_fallback_was_needed = False

            # get mime type of file (if called from cycle, then this part was worked out beforehand)
            if mime is None:
                try:
                    filetype_data = filetype.match(file)    # 'EXTENSION', 'MIME', 'extension', 'mime'
                    mime, extension = filetype_data.mime.split('/')
                    extension_label = extension.upper()
                    if mime not in ('video', 'image', 'audio'):
                        log_on_statusbar(f'File \'{file}\' appears to be corrupted or an invalid format and cannot be opened (invalid mime type).')
                        return -1

                # failed to determine mime type -> our library isn't 100% perfect, so...
                # ...wait for probe file to be created and attempt to parse it anyway
                except:
                    try:
                        if not FFPROBE:
                            raise

                        mime_fallback_was_needed = True
                        log_on_statusbar('The current file\'s mime type cannot be determined, checking FFprobe...')

                        # if FFprobe process is still running, wait for it. we could parse its...
                        # ...output directly, but it doesn't really matter for such a rare situation
                        if probe_process is not None:
                            while True:
                                if probe_process.poll() is not None:
                                    break                   # ^ returns None if process hasn't terminated yet

                        # wait for probe file to be created
                        while not exists(probe_file):
                            sleep(0.02)

                        # attempt to parse probe file. if successful, this might be actual media
                        with open(probe_file, 'r', encoding='utf-8') as probe:
                            while probe_data is None:
                                if probe.read():            # keep reading until the file actually contains data
                                    sleep(0.1)
                                    probe.seek(0)
                                    probe_data = parse_json(probe.read())

                        # for some asinine reason, FFprobe "recognizes" text as a form of video
                        # if that, or probe is literally just two braces with no data -> give up
                        if not probe_data or probe_data['format']['format_name'] == 'tty':
                            raise

                        # if there are no valid video streams, assume it's an audio file
                        for stream in probe_data['streams']:
                            if stream['codec_type'] == 'video' and stream['avg_frame_rate'] != '0/0':
                                mime = 'video'
                                break
                        else:
                            mime = 'audio'                  # for-loop goes to "else" if the loop did not break

                        # check known problem-formats to assign extension
                        # fallback to current extension if it's at least valid for this mime type
                        # resort to '???' if we genuinely have no idea what this is
                        if probe_data['format']['format_name'] == 'mpegts':
                            extension = 'mp4'
                            extension_label = 'MPEG-TS'
                        else:
                            if mime == 'video': valid_extensions = constants.VIDEO_EXTENSIONS
                            else:               valid_extensions = constants.AUDIO_EXTENSIONS
                            _, extension = splitext_media(file, valid_extensions, period=False)
                            if not extension:
                                extension = 'mp4' if mime == 'video' else 'mp3'
                                extension_label = '???'

                    except:
                        if not exists(file): log_on_statusbar(f'File \'{file}\' does not exist.')
                        else: log_on_statusbar(f'File \'{file}\' appears to be corrupted or an invalid format and cannot be opened (failed to determine mime type).')
                        logging.warning(format_exc())
                        return -1

        # --- Restoring window ---
            # restore window from tray if hidden, otherwise there's a risk for unusual VLC output
            if self.isVisible():
                was_minimzed_to_tray = False
            else:                                           # we need to do this even if `focus_window` is True
                was_minimzed_to_tray = True
                if self.isMaximized():
                    self.resize(self.last_window_size)      # restore size/pos or maximized windows will forget...
                    self.move(self.last_window_pos)         # ...their original geometry when you unmaximize them
                self.showMinimized()                        # minimize for now, we'll check if we need to focus later

        # --- Playing media ---
            self.open_in_progress = True                    # mark that we're now officially opening something

            player.stop()                                   # player must be stopped for images/gifs and to reduce delays on almost-finished media (for VLC)
            if mime == 'image': play_image(file, gif=extension == 'gif')
            elif not play(file): return -1                  # immediately attempt to play media once we know it might be valid
            else: play_image(None)                          # clear gifPlayer if we successfully played non-gif media

            # this and `_open_cleanup_in_progress` (set in `self.parse_media_file()`) are internal...
            # ...properties for tracking when it's safe to set `self.open_in_progress` back to False
            self._open_main_in_progress = True              # (set this here instead of above to slightly optimize cycling through corrupt files)

        # --- Parsing metadata and setting up UI/recent files list ---
            # parse non-video files and show/log file on statusbar
            parsed = False                                  # keep track of parse so we can avoid re-parsing it later if it ends up being a video
            if mime != 'video':                             # parse metadata early if it isn't a video
                if (reason := self.parse_media_file(file, probe_file, mime, extension, probe_data)) != 1:
                    log_on_statusbar(f'File \'{file}\' appears to be corrupted or an invalid format and cannot be opened ({reason}).')
                    return -1
                parsed = True

            logging.info('--- OPENING FILE ---')
            if not mime_fallback_was_needed: log_on_statusbar(f'Opening file ({mime}/{extension}): {file}')
            else: log_on_statusbar(f'This file is seemingly playable, but PyPlayer is unsure of its true mime-type/extension: {file}')

            # misc cleanup/setup for new media that we can safely do before fully parsing
            self.operations.clear()
            self.buttonTrimStart.setChecked(False)
            self.buttonTrimEnd.setChecked(False)

            # set basename (w/o extension) as default output text,...
            # ...full basename as placeholder text, and update tooltip
            self.lineOutput.setText(splitext_media(basename)[0])
            self.lineOutput.setPlaceholderText(basename)    # TODO: should these two lines be in cleanup anyway?
            self.lineOutput.setToolTip(file + constants.OUTPUT_TEXTBOX_TOOLTIP_SUFFIX)

            # update delete-action's QToolButton. if we're holding del, auto-mark the file accordingly
            if self.mark_for_deletion_held_down:            # NOTE: we don't update the tooltip until we've release del
                is_marked = self.mark_for_deletion_held_down_state
                if is_marked: self.marked_for_deletion.add(file)
                else:         self.marked_for_deletion.discard(file)
            else:
                is_marked = file in self.marked_for_deletion
            self.actionMarkDeleted.setChecked(is_marked)
            self.buttonMarkDeleted.setChecked(is_marked)

            # reset cropped mode if needed
            if self.actionCrop.isChecked():                 # `self.set_crop_mode` auto-returns if `self.mime_type` is 'audio'
                self.disable_crop_mode()

            # set size label for context menus and titlebar
            if filesize < 1048576:      self.size_label = f'{filesize / 1024:.0f}kb'
            elif filesize < 1073741824: self.size_label = f'{filesize / 1048576:.2f}mb'
            else:                       self.size_label = f'{filesize / 1073741824:.2f}gb'

            # extra setup before we absolutely must wait for the media to finish parsing
            # NOTE: this (and some of the above) is a disaster if we fail to parse, but...
            #      ...it's very rare for a file to get this far if it can't be parsed
            self.is_paused = False                          # slightly more efficient than using `force_pause`
            self.buttonPause.setIcon(self.icons['pause'])
            self.restarted = False
            self.lineOutput.clearFocus()                    # clear focus from output line so it doesn't interfere with keyboard shortcuts
            self.current_file_is_autoplay = _from_autoplay
            self.extension_label = extension_label or extension.upper()
            self.stat = stat

            # focus window if desired, depending on window state and autoplay/audio settings
            # NOTE: it is very rare but possible for "video" mime types to be mutated into "audio"...
            #       ...during parsing which happens immediately AFTER we focus the window. i'd...
            #       ...still rather focus first. it's rare enough that i think it's probably fine
            if not self.isActiveWindow():
                if not _from_edit:
                    if _from_cycle and settings.checkFocusIgnoreAutoplay.isChecked():
                        focus_window = False
                    elif mime == 'audio' and settings.checkFocusIgnoreAudio.isChecked():
                        focus_window = False

                if focus_window is None:
                    if self.isMinimized():
                        if was_minimzed_to_tray: focus_window = settings.checkFocusOnMinimizedTray.isChecked()
                        else:                    focus_window = settings.checkFocusOnMinimizedTaskbar.isChecked()
                    elif self.isFullScreen():    focus_window = settings.checkFocusOnFullscreen.isChecked()
                    elif self.isMaximized():     focus_window = settings.checkFocusOnMaximized.isChecked()
                    else:                        focus_window = settings.checkFocusOnNormal.isChecked()
                if focus_window and settings.checkFocusIgnoreFullscreen.isChecked():
                    if _from_edit or not settings.checkFocusIgnoreFullscreenEditsOnly.isChecked():
                        focus_window = not foreground_is_fullscreen()
                if focus_window:
                    qthelpers.showWindow(
                        window=self,
                        aggressive=settings.checkFocusAggressive.isChecked()
                    )
                else:
                    if pause_if_focus_rejected:
                        self.force_pause(True)
                    if beep_if_focus_rejected:
                        app.beep()
                    if flash_window and constants.IS_WINDOWS:
                        flash_count = (0, 1, 2, -1)[settings.comboTaskbarFlash.currentIndex()]
                        if flash_count == 1:    qthelpers.flashWindow(self, duration=1100, hold=True)
                        elif flash_count == -1: qthelpers.flashWindow(self, flash_count)
                        else:                   qthelpers.flashWindow(self, flash_count, interval=500, duration=1250 * flash_count)

            # if presumed to be a video -> finish parsing (done as late as possible to minimize downtime)
            if mime == 'video' and not parsed:
                if (reason := self.parse_media_file(file, probe_file, mime, extension, probe_data)) != 1:
                    log_on_statusbar(f'File \'{file}\' appears to be corrupted or an invalid format and cannot be opened ({reason}).')
                    return -1

            # update original path and literal last video if this is a new file and not an edit
            if update_original_video_path or not self.video_original_path:
                self.video_original_path = file
                if update_raw_last_file:
                    self.last_video = old_file

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
            # TODO: would local and/or global aliases here be worth it?
            h, m, s, ms = get_hms(self.duration_rounded)
            self.labelMaxTime.setText(f'{m:02}:{s:02}.{ms:02}' if h == 0 else f'{h}:{m:02}:{s:02}')
            self.spinHour.setEnabled(h != 0)                            # always leave `spinSecond` enabled
            self.spinMinute.setEnabled(m != 0)
            if self.width() > 335: prefix = f'{self.frame_rate_rounded} FPS: '
            else:                  prefix = ''
            self.spinFrame.setPrefix(prefix)
            self.spinFrame.setMaximum(self.frame_count)
            self.spinFrame.setToolTip(f'Frame rate:\t{self.frame_rate}\nFrame count:\t{self.frame_count_raw}')

            # refresh title (we have to emit here instead of `_open_cleanup_slot`, I don't remember why lol)
            refresh_title()

            # log opening time. all done! (except for cleanup)
            self.last_open_time = end = get_time()                      # TODO: is using a local alias here worth it?
            logging.info(f'Initial media opening completed after {end - start:.4f} seconds.')
            return 1

        except:
            log_on_statusbar(f'(!) OPEN FAILED: {format_exc()}')
            return -1
        finally:
            self._open_main_in_progress = False
            self.open_in_progress = self._open_cleanup_in_progress or player.open_cleanup_queued


    def _open_cleanup_slot(self):
        ''' A slot for `_open_cleanup_signal` that handles updating the progress
            slider's properties, as well as various non-essential actions. This
            is done through a signal so that `update_slider_thread` itself can
            initiate the cleanup, avoiding numerous timing issues (playback
            starting at the frame the last media was playing on, etc.).

            NOTE: Putting all of `open()` in this slot results in a noticable
            delay while opening media. '''
        try:
            # reset UI to frame 0 while `self._open_cleanup_in_progress` is True
            self._open_cleanup_in_progress = True       # set this again, juuuuust in case
            update_progress(0)

            # NOTE: `sliderProgress.setMaximum` has an override -> it expects the raw count (i.e. 9000 for...
            #       ...a 9000-frame video instead of 8999) and will adjust and enable/disable accordingly
            sliderProgress = self.sliderProgress
            sliderProgress.setMaximum(self.frame_count_raw)
            self.minimum = 0
            self.maximum = sliderProgress.maximum()     # this may be different than what we just put in

            # place one tick per second/minute (cosmetic, default theme only)
            sliderProgress.setTickInterval(self.frame_rate_rounded * (1 if self.duration_rounded < 3600 else 60))

            self.vsize.setWidth(self.vwidth)
            self.vsize.setHeight(self.vheight)
            if self.is_snap_mode_enabled():
                resize_on_open_state = settings.checkResizeOnOpen.checkState()
                snap_on_open_state = settings.checkSnapOnOpen.checkState()
                if resize_on_open_state and not (resize_on_open_state == 1 and self.first_video_fully_loaded):
                    self.snap_to_native_size()          # ^ 1 -> only resize first video opened
                elif snap_on_open_state and not (snap_on_open_state == 1 and self.first_video_fully_loaded):
                    self.snap_to_player_size(force_instant_resize=True)
                elif settings.checkClampOnOpen.isChecked():
                    qthelpers.clampToScreen(self)       # clamping enabled but snap/resize is disabled
            elif settings.checkClampOnOpen.isChecked():
                qthelpers.clampToScreen(self)           # clamping enabled but snap/resize is disabled for this media

            # update taskbar icon's toolbar, reset cursor, show media title on screen
            self.refresh_taskbar()
            if settings.checkTextOnOpen.isChecked():    # certain combinations of autoplay + settings can override this marquee
                if not (settings.checkAutoplayHideMarquee.isChecked() and self.current_file_is_autoplay):
                    show_on_player(os.path.basename(self.video), 1000)

            # reset track selections/delays for new files unless player specifies otherwise
            if self.video != self.last_video:
                if player.ENABLE_AUTOMATIC_TRACK_RESET:
                    self.last_video_track = None
                    self.last_audio_track = None
                    self.last_subtitle_delay = None
                    self.last_audio_delay = None
                    if settings.checkAutoEnableSubtitles.isChecked():
                        self.last_subtitle_track = 1
                        self.tracks_were_changed = not player.SUPPORTS_AUTOMATIC_SUBTITLE_ENABLING
                    else:
                        self.last_subtitle_track = -1       # -1 -> disabled
                        self.tracks_were_changed = player.SUPPORTS_AUTOMATIC_SUBTITLE_ENABLING
                if player.ENABLE_AUTOMATIC_TRACK_RESTORATION:
                    self.restore_tracks_signal.emit(True)

            # force volume/mute-state to quickly correct gain issues (ONLY if audio is present!)
            # player doesn't always want to update immediately after first file is opened - keep trying
            # TODO: is this VLC-only?
            if self.volume_startup_correction_needed and player.get_audio_track_count() > 0:
                muted = not self.sliderVolume.isEnabled()
                volume = get_volume_slider()
                while self.set_volume(volume, verbose=False) != player.get_volume():
                    sleep(0.002)
                while self.set_mute(muted, verbose=False) == -1:
                    sleep(0.002)
                self.volume_startup_correction_needed = False

            self.videos_opened += 1                     # can't reset
            self.first_video_fully_loaded = True        # can reset

            # gifs LOVE to pause themselves randomly
            image_player.gif.setPaused(False)

            player.on_open_cleanup()
            logging.info(f'Media info:\nmime={self.mime_type}, extension={self.extension}\n'
                         f'duration={self.duration}, frames={self.frame_count_raw}, fps={self.frame_rate}, delay={self.delay:.4f}\n'
                         f'size={self.vwidth}x{self.vheight}, ratio={self.ratio}')
            logging.info('--- OPENING COMPLETE ---\n')
            gc.collect(generation=2)                    # do manual garbage collection after opening (NOTE: this MIGHT be risky)

        except:
            logging.error(f'(!) OPEN-SLOT FAILED: {format_exc()}')
        finally:                                        # if another open is queued already, stay marked as "in progress"
            self._open_cleanup_in_progress = player.open_cleanup_queued
            self.open_in_progress = self._open_main_in_progress or player.open_cleanup_queued


    def open_from_thread(self, **kwargs):
        ''' Safely calls `self.open()` from a thread by
            emitting `self._open_signal` with any provided
            keyword arguments passed as a dictionary. '''
        self._open_signal.emit(kwargs)                  # do NOT unpack dictionary


    def _open_external_command_slot(self, cmdpath: str):
        ''' Handles a command within a file at
            `cmdpath` in a thread-safe manner. '''
        try:
            with open(cmdpath, 'rb') as txt:            # paths are encoded, to support special characters
                command = txt.readline().decode().strip()
                if command == 'EXIT':
                    logging.info('(CMD) External request to close received (likely an update pending). Exiting.')
                    try: os.remove(cmdpath)             # pre-emptively remove cmdpath before closing, if possible
                    except: pass
                    qtstart.exit(self)
                else:
                    self.open(command)
                    logging.info(f'(CMD) Fast-start for {command} received and handled.')
        finally:
            self.external_command_in_progress = False   # resume fast-start interface


    def restart(self) -> int:
        ''' "Restarts" media to circumvent strange behavior across multiple
            players when they "finish" media. Returns -1 if unsuccessful, else
            None. This took far more effort to figure out than you'd think.
            If `--play-and-exit` was specified in the command line arguments,
            this function closes PyPlayer. This is connected to libVLC's event
            manager in a similar manner to signals/slots in `widgets.py`. '''
        try:
            logging.info('Restarting media (Restart VI)')
            video = self.video

            if not player.can_restart():
                return

            # ensure media still exists, otherwise warn user
            if not exists(video):
                if video:                           # certain corrupt files will trigger a false restart
                    log_on_statusbar('Current media no longer exists. You likely renamed, moved, or deleted it from outside PyPlayer.')
                self.stop(icon='x')                 # use X-icon as visual clue that something is preventing playback
                return -1

            # if we want to loop, reload video, reset UI, and return immediately
            if self.actionLoop.isChecked():
                return player.loop()

            # if we want autoplay/shuffle, don't reload -> switch immediately
            if self.actionAutoplay.isChecked():
                update_progress(0)                  # [VLC] required due to audio issue side-effect? (1st video after audio file ends instantly)
                if self.actionAutoplayShuffle.isChecked(): return self.shuffle_media(autoplay=True)
                if self.actionAutoplayDirectionDynamic.isChecked(): next = self.last_cycle_was_forward
                else: next = self.actionAutoplayDirectionForwards.isChecked()
                return self.cycle_media(
                    next=next,
                    update_recent_list=settings.checkAutoplayAddToRecents.isChecked(),
                    autoplay=True
                )

            # if we want to stop, don't reload -> stop the player and return immediately
            want_to_stop = self.mime_type == 'audio' or settings.checkStopOnFinish.isChecked()
            if want_to_stop and player.get_state() != State.Stopped:
                update_progress(self.frame_count)   # ensure UI is visually at the end
                return self.stop(icon='restart')

            # reload video in player and restore position
            player.on_restart()
            self.restarted = True

            # forcibly re-pause player if necessary (slightly more efficient than using `force_pause`)
            player.set_pause(True)
            self.is_paused = True
            self.buttonPause.setIcon(self.icons['restart'])
            refresh_title()
            self.refresh_taskbar()
            show_on_player('')                      # VLC auto-shows last marq on restart -> this trick hides it

            # ensure this is True (it resets depending on settings)
            self.first_video_fully_loaded = True

            # force-close if requested. done here so as to slightly optimize normal restarts
            if qtstart.args.play_and_exit:
                logging.info('Play-and-exit requested. Closing.')
                return qtstart.exit(self)
        except:
            logging.error(f'(!) RESTART FAILED: {format_exc()}')


    # TODO: why was I restoring instantly for images?
    def restore(self, frame: int, was_paused: bool = None):
        ''' Replays the current file & immediately restores progress to `frame`,
            pausing if the media `was_paused`. Restores tracks if supported by
            the current player. Returns immediately for images. '''
        if was_paused is None:
            was_paused = self.is_paused
        if self.mime_type == 'image':
            if self.is_gif:
                image_player.gif.setFileName(self.video)
                set_gif_position(frame)             # ^ don't need to play new path - just update filename
                if not was_paused:                  # only unpause gif if it wasn't paused before
                    self.force_pause_signal.emit(False)
                image_player.filename = self.video  # also set our custom `filename` property (needed...
            return                                  # ...in `self.pause()` but I don't remember why)

        play(self.video, will_restore=True)
        set_and_update_progress(frame, SetProgressContext.RESTORE)
        if frame >= self.frame_count:               # if the media is over, stop player again immediately since most players...
            self.stop(icon='restart')               # ...will be blacked out anyway, so we might as well release the lock
        else:                                       # this can be called from a thread -> pause with a signal
            self.force_pause_signal.emit(was_paused)
            if player.ENABLE_AUTOMATIC_TRACK_RESTORATION:
                self.restore_tracks_signal.emit(True)


    def pause(self) -> bool:
        ''' Pauses/unpauses the media. Handles updating GUI, cleaning
            up/restarting, clamping progress to current trim, displaying
            the pause state on-screen, wrapping around the progress bar. '''
        will_pause = False

        # images/gifs
        if self.mime_type == 'image':
            if self.is_gif:                         # check if gif's filename is correct. if not, restart the gif and restore position
                old_state = image_player.gif.state()
                was_paused = old_state != QtGui.QMovie.Running          # ↓ .fileName() is formatted wrong -> fix with `abspath`
                if was_paused and abspath(image_player.gif.fileName()) != image_player.filename:
                    image_player.gif.setFileName(image_player.filename)
                    set_gif_position(get_ui_frame())
                image_player.gif.setPaused(not was_paused)
                will_pause = not was_paused
                frame = image_player.gif.currentFrameNumber()
            else:                                                       # just return if it's a static image
                return True

        # videos/audio
        else:
            frame = get_ui_frame()
            old_state = player.get_state()
            if old_state == State.Stopped:
                if self.restart() == -1:                                # restart media if currently stopped
                    return True                                         # -1 means media doesn't exist anymore
                set_and_update_progress(frame, SetProgressContext.RESTORE)

            if frame >= self.maximum or frame < self.minimum:           # play media from beginning if media is over
                self.lock_progress_updates = True
                set_and_update_progress(self.minimum, SetProgressContext.RESTART)
                self.lock_progress_updates = False
            player.pause()                                              # actually pause underlying player
            will_pause = True if old_state == State.Playing else False  # prevents most types of pause-bugs...?

        # update internal property as soon as we safely can
        self.is_paused = will_pause

        # update pause button
        self.buttonPause.setIcon(self.icons['play' if will_pause else 'pause'])
        if settings.checkTextOnPause.isChecked():
            pause_text = '𝗜𝗜' if will_pause else '▶'                    # ▷ ▶ ⏵︎
            show_on_player(pause_text)

        # update titlebar and taskbar icon
        refresh_title()
        self.refresh_taskbar()
        self.restarted = False
        logging.debug(f'Pausing: is_paused={will_pause} old_state={old_state} frame={frame} maxframe={self.maximum}')
        return will_pause


    def force_pause(self, paused: bool):
        ''' Immediately set pause-state to `paused`, without
            clamping, wrapping, restarting, or showing marquees. '''
        if self.is_gif: image_player.gif.setPaused(paused)
        else: player.set_pause(paused)
        self.is_paused = paused

        icon = self.icons['play' if paused else 'pause']
        self.buttonPause.setIcon(icon)

        refresh_title()
        self.refresh_taskbar()
        logging.debug(f'Force-pause: paused={paused}')
        return paused


    def stop(self, *, icon: str = 'stop'):          # * to capture unused signal args
        ''' A more robust way of stopping - stop the player while also force-
            pausing. `icon` specifies what icon to use on the pause button. '''
        player.stop()
        image_player.gif.setFileName('')

        if self.is_gif: image_player.gif.setPaused(True)
        else: player.set_pause(True)
        self.is_paused = True
        self.buttonPause.setIcon(self.icons[icon])

        # if the media is over, mark ourselves as having NOT restarted yet -> this...
        # ...keeps us from getting confused if the media file is renamed/deleted
        if get_ui_frame() == self.frame_count:
            self.restarted = False

        refresh_title()
        self.refresh_taskbar()
        if constants.IS_WINDOWS and settings.checkTaskbarIconPauseMinimized.isChecked():
            self.taskbar.clearOverlayIcon()

        logging.debug('Player stopped.')


    def rename(
        self,
        new_name: str = None,
        sanitize: bool = True,
        delete_source_dir: bool = True,
        warn_on_replace: bool = True,
        warn_on_drive: bool = True,
        undoable: bool = True
    ):
        ''' Renames the current media to `new_name`, restoring progress
            afterwards. If `new_name` is blank, `self.lineOutput` is used.
            Otherwise, if `sanitize` is True, `new_name` is passed through
            `self.get_output()` first. If `delete_source_dir` is True, empty
            folders left behind will be recursively deleted, super-rename-style
            (destination folders will always be created). `warn_on_replace` and
            `warn_on_drive` give the user a chance to cancel the rename rather
            than replace an existing file or rename across drives. If `undoable`
            is True, an `Undo` object will be added to `self.undo_dict`. '''

        # prepare new name
        old_name = self.video
        if sanitize or not new_name:
            new_name, basename_no_ext, ext = self.get_output(new_name)
        else:
            basename_no_ext, ext = os.path.splitext(os.path.basename(new_name))
        if not new_name:                            # output was invalid, blank, or the default
            return
        if old_name in self.locked_files:
            return show_on_statusbar('Current file cannot be renamed because it is set to be overwritten.')
        if new_name in self.locked_files:           # NOTE: you can't really get this far if this is True
            return show_on_statusbar('New name cannot be used because it is set to be overwritten.')

        # see if we're currently paused then stop the player
        was_paused = self.is_paused
        self.stop()                                 # player must be stopped before we can rename

        # actually rename the media
        try:
            try:
                if exists(new_name) and warn_on_replace:
                    if qthelpers.getPopupOkCancel(
                        title='Move conflict',
                        text=f'The destination already exists: {new_name}\n\nReplace? This can\'t be undone!',
                        icon='warning',
                        **self.get_popup_location_kwargs()
                    ).exec() == QtW.QMessageBox.Ok:
                        os.makedirs(os.path.dirname(old_name), exist_ok=True)
                        os.replace(old_name, new_name)
                        if delete_source_dir:       # this is how `os.renames()` deletes its empty directories
                            try: os.removedirs(os.path.dirname(old_name))
                            except OSError: pass
                    else:                           # don't want to replace -> restore and return without error
                        self.restore(get_ui_frame(), was_paused)
                        return log_on_statusbar('Rename cancelled.')
                elif delete_source_dir:
                    os.renames(old_name, new_name)
                else:
                    os.makedirs(os.path.dirname(old_name), exist_ok=True)
                    os.rename(old_name, new_name)
                marquee(f'File renamed to {new_name}', marq_key='Save', timeout=2500)

            # source media stopped existing in the time it took to start rename
            except FileNotFoundError:               # images/gifs are cached so they can be altered behind the scenes
                if self.mime_type == 'image' and settings.checkRenameMissingImages.isChecked():
                    image_player.art.save(new_name)
                    log_on_statusbar(f'Original file no longer exists, so a copy was created at {new_name}.')
                else:
                    return log_on_statusbar(f'Current file no longer exists at {old_name}.')

            # source media is being used by something other than PyPlayer
            except PermissionError:
                return log_on_statusbar('File cannot be renamed because it is in use by another process.')

            # this is usually OSError 17, which is trying to rename across drives
            except OSError as error:
                if 'disk drive' in str(error):
                    title = 'Move across drives?'
                    if constants.IS_WINDOWS:        # drives will be blank on posix
                        source_drive = os.path.splitdrive(old_name)[0]
                        dest_drive   = os.path.splitdrive(new_name)[0]
                        title += f' ({source_drive} -> {dest_drive})'

                    # ask before moving across drives if desired, otherwise just do it
                    if not warn_on_drive or qthelpers.getPopupOkCancel(
                        title=title,
                        text='The source and destination are on different drives.\nMoving across drives may lose obscure metadata\nlike file owners and alternate data streams.\n\nContinue?',
                        **self.get_popup_location_kwargs()
                    ).exec() == QtW.QMessageBox.Ok:
                        import shutil               # NOTE: `shutil.move()` CAN move across drives (on Windows, at least)
                        shutil.move(old_name, new_name)

                    # don't want to move across drives -> restore and return without error
                    else:
                        self.restore(get_ui_frame(), was_paused)
                        return log_on_statusbar('Rename cancelled.')
                else:
                    return log_on_statusbar(f'(!) OSError while renaming: {format_exc()}')

            # unexpected error :(
            except:
                return log_on_statusbar(f'(!) Failed to rename: {format_exc()}')

            # set output textbox to extension-less basename (same as in open())
            self.lineOutput.setText(basename_no_ext)
            self.lineOutput.setPlaceholderText(basename_no_ext + ext)
            self.lineOutput.setToolTip(new_name + constants.OUTPUT_TEXTBOX_TOOLTIP_SUFFIX)
            self.lineOutput.clearFocus()            # clear focus so we can navigate/use hotkeys again

            # create an `Undo` object with our old/new paths so we can undo this in the future
            if undoable:
                moved = os.path.basename(new_name) == os.path.basename(self.video)
                label = 'Move' if moved else 'Rename'
                self.undo_dict[new_name] = Undo(
                    type_=constants.UndoType.RENAME,
                    label=label,
                    description=f'Moved\n"{self.video}"\nto\n"{os.path.dirname(new_name)}"' if moved else f'Renamed\n"{self.video}"\nto\n"{new_name}"',
                    data={'new_path': new_name, 'old_path': self.video}
                )

            self.video = new_name
            refresh_title()                         # update titlebar
        except:
            log_on_statusbar(f'(!) Unexpected error while renaming: {format_exc()}')

        # replay the media, then restore position and pause state (no need for full-scale open())
        self.restore(get_ui_frame(), was_paused)

        # update recent files's list with new name, if possible
        # NOTE: this is done after playing in case the recent files list is very large
        try:
            recent_files = self.recent_files
            index = recent_files.index(old_name)
            recent_files[index] = self.video        # don't use `new_name` here in case we failed to rename
        except:
            pass


    def undo_rename(self, undo: Undo) -> bool | None:
        ''' Undo a rename/move by restoring `undo.data['new_path']` to
            its pre-rename path at `undo.data['old_path']`.Does not use
            super-renaming - any directories that were specifically created
            for the rename will not be deleted if they are left empty.

            If `restored_name` is now occupied by a new file, but that file is
            itself part of ANOTHER rename-undo, we will chain together these
            undos until we either hit a dead-end (file is not part of an undo)
            or we successfully find a chain that resolves all conflicts.
            Includes multiple layers of defense and recovery in case of
            disaster. Otherwise, we simply inform the user and give up.

            NOTE: Un-renaming uses `self.rename()` where necessary.
            NOTE: Returns True if the undo or undo-chain was successful. '''

        verb = undo.label.lower()
        current_name = undo.data['new_path']
        restored_name = undo.data['old_path']
        logging.info(f'Attempting to undo a rename from "{current_name}" back to "{restored_name}"')

        def restore(old_path: str, new_path: str):
            if old_path == self.video:
                self.rename(
                    new_path,
                    sanitize=False,
                    delete_source_dir=False,
                    warn_on_replace=False,
                    warn_on_drive=False,
                    undoable=False
                )
            else:   # TODO: is there ever a scenario where the user might want to delete a destination that was created?
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                os.rename(old_path, new_path)

        # make sure the file we're trying to undo still exists at its new, post-rename path
        if not exists(current_name):
            return log_on_statusbar(f'Cannot undo {verb}: File no longer exists.')

        # our old path is free for the taking. restore normally and skip the next 150 lines
        if not exists(restored_name):
            restore(current_name, restored_name)

        # oh, the path we're trying to restore to is being used by another file now?
        # no biggie, i'm sure this won't take hundreds of lines to safely handle            
        else:
            undo_chain: list[tuple[str, str, Undo]] = [(current_name, restored_name, undo)]
            please_dont_exist = restored_name

            # follow our undo dictionary until we run out of rename-undos that can be chained together
            # (e.g. we want to undo "test.mp3" back to "new.mp3" but it already exists - following...
            # ...the undo dictionary gets us the following chain of undos that would resolve our...
            # ...conflict: file5.mp3 -> file4.mp3; test.mp3 -> file5.mp3; new.mp3 -> test.mp3)
            while please_dont_exist in self.undo_dict and exists(please_dont_exist):
                chained_undo = self.undo_dict[please_dont_exist]
                if chained_undo.type == constants.UndoType.RENAME:
                    please_dont_exist = chained_undo.data['old_path']
                    undo_chain.append((chained_undo.data['new_path'], please_dont_exist, chained_undo))
                else:
                    break       # TODO: does this make sense? come back to this if new undo types are added

            # if our "restored_name" still exists, we either had no undos to fallback on or our undo...
            # ...chain was never resolved (undos eventually pointed to a file that isn't part of an undo)
            if exists(please_dont_exist):
                return show_on_statusbar(f'Cannot undo {verb}: A new file is occupying the old path.')

            # compile undo chain in a string so the user can understand what they're about to do before accepting
            msg = f'You are trying to restore a file back to a path that is now occupied by a new file, which itself can be restored to an older path. Would you like to undo all {verb}s?'
            chain_msg = '\n\n'.join(f'UNDO #{index}:\n"{name_from}" -> "{name_to}"' for index, (name_from, name_to) in enumerate(reversed(undo_chain), start=1))
            logging.info(f'The following undo chain has been identified:\n\n{chain_msg}')
            if qthelpers.getPopupOkCancel(
                title=f'Undo {len(undo_chain)} {verb}s?',
                text=msg,
                textDetailed=chain_msg,
                icon='warning',
                **self.get_popup_location_kwargs()
            ).exec() == QtW.QMessageBox.Ok:
                try:
                    logging.info('(Undo chain) Performing access-check before starting...')
                    access_denied: list[str] = []
                    for post_move, pre_move, _ in reversed(undo_chain):
                        try:
                            os.rename(post_move, post_move)
                        except PermissionError:
                            access_denied.append(post_move)
                        except:
                            return log_on_statusbar(f'(?) Unexpected error BEFORE starting undo chain. No files have been changed: {format_exc()}')

                    # if files are in use, do NOT try again. opens up too many horrible possibilites
                    # if the user wants to try again, the undo chain should resolve exactly the same way anyways
                    if access_denied:
                        qthelpers.getPopup(
                            title='This is going to ruin the tour',
                            text='Some files are currently in use.\nThe undo chain has been cancelled.',
                            textDetailed='\n'.join(access_denied),
                            icon='warning',
                            **self.get_popup_location_kwargs()
                        ).exec()
                        return show_on_statusbar(f'Cannot undo {verb}: Files in the undo chain are being used by other processes.')
                    logging.info('(Undo chain) Access-check successful. Starting undos...')

                    # begin undo chain (NOTE: chain goes from final file to first file, so loop in reverse)
                    start = get_time()
                    successful_undos: list[tuple[str, str, Undo]] = []
                    for index, (post_move, pre_move, chained_undo) in enumerate(reversed(undo_chain)):
                        logging.info(f'(Undo chain) Restoring "{post_move}" to "{pre_move}"')
                        while True:
                            try:
                                restore(post_move, pre_move)
                                successful_undos.append((post_move, pre_move, chained_undo))
                                break
                            except PermissionError:
                                logging.error(f'(!) Undo chain interrupted after {index} successful undo(s) by a PERMISSION ERROR??')
                                sleep(0.0001)       # sleep very briefly to encourage `get_time()` to update
                                prefix = f'Somehow, the following file started being used by another process\nin the last {get_time() - start:.5f} seconds.'

                                # index 0 means we didn't do any undos yet, so it's safe to cancel automatically
                                if index == 0:
                                    suffix = 'Thankfully, no undos have occured yet.\nThe undo chain has been cancelled.'
                                    qthelpers.getPopup(
                                        title='Undo chain interrupted?',
                                        text=f'{prefix} {suffix}',
                                        textDetailed=post_move,
                                        icon='warning',
                                        **self.get_popup_location_kwargs()
                                    ).exec()
                                    return show_on_statusbar(f'Cannot undo {verb}: Files in the undo chain are being used by other processes.')

                                suffix = (f'{index} undo(s) have already occured.\n\n'
                                        '> Retry: Try the next undo again and continue normally (close\n'
                                        'whatever is using the file first)\n\n'
                                        '> Abort: Attempt to undo the undos we just undid by restoring\n'
                                        f'the {index} undo(s) to their post-rename paths. This could make\n'
                                        'things worse.\n\n'
                                        '> Cancel: Leave the undo chain partially completed and do not\n'
                                        'risk any further confusion.')

                                russian_roulette = qthelpers.getPopupAbortRetryIgnore(
                                    title='Undo chain interrupted!!',
                                    text=f'{prefix} {suffix}',
                                    textDetailed=post_move,
                                    icon='critical',
                                    **self.get_popup_location_kwargs()
                                ).exec()

                                if russian_roulette == QtW.QMessageBox.Retry:
                                    logging.info('(Undo chain) Trying again...')
                                    continue        # ↓ remove the successful undos from our dictionary (NOTE: don't bother w/ empty folder warning)
                                elif russian_roulette == QtW.QMessageBox.Cancel:
                                    remove_dict_values(self.undo_dict, *(_undo[-1] for _undo in successful_undos))
                                    return log_on_statusbar(f'Failed to complete {len(undo_chain) - index}/{len(undo_chain)} undos.')
                                else:               # ↓ we still need to loop in reverse
                                    logging.info('(Undo chain) Trying to undo our undos...')
                                    for _post_move, _pre_move in reversed(successful_undos):
                                        logging.info(f'(Undo chain) UN-restoring "{_pre_move}" back to "{_post_move}"')
                                        while True:
                                            try:    # ↓ we're going BACK to our paths we just tried to undo
                                                restore(_pre_move, _post_move)
                                            except:
                                                explanation = f'"{_post_move}" was restored to "{_pre_move}" as part of an undo, but this could not be reversed.'
                                                if qthelpers.getPopupRetryCancel(
                                                    title='Abject disaster',
                                                    text='The following file could not have it\'s undo undone.\nYou can try again or give up. I\'m sorry.',
                                                    textDetailed=f'{explanation}\n\nError: {format_exc()}',
                                                    icon='critical',
                                                    **self.get_popup_location_kwargs()
                                                ).exec() == QtW.QMessageBox.Retry:
                                                    logging.info('(Undo chain) User is a FIGHTER. Mama didn\'t raise no quitter.')
                                                    continue
                                                logging.error('(!) User has thrown in the towel. Can\'t blame them.')
                                                return show_on_statusbar(f'Oops')
                                    return log_on_statusbar('Somehow, we\'ve averted all disaster and brought about peace on Earth.')

                    # check the folders of post-move paths and see if they're empty now, notifying the user
                    empty_folders = []
                    for (post_move, pre_move, _) in successful_undos:
                        if not os.listdir(empty_folder := os.path.dirname(post_move)):
                            logging.info(f'(Undo chain) An empty folder has been left behind at "{empty_folder}"')
                            empty_folders.append(empty_folder)

                    if len(empty_folders) == 1:
                        log_on_statusbar(f'{len(undo_chain)} {verb}s successfully undone, leaving behind an empty folder at "{empty_folders[0]}"')
                    elif len(empty_folders) > 1:
                        log_on_statusbar(f'{len(undo_chain)} {verb}s successfully undone, leaving behind {len(empty_folders)} empty folders.')
                    else:
                        log_on_statusbar(f'{len(undo_chain)} {verb}s successfully undone.')

                    # we... did it? the undo chain worked? remove all affected undos and return early
                    remove_dict_values(self.undo_dict, *(_undo[-1] for _undo in successful_undos))
                    return False                    # NOTE: return False here since we just removed the original undo

                except:
                    return log_on_statusbar(f'(!) Unexpected error while undoing {len(undo_chain)} {verb}s! View log to see which filenames may be mixed up. I\'m sorry: {format_exc()}')
            else:
                return show_on_statusbar(f'Cannot undo {verb}: A new file is occupying the old path.')

        # warn user if an empty folder has been left behind (see TODO in `restore()`)
        current_folder = os.path.dirname(current_name)
        if not os.listdir(current_folder):
            log_on_statusbar(f'Undo successful, but an empty folder has been left behind at "{current_folder}"')
        else:
            log_on_statusbar(f'Undo successful.')
        return True


    def delete(self, *files: str, cycle: bool = True):
        ''' Deletes (or recycles) an indeterminate number of `files`. If no
            `files` are provided, `self.video` is used. If `self.video` is
            within `files`, all players are stopped and the media is cycled
            (if `cycle` is True) before deleting. '''

        try:
            if not files:
                if not self.video:
                    return show_on_statusbar('No media is playing.', 10000)
                files = (self.video,)

            if self.video in files:
                if not cycle:
                    self.stop()
                else:                                   # cycle media before deleting if current video is about to be deleted
                    if self.is_gif:                     # image_player's QMovie must have its filename changed to unlock it
                        self.stop()
                    old_file = self.video               # self.video will likely change after media is cycled
                    new_file = self.cycle_media(next=self.last_cycle_was_forward, ignore=files)
                    if new_file is None or new_file == old_file:
                        self.stop()                     # media wasn't cycled -> stop player and uncheck deletion button
                        self.actionMarkDeleted.setChecked(False)
                        self.buttonMarkDeleted.setChecked(False)
                        log_on_statusbar('There are no remaining files to play in this folder.')

            count = len(files)
            fail_count = 0
            recycle = settings.checkRecycleBin.isChecked()
            verb = 'recycl' if recycle else 'delet'     # we're appending "ing" to these words
            verbing = f'{verb.capitalize()}ing'
            if recycle:
                import send2trash

            if count >= 10 and not self.edits_in_progress:
                logging.info(f'{verbing} {count} files...')
                self.set_save_progress_max_signal.emit(count)
                self.set_save_progress_format_signal.emit(f'{verbing} 0/{count} files...')
                self.set_save_progress_visible_signal.emit(True)
            else:
                log_on_statusbar(f'{verbing} {count} files...')
                app.processEvents()                     # process events so the statusbar updates immediately

            for index, file in enumerate(files, start=1):
                try:                                    # update statusbar every 5 files
                    send2trash.send2trash(file) if recycle else os.remove(file)
                    logging.info(f'File {file} {verb}ed successfully.')
                    if not self.edits_in_progress:
                        self.set_save_progress_value_and_format_signal.emit(index, f'{verbing} {index}/{count} files...')
                except Exception as error:
                    log_on_statusbar(f'File could not be deleted: {file} - {error}')

                # unmark file if it no longer exists, even if an error occurred
                if not exists(file):
                    if file in self.recent_files:
                        try: self.recent_files.remove(file)
                        except ValueError: pass
                    if file in self.marked_for_deletion:
                        self.marked_for_deletion.discard(file)
                else:                                   # track how many files still exist
                    fail_count += 1

            if fail_count == 0:
                log_on_statusbar(f'{count} files {verb}ed successfully.')
            else:
                log_on_statusbar(f'{count - fail_count}/{count} files {verb}ed successfully.')
        except:
            log_on_statusbar(f'(!) Unexpected error while deleting `files` ({files}), (cycle={cycle}): {format_exc()}')
        finally:                                        # ensure delete button's tooltip is still correct
            self.refresh_marked_for_deletion_tooltip()
            if not self.edits_in_progress:
                self.hide_edit_progress()


    def snapshot(self, *, mode: str = 'quick', is_temp: bool = False):      # * to capture unused signal args
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

        # aliases/variables
        frame = get_ui_frame()                          # immediately get frame, regardless of whether we need it or not
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
                except:
                    return log_on_statusbar(f'(!) Failed to delete last snapshot at "{cfg.last_snapshot_path}": {format_exc()}')

            # no media opened yet or this is audio with no cover art loaded
            elif not video:
                return show_on_statusbar('No media is playing.', 10000)
            elif self.is_audio_without_cover_art:
                if not can_load_cover_art():
                    return show_on_statusbar('You have cover art detection disabled.', 10000)
                return show_on_statusbar('You can only snapshot audio with cover art.', 10000)

        # >>> take new snapshot <<<
            is_gif = self.is_gif
            is_art = self.is_audio_with_cover_art
            frame_count_str = str(self.frame_count_raw)
            if mime == 'image' and settings.checkSnapshotGifPNG.isChecked(): format = 'PNG'
            else: format = settings.comboSnapshotFormat.currentText()

            if is_art:
                frame = 1
                frame_count_str = '1'                           # NOTE: art/gif snapshots use the default name format's placeholder text
                name_format          = settings.lineSnapshotArtFormat.text().strip() or settings.lineSnapshotNameFormat.placeholderText()
            elif is_gif: name_format = settings.lineSnapshotGifFormat.text().strip() or settings.lineSnapshotNameFormat.placeholderText()
            else:        name_format = settings.lineSnapshotNameFormat.text().strip() or settings.lineSnapshotNameFormat.placeholderText()

            video_basename_no_ext = splitext_media(os.path.basename(video), strict=False)[0]
            date_format = settings.lineSnapshotDateFormat.text().strip() or settings.lineSnapshotDateFormat.placeholderText()
            default_name = name_format.replace('?name', video_basename_no_ext) \
                                      .replace('?date', strftime(date_format, localtime())) \
                                      .replace('?framecount', frame_count_str) \
                                      .replace('?frame', str(frame).zfill(len(frame_count_str)))

            # get width, height, and jpeg quality of snapshot
            if mode == 'full':
                width, height, quality, _, _ = self.show_size_dialog(show_quality=True)
                if width is None:                               # dialog cancelled (finally-statement ensures we unpause if needed)
                    return
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
                os.makedirs(dirname, exist_ok=True)
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
                path, format, lastdir = qthelpers.saveFile(
                    lastdir=get_unique_path(path, key='?count', zeros=1, strict=True),
                    caption='Save snapshot as',
                    filter='PNG (*.png);;JPEG (*.jpg; *.jpeg; *.jpe; *.jfif; *.exif);;All files (*)',
                    selectedFilter=selected_filter,
                    returnFilter=True
                )
                if use_snapshot_lastdir: cfg.last_snapshot_folder = lastdir
                else: cfg.lastdir = lastdir
                if path is None:
                    return
                path = abspath(path)
                # 'BMP (*.bmp; *.dib, *.rle);;TIFF (*.tiff; *.tif);;GIF (*.gif);;TGA (*.tga);;WebP (*.webp)'

            logging.info(f'psz_filepath={path}, i_width={width}, i_height={height}, quality={quality}')

            # take and save snapshot
            if is_gif:
                if width or height:                             # use "scale" ffmpeg filter for gifs
                    w = width or -1                             # -1 uses aspect ratio in ffmpeg (as opposed to 0 in VLC)
                    h = height or -1
                    ffmpeg(f'-i "{self.video}" -vf "select=\'eq(n\\,{frame})\', scale={w}:{h}" -vsync 0 "{path}"')
                else:
                    ffmpeg(f'-i "{self.video}" -vf select=\'eq(n\\,{frame})\' -vsync 0 "{path}"')
            elif is_art:
                if can_show_cover_art():                        # this probably can have a race condition, but who cares
                    art = image_player.art
                else:                                           # if cover art is loaded but hidden,...
                    art = QtGui.QPixmap()                       # ...load it into a separate pixmap
                    art.loadFromData(self.cover_art_buffer)     # (we could use `PIL` but this is simpler)

                if width or height:
                    w = width or height * (self.vwidth / self.vheight)
                    h = height or width * (self.vheight / self.vwidth)
                    art.scaled(w, h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation).save(path, quality=quality)
                else:
                    art.save(path, quality=quality)
            else:
                player.snapshot(path, frame, width, height)

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
                            if not height:                      # width is set but height isn't -> match factors
                                y_factor = x_factor
                        if height:
                            y_factor = self.vheight / height
                            if not width:                       # height is set but width isn't -> match factors
                                x_factor = y_factor
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
            elif use_jpeg:
                self.convert_snapshot_to_jpeg(path, quality=quality)

            # return snapshot path
            return path

        except:
            log_on_statusbar(f'(!) SNAPSHOT FAILED: {format_exc()}')
        finally:                                                # restore pause-state before leaving
            if self.is_gif: image_player.gif.setPaused(self.is_paused)
            else: player.set_pause(self.is_paused)              # NOTE: DON'T do both - QMovie will emit a "frameChanged" signal!!!


    def save_as(
        self,
        *,                                                      # * to capture unused signal args
        noun: str = 'media',
        filter: str = 'MP4 files (*.mp4);;MP3 files (*.mp3);;WAV files (*.wav);;AAC files (*.aac);;All files (*)',
        valid_extensions: tuple[str] = constants.ALL_MEDIA_EXTENSIONS,
        ext_hint: str = None,
        default_path: str = None,
        unique_default: bool = True
    ) -> bool | None:
        ''' Opens a file dialog with `filter` and the caption "Save `noun`
            as...", before saving to the user-selected path, if any. Returns
            None if the dialog is cancelled. See `save()` for more details. '''

        video = self.video
        if not video: return show_on_statusbar('No media is playing.', 10000)
        if not self.is_safe_to_edit(video): return show_on_statusbar('Save cancelled (source media is set to be overwritten).', 10000)
        if not default_path:
            default_path, _, _ = self.get_output(
                valid_extensions=valid_extensions,
                ext_hint=ext_hint
            )

        try:
            logging.info('Opening \'Save As...\' dialog.')
            file = self.browse_for_save_file(
                noun=noun,
                filter=filter,
                valid_extensions=valid_extensions,
                ext_hint=ext_hint,
                default_path=default_path or video,
                unique_default=unique_default
            )

            if file:                                            # None if cancel was selected
                logging.info(f'Saving as \'{file}\'')
                return self.save(dest=file)
        except:
            log_on_statusbar(f'(!) SAVE_AS FAILED: {format_exc()}')


    def save(
        self,
        *,                                                      # * to capture unused signal args
        dest: str = None,
        noun: str = 'media',
        filter: str = 'MP4 files (*.mp4);;MP3 files (*.mp3);;WAV files (*.wav);;AAC files (*.aac);;All files (*)',
        valid_extensions: tuple[str] = constants.ALL_MEDIA_EXTENSIONS,
        preferred_extensions: tuple[str] = None,
        ext_hint: str = None,
        unique_default: bool = False
    ) -> bool | None:
        ''' Checks for any edit operations, applies them to the current media,
            and saves the new file to `dest`. If `dest` is None, `save_as()`
            is called, passing in `filter`, and a list of `valid_extensions`.
            If `preferred_extensions` is specified, `save_as()` will default
            to an extension from this list if possible, even if the current
            extension is already valid. If `dest` has no extension, `ext_hint`
            will be used. If `ext_hint` is None, PyPlayer will guess the
            extension. `unique_default` is passed to `save_as()` if necessary.

            NOTE: Saving occurs in a separate thread. '''

        video = self.video
        if not video: return show_on_statusbar('No media is playing.', 10000)
        if not self.is_safe_to_edit(video): return show_on_statusbar('Save cancelled (source media is set to be overwritten).', 10000)

        operations = self.operations.copy()
        if self.actionCrop.isChecked():      operations['crop'] = True
        if self.buttonTrimStart.isChecked(): operations['trim start'] = True
        if self.buttonTrimEnd.isChecked():   operations['trim end'] = True

        ext = ''
        old_base, old_ext = splitext_media(video)
        if not old_ext:
            old_ext = '.' + self.extension

        # see if we haven't sufficiently edited the destination (no abspath specified, same basename (excluding the extension))
        if not dest:
            dest_was_not_modified = True                        # TODO i don't think this code actually matters anymore
        else:
            old_tail_base = os.path.split(old_base)[-1]
            new_base, new_ext = splitext_media(dest)
            dest_was_not_modified = old_tail_base == new_base

        # get output name
        if dest_was_not_modified:

            # NOTE: `unique_default` behavior examples:
            # Example 1: video='test.mp4', output='test', ext_hint='.mp3'
            #     -> open prompt with 'test.mp3' as the default if it doesn't exist, 'test (2).mp3' otherwise
            # Example 2: video='test.mp4', output='new', ext_hint='.mp3'
            #     -> immediately saves as 'new.mp3' if it doesn't exist, opens a prompt with 'new (2).mp3' otherwise
            output_text, _, ext = self.get_output(              # TODO: ^ this is extremely stupid
                valid_extensions=valid_extensions,
                ext_hint=ext_hint,
            )

            # no name OR name already exists -> use preset name or "Save as..." prompt
            # NOTE: `exists(output_text)` only applies to OTHER files, not `self.video`
            unchanged = not output_text
            if unchanged or exists(output_text):
                if ext_hint and unchanged:                      # invalid/unchanged output -> use `ext_hint` if possible but still show prompt
                    output_text = old_base + ext_hint

                if settings.checkSaveAsForceOnNoName.isChecked():
                    return self.save_as(
                        noun=noun,
                        filter=filter,
                        valid_extensions=preferred_extensions or valid_extensions,
                        ext_hint=ext_hint or old_ext,           # ^ pass preferred extensions if provided
                        default_path=output_text,
                        unique_default=unique_default
                    )
                elif operations:
                    dest = add_path_suffix(video, '_edited', unique=True)
            else:
                dest = output_text
                if not os.path.dirname(dest):                   # output text is just a name w/ no directory
                    default_dir = settings.lineDefaultOutputPath.text().strip() or os.path.dirname(video)
                    dest = abspath(os.path.expandvars(os.path.join(default_dir, dest)))     # ^ if no default dir, use source media's dir
                if not splitext_media(dest, valid_extensions)[-1]:                          # append extension if needed
                    ext = ext_hint or old_ext
                    dest += ext                                 # use extension hint if specified, otherwise just use source file's extension
            dirname, basename = os.path.split(dest)             # sanitize our custom destination (`sanitize` does not account for full paths)
            dest = os.path.join(dirname, sanitize(basename))

        # ensure output has valid extension included
        if not ext:
            if not splitext_media(dest, valid_extensions)[-1]:
                dest += ext_hint or old_ext
        logging.info(f'Destination extension is "{ext}"')
        dest = abspath(dest)                                    # clean up destination one more time, just in case

        # check for common reasons we might not be allowed to use `dest`
        if not self.is_safe_to_edit(dest=dest):                 # NOTE: we already checked `self.video` above
            return self.save_as(noun=noun, filter=filter, default_path=dest, unique_default=True)

        # no operations -> check if video was renamed and return without starting a new thread
        if not operations:
            if dest != video:                                   # no operations, but name is changed
                logging.info(f'No operations detected, but a new name was specified. Renaming to {dest}')
                return self.rename(dest)                        # do a normal rename and return
            return marquee('No changes have been made.', log=False)

        # do actual saving in separate thread
        Thread(target=self._save, args=(dest, operations), daemon=True).start()
        return True


    def _save(self, dest: str = None, operations: dict = {}):
        ''' Do not call this directly. Use `save()` instead. Iteration: VII '''
        start_time = get_time()
        successful = True
        log_noun = ''

        # save copies of critical properties that could potentially change while we're saving
        video = self.video.strip()
        mime = self.mime_type
        extension = self.extension
        is_gif = self.is_gif
        is_static_image = self.is_static_image
        frame_count, frame_count_raw = self.frame_count, self.frame_count_raw
        frame_rate, duration = self.frame_rate, self.duration
        vwidth, vheight = self.vwidth, self.vheight
        minimum, maximum = self.minimum, self.maximum
        audio_track_count = player.get_audio_track_count()
        audio_track_titles: list[str] = [id_and_title[-1] for id_and_title in list(player.get_audio_tracks())[1:]]

        # what will we do to our output and original files after saving? (NOTE: concatenation will override these)
        open_after_save = None                                  # None means we'll decide after the edit finishes
        explore_after_save = False
        delete_mode = self.checkDeleteOriginal.checkState()     # 0, 1, or 2 (ultimately ignored if we're replacing `dest`)

        # operation aliases
        op_concat: dict[str] =               operations.get('concatenate', None)    # see `self.concatenate()` for details
        op_add_text =                        operations.get('add text', None)       # a list of `widgets.QTextOverlay` objects
        op_replace_audio: str =              operations.get('replace audio', None)  # path to audio track
        op_add_audio: str =                  operations.get('add audio', None)      # path to audio track
        op_isolate_track: tuple[str, int] =  operations.get('isolate track', None)  # track-type and index to isolate
        op_amplify_audio: float =            operations.get('amplify audio', None)  # new volume, from 0-1(+)
        op_resize: tuple[int, int] | float = operations.get('resize', None)         # (width, height) OR duration multiplier
        op_rotate_video: str =               operations.get('rotate video', None)   # rotation command (e.g. "vflip")
        op_trim_start: bool =                operations.get('trim start', False)    # represents both trimming and fading
        op_trim_end: bool =                  operations.get('trim end', False)      # represents both trimming and fading
        op_crop: bool =                      operations.get('crop', False)

        # save remnants dict (contains stuff like dialogs we want to hang onto for later if the save fails)
        if 'remnants' in operations:
            operations['remnants'].setdefault('video', video)
            operations['remnants'].setdefault('_in_progress', True)
            self.save_remnants[start_time] = operations['remnants']
            del operations['remnants']                          # delete the operation key, not the remnant itself

        # quick pre-operation checks (we do this here instead of being the...
        # ...thread because it's kinda slow + we reuse some of these variables)
        if op_crop:
            if mime == 'audio':                                 # don't disable crop, but ignore it as an operation for audio
                log_on_statusbar('Crop mode on audio files is designed for cropping cover art through snapshots/image copying.')
                del operations['crop']                          # remove operation key
                op_crop = False
            lfp = tuple(self.vlc.last_factored_points)
            crop_selection = tuple(self.vlc.factor_point(point) for point in self.vlc.selection)
            crop_top =    min(crop_selection[0].y(), vheight - 1)
            crop_left =   min(crop_selection[0].x(), vwidth - 1)
            crop_right =  min(crop_selection[1].x(), vwidth)
            crop_bottom = min(crop_selection[2].y(), vheight)
            crop_width =  round(crop_right - crop_left)
            crop_height = round(crop_bottom - crop_top)
            if crop_width == vwidth and crop_height == vheight:  # not actually cropped -> disable crop mode and update our operations
                log_on_statusbar('Crop is the same size as the source media.')
                self.disable_crop_mode_signal.emit(False)        # False to make sure we don't log crop mode being disabled
                del operations['crop']                           # remove operation key
                op_crop = False
        if op_trim_start or op_trim_end:
            if is_static_image:                                 # NOTE: shouldn't be possible, but just in case
                log_on_statusbar('I don\'t know how you got this far, but you can\'t trim/fade a static image.')
                operations.pop('trim start', None)              # remove operation keys if they exist
                operations.pop('trim end', None)
                op_trim_start = False
                op_trim_end = False
            elif minimum == 0 and maximum == frame_count:
                log_on_statusbar('It\'s not really a "trim" if you end up with the entire duration of the file, is it?')
                operations.pop('trim start', None)              # remove operation keys if they exist
                operations.pop('trim end', None)
                op_trim_start = False
                op_trim_end = False
            elif minimum == maximum:
                log_on_statusbar('If you want to trim off 100% of the file, you might as well just delete it.')
                operations.pop('trim start', None)              # remove operation keys if they exist
                operations.pop('trim end', None)
                op_trim_start = False
                op_trim_end = False

        # check if we still have work to do after the above checks
        if not operations:
            return logging.info('(?) All pre-operation checks failed, nothing left to do.')

        # min/max are usually offset in ffmpeg for some reason, so adjust if necessary
        # NOTE: audio-only will never be truly correct. might require audio re-encoding
        if mime == 'audio':
            maximum = min(frame_count, maximum + 3)
        else:
            minimum = max(0, minimum - 2)
            maximum = maximum if maximum == frame_count else (maximum - 1)

        # ffmpeg is required after this point, so check that it's actually present, and because...
        # ...we're in a thread, we skip the warning and display it separately through a signal
        if not constants.verify_ffmpeg(self, warning=False, force_warning=False):
            self.show_ffmpeg_warning_signal.emit(self)
            return marquee('You don\'t have FFmpeg installed!')

        # get the new ctime/mtime to set out output file to (0 means don't change)
        if not op_concat:                                       # NOTE: concatenation provides its own files
            new_ctime, new_mtime = self.get_new_file_timestamps(video, dest=dest)

        # NEVER directly save to our destination - always to a unique temp path. makes cleanup 100x easier
        intermediate_file = video                               # the path to the file that will be receiving all changes between operations
        final_dest = dest                                       # save the original dest so we can rename our temporary dest back later
        dest = add_path_suffix(dest, '_temp', unique=True)      # add _temp to dest, in case dest is the same as our base video

        logging.info(f'Saving file to "{final_dest}"')
        logging.debug(f'temp-dest={dest}, video={video}, delete={delete_mode}, operations={operations}')
        temp_paths = []                                         # some edits generate excess files we'll need to delete later

        # lock both temporary and actual destination in the player
        self.locked_files.add(dest)
        self.locked_files.add(final_dest)

        # open handle to our destination to lock it on the system
        DEST_ALREADY_EXISTED = exists(final_dest)
        dest_handle = open(final_dest, 'a')

    # --- Apply operations to media ---
        # TODO: GIFs should probably use Pillow for their operations
        # NOTE: ABSOLUTELY EXTREMELY IMPORTANT!!! update any relevant properties such as...
        # ...vheight/vwidth, is_gif/is_static_image, etc. as SOON as an operation is done!!!
        try:
            edit = Edit(final_dest)
            edit.frame_rate = frame_rate
            edit.frame_count = frame_count_raw
            edit.operation_count = len(operations)
            edit.audio_track_titles = audio_track_titles        # NOTE: ignored on edits that manually specify `-map`
            if op_trim_start and op_trim_end:                   # account for trimming taking up two keys
                edit.operation_count -= 1
            self.add_edit(edit)

            # static images are cached and can be deleted independent of pyplayer. if this happens, save the cached...
            # ...QPixmap to a temp file and delete it later (we'll assume the user wants the original to stay gone)
            # NOTE: we do this even if we're not sure the image will actually be used (like if we're concatenating)
            if is_static_image and video and not exists(video):
                temp_image_path = add_path_suffix(video, '_tempimage', unique=True)
                temp_paths.append(temp_image_path)
                intermediate_file = temp_image_path
                with get_PIL_Image().fromqpixmap(image_player.art) as image:
                    image.save(temp_image_path)

            # the code block formerly known as `self._concatenate()`
            if op_concat:
                log_noun = 'Concatenation'
                files = op_concat['files']
                open_after_save = op_concat['open']
                explore_after_save = op_concat['explore']
                delete_mode = op_concat['delete_mode']

                new_ctime, new_mtime = self.get_new_file_timestamps(*files, dest=dest)
                edit.frame_rate = op_concat['frame_rate_hint']
                edit.frame_count = op_concat['frame_count_hint']
                if op_concat['encode']:
                    if not FFPROBE:                             # couldn't probe files -> use special text and indeterminate progress
                        edit.percent_format = '(re-encode requested, this will take a while)'
                        self.set_save_progress_max_signal.emit(0)

                    inputs = '-i "' + '" -i "'.join(files)      # ↓ "[0:v:0][0:a:0][1:v:0][1:a:0]", etc.
                    funnysquares = ''.join(f'[{i}:v:0][{i}:a:0]' for i in range(len(files)))
                    filtercmd = f'-filter_complex "{funnysquares}concat=n={len(files)}:v=1:a=1[outv][outa]"'
                    cmd = f'{inputs}" {filtercmd} -map "[outv]" -map "[outa]" -vsync 2 %out'
                    edit.ffmpeg(None, cmd, dest, 'Concatenating', 'Preparing files for concatenation...')

                # no re-encoding, concatenate (almost instantly) using stream copying
                else:
                    # immediately and directly set text while we do intermediate step
                    edit.start_text = edit.text = 'Preparing files for concatenation...'
                    edit.give_priority(conditional=True)        # update priority so the UI's text refreshes

                    # convert files to MPEG-TS for easier concatenation
                    intermediate_files = []
                    for file in files:
                        temp_filename = file.replace(':', '').replace('/', '').replace('\\', '') + '.ts'
                        intermediate_file = f'{constants.TEMP_DIR}{sep}{temp_filename}'
                        try: os.remove(intermediate_file)
                        except: pass
                        intermediate_files.append(intermediate_file)
                        ffmpeg(f'-i "{file}" -c copy -bsf:v h264_mp4toannexb -f mpegts "{intermediate_file}"')

                    # concatentate with ffmpeg
                    if self.mime_type == 'audio': cmd = f'-i "concat:{"|".join(intermediate_files)}" -c copy %out'
                    else: cmd = f'-i "concat:{"|".join(intermediate_files)}" -c copy -video_track_timescale 100 -bsf:a aac_adtstoasc -movflags faststart -f mp4 %out'
                    edit.ffmpeg(None, cmd, dest, 'Concatenating', 'Preparing files for concatenation...')
                    for intermediate_file in intermediate_files:
                        try: os.remove(intermediate_file)
                        except: pass

            # we're overlaying text over the video/gif
            # HACK: For ~5 days, I tried to figure out how to consistently and accurately translate the preview generated with QPainter/QFontMetrics...
            # ...to what FFmpeg's drawtext filter expects. Modern (like so modern I don't think they're in public versions yet) releases of FFmpeg...
            # ...now have `y_align` and `text_align` parameters which fix most of my issues, but I didn't want to make an unstable beta branch...
            # ...a requirement. I assumed that doing this correctly was literally impossible with the arbitrarily limited infomation QFontMetrics...
            # ...exposes to you, so I gave up on that after an hour and decided on a pretty wild hack: Re-painting the preview onto a QPixmap...
            # ...before saving, then looping over the pixels to find the true coordinates of the text so that FFmpeg can place them correctly,...
            # ...on top of having to do a bunch of silly math with terrible numbers to get text alignment figured out. 5 days of trial-and-error...
            # ...later, I got everything mostly working at about 90% accuracy, before realizing that I could just use FFmpeg's image overlaying...
            # ...filter to overlay the QPixmap I'm already generating. All I have to do is apply some of these hacks to the preview image instead...
            # ...of the output, and it'll be 100% accurate no matter what AND we'll be able to do so much more, like overlaying actual images...
            # ...or doing outlines/blurs and stuff. Kinda sad with how close I was to getting this (almost) perfect, but it's 100% for the best.
            #
            # Anyways that's why this code is unfinished garbage, and also why I'm committing it regardless. Thanks for coming to my TED talk.
            #
            # -vf "drawtext=fontfile=/path/to/font.ttf:text='Text testing, here!':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=(h-text_h)/2"
            if op_add_text:                                     # 'ignore', 'start', 'end', 'both'
                # we are using the start marker for our text (NOTE: NOT IMPLEMENTED)
                #if op_add_text['markers'] in ('start', 'both'):
                #    if op_trim_start:
                #        del operations['trim start']
                #        op_trim_start = False
                #
                ## we are using the end marker for our text (NOTE: NOT IMPLEMENTED)
                #if op_add_text['markers'] in ('end', 'both'):
                #    if op_trim_end:
                #        del operations['trim start']
                #        op_trim_start = False
                filters = []
                pixmap = QtGui.QPixmap(self.vwidth, self.vheight)
                painter = QtGui.QPainter(pixmap)
                try:
                    for overlay in op_add_text['overlays']:
                        if not overlay.text.strip():
                            continue

                        top_line_adjusted_center = 0
                        text = overlay.text.strip('\n')
                        lines = text.split('\n')

                    # >>> see HACK above
                        # use manual labor to figure out font filepath that Qt refuses to expose
                        font = get_font_path(overlay.font.family())
                        if font:
                            font = font.replace('\\', '/')
                            font_param = f'fontfile=\'{font}\''
                        else:                                   # hope the user has a special build of ffmpeg that supports the "font" parameter
                            show_on_statusbar(f'(!) No font file found for "{overlay.font.family()}"')
                            font_param = f'font=\'{overlay.font.family()}\''

                        overlay.font.setPixelSize(overlay.size)
                        pixmap.fill(Qt.transparent)
                        painter.setFont(overlay.font)
                        painter.setPen(overlay.color)

                        font_metrics = painter.fontMetrics()
                        line_height = font_metrics.ascent() * 1.1
                        text_size = font_metrics.size(0, text)
                        text_rect = QtCore.QRect(overlay.pos.toPoint(), text_size)
                        #if overlay.centered_vertically:
                        #    text_rect.moveCenter(QtCore.QPoint(text_rect.x(), vheight / 2))

                        painter.drawText(text_rect, overlay.alignment | Qt.AlignTop, text)
                        image = get_PIL_Image().fromqpixmap(pixmap)
                        pixels = image.load()
                        local_pos = overlay.pos.toPoint()

                        # loop over pixels until visible one is found (start from Qt's coordinates to massively improve performance)
                        top_y = vheight * 2                     # use starting numbers outside the dimensions of the media
                        min_x = vwidth * 2
                        if len(lines) > 1 or not overlay.centered_vertically:
                            for y in range(local_pos.y(), min(image.height, local_pos.y() + text_size.height())):
                                for x in range(local_pos.x(), min(image.width, local_pos.x() + text_size.width())):
                                    if pixels[x, y][-1] != 0:
                                        logging.info(f'Overlay\'s first non-transparent pixel found at ({x}, {y}) -> {pixels[x, y]}')
                                        min_x = min(min_x, x)
                                        top_y = min(top_y, y)
                                        break
                                #else:                           # `else` means we didn't break the inner-loop (no pixels on this row)
                                #    continue
                                #break                           # break outer-loop if we broke the inner-loop
                            #else:                               # `else` means we didn't break the outer-loop either (no pixels at all)
                            if top_y > vheight:
                                logging.info(f'Overlay isn\'t actually visible on the screen (text: {text})')
                                continue                        # jump to the next overlay

                        text_rect.setLeft(min_x)
                        text_rect.setTop(top_y)
                        text_rect.setWidth(max(font_metrics.tightBoundingRect(line).width() for line in lines))
                        #text_rect.setWidth(font_metrics.size(0, text).width())
                        #text_bounding_rect = font_metrics.tightBoundingRect(text)
                        #text_rect.setWidth(text_bounding_rect.width())
                        #text_rect.setHeight(text_bounding_rect.height())
                        print('min_x, top_y, and text_rect', min_x, top_y, text_rect)
                    # >>> main part of HACK finished

                        for line_number, line in enumerate(lines):
                            if not line.strip():
                                continue

                            line_size = font_metrics.size(0, line)
                            #line_rect = QtCore.QRect(text_rect.topLeft(), line_size)
                            line_width = font_metrics.horizontalAdvance(line)

                            bounding_rect = font_metrics.tightBoundingRect(line)
                            print('ascent', line_height, 'size', line_size, 'width', line_width, 'tightBoundingRect', bounding_rect)

                            #bounding_rect.width

                            #line_rect = QtCore.QRect(text_rect.topLeft(), QtCore.QSize(line_size.width(), line_height))
                            #line_rect = QtCore.QRect(text_rect.topLeft(), QtCore.QSize(bounding_rect.width(), line_height))
                            line_rect = QtCore.QRect(text_rect.topLeft(), QtCore.QSize(bounding_rect.width(), bounding_rect.height()))

                            if line_number == 0:
                                #top_line_rect = line_rect
                                if overlay.centered_vertically:
                                    top_line_adjusted_center = (vheight / 2) - (line_height * len(lines) / 2) + (line_height / 4)
                                else:
                                    #top_line_adjusted_center = top_y + (bounding_rect.height() / 2)
                                    top_line_adjusted_center = top_y
                                #elif len(lines) == 1:
                                #    top_line_adjusted_center = top_y + (bounding_rect.height() / 2)
                                #else:
                                #    top_line_adjusted_center = line_rect.bottom() - (line_height / 2)
                            #    if overlay.centered_vertically:
                            #        if len(lines) == 1: y = '(h-text_h)/2'
                            #        else:               y = y - ((line_height * len(lines)) / 4)
                            #    else:                   y = y + 1
                            #else:
                            #    line_rect.moveCenter(QtCore.QPoint(
                            #        text_rect.center().x(),
                            #        top_line_rect.center().y() + (line_height * line_number)
                            #    ))
                            #    y = line_rect.y()

                            #if overlay.centered_vertically and len(lines) == 1:
                            if overlay.centered_vertically:
                                if len(lines) == 1:
                                    y = '(h-text_h)/2'
                                else:
                                    line_rect.moveCenter(QtCore.QPoint(
                                        text_rect.center().x(),
                                        #top_line_rect.center().y() + (line_height * line_number)
                                        int(top_line_adjusted_center + (line_height * line_number))
                                    ))
                                    y = line_rect.bottom() - bounding_rect.height()
                            else:
                                #line_rect.moveCenter(QtCore.QPoint(
                                #    text_rect.center().x(),
                                #    #top_line_rect.center().y() + (line_height * line_number)
                                #    int(top_line_adjusted_center + (line_height * line_number))
                                #))
                                #line_rect.moveTop(int(top_line_adjusted_center + (line_height * line_number)))
                                #y = line_rect.y()
                                #y = line_rect.bottom() - (line_height / 2)
                                #y = line_rect.bottom() - line_height
                                #y = line_rect.bottom() - line_size.height()
                                #y = line_rect.bottom() - bounding_rect.height()
                                #y = int(top_line_adjusted_center + (line_height * line_number))
                                y = int(top_line_adjusted_center + (line_height * line_number))

                            # attempt to manually align each line of text (FFmpeg only supports left-align)
                            if overlay.centered_horizontally:   # use FFmpeg's built-in variables to escape the garbage below if possible
                                x = '(w-text_w)/2'
                            else:
                                if overlay.alignment == Qt.AlignLeft:
                                    #x = overlay.pos.x()
                                    x = text_rect.left()
                                    print('ALIGNLEFT', x)
                                elif overlay.alignment == Qt.AlignHCenter:
                                    #x = text_rect.center().x() - (line_size.width() / 2)
                                    x = text_rect.center().x() - (bounding_rect.width() / 2)
                                    print('ALIGNHCENTER', text_rect, text_rect.center().x(), bounding_rect.width() / 2, x)
                                elif overlay.alignment == Qt.AlignRight:            # TODO: My right-align code just doesn't work and I don't understand why.
                                    #x = top_line_rect.right() - line_size.width()  # Thankfuly, now I don't HAVE to understand why. See you never, drawtext.
                                    #x = text_rect.right() - line_size.width()
                                    x = text_rect.right() - bounding_rect.width() - bounding_rect.left()
                                    print('ALIGNRIGHT', x)

                            # escape stuff drawtext doesn't like -> https://stackoverflow.com/a/71635094
                            line = (line.replace("\\", "\\\\")
                                        .replace('"', '""')
                                        .replace("'", "''")
                                        .replace("%", "\\%")
                                        .replace(":", "\\:"))

                            filter_params = [
                                f'text=\'{line}\'',
                                f'x={x}',
                                f'y={y}',
                                f'fontsize={overlay.size}',
                                f'fontcolor={overlay.color.name()}@{overlay.color.alpha() / 255}',
                                font_param
                                #'y_align=font'                 # see HACK comment above for why we can't use this
                            ]

                            # add background box
                            if overlay.bgcolor.alpha():
                                filter_params.append('box=1')
                                filter_params.append(f'boxcolor={overlay.bgcolor.name()}@{overlay.bgcolor.alpha() / 255}')
                                filter_params.append(f'boxborderw={overlay.bgwidth}')

                            # add drop-shadow
                            if overlay.shadowx or overlay.shadowy:
                                filter_params.append(f'shadowcolor={overlay.shadowcolor.name()}@{overlay.shadowcolor.alpha() / 255}')
                                filter_params.append(f'shadowx={overlay.shadowx}')
                                filter_params.append(f'shadowy={overlay.shadowy}')

                            # see HACK comment above for why we can't use this
                            #alignments = {
                            #    int(Qt.AlignLeft): 'L',
                            #    int(Qt.AlignHCenter): 'C',
                            #    int(Qt.AlignRight): 'R',
                            #}
                            #filter_params.append(f'text_align={alignments[overlay.alignment]}+M')

                            filters.append(f'drawtext={":".join(filter_params)}')
                finally:                                        # NOTE: IMPORTANT!!! we MUST close the painter manually...
                    painter.end()                               # ...or we'll crash to desktop when the thread closes!!!

                cmd = f'-i %in -vf "{",".join(filters)}" -codec:a copy %out'
                intermediate_file = edit.ffmpeg(intermediate_file, cmd, dest, 'Overlaying text')

            # trimming and fading (controlled using the same start/end points)
            # TODO: there are scenarios where cropping and/or resizing first is better
            #       - how should we handle reordering operations?
            if op_trim_start or op_trim_end:

                # trim -> https://trac.ffmpeg.org/wiki/Seeking TODO: -vf trim filter should be used in here
                if self.is_trim_mode():
                    trim_duration = (maximum - minimum) / frame_rate

                    # animated GIFs don't need a lot of the extra bits
                    if is_gif:
                        cmd = '-i %in '
                        if minimum > 0:           cmd += f'-ss {minimum / frame_rate} '
                        if maximum < frame_count: cmd += f'-to {maximum / frame_rate} '

                    else:
                        if mime == 'audio':                     # audio re-encoding should probably be an option in the future
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
                                    self.trim_mode_selection_cancelled = False
                                    cfg.trimmodeselected = False
                                    self.show_trim_dialog_signal.emit()
                                    while not cfg.trimmodeselected:
                                        sleep(0.1)
                                    if self.trim_mode_selection_cancelled:
                                        successful = False      # user hit X on the trim dialog
                                        return log_on_statusbar('Trim cancelled.')

                                start_time = get_time()         # reset start_time to undo time spent waiting for dialog
                                requires_precision = extension in constants.SPECIAL_TRIM_EXTENSIONS and mime != 'audio'
                                precise = requires_precision or self.trim_mode_action_group.checkedAction() is self.actionTrimPrecise
                                if not precise: log_on_statusbar('Imprecise trim requested.')
                                else:           log_on_statusbar('Precise trim requested (this is a time-consuming task).')

                        # construct FFmpeg command based on starting/ending frame, precision mode, and mime type
                        cmd = ''
                        if minimum:
                            trim_start = minimum / frame_rate
                            cmd = f'-ss {trim_start} -i %in '
                        if maximum < frame_count:
                            if not precise:
                                maximum -= 1
                            if minimum: cmd += f' -to {(trim_duration)} '
                            else:       cmd += f' -i %in -to {(maximum / frame_rate)} '
                        if mime != 'audio':
                            if precise: cmd += ' -c:v libx264 -c:a aac'
                            else:       cmd += ' -c:v copy -c:a copy -avoid_negative_ts make_zero'
                        else:           cmd += ' -codec copy -avoid_negative_ts make_zero'

                    duration = trim_duration                                        # update duration
                    edit.frame_count = frame_count = maximum - minimum              # update frame count
                    intermediate_file = edit.ffmpeg(intermediate_file, cmd, dest, 'Trimming', 'Seeking to start of trim...')

                # fade (using trim buttons as fade points) -> https://dev.to/dak425/add-fade-in-and-fade-out-effects-with-ffmpeg-2bj7
                # TODO: ffmpeg fading is actually very versatile, this could be WAY more sophisticated
                else:
                    log_on_statusbar('Fade requested (this is a time-consuming task).')
                    mode = {self.actionFadeBoth: 'both', self.actionFadeVideo: 'video', self.actionFadeAudio: 'audio'}[self.trim_mode_action_group.checkedAction()]
                    fade_cmd_parts = []
                    if mode == 'video' or mode == 'both':                           # fade video to/from black
                        fade_parts = []
                        if minimum > 0:
                            seconds = minimum / frame_rate
                            fade_parts.append(f'fade=t=in:st=0:d={seconds}')        # `d` defaults to ~1 second
                        if maximum < frame_count:
                            seconds = maximum / frame_rate
                            delta = duration - seconds - 0.1                        # TODO: 0.1 offset since fade out sometimes doesn't finish on time
                            fade_parts.append(f'fade=t=out:st={seconds}:d={delta}')
                        if fade_parts:
                            fade_cmd_parts.append(f'-vf "{",".join(fade_parts)}{" -c:a copy" if mode != "both" else ""}"')
                    if mode == 'audio' or mode == 'both':                           # fade audio in/out
                        fade_parts = []
                        if minimum > 0:
                            seconds = minimum / frame_rate
                            fade_parts.append(f'afade=t=in:st=0:d={seconds}')       # `d` defaults to ~1 second
                        if maximum < frame_count:
                            seconds = maximum / frame_rate
                            delta = duration - seconds - 0.1                        # TODO: 0.1 offset since fade out sometimes doesn't finish on time
                            fade_parts.append(f'afade=t=out:st={seconds}:d={delta}')
                        if fade_parts:
                            fade_cmd_parts.append(f'-af "{",".join(fade_parts)}{" -c:v copy" if mode != "both" and mime == "video" else ""}"')
                    if fade_cmd_parts:
                        cmd = f'-i %in {" ".join(fade_cmd_parts)}'
                        intermediate_file = edit.ffmpeg(intermediate_file, cmd, dest, 'Fading')

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
                    cmd = f'-i %in -filter:v "crop={crop_width}:{crop_height}:{round(crop_left)}:{round(crop_top)}"'
                    intermediate_file = edit.ffmpeg(intermediate_file, cmd, dest, 'Cropping')
                vwidth = round(crop_width) - 1                                      # update dimensions
                vheight = round(crop_height) - 1

            # resize video/GIF/image, or change audio file's tempo
            # TODO: this is a relatively fast operation and SHOULD be done much sooner but that requires...
            # ...dynamic ordering of operations (see above) and adjusting `crop_selection`/`lfp` and I'm lazy
            if op_resize is not None:       # audio -> https://stackoverflow.com/q/25635941/13010956
                log_note = ' (this is a time-consuming task)' if mime == 'video' else ' (this should be a VERY quick operation)' if mime == 'audio' else ''
                log_on_statusbar(f'{mime.capitalize()} resize requested{log_note}.')
                if mime == 'audio':         # for audio: only duration (as a multiplier, e.g. 1.5x) is given
                    duration_factor = op_resize
                    edit.frame_count = (duration / duration_factor) * frame_rate
                    cmd = f'-i %in -filter:a atempo="{duration_factor}"'
                    intermediate_file = edit.ffmpeg(intermediate_file, cmd, dest, 'Adjusting tempo')
                else:                       # for videos/images: (width, height) tuple
                    vwidth, vheight = scale(vwidth, vheight, *op_resize)
                    if is_static_image:     # ^ pillow can't handle 0/-1 and ffmpeg is stupid (see below) -> scale right away
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
                        cmd = f'-i %in -vf "scale={vwidth}:{vheight}" -crf 28 -c:a copy'
                        intermediate_file = edit.ffmpeg(intermediate_file, cmd, dest, 'Resizing')

            # rotate video/GIF/image
            # TODO: this should use Pillow for images/GIFs but I'm lazy
            # NOTE: ^ `get_PIL_safe_path` only still exists because of this
            if op_rotate_video is not None:
                log_on_statusbar('Video rotation/flip requested (this is a time-consuming task).')
                cmd = f'-i %in -vf "{op_rotate_video}" -crf 28 -c:a copy'
                if is_static_image:
                    with get_PIL_safe_path(original_path=video, final_path=dest) as temp_path:
                        edit.ffmpeg(intermediate_file, cmd, temp_path, 'Rotating')
                        intermediate_file = dest
                else:
                    intermediate_file = edit.ffmpeg(intermediate_file, cmd, dest, 'Rotating')
                if op_rotate_video == 'transpose=clock' or op_rotate_video == 'transpose=cclock':
                    vwidth, vheight = vheight, vwidth           # update dimensions

            # replace audio (entirely - TODO: track-by-track replacement)
            if op_replace_audio is not None:
                log_on_statusbar('Audio replacement requested.')
                audio = op_replace_audio    # TODO -shortest (before output) results in audio cutting out ~1 second before end of video despite the audio being longer
                cmd = f'-i %in -i "{audio}" -c:v copy -map 0:v:0 -map 1:a:0'
                intermediate_file = edit.ffmpeg(intermediate_file, cmd, dest, 'Replacing audio')

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
                            successful = False
                            return log_on_statusbar(f'(!) Failed to crop image that isn\'t divisible by 2: {format_exc()}')
                    edit.frame_count = int(get_audio_duration(audio) * 25)          # ffmpeg defaults to using 25fps for this
                    cmd = f'-loop 1 -i %in -i "{audio}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest'
                    intermediate_file = edit.ffmpeg(intermediate_file, cmd, dest, 'Adding audio track')
                elif is_gif:                # gifs
                    log_on_statusbar('Adding audio to animated GIF (final video duration may not exactly line up with audio).')
                    is_gif = False                              # mark that this is no longer a gif
                    edit.frame_count = int(get_audio_duration(audio) * frame_rate)
                    cmd = f'-stream_loop -1 -i %in -i "{audio}" -filter_complex amix=inputs=1 -shortest'
                    intermediate_file = edit.ffmpeg(intermediate_file, cmd, dest, 'Adding audio track')
                else:                       # video/audio TODO: adding "-stream_loop -1" and "-shortest" sometimes cause endless videos because ffmpeg is garbage
                    log_on_statusbar('Additional audio track requested.')
                    the_important_part = '-map 0:v:0 -map 1:a:0 -c:v copy' if (mime == 'video' and audio_track_count == 0) else '-filter_complex amix=inputs=2'
                    cmd = f'-i %in -i "{audio}" {the_important_part}'               # ^ use special cmd for audio-less videos
                    intermediate_file = edit.ffmpeg(intermediate_file, cmd, dest, 'Adding audio track')

            # isolate audio or all video tracks (does not turn file into an image/GIF)
            if op_isolate_track is not None:                    # NOTE: This can degrade audio quality slightly.
                noun, track = op_isolate_track                  # NOTE: video can keep all its tracks, but audio MUST pick just one
                log_on_statusbar(f'{noun}-track removal requested.')
                cmd = f'-i %in -q:a 0 -map 0:a:{track}' if noun == 'Audio' else '-i %in -c copy -an'
                intermediate_file = edit.ffmpeg(intermediate_file, cmd, dest, f'Removing {noun.lower()} track')

            # amplify audio (TODO: do math to chain several of these together at once to circumvent the max volume limitation)
            if op_amplify_audio is not None:
                log_on_statusbar('Audio amplification requested.')
                cmd = f'-i %in -filter:a "volume={op_amplify_audio}"'
                intermediate_file = edit.ffmpeg(intermediate_file, cmd, dest, 'Amplifying audio')

        # the code block formerly known as `self.cleanup_edit_exception()`
        except Exception as error:
            successful = False
            qthelpers.deleteTempPath(dest, 'FFmpeg file')

            # ffmpeg had a memory error
            text = str(error)
            if 'malloc of size' in text:
                start_index = text.find('malloc of size') + 14
                size = int(text[start_index:text.find('failed', start_index)])
                if size < 1048576:      size_label = f'{size / 1024:.0f}kb'
                elif size < 1073741824: size_label = f'{size / 1048576:.2f}mb'
                else:                   size_label = f'{size / 1073741824:.2f}gb'
                msg = (f'FFmpeg failed to allocate {size_label} of RAM. Rarely, this'
                       '\nmay happen even when plenty of free RAM is available.'
                       '\n\nIf the issue persists, try the following:'
                       '\n • Check if the issue happens with other files'
                       '\n • Restart PyPlayer'
                       '\n • Restart your computer'
                       '\n • Reinstall FFmpeg'
                       '\n • Pray'
                       '\n\nNo changes have been made. Feel free to try again.')
                self.popup_signal.emit(                         # TODO it *might* be nice to have retry/cancel options
                    dict(
                        title='FFmpeg error',
                        text=msg,
                        icon='warning',
                        **self.get_popup_location_kwargs()
                    )
                )

            # we tried to concat videos with different dimensions (if we got this far, assume FFprobe isn't available)
            # -> start by reopening concat dialog with previous files (NOTE: state won't be fully restored)
            elif 'do not match the corresponding output link' in text:
                self.concatenate_signal.emit(None, op_concat['files'])
                header = ('All files must have the same dimensions for re-encoded concatenation.\n'
                          'You\'ll need to crop or resize the offending files individually.')
                self.popup_signal.emit(
                    dict(
                        title='Concatenation cancelled!',
                        text=header,
                        icon='warning',
                        flags=Qt.WindowStaysOnTopHint,          # needed so it appears over the concat dialog
                        **self.get_popup_location_kwargs()
                    )
                )

            # edit was intentionally cancelled by the user
            elif text == 'Cancelled.':
                if not start_time: log_on_statusbar(f'{log_noun or "Save"} cancelled.')
                else: log_on_statusbar(f'{log_noun or "Save"} cancelled after {get_verbose_timestamp(get_time() - start_time)}.')

            # edit failed for an unknown reason
            else:
                if not start_time: log_on_statusbar(f'(!) {log_noun.upper() or "SAVE"} FAILED: {format_exc()}')
                else: log_on_statusbar(f'(!) {log_noun.upper() or "SAVE"} FAILED AFTER {get_verbose_timestamp(get_time() - start_time).upper()}: {format_exc()}')

        # --- Post-edit cleanup & opening our newly edited media ---
        finally:
            try:
                # close handle to destination. if there wasn't already a...
                # ...file there, delete the temp file our handle created
                close_handle(dest_handle, delete=not DEST_ALREADY_EXISTED)

                # clean up temp paths if we have any
                for path in temp_paths:
                    if exists(path):
                        qthelpers.deleteTempPath(path, 'edit-path')

                # confirm/validate/cleanup our operations
                if operations and successful:
                    to_delete = video if not op_concat else op_concat['files']
                    true_dest = self._cleanup_edit_output(dest, final_dest, new_ctime, new_mtime, delete_mode, to_delete, log_noun)
                    if not true_dest:
                        qthelpers.deleteTempPath(dest, 'FFmpeg file')
                        return

                    # auto-open output if desired or we're watching the media that just got edited
                    if (open_after_save) if open_after_save is not None else (self.video == video):
                        remember_old_file = not op_concat and settings.checkCycleRememberOriginalPath.checkState() == 2
                        self.open_from_thread(
                            file=true_dest,
                            _from_cycle=True,           # skips unnecessary validation (like checking if `file` is locked)
                            _from_edit=True,
                            focus_window=settings.checkFocusOnEdit.isChecked(),
                            pause_if_focus_rejected=settings.checkEditFocusRejectedPause.isChecked(),
                            beep_if_focus_rejected=settings.checkEditFocusRejectedBeep.isChecked(),
                            update_original_video_path=not remember_old_file
                        )                               # gifs will often just... pause themselves after an edit
                        if is_gif:                      # -> this is the only way i've found to fix it
                            self.force_pause_signal.emit(False)

                    # handle what to do if the newly edited file is not auto-opened
                    else:
                        if settings.checkEditOpenRejectedBeep.isChecked():
                            app.beep()
                        if settings.checkEditOpenRejectedAddToRecents.isChecked():
                            recent_files = self.recent_files
                            if true_dest in recent_files:
                                recent_files.append(recent_files.pop(recent_files.index(true_dest)))
                            else:                       # ^ move pre-existing recent file to front
                                recent_files.append(true_dest)
                                max_len = settings.spinRecentFiles.value()
                                self.recent_files = recent_files[-max_len:]
                        if settings.checkTextOnSave.isChecked():
                            show_on_player(f'{log_noun or "Changes"} saved to {true_dest}.')

                        # our current file might have been marked -> manually update action/button
                        current_video_is_marked = self.video in self.marked_for_deletion
                        self.actionMarkDeleted.setChecked(current_video_is_marked)
                        self.buttonMarkDeleted.setChecked(current_video_is_marked)

                    # open output in explorer if desired
                    if explore_after_save:
                        qthelpers.openPath(true_dest, explore=True)

                    # add our successful edit to our recent list (max of 25)
                    recent_edits = self.recent_edits
                    if true_dest in recent_edits:       # move pre-existing recent file to front
                        recent_edits.append(recent_edits.pop(recent_edits.index(true_dest)))
                    else:
                        recent_edits.append(true_dest)
                        max_len = settings.spinRecentEdits.value()
                        self.recent_edits = recent_edits[-max_len:]

                    # clear out inactive save remnants from this edit or earlier in a thread-safe manner
                    # this way, we only clear out remnants that have had edits started and finished after they were created
                    logging.debug(f'Clearing any remnants older than {start_time}')
                    remnant_times = sorted(self.save_remnants.keys())
                    for remnant_time in remnant_times:
                        if remnant_time > start_time:
                            break
                        try:                            # ignore marker for this edit's remnant
                            if remnant_time == start_time or not self.save_remnants[remnant_time].get('_in_progress', False):
                                logging.debug(f'Removing remnant from {remnant_time}')
                                del self.save_remnants[remnant_time]
                        except:
                            logging.warning(f'(!) Failed to remove stale save remnant from {remnant_time}: {format_exc()}')

                    # log our changes or lack thereof
                    log_on_statusbar(f'{log_noun or "Changes"} saved to {true_dest} after {get_verbose_timestamp(get_time() - start_time)}.')
                elif successful:                        # log our lack of changes
                    return log_on_statusbar('No changes have been made.')

            except:
                log_on_statusbar(f'(!) Post-{log_noun.lower() or "save"} cleanup failed: {format_exc()}')
            finally:
                self.locked_files.discard(dest)         # unlock temp destination
                self.locked_files.discard(final_dest)   # unlock final destination
                self.setFocus(True)                     # restore keyboard focus so we can use hotkeys again
                self.remove_edit(edit)                  # remove `Edit` object and update priority
                if start_time in self.save_remnants:    # mark save remnant as safe to remove, if still present
                    try: self.save_remnants[start_time]['_in_progress'] = False
                    except: logging.warning('(!) Failed to mark save remnant as safe to remove: ' + format_exc())
                logging.info(f'Remaining locked files after {log_noun.lower() or "edit"}: {self.locked_files}')


    def update_gif_progress(self, frame: int):
        ''' Updates animated GIF progress by manually looping
            the GIF when outside the designated trim markers. '''
        if self.is_gif:
            slider = self.sliderProgress
            if self.minimum <= frame <= self.maximum:
                update_progress(frame)                  # HACK: literally, forcibly repaint to stop slider from...
                if frame != self.minimum:               # ...eventually freezing on animated GIFs in fullscreen...
                    slider.repaint()                    # ...(no idea why it happens)
            elif not slider.grabbing_clamp_minimum and not slider.grabbing_clamp_maximum:
                set_gif_position(self.minimum)          # reset to minimum if we're not dragging the markers


    def update_progress(self, frame: int):
        ''' Updates every section of the UI to reflect the
            current `frame`. Clamps playback to desired trims.
            Loops if necessary. Locks spinboxes while updating. '''
        if not self.minimum <= frame <= self.maximum:
            if not (self.sliderProgress.grabbing_clamp_minimum or self.sliderProgress.grabbing_clamp_maximum):
                frame = min(self.maximum, max(self.minimum, frame))

                # pause or loop media if we've reached the end of our desired trim
                if frame >= self.maximum and self.buttonTrimEnd.isChecked():
                    if not self.actionLoop.isChecked():
                        self.force_pause(True)
                        set_and_update_progress(self.maximum, SetProgressContext.RESET_TO_MAX)
                    else:
                        return set_and_update_progress(self.minimum, SetProgressContext.RESET_TO_MIN)

        current_time = round(self.duration_rounded * (frame / self.frame_count), 2)
        self.current_time = current_time

        # this is `util.get_hms` but inlined, for optimization
        h_remainder = current_time % 3600
        h = int(current_time // 3600)
        m = int(h_remainder // 60)
        s = int(h_remainder % 60)
        ms = int(round((current_time - int(current_time)) * 100, 4))

        set_progress_slider(frame)
        if not current_time_lineedit_has_focus():       # use cleaner format for time-strings on videos > 1 hour
            set_current_time_text(f'{m:02}:{s:02}.{ms:02}' if h == 0 else f'{h}:{m:02}:{s:02}')

        set_hour_spin(h)
        set_minute_spin(m)
        set_second_spin(s)
        set_frame_spin(frame)


    def _update_progress_slot(self, frame: int):
        ''' A slot for updating the UI in a thread-safe manner. Because of the
            possible delay, this slot also checks for `self.frame_override`. '''
        if self.frame_override != -1:
            update_progress(self.frame_override)
        else:
            update_progress(frame)


    def update_time_spins(self):
        ''' Handles the hour, minute, and second spinboxes. Calculates
            the next frame based on the new values, and updates the progress
            UI accordingly. If the new frame is outside the bounds of the
            media, it's replaced with the current frame and the progress
            UI is reset to its previous state. '''

        # return if user is not manually setting the time spins
        if self.lock_progress_updates: return
        self.lock_progress_updates = True               # lock progress updates to prevent recursion errors from multiple elements updating at once

        try:
            seconds = self.spinHour.value() * 3600
            seconds += self.spinMinute.value() * 60
            seconds += self.spinSecond.value()

            old_frame = self.spinFrame.value()
            excess_frames = old_frame % self.frame_rate
            new_frame = round((seconds * self.frame_rate) + excess_frames)

            # if the new frame is out of bounds, just reset the UI to match the old frame
            if self.minimum < new_frame > self.maximum:
                update_progress(old_frame)
            else:
                set_and_update_progress(new_frame, SetProgressContext.NAVIGATION_EXACT)
            logging.debug(f'Manually updating time-spins: seconds={seconds} frame {old_frame} -> {new_frame} ({excess_frames} excess frame(s))')

        except: logging.error(f'(!) UPDATE_TIME_SPINS FAILED: {format_exc()}')
        finally: self.lock_progress_updates = False     # always release lock on progress updates


    def update_frame_spin(self, frame: int):
        ''' Sets progress to `frame` if media is paused. This is meant as a
            slot for `self.spinFrame` - Do not use this for frame seeking. '''
        if not self.is_paused or self.lock_progress_updates: return
        self.lock_progress_updates = True               # lock progress updates to prevent recursion errors from multiple elements updating at once

        try: player.set_frame(frame)
        except: logging.warning(f'Abnormal error while updating frame-spins: {format_exc()}')
        finally: self.lock_progress_updates = False     # always release lock on progress updates


    def manually_update_current_time(self):
        ''' Sets progress to the timestamp within `self.lineCurrentTime`.
            Supports various formats, including percentages and raw seconds. '''
        text = self.lineCurrentTime.text().strip()
        if not text: return
        logging.info(f'Manually updating current time "label" to {text}')

        try:
            if '%' in text:                             # do regular strip() again in case spaces were placed between number and %
                percent = float(text.strip('%').strip()) / 100
                frame = self.frame_count * percent
            else:
                seconds = 0
                parts = tuple(float(part) for part in text.split(':') if part)    # float() takes care of milliseconds at the end
                if len(parts) == 3:   seconds += (parts[0] * 3600) + (parts[1] * 60) + parts[2]
                elif len(parts) == 2: seconds += (parts[0] * 60) + parts[1]
                elif len(parts) == 1: seconds = parts[0]
                frame = int(seconds * self.frame_rate)  # int() instead of ceil() to ensure we don't go too far

            if self.minimum <= frame <= self.maximum:
                try:
                    self.lock_progress_updates = True
                    set_and_update_progress(frame, SetProgressContext.NAVIGATION_EXACT)
                except: logging.warning(f'Abnormal error while locking/setting/updating progress: {format_exc()}')
                finally: self.lock_progress_updates = False

        except: pass                                    # ignore invalid inputs
        finally: self.lineCurrentTime.clearFocus()      # clear focus after update no matter what


    def page_step(self, step: float = 0.1, forward: bool = True, scaled: bool = True):
        ''' Page-steps through the progress slider by `step`, a percentage from
            0-1, `forward` or backwards. If `step` is negative, `forward` is
            inverted. If `scaled` is True, `step` is scaled to `self.minimum`
            and `self.maximum`, otherwise `self.frame_count`. Page-steps are
            clamped to `self.minimum`/`self.maximum` regardless. '''

        old_frame = get_ui_frame()
        maximum = self.maximum
        minimum = self.minimum
        if scaled: step = int((maximum - minimum) * step)
        else:      step = int(self.frame_count * step)

        if forward and step > 0:
            if old_frame == maximum:
                return set_progress_slider(old_frame)   # visually clamp slider to maximum if we can't go forward
            new_frame = min(maximum, old_frame + step)
        else:
            new_frame = max(minimum, old_frame - step)

        set_and_update_progress(new_frame, SetProgressContext.NAVIGATION_RELATIVE)
        if self.restarted and settings.checkNavigationUnpause.isChecked():
            self.force_pause(False)                     # auto-unpause after restart if desired
            self.restarted = False


    def navigate(self, forward: bool, seconds_spinbox: QtW.QSpinBox):   # slightly longer than it could be, but cleaner/more readable
        ''' Navigates `forward` or backwards through the current
            media by the value specified in `seconds_spinbox`.

            NOTE: `seconds` has been replaced by `seconds_spinbox`
            since the former was never explicitly used. '''

        # cycle images with basic navigation keys
        if self.is_static_image: return self.cycle_media(next=forward)
        old_frame = get_ui_frame()
        seconds = seconds_spinbox.value()

        # calculate and update to new frame as long as it's within our bounds
        if forward:                                     # media will wrap around cleanly if it goes below 0/above max frames
            if old_frame == self.frame_count and settings.checkNavigationWrap.isChecked(): new_frame = 0
            else: new_frame = min(self.maximum, int(old_frame + self.frame_rate_rounded * seconds))
        else:                                           # NOTE: only wrap start-to-end if we're paused
            if old_frame == 0 and self.is_paused and settings.checkNavigationWrap.isChecked(): new_frame = self.frame_count
            else: new_frame = max(self.minimum, int(old_frame - self.frame_rate_rounded * seconds))

        # set progress to new frame while doing necessary adjustments/corrections/overrides
        set_and_update_progress(new_frame, SetProgressContext.NAVIGATION_RELATIVE)

        # HACK: if navigating away from end of media while unpaused and we HAVEN'T restarted...
        # ...yet -> ignore the restart we're about to do (does this only apply to VLC?)
        self.ignore_imminent_restart = old_frame == self.frame_count and not self.is_paused and not self.restarted

        # auto-unpause after restart if desired
        if self.restarted and settings.checkNavigationUnpause.isChecked():
            self.force_pause(False)
            self.restarted = False

        # show new position as a marquee if desired
        if self.isFullScreen() and settings.checkTextOnFullScreenPosition.isChecked():
            h, m, s, _ = get_hms(self.current_time)
            current_text = f'{m:02}:{s:02}' if h == 0 else f'{h}:{m:02}:{s:02}'
            max_text = self.labelMaxTime.text()[:-3] if self.duration_rounded < 3600 else self.labelMaxTime.text()
            show_on_player(f'{current_text}/{max_text}')

        logging.debug(f'Navigated {"forwards" if forward else "backwards"} {seconds} second(s), going from frame {old_frame} to {new_frame}')


    # ---------------------
    # >>> FFMPEG <<<
    # ---------------------
    def _cleanup_edit_output(
        self,
        temp_dest: str,
        final_dest: str,
        ctime: float,
        mtime: float,
        delete_mode: int = 0,
        to_delete: str | tuple[str] = None,
        noun: str = ''
    ) -> str | None:
        ''' Ensures `temp_dest` exists, isn't empty, and produces a valid probe.
            If unsuccessful, None is returned, the specific failure is logged
            (referring to the file as `noun`), and `temp_dest` is deleted.
            Once validated, `temp_dest` is renamed to `final_dest` with its
            timestamps set to `ctime`/`mtime`.

            - `delete_mode=1` - `to_delete` is marked for deletion
            - `delete_mode=2` - `to_delete` is deleted/recycled outright
            - NOTE: `final_dest` cannot be marked or deleted.

            If everything is valid but `temp_dest` cannot be renamed, a popup is
            shown and `temp_dest` is returned. Otherwise, returns `final_dest`.

            NOTE: If `temp_dest` is valid, this function is relatively "slow"
            as we must wait for a fresh probe file to be created. '''
        try:
            noun = noun or 'Media'
            if not exists(temp_dest):
                return log_on_statusbar(f'(!) {noun} saved without error, but never actually appeared. Possibly an FFmpeg error. No changes have been made.')
            if os.stat(temp_dest).st_size == 0:
                return log_on_statusbar(f'(!) {noun} saved without error, but was completely empty. Possibly an FFmpeg error. No changes have been made.')

            # next part takes a while so show text on the progress bar if this is the last edit
            if len(self.edits_in_progress) == 1:
                self.set_save_progress_format_signal.emit('Cleaning up...')

            # NOTE: this probe can't be reused since `temp_dest` is about to be renamed,...
            # ...but cleanup is 100x easier if we do this now rather than later
            new_probe = probe_files(temp_dest, refresh=True, write=False)
            if not new_probe:                   # no probe returned
                return log_on_statusbar(f'(!) {noun} saved without error, but cannot be probed. Possibly an FFmpeg error. No changes have been made.')
            elif not new_probe[temp_dest]:      # empty probe returned TODO: not possible anymore. add parameter for old `probe_files()` behavior?
                return log_on_statusbar(f'(!) {noun} saved without error, but returned an invalid probe. Possibly an FFmpeg error. No changes have been made.')

            # handle deletion behavior, ignoring `final_dest`
            if isinstance(to_delete, str): to_delete = (to_delete,) if to_delete != final_dest else None
            elif to_delete:                to_delete = [file for file in to_delete if file != final_dest]
            if to_delete:                       # 1 -> mark for deletion, 2 -> recycle/delete outright
                if delete_mode == 1:       self.mark_for_deletion(*to_delete, mark=True, mode='')
                elif delete_mode == 2:     self.delete(*to_delete, cycle=False)
                #elif replacing_original:       # TODO add setting for this behavior?
                #    temp_name = add_path_suffix(video, '_original', unique=True)
                #    os.rename(video, temp_name)
                #    video = temp_name

            # rename `dest` back to `final_dest` if possible
            if self.video == final_dest:        # stop player if necessary
                self.stop()
            try:
                if exists(final_dest): os.replace(temp_dest, final_dest)
                else:                  os.rename(temp_dest, final_dest)
            except PermissionError:
                dirname = os.path.dirname(temp_dest)
                temp_filename = os.path.basename(temp_dest)
                final_filename = os.path.basename(final_dest)
                header = 'Unable to rename our temporary file to our final output path.'
                body = f'\n\nFolder: {dirname}\n---\nFilenames: "{temp_filename}" -> "{final_filename}"\n\n'
                footer = 'Either the output path or the temporary file is currently being used by another process. The temporary file has not be renamed.'
                self.popup_signal.emit(
                    dict(
                        title='Output is in use!',
                        text=f'{header}{body}{footer}',
                        icon='warning',
                        **self.get_popup_location_kwargs()
                    )
                )
                final_dest = temp_dest

            # update `final_dest`'s ctime/mtime if necessary
            self.set_file_timestamps(
                path=final_dest,
                ctime=ctime,
                mtime=mtime
            )

            # delete `final_dest`'s probe file in rare event it becomes stale (size & mtime/ctime were not altered)
            self.open_probe_file(file=final_dest, delete=True, verbose=False)
            return final_dest
        except:
            return log_on_statusbar(f'(!) Post-{noun.lower() or "save"} destination cleanup failed: {format_exc()}')
        finally:                                # make sure `temp_dest` does not actually have a probe file
            self.open_probe_file(file=temp_dest, delete=True, verbose=False)


    def is_safe_to_edit(self, *infiles: str, dest: str = None, popup: bool = True) -> bool:
        ''' Returns True if `dest` and `infiles` are safe to use for FFmpeg
            operations. If not and `popup` is True, a detailed warning is shown.
            Checks if `dest`/`infiles` are in `self.locked_files` and tries
            renaming `dest` to itself to ensure no handles exist. Stops the
            player before the rename-check if `dest` is `self.video`. '''
        msg = ''
        if dest in infiles:                     # check if we're overwriting `dest`
            infiles = [file for file in infiles if file != dest]

        # check if our files were explicitly locked
        locked_files = self.locked_files
        output_locked = dest in locked_files
        locked = [(i, f) for i, f in enumerate(infiles) if f in locked_files]
        if locked or output_locked:
            logging.info(f'(?) Files to be concatenated and/or the output are locked, cancelling: {locked}')

            # generate an appropriate title, body, and list of offending files depending on how many...
            # ...files were provided, how many are invalid, and if both the output AND input files were bad
            if not popup:
                header = ''
                footer = ''
            elif output_locked:
                if len(locked) > 1:
                    title = 'Output and input files are in use!'
                    header = 'The output path and the files at the following indexes are set to be overwritten by different edit(s):'
                    footer = f'Output: {dest}\n' + '\n'.join(f'{index + 1}. {file}' for index, file in locked)
                elif len(locked) == 1:
                    title = 'Output and input file are both in use!'
                    if len(infiles) > 1:
                        header = 'The output path and the file at the following index are set to be overwritten by different edit(s):'
                        footer = '\n'.join(f'{index + 1}. {file}' for index, file in locked)
                    else:
                        header = 'The output path and input file are set to be overwritten by different edit(s):'
                        footer = f'Output: {dest}\nInput: {infiles[0]}'
                else:
                    title = 'Output is in use!'
                    header = 'The output path is set to be overwritten by a different edit:'
                    footer = dest
            else:
                if len(locked) == 1:
                    title = 'Input file is in use!'
                    if len(infiles) > 1:
                        header = 'The file at the following index is set to be overwritten by a different edit:'
                        footer = '\n'.join(f'{index + 1}. {file}' for index, file in locked)
                    else:
                        header = 'The input file is set to be overwritten by a different edit:'
                        footer = infiles[0]
                else:
                    title = 'Input files are in use!'
                    header = 'The files at the following indexes are set to be overwritten by different edit(s):'
                    footer = '\n'.join(f'{index + 1}. {file}' for index, file in locked)
            msg = f'{header}\n\n{footer}'

        # check if we might not be able to write to our `dest` when the edit is finished
        elif dest and exists(dest):
            try:
                if dest == self.video:          # stop player to make sure nothing else is using our destination
                    self.stop()
                os.rename(dest, dest)           # rename file to itself as a simple access-check
            except PermissionError:             # the path still cannot be written to
                title = 'Output is in use!'
                msg = f'The output path is currently being used by another process:\n\n{dest}'

        if msg:
            if popup:
                qthelpers.getPopup(             # TODO: add the signal version too if we need it
                    title=title,
                    text=msg,
                    icon='warning',
                    **self.get_popup_location_kwargs()
                ).exec()
            return False
        return True


    def cancel_all(self, *, wait: bool = False):
        ''' Cancels all edits in progress. If `wait` is True, this method
            blocks until the offending `Edit` objects are no longer in
            `self.edits_in_progress`, while ignoring any edits started
            after this method is called. '''

        # NOTE: this method works on the assumption a cancelled edit isn't removed from...
        # ...`self.edits_in_progress` until its FFmpeg process is confirmed to be killed
        log_on_statusbar('Cancelling all active edits...')
        if wait: to_cancel = self.edits_in_progress.copy()
        else:    to_cancel = self.edits_in_progress

        for edit in to_cancel:
            edit.cancel()

        if wait and to_cancel:                  # don't wait if we never had anything to cancel
            app.processEvents()                 # process events so our statusbar message shows up
            while True:
                sleep(0.1)
                for edit in to_cancel:
                    if edit in self.edits_in_progress:
                        break
                else:                           # else in a for-loop means we didn't break
                    log_on_statusbar('All edits cancelled, killed, and cleaned up.')
                    return


    def pause_all(self, paused: bool = True):
        ''' Sets the pause-state of all edits to `paused`. '''
        verb = 'Pausing' if paused else 'Resuming'
        logging.info(verb + ' all active edits...')
        for edit in self.edits_in_progress:
            edit.pause(paused=paused)


    def add_edit(self, edit: Edit):
        ''' Adds an `edit` to `self.edits_in_progress` and manually
            refreshes the progress bar in case the current edit is paused. '''
        self.edits_in_progress.append(edit)
        priority_edit = self.get_edit_with_priority()
        if priority_edit:
            priority_edit.set_progress_bar(value=priority_edit.value)


    def remove_edit(self, edit: Edit):
        ''' Removes an `edit` from `self.edits_in_progress` and updates edit
            priority if `edit` was the priority edit (or hides edit progress
            altogether if there are no edits remaining), otherwise refreshes
            the progress bar in case the actual priority edit is paused. '''
        self.edits_in_progress.remove(edit)
        if edit.has_priority or not self.edits_in_progress:
            self.reset_edit_priority()
        else:
            priority_edit = self.get_edit_with_priority()
            if priority_edit:
                priority_edit.set_progress_bar(value=priority_edit.value)


    def get_edit_with_priority(self) -> Edit:
        ''' Returns the `Edit` object in `self.edits_in_progress` that currently
            has priority. Only returns the first one found. '''
        for edit in self.edits_in_progress:
            if edit.has_priority:
                return edit


    def cycle_edit_priority(self):
        ''' Gives priority to the `Edit` at `self.edits_in_progress`'s next index,
            wrapping if necessary. Updates the progress bar immediately. '''
        try:
            edits = self.edits_in_progress
            for new_index, save in enumerate(edits, start=1):
                if save.has_priority:
                    save.has_priority = False
                    edits[new_index % len(edits)].give_priority()
                    break
        except ZeroDivisionError:
            logging.info('(?) Tried to cycle edit priority, but `self.edits_in_progress` became empty while doing so.')
        except:
            log_on_statusbar(f'(!) Unexpected error while cycling edit: {format_exc()}')


    def reset_edit_priority(self, _paranoia: bool = False):
        ''' Sets priority to the `Edit` in `self.edits_in_progress` closest
            to completion, preferring an unpaused one if possible. If 20+
            edits are running, the first unpaused edit is used instead.
            If they're all paused, index 0 is used instead. If no edits
            are remaining, the progress bar is reset. '''
        if not _paranoia:
            self.lock_edit_priority = True      # lock priority so the progress bar doesn't flicker from a rare double-switch

        # NOTE: Dealing with the high-precision slider has made me very, very paranoid about race conditions.
        # TODO: we should probably calculate ETAs and use those instead (and display them somewhere)
        try:
            sleep(0.05)                         # sleep to absolutely ensure we don't double-switch priority
            edits = self.edits_in_progress
            if edits:

                # 1 edit, switch priority immediately
                if len(edits) == 1:
                    edits[0].give_priority(ignore_lock=True, conditional=True)

                # 2-19 edits, switch to edit closest to completion
                elif len(edits) < 20:
                    highest_edit = None
                    highest_unpaused_edit = None
                    highest_value = -1
                    highest_unpaused_value = -1
                    for edit in edits:
                        percent = edit.value
                        if percent > highest_value:
                            highest_value = percent
                            highest_edit = edit
                        if not edit._is_paused:
                            if percent > highest_unpaused_value:
                                highest_unpaused_value = percent
                                highest_unpaused_edit = edit

                    # switch to highest unpaused edit if one exists, otherwise fallback to paused ones
                    if highest_unpaused_edit:
                        highest_unpaused_edit.give_priority(ignore_lock=True, conditional=True)
                    elif highest_edit:          # they're all paused
                        highest_edit.give_priority(ignore_lock=True, conditional=True)

                # 20+ edits in progress, just change priority fast
                else:
                    for edit in edits:
                        if not edit._is_paused:
                            edit.give_priority(ignore_lock=True, conditional=True)
                            break
                    else:                       # we didn't break the for-loop (they're all paused)
                        edits[0].give_priority(ignore_lock=True, conditional=True)

                # make sure something actually got priority
                if self.get_edit_with_priority() is None:
                    if not _paranoia:           # somehow, nothing got set. try again?
                        logging.warning('(!) Edit priority auto-update somehow accomplished nothing, resorting to emergency measures.')
                        self.reset_edit_priority(_paranoia=True)
                    elif edits:                 # nothing got set AGAIN? just try and brute-force the first edit
                        edits[0].give_priority(ignore_lock=True, update_others=True)
                    else:                       # failed repeatedly, yet there aren't even any edits. just hide everything
                        self.hide_edit_progress()

            # no edits are in progress anymore, hide progress bar and reset titlebar/taskbar
            else:
                self.hide_edit_progress()

        # uh oh spaghettios
        except:
            logging.warning(f'(!) Edit priority auto-update is failing, trying last-ditch effort: {format_exc()}')
            if not edits:                       # likely failed because all edits finished while this method was executing
                self.hide_edit_progress()
            else:
                try:                            # failed because... huh? try and set priority one more time
                    edits[0].give_priority(ignore_lock=True, update_others=True)
                except:                         # getting here basically requires several consecutive race conditions
                    log_on_statusbar(f'(!) Edit priority auto-update failed BADLY: {format_exc()}')
        finally:
            if not _paranoia:
                self.lock_edit_priority = False


    def hide_edit_progress(self):
        ''' Resets the editing progress bar to zero and hides its
            widget on the statusbar while clearing its percentage
            from the titlebar and taskbar button (on Windows). You
            should probably use `self.reset_edit_priority()` instead. '''
        self.set_save_progress_visible_signal.emit(False)           # hide the progress bar
        self.set_save_progress_max_signal.emit(0)                   # reset progress bar values
        self.set_save_progress_value_signal.emit(0)
        if constants.IS_WINDOWS and settings.checkTaskbarProgressEdit.isChecked():
            self.taskbar_progress.reset()                           # reset taskbar progress (`setVisible(False)` not needed)
        refresh_title()                                             # refresh title to hide progress percentage


    def set_trim_start(self, enabled: bool):
        ''' Sets the start-point marker's check-state to `enabled`, sets it to
            the current frame, validates it, and updates the UI accordingly. '''
        if not self.video:       return self.buttonTrimStart.setChecked(False)
        if self.is_static_image: return self.buttonTrimStart.setChecked(False)

        self.buttonTrimStart.setChecked(enabled)
        self.sliderProgress.clamp_minimum = enabled

        if enabled:
            desired_minimum = get_ui_frame()
            if desired_minimum > self.maximum:
                set_and_update_progress(self.maximum, SetProgressContext.RESET_TO_MAX)
                self.minimum = self.maximum
                show_on_statusbar('You cannot set the start of your trim after the end of it.')
            else:
                self.minimum = desired_minimum

            h, m, s, ms = get_hms(self.current_time)                # use cleaner format for time-strings on videos > 1 hour
            if self.duration_rounded < 3600: self.buttonTrimStart.setText(f'{m}:{s:02}.{ms:02}')
            else:                            self.buttonTrimStart.setText(f'{h}:{m:02}:{s:02}')
        else:
            self.minimum = self.sliderProgress.minimum()
            self.buttonTrimStart.setText('Start' if self.is_trim_mode() else ' Fade to ')


    def set_trim_end(self, enabled: bool):
        ''' Sets the end-point marker's check-state to `enabled`, sets it to
            the current frame, validates it, and updates the UI accordingly. '''
        if not self.video:       return self.buttonTrimEnd.setChecked(False)
        if self.is_static_image: return self.buttonTrimEnd.setChecked(False)

        self.buttonTrimEnd.setChecked(enabled)
        self.sliderProgress.clamp_maximum = enabled

        if enabled:
            desired_maximum = get_ui_frame()
            if desired_maximum < self.minimum:
                set_and_update_progress(self.minimum, SetProgressContext.RESET_TO_MIN)
                self.maximum = self.minimum
                show_on_statusbar('You cannot set the end of your trim before the start of it.')
            else:
                self.maximum = desired_maximum

            h, m, s, ms = get_hms(self.current_time)                # use cleaner format for time-strings on videos > 1 hour
            if self.duration_rounded < 3600: self.buttonTrimEnd.setText(f'{m}:{s:02}.{ms:02}')
            else:                            self.buttonTrimEnd.setText(f'{h}:{m:02}:{s:02}')
        else:
            self.maximum = self.sliderProgress.maximum()
            self.buttonTrimEnd.setText('End' if self.is_trim_mode() else ' Fade from ')


    def set_trim_mode(self, action: QtW.QAction):
        ''' Updates UI/tooltips for `action`'s associated trim mode. '''
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


    def concatenate(self, action: QtW.QAction = None, files: list[str] = None):
        ''' Opens a separate dialog for concatenation with `files` included by
            default. Behavior changes depending on which `action` is passed:

            - `actionCatDialog`     - Open dialog immediately with `self.video`
                                      if present, otherwise an empty dialog.
                                      This is the default if `action` is None.
            - `actionCatBeforeThis` - Open file browser first, then the dialog if
                                      more than one additional file was provided.
                                      Cancel if file browser is cancelled. Files
                                      picked are inserted BEFORE `self.video`.
            - `actionCatAfterThis`  - Ditto, but files are appended AFTER.
            - `actionCatBeforeLast` - Open dialog immediately with `self.video`
                                      placed before `self.last_video`. If
                                      `self.last_video` doesn't exist, cancel.
            - `actionCatAfterLast`  - Ditto, but the order is reversed.

            Dialog (if opened) stays open indefinitely until user either
            successfully concatenates or deliberately closes the dialog.
            Output naming, save-prompts, and the "Save"/"Save as..." buttons
            follow the same conventions as normal saving.

            See `self._concatenate()` for the actual concatenation process. '''
        # TODO should this be unified with the other edit methods in some way and allow chaining?
        # https://stackoverflow.com/questions/7333232/how-to-concatenate-two-mp4-files-using-ffmpeg
        # https://stackoverflow.com/questions/31691943/ffmpeg-concat-produces-dts-out-of-order-errors
        try:
            if not constants.verify_ffmpeg(self, force_warning=True):
                return marquee('You don\'t have FFmpeg installed!')
            if not action:
                action = self.actionCatDialog

            # we probe our files before starting so we set these here instead of in `self._concatenate()`
            FRAME_RATE_HINT = 0.0
            FRAME_COUNT_HINT = 0

            # aliases for the main types of behavior the user can choose from/expect
            CAT_APPEND_THIS  = action in (self.actionCatBeforeThis, self.actionCatAfterThis)
            CAT_APPEND_LAST  = action in (self.actionCatBeforeLast, self.actionCatAfterLast)
            CAT_APPEND_AFTER = action in (self.actionCatAfterThis, self.actionCatAfterLast)
            CAT_DIALOG       = action in (self.actionCatDialog, self.actionCatLastDialog)
            CAT_BROWSE       = files is None and not CAT_DIALOG and not CAT_APPEND_LAST

            # what will we do to our output and original files after saving?
            open_after_save = cfg.concatenate.open
            explore_after_save = cfg.concatenate.explore
            encode_mode = cfg.concatenate.encode    # ↓ set dialog's delete setting to our own
            delete_mode = self.checkDeleteOriginal.checkState()

            # reuse last file list (action is disabled until at least one dialog was opened)
            if action is self.actionCatLastDialog:
                old_files = self.last_concat_files
                old_output = self.last_concat_output

            # see if we have a file list left over from a failed edit and ask if user wants to reuse it
            # NOTE: if the user opens the dialog directly, we can skip the confirmation popup
            else:
                old_output, old_files, old_settings = self.get_save_remnant('concatenate', ('', None, None))
                if old_files and (self.video in old_files or not self.video):
                    if not CAT_DIALOG and qthelpers.getPopupYesNo(
                        title='Reuse previous concatenation?',
                        text='A previous incomplete concatenation\ninvolving this file exists. Reuse?',
                        **self.get_popup_location_kwargs()
                    ).exec() != QtW.QMessageBox.Yes:
                        old_files = None
                        old_settings = None
                else:
                    old_files = None
                    old_settings = None
                if old_settings:
                    encode_mode, open_after_save, explore_after_save, delete_mode = old_settings

            # construct starting file list, if any
            if old_files:
                files = old_files
            else:
                # determine if our current file, our last file, or no file should be included by default
                # if we're adding to the current file but our current file isn't a video, just return
                if files and CAT_DIALOG:
                    base_video = ''
                else:
                    files = files or list()
                    if CAT_APPEND_LAST:             base_video = self.last_video
                    elif self.mime_type == 'video': base_video = self.video
                    elif CAT_APPEND_THIS: return show_on_statusbar('Concatenation is not implemented for audio and image files yet.', 10000)
                    else:                           base_video = ''

                # if we're adding our last file and current file together,...
                # ...add current file to `files` (which should be empty)
                if CAT_APPEND_LAST:
                    files.append(self.video)

                # see where in the file list to put our base video if we have one
                # if we expected it to be our last file but it's not there, warn user and return
                # if we expected it to be our current file, don't return. the user is more likely...
                # ...to be okay with this behavior for the current file rather than the last file
                if exists(base_video):
                    if CAT_APPEND_AFTER: files.insert(0, base_video)
                    else:                files.append(base_video)
                elif CAT_APPEND_LAST:
                    if self.last_video == '': return marquee('No other files have been played.')
                    else:                     return marquee('Last file no longer exists.')

                # browse for additional files before (possibly) showing dialog
                # if no files are selected and we were expecting some, just return
                if CAT_BROWSE:
                    new_files, cfg.lastdir = qthelpers.browseForFiles(
                        lastdir=cfg.lastdir,
                        caption='Select media files to concatenate together',
                        filter='All files (*)'
                    )
                    if len(new_files) == 0 and CAT_APPEND_THIS:
                        return
                    files += new_files
                files = [file.strip() for file in files if file]

        # >>> create, setup, and open dialog <<<
            # NOTE: originally if we only had 2 files and already knew their order, we'd skip the...
            # ...dialog and use preset settings, but I think it's better to always use the dialog
            from bin.window_cat import Ui_catDialog
            dialog = qthelpers.getDialogFromUiClass(
                Ui_catDialog,
                deleteOnClose=False,                # TODO: this really should be True especially since there's a...
                flags=Qt.WindowStaysOnTopHint,      # ...memory leak later but i just don't feel like handling it
                **self.get_popup_location_kwargs()
            )

            dialog.checkOpen.setChecked(open_after_save)
            dialog.checkExplore.setChecked(explore_after_save)
            dialog.buttonEncode.setChecked(encode_mode)
            dialog.buttonNoEncode.setChecked(not encode_mode)
            dialog.checkDelete.setCheckState(delete_mode)
            dialog.reverse.setIcon(self.icons['reverse_vertical'])
            dialog.recent.setIcon(self.icons['recent'])
            dialog.recent.setMenu(QtW.QMenu(dialog))
            dialog.videoList.add(files=files)

            # set dialog's output to our current output text unless we're putting the current...
            # ...video AFTER the last watched video AND we haven't touched our current output text
            if old_output:
                dialog.output.setText(old_output)
            else:
                current_output_text = self.lineOutput.text().strip()
                if CAT_APPEND_LAST and CAT_APPEND_AFTER and current_output_text == splitext_media(os.path.basename(self.video))[0]:
                    dialog.output.setText(splitext_media(os.path.basename(self.last_video))[0])
                else:
                    dialog.output.setText(current_output_text)

            # change "Save All" to say "Save as..."
            # we could just add our own buttons manually but it doesn't really make...
            # ...a difference (unless we remove the Save All button from the .ui file)
            for button in dialog.buttonBox.buttons():
                if button.text() == 'Save All':
                    button.setText('Save as...')

            # TODO ctrl adds recent files when menu isn't open. should it?
            def keyPressEvent(event: QtGui.QKeyEvent):
                ''' If 0-9 is pressed while the recent files menu is open,
                    add that number's file to the dialog (0 adds the least
                    recent file). If the menu isn't open, only add files
                    if Ctrl is also held down.'''
                key = event.key()
                mod = event.modifiers()
                if 48 <= key <= 57:                 # numbers 0-9
                    if dialog.recent.menu().isVisible() or mod & Qt.ControlModifier:
                        index = -(key - 48)
                        path = self.recent_files[max(index, -len(self.recent_files))]
                        dialog.videoList.add(files=(path,))

            def set_choice(button: QtW.QAbstractButton):
                ''' Sets `button` to a `choice` property on the dialog,
                    allowing us to know which save-button was clicked,
                    even after the dialog is closed. '''
                dialog.choice = button

            def refresh_cat_recent_menu():
                ''' Refreshes the dialog's own recent files menu. Clicking
                    a file adds it to the dialog rather than playing it. '''
                cat_recent_menu = dialog.recent.menu()
                cat_recent_menu.clear()
                get_add_lambda = lambda path: lambda: dialog.videoList.add(files=(path,))
                get_basename = os.path.basename     # ^ workaround for python bug/oddity involving creating lambdas in iterables
                for index, file in enumerate(reversed(self.recent_files)):
                    number = str(index + 1)         # ^ reversed to show most recent first
                    action = QtW.QAction(f'{number[:-1]}&{number[-1]}. {get_basename(file)}', cat_recent_menu)
                    action.triggered.connect(get_add_lambda(file))
                    action.setToolTip(file)
                    cat_recent_menu.addAction(action)

            def add_last_file():
                ''' Adds the actual most recently played file. If no files have
                    been played yet, the normal recent files list is used. '''
                if self.last_video:
                    dialog.videoList.add(files=(self.last_video,))
                elif self.recent_files:
                    dialog.videoList.add(files=self.recent_files[-1:])

            # connect dialog signals/events
            dialog.keyPressEvent = keyPressEvent
            dialog.buttonBox.clicked.connect(set_choice)
            dialog.add.clicked.connect(dialog.videoList.add)
            dialog.delete.clicked.connect(dialog.videoList.remove)
            dialog.up.clicked.connect(dialog.videoList.move)
            dialog.down.clicked.connect(lambda: dialog.videoList.move(down=True))
            dialog.reverse.clicked.connect(dialog.videoList.reverse)
            dialog.recent.clicked.connect(add_last_file)
            dialog.recent.contextMenuEvent = lambda event: dialog.recent.showMenu()
            dialog.recent.menu().aboutToShow.connect(refresh_cat_recent_menu)
            dialog.browse.clicked.connect(
                lambda: self.browse_for_save_file(
                    lineEdit=dialog.output,
                    noun='concatenated video',
                    valid_extensions=constants.VIDEO_EXTENSIONS,
                    ext_hint='.mp4',
                    default_path=dialog.output.text().strip(),
                    fallback_override=dialog.videoList.item(0).toolTip() if dialog.videoList.count() else None
                )
            )
            dialog.videoList.itemDoubleClicked.connect(
                lambda item: (
                    self.open(
                        item.toolTip(),
                        focus_window=False,
                        flash_window=False,
                        update_recent_list=item.toolTip() in self.recent_files,
                        update_raw_last_file=False
                    ),
                    dialog.videoList.refresh_thumbnail_outlines()
                )
            )

            # repeatedly open dialog until user succeeds or outright cancels
            while True:
                self.vlc.idle_timeout_time = 0.0            # lock cursor (`QVideoPlayer.leaveEvent` might not trigger)

                logging.info('Opening concatenation dialog...')
                if dialog.exec() == QtW.QDialog.Rejected:   # cancel selected on dialog -> return
                    return log_on_statusbar('Concatenation cancelled.')

                # check if any files have stopped existing - if so, show a warning and re-loop
                files = [abspath(item.toolTip()) for item in dialog.videoList]
                missing = [(i, f) for i, f in enumerate(files) if not exists(f)]
                if missing:
                    logging.info(f'(?) Files to be concatenated no longer exist, cancelling: {missing}')
                    if len(missing) == 1: header = 'The file at the following index no longer exists:\n\n'
                    else:                 header = 'The files at the following indexes no longer exist:\n\n'
                    footer = '\n'.join(f'{index + 1}. {file}' for index, file in missing)
                    qthelpers.getPopup(                     # TODO this is a rare scenario so it just shows...
                        title='Concatenation cancelled!',   # ...the popup and goes away, but it should...
                        text=header + footer,               # ...really give "discard" and "ignore" options
                        icon='warning',
                        **self.get_popup_location_kwargs()
                    ).exec()
                    continue

                elif len(files) < 2:
                    marquee('Not enough files to concatenate.', log=False)
                    continue

                else:
                    # calculate final duration and average FPS of `files` for progress bar
                    # (we do this here so we can catch invalid dimensions early)
                    if FFPROBE:
                        dimensions = []
                        invalid_dimensions_detected = False
                        fps_sum = 0
                        new_frame_total = 0

                        # attempt to probe files. if we're low on RAM, wait one second and try again
                        probes = probe_files(*files, retries=1)

                        # get dimensions, total frame count, and average FPS of all `files`
                        for file, probe_data in probes.items():
                            for stream in probe_data['streams']:
                                if stream['codec_type'] == 'video' and stream['avg_frame_rate'] != '0/0':
                                    new_dimensions = (str(int(stream['width'])), str(int(stream['height'])))
                                    dimensions.append((file, new_dimensions))
                                    if new_dimensions != dimensions[0][-1]:
                                        invalid_dimensions_detected = True
                                    fps_parts = stream['avg_frame_rate'].split('/')
                                    fps = int(fps_parts[0]) / int(fps_parts[1])
                                    duration = float(probe_data['format']['duration'])
                                    occurances = files.count(file)
                                    new_frame_total += (math.ceil(duration * fps) * occurances)
                                    fps_sum += fps * occurances
                        FRAME_RATE_HINT = fps_sum / len(probes)
                        FRAME_COUNT_HINT = new_frame_total

                        # not all files were probed correctly -> warn user and cancel if necessary
                        corrupt = [(i, f) for i, f in enumerate(files) if f not in probes]
                        if corrupt:
                            logging.info(f'(?) Files to be concatenated could not be probed, cancelling: {corrupt}')
                            if len(corrupt) == 1: header = 'The file at the following index could not be probed and may be corrupt:\n\n'
                            else:                 header = 'The files at the following indexes could not be probed and may be corrupt:\n\n'
                            footer = '\n'.join(f'{index + 1}. {file}' for index, file in corrupt)
                            qthelpers.getPopup(             # TODO: ditto for the "discard" and "ignore" options
                                title='Concatenation cancelled!',
                                text=header + footer,
                                icon='warning',
                                **self.get_popup_location_kwargs()
                            ).exec()
                            continue

                        # the videos have different dimensions -> warn user and cancel if necessary
                        if invalid_dimensions_detected:
                            footer = '\n'.join(f'{index}. {"x".join(wh)}: {os.path.basename(f)}' for index, (f, wh) in enumerate(dimensions, start=1))
                            if dialog.buttonEncode.isChecked():
                                header = ('All files must have the same dimensions for re-encoded concatenation.\n'
                                          'You\'ll need to crop or resize the offending files individually.')
                                qthelpers.getPopup(
                                    title='Concatenation cancelled!',
                                    text=header if len(files) > 20 else f'{header}\n\n{footer}',
                                    textDetailed=footer if len(files) > 20 else None,
                                    icon='warning',         # ↓ needed so it appears over the concat dialog
                                    **self.get_popup_location_kwargs()
                                ).exec()
                                continue
                            else:
                                header = ('Your files do not have the same dimensions. You can still concatenate\n'
                                          'them with stream-copying, but the output will be very broken if you\n'
                                          'don\'t crop or resize the offending files individually. Continue?')
                                if qthelpers.getPopupOkCancel(
                                    title='Concatenation cancelled!',
                                    text=header if len(files) > 20 else f'{header}\n\n{footer}',
                                    textDetailed=footer if len(files) > 20 else None,
                                    icon='warning',         # ↓ needed so it appears over the concat dialog
                                    **self.get_popup_location_kwargs()
                                ).exec() == QtW.QMessageBox.Cancel:
                                    continue

                # >>> prepare output from dialog <<<
                    output = dialog.output.text().strip()
                    unchanged = output == self.lineOutput.text().strip()
                    no_output = output == ''

                    # if output is provided and altered, sanitize and validate it...
                    # ...so the extra validation we're about to do actually works
                    if not unchanged and not no_output:     # append appropriate extension if needed
                        if not splitext_media(output, constants.VIDEO_EXTENSIONS)[-1]:
                            output = f'{output}{splitext_media(files[0], strict=False)[-1]}'
                        dirname, basename = os.path.split(output)
                        if not dirname:                     # no output directory specified
                            default_dir = settings.lineDefaultOutputPath.text().strip()
                            dirname = default_dir or os.path.dirname(files[0])
                        output = os.path.join(dirname, sanitize(basename))  # `sanitize` doesn't account for full paths

                    # if output already exists or was unchanged from our...
                    # ...normal output, show "Save as..." for confirmation
                    # if output is blank, show "Save as..." if desired, else auto-name it
                    already_exists = exists(output)
                    chose_save_as = dialog.choice.text() == 'Save as...'
                    if chose_save_as or unchanged or already_exists or (no_output and settings.checkSaveAsForceOnNoName.isChecked()):
                        unique_default = chose_save_as or (not already_exists and not unchanged)
                        default_path = output or files[0]
                        output = self.browse_for_save_file(
                            noun='concatenated video',
                            valid_extensions=constants.VIDEO_EXTENSIONS,
                            ext_hint='.mp4',
                            default_path=default_path,      # use first file's path as default if no ouput was provided
                            unique_default=unique_default   # if exists/unchanged, assume user wants to overwrite -> no unique default name
                        )
                        if not output:
                            continue
                    elif no_output:                         # no output -> default to first file's name + "_concatenated"
                        output = add_path_suffix(files[0], '_concatenated', unique=True)

                    # check for common reasons we might not be allowed to use our output or input
                    if not self.is_safe_to_edit(*files, dest=output):
                        continue
                    break                                   # we have our files, we have our name -> break loop

            # store output and file list for potential reuse later
            self.last_concat_files = files
            self.last_concat_output = dialog.output.text()
            self.actionCatLastDialog.setEnabled(True)       # enable "reuse last dialog" action now that we have one

            logging.info(f'Concatenating dialog files to {output}: {files}')
            operations = {
                'concatenate': {
                    'files': files,
                    'encode': dialog.buttonEncode.isChecked(),
                    'open': dialog.checkOpen.isChecked(),
                    'explore': dialog.checkExplore.isChecked(),
                    'delete_mode': dialog.checkDelete.checkState(),
                    'frame_rate_hint': FRAME_RATE_HINT,
                    'frame_count_hint': FRAME_COUNT_HINT
                },
                'remnants': {
                    'concatenate': (
                        dialog.output.text(),
                        files,
                        (
                            dialog.buttonEncode.isChecked(),
                            dialog.checkOpen.isChecked(),
                            dialog.checkExplore.isChecked(),
                            dialog.checkDelete.checkState()
                        )
                    )
                }
            }

        # >>> concatenate and cleanup <<<
            Thread(target=self._save, args=(output, operations), daemon=True).start()

        except:
            log_on_statusbar(f'(!) Concatenation preparation failed: {format_exc()}')

        finally:
            try:
                dialog.close()              # TODO: !!! memory leak?
                cfg.concatenate.open = dialog.checkOpen.isChecked()
                cfg.concatenate.explore = dialog.checkExplore.isChecked()
                cfg.concatenate.encode = dialog.buttonEncode.isChecked()
                dialog.videoList.clear()    # clearing list does not free up the memory it takes
                dialog.deleteLater()        # deleting the dialog does not free up the list's memory either (you cannot delete the list items either)
                del dialog
                gc.collect(generation=2)
            except:
                pass

            # reset cursor idle timeout
            self.vlc.idle_timeout_time = get_time() + settings.spinHideIdleCursorDuration.value()


    def resize_media(self):                 # https://ottverse.com/change-resolution-resize-scale-video-using-ffmpeg/ TODO this should probably have an advanced crf option
        ''' Resizes the dimensions of video files,
            and changes the length of audio files. '''
        if not self.video: return show_on_statusbar('No media is playing.', 10000)

        # reuse old width/height values for images and videos (NOT audio) if our last...
        # ...resize failed OR we're resizing something with the same dimensions as last time
        is_audio = self.mime_type == 'audio'
        base_size = (self.vwidth, self.vheight)
        if not is_audio and self.last_resize_media_base_size == base_size:
            old_size = self.get_save_remnant('resize', self.last_resize_media_values, self.video)
        else:
            old_size = self.get_save_remnant('resize', ('0', '0'), self.video)

        while True:
            width, height, _, raw_width, raw_height = self.show_size_dialog(*old_size, show_quality=False)
            if width is None: return        # dialog cancelled
            if width == 0: width = -1       # ffmpeg takes -1 as a default value, not 0
            if height == 0: height = -1     # ffmpeg takes -1 as a default value, not 0

            # cancel if size/duration is unchanged
            if is_audio:
                if round(width, 2) == 1:    # might get something like 1.0000331463797563
                    return show_on_statusbar('New length cannot be the same as the old length.', 10000)
                self.operations['resize'] = width
            elif (width <= 0 or width == self.vwidth) and (height <= 0 or height == self.vheight):
                return show_on_statusbar('New size cannot be the same as the old size.', 10000)
            else:
                self.operations['resize'] = (width, height)

            # save the width and height values to save remnants so we can restore them if needed
            old_size = (raw_width, raw_height)
            self.operations.setdefault('remnants', {})['resize'] = old_size

            if self.save(                   # doesn't really need any hints
                noun='resized media',
                filter='All files(*)',
                unique_default=True
            ):
                if not is_audio:
                    self.last_resize_media_values = old_size
                    self.last_resize_media_base_size = base_size
                break


    def rotate_video(self, action: QtW.QAction):
        if not self.video:            return show_on_statusbar('No video is playing.', 10000)
        if self.mime_type == 'audio': return show_on_statusbar('Well that would just be silly, wouldn\'t it?', 10000)

        rotation_presets = {
            self.actionRotate90:         'transpose=clock',
            self.actionRotate180:        'transpose=clock,transpose=clock',
            self.actionRotate270:        'transpose=cclock',
            self.actionFlipVertically:   'vflip',
            self.actionFlipHorizontally: 'hflip'
        }
        self.operations['rotate video'] = rotation_presets[action]
        self.save(                          # doesn't really need any hints
            noun='rotated video/image',
            filter='All files(*)',
            unique_default=True
        )


    # TODO: doing this on an audio file is somewhat unstable
    # TODO: add option to toggle "shortest" setting?
    def add_audio(self, *, path: str = None, save: bool = True, caption: str = None) -> bool:
        if not self.video: return show_on_statusbar('No media is playing.', 10000)

        try:
            if not path:
                path, cfg.lastdir = qthelpers.browseForFile(
                    lastdir=cfg.lastdir,
                    caption=caption or 'Select audio file to add'
                )
                if not path:                # cancel selected
                    return False

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
            if save:                        # amplify_audio may call this, so saving is optional
                self.save(
                    noun='media with additional audio track',
                    filter=filter,
                    ext_hint='.mp4',
                    valid_extensions=valid_extensions,
                    unique_default=True
                )
            return True
        except:
            log_on_statusbar(f'(!) ADD_AUDIO FAILED: {format_exc()}')
            return False


    # https://stackoverflow.com/questions/81627/how-can-i-hide-delete-the-help-button-on-the-title-bar-of-a-qt-dialog
    def amplify_audio(self):
        if not self.video: return show_on_statusbar('No media is playing.', 10000)

        if self.mime_type == 'image' or (self.mime_type == 'video' and player.get_audio_track_count() == 0):
            show_on_statusbar('Add audio first, then you can amplify it.')
            if not self.add_audio(save=False, caption='Add audio first, then you can amplify it.'):
                return                      # add audio failed/was cancelled
            filter = 'MP4 files (*.mp4);;All files (*)'
            valid_extensions = constants.VIDEO_EXTENSIONS
            preferred_extensions = None
        elif self.mime_type == 'audio':
            filter = 'MP3 files (*.mp3);;WAV files (*.wav);;AAC files (*.aac);;All files (*)'
            valid_extensions = constants.VIDEO_EXTENSIONS + constants.AUDIO_EXTENSIONS
            preferred_extensions = constants.AUDIO_EXTENSIONS
        else:
            filter = 'MP4 files (*.mp4);;MP3 files (*.mp3);;WAV files (*.wav);;AAC files (*.aac);;All files (*)'
            valid_extensions = constants.VIDEO_EXTENSIONS + constants.AUDIO_EXTENSIONS
            preferred_extensions = None

        try:
            dialog = qthelpers.getDialog(
                title='Amplify Audio',
                deleteOnClose=False,        # TODO this MIGHT cause a memory leak
                fixedSize=(125, 105),
                flags=Qt.Tool,
                **self.get_popup_location_kwargs()
            )

            layout = QtW.QVBoxLayout(dialog)
            label = QtW.QLabel('Input desired volume \n(applies on save):', dialog)
            spin = QtW.QSpinBox(dialog)
            spin.setSuffix('%')
            spin.setMaximum(1000)
            spin.setValue(self.get_save_remnant('amplify audio', self.last_amplify_audio_value, self.video))
            for w in (label, spin):
                layout.addWidget(w)
            dialog.addButtons(layout, QtW.QDialogButtonBox.Cancel, QtW.QDialogButtonBox.Ok)

            # repeatedly open dialog until user succeeds or outright cancels (slightly less flair than the concat version)
            while dialog.exec() != QtW.QDialog.Rejected:
                self.last_amplify_audio_value = spin.value()                     # save value to re-display it next time
                self.operations['amplify audio'] = round(spin.value() / 100, 2)  # convert volume to 0-1 range
                self.operations.setdefault('remnants', {})['amplify audio'] = spin.value()
                if self.save(
                    noun='amplified video/audio',
                    filter=filter,
                    valid_extensions=valid_extensions,
                    preferred_extensions=preferred_extensions,
                    unique_default=True
                ):
                    break
        except:
            log_on_statusbar(f'(!) Audio amplification failed: {format_exc()}')
        finally:
            try:
                dialog.close()
                dialog.deleteLater()
                del dialog
                gc.collect(generation=2)
            except:
                pass


    def replace_audio(self, *, path: str = None):
        if not self.video:            return show_on_statusbar('No media is playing.', 10000)
        if self.mime_type == 'audio': return show_on_statusbar('Well that would just be silly, wouldn\'t it?', 10000)
        if self.mime_type == 'image': return self.add_audio(path=path)

        try:
            if not path:
                path, cfg.lastdir = qthelpers.browseForFile(
                    lastdir=cfg.lastdir,
                    caption='Select audio file to replace audio track with'
                )
                if not path:                                                # cancel selected
                    return
            self.operations['replace audio'] = path
            self.save(
                noun='video with replaced audio track',
                filter='MP4 files (*.mp4);;All files (*)',
                ext_hint='.mp4',
                valid_extensions=constants.VIDEO_EXTENSIONS,
                unique_default=True
            )
        except:
            log_on_statusbar(f'(!) REPLACE_AUDIO FAILED: {format_exc()}')


    # https://superuser.com/questions/268985/remove-audio-from-video-file-with-ffmpeg
    def isolate_track(self, *, audio: bool = True):
        if not self.video:            return show_on_statusbar('No media is playing.', 10000)
        if self.mime_type == 'image': return show_on_statusbar('Well that would just be silly, wouldn\'t it?', 10000)

        track_count = player.get_audio_track_count()
        if self.mime_type == 'audio':
            if track_count == 1: return show_on_statusbar('Well that would just be silly, wouldn\'t it?', 10000)
            else:                return show_on_statusbar('Track removal for audio files is not supported yet.', 10000)
        elif track_count == 0:
            if audio: return show_on_statusbar('There are no audio tracks. If you want to remove the video too, you might as well just close your eyes.', 10000)
            else:     return show_on_statusbar('There are no audio tracks left to remove.', 10000)

        if audio:
            current_track = player.get_audio_track()
            if current_track == -1:
                return show_on_statusbar('No audio track is currently selected.', 10000)
            self.operations['isolate track'] = ('Audio', max(0, current_track - 1))
            filter = 'MP4 files (*.mp4);;MP3 files (*.mp3);;WAV files (*.wav);;AAC files (*.aac);;All files (*)'
            valid_extensions = constants.VIDEO_EXTENSIONS + constants.AUDIO_EXTENSIONS
            preferred_extensions = constants.AUDIO_EXTENSIONS
        else:
            self.operations['isolate track'] = ('Video', 0)
            filter = 'MP4 files (*.mp4);;All files (*)'
            valid_extensions = constants.VIDEO_EXTENSIONS
            preferred_extensions = None

        self.save(
            noun=f'{self.operations["isolate track"][0]}',
            filter=filter,
            ext_hint='.mp3' if audio else None,                             # give hint for extension
            valid_extensions=valid_extensions,
            preferred_extensions=preferred_extensions,                      # tells a potential "save as" prompt which extensions should be default
            unique_default=True
        )


    def add_text(self):
        ''' Opens a dialog for adding text to the current media.
            Actual docstring coming in a different commit. '''
        if not constants.IS_WINDOWS:
            return qthelpers.getPopup(
                title='Adding text is Windows-only',
                text=('Adding text is Windows-only (for now). Qt doesn\'t expose font paths, and figuring out how to '
                      'get them on Windows was convoluted enough as it is.\n\nThat\'s it. That\'s the entire reason.')
            ).exec()

        if not self.video:            return show_on_statusbar('No media is playing.', 10000)
        if self.mime_type == 'audio': return show_on_statusbar('Well that would just be silly, wouldn\'t it?', 10000)
        if self.mime_type == 'image': return show_on_statusbar('Adding text to static images is not supported yet.', 10000)

        # pause video/GIF to avoid immediately generating several previews
        self.force_pause(True)

        last_preview_frame = -1
        preview_image_path = f'{constants.THUMBNAIL_DIR}{sep}textoverlaypreview.jpg'
        try: os.remove(preview_image_path)
        except: pass

        try:
            from bin.window_text import Ui_textDialog
            dialog = qthelpers.getDialogFromUiClass(
                Ui_textDialog,
                #modal=True,
                #deleteOnClose=True,
                flags=Qt.WindowStaysOnTopHint,
                **self.get_popup_location_kwargs()
            )

            dialog.buttonColorFont.setStyleSheet('QPushButton {background-color: rgba(255,255,255,255); border: 1px solid black;}')
            dialog.buttonColorBox.setStyleSheet('QPushButton {background-color: rgba(255,255,255,0); border: 1px solid black;}')
            dialog.buttonColorShadow.setStyleSheet('QPushButton {background-color: rgba(0,0,0,150); border: 1px solid black;}')
            overlay = widgets.QTextOverlay(dialog)

            vw = self.vwidth
            vh = self.vheight
            if vw > vh: dialog.preview.setFixedSize(*scale(vw, vh, new_x=800))
            else:       dialog.preview.setFixedSize(*scale(vw, vh, new_y=800))

            dialog.preview.ratio = dialog.preview.width() / vw
            dialog.preview.overlays.append(overlay)
            dialog.preview.selected = overlay
            dialog.preview.selected.pos = QtCore.QPointF(vw / 2, vh / 2)

            def update_selected(attribute: str, value):
                setattr(dialog.preview.selected, attribute, value)
                dialog.preview.update()

            def update_alignment(button: QtW.QPushButton):
                dialog.preview.selected.alignment = {
                    dialog.buttonAlignLeft: Qt.AlignLeft,
                    dialog.buttonAlignCenter: Qt.AlignHCenter,
                    dialog.buttonAlignRight: Qt.AlignRight
                }[button]
                dialog.preview.update()

            dialog.text.textChanged.connect(lambda: update_selected('text', dialog.text.toPlainText().strip('\n')))
            dialog.comboFont.currentFontChanged.connect(lambda font: update_selected('font', font))
            dialog.spinFontSize.valueChanged.connect(lambda size: update_selected('size', size))
            dialog.spinBoxWidth.valueChanged.connect(lambda size: update_selected('bgwidth', size))
            dialog.spinShadowX.valueChanged.connect(lambda x: update_selected('shadowx', x))
            dialog.spinShadowY.valueChanged.connect(lambda y: update_selected('shadowy', y))
            dialog.buttonColorFont.clicked.connect(lambda: update_selected('color', self.show_color_picker(button=dialog.buttonColorFont, alpha=True)))
            dialog.buttonColorBox.clicked.connect(lambda: update_selected('bgcolor', self.show_color_picker(button=dialog.buttonColorBox, alpha=True)))
            dialog.buttonColorShadow.clicked.connect(lambda: update_selected('shadowcolor', self.show_color_picker(button=dialog.buttonColorShadow, alpha=True)))
            dialog.buttonGroup.buttonClicked.connect(update_alignment)
            #dialog.adjustSize()            # TODO why is it not shrinking correctly
            #dialog.resize(0, 0)

            def update_preview():
                try:
                    nonlocal last_preview_frame
                    if not exists(constants.THUMBNAIL_DIR):
                        os.makedirs(constants.THUMBNAIL_DIR)
                    frame = get_ui_frame()
                    if frame != last_preview_frame:
                        ffmpeg(f'-ss {frame / self.frame_rate} -i "{self.video}" -vframes 1 "{preview_image_path}"')
                        try: dialog.preview.setPixmap(QtGui.QPixmap(preview_image_path, 'JPEG'))
                        except: return
                        last_preview_frame = frame
                except:
                    logging.warning(f'(!) "Add text" dialog failed to update preview image: {format_exc()}')

            preview_timer = QtCore.QTimer()
            preview_timer.timeout.connect(update_preview)
            preview_timer.timeout.emit()
            preview_timer.start(1000)

            if dialog.exec() == QtW.QDialog.Accepted:
                marker_modes = {
                    dialog.buttonMarkerIgnore: 'ignore',
                    dialog.buttonMarkerStart:  'start',
                    dialog.buttonMarkerBoth:   'both',
                    dialog.buttonMarkerEnd:    'end'
                }
                self.operations['add text'] = {
                    'markers': marker_modes[dialog.buttonGroup_2.checkedButton()],
                    'overlays': dialog.preview.overlays
                }
                self.save(
                    noun='media with overlaid text',
                    filter='All files(*)',
                    unique_default=True
                )

            preview_timer.stop()

        except:
            log_on_statusbar(f'(!) Add-text dialog failed: {format_exc()}')


    # ---------------------
    # >>> PROMPTS <<<
    # ---------------------
    def browse_for_directory(
        self,
        *,
        lineEdit: QtW.QLineEdit = None,
        noun: str = None,
        default_path: str = None
    ) -> str | None:
        caption = f'Select {noun} directory' if noun else 'Select directory'
        path, cfg.lastdir = qthelpers.browseForDirectory(
            lastdir=cfg.lastdir,
            caption=caption,
            directory=default_path,
            lineEdit=lineEdit
        )
        return path


    def browse_for_save_file(
        self,
        *,
        lineEdit: QtW.QLineEdit = None,
        noun: str = None,
        filter: str = 'All files (*)',
        valid_extensions: tuple[str] = constants.ALL_MEDIA_EXTENSIONS,
        ext_hint: str = None,
        default_path: str = None,
        unique_default: bool = True,
        fallback_override: str = None
    ) -> str | None:
        ''' Opens a file-browsing dialog and returns a path to save to. Assigns
            path to `lineEdit` if provided. Dialog caption will read, "Save
            `noun` as..." if provided, otherwise "Save as...". If `default_path`
            if provided, it will be validated and used as the starting folder
            and filename for the dialog. If not provided or invalid, it will
            fallback to:

            1. `fallback_override` if provided (if THAT'S invalid, fallback
            to `cfg.lastdir`)
            2. `self.video` if valid and `settings.checkSaveAsUseMediaFolder`
            is checked
            3. `cfg.lastdir`

            `default_path` may be a relative path. After the above validation,
            if `default_path` included path separators but its directory did
            not exist, it will evaluated relative to the new validated path.
            Example:

            1. Provided `default_path`: "music/test.mp3"
            2. Fallback directory: "C:/Users/Name"
            3. Validated `default_path`: "C:/Users/Name/test.mp3"
            4. Potential relative `default_path`: "C:/Users/Name/Music/test.mp3"

            If `default_path` starts with '.' or '..', the validated directory
            will be tried first, then the script/executable's directory second.
            If `default_path` lacks an extension within `valid_extensions`,
            `ext_hint` will be appended to `default_path`, if provided. If
            `unique_default` is True, `default_path` will start as unique (for
            when you expect the user doesn't want to overwrite anything). '''

        if default_path:
            if os.path.isdir(default_path): dirname, basename = default_path, None
            else:                           dirname, basename = os.path.split(default_path)
        else:
            dirname = ''
            basename = None

        # validate `default_path`. use fallback if needed (see docstring)
        if not default_path or not exists(dirname):
            if fallback_override:
                fallback_override = abspath(fallback_override)
                if exists(fallback_override):
                    fallback = fallback_override
                    if os.path.isdir(fallback_override):
                        fallback += sep         # `fallback_override` exists and is a directory
                else:   fallback = cfg.lastdir  # `fallback_override` does not exist
            else:       fallback = self.video   # `fallback_override` was not provided

            if fallback:
                if settings.checkSaveAsUseMediaFolder.isChecked(): default_path = fallback
                else: default_path = os.path.join(cfg.lastdir, os.path.basename(fallback))
            else:
                default_path = cfg.lastdir

            # evaluate possible relative paths (see docstring)
            if dirname:
                potential_dir = default_path if os.path.isdir(default_path) else os.path.dirname(default_path)
                potential_path = os.path.join(potential_dir, dirname)
                if exists(potential_path):
                    default_path = os.path.join(potential_path, basename)

        if os.path.isdir(default_path):
            dirname = default_path              # simply reuse basename if it was already set
        else:
            if unique_default:
                default_path = get_unique_path(default_path)
            dirname, basename = os.path.split(default_path)

        # verify the extension on the filename we're about to use
        if basename:
            base, ext = splitext_media(basename, valid_extensions)
            if ext_hint and not ext:
                basename = base + ext_hint

        path, cfg.lastdir = qthelpers.saveFile(
            lastdir=cfg.lastdir,
            directory=dirname,
            name=basename,
            caption=f'Save {noun} as...' if noun else 'Save as...',
            filter=filter,
            selectedFilter='All files (*)',     # NOTE: this simply does nothing if this filter isn't available
            lineEdit=lineEdit
        )

        return path                             # could be None if cancel was selected


    def browse_for_subtitle_files(self, *, urls: tuple[QtCore.QUrl] = None) -> None:
        if self.mime_type == 'image': return show_on_statusbar('Well that would just be silly, wouldn\'t it?', 10000)
        if urls is None:
            urls, cfg.lastdir = qthelpers.browseForFiles(
                lastdir=cfg.lastdir,
                caption='Select subtitle file(s) to add',
                filter='Subtitle Files (*.cdg *.idx *.srt *.sub *.utf *.ass *.ssa *.aqt *.jss *.psb *.it *.sami *smi *.txt *.smil *.stl *.usf *.dks *.pjs *.mpl2 *.mks *.vtt *.tt *.ttml *.dfxp *.scc);;All files (*)',
                url=True
            )
        self.add_subtitle_files(urls)


    def show_size_dialog(
        self,
        width: str = '',
        height: str = '',
        quality: int = -1,
        show_quality: bool = False,
    ) -> tuple[int, int, int, str, str] | tuple[int, int, None, str, str] | tuple[float, None, None, str, str]:
        ''' Opens a dialog for choosing a new size/length for the current file.
            Returns the width, height, quality, as well as the raw width and
            height strings entered into the dialog, for a total of 5 values.
            If the dialog was cancelled, the first value (the width) will be
            None. For audio, "width" will be the duration as a factor of the
            original (e.g. 1.5x). If `show_quality` is True, additional options
            for image quality are provided. Otherwise, the quality will be None.

            `width`, `height`, and `quality` parameters can be provided
            to define their respective default values within the dialog. '''
        vwidth, vheight, duration = self.vwidth, self.vheight, self.duration
        max_time_string = self.labelMaxTime.text()
        logging.debug(f'Showing size dialog with defaults: w={width} h={height} q={quality} (show={show_quality})')

        dimension_mode = show_quality or self.mime_type != 'audio'
        dialog = qthelpers.getDialog(
            title='Input desired ' + ('size' if dimension_mode else 'duration'),
            fixedSize=(0, 0),
            flags=Qt.Tool,
            **self.get_popup_location_kwargs()
        )

        # user-friendly properties for the various fields before and after conversion
        dialog.width = None
        dialog.height = None
        dialog.quality = None
        dialog.raw_width = width
        dialog.raw_height = height

        # setup dialog for images/videos
        if dimension_mode:
            label = QtW.QLabel(constants.SIZE_DIALOG_DIMENSIONS_LABEL_BASE.replace('?resolution', f'{vwidth}x{vheight}'), dialog)
            wline = QtW.QLineEdit(str(width) or '0', dialog)
            hline = QtW.QLineEdit(str(height) or '0', dialog)
            wbutton = QtW.QPushButton('Width:', dialog)
            wbutton.clicked.connect(lambda: wline.setText(str(int(vwidth))))
            wbutton.setToolTip(f'Reset width to native resolution ({vwidth:.0f} pixels).')
            wbutton.setMaximumWidth(50)
            hbutton = QtW.QPushButton('Height:', dialog)
            hbutton.clicked.connect(lambda: hline.setText(str(int(vheight))))
            hbutton.setToolTip(f'Reset height to native resolution ({vheight:.0f} pixels).')
            hbutton.setMaximumWidth(50)

            if show_quality:                    # add JPEG quality label/spinbox
                qlabel = QtW.QLabel('Quality:', dialog)
                qlabel.setMinimumWidth(50)
                qlabel.setAlignment(Qt.AlignCenter)
                qlabel.setToolTip('JPEG quality (0-100). Higher is better. Does not apply if saved as PNG format.')
                qspin = QtW.QSpinBox(dialog)
                qspin.setValue(quality if quality != -1 else settings.spinSnapshotJpegQuality.value())
                qspin.setMaximum(100)

            for lineEdit in (wline, hline):
                lineEdit.setMaxLength(6)        # ↓ https://stackoverflow.com/questions/13422995/set-qlineedit-to-accept-only-numbers
                lineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('\\d*%')))

        # setup dialog for audio
        else:
            label = QtW.QLabel('Enter a timestamp (hh:mm:ss.ms)\nor a percentage. Note: This is\ncurrently limited to 50-200%\nof the original audio\'s length.', dialog)
            wline = QtW.QLineEdit(str(width) or max_time_string, dialog)
            wbutton = QtW.QPushButton('Duration:', dialog)
            wbutton.clicked.connect(lambda: wline.setText(max_time_string))
            wbutton.setToolTip(f'Reset to native duration ({max_time_string}).')
            wbutton.setMaximumWidth(58)

        label.setAlignment(Qt.AlignCenter)
        wline.selectAll()                       # start with width lineEdit's text already selected, for quicker editing

        layout = QtW.QVBoxLayout(dialog)
        form = QtW.QFormLayout()
        form.addRow(label)
        form.addRow(wbutton, wline)
        if dimension_mode: form.addRow(hbutton, hline)
        if show_quality:   form.addRow(qlabel, qspin)
        layout.addLayout(form)
        dialog.addButtons(layout, QtW.QDialogButtonBox.Cancel, QtW.QDialogButtonBox.Ok)

        def accept():
            # video/image resize. accepts raw values or percentages. blank fields default to 0, which then align to aspect ratio
            if dimension_mode:                                  # if sizes are percents, strip '%' and multiply w/h by percentages
                width = dialog.raw_width = wline.text().strip()
                height = dialog.raw_height = hline.text().strip()
                if '%' in width:  width = round(vwidth * (float(width.strip('%').strip()) / 100))
                else:             width = int(width) if width else 0
                if '%' in height: height = round(vheight * (float(height.strip('%').strip()) / 100))
                else:             height = int(height) if height else 0
                dialog.width = width
                dialog.height = height
                dialog.quality = qspin.value() if show_quality else None

            # audio resize (adjusting tempo) NOTE: final duration is a multiplier of the original (e.g. 1.5x)
            # TODO: ffmpeg's atempo is limited to 0.5x-2.0x duration. this is fixable with math. i suck at math.
            else:                                               # ↓ audio doesn't use `hline` lineEdit
                duration_factor = dialog.raw_width = wline.text().strip()
                if '%' in duration_factor:                      # convert percentage to multiplier
                    duration_factor = 1 / (float(duration_factor.strip('%').strip()) / 100)

                # calculate duration (as seconds) from timestamp string (hh:mm:ss.ms)
                else:
                    new_duration = 0                            # ↓ float() takes care of milliseconds at the end
                    parts = tuple(float(part) for part in duration_factor.split(':') if part)
                    if len(parts) == 3:   new_duration += (parts[0] * 3600) + (parts[1] * 60) + parts[2]
                    elif len(parts) == 2: new_duration += (parts[0] * 60) + parts[1]
                    elif len(parts) == 1: new_duration = parts[0]
                    duration_factor = duration / new_duration

                # clamp between 0.5x and 2.0x (see TODO above)
                duration_factor = min(2, max(0.5, duration_factor))
                dialog.width = duration_factor

        # open resize dialog. if cancel is selected, return None's
        dialog.accepted.connect(accept)
        dialog.exec()
        return dialog.width, dialog.height, dialog.quality, dialog.raw_width, dialog.raw_height


    def show_about_dialog(self):                                # lazy version of about dialog
        from bin.window_about import Ui_aboutDialog
        dialog = qthelpers.getDialogFromUiClass(
            Ui_aboutDialog,
            modal=True,
            deleteOnClose=True,
            **self.get_popup_location_kwargs()
        )

        dialog.labelLogo.setPixmap(QtGui.QPixmap(f'{constants.RESOURCE_DIR}{sep}logo_filled.png'))
        dialog.labelVersion.setText(dialog.labelVersion.text().replace('?version', constants.VERSION))

        settings_were_open = settings.isVisible()               # hide the always-on-top settings while we show popups
        if settings_were_open: settings.hide()
        dialog.adjustSize()                                     # adjust size to match version string/OS fonts
        dialog.exec()                                           # don't bother setting a fixed size or using open()
        if settings_were_open: settings.show()                  # restore settings if they were originally open

        del dialog
        gc.collect(generation=2)


    def show_timestamp_dialog(self, *, file: str = None):       # * to capture unused signal args
        from bin.window_timestamp import Ui_timestampDialog
        dialog = qthelpers.getDialogFromUiClass(
            Ui_timestampDialog,
            modal=False,
            deleteOnClose=True,
            **self.get_popup_location_kwargs()
        )

        class Timestamp:
            __slots__ = 'original_time', 'dateTime', 'dateTimeEdit'

            def __init__(self, letter: str, stat: os.stat_result):
                self.original_time = int(getattr(stat, f'st_{letter}time'))
                self.dateTime = QtCore.QDateTime()
                self.dateTime.setSecsSinceEpoch(self.original_time)
                self.dateTimeEdit = getattr(dialog, f'date{letter.upper()}time')
                self.dateTimeEdit.setDateTime(self.dateTime)

            def reset(self, seconds: int = 0):
                self.dateTime.setSecsSinceEpoch(seconds or self.original_time)
                self.dateTimeEdit.setDateTime(self.dateTime)

        def open_file(file: str):
            ''' Reads `file`'s timestamps and updates the UI accordingly. '''
            try:
                dialog.file = file
                dialog.buttonPath.setText(os.path.basename(file))
                dialog.buttonPath.setToolTip(file)
                stat = os.stat(file)
                timestamps['c'] = Timestamp('c', stat)
                timestamps['m'] = Timestamp('m', stat)
                timestamps['a'] = Timestamp('a', stat)
            except:
                log_on_statusbar(f'(!) Failed to add file: {format_exc()}')

        def sync_file(file: str):
            sync_stat = os.stat(file)
            if dialog.checkCtime.isChecked(): timestamps['c'].reset(sync_stat.st_ctime)
            if dialog.checkMtime.isChecked(): timestamps['m'].reset(sync_stat.st_mtime)
            if dialog.checkAtime.isChecked(): timestamps['a'].reset(sync_stat.st_atime)

        def browse_for_file() -> str:
            ''' Browses for a file/folder to open.
                Returns opened file if successful. ''' 
            new_file, cfg.lastdir = qthelpers.browseForFile(
                lastdir=cfg.lastdir,
                caption='Select file to set timestamps for'
            )
            if new_file:
                open_file(new_file)
            return new_file

        def refresh_sync_button():
            ''' Disables `dialog.buttonSync` if no timestamps are checked. '''
            dialog.buttonSync.setEnabled(
                dialog.checkCtime.isChecked()
                or dialog.checkMtime.isChecked()
                or dialog.checkAtime.isChecked()
            )

        def get_timestamp_string(seconds: int) -> str:
            ''' Returns `seconds` as a timestamp formatted
                according to `dialog.lineFormat.text()`. '''
            date = QtCore.QDateTime()
            date.setSecsSinceEpoch(seconds)
            return date.toString(dialog.lineFormat.text())

        def swap(a: QtW.QDateTimeEdit, b: QtW.QDateTimeEdit):
            ''' From Qt's documentation:
                `QDateTime::swap(QDateTime &other) - Swaps this datetime
                with other. This operation is very fast and never fails.`

                It fails. '''
            a_date = a.dateTime()   # (only because of the bad way QDateTimeEdit holds its...
            b_date = b.dateTime()   # ...QDateTime property; QDateTime.swap() actually works fine)
            a.setDateTime(b_date)
            b.setDateTime(a_date)

        def on_menu(letter: str):
            ''' Generates a menu for the given `letter`time, i.e. "c" for ctime,
                "m" for ctime, etc. Menu re-reads current file's stats to
                provide the "current time" for a file. '''
            try:
                timestamp = timestamps[letter]
                current_time = int(getattr(os.stat(dialog.file), f'st_{letter}time'))

                action_swap_ctime = QtW.QAction('Swap with creation time')
                action_swap_ctime.triggered.connect(lambda: swap(timestamp.dateTimeEdit, dialog.dateCtime))
                action_swap_mtime = QtW.QAction('Swap with modified time')
                action_swap_mtime.triggered.connect(lambda: swap(timestamp.dateTimeEdit, dialog.dateMtime))
                action_swap_atime = QtW.QAction('Swap with accessed time')
                action_swap_atime.triggered.connect(lambda: swap(timestamp.dateTimeEdit, dialog.dateAtime))
                if letter == 'c':   swap_actions = (action_swap_mtime, action_swap_atime)
                elif letter == 'm': swap_actions = (action_swap_ctime, action_swap_atime)
                else:               swap_actions = (action_swap_ctime, action_swap_mtime)

                action_reset_original = QtW.QAction(f'Reset to original: {get_timestamp_string(timestamp.original_time)}')
                action_reset_original.triggered.connect(lambda: timestamp.reset())
                action_reset_current = QtW.QAction(f'Reset to current: {get_timestamp_string(current_time)}')
                action_reset_current.triggered.connect(lambda: timestamp.reset(seconds=current_time))

                context = QtW.QMenu(self)
                context.addActions(swap_actions)
                context.addSeparator()
                context.addAction(action_reset_original)
                context.addAction(action_reset_current)
                context.exec(QtGui.QCursor.pos())
            except:
                log_on_statusbar(f'(!) Failed to generate menu for {letter}time: {format_exc()}')

        def on_click(button: QtW.QPushButton):
            ''' Handles `dialog.buttonBox` clicks
                based on which `button` was pressed. '''
            cfg.timestampdialogformat = dialog.lineFormat.text()
            role = dialog.buttonBox.buttonRole(button)
            if role == QtW.QDialogButtonBox.ResetRole:
                timestamps['c'].reset()
                timestamps['m'].reset()
                timestamps['a'].reset()

            elif role in (QtW.QDialogButtonBox.AcceptRole, QtW.QDialogButtonBox.ApplyRole):
                ctime = mtime = atime = 0
                if dialog.checkCtime.isChecked(): ctime = dialog.dateCtime.dateTime().toSecsSinceEpoch()
                if dialog.checkMtime.isChecked(): mtime = dialog.dateMtime.dateTime().toSecsSinceEpoch()
                if dialog.checkAtime.isChecked(): atime = dialog.dateAtime.dateTime().toSecsSinceEpoch()
                self.set_file_timestamps(
                    path=dialog.file,
                    ctime=ctime,
                    mtime=mtime,
                    atime=atime
                )

        def on_sync():
            ''' Browses for new file to sync timestamps with.
                Only timestamps that are enabled will be synced. '''
            try:
                new_file, cfg.lastdir = qthelpers.browseForFile(
                    lastdir=cfg.lastdir,
                    caption='Select file to take timestamps from'
                )
                if new_file:
                    sync_file()
            except:
                log_on_statusbar(f'(!) Failed to sync timestamps: {format_exc()}')

        def on_update_format(format: str):
            ''' Updates all timestamps to use `format`. Uses
                fallback if `format` is now an empty string. '''
            if not format: format = 'MM/dd/yy - hh:mm:ss AP'
            dialog.dateCtime.setDisplayFormat(format)
            dialog.dateMtime.setDisplayFormat(format)
            dialog.dateAtime.setDisplayFormat(format)

        def dialogDragEnterEvent(event: QtGui.QDragEnterEvent):
            ''' Accepts a cursor-drag if files are being dragged.
                Requires `dialog.setAcceptDrops(True)`. '''
            if event.mimeData().hasUrls(): event.accept()
            else: event.ignore()

        def dialogDragMoveEvent(event: QtGui.QDragMoveEvent):
            ''' Accepts a cursor-drag if files are being dragged. Requires
                `dialog.setAcceptDrops(True)`. Animates the sync button to
                appear pressed when hovering over it, to convey that it can
                be dropped over to sync the file rather than open it. '''
            dialog.buttonSync.setDown(dialog.buttonSync.geometry().contains(event.pos()))

        def dialogDragLeaveEvent(event: QtGui.QDragLeaveEvent):
            ''' Ensure the sync button no longer appears pressed
                after dragging off of the window, just in case. '''
            dialog.buttonSync.setDown(False)

        def dialogDropEvent(event: QtGui.QDropEvent):
            ''' Opens the first dropped file/folder, or syncs its timestamps
                to the current file if dropped over the sync button. '''
            files = [url.toLocalFile() for url in event.mimeData().urls()]
            over_sync = dialog.buttonSync.geometry().contains(event.pos())
            if over_sync and dialog.buttonSync.isEnabled(): sync_file(files[0])
            else: open_file(files[0])
            dialog.buttonSync.setDown(False)

        # setup dialog and create timestamps dictionary
        timestamps = {}
        dialog.lineFormat.setText(cfg.loadFrom('general', 'timestampdialogformat', dialog.lineFormat.text()))
        dialog.setWindowFlags(Qt.WindowStaysOnTopHint)

        # connect events/signals
        dialog.dragEnterEvent = dialogDragEnterEvent
        dialog.dragMoveEvent = dialogDragMoveEvent
        dialog.dragLeaveEvent = dialogDragLeaveEvent
        dialog.dropEvent = dialogDropEvent
        dialog.buttonPath.clicked.connect(browse_for_file)
        dialog.checkCtime.clicked.connect(refresh_sync_button)
        dialog.checkMtime.clicked.connect(refresh_sync_button)
        dialog.checkAtime.clicked.connect(refresh_sync_button)
        dialog.toolCtime.clicked.connect(lambda: on_menu('c'))
        dialog.toolMtime.clicked.connect(lambda: on_menu('m'))
        dialog.toolAtime.clicked.connect(lambda: on_menu('a'))
        dialog.lineFormat.textChanged.connect(on_update_format)
        dialog.buttonSync.clicked.connect(on_sync)
        dialog.buttonBox.clicked.connect(on_click)

        # open `file` if provided. default to `self.video` if possible, otherwise open browsing dialog
        if file is None:
            if self.video:
                file = self.video
                open_file(file)
            else:
                file = browse_for_file()
                if not file:
                    return show_on_statusbar('No media is playing.', 10000)

        # open dialog then do cleanup after it's closed
        dialog.exec()
        del dialog
        gc.collect(generation=2)


    def show_trim_dialog(self):
        ''' Opens dialog for selecting which trim mode to default to. Only
            meant to appear for new users that haven't adjusted their trim
            settings yet. Sets cfg.trimmodeselected to True. '''
        try:
            self.force_pause(True)
            dialog = qthelpers.getDialog(
                title='Choose default trim mode',
                modal=True,
                deleteOnClose=True,
                flags=Qt.Tool,
                **self.get_popup_location_kwargs()
            )
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

            dialog.accepted.connect(accept)
            if not constants.IS_WINDOWS:
                dialog.adjustSize()

            if dialog.exec() == QtW.QDialog.Accepted:           # trim mode selected -> set appropriate QAction
                if dialog.choice == button_auto: self.actionTrimAuto.setChecked(True)
                else: self.actionTrimPrecise.setChecked(True)
            else:                                               # trim mode rejected -> set flag so whatever opened...
                self.trim_mode_selection_cancelled = True       # ...the dialog can cancel whatever work it was doing

        except: log_on_statusbar(f'(!) TRIM DIALOG ERROR: {format_exc()}')
        finally: cfg.trimmodeselected = True                    # set this to True no matter what (_save is waiting on this)


    def show_delete_prompt(self, *, exiting: bool = False) -> QtW.QDialogButtonBox.StandardButton:
        ''' Generates a dialog for deleting marked files. Dialog consists of
            a `QScrollArea` containing a `QCheckBox` for each file (each with
            their own context menu and middle-click event), with Yes/No/Cancel
            and "Select/Deselect All" buttons at the bottom. Returns the button
            chosen, or None if there was an error. If `exiting` is True, the
            dialog will not mention what happens if "No" is selected. '''

        # ensure there are actually existing files to delete
        marked_for_deletion = [f for f in self.marked_for_deletion if exists(f)]
        if not marked_for_deletion: return log_on_statusbar('No media is marked for deletion.')

        marked: list[str] = []
        unmarked: list[str] = []
        marked_count = len(marked_for_deletion)
        recycle: bool = settings.checkRecycleBin.isChecked()
        dialog_width = 450

        try:
            logging.info('Opening deletion prompt...')
            dialog = qthelpers.getDialog(
                title='Confirm Deletion',
                icon='SP_DialogDiscardButton',
                flags=Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint,
                **self.get_popup_location_kwargs()
            )

            # workarounds for python bug/oddity involving creating lambdas in iterables
            get_open_lambda =    lambda file: lambda: self.open(file, focus_window=False, update_recent_list=False)
            get_explore_lambda = lambda file: lambda: self.explore(file)

            # checkbox events
            def contextMenuEvent(event: QtGui.QContextMenuEvent):
                ''' Show "Play" and "Explore" actions for the context
                    menu of the checkbox currently under the mouse. '''
                for checkbox in qthelpers.layoutGetItems(scroll_area_layout):
                    if checkbox.underMouse():
                        checkbox.setStyleSheet('border: 1px solid blue; padding: 2px; background: rgba(20, 196, 255, 50)')
                        file = checkbox.text()          # ^ force stylesheet to use hover-style since it won't always update between right-clicks
                        break
                else:                                   # else in a for-loop means we didn't break
                    return
                context = QtW.QMenu(self)
                context.addAction('Play', get_open_lambda(file))
                context.addAction('Explore', get_explore_lambda(file))
                context.addSeparator()
                context.addAction(os.path.basename(file)).setEnabled(False)
                context.exec(event.globalPos())
                checkbox.setStyleSheet('')              # reset stylesheet to normal

            def mousePressEvent(event: QtGui.QMouseEvent):
                ''' Open the underlying path for the
                    checkbox currently under the mouse. '''
                if event.button() == Qt.MiddleButton:
                    for checkbox in qthelpers.layoutGetItems(scroll_area_layout):
                        if checkbox.underMouse():
                            get_open_lambda(checkbox.text())()
                            return

            def finished(result):
                ''' Populate the `marked` and `unmarked` lists
                    with each checked and unchecked checkbox. '''
                for checkbox in qthelpers.layoutGetItems(scroll_area_layout):
                    (marked if checkbox.isChecked() else unmarked).append(checkbox.text())

            def select_all(checked: bool):
                ''' Set all checkboxes to `checked`. '''
                for checkbox in qthelpers.layoutGetItems(scroll_area_layout):
                    checkbox.setChecked(checked)

            def checkbox_toggled(checked: bool):
                ''' Increments `marked_count` and
                    updates the header accordingly. '''
                nonlocal marked_count
                marked_count += 1 if checked else -1
                header.setText(get_header_text())

            def get_header_text() -> str:
                ''' Calculates and returns the proper header text. '''
                warning_verb = 'recycled' if recycle else 'permanently deleted'
                if len(marked_for_deletion) == 1:
                    warning_noun = 'file'
                elif marked_count != len(marked_for_deletion):
                    warning_noun = f'{marked_count}/{len(marked_for_deletion)} files'
                else:
                    warning_noun = f'{len(marked_for_deletion)} files'
                warning_text = f'The following {warning_noun} will be {warning_verb}. Continue?'
                return f'{warning_text}\n(Middle-click to play, right-click for more options)'

            # layout and header label
            header = QtW.QLabel(get_header_text(), dialog)
            header.setAlignment(Qt.AlignHCenter)
            layout = QtW.QVBoxLayout(dialog)
            layout.addWidget(header)

            # create scroll area (needlessly complicated - needs its own layout and sub-widget)
            scroll_area = QtW.QScrollArea(dialog)
            scroll_area_widget = QtW.QWidget(scroll_area)
            scroll_area.setWidget(scroll_area_widget)
            scroll_area.setWidgetResizable(True)
            scroll_area_layout = QtW.QVBoxLayout(scroll_area_widget)
            scroll_area_layout.setSpacing(0)
            scroll_area_layout.setContentsMargins(4, 4, 4, 4)
            layout.addWidget(scroll_area)

            # give scroll area a white background and checkboxes a cool blue highlight when hovering
            scroll_area.setStyleSheet(
                'QWidget {background: white}'
                'QScrollBar {background: none}'         # https://stackoverflow.com/a/62223180
                'QCheckBox {padding: 3px}'
                'QCheckBox::hover {border: 1px solid blue; padding-left: 2px; background: rgba(20, 196, 255, 50)}'
            )

            # add checkboxes for each file (key=splitext to ignore extensions when sorting)
            # TODO add setting related to sorting the files
            for file in sorted(marked_for_deletion, key=os.path.splitext):
                checkbox = QtW.QCheckBox(file, scroll_area_widget)
                checkbox.setToolTip(file)
                checkbox.setChecked(True)               # ↓ https://stackoverflow.com/a/7872508
                checkbox.toggled.connect(checkbox_toggled)
                dialog_width = max(dialog_width, checkbox.fontMetrics().width(file) + 58)
                scroll_area_layout.addWidget(checkbox)  # ^ track required width for each checkbox so we can resize later

            # add expanding vertical spacer to bottom of scroll area so checkboxes stay at the top
            scroll_area_layout.addSpacerItem(QtW.QSpacerItem(0, 10, QtW.QSizePolicy.Minimum, QtW.QSizePolicy.Expanding))

            # footer label
            if not exiting:
                label = QtW.QLabel('Clicking "No" will remove unchecked files from your deletion list.')
                label.setAlignment(Qt.AlignCenter)
                layout.addWidget(label)

            # create button box and add "select/deselect all" buttons to left side with spacer inbetween
            buttons = dialog.addButtons(None, QtW.QDialogButtonBox.Cancel, QtW.QDialogButtonBox.No, QtW.QDialogButtonBox.Yes)
            button_layout = QtW.QHBoxLayout()
            button_select_all = QtW.QPushButton('Select all')
            button_select_all.clicked.connect(lambda: select_all(True))
            button_deselect_all = QtW.QPushButton('Deselect all')
            button_deselect_all.clicked.connect(lambda: select_all(False))
            button_layout.addWidget(button_select_all)
            button_layout.addWidget(button_deselect_all)
            button_layout.addSpacerItem(QtW.QSpacerItem(0, 10, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum))
            button_layout.addWidget(buttons)
            layout.addLayout(button_layout)

            # connect final events/signals
            scroll_area_widget.contextMenuEvent = contextMenuEvent
            scroll_area_widget.mousePressEvent = mousePressEvent
            dialog.finished.connect(finished)

            # resize dialog based on longest path in checkboxes (trying to avoid BOTH scrollbars)
            dialog.setMinimumHeight(150)
            if len(marked_for_deletion) <= 2:
                height = 150
            else:
                dialog.adjustSize()
                height = dialog.height()

            if dialog_width > 700:
                dialog.resize(700, height + 7)
            else:
                dialog.resize(dialog_width, height - 10)

            # delete checked files or unmark unchecked files depending on dialog choice
            dialog.exec()
            if dialog.choice == QtW.QDialogButtonBox.Yes:
                self.delete(*marked)
            elif dialog.choice == QtW.QDialogButtonBox.No:
                self.mark_for_deletion(*unmarked, mark=False)

            logging.info(f'Deletion dialog choice: {dialog.choice}')
            return dialog.choice
        except:
            log_on_statusbar(f'(!) DELETION PROMPT FAILED: {format_exc()}')


    def show_search_popup(
        self,
        items: list[str],
        widget: QtW.QWidget,
        item_labels: list[str] = None,
        max_visible: int = 9,
        selected_index: int = 0,
        on_select=None
    ):
        ''' Displays an interactive popup below `widget` populated by `items`.
            If `item_labels` is provided, it will be used to populate the
            combobox instead of `items` (Example usage: providing a generator
            of custom names to avoid duplicating/editing a very large `items`).

            Combobox will truncate `items` to roughly 1000 elements (with some
            leniency - i.e. 1100 is okay, but 1500 becomes exactly 1000).

            Combobox shows `max_visible` items at a time and starts off with
            `selected_index` selected. `on_select` should be a slot that takes
            a `QComboBox` and `str` as parameters. '''

        combo = QtW.QComboBox(widget)
        combo.setModel(QtCore.QStringListModel())

        # limit max results if necessary and display count on statusbar
        max_count = 1000                            # too many results = tons of RAM + long population time
        max_threshold_count = max_count * 1.25      # allow some leniency, i.e. 1100 is okay, but 1500 becomes 1000
        if len(items) > max_threshold_count:
            show_on_statusbar(f'Results truncated from {len(items)} to {max_count}')
            items = items[:max_count]
        else:
            show_on_statusbar(f'Showing {len(items)} result{"s" if len(items) != 1 else ""}')
        app.processEvents()

        def showPopup():
            qthelpers.setCursor(Qt.ArrowCursor)     # force cursor to arrow to hide VLC's loading icon bug
            QtW.QComboBox.showPopup(combo)
            self.vlc.idle_timeout_time = 0.0        # lock cursor so it doesn't enter bugged state while popup is open

            # HACK: change context of any shortcuts that use Up, Down, or Enter so that the UI doesn't...
            # ...eat those inputs. otherwise, you can't use the keyboard to navigate the combobox if it...
            # ...has a parent (we NEED a parent because the combobox is VERY broken without one (blame Qt))
            ignored_keys = (                        # major advantage over other workarounds: you can control...
                QtGui.QKeySequence(Qt.Key_Up),      # ...the dropdown AND use other shortcuts at the same time
                QtGui.QKeySequence(Qt.Key_Down),
                QtGui.QKeySequence(Qt.Key_Enter)
            )
            for primary, secondary in self.shortcuts.values():
                if primary.key() in ignored_keys or secondary.key() in ignored_keys:
                    primary.setContext(0)
                    secondary.setContext(0)

        def hidePopup():
            _combo = combo
            expected_count = getattr(combo, 'reopen_count', 0) + 1
            QtW.QComboBox.hidePopup(_combo)         # hide popup, then start a self-destruct timer
            QtCore.QTimer.singleShot(10000, lambda: cleanup(_combo, expected_count))

            # reuse `QMenu.hideEvent()` hack to hide cursor consistently (NOTE: the dropdown...
            # ...eats all mouse events while open, so this will NOT cause cursor flickers)
            self.vlc.reset_undermouse_state()

            # HACK: reverses the shortcut context hack (see above)
            ignored_keys = (
                QtGui.QKeySequence(Qt.Key_Up),
                QtGui.QKeySequence(Qt.Key_Down),
                QtGui.QKeySequence(Qt.Key_Enter)
            )
            for primary, secondary in self.shortcuts.values():
                if primary.key() in ignored_keys or secondary.key() in ignored_keys:
                    primary.setContext(3)
                    secondary.setContext(3)

        # delete the combobox if it hasn't been opened `expected_count` times...
        # ...after a delay. this ensures it gets deleted if we don't actually...
        # ...select anything (the `textActivated` signal fires AFTER `.hidePopup()`)
        def cleanup(combo: QtW.QComboBox, expected_count: int):
            if getattr(combo, 'reopen_count', 0) < expected_count:
                combo.deleteLater()
                gc.collect(generation=2)

        combo.showPopup = showPopup
        combo.hidePopup = hidePopup
        combo.textActivated.connect(lambda: setattr(combo, 'reopen_count', getattr(combo, 'reopen_count', 0) + 1))
        if on_select:
            combo.textActivated.connect(lambda text: on_select(combo, text))

        # add basenames of every file to combobox
        combo.addItems(item_labels or items)

        # force combobox to align with textbox and stretch to width of widest entry
        # NOTE: why don't setMinimumContentsLength and setSizeAdjustPolicy work?
        combo.setFixedHeight(self.lineOutput.height())
        combo.view().setMinimumWidth(combo.minimumSizeHint().width())
        combo.setMaxVisibleItems(max_visible)       # ^ https://stackoverflow.com/a/54005207

        # open dropdown, selecting/scrolling to preferred position if needed
        combo.setCurrentIndex(selected_index)       # must set index BEFORE open, then scroll view AFTER open
        combo.showPopup()

        # `PositionAtCenter` is broken near the start, so only scroll if we're close...
        # ...to our visible limit (1 item away from the bottom/top of visible area)
        # NOTE: we do the reverse for items at the bottom by scrolling all the way down
        if selected_index > combo.maxVisibleItems() - 2:
            near_center = selected_index < (combo.count() - combo.maxVisibleItems() + 1)
            hint = QtW.QAbstractItemView.PositionAtCenter if near_center else QtW.QAbstractItemView.PositionAtTop
            combo.view().scrollTo(combo.model().createIndex(selected_index, 0), hint)


    # -------------------------------
    # >>> UTILITY FUNCTIONS <<<
    # -------------------------------
    def _log_on_statusbar_slot(self, msg: str, timeout: int = 20000):
        ''' Logs a `msg` while simultaneously displaying it
            on the statusbar for `timeout` milliseconds. '''
        logging.info(msg)
        show_on_statusbar(msg, timeout)


    def marquee(self, text: str, marq_key: str = '', timeout: int = 350, log: bool = True):
        ''' Conditionally displays `text` as a marquee over the player if
            the associated setting at `marq_key` is checked. Always displayed
            on statusbar. Logs as well if `log` is True. Escaped %-signs (%%)
            are replaced by regular %-signs when displayed on the statusbar.
            If `marq_key` is not provided, `text` will be shown on the player
            and statusbar no matter what.

            Example: marq_key="Save" -> `checkTextOnSave.isChecked()`? '''

        if log: log_on_statusbar(text.replace('%%', '%'))
        else: show_on_statusbar(text.replace('%%', '%'), 10000)

        try:
            if not marq_key or settings.__dict__[f'checkTextOn{marq_key}'].isChecked():
                show_on_player(text, timeout)
        except:
            pass


    def handle_updates(self, _launch: bool = False):
        ''' Handles update-checking/validation as well as updating the settings
            dialog. Updates validation only occurs on launch, and only if
            "update_report.txt" is present. Update checks only occur on
            launch if it has been `spinUpdateFrequency.value()` days since
            the last check. The last check date is only saved down to the
            day so that launch-checks are more predictable. '''
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
            try: last_check_time_seconds = mktime(strptime(cfg.lastupdatecheck, '%x'))
            except: last_check_time_seconds = 0         # ^ string into seconds needs %x
            if not _launch or last_check_time_seconds + (86400 * settings.spinUpdateFrequency.value()) < get_time():
                if not just_updated:
                    log_on_statusbar('Checking for updates...')
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
        ''' A slot for `update.check_for_update` which cleans up and handles
            the `results` of an update check, if any, in a thread-safe manner.

            `results` contains one of two keys:
            1. 'failed' - An error occurred. There may still be a pending update
            (URL might have had a mismatched format on GitHub, for example).
            2. 'latest_version_url' - The URL to download the update from.

            `popup_kwargs` are a dict of keyword-arguments needed to construct
            the relevant `QMessageBox` for the user, depending on `results`. '''
        try:
            logging.info(f'Cleaning up after update check. results={results}')
            settings_were_open = settings.isVisible()   # hide the always-on-top settings while we show popups
            if settings_were_open:
                settings.hide()

            if results:     # display relevant popups. if `results` is empty, skip the popups and only do cleanup
                if 'failed' in results:
                    return qthelpers.getPopup(**popup_kwargs, **self.get_popup_location_kwargs()).exec()

                # did not fail, and update is available. on windows -> auto-updater popup (TODO: cross-platform autoupdating)
                if constants.IS_COMPILED and constants.IS_WINDOWS:
                    choice = qthelpers.getPopup(**popup_kwargs, **self.get_popup_location_kwargs()).exec()
                    if choice == QtW.QMessageBox.Yes:
                        import update
                        name = constants.VERSION.split()[0]
                        latest_version_url = results['latest_version_url']
                        latest_version = latest_version_url.split('/')[-1].lstrip('v')

                        filename = f'{name}_{latest_version}.zip'
                        download_url = f'{latest_version_url.replace("/tag/", "/download/")}/{filename}'
                        download_path = f'{constants.TEMP_DIR}{sep}{filename}'
                        update.download_update(self, latest_version, download_url, download_path)
                else:                                   # non-windows version of popup
                    return qthelpers.getPopup(**popup_kwargs, **self.get_popup_location_kwargs()).exec()
        finally:
            self.checking_for_updates = False
            settings.buttonCheckForUpdates.setText('Check for updates')
            if settings_were_open:                      # restore settings if they were originally open
                settings.show()


    def add_info_actions(self, context: QtW.QMenu):
        ''' Appends greyed-out actions to `context` containing
            information about the current media. '''
        context.addSeparator()
        is_fullscreen = self.isFullScreen()             # always show all info in fullscreen
        if is_fullscreen or '?size' not in settings.lineWindowTitleFormat.text():
            context.addAction(f'Size: {self.size_label}').setEnabled(False)
        if is_fullscreen or '?resolution' not in settings.lineWindowTitleFormat.text():
            context.addAction(f'Res: {self.vwidth:.0f}x{self.vheight:.0f}').setEnabled(False)
        if is_fullscreen or '?ratio' not in settings.lineWindowTitleFormat.text():
            context.addAction(f'Ratio: {self.ratio}').setEnabled(False)

        # generate timestamps for media's ctime/mtime
        # enable tooltips for the menu if long format is present (or error occurred)
        short_format = settings.lineDateFormatShort.text().strip()
        long_format = settings.lineDateFormatLong.text().strip()
        if short_format:                                # don't do anything if short format is empty
            if constants.IS_WINDOWS:
                short_format = short_format.replace('%-', '%#')
                long_format = long_format.replace('%-', '%#')
            else:
                short_format = short_format.replace('%#', '%-')
                long_format = long_format.replace('%#', '%-')
            try:
                ctime_struct = localtime(self.stat.st_ctime)
                mtime_struct = localtime(self.stat.st_mtime)
                short_timestamp = strftime(short_format, ctime_struct)
                if long_format:
                    long_ctimestamp = strftime(long_format, ctime_struct)
                    long_mtimestamp = strftime(long_format, mtime_struct)
                    tooltip = (f'Date created:\t{long_ctimestamp}\n'
                               f'Date modified:\t{long_mtimestamp}')
                else:
                    tooltip = ''
            except ValueError:
                short_timestamp = 'Invalid date format!'
                tooltip = ('Change the two date formats in your settings.\n'
                           'See https://strftime.org/ for valid format codes, or\n'
                           'use https://www.strfti.me/ for an interactive sandbox.')
            action = context.addAction(short_timestamp)
            action.setEnabled(False)
            if tooltip:
                action.setToolTip(tooltip)
                context.setToolTipsVisible(True)


    # TODO: we have like THREE variations of this exact method for handling vague input,...
    #       ...all of which do *almost* the same thing. this should all be ONE method
    def get_output(
        self,
        text: str = None,
        valid_extensions: tuple[str] = constants.ALL_MEDIA_EXTENSIONS,
        ext_hint: str = None,
        unique: bool = False
    ) -> tuple[str]:
        ''' Returns `new_name` or `self.lineOutput.text()` as a `unique`, valid,
            sanitized, absolute path, along with its extensionless basename and
            extension (as determined by `valid_extensions`, with `ext_hint`
            being the preferred fallback if provided). If `new_name` ends
            up the same as `self.video`, `new_name`/`self.lineOutput` are both
            blank, or no media is playing, then three None's are returned. '''
        output = text or self.lineOutput.text().strip()
        video = self.video
        if not video or not output:                     # no media playing or no text provided/accessible
            return None, None, None

        video_base, video_ext = splitext_media(video)
        video_tail_base = os.path.split(video_base)[-1]
        if output == video_tail_base:                   # output is completely unchanged
            return None, None, None

        try:
            old_oscwd = os.getcwd()
            os.chdir(os.path.dirname(video))            # set os module's CWD to self.video's folder -> allows things like abspath, '.', and '..'

            # get absolute path, sanitize basename, then check for a valid extension
            dirname, basename = os.path.split(abspath(output))
            basename = sanitize(basename)
            output = abspath(os.path.join(dirname, basename))
            basename_no_ext, ext = splitext_media(basename, valid_extensions)

            # append valid extension if needed
            if not ext:
                ext = ext_hint or video_ext or ('.' + self.extension)
                output += ext

            # make sure new name didn't end up being the same as the old one anyway
            if output == video:
                return None, None, None

            # make output unique if it's not unchanged and update `basename_no_ext` if needed
            if unique:                                  # TODO make the usage of `get_unique_path` a setting
                unique_output = get_unique_path(output)
                if output != unique_output:
                    output = unique_output
                    basename_no_ext, _ = os.path.splitext(os.path.basename(output))

            return output, basename_no_ext, ext

        except:
            log_on_statusbar(f'(!) Could not get valid string from output textbox: {format_exc()}')
            return None, None, None
        finally:
            os.chdir(old_oscwd)                         # reset os module's CWD before returning


    def get_save_remnant(
        self,
        key: str,
        default=None,
        video: str = '',
        active: bool = True,
        inactive: bool = True,
        return_state: bool = False
    ):
        ''' Convenience method for accessing the most recent data within
            `self.save_remnants` for a given `key` on a given `video` (if
            provided). `active` and `inactive` control whether or not remnants
            for edits still in progress ("active") or not ("inactive") may be
            returned. If not present, `default` is returned. If `return_state`
            is True, the remnant's active/inactive state is be returned as a
            second value (always False for `default`). '''
        try:
            remnant_times = sorted(self.save_remnants.keys(), reverse=True)
            for remnant_time in remnant_times:
                try:
                    remnant = self.save_remnants[remnant_time]
                    if key in remnant and remnant.get('video', video) == video:
                        _active = remnant.get('_in_progress', False)
                        if (_active and active) or (not _active and inactive):
                            return (remnant[key], _active) if return_state else remnant[key]
                except:
                    log_on_statusbar(f'(!) Error accessing save remnant at {remnant_time}: {format_exc()}')
        except:
            log_on_statusbar(f'(!) Unexpected error while getting save remnant for key "{key}": {format_exc()}')
        return (default, False) if return_state else default


    def get_popup_location_kwargs(self) -> dict[str, str, str]:
        ''' Returns the center-parameters of popups/dialogs as a dictionary. '''
        index = settings.comboDialogPosition.currentIndex()
        if index:
            widget = None
        elif not constants.APP_RUNNING:                 # index is 0 but geometry isn't set yet, use cfg to get center of window
            x, y = cfg.pos
            w, h = cfg.size
            x += w / 2
            y += h / 2
            widget = (x, y)
        else:                                           # use player's container widget if it's big enough
            widget = self.vlc if self.vlc.height() >= 20 else self.frameGeometry()
        return {'centerWidget': widget, 'centerScreen': index == 1, 'centerMouse': index == 2}


    def get_hotkey_full_string(self, hotkey: str) -> str:
        ''' Returns a string in the format " (key1/key2)" for the given `hotkey`
            group, where key1 and key2 are the two `QKeySequenceFlexibleEdit`'s.
            Example: "mute" would return one of the following:
            1. `" ({settings.mute.toString()}/{settings.mute_.toString()})"`
            2. `" ({settings.mute.toString()}"`
            3. `" ({settings.mute_.toString()}"`
            4. `""` '''
        hotkey1 = getattr(settings, hotkey).toString()
        hotkey2 = getattr(settings, hotkey + '_').toString()
        if hotkey1 and hotkey2: hotkey_string = f' ({hotkey1}/{hotkey2})'
        elif hotkey1:           hotkey_string = f' ({hotkey1})'
        elif hotkey2:           hotkey_string = f' ({hotkey2})'
        else:                   hotkey_string = ''
        return hotkey_string


    def get_new_file_timestamps(self, *sources: str, dest: str) -> tuple[float, float]:
        ''' Returns a tuple of floats containing the new creation time and
            modified time to use when saving `sources` to `dest`, based on
            the various settings the user has checked/unchecked. If more than
            one file is provided for `sources`, concatenation settings are
            used to determine which times constitute the "original file."
            NOTE: Times that should not be changed will be returned as 0. '''

        # one source -> we can avoid the nightmare below
        if len(sources) == 1:
            stat = os.stat(sources[0])
            old_ctime = stat.st_ctime
            old_mtime = stat.st_mtime

        # multiple sources -> use concat settings to figure out what times to use
        else:
            def get_extremes() -> tuple[tuple[str, os.stat_result, float]]:
                ''' Returns a tuple of tuples. The outer tuple consists of the
                    four extremes - oldest/newest ctime/mtime. Each inner tuple
                    contains the source file, its stat result, and the actual
                    ctime or mtime value (only used for faster comparisons). '''
                all_stats = ((s, os.stat(s)) for s in sources)
                oldest_ctime = (sources[0], None, 99999999999)
                oldest_mtime = (sources[0], None, 99999999999)
                newest_ctime = (sources[0], None, 0)    # ^ NOTE: increase this number in a couple thousand years
                newest_mtime = (sources[0], None, 0)
                for source, stat in all_stats:
                    ctime = stat.st_ctime
                    mtime = stat.st_mtime
                    if ctime < oldest_ctime[-1]: oldest_ctime = (source, stat, ctime)
                    if ctime > newest_ctime[-1]: newest_ctime = (source, stat, ctime)
                    if mtime < oldest_mtime[-1]: oldest_mtime = (source, stat, mtime)
                    if mtime > newest_mtime[-1]: newest_mtime = (source, stat, mtime)
                return oldest_ctime, oldest_mtime, newest_ctime, newest_mtime

            # if `self.video` is preferred and is present in `sources`, use that
            if settings.checkEditCatPreferCurrentMedia.isChecked() and self.video in sources:
                old_ctime = self.stat.st_ctime
                old_mtime = self.stat.st_mtime

            # take both times from the same file
            elif settings.groupEditCatBoth.isChecked():
                if settings.radioEditCatBothFirst.isChecked():
                    first = os.stat(sources[0])
                    old_ctime = first.st_ctime
                    old_mtime = first.st_mtime
                elif settings.radioEditCatBothLast.isChecked():
                    last = os.stat(sources[-1])
                    old_ctime = last.st_ctime
                    old_mtime = last.st_mtime
                else:
                    oldest_ctime, oldest_mtime, newest_ctime, newest_mtime = get_extremes()
                    if settings.radioEditCatBothOldestCtime.isChecked():
                        old_ctime = oldest_ctime[1].st_ctime
                        old_mtime = oldest_ctime[1].st_mtime
                    elif settings.radioEditCatBothOldestMtime.isChecked():
                        old_ctime = oldest_mtime[1].st_ctime
                        old_mtime = oldest_mtime[1].st_mtime
                    elif settings.radioEditCatBothOldest.isChecked():
                        if oldest_ctime[-1] < oldest_mtime[-1]:
                            old_ctime = oldest_ctime[1].st_ctime
                            old_mtime = oldest_ctime[1].st_mtime
                        else:
                            old_ctime = oldest_mtime[1].st_ctime
                            old_mtime = oldest_mtime[1].st_mtime
                    elif settings.radioEditCatBothNewestCtime.isChecked():
                        old_ctime = newest_ctime[1].st_ctime
                        old_mtime = newest_ctime[1].st_mtime
                    elif settings.radioEditCatBothNewestMtime.isChecked():
                        old_ctime = newest_mtime[1].st_ctime
                        old_mtime = newest_mtime[1].st_mtime
                    elif settings.radioEditCatBothNewest.isChecked():
                        if newest_ctime[-1] > newest_mtime[-1]:
                            old_ctime = newest_ctime[1].st_ctime
                            old_mtime = newest_ctime[1].st_mtime
                        else:
                            old_ctime = newest_mtime[1].st_ctime
                            old_mtime = newest_mtime[1].st_mtime

            # take each time separately (but still possibly from the same file)
            else:
                first = os.stat(sources[0])
                last = os.stat(sources[-1])
                old_ctime = 0
                old_mtime = 0
                if settings.radioEditCatCtimeFirst.isChecked():
                    old_ctime = first.st_ctime
                elif settings.radioEditCatCtimeLast.isChecked():
                    old_ctime = last.st_ctime
                if settings.radioEditCatMtimeFirst.isChecked():
                    old_mtime = first.st_mtime
                elif settings.radioEditCatMtimeLast.isChecked():
                    old_mtime = last.st_mtime

                if old_ctime == 0 or old_mtime == 0:
                    oldest_ctime, oldest_mtime, newest_ctime, newest_mtime = get_extremes()
                    if settings.radioEditCatCtimeOldest.isChecked():
                        old_ctime = oldest_ctime[1].st_ctime
                    elif settings.radioEditCatCtimeNewest.isChecked():
                        old_ctime = newest_ctime[1].st_ctime
                    if settings.radioEditCatMtimeOldest.isChecked():
                        old_mtime = oldest_mtime[1].st_mtime
                    elif settings.radioEditCatMtimeNewest.isChecked():
                        old_mtime = newest_mtime[1].st_mtime

        # check if mtime and ctime should be swapped (mtime must be at least one minute older than ctime)
        mtime_is_older = old_mtime < (old_ctime - 60)
        if mtime_is_older and settings.checkEditOlderMtimeUseAsCtime.isChecked():
            old_ctime = old_mtime

        # the ctime/mtime we'll be returning
        new_ctime = 0
        new_mtime = 0

        # evaluate which ctime/mtime to return
        if dest in sources:                             # dest is replacing one of the sources
            if settings.checkEditCtimeOnOriginal.isChecked():           new_ctime = old_ctime
            if settings.checkEditMtimeOnOriginal.isChecked():           new_mtime = old_mtime
            if mtime_is_older:
                if settings.checkEditOlderMtimeAlwaysReuse.isChecked(): new_mtime = old_mtime
        elif not exists(dest):                          # dest is a new file
            if settings.checkEditCtimeOnNew.isChecked():                new_ctime = old_ctime
            if settings.checkEditMtimeOnNew.isChecked():                new_mtime = old_mtime
            if mtime_is_older:
                if settings.checkEditOlderMtimeAlwaysReuse.isChecked(): new_mtime = old_mtime
        else:                                           # dest is replacing a different file
            other_stat = os.stat(dest)
            other_ctime = other_stat.st_ctime
            other_mtime = other_stat.st_mtime
            if settings.radioEditCtimeConflictUseOriginal.isChecked():  new_ctime = old_ctime
            elif settings.radioEditCtimeConflictUseOther.isChecked():   new_ctime = other_ctime
            elif settings.radioEditCtimeConflictUseNewest.isChecked():  new_ctime = max(old_ctime, other_ctime)
            elif settings.radioEditCtimeConflictUseOldest.isChecked():  new_ctime = min(old_ctime, other_ctime)
            if settings.radioEditMtimeConflictUseOriginal.isChecked():  new_mtime = old_mtime
            elif settings.radioEditMtimeConflictUseOther.isChecked():   new_mtime = other_mtime
            elif settings.radioEditMtimeConflictUseNewest.isChecked():  new_mtime = max(old_mtime, other_mtime)
            elif settings.radioEditMtimeConflictUseOldest.isChecked():  new_mtime = min(old_mtime, other_mtime)

        return new_ctime, new_mtime


    def set_file_timestamps(self, path: str, ctime: float = 0, mtime: float = 0, atime: float = 0):
        ''' Sets a `path`'s creation time and modified time to `ctime`, `mtime`,
            and `atime`, if non-zero. NOTE: "ctime" represents "changed time" on
            non-Windows systems, so `ctime` is ignored outside of Windows. '''
        if ctime and constants.IS_WINDOWS:              # ctime means something else on other systems
            try: setctime(path=path, ctime=ctime)
            except: log_on_statusbar(f'(!) Failed to update creation time for file: {format_exc()}')
        if mtime or atime:                              # os.utime takes (atime, mtime)
            stat = os.stat(path)
            if mtime == 0: mtime = stat.st_mtime
            if atime == 0: atime = stat.st_atime
            try: os.utime(path=path, times=(atime, mtime))
            except: log_on_statusbar(f'(!) Failed to update modified time for file: {format_exc()}')


    def set_playback_rate(self, rate: float, increment: bool = False):
        ''' Sets the playback `rate` for the media, or increments it by
            `rate` if `increment` is True. Displays a marquee if desired. '''
        if increment:
            rate += self.playback_rate
        rate = round(rate, 4)                           # round `rate` to 4 places to avoid floating point imprecision

        player.set_playback_rate(rate)
        image_player.gif.setSpeed(int(rate * 100))
        self.playback_rate = rate

        if settings.checkTextOnSpeed.isChecked():
            show_on_player(f'{rate:.2f}x', 1000)
        log_on_statusbar(f'Playback speed set to {rate:.2f}x')


    def set_subtitle_delay(self, msec: int = 50, increment: bool = False, marq: bool = True):
        ''' Sets the subtitle delay to `msec`, or increments it by `msec` if
            `increment` is True. Displays a marquee if `marq` is True. '''
        if player.get_subtitle_track_count() <= 0:
            if marq:
                self.marquee('No subtitles available', marq_key='SubtitleDelay', log=False)
            return

        if increment:
            msec += player.get_subtitle_delay()
        player.set_subtitle_delay(int(msec))

        if marq:
            suffix = ' (later)' if msec > 0 else ' (sooner)' if msec < 0 else ''
            self.marquee(f'Subtitle delay {msec / 1000:.2f}s{suffix}', marq_key='SubtitleDelay', log=False)
        self.last_subtitle_delay = msec
        self.tracks_were_changed = True


    def set_audio_delay(self, msec: int = 50, increment: bool = False, marq: bool = True):
        ''' Sets the audio delay to `msec`, or increments it by `msec` if
            `increment` is True. Displays a marquee if `marq` is True. '''
        if player.get_audio_track_count() <= 0:
            if marq:
                self.marquee('No audio tracks available', marq_key='SubtitleDelay', log=False)
            return

        if increment:
            msec += player.get_audio_delay()
        player.set_audio_delay(int(msec))

        if marq:
            suffix = ' (later)' if msec > 0 else ' (sooner)' if msec < 0 else ''
            self.marquee(f'Audio delay {msec / 1000:.2f}s{suffix}', marq_key='SubtitleDelay', log=False)

        self.last_audio_delay = msec
        self.tracks_were_changed = True


    def set_volume(self, volume: int, verbose: bool = True) -> int:
        ''' Sets and displays `volume`, multiplied by `self.volume_boost`.
            Quietly unmutes player if necessary. Refreshes UI and displays
            a marquee (if `verbose`). Returns the new boosted volume,
            or -1 if unsuccessful. '''
        try:
            boost = self.volume_boost
            boosted_volume = int(volume * boost)
            player.set_volume(boosted_volume)
            player.set_mute(False)
            self.sliderVolume.setEnabled(True)

            if settings.checkTextOnVolume.isChecked() and verbose:
                show_on_player(f'{boosted_volume}%%', 200)
            refresh_title()
            self.refresh_volume_tooltip()
            return boosted_volume
        except:
            if constants.APP_RUNNING:                   # `show_on_player` errors out when the config triggers this on launch
                logging.error(f'(!) Failed to set volume: {format_exc()}')
            return -1


    def set_volume_boost(self, value: float = 1.0, increment: bool = False):
        ''' Sets `self.volume_boost` to `value`, or increments it by `value`
            if `increment` is True. Refreshs UI and displays marquee.
            NOTE: Cancels if a file was opened in the last 0.35 seconds. '''
        cancel_delta = get_time() - self.last_open_time
        if cancel_delta < 0.35:
            logging.info(f'Blocking possibly accidental volume boost (triggered {cancel_delta:.2f} seconds after opening a file)')
            return

        base_volume = self.sliderVolume.value()
        if increment: boost = max(0.5, min(5, self.volume_boost + value))
        else:         boost = max(0.5, min(5, value))

        self.volume_boost = boost
        if not player.get_mute(): self.set_volume(base_volume)
        else: self.refresh_volume_tooltip()

        if boost == 1.0: marq = f'{boost:.1f}x volume boost ({base_volume}%%)'
        else:            marq = f'{boost:.1f}x volume boost ({base_volume}%% -> {base_volume * boost:.0f}%%)'
        self.marquee(marq, marq_key='VolumeBoost', log=False)


    def set_mute(self, muted: bool, verbose: bool = True) -> int:
        ''' Sets mute-state to `muted`, updates UI, and shows a marquee (if
            `verbose`). Returns the player's new internal mute-state value. '''
        try:
            player.set_mute(muted)
            self.sliderVolume.setEnabled(not muted)     # disabled if muted, enabled if not muted
            base_volume = get_volume_slider()
            boost = self.volume_boost

            if muted:          marq = f'Muted{self.get_hotkey_full_string("mute")}'
            elif boost == 1.0: marq = f'Unmuted ({base_volume}%%)'
            else:              marq = f'Unmuted ({base_volume}%% -> {base_volume * boost:.0f}%%)\n{boost:.1f}x volume boost'

            if settings.checkTextOnMute.isChecked() and verbose:
                show_on_player(marq)
            self.refresh_volume_tooltip()
        except: logging.error(f'(!) Failed to set mute state: {format_exc()}')
        finally: return player.get_mute()


    def toggle_mute(self):
        ''' Toggles mute-state to the opposite of
            `self.sliderVolume`'s enable-state. '''
        self.set_mute(self.sliderVolume.isEnabled())


    def set_fullscreen(self, fullscreen: bool):
        ''' Toggles fullscreen-mode on and off. Saves window-state to
            `self.was_maximized` to remember if the window is maximized
            or not and restore the window accordingly. '''

        # FramelessWindowHint and WindowStaysOnTopHint not needed
        self.dockControls.setFloating(fullscreen)

        # entering fullscreen
        if fullscreen:  # TODO: figure out why dockControls won't resize in fullscreen mode -> strange behavior when showing/hiding control-frames
            current_screen = app.screenAt(self.mapToGlobal(self.rect().center()))   # fullscreen destination is based on center of window
            screen_size = current_screen.size()
            screen_geometry = current_screen.geometry()

            width_factor = settings.spinFullScreenWidth.value() / 100
            width = int(screen_size.width() * width_factor)
            height = sum(frame.height() for frame in (self.frameProgress, self.frameAdvancedControls) if frame.isVisible())
            x = int(screen_geometry.right() - ((screen_size.width() + width) / 2))  # adjust x/y values for screen's actual global position
            y = screen_geometry.bottom() - height

            self.dockControls.resize(width, height)
            #self.dockControls.setFixedWidth(width)     # TODO this is bad for DPI/scale and doesn't even fully get rid of the horizontal separator cursors. bandaid fix
            self.dockControls.move(x, y)
            self.dockControls.setWindowOpacity(settings.spinFullScreenMaxOpacity.value() / 100)     # opacity only applies while floating

            self.statusbar.setVisible(False)
            self.menubar.setVisible(False)              # TODO should this be like set_crop_mode's version? this requires up to 2 alt-presses to open
            self.was_maximized = self.isMaximized()     # remember if we're maximized or not

            # don't fade UI if we're hovering over the pending dockControls rect, the media...
            # ...is not playing (but not because we're paused), or the media is an image/GIF
            if settings.checkHideIdleCursor.isChecked():
                always_lock_ui = not player.is_playing() and not self.is_paused and not self.mime_type == 'image'
                if always_lock_ui or QtCore.QRect(x, y, width, height).contains(QtGui.QCursor.pos()):
                    self.vlc.idle_timeout_time = 0.0
                else:                                   # set timer to act like we JUST stopped moving the mouse
                    self.vlc.idle_timeout_time = get_time() + settings.spinHideIdleCursorDuration.value()

            player.on_fullscreen(fullscreen)
            self.ignore_next_fullscreen_move_event = True
            self.showFullScreen()                       # FullScreen with a capital S

        # leaving fullscreen
        else:
            self.statusbar.setVisible(self.actionShowStatusBar.isChecked())
            self.menubar.setVisible(self.actionShowMenuBar.isChecked())
            #self.dockControls.setFixedWidth(QWIDGETSIZE_MAX)

            player.on_fullscreen(fullscreen)
            self.showMaximized() if self.was_maximized else self.showNormal()


    def toggle_maximized(self):
        if self.isFullScreen():
            self.actionFullscreen.trigger()
        if self.isMaximized():
            self.showNormal()
        else:
            self.invert_next_move_event = True
            self.invert_next_resize_event = True
            self.showMaximized()


    def set_advancedcontrols_visible(self, visible: bool):
        ''' Sets visibility of the advanced controls (controls beneath
            the progress bar and above the status bar) to `visible`. '''
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
        if not self.isMaximized() and not self.isFullScreen():                      # resize window to preserve player size
            height = self.menubar.height()
            self.resize(self.width(), self.height() + (height if visible else -height))


    # https://video.stackexchange.com/questions/4563/how-can-i-crop-a-video-with-ffmpeg
    def set_crop_mode(self, on: bool):
        try:
            mime = self.mime_type
            is_gif = self.is_gif
            if not self.video or self.is_audio_without_cover_art:                   # reset crop mode if there's nothing to crop
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

                # create & setup crop frames for the first time. this is done here... because...
                if not vlc.crop_frames:
                    vlc.crop_frames = (
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
                        view.leaveEvent = vlc.leaveEvent
                        view.setVisible(True)
                        view.setMouseTracking(True)
                        view.setStyleSheet('background: rgba(0, 0, 0, 135)')        # TODO add setting here?

                # crop frames already exist -> enable/restore them
                else:
                    for view in vlc.crop_frames:
                        view.setEnabled(True)
                        view.setVisible(True)

                width = self.width()
                vlc.update_crop_frames()                                            # update crop frames and factored points
                vlc.refresh_crop_cursor(vlc.mapFromGlobal(QtGui.QCursor.pos()))     # set appropriate cropping cursor
                self.frameCropInfo.setVisible(width >= 621)                         # show crop info panel if there's space
                self.frameQuickChecks.setVisible(width >= 800)                      # hide checkmarks if there's no space
                if self.underMouse():                                               # unhide/lock ui if we're over the window
                    self.vlc.idle_timeout_time = 0.0
        except:
            log_on_statusbar(f'(!) Failed to toggle crop mode: {format_exc()}')


    def disable_crop_mode(self, log: bool = True):
        for view in self.vlc.crop_frames:                       # hide/disable crop frames
            view.setVisible(False)
            view.setEnabled(False)

        image_player.update()                                   # repaint gifPlayer to fix background
        self.vlc.dragging = None                                # clear crop-drag
        self.vlc.panning = False                                # clear crop-pan
        self.frameCropInfo.setVisible(False)                    # hide crop info panel
        self.frameQuickChecks.setVisible(self.width() >= 568)   # show checkmarks if there's space
        if settings.checkHideIdleCursor.isChecked():            # start hiding the cursor/UI right away if possible
            self.vlc.idle_timeout_time = 1.0                    # 0 locks the UI, so set it to 1

        # uncheck action and restore menubar/scale state. NOTE: if you do this part...
        # ...first, there's a chance of seeing a flicker after a crop edit is saved
        self.actionCrop.setChecked(False)
        restore_state = self.crop_restore_state
        self.set_menubar_visible(restore_state['menubar_visible'])
        if 'scale_setting' in restore_state:
            current_value = restore_state['scale_setting'].currentIndex()
            restore_state['scale_updater'](current_value, force=True)
        restore_state.clear()

        # `log` may be False when we're forcing crop mode to disable, such as while saving
        if log:
            log_on_statusbar('Crop mode disabled.')


    def set_track(self, track_type: str, track: int = -1, index_hint: int = None, title: str = None):
        ''' Sets `track_type` ("video", "audio", or "subtitle") to `track`,
            which can be either the `track`'s index or its associated
            `QtW.QAction`. If provided, `index_hint` is the index to
            show in the marquee instead of the garbage nonsense number
            that it probably was. `title` is the custom title to use in
            the marquee. This must be provided manually.'''
        logging.debug(f'Setting "{track_type}" track to {track} (hint={index_hint}, title={title})')
        types = {'video':    (-1, player.set_video_track),      # -1 = disabled, 0 = track 1
                 'audio':    (0,  player.set_audio_track),      # -1 = disabled, 1 = track 1
                 'subtitle': (1,  player.set_subtitle_track)}   # -1 = disabled, 2 = track 1
        offset_from_1, _set_track = types[track_type]           # TODO check back on this when more track-supporting players are added

        if isinstance(track, QtW.QAction):                      # `track` is actually a QAction
            index_hint = int(track.toolTip())                   # true index is stored in the action's tooltip
            #title = title or track.text()                      # TODO: should we still show the title even though the user literally clicked on it?
            track = track.data()                                # track index is stored in the action's `data` property

        # actually set the track, then choose what number we're going to show in the marquee
        _set_track(track)
        setattr(self, f'last_{track_type}_track', track)        # remember the track we've chosen so we can restore it
        track_index = index_hint if index_hint is not None else (track - offset_from_1)

        # check if `title` is actually unique and not something like "Track 1"
        if title is not None:
            parts = title.split()
            if len(parts) > 1 and parts[0].lower() == 'track':  # ↓ detect things like 'Track "2"' or 'Track 2)'
                if parts[1].strip('"\'()[]{}<>;:-').isnumeric():
                    if len(parts) > 2:                          # ↓ skip third "word" if it's just a hyphen or something
                        start = 2 if parts[2].strip('"\'()[]{}<>;:-') else 3
                        title = ' '.join(parts[start:])
                    else: title = None
                else: title = None

        # if `title` is (or has become) None, use generic marquee, i.e. "Audio track 2 enabled"
        # otherwise, use something like "Audio track 2 'Microphone' enabled"
        if track != -1:
            prefix = f'{track_type.capitalize()} track {track_index}'
            if title: title = f'{prefix}  \'{title}\' enabled'
            else:     title = f'{prefix} enabled'
            marquee(title, marq_key='TrackChanged', log=False)
        else:
            if getattr(player, f'SUPPORTS_{track_type.upper()}_TRACK_MANIPULATION'):
                if track_type == 'subtitle':
                    track_type = 'subtitles'                    # prefer "Subtitles disabled" over "Subtitle disabled"
                marquee(f'{track_type.capitalize()} disabled', marq_key='TrackChanged', log=False)
            else:
                marquee(f'The selected player does not support {track_type} track manipulation', marq_key='TrackChanged', log=False)

        self.tracks_were_changed = True
        gc.collect(generation=2)


    def cycle_track(self, track_type: str):
        ''' Cycles to the next valid `track_type` ("video", "audio", or
            "subtitle"), if one is available. Depending on settings, this
            may loop back around to either "Disabled" or track #1. Displays
            a marquee if cycle could not play a new track. '''
        types = {'video':    (player.get_video_tracks,    player.get_video_track_count,    player.get_video_track),
                 'audio':    (player.get_audio_tracks,    player.get_audio_track_count,    player.get_audio_track),
                 'subtitle': (player.get_subtitle_tracks, player.get_subtitle_track_count, player.get_subtitle_track)}
        get_ids_and_titles, get_count, get_current_id = types[track_type]

        track_count = get_count() - 1
        if track_count > 0:
            current_track_id = get_current_id()
            first_track_parameters = (-1, None, None)
            show_title = settings.checkTrackCycleShowTitle.isChecked()
            for index, (track_id, track_title) in enumerate(get_ids_and_titles(raw=True)):
                track_title = track_title if show_title else None
                if first_track_parameters[0] == -1 and track_id > -1:
                    first_track_parameters = (track_id, index, track_title)
                if track_id > current_track_id:                 # ^ mark the first valid track
                    self.set_track(track_type, track_id, index, track_title)
                    break

            # `else` is reached if we didn't break the for-loop (we ran out of tracks to cycle through)
            # loop back to either the first valid track or to "disabled", depending on user settings
            else:
                if settings.checkTrackCycleCantDisable.isChecked():
                    if first_track_parameters[0] != current_track_id:
                        self.set_track(track_type, *first_track_parameters)
                    else:                                       # display special message if there's nothing else to cycle to
                        marquee(f'No other {track_type} tracks available', marq_key='TrackChanged', log=False)
                else:
                    self.set_track(track_type, -1)
        else:
            if getattr(player, f'SUPPORTS_{track_type.upper()}_TRACK_MANIPULATION'):
                marquee(f'No {track_type} tracks available', marq_key='TrackChanged', log=False)
            else:
                marquee(f'The selected player does not support {track_type} track manipulation', marq_key='TrackChanged', log=False)


    def restore_tracks(self, safely: bool = False):
        ''' Restores the previously selected audio/subtitle/video track/delays.
            This is needed because some players reset all track selections after
            they're stopped. If `safely` is True, safeguards are used to prevent
            infinite loops, even in the event of a corrupted file being opened.
            `safely` should only be used for players that cannot do not emit
            their own events for opening/playing media. '''

        video = self.video                                      # remember what video we were trying to open
        if not self.tracks_were_changed:
            return

        if safely:
            # tracks cannot be consistently set or read properly while in the `Opening` state
            # NOTE: this mostly affects keeping tracks disabled since the track numbers default...
            # ...to disabled so we can't tell if the track is actually disabled yet or not
            timeout = get_time() + 3.0
            while (player.get_state() == State.NothingSpecial or player.get_state() == State.Opening) and video == self.video and get_time() < timeout:
                if get_time() > timeout:
                    return log_on_statusbar('(!) Could not restore track selections, libVLC failed to leave the "Opening" state after 3 seconds.')
                sleep(0.002)

            # make sure we didn't open a new file just now. this SHOULD be impossible, but just in case
            if video != self.video:
                return logging.info('(?) Track restoration cancelled, file is changing.')

        # most to least important: audio -> subtitles -> subtitle delay -> audio delay -> video
        logging.info('Restoring tracks to their previous selections...')
        try: player.set_audio_track(self.last_audio_track)
        except: pass
        try: player.set_subtitle_track(self.last_subtitle_track)
        except: pass
        try: self.set_subtitle_delay(self.last_subtitle_delay, marq=False)
        except: pass
        try: self.set_audio_delay(self.last_audio_delay, marq=False)
        except: pass
        try: player.set_video_track(self.last_video_track)
        except: pass

        # clear marquee if needed
        player.show_text('')


    def refresh_track_menu(self, menu: QtW.QMenu):
        menus = {self.menuVideoTracks: ('video',    player.get_video_tracks,    player.get_video_track,    player.get_video_track_count,    -1),
                 self.menuAudioTracks: ('audio',    player.get_audio_tracks,    player.get_audio_track,    player.get_audio_track_count,    0),
                 self.menuSubtitles:   ('subtitle', player.get_subtitle_tracks, player.get_subtitle_track, player.get_subtitle_track_count, 0)}
        track_type, get_ids_and_titles, get_current_id, get_count, minimum_tracks = menus[menu]

        menu.clear()                                            # clear previous contents of menu
        if menu is self.menuSubtitles:
            menu.addAction(self.actionAddSubtitleFile)
            menu.addSeparator()

        track_count = get_count()
        if track_count > minimum_tracks:
            current_track_id = get_current_id()
            action_group = QtW.QActionGroup(menu)
            action_group.triggered.connect(lambda *args: self.set_track(track_type, *args))

            for index, (track_id, track_title) in enumerate(get_ids_and_titles(raw=True)):
                name_parts = track_title.split()                # check if track number is in it's title -> add &-shortcut
                new_parts = []
                for part_index, part in enumerate(name_parts):  # NOTE: use `part_index` so we don't overwrite outer-loop's `index`
                    if part.isnumeric():                        # track number identified, add &-shortcut and stop
                        new_parts.append('&' + part)
                        new_parts.extend(name_parts[part_index + 1:])
                        break
                    else:
                        new_parts.append(part)
                track_name = ' '.join(new_parts)

                # create and add action, storing its track index and true index in its `data` and tooltip
                action = QtW.QAction(track_name, action_group)  # get_spu_description includes pre-generated track titles with tags -> VLC uses the last...
                action.setData(track_id)                        # ...non-extension keyword separated by a period in the filename as the track's tag
                action.setToolTip(str(index))                   # e.g. 'dawnofthedead.2004.ENG.srt' -> 'Track 1 - [ENG]'
                action.setCheckable(True)                       # originally I was doing all of that manually, while juggling the random inconsistent indexes
                if current_track_id == track_id:                # NOTE: one year later and I don't remember why I put these comments here ^
                    action.setChecked(True)
                menu.addAction(action)
        else:
            menu.addAction(f'No {track_type} tracks').setEnabled(False)


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


    def refresh_undo_menu(self):
        ''' Generates undo action(s) for the undo menu, if necessary. '''
        self.menuUndo.clear()
        if not self.undo_dict:
            return self.menuUndo.addAction('Nothing to undo').setEnabled(False)

        # NOTE: signals must be wrapped in lambdas or they'll be considered "weak references" and crash
        primary = tuple(self.undo_dict.values())[-1]            # stack -> last undo is the latest one
        undo_action = self.menuUndo.addAction(f'Undo {primary.label}')
        undo_action.setToolTip(primary.description)
        undo_action.triggered.connect(lambda: primary.execute())

        # if there's an undo specifically for this file that ISN'T the latest undo, add a second action
        if (secondary := self.undo_dict.get(self.video)) and secondary is not primary:
            undo_action = self.menuUndo.addAction(f'For this file: Undo {secondary.label}')
            undo_action.setToolTip(secondary.description)
            undo_action.triggered.connect(lambda: secondary.execute())


    def _refresh_title_slot(self):                              # TODO this could theoretically be much faster, but is it worth it?
        ''' Updates the window's titlebar using various variables,
            based on `lineWindowTitleFormat`. This can be called
            directly, but you probably shouldn't. '''

        if self.video:
            path = self.video
            basepath, name = os.path.split(path)
            parent = f'{basepath.split(sep)[-1]}{sep}{name}'
            base, _ = splitext_media(name, strict=False)        # don't actually need ext, just the accurate basename

            mime = self.mime_type.capitalize()                  # capitalize first letter of mime type
            h, m, s, _ = get_hms(self.duration_rounded)         # no milliseconds in window title
            duration = f'{m}:{s:02}' if h == 0 else f'{h}:{m:02}:{s:02}'
            ratio = self.ratio

            # set pause icon
            if player.get_state() == State.Stopped or get_ui_frame() == self.frame_count:
                paused = '■'
            elif self.is_paused:
                paused = '𝗜𝗜'
            else:
                paused = '▷'                                    # ▶ ↻

            # set fps and resolution labels
            if mime != 'Audio':                                 # remember, we just capitalized this
                fps = str(self.frame_rate_rounded)
                resolution = f'{self.vwidth:.0f}x{self.vheight:.0f}'
            elif self.is_audio_with_cover_art:                  # show resolution of cover art
                fps = '0'
                resolution = f'{self.vwidth:.0f}x{self.vheight:.0f}'
            else:
                fps = '0'
                resolution = '0x0'

        else:
            path = name = base = parent = 'No media is playing'
            mime = 'Unknown'
            paused = '■'    # ▁▂▃▄▅▇▉ ▊▋█ ❏ ?paused ?name (?duration | ?fpsfps)
            fps = '0'       # ?base | ?name | ?parent | ?path | ?ext | ?mime | ?paused | ?fps | ?duration | ?resolution | ?ratio | ?volume | ?speed | ?size
            duration = '--:--'
            resolution = '0x0'
            ratio = '0:0'

        # add progress percentage if it should be visible
        if self.edits_in_progress:
            avg_value = 0
            total_operations = 0
            for edit in self.edits_in_progress:                 # get average across all operations in all edits
                total_operations += edit.operation_count
                avg_value += edit.value + ((edit.operations_started - 1) * 100)
            avg_value /= total_operations                       # divide-by-zero SHOULD be impossible here
            title = f'[{max(0, avg_value):.0f}%] {settings.lineWindowTitleFormat.text()}'
        else:
            title = settings.lineWindowTitleFormat.text()

        # replace potential variables in the title with their values and set new title
        replace = {'?base': base, '?name': name, '?parent': parent, '?path': path, '?ext': self.extension_label, '?mime': mime,
                   '?paused': paused, '?fps': fps, '?duration': duration, '?resolution': resolution, '?ratio': ratio,
                   '?volume': str(get_volume_slider()), '?speed': f'{self.playback_rate:.2f}', '?size': self.size_label}
        for var, val in replace.items():
            title = title.replace(var, val)
        self.setWindowTitle(title.strip())


    def refresh_copy_image_action(self):
        ''' Updates `self.actionCopyImage`'s text to the current context,
            i.e. "Copy image" for an image or "Copy cropped frame" for a
            video with crop-mode enabled, etc. '''
        mime = self.mime_type
        cropped = self.actionCrop.isChecked()
        if mime == 'audio':                  text = 'Copy cover art'
        elif mime == 'video' or self.is_gif: text = 'Copy cropped frame' if cropped else 'Copy frame'
        else:                                text = 'Copy cropped image' if cropped else 'Copy image'
        self.actionCopyImage.setText('&' + text)


    def refresh_shortcuts(self, last_edit: widgets.QKeySequenceFlexibleEdit = None):
        ''' Refreshes the `Hotkeys` page in the settings dialog, clearing out
            duplicate shortcuts on launch (when `last_edit` is None) and
            swapping newly duplicated shortcuts while editing hotkeys. '''

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


    def refresh_cover_art(self, show: bool):
        ''' Toggles cover art on/off if there's any data in our buffer.
            Updates `self.vwidth` and `self.vheight` accordingly. '''
        if show:
            if self.is_audio_with_cover_art:                    # do nothing if we want to show but have nothing in our buffer
                try:
                    play_image(self.cover_art_buffer, coverart=True, interactable=False)
                    size = image_player.art.size()
                    self.vwidth = size.width()
                    self.vheight = size.height()
                except:
                    log_on_statusbar(f'(!) Unable to display the current media\'s cover art: {format_exc()}')
        else:                                                   # ONLY clear cover art if `show` is False
            play_image(None)                                    # NOTE: don't reset vwidth/vheight to 16/9


    def refresh_autoplay_button(self):
        ''' Updates the autoplay button's icon and check-state. '''
        if self.actionAutoplayShuffle.isChecked():              icon = 'autoplay_shuffle'
        elif self.actionAutoplayDirectionForwards.isChecked():  icon = 'autoplay'
        elif self.actionAutoplayDirectionBackwards.isChecked(): icon = 'autoplay_backward'
        elif self.last_cycle_was_forward:                       icon = 'autoplay'
        else:                                                   icon = 'autoplay_backward'
        self.buttonAutoplay.setIcon(self.icons[icon])
        self.buttonAutoplay.setChecked(self.actionAutoplay.isChecked())


    def refresh_confusing_zoom_setting_tooltip(self, value: float):
        ''' Updates the `value`'s in a tooltip for a particularly confusing
            setting to make it more obvious what the setting actually does. '''
        settings.checkZoomForceMinimum.setToolTip(
            constants.ZOOM_FORCE_MINIMUM_TOOLTIP_BASE.replace('?value', str(value))
        )


    def refresh_recycle_tooltip(self, recycle: bool):
        ''' Updates some text/tooltips to reflect whether "deleting" means
            to actually delete something or to just move it to the `recycle` bin. '''
        if recycle:
            self.actionDeleteImmediately.setText('Immediately recycle')
            self.actionDeleteImmediately.setToolTip('Immediately move the current media to the recycle bin.')
        else:
            self.actionDeleteImmediately.setText('Immediately delete')
            self.actionDeleteImmediately.setToolTip('Immediately delete the current media.\nThis cannot be undone.')


    def refresh_volume_tooltip(self):
        ''' Updates the volume slider's tooltip to include
            mute-state and current volume boost, if necessary. '''
        muted = not self.sliderVolume.isEnabled()
        boost = self.volume_boost
        base_volume = get_volume_slider()
        boosted_volume = base_volume * boost

        if muted:
            hotkey_string = self.get_hotkey_full_string('mute')
            if boost == 1.0: tooltip = f'{boosted_volume:.0f}%\nMuted{hotkey_string}'
            else:            tooltip = f'{boosted_volume:.0f}% ({boost:.1f}x boost)\nMuted{hotkey_string}'
        elif boost == 1.0:   tooltip = f'{boosted_volume:.0f}%'
        else:                tooltip = f'{boosted_volume:.0f}% ({boost:.1f}x boost)'
        self.sliderVolume.setToolTip(tooltip)


    def refresh_marked_for_deletion_tooltip(self):
        ''' Updates the deletion button's tooltip to
            include the current number of marked files. '''
        tooltip_count_string = f'{len(self.marked_for_deletion)} file{"s" if len(self.marked_for_deletion) != 1 else ""}'
        self.buttonMarkDeleted.setToolTip(constants.MARK_DELETED_TOOLTIP_BASE.replace('?count', tooltip_count_string))


    def refresh_snapshot_button_controls(self):
        ''' Updates the various actions that the snapshot button
            can perform, updating the tooltip accordingly. '''
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


    def handle_cycle_buttons(self, *, next: bool = True):
        ''' Handles what to do when a cycle button is clicked, depending on what
            keyboard modifiers are held down and whether `next` is True. '''
        mod = app.keyboardModifiers()
        if not mod:                    self.cycle_media(next=next)
        elif mod & Qt.ShiftModifier:   self.cycle_media(next=next, valid_mime_types=(self.mime_type,))
        elif mod & Qt.ControlModifier: self.shuffle_media()
        elif mod & Qt.AltModifier:     self.shuffle_media(valid_mime_types=(self.mime_type,))


    def handle_snapshot_button(self):
        ''' Handles what to do when the snapshot button is clicked,
            depending on what keyboard modifiers are currently held
            down and what snapshot actions the user has enabled. '''
        mod = app.keyboardModifiers()
        if not mod:                    self.snapshot_actions[settings.comboSnapshotDefault.currentIndex()][0]()
        elif mod & Qt.ShiftModifier:   self.snapshot_actions[settings.comboSnapshotShift.currentIndex()][0]()
        elif mod & Qt.ControlModifier: self.snapshot_actions[settings.comboSnapshotCtrl.currentIndex()][0]()
        elif mod & Qt.AltModifier:     self.snapshot_actions[settings.comboSnapshotAlt.currentIndex()][0]()


    def refresh_taskbar(self):
        ''' Updates the current pause-state icon in the taskbar toolbar,
            as well as the current overlay icon. NOTE: Windows-only. '''
        if not constants.IS_WINDOWS: return

        overlay_taskbar_icon = self.isMinimized() and settings.checkTaskbarIconPauseMinimized.isChecked()
        if get_ui_frame() == self.frame_count:
            self.taskbar_toolbar_restart.setVisible(True)
            self.taskbar_toolbar_play.setVisible(False)
            self.taskbar_toolbar_pause.setVisible(False)
            if overlay_taskbar_icon:
                self.taskbar.setOverlayIcon(self.icons['restart'])
        else:
            paused = self.is_paused
            self.taskbar_toolbar_restart.setVisible(False)
            self.taskbar_toolbar_play.setVisible(paused)
            self.taskbar_toolbar_pause.setVisible(not paused)
            if overlay_taskbar_icon:
                self.taskbar.setOverlayIcon(self.icons['pause' if paused else 'play'])


    def create_taskbar_controls(self):
        ''' Creates controls for a special progress bar and toolbar embedded
            within the taskbar icon and its flyout-thumbnail. To actually
            enable/display the toolbar, call `self.enable_taskbar_controls`
            after the window has been shown. NOTE: Windows-only.

            NOTE: Qt does not expose `ITaskbarList3.ThumbBarUpdateButtons`.
            As a result, we MUST use three separate buttons for pausing and
            toggle visibility between them to force Qt to update, simulating
            the appearance of the icons changing in real-time. You cannot
            achieve the effect any other way as far as I know, not even by
            changing the icon and then flickering visiblity (for some reason).

            NOTE: I wanted to implement this myself as `QtWinExtras` is no
            longer supported in Qt 6.0, but I cannot find a single working,
            up-to-date implementation of toolbar buttons in Python. In fact,
            I can only find two attempts at this AT ALL, with only one appearing
            to be "finished". It uses Cython and seems to no longer work (?) -
            https://github.com/sjohannes/winmmtaskbar - Taskbar extensions have
            a VERY unusual method of implementation (involving compiling your
            own file and using COM) which is particularly difficult to convert
            into native Python. Combine that with a lack of interest (how many
            programs can you name that even use taskbar extensions, let alone
            an embedded thumbnail toolbar?), and you end up with ONE PERSON
            finishing a library for the embedded toolbar in 14 years (unlike
            the progress bar, which has many working implementations). '''
        if not constants.IS_WINDOWS: return

        from PyQt5 import QtWinExtras
        self.taskbar = QtWinExtras.QWinTaskbarButton()
        self.taskbar_progress = self.taskbar.progress()
        self.taskbar_progress.setVisible(True)
        self.taskbar_toolbar = QtWinExtras.QWinThumbnailToolBar()

        self.taskbar_toolbar_pause = QtWinExtras.QWinThumbnailToolButton(self.taskbar_toolbar)
        self.taskbar_toolbar_pause.setIcon(self.icons['pause'])
        self.taskbar_toolbar_pause.clicked.connect(self.pause)

        self.taskbar_toolbar_play = QtWinExtras.QWinThumbnailToolButton(self.taskbar_toolbar)
        self.taskbar_toolbar_play.setIcon(self.icons['play'])
        self.taskbar_toolbar_play.clicked.connect(self.pause)

        self.taskbar_toolbar_restart = QtWinExtras.QWinThumbnailToolButton(self.taskbar_toolbar)
        self.taskbar_toolbar_restart.setIcon(self.icons['restart'])
        self.taskbar_toolbar_restart.clicked.connect(self.pause)

        stop_button = QtWinExtras.QWinThumbnailToolButton(self.taskbar_toolbar)
        stop_button.setToolTip('Stop')
        stop_button.setIcon(self.icons['stop'])
        stop_button.clicked.connect(self.stop)

        cycle_forward_button = QtWinExtras.QWinThumbnailToolButton(self.taskbar_toolbar)
        cycle_forward_button.setToolTip(self.buttonNext.toolTip())
        cycle_forward_button.setIcon(self.icons['cycle_forward'])
        cycle_forward_button.clicked.connect(self.cycle_media)

        cycle_backward_button = QtWinExtras.QWinThumbnailToolButton(self.taskbar_toolbar)
        cycle_backward_button.setToolTip(self.buttonPrevious.toolTip())
        cycle_backward_button.setIcon(self.icons['cycle_backward'])
        cycle_backward_button.clicked.connect(lambda: self.cycle_media(next=False))

        settings_button = QtWinExtras.QWinThumbnailToolButton(self.taskbar_toolbar)
        settings_button.setToolTip('Settings')
        settings_button.setIcon(self.icons['settings'])
        settings_button.setDismissOnClick(True)
        settings_button.clicked.connect(self.dialog_settings.exec)

        self.taskbar_toolbar_play.setVisible(False)
        self.taskbar_toolbar_restart.setVisible(False)
        self.taskbar_toolbar.setButtons((
            stop_button,
            cycle_backward_button,
            self.taskbar_toolbar_pause,
            self.taskbar_toolbar_play,
            self.taskbar_toolbar_restart,
            cycle_forward_button,
            settings_button
        ))


    def enable_taskbar_controls(self, checked: bool = True):
        ''' Sets the window handle for the taskbar toolbar if `checked`
            is True. This cannot be undone. NOTE: Windows-only. '''
        if checked and constants.IS_WINDOWS:
            self.taskbar_toolbar.setWindow(self.windowHandle())


    def is_snap_mode_enabled(self) -> bool:
        ''' Returns True if snap-modes can be used on the current mime type.
            Does not snap audio if there is no currently visible cover art. '''
        if self.mime_type == 'video':   return settings.checkSnapVideos.isChecked()
        elif self.mime_type == 'audio': return self.is_audio_with_cover_art and can_show_cover_art() and settings.checkSnapArt.isChecked()
        elif self.is_gif:               return settings.checkSnapGifs.isChecked()
        else:                           return settings.checkSnapImages.isChecked()


    def snap_to_player_size(self, shrink: bool = False, force_instant_resize: bool = False):
        ''' Resizes the window to match what the internal player is actually
            showing, without black bars. If `shrink` is False, the window will
            find the average between the current size and the player's size.
            If `force_instant_resize` is True, the resize will happen instantly,
            regardless of settings. Clamps to screen afterwards if desired. '''
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
                    if expected_vlc_size != vlc_size:
                        self.resize(expected_vlc_size.width(), true_height)
                    return self.snap_to_player_size(shrink=True)    # snap again, but shrink this time

            # experimental animated snap (discovered by accident)
            else:
                expected_vlc_size.setWidth(expected_vlc_size.width() + round(void_width / 2))
                expected_vlc_size.setHeight(expected_vlc_size.height() + round(void_height / 2))

            # resize window if player size does not match the expected size (expected size = w/o black bars)
            true_height = expected_vlc_size.height() + self.height() - self.vlc.height()
            if expected_vlc_size != vlc_size:
                self.resize(expected_vlc_size.width(), true_height)

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
        ''' Resizes window to the current media's native resolution, unless it's
            an audio file without cover art. Clamps to screen afterwards. '''
        if not self.video or self.is_audio_without_cover_art: return
        excess_height = self.height() - self.vlc.height()
        self.resize(self.vwidth, self.vheight + excess_height)
        qthelpers.clampToScreen(self)


    def mark_for_deletion(self, *files: str, mark: bool = False, mode: str = None):
        ''' Marks `files` for deletion if `mark` is True, updating the deletion
            checkboxes accordingly. Alternate behavior is triggered if `mode` is
            set to "delete" or "prompt". If `mode` is None, it will be set based
            on what (if any) modifiers are being held down: "delete" for Ctrl,
            "prompt" for Shift. '''

        # auto-uncheck button if no file is open or given
        if not files:
            if not self.video:
                self.actionMarkDeleted.setChecked(False)
                self.buttonMarkDeleted.setChecked(False)
                return show_on_statusbar('No media is playing.', 10000)
            files = (self.video,)

        # auto-set `mode` based on modifier keys if `mode` was None
        if mode is None:
            mod = app.keyboardModifiers()
            if mod and not self.mark_for_deletion_held_down:    # don't auto-set `mode` while auto-marking
                if mod & Qt.ControlModifier: mode = 'delete'    # ctrl pressed -> immediately delete video
                elif mod & Qt.ShiftModifier: mode = 'prompt'    # shift pressed -> show deletion prompt
        else:
            mode = mode.lower()
        logging.info(f'Marking files {files} for deletion: {mark}. Mode: {mode}')

        if mode == 'delete':   self.delete(*files)
        elif mode == 'prompt': self.show_delete_prompt()
        elif mark:             self.marked_for_deletion.update(files)
        else:                  self.marked_for_deletion.difference_update(files)

        # ensure mark-button is in the correct state and update tooltip
        if self.video in files:
            self.actionMarkDeleted.setChecked(mark)
            self.buttonMarkDeleted.setChecked(mark)
        self.refresh_marked_for_deletion_tooltip()


    def clear_marked_for_deletion(self):
        ''' Clears all marked files and updates the UI accordingly. '''
        self.marked_for_deletion.clear()
        self.actionMarkDeleted.setChecked(False)
        self.buttonMarkDeleted.setChecked(False)
        self.refresh_marked_for_deletion_tooltip()


    # https://www.geeksforgeeks.org/convert-png-to-jpg-using-python/
    def convert_snapshot_to_jpeg(self, path: str = None, image_data=None, quality: int = None) -> str:
        ''' Saves `path` or `image_data` as a JPEG file with the desired
            `quality` using PIL. If `quality` is None, the preset quality
            in the user's settings is used. If provided, assumes that `path`
            already ends in a valid file-extension. '''
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
        app = QtW.QApplication(sys.argv)                # init qt
        gui = widgets.gui = GUI_Instance(app)           # init empty GUI instance
        gui.setup()                                     # setup gui's variables, widgets, and threads (0.3mb)

        # --------------------------------------------------------
        # Aliases for common/time-sensitive functions & variables
        # --------------------------------------------------------
        player = gui.vlc.player
        image_player = gui.gifPlayer
        play = player.play
        play_image = gui.gifPlayer.play
        settings = gui.dialog_settings
        refresh_title = gui.refresh_title_signal.emit
        marquee = gui.marquee
        show_on_player = player.show_text
        log_on_statusbar = gui.log_on_statusbar_signal.emit
        show_on_statusbar = gui.statusbar.showMessage
        update_progress = gui.update_progress
        set_and_update_progress = player.set_and_update_progress
        set_volume_slider = gui.sliderVolume.setValue
        get_volume_slider = gui.sliderVolume.value
        get_volume_scroll_increment = settings.spinScrollVolume.value
        get_ui_frame = gui.sliderProgress.value
        set_progress_slider = gui.sliderProgress.setValue
        set_hour_spin = gui.spinHour.setValue
        set_minute_spin = gui.spinMinute.setValue
        set_second_spin = gui.spinSecond.setValue
        set_frame_spin = gui.spinFrame.setValue
        set_player_position = player.set_position
        set_gif_position = image_player.gif.jumpToFrame
        set_current_time_text = gui.lineCurrentTime.setText
        current_time_lineedit_has_focus = gui.lineCurrentTime.hasFocus
        can_load_cover_art = settings.checkLoadCoverArt.isChecked
        can_show_cover_art = settings.checkShowCoverArt.isChecked
        parse_json = json.JSONDecoder(object_hook=None, object_pairs_hook=None).decode
        abspath = os.path.abspath
        exists = os.path.exists
        sep = os.sep

        widgets.settings = settings                     # set settings dialog as global object in widgets.py
        qtstart.connect_widget_signals(gui)             # connect signals and slots
        cfg = widgets.cfg = config.loadConfig(gui)      # create and load config (uses constants.CONFIG_PATH)

        if not qtstart.args.minimized:                  # show UI
            gui.show()
        else:
            check_tray = settings.groupTray
            if not check_tray.isChecked():              # if tray icon is enabled, don't show UI at all
                gui.showMinimized()                     # otherwise, start with window minimized

        constants.verify_ffmpeg(gui)                    # confirm/look for valid ffmpeg path if needed
        FFPROBE = constants.verify_ffprobe(gui)         # confirm/look/return valid ffprobe path if needed
        qtstart.after_show_setup(gui)                   # perform final bits of misc setup before showing UI

        with open(constants.PID_PATH, 'w'):             # create PID file
            gc.collect(generation=2)                    # final garbage collection before starting
            constants.APP_RUNNING = True
            logging.info(f'Starting GUI after {get_time() - constants.SCRIPT_START_TIME:.2f} seconds.')
            try: app.exec()
            except: logging.critical(f'(!) GUI FAILED TO EXECUTE: {format_exc()}')
            logging.info('Application execution has finished.')
        try: os.remove(constants.PID_PATH)
        except: logging.warning(f'(!) Failed to delete PID file: {format_exc()}')
    except: logging.critical(f'(!) SCRIPT FAILED TO INITIALIZE: {format_exc()}')
