''' Generic, non-Qt-related utility functions.
    thisismy-github 4/23/22 '''

from __future__ import annotations

import constants

import os
import sys
import time
import logging
import subprocess
import unicodedata
from traceback import format_exc


# reserved words/characters on Windows
_SANITIZE_BLACKLIST = ('\\', '/', ':', '*', '?', '\'', '<', '>', '|', '\0')
_SANITIZE_RESERVED = (
    'CON', 'PRN', 'AUX', 'NUL', 'COM0', 'COM1', 'COM2', 'COM3',
    'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT0', 'LPT1',
    'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9',
)

# logger
logger = logging.getLogger('util.py')


def add_path_suffix(path: str, suffix: str, unique: bool = False) -> str:
    ''' Returns a path with `suffix` added between the basename and extension.
        If `unique` is True, the new path will be run through getUniquePath()
        with default arguments before returning. '''
    base, ext = os.path.splitext(path)
    return f'{base}{suffix}{ext}' if not unique else get_unique_path(f'{base}{suffix}{ext}')


# https://code.activestate.com/recipes/409002-launching-a-subprocess-without-a-console-window/
def ffmpeg(cmd: str) -> None:
    cmd = f'"{constants.FFMPEG}" -y {cmd} -progress pipe:1 -hide_banner -loglevel warning'.replace('""', '"')
    logger.info('FFmpeg command: ' + cmd)
    if not constants.IS_WINDOWS:
        import shlex
        cmd = shlex.split(cmd)                  # w/o `shell=True`, linux will try to read the entire `cmd` like a file

    subprocess.run(
        cmd,
        startupinfo=constants.STARTUPINFO       # hides command prompt that appears w/o `shell=True`
    )


def ffmpeg_async(cmd: str, priority: int = None, niceness: int = None, threads: int = 0) -> subprocess.Popen:
    ''' Valid `priority` level aliases and their associated nice value on Unix:
        - 0 - High (-10)
        - 1 - Above normal (-5)
        - 2 - Normal (0)
        - 3 - Below normal (5)
        - 4 - Low (10)

        On Windows, `priority` > 4 is treated as an actual Windows constant,
        and on Linux `niceness` is treated as a raw niceness value.

        NOTE: From what I've read, "niceness" does literally nothing on Mac.
        NOTE: Negative niceness requires root. Otherwise, 0 is used.
        NOTE: `threads` expects `cmd` to end with a quoted output path.
        NOTE: `threads` will be ignored if "-threads" is already in `cmd`. '''

    # add "-threads" parameter just before `cmd`'s output path if desired
    if threads and cmd[-1] == '"' and ' -threads ' not in cmd:
        output_index = cmd.rfind(' "', 0, -1)
        cmd = f'{cmd[:output_index]} -threads {threads} {cmd[output_index:]}'

    # add extra supplemental parameters to formatting, piping, and overwriting
    cmd = f'"{constants.FFMPEG}" -y {cmd} -progress pipe:1 -hide_banner -loglevel warning'.replace('""', '"')
    logger.info('FFmpeg command: ' + cmd)

    # set priority on Windows
    if constants.IS_WINDOWS:
        if priority is not None:
            if priority < 5:                    # <5 means we want to use it like an index (0-4)
                priority = (                    # otherwise it might be a raw value, like 64
                    subprocess.HIGH_PRIORITY_CLASS,
                    subprocess.ABOVE_NORMAL_PRIORITY_CLASS,
                    subprocess.NORMAL_PRIORITY_CLASS,
                    subprocess.BELOW_NORMAL_PRIORITY_CLASS,
                    subprocess.IDLE_PRIORITY_CLASS,
                )[priority]
        else:
            priority = 0

    # split `cmd` and calculate priority ("niceness") on Linux
    else:
        import shlex
        cmd = shlex.split(cmd)                  # w/o `shell=True`, linux will try to read the entire `cmd` like a file

        # calculate priority
        if niceness is not None:                # raw `niceness` value was provided, just use that
            priority = niceness
        elif priority is not None:              # no `niceness` -> calculate it from `priority`
            priority = -10 + (priority * 5)     # 0 = -10, 1 = -5, 2 = 0, 3 = 5, 4 = 10

        # prepend niceness command to our ffmpeg command (doesn't do anything on macOS apparently)
        if constants.IS_LINUX and priority:     # who's really gonna use PyPlayer on a Mac anyways?
            cmd = ['nice', '-n', str(priority)] + cmd
        priority = 0                            # creationflags must be 0, not None

    # open process
    return subprocess.Popen(
        cmd,
        bufsize=1,                              # line-by-line buffering (helps us with parsing in batches)
        stdout=subprocess.PIPE,                 # pipes stdout so that we can read the output in real time
        stderr=subprocess.STDOUT,               # pipes errors to stdout so we can read both (keeping them separate is hard)
        startupinfo=constants.STARTUPINFO,      # hides command prompt that appears w/o `shell=True`
        creationflags=priority,                 # sets the priority level ffmpeg will start with
        start_new_session=True,                 # this allows us to more easily kill the ffmpeg process if needed
        text=True                               # turns stdout into easily parsible lines of text rather than a byte stream
    )


