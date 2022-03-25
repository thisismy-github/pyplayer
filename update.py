import qtstart
import constants
import qthelpers

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
import os
import sys
import logging
import subprocess
from traceback import format_exc


logger = logging.getLogger('update.py')
HYPERLINK = f'<a href="{constants.REPOSITORY_URL}/releases/latest">latest release on Github here</a>'


def get_later_version_string(a, b):     # https://stackoverflow.com/questions/11887762/how-do-i-compare-version-numbers-in-python
    ''' Returns the greater of two version strings, with mild future-proofing. Allows for an
        arbitrary number in each sequence of the version, with an arbitrary number of sequences. '''
    atuple = tuple(map(int, (a.split('.'))))
    btuple = tuple(map(int, (b.split('.'))))
    return a if atuple > btuple else b


def check_for_update(self):
    ''' The following format is assumed:
            > constants.REPOSITORY_URL -- https://github.com/thisismy-github/PyPlayer
            > constants.VERSION        -- pyplayer 0.1.0 beta
                - version number can be variable length, "beta" modifier is optional

        The following example is expected:
            ->     https://github.com/thisismy-github/PyPlayer/releases/latest
              ->   https://github.com/thisismy-github/PyPlayer/releases/tags/v1.2.3
                -> https://github.com/thisismy-github/PyPlayer/releases/download/v1.2.3/pyplayer_1.2.3.zip

        NOTE: It's possible to directly access the latest version of an asset by doing
              {constants.REPOSITORY_URL}/releases/latest/download/*asset_name*,
              but that requires not including the version in the asset's filename.
    '''
    import requests
    release_url = f'{constants.REPOSITORY_URL}/releases/latest'
    logger.info(f'Checking {release_url} for updates')
    try:
        response = requests.get(release_url)
        response.raise_for_status()
        latest_version_url = response.url.rstrip('/')
        latest_version = latest_version_url.split('/')[-1].lstrip('v')

        current_version = constants.VERSION.split()[1]
        logger.info(f'Latest version: {latest_version} | Current version: {current_version}')

        if len(latest_version) != len(current_version):
            self.log('Github release URL could not be parsed correctly.')
            return self._handle_updates_signal.emit(
                dict(failed=True),
                dict(title='Update URL mismatch',
                     icon=QMessageBox.Warning,
                     text=f'The update URL on Github has an unexpected format. \nGithub version: "{latest_version}"\nCurrent version: "{current_version}"',
                     textInformative='Newer versions might use a different naming scheme, or perhaps '
                                     f'there was an error while checking. You can manually check the {HYPERLINK}.')
            )

        if get_later_version_string(latest_version, current_version) != current_version:    # latest version is more recent than current version
            if sys.platform == 'win32':                                                     # TODO Windows only for now
                return self._handle_updates_signal.emit(
                    dict(latest_version_url=latest_version_url),
                    dict(title=f'Update {latest_version} available',
                         icon=QMessageBox.Information,
                         buttons=(QMessageBox.Yes | QMessageBox.No),        # | QMessageBox.Ignore
                         text=f'An update is available on Github ({current_version} -> {latest_version}).',
                         textInformative='You can manually view the '
                                         f'{HYPERLINK}.\n Click "Yes" '
                                         'to download and install this update (PyPlayer will restart automatically).')
                )
            else:                                                           # non-windows version of popup (no auto-updater yet)
                return self._handle_updates_signal.emit(
                    dict(latest_version_url=latest_version_url),
                    dict(title=f'Update {latest_version} available',
                         icon=QMessageBox.Information,
                         text=f'An update is available on Github ({current_version} -> {latest_version}).',
                         textInformative=f'You can download the {HYPERLINK}.')
                )
        else: self.log('You\'re up to date!')
    except: self.log(f'(!) UPDATE-CHECK FAILED: {format_exc()}')
    self._handle_updates_signal.emit(None, None)                            # call empty signal to perform cleanup


