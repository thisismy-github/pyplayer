import qtstart
import constants
import qthelpers
from util import get_unique_path

from PyQt5.QtWidgets import QMessageBox, QApplication
import os
import time
import logging
import subprocess
from traceback import format_exc


logger = logging.getLogger('update.py')
HYPERLINK = f'<a href="{constants.REPOSITORY_URL}/releases/latest">latest release on GitHub here</a>.'


def get_later_version(version_a: str, version_b: str) -> str:
    ''' Returns the greater of two version strings, with mild future-proofing. Allows for an
        arbitrary number in each sequence of the version, with an arbitrary number of sequences.
        https://stackoverflow.com/questions/11887762/how-do-i-compare-version-numbers-in-python '''
    atuple = tuple(map(int, (version_a.split('.'))))
    btuple = tuple(map(int, (version_b.split('.'))))
    return version_a if atuple > btuple else version_b


def check_for_update(self, log: bool = True, _launch: bool = False) -> None:
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
            self.log_on_statusbar_signal.emit('GitHub release URL could not be parsed correctly.')
            return self._handle_updates_signal.emit(
                dict(failed=True),
                dict(title='Update URL mismatch',
                     icon=QMessageBox.Warning,
                     text=f'The URL for the latest release on GitHub has an unexpected format.\n\nGitHub version: "{latest_version}"\nCurrent version: "{current_version}"',
                     textInformative='Newer versions might use a different naming scheme, or perhaps '
                                     'there was an error while checking. You can manually check the ' + HYPERLINK)
            )

        if get_later_version(latest_version, current_version) != current_version:    # current version is older than latest version
            if constants.IS_COMPILED and constants.IS_WINDOWS:          # TODO Windows only for now (and no auto-updating directly from the script)
                return self._handle_updates_signal.emit(
                    dict(latest_version_url=latest_version_url),
                    dict(title=f'Update {latest_version} available',
                         icon=QMessageBox.Information,
                         buttons=(QMessageBox.Yes | QMessageBox.No),    # TODO | QMessageBox.Ignore
                         text=f'An update is available on GitHub ({current_version} -> {latest_version}). '
                              'Would you\nlike to download and install this update automatically?',
                         textInformative='You can manually view the ' + HYPERLINK)
                )
            else:                                                       # non-windows version of popup (no auto-updater yet)
                if constants.IS_COMPILED: reason = 'Auto-updating is currently only available on Windows.<br><br>'      # \n breaks hyperlinks
                else: reason = 'Because you\'re running directly from the script, auto-updating is disabled.<br><br>'   # \n breaks hyperlinks
                return self._handle_updates_signal.emit(
                    dict(latest_version_url=latest_version_url),
                    dict(title=f'Update {latest_version} available',
                         icon=QMessageBox.Information,
                         text=f'An update is available on GitHub ({current_version} -> {latest_version}).',
                         textInformative=f'{reason}You can view the {HYPERLINK}')
                )
        elif log: self.log_on_statusbar_signal.emit('You\'re up to date!')
    except requests.exceptions.ConnectionError:
        if _launch: logger.warning('Update check was unable to reach GitHub (no internet connection?).')
        else: self.log_on_statusbar_signal.emit('Update check was unable to reach GitHub (no internet connection?).')
    except: self.log_on_statusbar_signal.emit(f'(!) UPDATE-CHECK FAILED: {format_exc()}')
    self._handle_updates_signal.emit({}, {})                            # call empty signal to perform cleanup


