''' This script compiles PyPlayer to an executable. Make sure you
    have all appropriate libraries in requirements.txt installed.
    View readme.txt for more information.
    thisismy-github 4/16/22 '''

import os
import sys
import glob
import shutil
import platform
import subprocess


pjoin = os.path.join
PLATFORM = platform.system()
CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
RELEASE_DIR = pjoin(CWD, 'compiling', 'release')
FINAL_RELEASE_DIR = pjoin(CWD, 'compiled')
PYQT_DIR = pjoin(RELEASE_DIR, 'PyQt5')
EXPECTED_SUBDIRS = ('plugins', 'pyqt5', 'themes')


# ensure python is running from a venv, if possible
if 'venv' not in sys.executable.split(os.sep):
    VENV_DIR = pjoin(ROOT_DIR, 'venv')
    if not os.path.exists(VENV_DIR): VENV_DIR = pjoin(CWD, 'venv')

    if PLATFORM == 'Windows': venv = pjoin(VENV_DIR, 'Scripts', 'python.exe')
    else: venv = pjoin(VENV_DIR, 'bin', 'python3')
    if os.path.exists(venv):
        print(f'Restarting with virtual environment at "{venv}"')
        process = subprocess.Popen(f'"{venv}" "{sys.argv[0]}"', shell=True)
        process.wait()
        sys.exit(0)


def compile():
    print(f'\nCompiling PyPlayer (sys.executable="{sys.executable}")...\n')
    pyinstaller = f'"{sys.executable}" -m PyInstaller'
    args = f'--distpath "{pjoin(CWD, "compiling")}" --workpath "{pjoin(CWD, "build")}"'
    subprocess.call(f'{pyinstaller} "{pjoin(CWD, "main.spec")}" --noconfirm {args}')
    subprocess.call(f'{pyinstaller} "{pjoin(CWD, "updater.spec")}" --noconfirm {args}')

    print('Checking for pre-existing config files to reuse...')
    override_config_path = pjoin(CWD, 'config.ini')
    existing_config_path = pjoin(FINAL_RELEASE_DIR, 'config.ini')
    if os.path.exists(override_config_path):
        print('Copying config-override from current directory...')
        shutil.copyfile(override_config_path, pjoin(RELEASE_DIR, 'config.ini'))
    elif os.path.exists(existing_config_path):
        print('Copying existing config from previous build...')
        shutil.copyfile(existing_config_path, pjoin(RELEASE_DIR, 'config.ini'))
    else: print('No pre-existing config files detected, skipping...')

    if os.path.exists(FINAL_RELEASE_DIR):
        print('Deleting old build...')
        shutil.rmtree(FINAL_RELEASE_DIR)
    else: print('No previous build detected, skipping...')

    print(f'Deleting files defined in {pjoin(CWD, "exclude.txt")}...')
    with open(pjoin(CWD, 'exclude.txt')) as exclude:
        for line in exclude:
            line = line.strip()
            if line and line[0] not in '#;' and line[:2] != '//':
                for path in glob.glob(pjoin(RELEASE_DIR, line)):
                    print(f'exists={os.path.exists(path)} - {path}')
                    if os.path.exists(path):
                        if os.path.isdir(path): shutil.rmtree(path)
                        else: os.remove(path)

    print('Copying cacert.pem...')
    certifi_dir = pjoin(RELEASE_DIR, 'certifi')
    shutil.copy2(pjoin(certifi_dir, 'cacert.pem'), pjoin(PYQT_DIR, 'cacert.pem'))
    shutil.rmtree(certifi_dir)

    print('Moving PIL folder to PyQt folder and deleting unnecessary files...')
    shutil.move(pjoin(RELEASE_DIR, 'PIL'), pjoin(PYQT_DIR, 'PIL'))
    for filename in os.listdir(pjoin(PYQT_DIR, 'PIL')):
        if not filename.startswith('_imaging.'):
            os.remove(pjoin(PYQT_DIR, 'PIL', filename))

    print('Moving updater to PyQt folder...')
    name = 'updater' + ('.exe' if PLATFORM == 'Windows' else '')
    shutil.move(pjoin(os.path.dirname(RELEASE_DIR), name), pjoin(PYQT_DIR, name))

    print(f'Deleting non-{PLATFORM} files from plugins folder...')
    right_suffix = '-windows' if PLATFORM == 'Windows' else '-unix'
    wrong_suffix = '-unix' if PLATFORM == 'Windows' else '-windows'
    for filename in os.listdir(pjoin(RELEASE_DIR, 'plugins')):
        path = pjoin(RELEASE_DIR, 'plugins', filename)
        if filename.endswith(right_suffix):
            os.rename(path, pjoin(RELEASE_DIR, 'plugins', filename[:-len(right_suffix)]))
        elif filename.endswith(wrong_suffix):
            if os.path.isdir(path): shutil.rmtree(path)
            else: os.remove(path)


# ---------------------
# Windows
# ---------------------
def compile_windows():
    compile()
    print(f'\nPerforming post-compilation tasks for {PLATFORM}...')

    def move(folder):
        for pattern in ('*.pyd', '*.dll'):
            for path in glob.glob(pjoin(folder, pattern)):
                print(f'{path} -> {pjoin(PYQT_DIR, os.path.basename(path))}')
                shutil.move(path, pjoin(PYQT_DIR, os.path.basename(path)))

    print('Moving .pyd and .dll files to PyQt folder...')
    move(RELEASE_DIR)
    for filename in os.listdir(RELEASE_DIR):
        if filename.lower() in EXPECTED_SUBDIRS: continue
        folder = pjoin(RELEASE_DIR, filename)
        if not os.path.isdir(folder): continue
        move(folder)
        shutil.rmtree(folder)

    print('Moving python3*.dll back to root folder...')
    for path in glob.glob(pjoin(PYQT_DIR, 'python3*.dll')):
        filename = os.path.basename(path)
        print(path, filename, filename != 'python3.dll')
        if filename != 'python3.dll':
            shutil.move(path, pjoin(RELEASE_DIR, filename))

    print('Lowercasing PyQt folder (for aesthetics)...')
    os.rename(PYQT_DIR, pjoin(RELEASE_DIR, 'pyqt5'))


#######################################
if __name__ == '__main__':
    while True:
        try:
            compile_windows() if PLATFORM == 'Windows' else compile()

            print('Compile finished, renaming "compiling" to "compiled"...')
            os.renames(RELEASE_DIR, FINAL_RELEASE_DIR)

            choice = input('\nDone! Type anything to exit, or press enter to recompile... ')
            if choice != '': break
        except:
            import traceback
            input(f'\n(!) Compile failed:\n\n{traceback.format_exc()}')