def download_update(self, latest_version, download_url, download_path):
    import requests
    try:
        logger.info(f'Downloading version {latest_version} from {download_url} to {download_path}')
        download_response = requests.get(download_url, stream=True)
        download_response.raise_for_status()
        total_size = int(download_response.headers.get('content-length'))
        downloaded = 0

        self.save_progress_bar.setMaximum(100)
        self.save_progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.show_save_progress_signal.emit(True)
        self.statusbar.setVisible(True)

        with open(download_path, 'wb') as file:
            for chunk in download_response.iter_content(chunk_size=1048576):     # 1048576 = 1024 * 1024
                file.write(chunk)
                downloaded += len(chunk)
                self.save_progress_bar.setValue(downloaded / total_size)
                self.save_progress_bar.setFormat(f'{downloaded / 1048576:.2f}/{total_size / 1048576:.2f} %p%')
                self.app.processEvents()                    # manually update GUI during download, since this is not a thread
        self.save_progress_bar.setFormat('Update downloaded, restarting...')
        logger.info('Download successful, preparing updater-utility...')

        # send exit-signals to all PyPlayer instances through their PID files
        pid_files = []
        for file in os.listdir(constants.TEMP_DIR):
            if file[-4:] == '.pid':
                pid_file = os.path.join(constants.TEMP_DIR, file)
                try: os.remove(pid_file)                    # try to delete PID file to confirm whether it's active or not
                except:                                     # couldn't delete PID file -> send exit-signal to its instance
                    logger.info(f'Active PyPlayer instance detected through PID file {pid_file}')
                    pid_files.append(f'"{pid_file}"')
                    pid = file[:-4]
                    if pid == os.getpid(): continue         # do not send exit-signal to ourselves
                    cmdpath = os.path.join(constants.TEMP_DIR, f'cmd.{pid}.txt')
                    with open(cmdpath, 'wb') as txt:
                        txt.write('EXIT'.encode())          # normal cmdfiles are encoded
                        logger.info(f'EXIT-signal CMD file opened as {txt}')
                    logger.info(f'EXIT-signal CMD file successfully written for PID #{pid}')

        # copy existing updater utility to temporary path so it can be replaced during the update
        import shutil
        original_updater_path = 'updater.exe' if constants.IS_COMPILED else os.path.join(constants.BIN_DIR, 'updater.py')
        active_updater_path = qthelpers.addPathSuffix(original_updater_path, '_active', unique=True)
        logger.info(f'Copying updater-utility to temporary path ({active_updater_path})')
        shutil.copy2(original_updater_path, active_updater_path)

        # run updater utility and exit current PyPlayer instance
        logger.info('PyPlayer closing, updater-utility starting...')
        file, play_and_exit = self.video if self.video else qtstart.args.file, qtstart.args.play_and_exit
        cmd_args = f'\"{file if file else ""}\" {play_and_exit if play_and_exit else ""}'
        subprocess.Popen(f'{active_updater_path} '
                         f'--zip {download_path} '                          # the zip file we want the updater to unpack
                         f'--cmd "{constants.SCRIPT_PATH} {cmd_args}" '     # the command the updater should run to restart us
                         f'--lock-files {" ".join(pid_files)} '             # tell updater to wait for each PID file to be deleted
                         f'--add-to-report "{active_updater_path}"')        # add temp-updater's path to report so we can delete it after
        return qtstart.exit(self)
    except:
        logger.warning(f'(!) Could not download latest version. New naming format? Missing updater? {format_exc()}')
        qthelpers.getPopup(title='Update download failed',                  # download_update does not occur inside a thread, so this is safe
                           icon=QMessageBox.Warning,
                           text=f'Update {latest_version} failed to install.',
                           textInformative='There could have been an error while creating the download link, '
                                           'the download may have failed, the update utility may be missing, '
                                           'or perhaps newer versions use a different format for updating.\n\n'
                                           f'You can manually download the {HYPERLINK}.',
                           textDetailed=format_exc()).exec()
        self.statusbar.setVisible(self.actionShowStatusBar.isChecked())     # restore statusbar to original state if update failed
        self.save_progress_bar.setMaximum(0)                                # set progress bar's maximum to 0 to restore indeterminate style
        return self.show_save_progress_signal.emit(False)                   # hide progress bar if update failed


def validate_update(self, update_report):
    logger.info(f'Update report detected at {update_report}, validating...')
    with open(update_report) as report:
        lines = tuple(line.strip() for line in report)
        active_updater_path, download_path, status = lines[:3]

        try: os.remove(active_updater_path)
        except: self.log(f'Could not clean up temporary updater after update: {download_path}')
        try: os.remove(download_path)
        except: self.log(f'Could not clean up .zip file after update: {download_path}')

        if status != 'SUCCESS':
            logger.warning(f'(!) UPDATE FAILED: {status}')
            qthelpers.getPopup(title='Update failed',
                               icon=QMessageBox.Warning,
                               text='The attempted update failed while unpacking.',
                               textInformative=f'If needed, you can manually download the {HYPERLINK}.',
                               textDetailed=status).exec()
    try: os.remove(update_report)
    except: logger.warning('Failed to delete update report after validation.')
    logger.info('Update validated.')
