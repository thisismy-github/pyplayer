''' Generic, non-Qt-related utility functions.
    thisismy-github 4/23/22 '''

import os
import constants


def get_unique_path(path: str, start: int = 2, key: str = None, zeros: int = 0, strict: bool = False) -> str:
    ''' Returns a unique `path`. If `path` already exists, version-numbers starting from `start` are added. If a
        keyword `key` is provided and exists within `path`, it is replaced with the version number with `zeros`
        padded zeros. Otherwise, Windows-style naming is used with no padding: "(base) (version).(ext)".
        The `strict` parameter forces `key` paths to always have version numbers included, even if `path`
        was unique to begin with. This does not apply to Windows-style naming. '''
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


def add_path_suffix(path: str, suffix: str, unique: bool = False) -> str:
    ''' Returns a path with `suffix` added between the basename and extension. If `unique` is set,
        the new path will be run through get_unique_path with default arguments before returning. '''
    base, ext = os.path.splitext(path)
    return f'{base}{suffix}{ext}' if not unique else get_unique_path(f'{base}{suffix}{ext}')


def get_from_PATH(filename: str) -> str:
    ''' Returns the full path to a `filename` if it exists in
        the user's PATH, otherwise returns an empty string. '''
    from platform import system
    for path in os.environ.get('PATH', '').split(';' if system() == 'Windows' else ':'):
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


if constants.PLATFORM != 'Windows': file_is_hidden = lambda path: os.path.basename(path)[0] == '.'
else: file_is_hidden = lambda path: os.stat(path).st_file_attributes & 2
