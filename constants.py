''' Contains a number of constants used throughout the project that were originally
    at the top of several files. Unlike qtstart.py, I think this one will stay.
    thisismy-github 3/14/22 '''

import config
import qthelpers

import os
import sys
import time

# ---------------------

VERSION = 'pyplayer 0.1.1 beta'
REPOSITORY_URL = 'https://github.com/thisismy-github/pyplayer'
SCRIPT_START_TIME = time.time()

# ---------------------

IS_COMPILED = getattr(sys, 'frozen', False)
SCRIPT_PATH = sys.executable if IS_COMPILED else os.path.realpath(__file__)
CWD = os.path.dirname(SCRIPT_PATH)

BIN_DIR = os.path.join(CWD, 'bin')
TEMP_DIR = os.path.join(CWD, 'temp')
THEME_DIR = os.path.join(CWD, 'themes')
RESOURCE_DIR = os.path.join(THEME_DIR, 'resources')
LOG_PATH = os.path.join(CWD, 'pyplayer.log')
CONFIG_PATH = os.path.join(CWD, 'config.ini')
PID_PATH = os.path.join(TEMP_DIR, str(os.getpid()))

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

MARK_DELETED_TOOLTIP_BASE = '''Mark media for future deletion.
?count are currently marked for deletion.

Shortcuts:
Shift + click: Show deletion-confirmation prompt.
Ctrl + click: Immediately delete current media.

Right-click for more options. Deletion-confirmation
prompt is shown on exit if any files are marked.'''

# ---------------------

FFMPEG = 'ffmpeg.exe' if IS_COMPILED else os.path.join(BIN_DIR, 'ffmpeg.exe')

def verify_ffmpeg():
    popup_text = 'ffmpeg was not detected in the bin folder, your install folder,\n' \
                 'or your system PATH variable. ffmpeg is used for editing.\n\n' \
                 'Without it, editing features will not function. It should have been\n' \
                 'included with your download. If it wasn\'t, download the ffmpeg\n' \
                 'essentials below, or click "Cancel" to stop receiving this warning.'
    popup_text_informative = '<a href=https://ffmpeg.org/download.html>https://ffmpeg.org/download.html</a>'

    if not os.path.exists(FFMPEG):
        from PyQt5.QtWidgets import QMessageBox
        if config.cfg.ffmpegwarningignored:
            import logging
            logging.getLogger('constants.py').warning('(!) ffmpeg not detected in /bin folder. Assuming it is still accessible.')
        else:
            if not qthelpers.file_in_PATH('ffmpeg.exe') and not os.path.exists('ffmpeg.exe'):
                choice = qthelpers.getPopupOkCancel(title='ffmpeg not detected',
                                                    text=popup_text,
                                                    textInformative=popup_text_informative,
                                                    icon=QMessageBox.Warning).exec()
                if choice == QMessageBox.Cancel: config.cfg.ffmpegwarningignored = True
