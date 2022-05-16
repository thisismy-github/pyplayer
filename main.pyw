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
TODO: move open_color_picker and other browse dialogs + indeterminate_progress decorator + setCursor(app) and resetCursor(app) to qthelpers?
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
TODO: refactor:
        - refactor inconsistent function indentations (especially for qthelpers functions)
        - refactor inconsistent parent usage (is setParent() and parent() worth the likely performance loss?)
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
TODO: pressing esc on QWidgetPassthrough clears focus, but sometimes clears focus on the entire window
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
        native "Save as..." prompt replaced by strange and extremely buggy Qt version if the first thing you open after launch is an image
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
from util import get_unique_path, add_path_suffix, get_hms, get_aspect_ratio, file_is_hidden
from bin.window_pyplayer import Ui_MainWindow
from bin.window_settings import Ui_settingsDialog

import os
import gc
import sys
import math
import json
import logging
import subprocess
from time import sleep, localtime, mktime, strftime, strptime
from time import time as get_time                       # from time import time -> time() errors out
from threading import Thread
from traceback import format_exc

import filetype                                         # 0.4mb ram
from vlc import State, VideoMarqueeOption
from sanitize_filename import sanitize
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
def ffmpeg(infile: str, cmd: str, outfile: str = '') -> str:
    start = get_time()
    logging.info(f'Performing FFmpeg operation (infile={infile} | outfile={outfile} | cmd={cmd})...')

    # create temp file if '%tp' is in ffmpeg command (and we have a valid `out` file)
    temp_path = ''
    if '%tp' in cmd and infile and os.path.exists(infile):
        temp_path = add_path_suffix(infile, '_temp', unique=True)
        if infile == gui.locked_video: gui.locked_video = temp_path    # update locked video if needed TODO does this make sense...?
        os.renames(infile, temp_path)                                  # rename `out` to temp name

    # run final ffmpeg command
    try: ffmpeg_simple(cmd.replace("%tp", temp_path))
    except: logging.error(f'(!) FFMPEG CALL FAILED: {format_exc()}')

    # cleanup temp file, if needed
    if temp_path:
        if os.path.exists(infile):
            try: os.remove(temp_path)
            except: logging.warning(f'Temporary FFmpeg file {temp_path} could not be deleted')
        else:   # TODO I don't think this can ever actually happen, and it makes as little sense as the locked_file line up there
            if temp_path == gui.locked_video: gui.locked_video = infile
            os.renames(temp_path, infile)
    gui.log(f'FFmpeg operation succeeded after {get_time() - start:.1f} seconds.')
    return outfile


def ffmpeg_simple(cmd: str) -> None:    # https://code.activestate.com/recipes/409002-launching-a-subprocess-without-a-console-window/
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    cmd = f'{constants.FFMPEG} -y {cmd} -hide_banner -loglevel warning'
    logging.info('FFmpeg command: ' + cmd)
    subprocess.Popen(cmd, startupinfo=startupinfo, shell=True).wait()


