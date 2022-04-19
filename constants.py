''' Contains a number of constants used throughout the project
    that were originally spread across the tops of several files.
    thisismy-github 3/14/22 '''

import config
import qthelpers

import os
import sys
import time
import platform

# ---------------------

VERSION = 'pyplayer 0.2.0 beta'
REPOSITORY_URL = 'https://github.com/thisismy-github/pyplayer'

# ---------------------

SCRIPT_START_TIME = time.time()
IS_COMPILED = getattr(sys, 'frozen', False)
PLATFORM = platform.system()
SCRIPT_PATH = sys.executable if IS_COMPILED else os.path.realpath(__file__)
CWD = os.path.dirname(SCRIPT_PATH)

BIN_DIR = os.path.join(CWD, 'bin' if not IS_COMPILED else 'PyQt5')
TEMP_DIR = os.path.join(BIN_DIR, 'temp')
THEME_DIR = os.path.join(CWD, 'themes')
RESOURCE_DIR = os.path.join(THEME_DIR, 'resources')
LOG_PATH = os.path.join(CWD, 'pyplayer.log')
CONFIG_PATH = os.path.join(CWD, 'config.ini')
PID_PATH = os.path.join(TEMP_DIR, f'{os.getpid()}.pid')

THUMBNAIL_DIR = os.path.join(TEMP_DIR, 'thumbnails')
for _dir in (THEME_DIR, TEMP_DIR, THUMBNAIL_DIR):
    try: os.makedirs(_dir)
    except: continue

# ---------------------

SUBTITLE_EXTENSIONS = ('.cdg', '.idx', '.srt', '.sub', '.utf', '.ass', '.ssa', '.aqt', '.jss',
                       '.psb', '.it', '.sami', 'smi', '.txt', '.smil', '.stl', '.usf', '.dks',
                       '.pjs', '.mpl2', '.mks', '.vtt', '.tt', '.ttml', '.dfxp', '.scc')

SPECIAL_TRIM_EXTENSIONS = ('x-msvideo', 'quicktime', 'x-flv', 'webm', 'mpeg', 'ogg')

# ---------------------

TRIM_BUTTON_TOOLTIP_BASE = '''Click to set the starting position of a trim/
the point where the intro fade will stop.

Currently in ?mode mode.
Right-click for more options.'''

MARK_DELETED_TOOLTIP_BASE = '''Mark media for future deletion.
?count are currently marked for deletion.

Shortcuts:
Shift + click: Show deletion-confirmation prompt.
Ctrl + click: Immediately delete current media.

Right-click for more options. Deletion-confirmation
prompt is shown on exit if any files are marked.'''

# ---------------------

if IS_COMPILED: FFMPEG = os.path.join(CWD, 'plugins', 'ffmpeg')
else: FFMPEG = os.path.join(BIN_DIR, 'ffmpeg')


def verify_ffmpeg(warning: bool = True, force_warning: bool = False) -> str:
    ''' Checks, sets, and returns constants.FFMPEG if it's present in the
        bin/PyQt/root folders, or the user's PATH variable. If not, FFMPEG is
        set to ''. If `warning` is True, a popup is displayed unless the user
        clicks 'Cancel' on one of the popups. If `force_warning` is True and
        constants.FFMPEG is missing, a popup is displayed no matter what. '''
    global FFMPEG
    expected_path = (FFMPEG + '.exe') if PLATFORM == 'Windows' else FFMPEG
    filename = 'ffmpeg.exe' if PLATFORM == 'Windows' else 'ffmpeg'
    if not os.path.exists(expected_path):                   # FFmpeg not in expected path
        if os.path.exists(filename):
            FFMPEG = os.path.realpath(filename)             # ffmpeg.exe exists in root
            if PLATFORM == 'Windows': FFMPEG = FFMPEG[:-4]  # strip '.exe'
        else:
            import logging
            warn = logging.getLogger('constants.py').warning
            FFMPEG = qthelpers.getFromPATH(filename)
            if FFMPEG == '':
                if config.cfg.ffmpegwarningignored and not force_warning:
                    warn('(!) FFmpeg not detected in /bin folder. Assuming it is still accessible.')
                elif warning or force_warning:
                    _display_ffmpeg_warning(forced=force_warning)
            warn('FFmpeg not detected in /bin folder. Current FFMPEG constant: ' + FFMPEG)
    return FFMPEG


def _display_ffmpeg_warning(forced: bool = True) -> None:
    import logging
    from PyQt5.QtWidgets import QMessageBox
    dir_name = 'plugins' if IS_COMPILED else 'bin'
    warning_text = '.' if forced else ', or click\n"Cancel" to stop receiving this warning.'
    popup_text = f'FFmpeg was not detected in the {dir_name} folder, your install folder,\n' \
                 'or your system PATH variable. FFmpeg is used for editing.\n\n' \
                 'Without it, editing features will not function. For Windows\n' \
                 'users, it should have been included with your download.\n' \
                 'If it wasn\'t, download the FFmpeg essentials below' + warning_text
    popup_text_informative = '<a href=https://ffmpeg.org/download.html>https://ffmpeg.org/download.html</a>'
    choice = qthelpers.getPopupOkCancel(title='FFmpeg not detected',
                                        text=popup_text,
                                        textInformative=popup_text_informative,
                                        icon=QMessageBox.Warning).exec()
    if not forced and choice == QMessageBox.Cancel: config.cfg.ffmpegwarningignored = True
    logging.getLogger('constants.py').warning('FFmpeg not detected in /bin folder. Current FFMPEG constant: ' + FFMPEG)
