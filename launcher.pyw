''' Not actually PyPlayer, but a dedicated launcher for PyPlayer, meant to
    create and communicate with active PyPlayer instances through their PID
    files. The typical usage is to send the most recently opened instance a
    file that the user wants to open, so as to skip re-opening PyPlayer.
    thisismy-github 2/1/22 '''

import time
LAUNCHER_START_TIME = time.time()

import os
import sys
import glob
import subprocess


CMD_DELETION_TIMEOUT = 30                                   # WARNING: Values < 15 seconds may result in unusual behavior on Windows.
EXECUTABLE_NAME = 'main.exe'
SCRIPT_NAME = 'main.pyw'

# ---

CWD = os.path.dirname(os.path.realpath(__file__))
TEMP_DIR = os.path.join(CWD, 'temp')
if getattr(sys, 'frozen', False): LAUNCH_CMD = os.path.join(CWD, EXECUTABLE_NAME)
else: LAUNCH_CMD = f'{sys.executable} {SCRIPT_NAME}'


def log_error(message=''):
    import logging
    import traceback
    logging.basicConfig(
        level=logging.info,
        format='{asctime} {lineno:<3} {levelname} {funcName}: {message}',
        datefmt='%m/%d/%y | %I:%M:%S%p',
        style='{',
        filename=os.path.join(CWD, 'launcher_error.log'),
        filemode='w')
    logging.error(f'{message} {traceback.format_exc()}')


def get_latest_instance():
    latest_pid = False
    pids = glob.glob(os.path.join(TEMP_DIR, '*.pid'))       # get all .pid files
    pids.sort(key=os.path.getctime)                         # sort by age (oldest to newest)
    for pid in reversed(pids):
        try:
            os.remove(pid)                                  # attempt to delete pid -> active pids throw PermissionErrors
            #logging.info(f'PID file {pid} has been deleted.')
        except PermissionError:
            if not latest_pid: latest_pid = os.path.basename(pid)[:-4]  # set most recent active pid and strip ".pid"
            #logging.info(f'PID file {pid} is in use.')      # do not return yet, continue deleting outdated pid files
    return latest_pid                                       # return pid or False if no active pids were found


def clean_temp_folder():
    cmds = glob.glob(os.path.join(TEMP_DIR, 'cmd.*.txt'))   # get all stray cmd files
    now = time.time()
    for cmd in cmds:
        stat = os.stat(cmd)
        #logging.info(f'\nCMD file: {cmd}\nCurrent time: {now}\nCMD_DELETION_TIMEOUT: {CMD_DELETION_TIMEOUT}\nCMD file stats: {stat}')
        if now > stat.st_atime + CMD_DELETION_TIMEOUT:      # check if cmd file is > CMD_DELETION_TIMEOUT seconds old using "last accessed" time
            #logging.info(f'Deleting outdated cmd file: {cmd} {os.stat(cmd)}')
            try: os.remove(cmd)                             # delete outdated cmd file
            except: log_error(f'Failed to delete outdated cmd file {cmd} -')


#######################################
if __name__ == "__main__":
    try:
        #logging.info(f'Interface opened. {len(sys.argv)} argument(s) detected: {sys.argv}')
        #logging.info(f'Base launch command: {LAUNCH_CMD}')
        if len(sys.argv) == 1: subprocess.Popen(LAUNCH_CMD, shell=True)    # no file specified -> run base script immediately
        else:                                               # file specified -> check if base script is running
            #logging.info(f'Opening argument #1 as media: {sys.argv[1]}')
            filepath = sys.argv[1]                          # get specified file
            if (pid := get_latest_instance()):              # if already running, send file to base script
                cmdpath = os.path.join(TEMP_DIR, f'cmd.{pid}.txt')
                with open(cmdpath, 'wb') as txt:
                    txt.write(filepath.encode())            # encode path to support special characters
                    #logging.info(f'CMD file opened as {txt}.')
                #logging.info(f'CMD file successfully written for PID #{pid} to {filepath}.')
            else: subprocess.Popen(f'{LAUNCH_CMD} "{filepath}"', shell=True)
        #logging.info('Cleaning temp folder...')
        clean_temp_folder()
    except: log_error('(!) Unexpected error while launching -')

    #logging.info(f'External launcher finished in {time.time() - LAUNCHER_START_TIME:.3f} seconds.')
