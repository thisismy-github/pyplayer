''' Generic, non-Qt-related utility functions.
    thisismy-github 4/23/22 '''


import constants

import os
import sys
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


def ffmpeg(cmd: str) -> None:   # https://code.activestate.com/recipes/409002-launching-a-subprocess-without-a-console-window/
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    cmd = f'"{constants.FFMPEG}" -y {cmd} -progress pipe:1 -hide_banner -loglevel warning'.replace('""', '"')
    logger.info('FFmpeg command: ' + cmd)
    subprocess.run(cmd, startupinfo=startupinfo, shell=True)


def ffmpeg_async(cmd: str) -> subprocess.Popen:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    cmd = f'"{constants.FFMPEG}" -y {cmd} -progress pipe:1 -hide_banner -loglevel warning'.replace('""', '"')
    logger.info('FFmpeg command: ' + cmd)
    return subprocess.Popen(cmd, startupinfo=startupinfo, shell=True, stdout=subprocess.PIPE, text=True)


def add_path_suffix(path: str, suffix: str, unique: bool = False) -> str:
    ''' Returns a path with `suffix` added between the basename and extension.
        If `unique` is True, the new path will be run through getUniquePath()
        with default arguments before returning. '''
    base, ext = os.path.splitext(path)
    return f'{base}{suffix}{ext}' if not unique else get_unique_path(f'{base}{suffix}{ext}')


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
        else: path = key_path.replace(key, '')  # if not strict, replace key with nothing first to see if original name is unique
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


def get_from_PATH(filename: str) -> str:
    ''' Returns the full path to a `filename` if it exists in
        the user's PATH, otherwise returns an empty string. '''
    is_windows = constants.PLATFORM == 'Windows'
    for path in os.environ.get('PATH', '').split(';' if is_windows else ':'):
        try:
            if filename in os.listdir(path):
                return os.path.join(path, filename)
        except: pass
    return ''


def get_hms(seconds: float) -> tuple:
    ''' Converts seconds to the hours, minutes, seconds, and milliseconds it represents. '''
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int((seconds % 3600) % 60)
    ms = int(round((seconds - int(seconds)) * 100, 4))  # round to account for floating point imprecision
    return h, m, s, ms


def get_aspect_ratio(width: int, height: int) -> str:
    ''' Calculates the ratio between two numbers. https://gist.github.com/Integralist/4ca9ff94ea82b0e407f540540f1d8c6c '''
    if width == 0: return '0:0'
    gcd = lambda w, h: w if h == 0 else gcd(h, w % h)   # GCD is the highest number that evenly divides both W and H
    r = gcd(width, height)
    return f'{int(width / r)}:{int(height / r)}'


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
            if os.path.exists(old_path):                # if old PIL path doesn't exist, just hope the new PIL path is correct
                import shutil
                shutil.copytree(old_path, backup_path)
                if new_path_already_existed:
                    try:
                        new_path_temp_name = get_unique_path(new_path + '_temp')
                        os.rename(new_path, new_path_temp_name)
                        new_path_renamed = True
                    except: logger.warning(f'Could not rename {new_path} to {new_path}_temp: {format_exc()}')
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
            if new_path_renamed: os.rename(new_path_temp_name, new_path)
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
        except NameError: pass              # NameError -> error occurred before the paths were even defined
        except:     # PIL is seemingly unrecoverable. hopefully this is extremely unlikely outside of user-tampering
            logger.critical(f'(!!!) COULD NOT RESTORE PIL FOLDER: {format_exc()}')
            logger.critical('\n\n  WARNING -- You may need to reinstall PyPlayer to restore snapshotting capabilities.'
                             '\n             If you cannot find the PIL folder within your installation, please report '
                             '\n             this error (along with this log file) on Github.\n')


def sanitize(filename: str, allow_reserved_words: bool = True, default: str = ''):
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
        if not allow_reserved_words: filename = default
        else: filename = '__' + filename
    return filename


if constants.PLATFORM != 'Windows': file_is_hidden = lambda path: os.path.basename(path)[0] == '.'
else: file_is_hidden = lambda path: os.stat(path).st_file_attributes & 2