def get_PIL_Image():
    ''' An over-the-top way of hiding the PIL folder. PIL folder cannot be avoided due to
        the from-import, and hiding it using conventional means does not seem to work, so
        instead we hide the folder, move (NOT copy) it to the root folder so we can import
        it, and then move it back. All this, just to hide a single item. Honestly worth it.
        NOTE: If PIL.Image isn't already imported, this can hang when called from the script. '''
    try:    # prepare PIL for importing if it hasn't been imported yet (once imported, it's imported for good)
        PIL_already_imported = 'PIL.Image' in sys.modules
        if not PIL_already_imported and constants.IS_COMPILED:
            logging.info('Import PIL for the first time...')
            join = os.path.join                 # create alias due to high usage
            exists = os.path.exists             # create alias due to high usage
            files_moved = []

            # identify new PIL path and check if it already exists
            new_path = join(constants.CWD, 'PIL')
            new_path_already_existed = exists(new_path)
            new_path_renamed = False

            # identify expected PIL path and a backup for it, assert existence of at least one PIL path
            old_path = join(constants.BIN_DIR, 'PIL')
            backup_path = old_path + '.bak'
            backup_path_already_existed = exists(backup_path)
            if backup_path_already_existed:     # backup already exists (likely from error in previous session)
                logging.warning(f'PIL backup path {backup_path} already exists, using it...')
                old_path, backup_path = backup_path, old_path   # swap backup and old paths
            assert exists(old_path) or new_path_already_existed, 'PIL folder not found at ' + old_path

            # backup old PIL path and create new PIL path. if it already exists (for some reason), rename it temporarily
            if exists(old_path):                # if old PIL path doesn't exist, just hope the new PIL path is correct
                import shutil
                shutil.copytree(old_path, backup_path)
                if new_path_already_existed:
                    try:
                        new_path_temp_name = get_unique_path(new_path + '_temp')
                        os.rename(new_path, new_path_temp_name)
                        new_path_renamed = True
                    except: logging.warning(f'Could not rename {new_path} to {new_path}_temp: {format_exc()}')
                try: os.makedirs(new_path)
                except: logging.warning(f'Could not make {new_path}: {format_exc()}')

            # move (NOT copy) each file from the normal PIL path to the new PIL path and append each move to files_moved
            for file in os.listdir(old_path):
                if file[-4:] != '.pyd': continue
                old_file = join(old_path, file)
                new_file = join(new_path, file)
                os.rename(old_file, new_file)
                files_moved.append((old_file, new_file))

        from PIL import Image                   # actually import PIL.Image (this is what hangs in the script)

        # return files to their original spots, delete/restore new PIL path, and return PIL.Image
        if not PIL_already_imported and constants.IS_COMPILED:
            import shutil
            for source, dest in files_moved:
                try: os.rename(dest, source)
                except: logging.warning(f'Could not move {dest} to {source}: {format_exc()}')
            if not (new_path_already_existed and not new_path_renamed):
                try: shutil.rmtree(new_path)
                except: logging.warning(f'Could not delete {new_path}: {format_exc()}')
            if new_path_renamed: os.rename(new_path_temp_name, new_path)
            if exists(backup_path): shutil.rmtree(backup_path)
            if backup_path_already_existed: os.rename(old_path, backup_path)
            logging.info('First-time PIL import successful.')
        return Image                            # return PIL.Image
    except:
        logging.error(f'(!) PIL IMPORT FAILED: {format_exc()}')
        try:        # in the event of an error, attempt to restore backup if one exists
            if exists(backup_path):
                import shutil
                shutil.rmtree(old_path)
                os.rename(backup_path, old_path)
            elif not exists(old_path) and not exists(new_path):
                raise Exception('None of the following candidates for a PIL folder were found:'
                                f'\nOld: {old_path}\nNew: {new_path}\nBackup: {backup_path}')
        except NameError: pass              # NameError -> error occurred before the paths were even defined
        except:     # PIL is seemingly unrecoverable. hopefully this is extremely unlikely outside of user-tampering
            logging.critical(f'(!!!) COULD NOT RESTORE PIL FOLDER: {format_exc()}')
            logging.critical('\n\n  WARNING -- You may need to reinstall PyPlayer to restore snapshotting capabilities.'
                             '\n             If you cannot find the PIL folder within your installation, please report '
                             '\n             this error (along with this log file) on Github.\n')


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
    update_title_signal = QtCore.pyqtSignal()
    log_signal = QtCore.pyqtSignal(str)
    show_save_progress_signal = QtCore.pyqtSignal(bool)
    disable_crop_mode_signal = QtCore.pyqtSignal()
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
            'window': QtGui.QIcon(os.path.join(constants.RESOURCE_DIR, 'logo.ico')),
            'loop': QtGui.QIcon(os.path.join(constants.RESOURCE_DIR, 'loop.png')),
            'autoplay': QtGui.QIcon(os.path.join(constants.RESOURCE_DIR, 'autoplay.png')),
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
        self.frame_override: int = None
        self.open_queued = False
        self.swap_slider_styles_queued = False
        self.lock_progress_updates = False
        self.lock_spin_updates = False
        self.timer_id_resize_snap: int = None
        self.close_was_spontaneous = False
        self.was_maximized = False
        self.was_paused = False
        self.lock_fullscreen_ui = False
        self.menubar_visible_before_crop = False
        self.last_cycle_was_forward = True
        self.last_cycle_index: int = None

        self.video: str = None
        self.video_original_path: str = None
        self.recent_videos = []
        self.locked_video: str = None
        self.mime_type = 'image'    # defaults to 'image' since self.pause() is disabled for 'image' mime_types
        self.extension: str = None

        self.fractional_frame = 0.0
        self.delay = self.duration = 0
        self.frame_count = self.frame_rate = self.frame_rate_rounded = self.current_time = self.minimum = self.maximum = 1
        self.vwidth = self.vheight = 1000
        self.vsize = QtCore.QSize(1000, 1000)
        self.ratio = '0:0'

        self.last_amplify_audio_value = 100
        self.marked_for_deletion = set()
        self.shortcuts = None
        self.shortcut_bandaid_fix = False
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
        self.vlc.parent = self
        self.player = self.vlc.player                                        # this is a secondary alias for other files to use
        self.sliderProgress.parent = self
        self.sliderProgress.update_parent_progress = self.set_and_update_progress
        self.sliderVolume.keyPressEvent = self.keyPressEvent                 # pass sliderVolume key presses directly to GUI_Instance
        self.sliderVolume.keyReleaseEvent = self.keyReleaseEvent
        self.sliderProgress.cfg = self.dialog_settings
        self.sliderProgress.dragEnterEvent = self.vlc.dragEnterEvent         # reuse player's drag-and-drop code for slider
        self.sliderProgress.dropEvent = self.vlc.dropEvent
        self.dockControls.setTitleBarWidget(QtW.QWidget(self.dockControls))  # disables QDockWidget's unique titlebar
        self.dockControls.leaveEvent = self.leaveEvent                       # ensures leaving dockControls hides cursor/controls in fullscreen
        self.dockControls.resizeEvent = self.dockControlsResizeEvent         # ensures dockControls correctly hides/shows widgets in fullscreen
        self.frameAdvancedControls.setDragTarget(self)
        self.lineOutput.setIgnoreAll(False)

        for spin in (self.spinHour, self.spinMinute, self.spinSecond, self.spinFrame): spin.setProxyWidget(self)
        self.save_progress_bar.setMaximum(0)
        self.save_progress_bar.setMaximumHeight(16)
        self.save_progress_bar.setFormat('Saving...')
        self.save_progress_bar.setAlignment(Qt.AlignCenter)
        self.save_progress_bar.setSizePolicy(QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Expanding)
        self.save_progress_bar.hide()

        self.trim_mode_action_group = QtW.QActionGroup(self.menuTrimMode)
        for fade_action in (self.actionTrimAuto, self.actionTrimPrecise,
                            self.actionFadeBoth, self.actionFadeVideo, self.actionFadeAudio):
            self.trim_mode_action_group.addAction(fade_action)
        self.trim_mode_action_group.triggered.connect(self.set_trim_mode)

        self.frameProgress.contextMenuEvent = self.frameProgressContextMenuEvent
        self.buttonPause.contextMenuEvent = self.pauseButtonContextMenuEvent
        self.buttonTrimStart.contextMenuEvent = self.trimButtonContextMenuEvent
        self.buttonTrimEnd.contextMenuEvent = self.trimButtonContextMenuEvent
        self.buttonOpenMediaLocation.contextMenuEvent = self.openMediaLocationButtonContextMenuEvent
        self.buttonMarkDeleted.contextMenuEvent = self.buttonMarkDeletedContextMenuEvent
        self.buttonSnapshot.contextMenuEvent = self.buttonSnapshotContextMenuEvent
        self.menuRecent.contextMenuEvent = self.menuRecentContextMenuEvent
        self.buttonLoop.setIcon(self.icons['loop'])
        self.buttonAutoplay.setIcon(self.icons['autoplay'])

        # TODO: why isn't currentIndexChanged called when the config loads?
        self.gifPlayer.updateImageScale(self.dialog_settings.comboScaleArt.currentIndex())
        self.gifPlayer.updateArtScale(self.dialog_settings.comboScaleArt.currentIndex())
        self.gifPlayer.updateGifScale(self.dialog_settings.comboScaleGifs.currentIndex())
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
                    self.open(command, focus_window=self.dialog_settings.checkFocusDoubleClick.isChecked())
                    logging.info(f'(FS) Fast-start for {command} recieved and handled.')
        finally: self.fast_start_in_progress = False    # resume fast-start interface


    def fast_start_interface_thread(self):
        ''' Simple interface for detecting and reading cmd.txt files. Used for instantly playing new media upon double-click
            if we're already open (cmd.txt contains the path to the media) or closing in preparation for an update (cmd.txt
            contains the word "EXIT"). NOTE: Also used to auto-correct high-precision progress sliders, once every 5 seconds. '''
        cmdpath = os.path.join(constants.TEMP_DIR, f'cmd.{os.getpid()}.txt')  # the cmd.txt file with our PID to look for
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
                    if os.path.exists(cmdpath):
                        self.fast_start_in_progress = True
                        self.fast_start_open_signal.emit(cmdpath)
                        logging.info(f'(FS) CMD-file detected: {cmdpath}')
                        while self.fast_start_in_progress and not self.closed: sleep(0.05)
                        os.remove(cmdpath)                                    # delete cmd.txt if possible
                except: self.log(f'(!) FAST-START INTERFACE FAILED: {format_exc()}')
                finally: sleep(check_delay)

            # once every 5 seconds, check to make sure high-precision progress slider is maintaining accuracy
            if player.is_playing() and not self.lock_progress_updates and self.dialog_settings.checkHighPrecisionProgress.isChecked():
                vlc_frame = player.get_position() * self.frame_count          # get the frame VLC thinks it is
                next_frame = get_progess_slider() + 1 * self.playback_speed
                if abs(next_frame - vlc_frame) > self.frame_rate * 2:         # if our frame is way, WAY off (2+ seconds)...
                    true_frame = vlc_frame + (self.frame_rate * 0.3)          # reset to VLC's frame, +0.3 secs (VLC is usually 0.3-0.6 behind)
                    self.frame_override = true_frame
                    self.log('Warning: high-precision slider was desynced by >2 seconds. Corrected.')


    # ---------------------
    # >>> EVENTS <<<
    # ---------------------
    def event(self, event: QtCore.QEvent) -> bool:
        ''' A global event callback. Used to detect windowStateChange events,
            so we can save/remember the maximized state when necessary. '''
        if event.type() == WindowStateChange:       # alias used for speed
            if not (self.windowState() & Qt.WindowMinimized or self.windowState() & Qt.WindowFullScreen):
                self.was_maximized = bool(self.windowState() & Qt.WindowMaximized)
        return super().event(event)


    def closeEvent(self, event: QtGui.QCloseEvent):  # 'spontaneous' -> X-button pressed
        self.close_cancel_selected = False           # referenced in qtstart.exit()
        self.close_was_spontaneous = event.spontaneous()
        logging.info(f'Closing (spontaneous={event.spontaneous()}).')

        if self.marked_for_deletion:
            logging.info(f'The following files are still marked for deletion, opening prompt: {self.marked_for_deletion}')
            choice = self.show_delete_prompt()
            if choice == QtW.QMessageBox.Cancel:    # cancel selected, don't close
                self.close_cancel_selected = True   # required in case .close() was called from qtstart.exit()
                logging.info('Close cancelled.')
                return event.ignore()
            elif choice == QtW.QMessageBox.Yes:
                for file in self.marked_for_deletion:
                    try: os.remove(file)
                    except Exception as error: logging.warning(f'Error deleting file {file} - {type(error)}: {error}')

        #set_and_update_progress(0)
        self.stop()                                 # stop player
        self.dialog_settings.close()                # close settings dialog
        self.dockControls.setFloating(False)        # hide fullscreen UI if needed
        logging.info('Player has been stopped.')

        minimize_to_tray = self.dialog_settings.groupTray.isChecked() and self.dialog_settings.checkTrayClose.isChecked()
        force_close = self.close_was_spontaneous and not minimize_to_tray
        if force_close or self.tray_icon is None: qtstart.exit(self)
        else:
            if not cfg.minimizedtotraywarningignored:
                if self.close_was_spontaneous:      # only show message if closeEvent was called by OS (i.e. X button pressed)
                    self.tray_icon.showMessage('PyPlayer', 'Minimized to system tray')  # this emits messageClicked signal
                cfg.minimizedtotraywarningignored = True
            if self.dialog_settings.checkFirstFileTrayReset.isChecked():
                self.first_video_fully_loaded = False
            gc.collect(generation=2)
        return event.accept()


    def hideEvent(self, event: QtGui.QHideEvent):   # 'spontaneous' -> native minimize button pressed
        if event.spontaneous():
            if self.dialog_settings.checkMinimizePause.isChecked():
                self.was_paused = self.is_paused
                self.force_pause(True)
            elif self.dialog_settings.groupTray.isChecked() and self.dialog_settings.checkTrayMinimize.isChecked():
                self.close()                        # TODO these do not work with each other yet
        return super().hideEvent(event)


    def showEvent(self, event: QtGui.QShowEvent):   # 'spontaneous' -> restored by OS (e.g. clicked on taskbar icon)
        super().showEvent(event)

        # refresh VLC instance's winId
        if constants.PLATFORM == 'Windows': player.set_hwnd(self.vlc.winId())              # Windows
        elif constants.PLATFORM == 'Darwin': player.set_nsobject(int(self.vlc.winId()))    # MacOS
        else: player.set_xwindow(self.vlc.winId())                                         # Linux (sometimes)

        # strangely, closing/reopening the window applies an alignment to our QVideoPlayer/QWidget (very bad)
        self.gridLayout.setAlignment(self.vlc, Qt.Alignment())          # reset alignment to nothing

        s = self.dialog_settings
        if event.spontaneous():
            if not self.was_paused and s.checkMinimizePause.isChecked() and s.checkMinimizeRestore.isChecked():
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
        if not self.isMaximized():  # don't save position if we're currently maximized
            self.last_window_pos = event.oldPos()


    def resizeEvent(self, event: QtGui.QResizeEvent):
        if not self.isMaximized():  # don't save size if we're currently maximized
            self.last_window_size = event.oldSize()


    def dockControlsResizeEvent(self, event: QtGui.QResizeEvent):
        ''' Makes UI controls more compact as the size of the controls shrinks. '''
        width = event.size().width()
        self.frameQuickChecks.setVisible(width >= 528)                  # hide checkboxes at <= 500 pixels wide TODO this shouldn't be a frame, should it?
        self.lineOutput.setMinimumWidth(10 if width <= 380 else 120)    # reduce output lineEdit (but retain usability)
        self.advancedControlsLine.setVisible(width >= 357)              # hide aesthetic line-separator
        self.hlayoutQuickButtons.setSpacing(2 if width <= 394 else 6)   # reduce spacing between buttons
        self.buttonTrimStart.setMinimumWidth(32 if width <= 347 else 44)

        if width <= 335:            # hide trim/snapshot buttons, reduce quick-button spacing
            self.buttonTrimStart.setVisible(False)
            self.buttonTrimEnd.setVisible(False)
            self.buttonMarkDeleted.setVisible(False)
            self.buttonSnapshot.setVisible(False)
        else:                       # restore trim/snapshot buttons and quick-button spacing
            self.buttonTrimStart.setVisible(True)
            self.buttonTrimEnd.setVisible(True)
            self.buttonMarkDeleted.setVisible(True)
            self.buttonSnapshot.setVisible(True)


    def timerEvent(self, event: QtCore.QTimerEvent):
        ''' The base timeout event, used for adjusting the window's aspect ratio after a resize. '''
        if self.timer_id_resize_snap is not None:
            self.killTimer(self.timer_id_resize_snap)
            self.timer_id_resize_snap = None
            shrink = app.keyboardModifiers() & Qt.ShiftModifier         # TODO: would queryKeyboardModifiers be better?
            force_instant_resize = self.dialog_settings.checkSnapOnResize.checkState() == 0
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
            self.update_title_signal.emit()
        else: self.increment_volume(get_volume_scroll_increment() if add else -get_volume_scroll_increment())
        event.accept()


    def keyPressEvent(self, event: QtGui.QKeyEvent):    # TODO 3.10 match case
        key =  event.key()
        mod =  event.modifiers()
        text = event.text()

        # if a lineEdit has focus, ignore keypresses except for esc, which can be used to clear focus. spinboxes use QSpinBoxPassthrough
        editable = (self.lineOutput, self.lineCurrentTime)
        if any(w.hasFocus() for w in editable):
            if key == 16777216:                         # esc (clear focus)
                for widget in editable:                 # TODO there is a faster way to do this (by getting the current focus)
                    widget.clearFocus()
            return

        # this is a fix for QShortcuts not working in QSpinBoxPassthrough. it may or may not be changed in the future
        # https://stackoverflow.com/questions/10383418/qkeysequence-to-qkeyevent
        if self.shortcut_bandaid_fix:       # TODO like in widgets.py, this had "and text" on it. why?
            true = QtGui.QKeySequence(event.modifiers() | event.key())
            for primary, secondary in self.shortcuts.values():
                if primary.key() == true or secondary.key() == true:
                    primary.activated.emit()
        self.shortcut_bandaid_fix = False

        # handle individual keys. TODO: change these to their enums? (70 -> Qt.Key.Key_F)
        if key == 16777216 and self.actionFullscreen.isChecked(): self.actionFullscreen.trigger()   # esc (fullscreen only)

        # emulate menubar shortcuts when menubar is not visible (which disables shortcuts for some reason)
        elif not self.menubar.isVisible():
            if mod & Qt.ControlModifier:
                if key == 79: self.actionOpen.trigger()                     # ctrl + o (open)
                elif key == 83:
                    if mod & Qt.ShiftModifier: self.actionSaveAs.trigger()  # ctrl + shift + s (save as)
                    else: self.actionSave.trigger()                         # ctrl + s (save)
            elif mod & Qt.AltModifier:
                if key == 81: self.actionExit.trigger()                     # alt + q (exit)
        logging.debug(f'PRESSED key={key} mod={int(mod)} text="{text}"')


    def keyReleaseEvent(self, event: QtGui.QKeyEvent):                      # 3.10 match case
        editable = (self.lineOutput, self.lineCurrentTime, self.spinHour, self.spinMinute, self.spinSecond, self.spinFrame)
        if any(w.hasFocus() for w in editable): return                      # TODO

        key = event.key()
        if key == 16777251 and not self.vlc.dragdrop_in_progress:           # alt (ignore this if we're dragging files since alt affects that)
            self.actionShowMenuBar.trigger()                                # manually trigger actions to keep the menus & widgets consistent
        else: super().keyReleaseEvent(event)
        logging.debug(f'RELEASED key={key} text="{event.text()}"')


    def contextMenuEvent(self, event: QtGui.QContextMenuEvent):             # should these use QWidget.actions() instead of contextMenuEvent?
        ''' Handles creating the context menu (right-click) for the main window. '''
        context = QtW.QMenu(self)
        if self.actionCrop.isChecked(): context.addAction(self.actionCrop)
        context.addAction(self.actionStop)
        context.addMenu(self.menuWindow)
        context.addSeparator()
        context.addSeparator()
        context.addAction(self.actionSettings)
        context.addAction(self.actionLoop)
        context.addAction(self.actionAutoplay)
        context.addSeparator()
        context.addMenu(self.menuFile)
        context.addMenu(self.menuEdit)
        context.addMenu(self.menuVideo)
        context.addMenu(self.menuAudio)
        context.addMenu(self.menuHelp)
        context.exec(event.globalPos())


    def frameProgressContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        precision_action = QtW.QAction(self.dialog_settings.checkHighPrecisionProgress.text())
        precision_action.setCheckable(True)
        precision_action.setChecked(self.dialog_settings.checkHighPrecisionProgress.isChecked())
        precision_action.setToolTip(self.dialog_settings.checkHighPrecisionProgress.toolTip())
        precision_action.toggled.connect(self.dialog_settings.checkHighPrecisionProgress.setChecked)

        context = QtW.QMenu(self)
        context.setToolTipsVisible(True)
        context.addAction(precision_action)
        context.exec(event.globalPos())


    def pauseButtonContextMenuEvent(self, event: QtGui.QContextMenuEvent):  # should these use QWidget.actions() instead of contextMenuEvent?
        context = QtW.QMenu(self)
        context.addAction(self.actionStop)
        context.addAction('Restart', set_and_update_progress)          # TODO this might have timing issues with update_thread
        context.exec(event.globalPos())


    def trimButtonContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles creating the context menu (right-click) for the start/end trim buttons. Includes
            the fade-mode menu, actions for instantly setting new start/end positions, and disabled
            (grayed out) actions containing information about the current start/end positions. '''
        if not self.video: return       # do not render context menu if no media is playing

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

        # actions for force-setting start/end times
        set_start_action = QtW.QAction('Set &start to current position', self)
        set_start_action.triggered.connect(lambda: self.set_trim_start(force=True))
        set_end_action = QtW.QAction('Set &end to current position', self)
        set_end_action.triggered.connect(lambda: self.set_trim_end(force=True))

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
        ''' Handles creating the context menu (right-click) for the open media location button. '''
        if not self.video: return       # do not render context menu if no media is playing
        context = QtW.QMenu(self)
        context.addAction(self.actionOpenMediaLocation)
        context.addAction(self.actionCopyMediaLocation)
        context.exec(event.globalPos())


    def buttonMarkDeletedContextMenuEvent(self, event: QtGui.QContextMenuEvent):    # should these use QWidget.actions() instead of contextMenuEvent?
        ''' Handles creating the context menu (right-click) for buttonMarkDeleted. Due to the uniqueness of
            each context menu, contextMenuEvent is replaced directly instead of subclassing the entire widget. '''
        context = QtW.QMenu(self)
        context.setToolTipsVisible(True)
        context.addAction(self.actionMarkDeleted)
        context.addAction(self.actionClearMarked)
        context.addAction(self.actionShowDeletePrompt)
        context.addSeparator()
        context.addAction(self.actionDeleteImmediately)
        context.exec(event.globalPos())


    def buttonSnapshotContextMenuEvent(self, event: QtGui.QContextMenuEvent):       # should these use QWidget.actions() instead of contextMenuEvent?
        ''' Handles creating the context menu (right-click) for buttonSnapshot. Due to the uniqueness of
            each context menu, contextMenuEvent is replaced directly instead of subclassing the entire widget. '''
        def explore_last_screenshot():
            if not os.path.exists(cfg.last_snapshot_path): return self.log(f'Previous snapshot at {cfg.last_snapshot_path} no longer exists.')
            else: qthelpers.openPath(cfg.last_snapshot_path, explore=True)

        open_action1 = QtW.QAction('Open last snapshot (&PyPlayer)')
        open_action1.triggered.connect(lambda: self.snapshot(modifiers=Qt.ControlModifier))
        open_action2 = QtW.QAction('Open last snapshot (&default)')
        open_action2.triggered.connect(lambda: self.snapshot(modifiers=Qt.AltModifier))
        explore_action = QtW.QAction('&Explore last snapshot')
        explore_action.triggered.connect(explore_last_screenshot)

        context = QtW.QMenu(self)
        context.addAction(open_action1)
        context.addAction(open_action2)
        context.addAction(explore_action)
        context.addSeparator()
        context.addAction(self.actionQuickSnapshot)         # quick snapshot action
        context.addAction(self.actionSnapshot)              # regular snapshot action
        context.exec(event.globalPos())


    def menuRecentContextMenuEvent(self, event: QtGui.QContextMenuEvent):
        ''' Handles context menus for individual recent files. '''
        action = self.menuRecent.actionAt(event.pos())
        if action is self.actionClearRecent or not action: return
        path = action.toolTip()

        explore_action = QtW.QAction('M&edia location')
        explore_action.triggered.connect(lambda: self.explore_media_location(path))
        copy_action = QtW.QAction('&Copy media path')
        copy_action.triggered.connect(lambda: self.copy_media_location(path))
        remove_action = QtW.QAction('&Remove from recent files')
        remove_action.triggered.connect(lambda: (self.recent_videos.remove(path), self.refresh_recent_menu()))

        context = QtW.QMenu(self)
        context.addAction(remove_action)
        context.addSeparator()
        context.addAction(explore_action)
        context.addAction(copy_action)
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
                with open(os.path.join(constants.THEME_DIR, filename)) as theme_file:
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
        comboThemes = self.dialog_settings.comboThemes
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
            self.dialog_settings.comboThemes.setToolTip('No theme is currently selected.')
            config.cfg.theme = 'None'
        else:
            try:
                stylesheet = theme['stylesheet']
                self.setStyleSheet(stylesheet)
                self.dialog_settings.comboThemes.setToolTip(theme['description'])
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
    def cycle_media(self, *args, next: bool = True, ignore: tuple = tuple()):   # *args to capture unused signal args
        ''' Cycles through the current media's folder and looks for the `next`
            or previous openable, non-hidden file that isn't in the `ignore`
            list. If there are no other openable files, nothing happens.
            Otherwise, the new file is opened and returned. '''
        if self.video is None: return self.statusbar.showMessage('No media is playing.', 10000)    # TODO remember last media's folder?
        logging.info(f'Getting {"next" if next else "previous"} media file...')

        base_file = self.video_original_path if self.dialog_settings.checkCycleRememberOriginalPath.checkState() else self.video
        current_dir, current_media = os.path.split(os.path.abspath(base_file))
        files = os.listdir(current_dir)
        if len(files) == 1: return self.log('This is the only file in this folder.')

        self.last_cycle_was_forward = next
        if current_media in files: original_index = files.index(current_media)
        elif self.last_cycle_index is not None: original_index = self.last_cycle_index
        else:           # video was moved/renamed and never cycled, use human sorting to roughly determine where to start from
            import re   # https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
            test = lambda char: int(char) if char.isdigit() else char   # NOTE: Most OS's do not actually use pure human sorting
            human_sort = lambda string: [test(c) for c in re.split(r'(\d+)', os.path.splitext(string)[0])]
            restored_files = files.copy()
            restored_files.append(current_media)
            restored_files.sort(key=human_sort)
            original_index = max(0, min(len(files), restored_files.index(current_media)) - 1)

        skip_marked = self.checkSkipMarked.isChecked()
        if next: file_range = range(original_index + 1, len(files) + original_index + 1)
        else: file_range = range(original_index - 1, original_index - len(files) - 1, -1)
        for index in file_range:
            index = index % len(files)

            # if we've reached the original file or the new video opens successfully -> stop
            file = os.path.abspath(os.path.join(current_dir, files[index]))
            logging.debug(f'Checking {file} at index #{index}')

            # check for reasons we might skip a given file (from most to least likely)
            if os.path.isdir(file): continue
            if file_is_hidden(file): continue
            if file in ignore: continue
            if skip_marked and file in self.marked_for_deletion: continue
            if file == base_file: continue

            # get mime type of file to verify this is actually playable and skip the extra setup done in open()
            try:
                mime, extension = filetype.guess(file).mime.split('/')
                if mime not in ('video', 'image', 'audio'): continue
            except: continue

            # attempt to play file -> -1 is returned if file can't be opened
            if self.open(file, _from_cycle=True, mime=mime, extension=extension) != -1:
                self.last_cycle_index = index
                return file
        return self.log('This is the only playable media file in this folder.')


    def explore_media_location(self, path: str = None):
        ''' Opens `path` (or self.video if not provided) in the default
            file explorer, with `path` pre-selected if possible. '''
        if not path: path = self.video if self.video else cfg.lastdir
        if not os.path.exists(path):
            if path in self.recent_vidoes:
                self.recent_videos.remove(path)
            return self.log(f'Recent file "{path}" no longer exists.')
        else: qthelpers.openPath(path, explore=True)


    def copy_media_location(self, path: str = None):
        ''' Copies `path` (or self.video if not provided) to the clipboard,
            surrounded by quotes and with backslashes escaped (if desired). '''
        if not path: path = self.video if self.video else cfg.lastdir
        if not os.path.exists(path):
            if path in self.recent_vidoes:
                self.recent_videos.remove(path)
            return self.log(f'Recent file "{path}" no longer exists.')
        else:
            if self.dialog_settings.checkCopyEscapeBackslashes.isChecked():
                sep = '\\'
                escaped_sep = r'\\'
                app.clipboard().setText(f'"{path.replace(sep, escaped_sep)}"')
            else: app.clipboard().setText(f'"{path}"')


    def parse_media_file(self, file, probe_file=None, mime='video', extension=None, data=None):
        ''' Parses a media file for relevant metadata and emits _open_signal.
            This *could* be simpler, but it still needs to be fast.
            The following properties should be set by this function:
                - self.mime
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
                            while not os.path.exists(probe_file): pass
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
                            logging.debug(f'FFprobe for {file}:\n{data}')
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
                            else: mime = 'audio'    # the rare for-else-loop (else only happens if we don't break). audio streams usually report 0/0
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
                            if cover_art:
                                gif_player.play(cover_art)          # cover art is bytes -> set to gif_player's QPixmap, open QPixmap with PIL
                                self.vwidth, self.vheight = get_PIL_Image().fromqpixmap(gif_player.art).size
                            else:
                                self.vwidth = 16
                                self.vheight = 9
                            duration = tag.duration
                        except:                                     # TinyTag is lightweight but cannot handle everything
                            import music_tag                        # only import music_tag if we absolutely need to
                            tag = music_tag.load_file(file)
                            if 'artwork' in tag:
                                art = tag['artwork'].first
                                gif_player.play(art.data)           # art.data is bytes -> set to gif_player's QPixmap
                                self.vwidth = art.width             # music_tag directly reports width/height of artwork
                                self.vheight = art.height
                            else:
                                self.vwidth = 16
                                self.vheight = 9
                            duration = tag['#length'].value
                        #gif_player.pixmap().save(os.path.join(constants.TEMP_DIR, f'{os.path.basename(file)}_{os.path.getctime(file)}.png'))
                    except:                                         # this is to handle things that wrongly report as audio, like .ogv files
                        logging.info(f'Invalid audio file detected, parsing as a video file... {format_exc()}')
                        if probe_file:
                            start = get_time()
                            while not os.path.exists(probe_file): pass
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
                if extension == 'gif':
                    mime = 'video'
                    gif = gif_player.gif
                    self.frame_count = gif.frameCount()
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
                        self.delay = gif.nextFrameDelay() / 1000
                        self.duration = self.frame_count * self.delay
                        self.frame_rate = 1 / self.delay
                        self.frame_rate_rounded = round(self.frame_rate)
                        size = gif.frameRect().size()
                        self.vwidth, self.vheight = size.width(), size.height()
                    self.ratio = get_aspect_ratio(self.vwidth, self.vheight)
                else:
                    self.duration = 0.0000001       # low duration to avoid errors but still show up as 0 on the UI
                    self.frame_count = 1
                    self.frame_rate = 1
                    self.frame_rate_rounded = 1
                    try: self.vwidth, self.vheight = get_PIL_Image().open(file).size
                    except AttributeError: self.vwidth, self.vheight = 1, 1
                    self.ratio = get_aspect_ratio(self.vwidth, self.vheight)
                    self.delay = 0.2                # run update_slider_thread only 5 times/second

            assert self.duration != 0, f'File \'{file}\' appears to be corrupted or an invalid format and cannot be opened (invalid duration).'
        except:
            logging.error(format_exc())
            return -1

        # extra setup. frame_rate_rounded, ratio, and delay could all be set here, but it would be slower overall
        self.video = file                           # set media AFTER opening but BEFORE _open_signal
        self.mime_type = mime
        if base_mime == 'image':
            self._open_signal.emit()                # manually emit _open_signal for images/gifs (slider thread will be idle)
        else:
            self.open_queued = True
            self.frame_override = 0                 # set frame_override to trigger open_queue in update_slider_thread
        self.extension = extension
        if mime != 'audio': self.vlc.find_true_borders()


    def open(self, file=None, focus_window=True, update_recent_list=True, remember_old_file=False,
             mime=None, extension=None, _from_cycle=False, _from_dir=False):
        ''' Current iteration: IV '''
        try:
            if not _from_cycle:                     # assume that this is already sorted out if called from cycle
                if not file: file, cfg.lastdir = qthelpers.browseForFile(cfg.lastdir, 'Select media file to open')
                if not file or file == self.locked_video: return
                file = os.path.abspath(file)
                start = get_time()

                # if `file` is actually a directory -> open first valid, non-hidden file and enable Autoplay
                if os.path.isdir(file):
                    if _from_dir: return -1         # avoid recursively opening directories
                    for filename in os.listdir(file):
                        path = os.path.join(file, filename)

                        if not file_is_hidden(path) and self.open(path, _from_dir=True) != -1:
                            self.actionAutoplay.setChecked(True)
                            self.log(f'Opened {filename} from folder {file} and enabled Autoplay.')
                            return
                    else: return self.log(f'No files in {file} were playable.')
            else: start = get_time()

        # --- Probing file and determining mime type ---
            # probe file with FFprobe if possible. if file has already been probed, reuse old probe. otherwise, save output to txt file
            # probing calls Popen through a Thread (faster than calling Popen itself or using Thread on a middle-ground function)
            probe_data = None
            if FFPROBE:                             # generate probe file's path and check if it already exists
                probe_file = os.path.join(constants.PROBE_DIR, f'{os.path.basename(file)}_{os.path.getctime(file)}.txt')
                if os.path.exists(probe_file):      # probe file already exists
                    with open(probe_file, 'r') as f:
                        try:
                            probe_data = json.load(f)   # parse pre-existing probe file and check if listed size is correct
                            if int(probe_data['format']['size']) == os.path.getsize(file):
                                logging.info('Reusing previously parsed metadata.')
                            else:
                                Thread(target=subprocess.Popen, args=(f'{FFPROBE} -show_format -show_streams -of json "{file}" > "{probe_file}"',), kwargs=dict(shell=True)).start()
                                logging.info('Previously parsed metadata is now out-of-date. Re-probing with FFprobe.')
                        except:
                            try: os.remove(probe_file)
                            except: logging.warning('FAILED TO DELETE PROBE FILE: ' + probe_file)
                            Thread(target=subprocess.Popen, args=(f'{FFPROBE} -show_format -show_streams -of json "{file}" > "{probe_file}"',), kwargs=dict(shell=True)).start()
                else: Thread(target=subprocess.Popen, args=(f'{FFPROBE} -show_format -show_streams -of json "{file}" > "{probe_file}"',), kwargs=dict(shell=True)).start()
            else: probe_file = None                 # no FFprobe -> no probe file (even if one exists already)

            # get mime type of file (if called from cycle, then this part was worked out beforehand)
            if mime is None:
                try:
                    filetype_data = filetype.guess(file)    # 'EXTENSION', 'MIME', 'extension', 'mime'
                    mime, extension = filetype_data.mime.split('/')
                    if mime not in ('video', 'image', 'audio'):
                        self.log(f'File \'{file}\' appears to be corrupted or an invalid format and cannot be opened (invalid mime type).')
                        return -1
                except:
                    if not os.path.exists(file): self.log(f'File \'{file}\' does not exist.')
                    else: self.log(f'File \'{file}\' appears to be corrupted or an invalid format and cannot be opened (failed to determine mime type).')
                    return -1                       # ^^^ .guess() errors out in rare circumstances ^^^

        # --- Restoring window ---
            # restore window from tray if hidden, otherwise there's a risk for unusual VLC output
            if not self.isVisible():                # we need to do this even if focus_window is True
                was_minimzed_to_tray = True
                self.resize(self.last_window_size)  # restore size/pos or maximized windows will forget...
                self.move(self.last_window_pos)     # ...their original geometry when you unmaximize them
                self.showMinimized()                # minimize for now, we'll check if we need to focus later
            else: was_minimzed_to_tray = False

        # --- Playing media ---
            # attempt to play media
            if mime == 'image':
                gif_player.play(file, gif=extension == 'gif')
                player.stop()
            elif not self.vlc.play(file): return    # immediately attempt to play media once we know it might be valid
            else: gif_player.play(None)             # clear gifPlayer if vlc successfully played media

        # --- Parsing metadata and setting up UI/recent files list ---
            # parse non-video files and show/log file on statusbar
            parsed = False                          # keep track of parse so we can avoid re-parsing it later if it ends up being a video
            if mime != 'video':                     # parse metadata early if it isn't a video
                if self.parse_media_file(file, probe_file, mime, extension, probe_data) == -1:
                    self.log(f'File \'{file}\' appears to be corrupted or an invalid format and cannot be opened (non-video parsing failed).')
                    return -1
                parsed = True
            logging.info('--- OPENING FILE ---')
            self.log(f'Opening file ({mime}/{extension}): {file}')

            # misc cleanup/setup for new media
            self.operations = {}
            self.sliderProgress.setEnabled(mime != 'image' or extension == 'gif')   # static images have odd but harmless behavior
            self.buttonTrimStart.setChecked(False)
            self.buttonTrimEnd.setChecked(False)
            self.lineOutput.setText('')
            self.lineOutput.setPlaceholderText(os.path.basename(file))
            self.lineOutput.setToolTip(f'{file}\nEnter a new name and press enter to rename this file.')

            # update delete-action's QToolButton
            is_marked = file in self.marked_for_deletion
            self.actionMarkDeleted.setChecked(is_marked)
            self.buttonMarkDeleted.setChecked(is_marked)

            # reset cropped mode if needed
            if self.actionCrop.isChecked(): self.disable_crop_mode()    # set_crop_mode auto-returns if mime_type is 'audio'

            # extra setup before we absolutely must wait for the media to finish parsing
            self.is_paused = False                  # force_pause could be used here, but it is slightly more efficient this way
            set_pause_button_text('𝗜𝗜')
            if not self.first_video_fully_loaded: self.set_volume(get_volume_slider())  # force volume to quickly correct gain issue
            self.lineOutput.clearFocus()            # clear focus from output line so it doesn't interfere with keyboard shortcuts

            # focus window. if disabled but window is minimized, check for special focus settings. ignore Autoplay focus if desired.
            if not self.isActiveWindow() and not (_from_cycle and self.dialog_settings.checkIgnoreFocusWithAutoplay.isChecked()):
                if not focus_window:
                    if self.isMinimized():
                        if was_minimzed_to_tray:    # check appropriate setting based on our original minimize state
                            if self.dialog_settings.checkFocusMinimizedToTray.isChecked(): focus_window = True
                        elif self.dialog_settings.checkFocusMinimized.isChecked(): focus_window = True
                if focus_window: qthelpers.showWindow(self)

            # if presumed to be a video -> finish VLC's parsing (done as late as possible to minimize downtime)
            if mime == 'video' and not parsed:
                if self.parse_media_file(file, probe_file, mime, extension, probe_data) == -1:        # parse metadata from VLC
                    self.log(f'File \'{file}\' appears to be corrupted or an invalid format and cannot be opened (video parsing failed).')
                    return -1

            if not remember_old_file or not self.video_original_path: self.video_original_path = file

            # update recent media list
            if update_recent_list:
                recent_videos = self.recent_videos
                if file in recent_videos:
                    recent_videos.append(recent_videos.pop(recent_videos.index(file)))
                else:
                    recent_videos.append(file)
                    if len(recent_videos) > 10:     # do NOT use the recent_videos alias here
                        self.recent_videos = self.recent_videos[-10:]

            # update marquee size and offset relative to media's dimensions
            player.video_set_marquee_int(VideoMarqueeOption.Size, int(self.vheight * self.vlc.text_height_percent))
            player.video_set_marquee_int(VideoMarqueeOption.X, int(self.vheight * self.vlc.text_x_percent))
            player.video_set_marquee_int(VideoMarqueeOption.Y, int(self.vheight * self.vlc.text_y_percent))

            # update UI with new media's duration
            h, m, s, ms = get_hms(self.duration)
            self.labelMaxTime.setText(f'{m:02}:{s:02}.{ms:02}' if self.duration < 3600 else f'{h}:{m:02}:{s:02}')
            self.spinHour.setEnabled(h != 0)        # spinSecond does not need to be adjusted here
            self.spinMinute.setEnabled(m != 0)
            self.spinHour.setMaximum(h)
            self.spinMinute.setMaximum(m)
            self.spinFrame.setMaximum(self.frame_count)
            self.spinFrame.setPrefix(f'{self.frame_rate_rounded} FPS: ')

            logging.info(f'Initial media opening completed after {get_time() - start:.4f} seconds.')
        except: self.log(f'(!) OPEN FAILED: {format_exc()}')


    def _open(self):
        ''' NOTE: Not intended to be called manually. A slot for _open_signal which handles updating the progress slider's attributes.
            This is done here so that the progress bar updates in a uniform and quick manner as update_slider_thread must be used to
            reset the progress regardless, or we'll experience timing issues that cause newly opened media to play from the frame
            the previous media left off at. Putting ALL of open() in this slot, however, results in a noticable delay when opening
            media. Non-essential actions - emitting update_title_signal and displaying a marquee - are handled here as well. '''
        try:
            self.sliderProgress.setMaximum(self.frame_count)
            update_progress(0)
            self.minimum = self.sliderProgress.minimum()
            self.maximum = self.sliderProgress.maximum()
            self.sliderProgress.setTickInterval(self.frame_rate_rounded * (1 if self.duration < 3600 else 60))  # place one tick per second/minute (default theme)
            self.sliderProgress.setPageStep(int(self.frame_count / 10))

            self.vsize.setWidth(self.vwidth)
            self.vsize.setHeight(self.vheight)
            if self.is_snap_mode_enabled():
                resize_on_open_state = self.dialog_settings.checkResizeOnOpen.checkState()
                snap_on_open_state = self.dialog_settings.checkSnapOnOpen.checkState()
                if resize_on_open_state and not (resize_on_open_state == 1 and self.first_video_fully_loaded):      # 1 -> only resize first video opened
                    self.snap_to_native_size()
                elif snap_on_open_state and not (snap_on_open_state == 1 and self.first_video_fully_loaded):
                    self.snap_to_player_size(force_instant_resize=True)
                elif self.dialog_settings.checkClampOnOpen.isChecked():
                    qthelpers.clampToScreen(self)   # clamping enabled but snap/resize is disabled
            elif self.dialog_settings.checkClampOnOpen.isChecked():
                qthelpers.clampToScreen(self)       # clamping enabled but snap/resize is disabled for this media

            self.update_title_signal.emit()
            if self.dialog_settings.checkTextOnOpen.isChecked(): show_text(os.path.basename(self.video), 1000)
            if not self.dialog_settings.checkAutoEnableSubtitles.isChecked(): player.video_set_spu(-1)
            self.first_video_fully_loaded = True

            logging.info(f'Metadata: duration={self.duration}, fps={self.frame_rate} ({self.frame_rate_rounded}), frames={self.frame_count}, size={self.vwidth}x{self.vheight}, ratio={self.ratio}, delay={self.delay:.6f}')
            logging.info('--- OPENING COMPLETE ---\n')
            gc.collect(generation=2)            # do manual garbage collection after opening (NOTE: this MIGHT be risky)
        except: logging.error(f'(!) OPEN-SLOT FAILED: {format_exc()}')


    def restart(self):
        ''' Restarts media after it is finished playing to circumvent a strange design choice in libvlc which renders
            finished media unusable. While simple now, it took a LOT of experimentation, refactoring, and 5 iterations
            to reach this point. Called automatically as a callback through the MediaPlayerEndReached event <widgets.py>.
            If --play-and-exit is specified, program exits. '''
        try:
            logging.info('Restarting VLC media (Restart V)')
            if self.actionLoop.isChecked():     # if we want to loop, reload video, reset UI, and return immediately
                self.vlc.play(self.video)
                return update_progress(0)
            if self.actionAutoplay.isChecked():
                update_progress(0)              # TODO required due to the audio issue side-effect (I think) -> 1st video file after audio file ends instantly
                return self.cycle_media()       # if we want autoplay, don't reload video -> cycle immediately
            if self.dialog_settings.checkStopOnFinish.isChecked() and player.get_state() != State.Stopped:
                return self.stop()

            self.vlc.play(self.video)                                   # reload video in VLC
            frame = self.frame_count
            set_player_position((frame - 2) / frame)                    # reset VLC player position (-2 frames to ensure visual update)
            update_progress_signal.emit(frame)                          # ensure UI snaps to final frame
            self.restarted = True

            if qtstart.args.play_and_exit:      # force-close if requested. this is done here so as to slightly optimize normal restarts
                logging.info('Play-and-exit requested. Closing.')
                return qtstart.exit(self)

            while player.get_state() == State.Ended: sleep(0.005)       # wait for VLC to update the player state
            self.force_pause(True, '⟳')                                # forcibly re-pause VLC
            if self.isFullScreen() and self.dialog_settings.checkFullScreenMediaFinishedLock.isChecked():
                self.lock_fullscreen_ui = True  # indicate we've restarted in fullscreen by showing the UI (marquee doesn't work -> player is stopped)
                self.timer_fullscreen_media_ended = QtCore.QTimer(self, interval=500, timeout=self.timerFullScreenMediaEndedEvent)
                self.timer_fullscreen_media_ended.start()
            else: show_text('')                                         # VLC will auto-show last marq text everytime it restarts
            self.first_video_fully_loaded = True                        # ensure this is True (it resets depending on settings)
        except: logging.error(f'(!) RESTART FAILED: {format_exc()}')


    def pause(self):
        ''' Pauses/unpauses the media. Handles updating GUI, cleaning
            up/restarting, clamping progress to current trim, displaying
            the pause state on-screen, wrapping around the progress bar. '''
        if self.mime_type == 'image': return
        if self.extension == 'gif':             # check if gif's filename is correct. if not, restart the gif and restore position
            old_state = gif_player.gif.state()
            was_paused = old_state != QtGui.QMovie.Running
            if was_paused and os.path.abspath(gif_player.gif.fileName()) != gif_player.filename:
                gif_player.gif.setFileName(gif_player.filename)             # ^ .fileName() is formatted wrong -> fix with abspath()
                set_gif_position(get_progess_slider())
            gif_player.gif.setPaused(not was_paused)
            self.is_paused = not was_paused
            frame = gif_player.gif.currentFrameNumber()
        else:
            frame = get_progess_slider()
            old_state = player.get_state()
            if old_state == State.Stopped:
                self.restart()
                set_and_update_progress(frame)

            if frame >= self.maximum or frame <= self.minimum:              # play media from beginning if media is over
                self.lock_progress_updates = True
                set_and_update_progress(self.minimum)
                self.lock_progress_updates = False
            player.pause()                                                  # actually pause VLC player
            self.is_paused = True if old_state == State.Playing else False  # prevents most types of pause-bugs...?

        pause_text = '▶' if self.is_paused else '𝗜𝗜'                         # ▷ ▶ ⏵︎
        set_pause_button_text(pause_text)
        if self.dialog_settings.checkTextOnPause.isChecked(): show_text(pause_text)
        self.update_title_signal.emit()

        self.restarted = False
        logging.debug(f'Pausing: is_paused={self.is_paused} old_state={old_state} frame={frame} max-frame={self.maximum}')
        return self.is_paused


    def force_pause(self, paused: bool, text=None):
        player.set_pause(paused)
        gif_player.gif.setPaused(paused)
        self.is_paused = paused
        set_pause_button_text(text if text is not None else '▶' if paused else '𝗜𝗜')
        self.update_title_signal.emit()
        logging.debug(f'Force-pause: paused={paused} text={text}')
        return self.is_paused


    def stop(self):
        ''' A more robust way of stopping - stop the player while also force-pausing. '''
        player.stop()
        gif_player.gif.setFileName('')
        self.force_pause(True)


    def get_renamed_output(self, new_name: str = None):
        ''' Returns `new_name` or self.lineOutput as a valid, sanitized, unique path.
            If `new_name` ends up being the same as self.video, no media is playing,
            or `new_name` and self.lineOutput are both blank, then None is returned. '''
        if not self.video or (not new_name and not self.lineOutput.text().strip()): return None
        try:
            old_oscwd = os.getcwd()
            os.chdir(os.path.dirname(self.video))       # set os module's CWD to self.video's folder -> allows things like abspath, '.', and '..'

            dirname, basename = os.path.split(new_name or self.lineOutput.text().strip())
            new_name = os.path.abspath(os.path.join(dirname, sanitize(basename)))
            if not os.path.splitext(new_name)[-1]: new_name = f'{new_name}{os.path.splitext(self.video)[-1]}'   # append extension if needed
            if new_name == self.video: return None      # make sure new name isn't the same as the old name
            return get_unique_path(new_name)            # TODO make this a setting (use os.replace instead of renames)
        finally: os.chdir(old_oscwd)                    # reset os module's CWD before returning


    def rename(self, new_name: str = None):
        ''' Renames the current media to `new_name`. If `new_name` is blank,
            self.lineOutput is used. See get_renamed_output() for details. '''
        new_name = self.get_renamed_output(new_name)
        if new_name is None: return                     # get_renamed_output failed to create a valid output path
        was_paused = self.is_paused
        self.stop()                                     # player must be stopped before we can rename
        try:
            try:
                os.renames(self.video, new_name)
                self.log_on_player(f'File renamed to {new_name}', 2500, marq_key='Save')
            except FileNotFoundError:                   # images are cached so they can be altered behind the scenes
                if self.dialog_settings.checkRenameMissingImages.isChecked():
                    gif_player.art.save(new_name)
                    self.log('Current file no longer exists, so a renamed copy was created.')
                else: return self.log('Current file no longer exists.')
            self.video = new_name
            self.lineOutput.setText('')                 # clear lineedit after successful rename (same as in open())
            self.lineOutput.setPlaceholderText(os.path.basename(new_name))
            self.lineOutput.setToolTip(f'{new_name}\nEnter a new name and press enter to rename this file.')
            self.update_title_signal.emit()
        except: self.log(f'RENAME FAILED: {format_exc()}')

        # replay the media and restore position (no need for full-scale open())
        if self.extension == 'gif':
            gif_player.gif.setFileName(new_name)
            set_gif_position(get_progess_slider())
            if not was_paused: self.force_pause_signal.emit(False)          # we have to do this and this must be a signal
            gif_player.filename = new_name
        elif self.mime_type != 'image':
            self.vlc.play(self.video)
            set_player_position(get_progess_slider() / self.frame_count)    # set VLC back to current position
        self.recent_videos[-1] = self.video                                 # update recent video's list with new name


    def delete(self, files):
        if isinstance(files, str): files = (files,)
        if self.video in files:                         # cycle media before deleting if current video is about to be deleted
            if self.extension == 'gif': self.stop()     # gif_player's QMovie must have its filename changed to unlock it
            old_file = self.video                       # self.video will likely change after media is cycled
            new_file = self.cycle_media(next=self.last_cycle_was_forward, ignore=files)
            if new_file is None or new_file == old_file:
                self.stop()                             # media wasn't cycled -> stop player and uncheck deletion button
                self.actionMarkDeleted.setChecked(False)
                self.buttonMarkDeleted.setChecked(False)
                self.log('There are no remaining files to play.')

        recycle = self.dialog_settings.checkRecycleBin.isChecked()
        verb = 'recycl' if recycle else 'delet'
        if recycle: import send2trash
        logging.info(f'{verb.capitalize()}ing {len(files)} files...')

        for file in files:
            try:
                send2trash.send2trash(file) if recycle else os.remove(file)
                logging.info(f'File {file} {verb}ed successfully.')
            except Exception as error: self.log(f'File could not be deleted: {file} - {error}')
            if not os.path.exists(file):    # if file doesn't exist, unmark file (even if error occurred)
                if file in self.recent_videos: self.recent_videos.remove(file)
                if file in self.marked_for_deletion: self.marked_for_deletion.remove(file)


    def save_as(self, *args, caption='Save media as...', filter='MP4 files (*.mp4);;MP3 files (*.mp3);;WAV files (*.wav);;AAC files (*.aac);;All files (*)'):
        if not self.video: return self.statusbar.showMessage('No media is playing.', 10000)
        Thread(target=self._save_as, args=(caption, filter), daemon=True).start()


    def save(self, *args, dest=None, ext_hint=None):    # *args to capture unused signal args
        if not self.video: return self.statusbar.showMessage('No media is playing.', 10000)
        Thread(target=self._save, args=(dest, ext_hint), daemon=True).start()


    def _save_as(self, caption='Save media as...', filter='MP4 files (*.mp4);;MP3 files (*.mp3);;WAV files (*.wav);;AAC files (*.aac);;All files (*)'):
        ''' Trim and save to a specified path. '''
        logging.info('Opening \'Save As...\' dialogue.')
        starting_name = self.video if self.dialog_settings.checkSaveAsUseMediaFolder.isChecked() else os.path.join(cfg.lastdir, os.path.basename(self.video))
        file, cfg.lastdir = qthelpers.saveFile(lastdir=get_unique_path(starting_name),
                                               caption=caption,
                                               filter=filter,
                                               selectedFilter='All files (*)' if 'All files (*)' in filter else '')     # TODO this is a temporary change until all file prompts/editing features become more robust
        if file is None: return
        logging.info(f'Saving as \'{file}\'')
        self._save(dest=file)


    def _save(self, dest=None, ext_hint=None):
        ''' Current iteration: IV '''
        start_time = get_time()

        # save copies of all critical properties that could potentially change while we're saving
        video = self.video.strip()
        mime = self.mime_type
        default_dir = self.dialog_settings.lineDefaultOutputPath.text().strip()   # default dir for if output text is provided, but w/ no dir
        minimum, maximum, frame_count, frame_rate, duration = self.minimum, self.maximum, self.frame_count, self.frame_rate, self.duration
        vwidth, vheight = self.vwidth, self.vheight

        audio_tracks = player.audio_get_track_count()

        delete_after_save = self.checkDeleteOriginal.checkState()       # what will we do to the media file after saving? (0, 1, or 2)
        MARK_DELETE = 1                                                 # checkState() values for delete_after_save
        FULL_DELETE = 2
        no_name_specified = False                                       # track whether we started with a unique destination or not

        op_replace_audio = self.operations.get('replace audio', None)   # path to audio track
        op_add_audio =     self.operations.get('add audio', None)       # path to audio track
        op_remove_track =  self.operations.get('remove track', None)    # track to remove
        op_amplify_audio = self.operations.get('amplify audio', None)   # new volume, from 0-1(+)
        op_resize =        self.operations.get('resize', None)
        op_rotate_video =  self.operations.get('rotate video', None)    # rotate angle -> 90/180/270
        op_trim_start =    self.buttonTrimStart.isChecked()             # represents both trimming and fading
        op_trim_end =      self.buttonTrimEnd.isChecked()               # represents both trimming and fading
        op_crop =          self.actionCrop.isChecked()
        if op_crop:
            crop_selection = tuple(self.vlc.factor_point(point) for point in self.vlc.selection)
            lfp = tuple(self.vlc.last_factored_points)

        non_crop_operations_detected = any((self.operations, op_trim_start, op_trim_end))
        operations_detected = non_crop_operations_detected or op_crop

        # get output name
        if not dest:
            output_text = self.get_renamed_output()
            if not output_text or output_text == video:
                no_name_specified = True
                if delete_after_save == FULL_DELETE: dest = video
                elif self.dialog_settings.checkAlwaysSaveAs.isChecked(): return self._save_as()
                else: dest = add_path_suffix(video, '_edited', unique=True)
            else:
                dest = output_text
                if not os.path.dirname(dest):                                                       # output text is just a name w/ no directory
                    if not default_dir: default_dir = os.path.dirname(video)                        # if no default path, use source video's path
                    dest = os.path.abspath(os.path.expandvars(os.path.join(default_dir, dest)))     # create and expand full path
                if not os.path.splitext(dest)[-1]:                                                  # append extension if needed
                    new_ext = ext_hint or os.path.splitext(video)[-1]
                    dest = f'{dest}{new_ext}'               # use extension hint if specified, otherwise just use source file's extension
            dirname, basename = os.path.split(dest)         # sanitize our custom destination (sanitize() does not account for full paths)
            dest = os.path.join(dirname, sanitize(basename))

        # no operations means we'll be returning early, but we might still be renaming the video
        if not operations_detected:
            if dest != video and not no_name_specified:     # destination is different from the video and not because we added "_edited" to it
                logging.info(f'No operations detected, but a new name was specified. Renaming to {dest}')
                return self.rename(dest)                    # no operations, but name is changed. do a normal rename and return (not thread safe?)
            return self.log_on_player('No changes have been made.', log=False)

        # ffmpeg is required after this point, so check that it's actually present
        # because we're in a thread, we skip the warning and display it separately through a signal
        if not constants.verify_ffmpeg(self, warning=False, force_warning=False):
            self.show_ffmpeg_warning_signal.emit(self)
            return self.log_on_player('You don\'t have FFmpeg installed!')

        # log data and create some strings for temporary paths we'll be needing
        logging.info(f'Saving file to "{dest}"')
        intermediate_file = video   # the path to the file that will be receiving all changes between operations
        final_dest = dest           # save the original dest so we can rename our temporary dest back later
        dest = add_path_suffix(dest, '_temp', unique=True)  # add _temp to dest, in case dest is the same as our base video
        logging.debug(f'temp-dest={dest}, video={video} delete_after_save={delete_after_save} operations_detected={operations_detected}')

        # stop player if we've reached this point. it's our last chance to do so safely (without theoretically disrupting the user)
        self.stop()
        #self.frame_override = 0                            # reset UI to frame 0 to avoid glitched times after stopping the player
        #self.lineCurrentTime.setText('')
        if dest == video or delete_after_save == FULL_DELETE:         # TODO add comment here once this is figured out better
            self.locked_video = video
            logging.info(f'Video locked during edits: {self.locked_video}')

        #self.frame_override = 0
        self.show_save_progress_signal.emit(True)           # show transparent indeterminant progress bar over statusbar
        update_progress_signal.emit(0)

        try:
            # check for specific operations
            if op_replace_audio is not None:
                self.log('Audio replacement requested.')
                audio = op_replace_audio    # TODO -shortest (before "{dest}") results in audio cutting out ~1 second before end of video despite the audio being longer
                intermediate_file = ffmpeg(intermediate_file, f'-i "%tp" -i "{audio}" -c:v copy -map 0:v:0 -map 1:a:0 "{dest}"', dest)
            if op_add_audio is not None:                    # https://superuser.com/questions/1041816/combine-one-image-one-audio-file-to-make-one-video-using-ffmpeg
                self.log('Additional audio track requested.')
                audio = op_add_audio        # TODO :duration=shortest (after amix=inputs=2) has same issue as above
                if mime != 'image':         # normal audio mixing does NOT work if the video has 0 audio tracks
                    the_important_part = '-map 0:v:0 -map 1:a:0 -c:v copy' if mime == 'video' and audio_tracks == 0 else '-filter_complex amix=inputs=2'
                    intermediate_file = ffmpeg(intermediate_file, f'-i "%tp" -i "{audio}" {the_important_part} "{dest}"', dest)
                elif mime == 'audio': intermediate_file = ffmpeg(intermediate_file, f'-i "%tp" -i "{audio}" -filter_complex amix=inputs=2 "{dest}"', dest)
                else: intermediate_file = ffmpeg(intermediate_file, f'-loop 1 -i "%tp" -i "{audio}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest "{dest}"', dest)
            if op_remove_track is not None:                 # NOTE: This can degrade audio quality slightly.
                self.log(f'{op_remove_track.title()}-track removal requested.')
                intermediate_file = ffmpeg(intermediate_file, f'-i "%tp" {"-q:a 0 -map a" if op_remove_track == "video" else "-c copy -an"} "{dest}"', dest)
            if op_amplify_audio is not None:
                self.log('Audio amplification requested.')
                intermediate_file = ffmpeg(intermediate_file, f'-i "{video}" -filter:a "volume={op_amplify_audio}" "{dest}"', dest)
            if op_resize is not None:                       # audio -> https://stackoverflow.com/questions/25635941/ffmpeg-modify-audio-length-size-stretch-or-shrink
                log_note = ' (this is a time-consuming task)' if mime == 'video' else ' (Note: this should be a VERY quick operation)' if mime == 'audio' else ''
                self.log(f'{mime.title()} resize requested{log_note}.')
                width, height = op_resize                   # for audio, width is the percentage and height is None
                if mime == 'audio': intermediate_file = ffmpeg(intermediate_file, f'-i "%tp" -filter:a atempo="{width}" "{dest}"', dest)
                else: intermediate_file = ffmpeg(intermediate_file, f'-i "%tp" -vf "scale={width}:{height}" -crf 28 -c:a copy "{dest}"', dest)
            if op_rotate_video is not None:
                self.log('Video rotation/flip requested (this is a time-consuming task).')
                intermediate_file = ffmpeg(intermediate_file, f'-i "%tp" -vf "{op_rotate_video}" -crf 28 -c:a copy "{dest}"', dest)

            # trim -> https://trac.ffmpeg.org/wiki/Seeking TODO: -vf trim filter should be used in here
            if op_trim_start or op_trim_end:
                if not cfg.trimmodeselected:
                    self.show_trim_dialog_signal.emit()
                    while not cfg.trimmodeselected: sleep(0.2)
                    start_time = get_time()                 # reset start_time to undo time spent waiting for dialog
                if self.is_trim_mode():
                    precise = self.trim_mode_action_group.checkedAction() is self.actionTrimPrecise or self.extension in constants.SPECIAL_TRIM_EXTENSIONS
                    self.log(f'{"Precise" if precise else "Imprecise"} trim requested{" (this is a time-consuming task)" if precise else ""}.')
                    cmd_parameters = f' -c:v {"libx264" if precise else "copy"} -c:a {"aac" if precise else "copy -avoid_negative_ts make_zero"} '
                    trim_cmd_parts = []
                    if minimum > 0:           trim_cmd_parts.append(f'-ss {minimum / frame_rate}')
                    if maximum < frame_count: trim_cmd_parts.append(f'-to {maximum / frame_rate}')  # "-c:v libx264" vs "-c:v copy"
                    if trim_cmd_parts: intermediate_file = ffmpeg(intermediate_file, f'-i "%tp" {" ".join(trim_cmd_parts)}{cmd_parameters}"{dest}"', dest)

                # fade (using trim buttons as fade points) -> https://dev.to/dak425/add-fade-in-and-fade-out-effects-with-ffmpeg-2bj7
                else:
                    self.log('Fade requested (this is a time-consuming task).')     # TODO: ffmpeg fading is actually very versatile, this could be WAY more sophisticated
                    mode = {self.actionFadeBoth: 'both', self.actionFadeVideo: 'video', self.actionFadeAudio: 'audio'}[self.trim_mode_action_group.checkedAction()]
                    fade_cmd_parts = []                                             # TODO: fading out sometimes does not fully complete by a few frames
                    if mode == 'video' or mode == 'both':
                        fade_parts = []
                        if minimum > 0:
                            seconds = minimum / frame_rate
                            fade_parts.append(f'fade=t=in:st=0:d={seconds}')        # d defaults to ~1 second
                        if maximum < frame_count:
                            seconds = maximum / frame_rate
                            delta = duration - seconds
                            fade_parts.append(f'fade=t=out:st={seconds}:d={delta}')
                        if fade_parts: fade_cmd_parts.append(f'-vf "{",".join(fade_parts)}{" -c:a copy" if mode != "both" else ""}"')
                    if mode == 'audio' or mode == 'both':
                        fade_parts = []
                        if minimum > 0:
                            seconds = minimum / frame_rate
                            fade_parts.append(f'afade=t=in:st=0:d={seconds}')       # d defaults to ~1 second
                        if maximum < frame_count:
                            seconds = maximum / frame_rate
                            delta = duration - seconds
                            fade_parts.append(f'afade=t=out:st={seconds}:d={delta}')
                        if fade_parts: fade_cmd_parts.append(f'-af "{",".join(fade_parts)}{" -c:v copy" if mode != "both" and mime == "video" else ""}"')
                    if fade_cmd_parts: intermediate_file = ffmpeg(intermediate_file, f'-i "%tp" {" ".join(fade_cmd_parts)} "{dest}"', dest)

            # crop -> https://video.stackexchange.com/questions/4563/how-can-i-crop-a-video-with-ffmpeg
            if op_crop:     # ffmpeg cropping is not 100% accurate, final dimensions may be off by ~1 pixel
                self.log('Cropping...')                     # -filter:v "crop=out_w:out_h:x:y"
                crop_top =    min(crop_selection[0].y(), vheight - 1)
                crop_left =   min(crop_selection[0].x(), vwidth - 1)
                crop_right =  min(crop_selection[1].x(), vwidth)
                crop_bottom = min(crop_selection[2].y(), vheight)
                crop_width =  crop_right - crop_left
                crop_height = crop_bottom - crop_top
                if crop_width == vwidth and crop_height == vheight:                 # not actually cropped -> disable crop mode and update our operations
                    logging.info('Crop is the same size as the source media.')
                    if self.video == video: self.disable_crop_mode_signal.emit()    # no new video has started playing during saving process
                    operations_detected = non_crop_operations_detected              # see if any other operations were detected beforehand
                else:
                    if self.mime_type == 'image':
                        image_data = get_PIL_Image().open(video)
                        image_data.crop((round(lfp[0].x()), round(lfp[0].y()),              # left/top/right/bottom (crop takes a tuple)
                                         round(lfp[1].x()), round(lfp[2].y()))).save(dest)  # round QPointFs
                    else: ffmpeg(intermediate_file, f'-i "%tp" -filter:v "crop={round(crop_width)}:{round(crop_height)}:{round(crop_left)}:{round(crop_top)}" "{dest}"')

            # confirm our operations, clean up temp files/base video, and get final path
            if operations_detected:                         # double-check that we've actually done anything at all
                if not os.path.exists(dest): raise AssertionError('(!) Media saved without error, but never actually appeared. Likely an FFmpeg error.')
                if os.path.getsize(dest) == 0:
                    os.remove(dest)
                    raise AssertionError('(!) Media saved without error, but is completely empty. Likely an FFmpeg error.')

                if delete_after_save == FULL_DELETE: self.mark_for_deletion(modifiers=Qt.ControlModifier)
                else:                                       # we either don't want to delete or we want to only mark it for now
                    if dest == video:                       # destination has same name as original video, but we don't want to delete it (yet)
                        temp_name = add_path_suffix(video, '_original', unique=True)
                        os.rename(video, temp_name)
                        video = temp_name
                    if delete_after_save == MARK_DELETE: self.marked_for_deletion.add(video)

                if os.path.exists(final_dest): os.replace(dest, final_dest)
                else: os.renames(dest, final_dest)

                # only open edited video if user hasn't opened something else TODO make this a setting
                if self.video == video: self._save_open_signal.emit(final_dest, self.dialog_settings.checkCycleRememberOriginalPath.checkState() == 2)
                elif self.dialog_settings.checkTextOnSave.isChecked(): show_text(f'Changes saved to {final_dest}.')
                self.log(f'Changes saved to {final_dest} after {get_time() - start_time:.1f} seconds.')
            else: return self.log('No changes have been made because the crop was the same size as the source media.')
        except: self.log(f'(!) SAVE FAILED: {format_exc()}')
        finally:
            self.locked_video = None                        # unlock video if needed
            self.show_save_progress_signal.emit(False)      # make sure we hide the progress bar no matter what


    def update_slider_thread(self):
        ''' Handles updating the progress bar. This includes both slider-types and swapping between them.
            frame_override can be set to override the next pending frame (circumventing timing-related
            bugs), and if used with open_queued, the file-opening process is completed and cleaned up.
            While not playing and/or not visible, resource-usage is kept to a minimum. '''
        logging.info('Slider-updating thread started.')

        # re-define global aliases -> having them as locals is even faster
        current_frame = self.sliderProgress.value
        player = self.player
        is_playing = player.is_playing
        get_rate = player.get_rate                          # TODO: get_rate() vs. self.playback_speed <- which is faster?
        update_progress_signal = self.update_progress_signal
        set_progress_slider = self.sliderProgress.setValue

        while not self.closed:
            # window is NOT visible, stay relatively idle and do not update
            while not self.isVisible() and not self.closed: sleep(0.25)

            # window is visible, but nothing is actively playing
            while self.isVisible() and not is_playing() and not self.closed:
                self.sliderProgress.update()                # force QVideoSlider to keep painting (this refreshes the hover-timestamp)
                sleep(0.025)                                # update at 40fps
            self.swap_slider_styles_queued = False          # reset queued slider-swap (or the slider won't update anymore after a swap)

            # high-precision option enabled -> fake a smooth slider based on media's frame rate (simulates what libvlc SHOULD have)
            if self.dialog_settings.checkHighPrecisionProgress.isChecked():     # NOTE: (fast_start_interface_thread checks for accuracy every 5 seconds)
                start = get_time()
                while is_playing() and not self.lock_progress_updates and not self.swap_slider_styles_queued:  # not playing, not locked, and not about to swap styles
                    # lock_progress_updates is not always reached fast enough, so we use open_queued to force this thread to override the current frame
                    if self.frame_override is not None:
                        if self.open_queued:
                            self._open_signal.emit()    # _open_signal uses self._open()
                            set_progress_slider(0)      # risky -> force sliderProgress to 0 to fix very rare timing issue (not thread safe, might "freeze" GUI)
                        else:
                            update_progress_signal.emit(self.frame_override)
                        self.frame_override = None      # reset frame_override
                        self.open_queued = False        # reset open_queued
                    elif (next_frame := current_frame() + 1 * get_rate()) <= self.frame_count:     # do NOT update progress if we're at the end
                        update_progress_signal.emit(next_frame)                                     # update_progress_signal -> update_progress_slot

                    sleep(0.0001)                       # sleep to force-update get_time()
                    try: sleep(self.delay - (get_time() - start) - 0.0011)
                    except Exception as error: logging.warning(f'update_slider_thread bottleneck - {type(error)}: {error} -> delay={self.delay} execution-time={get_time() - start}')
                    finally: start = get_time()

            # high-precision option disabled -> use libvlc's native progress at 8fps and manually paint QVideoSlider at 40fps
            else:
                while is_playing() and not self.lock_progress_updates and not self.swap_slider_styles_queued:   # not playing, not locked, and not about to swap styles
                    # lock_progress_updates is not always reached fast enough, so we use open_queued to force this thread to override the current frame
                    if self.frame_override is not None:
                        if self.open_queued:
                            self._open_signal.emit()    # _open_signal uses self._open()
                            set_progress_slider(0)      # risky -> force sliderProgress to 0 to fix very rare timing issue (not thread safe, might "freeze" GUI)
                        else:
                            update_progress_signal.emit(self.frame_override)
                        self.frame_override = None      # reset frame_override
                        self.open_queued = False        # reset open_queued
                    else:
                        for _ in range(5):              # force QVideoSlider to paint at 40fps (this refreshes the hover-timestamp)
                            self.sliderProgress.update()
                            sleep(0.025)                # only update slider position at 8fps (every 0.125 seconds -> VLC updates every 0.2-0.35)
                        new_frame = player.get_position() * self.frame_count                       # convert VLC position to frame
                        if new_frame >= current_frame(): update_progress_signal.emit(new_frame)    # make sure VLC didn't literally go backwards (pretty common)
                        #else: update_progress_signal.emit(int(new_frame + (self.frame_rate / 5)))  # simulate a non-backwards update TODO this actually makes it look worse
        return logging.info('Program closed. Ending update_slider thread.')


    def set_and_update_progress(self, frame: int = 0):
        ''' Simultaneously sets VLC/gif player position and updates progress on GUI. '''
        set_player_position(frame / self.frame_count)
        #self.set_player_time(round(frame * (1000 / self.frame_rate)))
        update_progress(frame)
        set_gif_position(frame)


    def update_progress_slot(self, frame: float):
        ''' A slot for update_progress_signal which updates our progress in a thread-safe manner and without slowing
            down update_slider_thread. Takes `frame` as a float in order to handle partial frames caused by
            non-1 playback speeds. Saves the partial frame for later use as updates use an integer frame. '''
        # TODO: fractional_frame might not work as well as I hope
        frame += self.fractional_frame                  # add previous partial frame to get true position
        int_frame = int(frame)
        update_progress(int_frame)                      # update with an integer frame
        self.fractional_frame = frame - int_frame       # save new partial frame for later use


    def update_progress(self, frame: int):
        ''' Updates every section of the UI to reflect the current `frame`. Restarts the
            player if called while the video has ended. Clamps playback to desired trims. '''
        if not self.minimum <= frame <= self.maximum:
            if not (self.sliderProgress.grabbing_clamp_minimum or self.sliderProgress.grabbing_clamp_maximum):
                frame = min(self.maximum, max(self.minimum, frame))
                if frame == self.maximum and self.buttonTrimEnd.isChecked():
                    self.force_pause(True)
        self.current_time = round(self.duration * (frame / self.frame_count), 3)
        h, m, s, ms = get_hms(self.current_time)

        set_progress_slider(frame)
        if not current_time_lineedit_has_focus():       # use cleaner format for time-strings on videos > 1 hour
            set_current_time_text(f'{m:02}:{s:02}.{ms:02}' if self.duration < 3600 else f'{h}:{m:02}:{s:02}')

        self.lock_spin_updates = True                   # lock spins from actually updating player so we don't get recursion
        set_hour_spin(h)
        set_minute_spin(m)
        set_second_spin(s)
        set_frame_spin(frame)
        self.lock_spin_updates = False                  # unlock spins so they can be edited by hand again


    def update_time_spins(self):
        ''' Handles the hour, minute, and second spinboxes. Calculates the next frame based on the new
            values, and updates the progress UI accordingly. If the new frame is after the end of the media,
            it's replaced with the current frame and the progress UI is reset to its previous state. '''
        if self.lock_spin_updates or self.lock_progress_updates: return         # return if user is not manually setting the time spins
        self.lock_progress_updates = True               # lock progress updates to prevent recursion errors from multiple elements updating at once
        try:
            seconds = self.spinHour.value() * 3600
            seconds += self.spinMinute.value() * 60
            seconds += self.spinSecond.value()

            old_frame = self.spinFrame.value()
            excess_frames = old_frame % self.frame_rate
            new_frame = math.ceil((seconds * self.frame_rate) + excess_frames)  # ceil() to ensure we don't overshoot frame_count on the next frame
            if new_frame > self.frame_count: new_frame = old_frame
            set_and_update_progress(new_frame)

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
    def set_trim_start(self, *args, force=False):
        if not self.video:
            if self.buttonTrimStart.isChecked(): self.buttonTrimStart.setChecked(False)
            return
        if force: self.buttonTrimStart.setChecked(True)         # force-check trim button, typically used from context menu

        if self.buttonTrimStart.isChecked():
            desired_minimum = get_progess_slider()
            if desired_minimum >= self.maximum:
                self.buttonTrimStart.setChecked(False)
                return self.log('You cannot set the start of your trim after the end of it.')
            self.minimum = desired_minimum

            h, m, s, ms = get_hms(self.current_time)  # use cleaner format for time-strings on videos > 1 hour
            if self.duration < 3600: self.buttonTrimStart.setText(f'{m}:{s:02}.{ms:02}')
            else: self.buttonTrimStart.setText(f'{h}:{m:02}:{s:02}')
            self.sliderProgress.clamp_minimum = True
        else:
            self.minimum = self.sliderProgress.minimum()
            self.buttonTrimStart.setText('Start' if self.is_trim_mode() else 'Fade to')
            self.sliderProgress.clamp_minimum = False


    def set_trim_end(self, *args, force=False):
        if not self.video:
            if self.buttonTrimEnd.isChecked(): self.buttonTrimEnd.setChecked(False)
            return
        if force: self.buttonTrimEnd.setChecked(True)           # force-check trim button, typically used from context menu

        if self.buttonTrimEnd.isChecked():
            desired_maximum = get_progess_slider()
            if desired_maximum <= self.minimum:
                self.buttonTrimEnd.setChecked(False)
                return self.log('You cannot set the end of your trim before the start of it.')
            self.maximum = desired_maximum

            h, m, s, ms = get_hms(self.current_time)            # use cleaner format for time-strings on videos > 1 hour
            if self.duration < 3600: self.buttonTrimEnd.setText(f'{m}:{s:02}.{ms:02}')
            else: self.buttonTrimEnd.setText(f'{h}:{m:02}:{s:02}')
            self.sliderProgress.clamp_maximum = True
        else:
            self.maximum = self.sliderProgress.maximum()
            self.buttonTrimEnd.setText('End' if self.is_trim_mode() else 'Fade from')
            self.sliderProgress.clamp_maximum = False


    def set_trim_mode(self, action: QtW.QAction):
        cfg.trimmodeselected = True
        if action in (self.actionTrimAuto, self.actionTrimPrecise):
            self.buttonTrimStart.setText(self.buttonTrimStart.text().replace('Fade to', 'Start'))
            self.buttonTrimEnd.setText(self.buttonTrimEnd.text().replace('Fade from', 'End'))
            for button in (self.buttonTrimStart, self.buttonTrimEnd):
                button.setToolTip(constants.TRIM_BUTTON_TOOLTIP_BASE.replace('?mode', 'trim'))
        else:
            self.buttonTrimStart.setText(self.buttonTrimStart.text().replace('Start', 'Fade to'))
            self.buttonTrimEnd.setText(self.buttonTrimEnd.text().replace('End', 'Fade from'))
            for button in (self.buttonTrimStart, self.buttonTrimEnd):
                button.setToolTip(constants.TRIM_BUTTON_TOOLTIP_BASE.replace('?mode', 'fade'))


    def concatenate(self, action: QtW.QAction, files=None):                             # TODO this is old and needs to be unified with the other edit methods
        # https://stackoverflow.com/questions/7333232/how-to-concatenate-two-mp4-files-using-ffmpeg
        # https://stackoverflow.com/questions/31691943/ffmpeg-concat-produces-dts-out-of-order-errors
        if not constants.verify_ffmpeg(self, force_warning=True):
            return self.log_on_player('You don\'t have FFmpeg installed!')

        style = {self.actionCatNone: 0, self.actionCatAny: 1, self.actionCatBefore: 2, self.actionCatAfter: 3}[action]
        if self.mime_type != 'video' and style > 1: return self.statusbar.showMessage('Concatenation is not implemented for audio and image files yet.', 10000)

        try:
            if self.video is None and style > 1: return self.statusbar.showMessage('No video is playing.', 10000)  # for styles that assume a video is playing -> return
            logging.info(f'Preparing to concatenate videos with style={style} and files={files}')

            # create/setup dialog and connect signals
            from bin.window_cat import Ui_catDialog
            dialog = qthelpers.getDialogFromUiClass(Ui_catDialog, **self.get_popup_location())
            dialog.videoList.parent = self                                              # set fake parent for videoList so it can directly access our properties
            dialog.checkOpen.setChecked(cfg.concatenate.open)
            dialog.checkExplore.setChecked(cfg.concatenate.explore)
            dialog.checkDelete.setCheckState(self.checkDeleteOriginal.checkState())     # set dialog's delete setting to our current delete setting
            dialog.output.setText(self.lineOutput.text().strip())                       # set dialog's output text to our current output text

            dialog.add.clicked.connect(dialog.videoList.add)
            dialog.delete.clicked.connect(lambda: qthelpers.listRemoveSelected(dialog.videoList))   # TODO itemDoubleClicked -> play video?
            dialog.up.clicked.connect(dialog.videoList.move)
            dialog.down.clicked.connect(lambda: dialog.videoList.move(down=True))
            dialog.browse.clicked.connect(lambda: self.browse_concatenate_output(dialog.output))
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
                if len(files) < 2: return self.log('Not enough videos to concatenate.')   # user ended up with <2 videos in dialog and hit OK -> return
            elif not dialog.output.text(): self.browse_concatenate_output(dialog.output)  # dialog skipped, but no output text was passed from the main window
            self.log(f'Concatenating files: {files}')

            # preparing videos for concatenation
            intermediate_files = []
            for file in files:
                intermediate_file = os.path.join(constants.TEMP_DIR, file.replace('.mp4', '.ts').replace('/', '.').replace('\\', '.'))
                try: os.remove(intermediate_file)
                except: pass
                intermediate_files.append(intermediate_file)
                ffmpeg_simple(f'-i "{file}" -c copy -bsf:v h264_mp4toannexb -f mpegts "{intermediate_file}"')

            # preparing output destination
            output = dialog.output.text().strip()
            if not output: output = add_path_suffix(files[0] if style < 2 else self.video, '_concatenated')   # no output name -> default to first file's name + "_concatenated"
            if not os.path.splitext(output)[-1]: output = f'{output}{os.path.splitext(files[0])[-1]}'   # append appropriate extension if needed
            output = get_unique_path(output)
            dirname, basename = os.path.split(output)
            if not dirname:                                         # no output directory specified
                default_dir = self.dialog_settings.lineDefaultOutputPath.text().strip()
                dirname = default_dir if default_dir else os.path.dirname(files[0])
            output = os.path.join(dirname, sanitize(basename))      # sanitize() does not account for full paths

            # actually concatentating videos
            if self.mime_type == 'audio': cmd = f'-i "concat:{"|".join(intermediate_files)}" -c copy "{output}"'
            else: cmd = f'-i "concat:{"|".join(intermediate_files)}" -c copy -video_track_timescale 100 -bsf:a aac_adtstoasc -movflags faststart -f mp4 -threads 1 "{output}"'
            ffmpeg_simple(cmd)
            for intermediate_file in intermediate_files:
                try: os.remove(intermediate_file)
                except: pass

            if not os.path.exists(output): return self.log('(!) Concatenation failed. No files have been altered.')
            self.log(f'Concatenation saved to {output}.')

            if dialog.checkExplore.isChecked(): qthelpers.openPath(output, explore=True)
            if dialog.checkOpen.isChecked(): self.open(output)
            if dialog.checkDelete.checkState() == 1: self.marked_for_deletion.update(files)
            elif dialog.checkDelete.checkState() == 2:
                for file in files: self.mark_for_deletion(file=file, modifiers=Qt.ControlModifier)
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
        if not self.video: return self.statusbar.showMessage('No media is playing.', 10000)
        width, height = self.get_size_dialog()
        if width is None: return            # dialog cancelled
        if width == 0: width = -1           # ffmpeg takes -1 as a default value, not 0
        if height == 0: height = -1         # ffmpeg takes -1 as a default value, not 0

        self.operations['resize'] = (width, height)
        if self.lineOutput.text().strip(): self.save()
        else: self.save_as('Save resized media as...')


    def rotate_video(self, action: QtW.QAction):
        if not self.video: return self.statusbar.showMessage('No video is playing.', 10000)
        if self.mime_type == 'audio': return self.statusbar.showMessage('Well that would just be silly, wouldn\'t it?', 10000)
        rotation_presets = {
            self.actionRotate90:         'transpose=clock',
            self.actionRotate180:        'transpose=clock,transpose=clock',
            self.actionRotate270:        'transpose=cclock',
            self.actionFlipVertically:   'vflip',
            self.actionFlipHorizontally: 'hflip'
        }
        self.operations['rotate video'] = rotation_presets[action]
        if self.lineOutput.text().strip(): self.save()                 # TODO this defeats the purpose of self.operations
        else: self.save_as('Save rotated video/image as...', filter='All files(*)')     # TODO better filter/hint


    def amplify_audio(self):                # https://stackoverflow.com/questions/81627/how-can-i-hide-delete-the-help-button-on-the-title-bar-of-a-qt-dialog
        if not self.video: return self.statusbar.showMessage('No media is playing.', 10000)
        if self.mime_type == 'image': return self.statusbar.showMessage('Well that would just be silly, wouldn\'t it?', 10000)
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
            if self.lineOutput.text().strip(): self.save()
            else: self.save_as('Save amplified video/audio as...')

        dialog.accepted.connect(accept)
        dialog.exec()


    def replace_audio(self, *args, path=None):
        if not self.video: return self.statusbar.showMessage('No media is playing.', 10000)
        if self.mime_type == 'audio': return self.statusbar.showMessage('Well that would just be silly, wouldn\'t it?', 10000)
        if self.mime_type == 'image': return self.add_audio(path=path)
        try:
            if path is None: path, cfg.lastdir = qthelpers.browseForFile(cfg.lastdir, caption='Select audio file to replace audio track with')
            if not path: return                                             # cancel selected
            self.operations['replace audio'] = path
            if self.lineOutput.text().strip(): self.save()
            else: self.save_as('Save video with replaced audio track as...')
        except: self.log(f'(!) REPLACE_AUDIO FAILED: {format_exc()}')


    def add_audio(self, *args, path=None):          # TODO: doing this on an audio file is somewhat unstable TODO: add option to toggle "shortest" setting
        if not self.video: return self.statusbar.showMessage('No media is playing.', 10000)
        try:
            if path is None: path, cfg.lastdir = qthelpers.browseForFile(cfg.lastdir, caption='Select audio file to add')
            if not path: return                                             # cancel selected
            self.operations['add audio'] = path
            if self.lineOutput.text().strip(): self.save()
            else: self.save_as('Save media with additional audio track as...', filter='All files (*)')  # TODO better filter/hint
        except: self.log(f'(!) ADD_AUDIO_TRACK FAILED: {format_exc()}')


    def remove_track(self, *args, audio=True):     # https://superuser.com/questions/268985/remove-audio-from-video-file-with-ffmpeg
        if not self.video: return self.statusbar.showMessage('No media is playing.', 10000)
        if self.mime_type != 'video': return self.statusbar.showMessage('Well that would just be silly, wouldn\'t it?', 10000)
        self.operations['remove track'] = 'audio' if audio else 'video'
        if self.lineOutput.text().strip(): self.save(ext_hint=None if audio else '.mp3')           # give hint for extension
        else: self.save_as(caption=f'Save {self.operations["remove track"]} as...',     # TODO set "save as" default filter to .mp3 for video-removal as well?
                           filter=f'{"MP3 files (*.mp3);;WAV files (*.wav);;AAC files (*.aac);;" if not audio else ""}MP4 files (*.mp4);;All files (*)')


    # ---------------------
    # >>> PROMPTS <<<
    # ---------------------
    def browse_default_path_output(self):
        path, cfg.lastdir = qthelpers.browseForDirectory(cfg.lastdir, caption='Select default output directory')
        if path is None: return
        self.dialog_settings.lineDefaultOutputPath.setText(path)


    def browse_default_snapshot_path_output(self):
        path, cfg.lastdir = qthelpers.browseForDirectory(cfg.lastdir, caption='Select default snapshot directory')
        if path is None: return
        self.dialog_settings.lineDefaultSnapshotPath.setText(path)


    def browse_concatenate_output(self, lineEdit):
        starting_name = self.video if self.dialog_settings.checkSaveAsUseMediaFolder.isChecked() else os.path.join(cfg.lastdir, os.path.basename(self.video))
        file, cfg.lastdir = qthelpers.saveFile(lastdir=get_unique_path(starting_name), caption='Save concatenated video as...', filter='All files (*)')
        if file is None: return
        lineEdit.setText(file)


    def browse_subtitle_file(self, urls=None):
        if self.mime_type == 'image': self.statusbar.showMessage('Well that would just be silly, wouldn\'t it?', 10000)
        if urls is None:
            urls, cfg.lastdir = qthelpers.browseForFiles(cfg.lastdir,
                                                         caption='Select subtitle file(s) to add',
                                                         filter='Subtitle Files (*.cdg *.idx *.srt *.sub *.utf *.ass *.ssa *.aqt *.jss *.psb *.it *.sami *smi *.txt *.smil *.stl *.usf *.dks *.pjs *.mpl2 *.mks *.vtt *.tt *.ttml *.dfxp *.scc);;All files (*)',
                                                         url=True)
        for url in urls:
            url = url.url()
            if player.add_slave(0, url, self.dialog_settings.checkAutoEnableSubtitles.isChecked()) == 0:   # slaves can be subtitles (0) or audio (1). last arg = auto-select
                self.log(f'Subtitle file {url} added and enabled.')                                             # returns 0 on success
                if self.dialog_settings.checkTextOnSubtitleAdded.isChecked(): show_text('Subtitle file added and enabled')
            else:
                self.log(f'Failed to add subtitle file {url} (VLC does not report specific errors for this).')
                if self.dialog_settings.checkTextOnSubtitleAdded.isChecked(): show_text('Failed to add subtitle file')


    def get_size_dialog(self):
        is_video = self.mime_type == 'video'
        vwidth, vheight, duration = self.vwidth, self.vheight, self.duration
        max_time_string = self.labelMaxTime.text()
        dialog = qthelpers.getDialog(title='Input desired ' + 'size' if is_video else 'length',
                                     **self.get_popup_location(), fixedSize=(0, 0), flags=Qt.Tool)

        layout = QtW.QVBoxLayout(dialog)
        form = QtW.QFormLayout()
        label = QtW.QLabel(dialog)
        if is_video: label.setText('If width AND height are 0,\nthe native resolution is used.\n\nIf width OR height are 0,\nnative aspect-ratio is used.\n\nSupports percentages,\nsuch as 50%.')
        else: label.setText('Enter a timestamp (hh:mm:ss.ms)\nor a percentage. Note: This is\ncurrently limited to 50-200%\nof the original audio\'s length.')
        label.setAlignment(Qt.AlignCenter)

        wline = QtW.QLineEdit('0' if is_video else max_time_string, dialog)
        wbutton = QtW.QPushButton('Width:' if is_video else 'Length:', dialog)
        wbutton.clicked.connect(lambda: wline.setText(str(int(vwidth)) if is_video else max_time_string))
        if is_video: wbutton.setToolTip(f'Reset width to native resolution ({vwidth:.0f} pixels).')
        else: wbutton.setToolTip(f'Reset length to native length ({max_time_string}).')

        if is_video:
            hline = QtW.QLineEdit('0', dialog)
            hbutton = QtW.QPushButton('Height:', dialog)
            hbutton.clicked.connect(lambda: hline.setText(str(int(vheight))))
            hbutton.setToolTip(f'Reset height to native resolution ({vheight:.0f} pixels).')

            for w in (wbutton, hbutton): w.setMaximumWidth(50)
            for w in (wline, hline):
                w.setMaxLength(6)
                w.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('\\d*%')))    # https://stackoverflow.com/questions/13422995/set-qlineedit-to-accept-only-numbers
        else: wbutton.setMaximumWidth(50)

        wline.selectAll()                       # start with text in width lineEdit selected, for quicker editing
        form.addRow(label)
        form.addRow(wbutton, wline)
        if is_video: form.addRow(hbutton, hline)
        layout.addLayout(form)
        dialog.addButtons(layout, QtW.QDialogButtonBox.Cancel, QtW.QDialogButtonBox.Ok)

        def accept():
            if is_video:
                width, height =   wline.text().strip(), hline.text().strip()
                if '%' in width:  width = round(vwidth * (float(width.strip('%').strip()) / 100))
                else:             width = int(width)
                if '%' in height: height = round(vheight * (float(height.strip('%').strip()) / 100))
                else:             height = int(height)
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

        # open resize dialog. if sizes are percents, strip '%' and multiply w/h by percentages
        dialog.accepted.connect(accept)
        if not dialog.exec(): return None, None  # cancel selected, return None
        return dialog.width, dialog.height


    def open_color_picker(self):                # NOTE: F suffix is Float -> values are represented from 0-1 (e.g. getRgb() becomes getRgbF())
        ''' Opens color-picking dialog, specifically for the hover-timestamp font color setting.
            Saves new color and adjusts the color of the color-picker's button through a stylesheet. '''
        try:                                    # TODO: add support for marquee colors
            picker = QtW.QColorDialog()
            #for index, default in enumerate(self.defaults): picker.setCustomColor(index, QtGui.QColor(*default))
            color = picker.getColor(initial=self.sliderProgress.hover_font_color, parent=self.dialog_settings, title='Picker? I hardly know her!')
            if not color.isValid(): return
            self.sliderProgress.hover_font_color = color

            color_string = str(color.getRgb())
            self.dialog_settings.buttonHoverFontColor.setToolTip(color_string)
            self.dialog_settings.buttonHoverFontColor.setStyleSheet('QPushButton {background-color: rgb' + color_string + ';border: 1px solid black;}')
        except: self.log(f'OPEN_COLOR_PICKER FAILED: {format_exc()}')


    def show_about_dialog(self):                # lazy version of about dialog
        from bin.window_about import Ui_aboutDialog
        dialog_about = qthelpers.getDialogFromUiClass(Ui_aboutDialog, **self.get_popup_location(),
                                                      modal=True, deleteOnClose=True)
        dialog_about.labelLogo.setPixmap(QtGui.QPixmap(os.path.join(constants.RESOURCE_DIR, 'logo_filled.png')))
        dialog_about.labelVersion.setText(dialog_about.labelVersion.text().replace('?version', constants.VERSION))

        settings_were_open = self.dialog_settings.isVisible()   # hide the always-on-top settings while we show popups
        if settings_were_open: self.dialog_settings.hide()
        dialog_about.adjustSize()                               # adjust size to match version string/OS fonts
        dialog_about.exec()                                     # don't bother setting a fixed size or using open()
        if settings_were_open: self.dialog_settings.show()      # restore settings if they were originally open

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
                'setting in the future by right-clicking the \'Start\' and '
                '\'End\' buttons, or by using the \'Video\' menu.')
            button_precise = QtW.QCommandLinkButton(
                'Precise trim',
                'Re-encode your trim. This is a slow process, but will always be '
                '100% accurate. Recommended if you need the start of a trim to be '
                'accurate down to the frame, or if you use a variety of formats.')
            button_auto = QtW.QCommandLinkButton(
                'Auto trim',
                'Instantly trim your clip by rounding the start back to the last keyframe '
                'and cutting from there. Some formats/encoders may be corrupted or briefly '
                'frozen at the start (formats like MP4 usuallly work better). PyPlayer '
                'will try falling back to precise trimming when possible.')

            label.setAlignment(Qt.AlignCenter)
            label.setWordWrap(True)
            button_precise.setDefault(True)
            button_precise.clicked.connect(dialog.accept)
            button_precise.clicked.connect(lambda: dialog.select(button_precise))
            button_auto.clicked.connect(dialog.accept)
            button_auto.clicked.connect(lambda: dialog.select(button_auto))

            layout = QtW.QVBoxLayout(dialog)
            layout.addWidget(label)
            layout.addWidget(button_precise)
            layout.addWidget(button_auto)

            if constants.PLATFORM != 'Windows': dialog.adjustSize()
            if dialog.exec() == QtW.QDialog.Accepted:
                if dialog.choice == button_auto: self.actionTrimAuto.setChecked(True)
                else: self.actionTrimPrecise.setChecked(True)
        except: pass
        finally: cfg.trimmodeselected = True                # set this to True no matter what (_save is waiting on this)


    def show_delete_prompt(self):
        ''' Creates and shows a dialog for deleting marked files. Dialog consists of a QGroupBox
            containing a QCheckBox for each file, with Yes/No/Cancel buttons at the bottom. '''
        if not self.marked_for_deletion: return self.log('No media is marked for deletion.')
        logging.info('Opening deletion prompt...')
        try:
            dialog = qthelpers.getDialog(title='Confirm Deletion', icon='SP_DialogDiscardButton', **self.get_popup_location())
            recycle = self.dialog_settings.checkRecycleBin.isChecked()

            # layout at "fixed size" https://stackoverflow.com/questions/14980620/qt-layout-resize-to-minimum-after-widget-size-changes
            layout = QtW.QVBoxLayout(dialog)
            layout.setSizeConstraint(QtW.QLayout.SetFixedSize)

            # group box and its own layout
            group = QtW.QGroupBox(f'The following files will be {"recycled. Recycle?" if recycle else "permanently deleted. Delete?"}', dialog)
            group.setAlignment(Qt.AlignHCenter)
            groupLayout = QtW.QVBoxLayout(group)
            layout.addWidget(group)

            # checkboxes for each file TODO add setting for sorting the files
            for file in sorted(self.marked_for_deletion, key=os.path.splitext):   # key=os.path.splitext to ignore extensions when sorting
                checkbox = QtW.QCheckBox(file, group)
                checkbox.setChecked(True)
                groupLayout.addWidget(checkbox)

            def accept():                       # delete all files that are still checked off
                still_marked = [check.text() for check in group.children() if isinstance(check, QtW.QCheckBox) and check.isChecked()]
                self.delete(still_marked)

            dialog.addButtons(layout, QtW.QDialogButtonBox.Cancel, QtW.QDialogButtonBox.No, QtW.QDialogButtonBox.Yes)
            dialog.accepted.connect(accept)
            dialog.exec()
            logging.info(f'Deletion dialog choice: {dialog.choice}')
            return dialog.choice
        except: self.log(f'(!) DELETION PROMPT FAILED: {format_exc()}')


    # -------------------------------
    # >>> UTILITY FUNCTIONS <<<
    # -------------------------------
    def log_slot(self, msg, timeout=20000):
        ''' Logs message from self.log signal and displays it on the GUI's status bar. '''
        logging.info(msg)
        self.statusbar.showMessage(msg, timeout)


    def log_on_player(self, text: str, timeout: int = 350, marq_key: str = '', log: bool = True):
        ''' Like log_slot, but displays `text` on-screen as a marquee as well. Actual
            logging can be skipped for less important messages with the `log` parameter.
            `marq_key` is the suffix for the appropriate marquee setting that this message
            should apply to. Example: marq_key='Save' -> checkTextOnSave.isChecked()? '''
        if log: self.log(text)
        else: self.statusbar.showMessage(text, 10000)
        check = self.dialog_settings.findChild(QtW.QCheckBox, f'checkTextOn{marq_key}')
        if check and check.isChecked(): show_text(text, timeout)


    def handle_updates(self, *args, _launch=False):
        ''' Handles validating/checking updates as well as updating the settings dialog. Updates
            are only validated on launch, and if 'update_report.txt' is present. Update checks only
            occur on launch if it has been spinUpdateFrequency days since the last check. The last
            check date is only saved down to the day so that checks on launch are more predictable. '''
        if self.checking_for_updates: return    # prevent spamming the "check for updates" button
        settings = self.dialog_settings

        if _launch:
            settings.labelLastCheck.setText(f'Last check: {cfg.lastupdatecheck or "never"}')
            settings.labelCurrentVersion.setText(f'Current version: {constants.VERSION}')
            settings.labelGithub.setText(settings.labelGithub.text().replace('?url', f'{constants.REPOSITORY_URL}/releases/latest'))
            update_report = os.path.join(constants.CWD, 'update_report.txt')
            if os.path.exists(update_report):
                import update
                update.validate_update(self, update_report)

        if not _launch or settings.checkAutoUpdateCheck.isChecked():
            try: last_check_time_seconds = mktime(strptime(cfg.lastupdatecheck, '%x'))  # string into seconds needs %x
            except: last_check_time_seconds = 0
            if not _launch or last_check_time_seconds + (86400 * settings.spinUpdateFrequency.value()) < get_time():
                self.log('Checking for updates...')
                self.checking_for_updates = True
                self.dialog_settings.buttonCheckForUpdates.setText('Checking for updates...')

                if constants.IS_COMPILED:       # if compiled, override cacert.pem path to get rid of pointless folder
                    import certifi.core
                    cacert_override_path = os.path.join(constants.BIN_DIR, 'cacert.pem')
                    os.environ["REQUESTS_CA_BUNDLE"] = cacert_override_path
                    certifi.core.where = lambda: cacert_override_path

                import update
                Thread(target=update.check_for_update, args=(self,)).start()

                cfg.lastupdatecheck = strftime('%#D', localtime())      # seconds into string needs %D
                settings.labelLastCheck.setText(f'Last check: {cfg.lastupdatecheck}')


    def _handle_updates(self, results: dict, popup_kwargs: dict):
        ''' A slot for update.check_for_update which cleans up and handles the results of an update
            check, if any, in a thread-safe manner. `results` is a dict containing either 'failed'
            to represent that there was an unusual error that could still indicate a pending update
            (mismatched URL format on Github, for example), or 'latest_version_url'. `popup_kwargs`
            are the keyword-arguments needed to construct the relevant QMessageBox. '''
        try:
            logging.info(f'Cleaning up after update check. results={results}')
            settings_were_open = self.dialog_settings.isVisible()       # hide the always-on-top settings while we show popups
            if settings_were_open: self.dialog_settings.hide()
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
                        download_path = os.path.join(constants.TEMP_DIR, filename)
                        update.download_update(self, latest_version, download_url, download_path)
                else: return qthelpers.getPopup(**popup_kwargs, **self.get_popup_location()).exec()  # non-windows version of popup
        finally:
            self.checking_for_updates = False
            self.dialog_settings.buttonCheckForUpdates.setText('Check for updates')
            if settings_were_open: self.dialog_settings.show()          # restore settings if they were originally open


    def get_popup_location(self):
        ''' Returns keyword arguments as a dictionary for the center-parameters of popups and dialogs. '''
        index = self.dialog_settings.comboDialogPosition.currentIndex()
        if index: widget = None
        elif not constants.APP_RUNNING:  # index is 0 but geometry isn't set yet, use cfg to get center of window
            x, y = cfg.pos
            w, h = cfg.size
            x += w / 2
            y += h / 2
            widget = (x, y)
        else: widget = self.vlc if self.vlc.height() >= 20 else self.frameGeometry()    # use VLC window if it's big enough
        return {'centerWidget': widget, 'centerScreen': index == 1, 'centerMouse': index == 2}


    def swap_slider_styles(self):
        ''' Used to switch between high-precision and low-precision sliders in update_slider_thread. '''
        self.swap_slider_styles_queued = True


    def set_frame_override(self, frame: int = 0):
        self.frame_override = frame


    def set_fullscreen(self, fullscreen: bool):
        ''' Toggles fullscreen-mode on and off. Saves window-state to self.was_maximized to
            remember if the window is maximized or not and restore the window accordingly. '''
        self.dockControls.setFloating(fullscreen)                       # FramelessWindowHint and WindowStaysOnTopHint not needed
        if fullscreen:  # TODO: figure out why dockControls won't resize in fullscreen mode -> strange behavior when showing/hiding control-frames
            current_screen = app.screenAt(self.mapToGlobal(self.rect().center()))   # fullscreen destination is based on center of window
            screen_size = current_screen.size()
            screen_geometry = current_screen.geometry()

            width_factor = self.dialog_settings.spinFullScreenWidth.value() / 100
            width = int(screen_size.width() * width_factor)
            height = sum(frame.height() for frame in (self.frameProgress, self.frameAdvancedControls) if frame.isVisible())
            x = int(screen_geometry.right() - ((screen_size.width() + width) / 2))  # adjust x/y values for screen's actual global position
            y = screen_geometry.bottom() - height

            self.dockControls.resize(width, height)
            #self.dockControls.setFixedWidth(width)         # TODO this is bad for DPI/scale and doesn't even fully get rid of the horizontal separator cursors. bandaid fix
            self.dockControls.move(x, y)
            self.dockControls.setWindowOpacity(self.dialog_settings.spinFullScreenMaxOpacity.value() / 100)     # opacity only applies while floating

            # if we're already hovering over the pending dockControls rect OR the video already ended (and we're not paused) -> lock fullscreen controls
            self.lock_fullscreen_ui = (not player.is_playing() and not self.is_paused) or QtCore.QRect(x, y, width, height).contains(QtGui.QCursor().pos())

            self.statusbar.setVisible(False)
            self.menubar.setVisible(False)                  # TODO should this be like set_crop_mode's version? this requires up to 2 alt-presses to open
            self.was_maximized = self.isMaximized()         # remember if we're maximized or not
            self.vlc.last_move_time = get_time()            # reset last_move_time, just in case we literally haven't moved the mouse yet
            return self.showFullScreen()                    # FullScreen with a capital S
        else:
            self.statusbar.setVisible(self.actionShowStatusBar.isChecked())
            self.menubar.setVisible(self.actionShowMenuBar.isChecked())
            #self.dockControls.setFixedWidth(QWIDGETSIZE_MAX)
            if self.was_maximized: self.showMaximized()
            else: self.showNormal()


    def set_playback_speed(self, rate: float):
        ''' Sets, saves, and displays the playback speed/rate for the video. '''
        player.set_rate(rate)
        gif_player.gif.setSpeed(rate * 100)
        self.playback_speed = rate
        if self.dialog_settings.checkTextOnSpeed.isChecked(): show_text(f'{rate:.2f}x', 1000)
        self.log(f'Playback speed set to {rate:.2f}x')


    def set_volume(self, volume):
        try:
            volume = int(volume * self.volume_boost)
            player.audio_set_volume(volume)
            player.audio_set_mute(False)
            self.sliderVolume.setEnabled(True)
            self.sliderVolume.setToolTip(f'{volume}%')
            if self.dialog_settings.checkTextOnVolume.isChecked(): show_text(f'{volume}%%', 200)
        except: logging.error(format_exc())
        self.update_title_signal.emit()


    def toggle_mute(self):
        try:
            muted = not bool(player.audio_get_mute())       # returns 1 or 0
            player.audio_set_mute(muted)
            self.sliderVolume.setEnabled(not muted)         # disabled if muted, enabled if not muted
            self.sliderVolume.setToolTip('Muted (M)' if muted else f'Unmuted ({get_volume_slider()}%)')
            if self.dialog_settings.checkTextOnMute.isChecked(): show_text('Muted (M)' if muted else f'Unmuted ({get_volume_slider()}%%)')
        except: logging.error(format_exc())


    def set_progressbar_visible(self, visible: bool):
        ''' Readjusts the advanced controls' margins based on whether or not the progress bar's frame is `visible`. '''
        self.frameProgress.setVisible(visible)
        self.frameAdvancedControls.layout().setContentsMargins(0, 0 if visible else 3, 0, 0 if self.statusbar.isVisible() else 3)       # left/top/right/bottom


    def set_statusbar_visible(self, visible: bool):
        ''' Readjusts the advanced controls' margins based on whether or not the status bar is `visible`. '''
        self.statusbar.setVisible(visible)
        self.frameAdvancedControls.layout().setContentsMargins(0, 0 if self.frameProgress.isVisible() else 3, 0, 0 if visible else 3)   # left/top/right/bottom


    def set_menubar_visible(self, visible: bool):
        if visible and self.actionCrop.isChecked():
            return self.actionShowMenuBar.setChecked(False)
        self.menubar.setVisible(visible)
        if not self.isMaximized() and not self.isFullScreen() and self.first_video_fully_loaded:    # do not resize until a video is loaded
            self.resize(self.width(), self.height() + (21 if visible else -21))  # resize window to preserve player size TODO DPI/scale issues probably


    def set_crop_mode(self, on):     # https://video.stackexchange.com/questions/4563/how-can-i-crop-a-video-with-ffmpeg
        if not self.video or self.mime_type == 'audio':     # reset crop mode if no video is playing
            return self.actionCrop.trigger() if on else None
        if not on: self.disable_crop_mode()
        else:
            vlc = self.vlc
            if self.actionShowMenuBar.isChecked():
                self.actionShowMenuBar.trigger()    # can't just set to False and reuse actionShowMenuBar.isChecked()...
                self.menubar_visible_before_crop = True     # ...since set_menubar_visible() is more involved than just doing setVisible
            else: self.menubar_visible_before_crop = False

            self.log('Crop mode enabled. Right-click or press C to exit.')
            vlc.find_true_borders()

            if not vlc.selection:
                vlc.selection = [
                    QtCore.QPoint(vlc.true_left + 20,  vlc.true_top + 20),     # 0 top left
                    QtCore.QPoint(vlc.true_right - 20, vlc.true_top + 20),     # 1 top right
                    QtCore.QPoint(vlc.true_left + 20,  vlc.true_bottom - 20),  # 2 bottom left
                    QtCore.QPoint(vlc.true_right - 20, vlc.true_bottom - 20)   # 3 bottom right
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
                                     P.TOP_RIGHT:    lambda _, y: s[1].setY(min(y, s[2].y() - 10)),
                                     P.BOTTOM_LEFT:  lambda x, _: s[2].setX(min(x, s[1].x() - 10))},
                    P.TOP_RIGHT:    {P.TOP_LEFT:     lambda _, y: s[0].setY(min(y, s[2].y() - 10)),
                                     P.TOP_RIGHT:    lambda x, y: (s[1].setX(max(x, s[2].x() + 10)), s[1].setY(min(y, s[2].y() - 10))),
                                     P.BOTTOM_RIGHT: lambda x, _: s[3].setX(max(x, s[0].x() + 10))},
                    P.BOTTOM_LEFT:  {P.TOP_LEFT:     lambda x, _: s[0].setX(min(x, s[1].x() - 10)),
                                     P.BOTTOM_LEFT:  lambda x, y: (s[2].setX(min(x, s[1].x() - 10)), s[2].setY(max(y, s[1].y() + 10))),
                                     P.BOTTOM_RIGHT: lambda _, y: s[3].setY(max(y, s[0].y() + 10))},
                    P.BOTTOM_RIGHT: {P.TOP_RIGHT:    lambda x, _: s[1].setX(max(x, s[0].x() + 10)),
                                     P.BOTTOM_LEFT:  lambda _, y: s[2].setY(max(y, s[0].y() + 10)),
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
                vlc.crop_frames = (  # can't reuse crop_frames alias here since it is None
                    QtW.QFrame(self),     # 0 top
                    QtW.QFrame(self),     # 1 left
                    QtW.QFrame(self),     # 2 right
                    QtW.QFrame(self),     # 3 bottom
                )

                for view in vlc.crop_frames:
                    view.mousePressEvent = vlc.mousePressEvent
                    view.mouseMoveEvent = vlc.mouseMoveEvent
                    view.mouseReleaseEvent = vlc.mouseReleaseEvent
                    view.mouseDoubleClickEvent = vlc.mouseDoubleClickEvent
                    view.setVisible(True)
                    view.setMouseTracking(True)
                    view.setStyleSheet('background: rgba(0, 0, 0, 115)')    # TODO add setting here?
            else:
                for view in vlc.crop_frames: view.setVisible(True)
            vlc.update_crop_frames()  # update crop frames and factored points
            while app.overrideCursor(): app.restoreOverrideCursor()         # reset cursor


    def disable_crop_mode(self):
        for view in self.vlc.crop_frames:
            view.setVisible(False)
            view.setMouseTracking(False)
        if self.menubar_visible_before_crop:
            self.actionShowMenuBar.trigger()
            self.menubar.setVisible(True)
            self.menubar_visible_before_crop = False
        self.vlc.setToolTip('')                                     # clear crop-size tooltip
        self.vlc.dragging = None                                    # clear crop-drag
        self.vlc.panning = False                                    # clear crop-pan
        while app.overrideCursor(): app.restoreOverrideCursor()     # reset cursor
        self.actionCrop.setChecked(False)
        self.log('Crop mode disabled.')


    def is_snap_mode_enabled(self):
        mime = self.mime_type
        if mime == 'video':
            if self.extension == 'gif': return self.dialog_settings.checkSnapGifs.isChecked()
            return self.dialog_settings.checkSnapVideos.isChecked()
        if mime == 'audio':
            if not gif_player.pixmap(): return False
            return self.dialog_settings.checkSnapArt.isChecked()
        if mime == 'image': return self.dialog_settings.checkSnapImages.isChecked()
        return False


    def snap_to_player_size(self, shrink=False, force_instant_resize=False):
        if self.video and not self.isMaximized() and not self.isFullScreen():
            vlc_size = self.vlc.size()
            expected_vlc_size = self.vsize.scaled(vlc_size, Qt.KeepAspectRatio)
            void_width = vlc_size.width() - expected_vlc_size.width()
            void_height = vlc_size.height() - expected_vlc_size.height()

            # default instant snap. normally this shrinks the window, but to mitigate this and have a more balanced...
            # ...resize, we snap twice - once to resize it bigger than needed, then again to shrink it back down
            if force_instant_resize or self.dialog_settings.checkSnapOnResize.checkState() == 2:
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
            if self.dialog_settings.checkClampOnResize.isChecked():
                frame_size = self.frameGeometry().size()
                screen = qthelpers.getScreenForRect(self.rect())
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


    def update_title(self):
        ''' Updates the window's titlebar using various variables, based on lineWindowTitleFormat. '''
        title = self.dialog_settings.lineWindowTitleFormat.text()
        if self.video:
            path = self.video
            basepath, name = os.path.split(path)
            parent = os.path.join(basepath.split(os.sep)[-1], name)
            base, ext = os.path.splitext(name)
            ext = ext[1:].upper()               # uppercase and strip '.' from beginning

            mime = self.mime_type.capitalize()  # capitalize first letter of mime type
            paused = '■' if get_progess_slider() == self.frame_count else '▷' if not self.is_paused else '𝗜𝗜'   # ▶
            h, m, s, _ = get_hms(self.duration)
            duration = f'{m}:{s:02}' if self.duration < 3600 else f'{h}:{m:02}:{s:02}'  # no milliseconds in window title
            if self.mime_type != 'audio':
                fps = str(self.frame_rate_rounded)
                size = f'{self.vwidth:.0f}x{self.vheight:.0f}'
            else:
                fps = '0'
                size = '0x0'
            ratio = self.ratio
        else:
            path = name = base = parent = 'No media is playing'
            ext = '?'
            mime = 'Unknown'
            paused = '■'    # ▁▂▃▄▅▇▉ ▊▋█ ❏ ?paused ?name (?duration | ?fpsfps)
            fps = '0'       # ?base | ?name | ?parent | ?path | ?ext | ?mime | ?paused | ?fps | ?duration | ?size | ?ratio | ?volume | ?speed
            duration = '--:--'
            size = '0x0'
            ratio = '0:0'

        replace = {'?base': base, '?name': name, '?parent': parent, '?path': path, '?ext': ext, '?mime': mime,
                   '?paused': paused, '?fps': fps, '?duration': duration, '?size': size, '?ratio': ratio,
                   '?volume': str(get_volume_slider()), '?speed': f'{player.get_rate():.2f}'}
        for var, val in replace.items(): title = title.replace(var, val)
        self.setWindowTitle(title.strip())


    def refresh_shortcuts(self, last_edit: widgets.QKeySequenceFlexibleEdit = None):
        # get list of all keySequenceEdits
        all_key_sequence_edits = []
        for layout in qthelpers.formGetItemsInColumn(self.dialog_settings.tabKeys.layout(), 1):
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
                for other_edit in all_key_sequence_edits:   # loop over every keySequenceEdit for every keySequenceEdit to compare all of them
                    if edit.keySequence() == other_edit.keySequence() and edit is not other_edit:
                        other_name = other_edit.objectName()
                        other_index = 0 if other_name[-1] != '_' else 1
                        other_name = other_name.rstrip('_')
                        other_edit.setKeySequence(0)
                        self.shortcuts[other_name][other_index].setKey(other_edit.keySequence())
                self.shortcuts[name][index].setKey(edit.keySequence())


    def cycle_subtitle_track(self):
        track_count = player.video_get_spu_count() - 1
        if track_count > 0:
            new_track = player.video_get_spu() - 1     # disabled = -1, track #1 = 2. Yeah.
            self.set_track('subtitle', -1 if new_track == track_count else 0 if new_track == -2 else new_track)
        else: self.log_on_player('No subtitles available', marq_key='SubtitleChanged', log=False)


    def set_track(self, track_type, track=-1):
        types = {'video': (1, -1, player.video_set_track),
                 'audio': (2, 0, player.audio_set_track),
                 'subtitles': (2, 1, player.video_set_spu)}
        track_offset, offset_from_1, set_track = types[track_type]

        if not isinstance(track, int): track = track.data()
        else: track += track_offset if track != -1 else 0
        set_track(track)
        if track >= 0: self.log_on_player(f'{track_type.title().rstrip("s")} track {track - offset_from_1} enabled', marq_key='SubtitleChanged', log=False)
        else: self.log_on_player(f'{track_type.title()} disabled', marq_key='SubtitleChanged', log=False)
        gc.collect(generation=2)


    def refresh_track_menu(self, menu: QtW.QMenu):
        menus = {self.menuVideoTracks: ('video', player.video_get_track_description, player.video_get_track, player.video_get_track_count, 2, -1),
                 self.menuAudioTracks: ('audio', player.audio_get_track_description, player.audio_get_track, player.audio_get_track_count, 1, 0),
                 self.menuSubtitles:   ('subtitles', player.video_get_spu_description, player.video_get_spu, player.video_get_spu_count, 1, 0)}
        string, get_description, get_track, get_count, count_offset, minimum_tracks = menus[menu]

        menu.clear()      # clear previous contents of menu
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

            for track_index, track_title in get_description():  # find track number in title -> add &-shortcut
                name_parts = track_title.decode().split()
                new_parts = []
                for index, part in enumerate(name_parts):
                    if part.isnumeric():                        # track number identified, add &-shortcut and stop
                        new_parts.append('&' + part)
                        new_parts.extend(name_parts[index + 1:])
                        break
                    else: new_parts.append(part)
                track_name = ' '.join(new_parts)

                action = QtW.QAction(track_name, action_group)  # get_spu_description includes pre-generated track titles with tags -> VLC uses the last...
                action.setData(track_index)                     # ...non-extension keyword separated by a period in the filename as the track's tag
                action.setCheckable(True)                       # e.g. 'dawnofthedead.2004.ENG.srt' -> 'Track 1 - [ENG]'
                if current_track == track_index:                # originally I was doing all of that manually, while juggling the random inconsistent indexes
                    action.setChecked(True)
                menu.addAction(action)
        else:
            action = QtW.QAction(f'No {string} tracks', menu)   # The parent is required here for this action. Here and here alone. I don't know why.
            action.setEnabled(False)
            menu.addAction(action)


    def refresh_recent_menu(self):
        ''' Clears and refreshes the recent files submenu. '''
        self.menuRecent.clear()
        get_open_lambda = lambda path: lambda: self.open(path) if os.path.exists(path) else (self.log(f'Recent file {path} does not exist anymore.'), self.recent_videos.remove(path))
        for index, video in enumerate(reversed(self.recent_videos)):         # reversed to show most recent first
            action = QtW.QAction(f'&{index + 1}. {os.path.basename(video)}', self.menuRecent)
            action.triggered.connect(get_open_lambda(video))                 # workaround for python bug/oddity involving creating lambdas in iterables
            action.setToolTip(video)
            self.menuRecent.addAction(action)
        self.menuRecent.addSeparator()
        self.menuRecent.addAction(self.actionClearRecent)                    # add separator and clear action at bottom


    def navigate(self, forward=True, seconds=5):    # slightly longer than it could be, but cleaner/more readable
        if self.mime_type == 'image': return self.cycle_media(next=forward)  # cycle images with basic navigation keys
        old_frame = get_progess_slider()
        if forward:                                 # media will wrap around cleanly if it goes below 0/above max frames
            if old_frame == self.frame_count and self.dialog_settings.checkNavigationWrap.isChecked(): new_frame = 0
            else: new_frame = min(self.frame_count, old_frame + self.frame_rate_rounded * seconds)
        else:   # TODO use vvv this line vvv as workaround to VLC bug that sometimes causes media to play 1 frame when wrapping?
            #if old_frame <= 1 and self.dialog_settings.checkNavigationWrap.isChecked(): new_frame = self.frame_count
            if old_frame == 0 and self.dialog_settings.checkNavigationWrap.isChecked(): new_frame = self.frame_count
            else: new_frame = max(0, old_frame - self.frame_rate_rounded * seconds)
        set_and_update_progress(new_frame)
        if self.restarted and self.dialog_settings.checkNavigationUnpause.isChecked(): self.pause()  # auto-unpause after restart
        if self.isFullScreen() and self.dialog_settings.checkTextOnFullScreenPosition.isChecked():   # if we're in fullscreen mode, show the current position as a marquee
            h, m, s, _ = get_hms(self.current_time)
            current_text = f'{m:02}:{s:02}' if self.current_time < 3600 else f'{h}:{m:02}:{s:02}'
            max_text = self.labelMaxTime.text()[:-3] if self.duration < 3600 else self.labelMaxTime.text()
            show_text(f'{current_text}/{max_text}')


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
        if self.restarted and self.dialog_settings.checkNavigationUnpause.isChecked(): self.pause()  # auto-unpause after restart


    def mark_for_deletion(self, checked: bool = False, file=None, modifiers=None):
        if not self.video:
            if checked: self.actionMarkDeleted.trigger()
            return self.statusbar.showMessage('No media is playing.', 10000)
        file = file or self.video
        logging.info(f'Marking file {file} for deletion: {checked}')
        mod = app.keyboardModifiers() if modifiers is None else modifiers

        if file and mod & Qt.ControlModifier: self.delete(file)                     # ctrl pressed -> immediately delete video
        elif mod & Qt.ShiftModifier: self.show_delete_prompt()                      # shift pressed -> show deletion prompt
        elif checked and file: self.marked_for_deletion.add(file)
        elif not checked:
            try: self.marked_for_deletion.remove(file)
            except (ValueError, KeyError): pass
            except: self.log(f'(!) MARK_FOR_DELETION FAILED: {format_exc()}')
        tooltip_count_string = f'{len(self.marked_for_deletion)} file{"s" if len(self.marked_for_deletion) == 1 else ""}'
        self.buttonMarkDeleted.setToolTip(constants.MARK_DELETED_TOOLTIP_BASE.replace('?count', tooltip_count_string))


    def clear_marked_for_deletion(self):
        self.marked_for_deletion.clear()
        self.actionMarkDeleted.setChecked(False)
        self.buttonMarkDeleted.setChecked(False)
        self.buttonMarkDeleted.setToolTip(constants.MARK_DELETED_TOOLTIP_BASE.replace('?count', '0'))


    def snapshot(self, *args, modifiers=None):  # uses libvlc_video_take_snapshot. *args to capture unused signal args
        ''' libvlc_video_take_snapshot's docstring:         TODO: add a real docstring here
            "Take a snapshot of the current video window. If `i_width` AND `i_height` is 0, original
            size is used. If `i_width` XOR `i_height` is 0, original aspect-ratio is preserved."
            Returns: 0 on success, -1 if the video was not found.
            Parameters:
                `p_mi` - media player instance.
                `num` - number of video output (typically 0 for the first/only one).
                `psz_filepath` - the path of a file or a folder to save the screenshot into.
                `i_width` - the snapshot's width.
                `i_height` - the snapshot's height. '''
        try:
            d_set = self.dialog_settings
            if d_set.checkSnapshotPause.isChecked(): player.set_pause(True)    # pause video if desired (undone by finally statement)
            mod = app.keyboardModifiers() if modifiers is None else modifiers

            # no modifiers -> quick snapshot, no dialogs TODO: maybe add default width/height scale settings
            if not mod:
                if not self.video: return self.statusbar.showMessage('No video is playing.', 10000)
                if self.mime_type != 'video':
                    if self.mime_type == 'image' and self.actionCrop.isChecked(): return self.statusbar.showMessage('Images must be cropped directly, without snapshots.', 10000)
                    else: return self.statusbar.showMessage('You can only take snapshots of a video.', 10000)

                # get default snapshot name (done here in case shift is pressed -> faster to have shift section later)
                name_format = d_set.lineSnapshotNameFormat.text().strip() or d_set.lineSnapshotNameFormat.placeholderText()
                date_format = d_set.lineSnapshotDateFormat.text().strip() or d_set.lineSnapshotDateFormat.placeholderText()
                video_basename = os.path.basename(os.path.splitext(self.video)[0])
                default_name = name_format.replace('?video', video_basename).replace('?date', strftime(date_format, localtime()))

                format = d_set.comboSnapshotFormat.currentText()
                dirname = os.path.expandvars(d_set.lineDefaultSnapshotPath.text().strip() or os.path.dirname(default_name))
                try: os.makedirs(dirname)
                except FileExistsError: pass

                # take and save snapshot
                path = get_unique_path(f'{os.path.join(dirname, default_name)}.{"jpg" if format == "JPEG" else "png"}', key='?count')
                player.video_take_snapshot(num=0, psz_filepath=path, i_width=0, i_height=0)
                cfg.last_snapshot_path = os.path.abspath(path)
                self.log(f'Snapshot saved to {path}')

                # crop final snapshot if desired
                if self.actionCrop.isChecked():
                    logging.info('Cropping previously saved snapshot...')
                    lfp = self.vlc.last_factored_points
                    image_data = get_PIL_Image().open(path)
                    image_data = image_data.crop((round(lfp[0].x()), round(lfp[0].y()),     # left/top/right/bottom (crop takes a tuple)
                                                  round(lfp[1].x()), round(lfp[2].y())))    # round QPointFs
                    if format == 'JPEG': self.convert_snapshot_to_jpeg(path, image_data)
                    else: image_data.save(path)

                # VLC doesn't support jpeg snapshots -> convert manually https://www.geeksforgeeks.org/convert-png-to-jpg-using-python/
                elif format == 'JPEG': self.convert_snapshot_to_jpeg(path)

            # ctrl pressed -> show resize + save-file dialog
            elif mod & Qt.ControlModifier:
                if not self.video: return self.statusbar.showMessage('No video is playing.', 10000)
                if self.mime_type != 'video':
                    if self.mime_type == 'image' and self.actionCrop.isChecked(): return self.statusbar.showMessage('Images must be cropped directly, without snapshots.', 10000)
                    else: return self.statusbar.showMessage('You can only take snapshots of a video.', 10000)

                player.set_pause(True)     # player may have already been paused earlier, but it DEFINITELY needs to be paused now
                try:
                    # get default snapshot name (done here in case shift is pressed -> faster to have shift section later)
                    name_format = d_set.lineSnapshotNameFormat.text().strip() or d_set.lineSnapshotNameFormat.placeholderText()
                    date_format = d_set.lineSnapshotDateFormat.text().strip() or d_set.lineSnapshotDateFormat.placeholderText()
                    video_basename = os.path.basename(os.path.splitext(self.video)[0])
                    default_name = name_format.replace('?video', video_basename).replace('?date', strftime(date_format, localtime()))

                    width, height = self.get_size_dialog()
                    if width is None: return                        # dialog cancelled (finally-statement ensures we unpause if needed)

                    # open save-file dialog
                    use_snapshot_lastdir = d_set.checkSnapshotRemember.isChecked()
                    selected_filter = 'JPEG (*.jpg; *.jpeg; *.jpe; *.jfif; *.exif)' if d_set.comboSnapshotFormat.currentText() == 'JPEG' else ''
                    directory = os.path.join(cfg.last_snapshot_folder if use_snapshot_lastdir else cfg.lastdir, default_name)
                    directory = f'{directory}{".png" if not selected_filter else ".jpg"}'
                    path, filter, lastdir = qthelpers.saveFile(lastdir=get_unique_path(directory, key='?count', zeros=1),
                                                               caption='Save snapshot as',
                                                               filter='PNG (*.png);;JPEG (*.jpg; *.jpeg; *.jpe; *.jfif; *.exif);;All files (*)',
                                                               selectedFilter=selected_filter,
                                                               returnFilter=True)
                    if use_snapshot_lastdir: cfg.last_snapshot_folder = lastdir
                    else: cfg.lastdir = lastdir
                    if path is None: return
                    # 'BMP (*.bmp; *.dib, *.rle);;TIFF (*.tiff; *.tif);;GIF (*.gif);;TGA (*.tga);;WebP (*.webp)'

                    # take and save snapshot
                    player.video_take_snapshot(num=0, psz_filepath=path, i_width=width, i_height=height)
                    logging.info(f'psz_filepath={path}, i_width={width}, i_height={height}')
                    cfg.last_snapshot_path = os.path.abspath(path)
                    cfg.last_snapshot_folder = os.path.dirname(cfg.last_snapshot_path)
                    self.log(f'Snapshot saved to {path}')

                    # crop final snapshot if desired, taking into account the custom width/height
                    if self.actionCrop.isChecked():
                        logging.info('Cropping previously saved snapshot...')
                        lfp = self.vlc.last_factored_points
                        image_data = get_PIL_Image().open(path)

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
                        image_data = image_data.crop((round(lfp[0].x() / x_factor), round(lfp[0].y() / y_factor),   # left/top/right/bottom (crop takes a tuple)
                                                      round(lfp[1].x() / x_factor), round(lfp[2].y() / y_factor)))  # round QPointFs

                        if filter[:4] == 'JPEG': self.convert_snapshot_to_jpeg(path, image_data)
                        else: image_data.save(path)

                    # VLC doesn't support jpeg snapshots -> convert manually https://www.geeksforgeeks.org/convert-png-to-jpg-using-python/
                    if filter[:4] == 'JPEG': self.convert_snapshot_to_jpeg(path)

                except: self.log(f'(!) NORMAL/CUSTOM SNAPSHOT FAILED: {format_exc()}')
                finally: player.set_pause(False or self.is_paused)  # only needed if checkSnapshotPause is False

            # shift pressed -> open last snapshot in pyplayer (not in explorer)
            elif mod & Qt.ShiftModifier:
                if not cfg.last_snapshot_path: return self.statusbar.showMessage('No snapshots have been taken yet.', 10000)
                if not os.path.exists(cfg.last_snapshot_path): return self.log(f'Previous snapshot at {cfg.last_snapshot_path} no longer exists.')
                self.open(cfg.last_snapshot_path)
                self.log(f'Opening last screenshot at {cfg.last_snapshot_path}.')

            # alt pressed -> open last snapshot in default program (not in explorer)
            elif mod & Qt.AltModifier:
                if not cfg.last_snapshot_path: return self.statusbar.showMessage('No snapshots have been taken yet.', 10000)
                if not os.path.exists(cfg.last_snapshot_path): return self.log(f'Previous snapshot at {cfg.last_snapshot_path} no longer exists.')
                qthelpers.openPath(cfg.last_snapshot_path)
                self.log(f'Opening last screenshot at {cfg.last_snapshot_path}.')
        except: self.log(f'(!) SNAPSHOT FAILED: {format_exc()}')
        finally: player.set_pause(False or self.is_paused)


    def convert_snapshot_to_jpeg(self, path, image_data=None):      # https://www.geeksforgeeks.org/convert-png-to-jpg-using-python/
        ''' Saves image at `path` as a JPEG file with the desired quality in the settings
            dialog, using PIL. Assumes that `path` already ends in a valid file-extension. '''
        jpeg_quality = self.dialog_settings.spinSnapshotJpegQuality.value()
        self.log(f'Saving JPEG snapshot at {jpeg_quality}% quality to {path}.')
        if image_data is None: image_data = get_PIL_Image().open(path)
        image_data.convert('RGB')
        image_data.save(path, quality=jpeg_quality)


#######################################
if __name__ == "__main__":
    if not constants.IS_COMPILED:
        import executable.hook                  # manually import launch-hook when running from script
        from PIL import Image                   # get_PIL_Image sometimes hangs on import when running from script
    try:
        logging.info(f'PyPlayer opened at {constants.SCRIPT_PATH} with executable {sys.executable}')
        logging.info('Creating QApplication and GUI...')
        app = QtW.QApplication(sys.argv)        # init qt
        gui = GUI_Instance(app)                 # init empty GUI instance
        gui.setup()                             # setup gui's variables, widgets, and threads (0.3mb)

        # -----------------------------------------------
        # Aliases for time-sensitive functions/variables
        # -----------------------------------------------
        player = gui.vlc.player
        gif_player = gui.gifPlayer
        show_text = gui.vlc.show_text
        update_progress = gui.update_progress
        update_progress_signal = gui.update_progress_signal
        set_and_update_progress = gui.set_and_update_progress
        set_volume_slider = gui.sliderVolume.setValue
        get_volume_slider = gui.sliderVolume.value
        get_volume_scroll_increment = gui.dialog_settings.spinVolumeScroll.value
        get_progess_slider = gui.sliderProgress.value
        set_progress_slider = gui.sliderProgress.setValue
        set_pause_button_text = gui.buttonPause.setText
        set_hour_spin = gui.spinHour.setValue
        set_minute_spin = gui.spinMinute.setValue
        set_second_spin = gui.spinSecond.setValue
        set_frame_spin = gui.spinFrame.setValue
        set_player_position = player.set_position
        set_gif_position = gif_player.gif.jumpToFrame
        set_current_time_text = gui.lineCurrentTime.setText
        current_time_lineedit_has_focus = gui.lineCurrentTime.hasFocus

        gui.show()                                              # begin showing UI
        qtstart.connect_widget_signals(gui)                     # connect signals and slots
        cfg = config.loadConfig(gui, constants.CONFIG_PATH)     # create and load config
        gui.refresh_theme_combo(set_theme=cfg.theme)            # load and set themes
        widgets.init_custom_widgets(cfg, app)                   # set config and app as global objects in widgets.py
        constants.verify_ffmpeg(gui, warning=True)              # confirm/look for valid ffmpeg path if needed
        FFPROBE = constants.verify_ffprobe(gui, warning=True)   # confirm/look/return valid ffprobe path if needed

        with open(constants.PID_PATH, 'w'):     # create PID file
            gui.handle_updates(_launch=True)    # check for/download/validate pending updates
            qtstart.after_show_setup(gui)       # finish up any last second setup
            gc.collect(generation=2)            # final garbage collection before starting
            logging.info(f'Starting GUI after {get_time() - constants.SCRIPT_START_TIME:.2f} seconds.')

            if gui.dialog_settings.groupTray.isChecked():       # start system tray icon
                logging.info('Creating system tray icon...')
                app.setQuitOnLastWindowClosed(False)            # ensure qt does not exit until we tell it to
                gui.tray_icon = qtstart.get_tray_icon(gui)
            else: gui.tray_icon = None

            constants.APP_RUNNING = True
            try: app.exec()
            except: logging.critical(f'(!) GUI FAILED TO EXECUTE: {format_exc()}')
            logging.info('Application execution has finished.')
        try: os.remove(constants.PID_PATH)
        except: logging.warning('(!) Failed to remove PID file:' + format_exc())
    except: logging.critical(f'(!) SCRIPT FAILED TO INITIALIZE: {format_exc()}')