def foreground_is_fullscreen() -> bool:
    ''' Returns True if the foreground window is fullscreen. Windows
        only (for now). Does not account for multi-monitor setups where
        the fullscreen window is not on the main monitor (for now). '''
    if not constants.IS_WINDOWS: return False

    # NOTE: ctypes can do this quite easily, but `ctypes.wintypes` is unreliable
    import win32gui

    def rects_are_equal(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> bool:
        return a[0] == b[0] and a[1] == b[1] and a[2] == b[2] and a[3] == b[3]

    hwnd = win32gui.GetForegroundWindow()
    screen_hwnd = win32gui.GetDesktopWindow()
    if hwnd == screen_hwnd or hwnd == 0:
        return False

    screen_rect = win32gui.GetWindowRect(screen_hwnd)
    window_rect = win32gui.GetWindowRect(hwnd)
    return rects_are_equal(screen_rect, window_rect)


def get_from_PATH(filename: str) -> str:        # i learned about `shutil.which()` way too late. oh well, this works
    ''' Returns the full path to a `filename` if it exists in
        the user's PATH, otherwise returns an empty string. '''
    sep = ';' if constants.IS_WINDOWS else ':'
    for path in os.environ.get('PATH', '').split(sep):
        try:
            if filename in os.listdir(path):
                return os.path.join(path, filename)
        except:
            pass
    return ''


def get_hms(seconds: float) -> tuple[int, int, int, int]:
    ''' Converts seconds to the hours, minutes, seconds, and milliseconds it represents. '''
    h_remainder = seconds % 3600
    h = int(seconds // 3600)
    m = int(h_remainder // 60)
    s = int(h_remainder % 60)
    ms = int(round((seconds - int(seconds)) * 100, 4))  # round to account for floating point imprecision
    return h, m, s, ms


def get_PIL_Image():
    ''' An over-the-top way of hiding PIL's folder. The PIL folder cannot be
        avoided due to the required from-import, and conventional means of
        hiding it do not seem to work, so instead we hide the folder at first,
        then move (NOT copy) it to the root folder so we can import PIL, then
        immediately move the folder back. All this, just to have one less item
        in the root folder. Honestly worth it. '''

    try:    # prepare PIL for importing if it hasn't been imported yet (once imported, it's imported for good)
        PIL_already_imported = 'PIL.Image' in sys.modules
        if not PIL_already_imported and constants.IS_COMPILED:
            logger.info('Importing PIL for the first time...')
            files_moved = []

            # identify new PIL path and check if it already exists
            new_path = f'{constants.CWD}{os.sep}PIL'
            new_path_already_existed = os.path.exists(new_path)
            new_path_renamed = False

            # identify expected PIL path and a backup for it, assert existence of at least one PIL path
            old_path = f'{constants.BIN_DIR}{os.sep}PIL'
            backup_path = old_path + '.bak'
            backup_path_already_existed = os.path.exists(backup_path)
            if backup_path_already_existed:     # backup already exists (likely from error in previous session)
                logger.warning(f'PIL backup path {backup_path} already exists, using it...')
                old_path, backup_path = backup_path, old_path   # swap backup and old paths
            assert os.path.exists(old_path) or new_path_already_existed, 'PIL folder not found at ' + old_path

            # backup old PIL path and create new PIL path. if it already exists (for some reason), rename it temporarily
            if os.path.exists(old_path):        # if old PIL path doesn't exist, just hope the new PIL path is correct
                import shutil
                shutil.copytree(old_path, backup_path)
                if new_path_already_existed:
                    try:
                        new_path_temp_name = get_unique_path(new_path + '_temp')
                        os.rename(new_path, new_path_temp_name)
                        new_path_renamed = True
                    except:
                        logger.warning(f'Could not rename {new_path} to {new_path}_temp: {format_exc()}')
                try: os.makedirs(new_path)
                except: logger.warning(f'Could not make {new_path}: {format_exc()}')

            # move (NOT copy) each file from the normal PIL path to the new PIL path and append each move to files_moved
            for file in os.listdir(old_path):
                if file[-4:] != '.pyd': continue
                old_file = f'{old_path}{os.sep}{file}'
                new_file = f'{new_path}{os.sep}{file}'
                os.rename(old_file, new_file)
                files_moved.append((old_file, new_file))

        from PIL import Image                   # actually import PIL.Image (this is what hangs in the script)

        # return files to their original spots, delete/restore new PIL path, and return PIL.Image
        if not PIL_already_imported and constants.IS_COMPILED:
            import shutil
            for source, dest in files_moved:
                try: os.rename(dest, source)
                except: logger.warning(f'Could not move {dest} to {source}: {format_exc()}')
            if not (new_path_already_existed and not new_path_renamed):
                try: shutil.rmtree(new_path)
                except: logger.warning(f'Could not delete {new_path}: {format_exc()}')
            if new_path_renamed:            os.rename(new_path_temp_name, new_path)
            if os.path.exists(backup_path): shutil.rmtree(backup_path)
            if backup_path_already_existed: os.rename(old_path, backup_path)
            logger.info('First-time PIL import successful.')
        return Image                            # return PIL.Image
    except:
        logger.error(f'(!) PIL IMPORT FAILED: {format_exc()}')
        try:        # in the event of an error, attempt to restore backup if one exists
            if os.path.exists(backup_path):
                import shutil
                shutil.rmtree(old_path)
                os.rename(backup_path, old_path)
            elif not os.path.exists(old_path) and not os.path.exists(new_path):
                raise Exception('None of the following candidates for a PIL folder were found:'
                                f'\nOld: {old_path}\nNew: {new_path}\nBackup: {backup_path}')
        except NameError:                       # NameError -> error occurred before the paths were even defined
            pass
        except:     # PIL is seemingly unrecoverable. hopefully this is extremely unlikely outside of user-tampering
            logger.critical(f'(!!!) COULD NOT RESTORE PIL FOLDER: {format_exc()}')
            logger.critical('\n\n  WARNING -- You may need to reinstall PyPlayer to restore snapshotting capabilities.'
                            '\n             If you cannot find the PIL folder within your installation, please report '
                            '\n             this error (along with this log file) on Github.\n')


def get_ratio_string(width: int, height: int) -> str:
    ''' Calculates the ratio between two numbers.
        https://gist.github.com/Integralist/4ca9ff94ea82b0e407f540540f1d8c6c '''
    if width == 0:
        return '0:0'
    gcd = lambda w, h: w if h == 0 else gcd(h, w % h)   # GCD is the highest number that evenly divides both W and H
    r = gcd(width, height)
    return f'{int(width / r)}:{int(height / r)}'


def get_unique_path(path: str, start: int = 2, key: str = None, zeros: int = 0, strict: bool = False) -> str:
    ''' Returns a unique `path`. If `path` already exists, version-numbers
        starting from `start` are added. If a keyword `key` is provided and
        is a substring within `path`, it is replaced with the version number
        with `zeros` padded zeros. Otherwise, Windows-style naming is used
        with no padding: "(base) (version).(ext)". `strict` forces paths
        with non-Windows-style naming to always include a version number,
        even if `path` was unique to begin with. '''
    # TODO: add ignore_extensions parameter that uses os.path.splitext and glob(basepath.*)
    version = start
    if key and key in path:                     # if key and key exists in path -> replace key in path with padded version number
        print(f'Replacing key "{key}" in path: {path}')
        key_path = path
        if strict:                              # if strict, replace key with first version number
            path = key_path.replace(key, str(version).zfill(zeros if version >= 0 else zeros + 1))  # +1 zero if version is negative
            version += 1                        # increment version here to avoid checking this first path twice when we start looping
        else:
            path = key_path.replace(key, '')    # if not strict, replace key with nothing first to see if original name is unique
        while os.path.exists(path):
            path = key_path.replace(key, str(version).zfill(zeros if version >= 0 else zeros + 1))
            version += 1
    else:                                       # no key -> use windows-style unique paths
        base, ext = os.path.splitext(path)
        if os.path.exists(path):                # if path exists, check if it's already using window-style names
            parts = base.split()
            if parts[-1][0] == '(' and parts[-1][-1] == ')' and parts[-1][1:-1].isnumeric():
                base = ' '.join(parts[:-1])     # path is using window-style names, remove pre-existing version string from basename
            while os.path.exists(path):
                path = f'{base} ({version}){ext}'
                version += 1
    return path


def get_verbose_timestamp(seconds: float) -> str:
    ''' - Example: "3 hours, 12 minutes, and 57 seconds"
        - Example: "15 minutes, 1 second"
        - Example: "5.3 seconds" '''
    if seconds < 10.0:
        seconds = round(seconds, 1)
        int_seconds = int(seconds)
        if seconds == int_seconds:
            return f'{int_seconds} second{"s" if int_seconds != 1 else ""}'
        return f'{seconds:.1f} second{"s" if seconds != 1 else ""}'
    else:
        h, m, s, _ = get_hms(seconds)
        deltaFormat = []
        if h: deltaFormat.append(f'{h} hour{"s" if h > 1 else ""}')
        if m: deltaFormat.append(f'{m} minute{"s" if m > 1 else ""}')
        if s: deltaFormat.append(f'{s} second{"s" if s > 1 else ""}')
        if len(deltaFormat) == 3: deltaFormat.insert(-1, 'and')
        return ', '.join(deltaFormat).replace('and,', 'and')


def sanitize(filename: str, allow_reserved_words: bool = True, default: str = '') -> str:
    ''' A slightly more optimized version of `sanitize_filename.sanitize()`,
        with added parameters.

        Returns a fairly safe version of `filename` (which should not be a
        full path). If `filename` is completely invalid, `default` is used.
        If `allow_reserved_words` is True, filenames such as "CON" will be
        returned as "__CON". Otherwise, `default` is returned. '''

    # remove blacklisted characters and charcters below code point 32
    filename = ''.join(c for c in filename if c not in _SANITIZE_BLACKLIST and ord(c) > 31)
    filename = unicodedata.normalize('NFKD', filename)
    filename = filename.strip().rstrip('. ')    # cannot end with spaces or periods on Windows

    if len(filename) == 0:
        filename = default
    elif filename in _SANITIZE_RESERVED:        # check for reserved filenames such as CON
        filename = default if not allow_reserved_words else ('__' + filename)
    return filename


def scale(x: float, y: float, new_x: float = -1, new_y: float = -1) -> tuple[int | float, int | float]:
    ''' Returns (`x`, `y`) scaled to either `new_x` or `new_y`, if
        either is >=0. If both are provided, `new_y` is ignored. '''
    if new_x <= 0:   new_x = round((float(new_y) / y) * x)
    elif new_y <= 0: new_y = round((float(new_x) / x) * y)
    return new_x, new_y


def setctime(path: str, ctime: int) -> None:
    ''' A slightly stripped down version of the `win32_setctime` library,
        which I had trouble importing correctly after compiling. Sets the
        creation time of `path` to `ctime` seconds (a unix timestamp). To
        set last modified time or last accessed time, use `os.utime()`.
        Windows-only. https://github.com/Delgan/win32-setctime '''

    if not constants.IS_WINDOWS: return
    from ctypes import byref, get_last_error, wintypes, WinDLL, WinError

    # dll and function definitions
    kernel32 = WinDLL("kernel32", use_last_error=True)
    CreateFileW = kernel32.CreateFileW
    SetFileTime = kernel32.SetFileTime
    CloseHandle = kernel32.CloseHandle

    # defining return/argument types for the above functions for type-safety
    CreateFileW.restype = wintypes.HANDLE
    CreateFileW.argtypes = (
        wintypes.LPWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    )

    SetFileTime.restype = wintypes.BOOL
    SetFileTime.argtypes = (
        wintypes.HANDLE,
        wintypes.PFILETIME,
        wintypes.PFILETIME,
        wintypes.PFILETIME,
    )

    CloseHandle.restype = wintypes.BOOL
    CloseHandle.argtypes = (wintypes.HANDLE,)

    # ---

    path = os.path.normpath(os.path.abspath(path))
    ctime = int(ctime * 10000000) + 116444736000000000
    if not 0 < ctime < (1 << 64):
        raise ValueError("The system value of the timestamp exceeds u64 size: %d" % ctime)

    atime = wintypes.FILETIME(0xFFFFFFFF, 0xFFFFFFFF)
    mtime = wintypes.FILETIME(0xFFFFFFFF, 0xFFFFFFFF)
    ctime = wintypes.FILETIME(ctime & 0xFFFFFFFF, ctime >> 32)

    flags = 128 | 0x02000000
    handle = wintypes.HANDLE(CreateFileW(path, 256, 0, None, 3, flags, None))

    if handle.value == wintypes.HANDLE(-1).value:
        raise WinError(get_last_error())
    if not wintypes.BOOL(SetFileTime(handle, byref(ctime), byref(atime), byref(mtime))):
        raise WinError(get_last_error())
    if not wintypes.BOOL(CloseHandle(handle)):
        raise WinError(get_last_error())


def suspend_process(process: subprocess.Popen, suspend: bool = True) -> int:
    ''' Cross-platform way of suspending or resuming a `process`. On Linux/Mac,
        SIGSTOP/SIGCONT signals are sent. On Windows, the undocumented
        `ntdll.NtSuspendProcess()` and `ntdll.NtResumeProcess()` APIs are
        used. Returns 0 on success (this does not inherently mean `process`
        was actually suspended, just that the calls did not fail).

        Windows notes:
        - `ntdll.NtSuspendProcess` calls stack (i.e. each suspend call must
        have a corresponding resume call before `process` actually resumes)!
        This method does not check if `process` is already suspended or not.
        - Suspend/resume calls will be sent to the parent shell rather than
        the actual process if `process` was created using `shell=True`!
        - This is based on `psutil`'s `psutil_proc_suspend_or_resume()`
        function, recreated from scratch in "pure" Python. '''

    if not constants.IS_WINDOWS:
        import signal
        process.send_signal(signal.SIGSTOP if suspend else signal.SIGCONT)
        return 0

    from ctypes import wintypes, WinDLL

    # dll and function definitions
    ntdll = WinDLL("ntdll", use_last_error=True)
    kernel32 = WinDLL("kernel32", use_last_error=True)
    CloseHandle = kernel32.CloseHandle
    OpenProcess = kernel32.OpenProcess

    # defining return/argument types for the above functions for type-safety
    CloseHandle.restype = wintypes.LONG
    CloseHandle.argtypes = (wintypes.HANDLE,)
    OpenProcess.restype = wintypes.HANDLE
    OpenProcess.argtypes = (
        wintypes.DWORD,
        wintypes.BOOL,
        wintypes.DWORD,
    )

    # open limited handle to process using its pid (closed in the finally-statement)
    access_flags = 2048 | 4096      # PROCESS_SUSPEND_RESUME | PROCESS_QUERY_LIMITED_INFORMATION
    process_handle = OpenProcess(access_flags, False, process.pid)

    # define and call either ntdll.NtSuspendProcess or ntdll.NtResumeProcess
    try:
        if suspend:
            logger.info(f'Suspending process {process} at handle {process_handle}...')
            NtSuspendProcess = ntdll.NtSuspendProcess
            NtSuspendProcess.argtypes = (wintypes.HANDLE,)
            NtSuspendProcess.restype = wintypes.LONG
            return NtSuspendProcess(process_handle)
        else:
            logger.info(f'Resuming process {process} at handle {process_handle}...')
            NtResumeProcess = ntdll.NtResumeProcess
            NtResumeProcess.argtypes = (wintypes.HANDLE,)
            NtResumeProcess.restype = wintypes.LONG
            return NtResumeProcess(process_handle)
    except:
        logger.info(f'(!) Failed to {"suspend" if suspend else "resume"} process: {format_exc()}')
        return -1
    finally:
        CloseHandle(process_handle)


def kill_process(process: subprocess.Popen, wait: bool = True, wait_after: float = 0.0) -> None:
    ''' Cross-platform way of killing a `process`. On Windows, taskkill is used.
        On Linux/Mac, a SIGTERM signal is sent to `process`'s group pid. If
        `wait` is True, this function blocks until `process` is gone, then waits
        `wait_after` seconds afterwards to allow any handles to be released. '''
    try:
        if constants.IS_WINDOWS:                # why bother with signals when you can just nuke it from orbit?
            subprocess.call(
                f'taskkill /F /T /PID {process.pid}',
                startupinfo=constants.STARTUPINFO
            )                                   # ^ hides command prompt that appears if called while compiled
        else:
            try:
                import signal
                group_pid = os.getpgid(process.pid)
                os.killpg(group_pid, signal.SIGTERM)
                process.wait(timeout=0.25)      # wait briefly to see if it terminates peacefully
            except subprocess.TimeoutExpired:   # it's is still alive. old yeller it
                os.killpg(group_pid, signal.SIGKILL)
        if wait:
            process.wait(timeout=3)             # give it up to 3 seconds to actually close before giving up
            time.sleep(wait_after)              # wait for any handles to (hopefully) be released
    except:
        logger.warning(f'(!) Failed to terminate process: {format_exc()}')


if constants.IS_WINDOWS: file_is_hidden = lambda path: os.stat(path).st_file_attributes & 2
else:                    file_is_hidden = lambda path: os.path.basename(path)[0] == '.'
