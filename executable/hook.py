''' Runtime hook that takes the place of launcher.pyw. Runtime hooks run before
    the actual script runs. Communicates with active PyPlayer instances through
    their PID files, typically by sending the most recently opened instance a
    file that the user wants to open and then exiting the current instance, so
    as to skip re-opening PyPlayer. Also cleans temp folder and uses sys.path
    magic to hide our .dll, .pyd, and libvlc files in alternate directories.
    thisismy-github -> launcher.pyw: 2/1/22, hook.py: 4/8/22, combined: 4/13/22 '''

import sys
import os


CWD = os.path.dirname(sys.argv[0])
TEMP_DIR = os.path.join(CWD, 'PyQt5', 'temp')


''' If a file is specified, check for running instances and send the file to
    the latest one by writing a text file with an encoded path and a specially
    formatted name, then signal to our current instance that it should exit. '''
try:
    filepath = sys.argv[1]
    pids = (os.path.join(TEMP_DIR, file) for file in os.listdir(TEMP_DIR) if file[-4:] == '.pid')   # get all .pid files
    for pid in reversed(sorted(pids, key=os.path.getctime)):                # sort by age then reverse (newest first)
        try: os.remove(pid)                                                 # attempt to delete pid -> PermissionError = active
        except PermissionError:                                             # pid file in use -> send path to its instance
            cmdpath = os.path.join(TEMP_DIR, f'cmd.{os.path.basename(pid)[:-4]}.txt')   # cmd.{pid}.txt
            with open(cmdpath, 'wb') as txt: txt.write(filepath.encode())   # encode path and write to cmd file
            sys.argv.append('?EXIT')                                        # add exit flag to args so this instance exits

            # cmd file sent, clean temp folder while user waits for other instance to open
            import time
            now = time.time()
            max_age = 30                            # NOTE: Values < 15 seconds may result in unusual behavior on Windows

            for file in os.listdir(TEMP_DIR):
                file = os.path.join(TEMP_DIR, file)
                if not os.path.isfile(file): continue
                stat = os.stat(file)
                if now > stat.st_atime + max_age:   # check if file is > max_age seconds old using "last accessed" time
                    try: os.remove(file)            # delete outdated file
                    except: pass
            break                                   # break out of pid-loop
except (IndexError, FileNotFoundError): pass        # no file specified, or temp folder doesn't exist
except:                                             # unexpected serious error -> setup logging and log error
    import logging
    from traceback import format_exc
    logging.basicConfig(filename=os.path.join(CWD, 'LAUNCHER_ERROR.log'),
                        filemode='a', datefmt='%m/%d/%y | %I:%M:%S%p', style='{',
                        format='{asctime} {lineno:<3} {levelname} {funcName}: {message}')
    message = '(!) Unexpected error while launching -'
    logging.error(f'{message} {format_exc()}')


##############################################################################
''' Add PyQt5 to sys.path and create VLC environment variables (if needed)
    so we can hide our .dll, .pyd, and libvlc files in alternate folders. '''
sys.path.append(os.path.join(CWD, 'PyQt5'))

VLC_PATH = os.path.join(CWD, 'plugins', 'vlc')
LIB_PATH = os.path.join(VLC_PATH, 'libvlc.dll')
MODULE_PATH = os.path.join(VLC_PATH, 'plugins')
if 'PYTHON_VLC_LIB_PATH' not in os.environ and os.path.exists(LIB_PATH):
    os.environ['PYTHON_VLC_LIB_PATH'] = LIB_PATH
if 'PYTHON_VLC_MODULE_PATH' not in os.environ and os.path.exists(MODULE_PATH):
    os.environ['PYTHON_VLC_MODULE_PATH'] = MODULE_PATH