def download_update(self, latest_version: str, download_url: str, download_path: str) -> None:
    import requests
    try:
        logger.info(f'Downloading version {latest_version} from {download_url} to {download_path}')
        download_response = requests.get(download_url, stream=True)
        download_response.raise_for_status()
        total_size = int(download_response.headers.get('content-length'))
        downloaded = 0

        self.save_progress_bar.setMaximum(100)
        self.save_progress_bar.setVisible(True)
        self.statusbar.setVisible(True)
        mb_per_chunk = 3

        with open(download_path, 'wb') as file:
            logger.info(f'Downloading {total_size / 1048576:.2f}mb')
            chunk_size = mb_per_chunk * (1024 * 1024)
            start_time = time.time()
            for chunk in download_response.iter_content(chunk_size=chunk_size):
                file.write(chunk)
                downloaded += len(chunk)
                percent = (downloaded / total_size) * 100
                self.save_progress_bar.setValue(percent)

                message = f'{percent:.0f}% ({downloaded / 1048576:.0f}mb/{total_size / 1048576:.2f}mb)'
                self.statusbar.showMessage(message)
                self.save_progress_bar.setFormat(message)
                QApplication.processEvents()                # manually update GUI since this is not taking place in a thread

        message = f'Update downloaded after {time.time() - start_time:.1f} seconds, restarting...'
        self.log_on_statusbar_signal.emit(message)
        self.save_progress_bar.setFormat(message)

        # send exit-signals to all PyPlayer instances through their PID files
        logger.info('Sending EXIT-signals to any other active PyPlayer instances...')
        pid_files = []
        for file in os.listdir(constants.TEMP_DIR):
            if file[-4:] == '.pid':
                pid_file = os.path.join(constants.TEMP_DIR, file)
                try: os.remove(pid_file)                    # try to delete PID file to confirm whether it's active or not
                except:                                     # couldn't delete PID file -> send exit-signal to its instance
                    logger.info(f'Active PyPlayer instance detected through PID file {pid_file}')
                    pid_files.append(f'"{pid_file}"')
                    pid = file[:-4]
                    if pid == str(os.getpid()): continue    # do not send exit-signal to ourselves (but still append to pid_files)
                    cmdpath = os.path.join(constants.TEMP_DIR, f'cmd.{pid}.txt')
                    with open(cmdpath, 'wb') as txt:
                        txt.write('EXIT'.encode())          # normal cmdfiles are encoded
                        logger.info(f'EXIT-signal CMD file opened as {txt}')
                    logger.info(f'EXIT-signal CMD file successfully written for PID #{pid}')

        # locate updater executable -> check both root folder and bin/pyqt5 folder
        ext = '.exe' if constants.IS_WINDOWS else ''
        original_updater_path = os.path.join(constants.CWD, 'updater') + ext    # `IS_COMPILED` is assumed here
        if not os.path.exists(original_updater_path):
            original_updater_path = os.path.join(constants.BIN_DIR, 'updater') + ext
            if not os.path.exists(original_updater_path):
                raise Exception(f'Could not find updater at {original_updater_path}')

        # copy updater utility to temporary path so it can be replaced during the update
        import shutil
        active_updater_path = get_unique_path(os.path.join(constants.CWD, 'updater_active') + ext)
        logger.info(f'Copying updater-utility to temporary path ({active_updater_path})')
        shutil.copyfile(original_updater_path, active_updater_path)

        # run updater utility and exit current PyPlayer instance
        args = []
        if self.video or qtstart.args.file: args.append(f'"{self.video or qtstart.args.file}"')
        if qtstart.args.play_and_exit: args.append('"--play-and-exit"')
        cmd_args = f' {" ".join(args)}' if args else ''
        add_to_report = f'"{constants.VERSION.split()[1]} -> {latest_version}" "{active_updater_path}"'

        logger.info('PyPlayer closing, updater-utility starting...')
        updater_cmd = (f'{active_updater_path} {download_path} '        # the updater and the zip file we want it to unpack
                       f'--destination {constants.CWD} '                # the destination to unzip the file to
                       f'--cmd "{constants.SCRIPT_PATH}{cmd_args}" '    # the command the updater should run to restart us
                       f'--lock-files {" ".join(pid_files)} '           # tell updater to wait for each PID file to be deleted
                       f'--add-to-report {add_to_report}')              # add versions and temp-updater's path to report
        logger.info(updater_cmd)
        subprocess.Popen(updater_cmd)
        return qtstart.exit(self)
    except:
        logger.warning(f'(!) Could not download latest version. New naming format? Missing updater? {format_exc()}')

        updater_removal_failed = ''
        download_removal_failed = ''
        if os.path.exists(active_updater_path):
            try: os.remove(active_updater_path)
            except: updater_removal_failed = f'Additionally, the temporary update-utility file at {active_updater_path} could not be deleted.<br><br>'
        if os.path.exists(download_path):
            try: os.remove(download_path)
            except: download_removal_failed = f'Additionally, the downloaded .zip file at {download_path} could not be deleted.<br><br>'

        qthelpers.getPopup(title='Update download failed',                  # download_update does not occur inside a thread, so this is safe
                           icon=QMessageBox.Warning,
                           text=f'Update {latest_version} failed to install.',
                           textInformative='There could have been an error while creating the download link, '
                                           'the download may have failed, the update utility may be missing, '
                                           'or perhaps newer versions use a different format for updating.<br><br>'   # \n breaks hyperlinks
                                           f'{updater_removal_failed}{download_removal_failed}'
                                           'You can still manually download the ' + HYPERLINK,
                           textDetailed=format_exc(),
                           textDetailedAutoOpen=True,
                           **self.get_popup_location()).exec()

        self.statusbar.setVisible(self.actionShowStatusBar.isChecked())     # restore statusbar to original state if update failed
        self.save_progress_bar.setMaximum(0)                                # set progress bar's maximum to 0 to restore indeterminate style
        self.save_progress_bar.setFormat('Saving...')                       # reset progress bar to default text
        return self.save_progress_bar.setVisible(False)                     # hide progress bar if update failed


def validate_update(self, update_report: str) -> None:
    logger.info(f'Update report detected at {update_report}, validating...')
    with open(update_report) as report:
        lines = tuple(line.strip() for line in report)
        version_change, active_updater_path, download_path, status = lines  # version_change = '<old_version> -> <new_version>'

        try: os.remove(active_updater_path)
        except: self.log_on_statusbar_signal.emit(f'Could not clean up temporary updater after update: {download_path}')
        try: os.remove(download_path)
        except: self.log_on_statusbar_signal.emit(f'Could not clean up .zip file after update: {download_path}')

        if status != 'SUCCESS':
            logger.warning(f'(!) UPDATE FAILED: {status}')
            return qthelpers.getPopup(title='Update failed',
                                      icon=QMessageBox.Warning,
                                      text='The attempted update failed while unpacking.',
                                      textInformative='If needed, you can manually download the ' + HYPERLINK,
                                      textDetailed=status,
                                      textDetailedAutoOpen=True,
                                      **self.get_popup_location()).exec()
    try: os.remove(update_report)
    except: logger.warning('Failed to delete update report after validation.')
    logger.info('Update validated.')
    update_migration(self, version_change.split(' -> ')[0])
    self.log_on_statusbar_signal.emit(f'Update from {version_change} successful.')


def update_migration(self, old_version: str) -> None:
    ''' Handles additional work required to migrate
        `old_version` to the latest version, if any. '''
    settings = self.dialog_settings
    older_than = lambda v: old_version != v and get_later_version(old_version, v) == v
    if older_than('0.3.0'):     # updated from 0.1.0 - 0.2.0
        qthelpers.getPopup(title='Update successful, but reinstall recommended',
                           text='The update was successful, but there has been a massive change\n'
                                'in PyPlayer\'s file structure (bringing a significant size reduction)\n'
                                'that cannot be applied through the update utility. Reinstalling\n'
                                'manually is not required, but is highly recommended.',
                           textInformative='You can redownload the ' + HYPERLINK + ' Be sure to copy '
                                           'over config.ini and any personal files you may have saved.',
                           **self.get_popup_location()).exec()
    if older_than('0.4.0'):     # updated from <=0.3.0
        old_ffmpeg = os.path.join(constants.CWD, 'plugins', 'ffmpeg.exe')
        if os.path.exists(old_ffmpeg) and os.path.getsize(old_ffmpeg) == 35445760:
            try: os.remove(old_ffmpeg)
            except: logger.info('(!) Failed to remove outdated ffmpeg.exe.')
    if older_than('0.5.0'):     # updated from <=0.4.0
        import config
        new_format = settings.lineSnapshotNameFormat.text().strip().replace('?video', '?name')
        settings.lineSnapshotNameFormat.setText(new_format)
        config.cfg.saveTo('settings', 'linesnapshotnameformat', new_format)
        self.recent_files += config.cfg.loadFrom('general', 'recent_videos', '', '<|>')
    if older_than('0.6.0'):     # updated from <=0.5.0
        import config
        new_format = settings.lineWindowTitleFormat.text().strip().replace('?size', '?resolution')
        settings.lineSnapshotNameFormat.setText(new_format)
        settings.comboScaleImages.setCurrentIndex(settings.comboScaleImages.currentIndex() + 1)
        settings.comboScaleArt.setCurrentIndex(settings.comboScaleArt.currentIndex() + 1)
        settings.checkFocusIgnoreAutoplay.setChecked(config.cfg.loadFrom('settings', 'checkignorefocuswithautoplay', True))
        settings.checkTrayResetFirstFileOnRestore.setChecked(config.cfg.loadFrom('settings', 'checkfirstfiletrayreset', True))
        try: self.resize(*config.cfg.load('size', '871,588', ',', int, tuple))
        except: pass
        try:
            screen = self.app.primaryScreen().size()
            self.move(*config.cfg.load('pos', f'{screen.width() / 2 - (self.width() / 2):.0f},{screen.height() / 2 - (self.height() / 2):.0f}', ',', int, tuple))
        except: pass
