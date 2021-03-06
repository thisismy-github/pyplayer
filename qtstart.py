''' Contains several single-use bits of startup code that were originally in main.pyw.
    This file might be removed in the future, since it slightly overcomplicates things.
    thisismy-github 3/14/22 '''

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets as QtW
import config
import constants
import qthelpers

import os
import sys
import logging
import argparse
from threading import Thread
from traceback import format_exc


# ---------------------
# Arguments
# ---------------------
parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='?', help='Specifies a filepath to open')     # '?' allows for optional positionals
parser.add_argument('--exit', action='store_true', help='Instantly exits. Used when sending media to other instances')
parser.add_argument('--play-and-exit', action='store_true', help='Automatically exits at the conclusion of a media file')
parser.add_argument('-v', '--vlc', default='--gain=2.0', help='Specifies arguments to pass to the underlying VLC instance')
args = parser.parse_args()
if args.exit: sys.exit(100)


# ---------------------
# Logging
# ---------------------
file_handler = logging.FileHandler(constants.LOG_PATH, 'w', delay=False)
file_handler.setLevel(logging.INFO)
logging.basicConfig(
    level=logging.DEBUG,
    format='{asctime} {lineno:<3} {levelname} {funcName}: {message}',
    datefmt='%m/%d/%y | %I:%M:%S%p',
    style='{',
    handlers=(file_handler, logging.StreamHandler())
)
logging.info(f'Logger initalized at {constants.LOG_PATH}.')
logging.info(f'Arguments: {args}')


# ---------------------
# System Tray Icon
# ---------------------
def exit(self: QtW.QMainWindow):
    try:
        self.closed = True
        logging.info('Exiting. self.closed set to True.')

        if self.tray_icon is not None:
            if self.dialog_settings.groupTray.isChecked() and not self.isHidden():
                self.close()
                if self.close_cancel_selected: return   # in case we show a file-deletion dialog and the user clicks cancel/X
            self.tray_icon.setVisible(False)
            logging.info('System tray icon stopped.')

        self.app.quit()
        logging.info('QApplication quit.')

        try: config.saveConfig(self, constants.CONFIG_PATH)
        except: logging.warning(f'Error saving configuration: {format_exc()}')
        logging.info('Configuration has been saved. Goodbye.')
    except: logging.critical(f'\n\n(!)QTSTART.EXIT FAILED: {format_exc()}')
    finally: self.closed = True                         # absolutely must be True or else daemon threads will never close


def get_tray_icon(self: QtW.QMainWindow) -> QtW.QSystemTrayIcon:
    ''' Generates the system tray icon. For a while I was using pystray because I genuinely forgot QSystemTrayIcon existed.
        QSystemTrayIcon has some issues, one being the fact that if placed in the "hidden icons" area on Windows, that area will
        close while the tray icon's context menu is open. That's not much of an issue with this very barebones tray icon, but it
        may become an issue if the tray icon is expanded upon. Pystray is still a decent (albeit heavy) fallback if necessary. '''
    def handle_click(reason: QtW.QSystemTrayIcon.ActivationReason):
        if reason == QtW.QSystemTrayIcon.Context:
            action_show = QtW.QAction('&PyPlayer')
            action_show.triggered.connect(lambda: qthelpers.showWindow(self))
            action_settings = QtW.QAction('&Settings')
            action_settings.triggered.connect(self.dialog_settings.exec)
            action_exit = QtW.QAction('&Exit')
            action_exit.triggered.connect(lambda: exit(self))
            menu = QtW.QMenu()
            menu.addAction(action_show)
            menu.addAction(action_settings)
            menu.addSeparator()
            menu.addAction(action_exit)
            return menu.exec(QtGui.QCursor.pos())
        if reason == QtW.QSystemTrayIcon.Trigger: return qthelpers.showWindow(self)
        if reason == QtW.QSystemTrayIcon.MiddleClick: return exit(self)

    tray = QtW.QSystemTrayIcon(self.icons['window'])
    tray.setToolTip('PyPlayer')
    tray.setVisible(True)
    tray.activated.connect(handle_click)
    return tray


# ---------------------
# GUI Setup
# ---------------------
def after_show_setup(self: QtW.QMainWindow):
    self.handle_updates_signal.emit(True)           # check for/download/validate pending updates

    if args.file:
        if not os.path.exists(args.file):
            self.update_title_signal.emit()
            self.log(f'Command-line file {args.file} does not exist.')
        else:
            try:
                logging.info(f'Opening pre-selected path: {args.file}')
                self.open(args.file)
                self.log(f'Command-line path opened: {args.file}')
            except:
                self.update_title_signal.emit()
                self.log(f'Failed to open pre-selected path: {args.file}')
                logging.error(format_exc())
    else: self.update_title_signal.emit()

    if self.last_window_size is None: self.last_window_size = self.size()
    if self.last_window_pos is None: self.last_window_pos = self.pos()

    recent_files_count = self.dialog_settings.spinRecentFiles.value()
    files = config.cfg.load('recent_files', '', '<|>', section='general')
    if recent_files_count <= 25:
        recent_files = self.recent_files
        append = recent_files.append
        for file in files:
            if os.path.isfile(file) and file not in recent_files: append(file)
            if len(recent_files) == recent_files_count: break
    else: self.recent_files += files[-recent_files_count:]

    if config.cfg.grouptray:                        # start system tray icon
        logging.info('Creating system tray icon...')
        self.app.setQuitOnLastWindowClosed(False)   # ensure qt does not exit until we tell it to
        self.tray_icon = get_tray_icon(self)

    Thread(target=self.fast_start_interface_thread, daemon=True).start()
    connect_shortcuts(self)                         # setup and connect hotkeys


def connect_shortcuts(self: QtW.QMainWindow):
    # TODO add standardShortcuts | TODO are these noticably slower than using keyPressEvent or am I crazy?
    def increment_volume_boost(value=0.5):
        self.volume_boost = min(self.volume_boost + value, 5)
        self.set_volume(self.sliderVolume.value())
        self.log_on_player(f'{self.volume_boost:.1f}x volume multiplier', marq_key='VolumeBoost', log=False)

    def increment_subtitle_delay(value=50):
        if (self.player.video_get_spu_count() - 1) <= 0: return self.log_on_player('No subtitles available', marq_key='SubtitleDelay', log=False)
        new_delay = self.player.video_get_spu_delay() + (value * 1000)
        self.player.video_set_spu_delay(new_delay)
        if new_delay == 0: self.log_on_player('Subtitle delay 0ms', marq_key='SubtitleDelay', log=False)
        else: self.log_on_player(f'Subtitle delay {new_delay/ 1000:.0f}ms ({"later" if new_delay > 0 else "sooner"})', marq_key='SubtitleDelay', log=False)

    def toggle_loop():
        self.log_on_player(f'Looping {"disabled" if self.actionLoop.isChecked() else "enabled"}', marq_key='Loop', log=False),
        self.actionLoop.trigger()

    shortcut_actions = {      # NOTE: having empty rows in tabKeys's formLayout (in QtDesigner) causes actions below empty rows to not work
        'pause':              self.pause,
        'plus5seconds':       self.navigate,
        'minus5seconds':      lambda: self.navigate(forward=False, seconds=5),
        'plus10seconds':      lambda: self.navigate(forward=True, seconds=10),
        'minus10seconds':     lambda: self.navigate(forward=False, seconds=10),
        'plusframe':          self.spinFrame.stepUp,
        'minusframe':         self.spinFrame.stepDown,
        'plusspeed':          lambda: self.set_playback_speed(self.playback_speed + 0.05),
        'minusspeed':         lambda: self.set_playback_speed(self.playback_speed - 0.05),
        'plus5volume':        lambda: self.increment_volume(5),
        'minus5volume':       lambda: self.increment_volume(-5),
        'plusvolumeboost':    increment_volume_boost,
        'minusvolumeboost':   lambda: increment_volume_boost(-0.5),
        'mute':               self.toggle_mute,
        'fullscreen':         self.actionFullscreen.trigger,
        'crop':               self.actionCrop.trigger,
        'loop':               toggle_loop,
        'nextmedia':          self.cycle_media,
        'previousmedia':      lambda: self.cycle_media(next=False),
        'forward':            lambda: self.cycle_recent_files(forward=True),
        'back':               lambda: self.cycle_recent_files(forward=False),
        'plussubtitledelay':  increment_subtitle_delay,
        'minussubtitledelay': lambda: increment_subtitle_delay(-50),
        'cyclesubtitles':     self.cycle_subtitle_track,
        'markdeleted':        self.actionMarkDeleted.trigger,
        'deleteimmediately':  self.delete,
        'snapshot':           lambda: self.snapshot(mode='full'),
        'quicksnapshot':      self.snapshot,
    }
    self.shortcuts = {action_name: (QtW.QShortcut(self, context=3), QtW.QShortcut(self, context=3)) for action_name in shortcut_actions}
    #self.shortcuts = {action_name: (Qtself.QKeySequence(), Qtself.QKeySequence()) for action_name in shortcut_actions}

    get_refresh_shortcuts_lambda = lambda widget: lambda: self.refresh_shortcuts(widget)
    for layout in qthelpers.formGetItemsInColumn(self.dialog_settings.formKeys, 1):
        for keySequenceEdit in qthelpers.layoutGetItems(layout):
            name = keySequenceEdit.objectName()
            index = 0 if name[-1] != '_' else 1
            name = name.rstrip('_')
            self.shortcuts[name][index].activated.connect(shortcut_actions[name])
            keySequenceEdit.editingFinished.connect(get_refresh_shortcuts_lambda(keySequenceEdit))  # lambda-in-iterable workaround
    self.refresh_shortcuts()


def connect_widget_signals(self: QtW.QMainWindow):
    self._open_signal.connect(self._open)
    self._save_open_signal.connect(lambda file, remember_old_file: self.open(file=file, remember_old_file=remember_old_file))
    self.fast_start_open_signal.connect(self.fast_start_open)
    self.restart_signal.connect(self.restart)
    self.force_pause_signal.connect(self.force_pause)
    self.show_ffmpeg_warning_signal.connect(constants._display_ffmpeg_warning)
    self.show_trim_dialog_signal.connect(self.show_trim_dialog)
    self.update_progress_signal.connect(self.update_progress_slot)
    self.update_title_signal.connect(self.update_title)
    self.show_save_progress_signal.connect(self.save_progress_bar.setVisible)
    self.disable_crop_mode_signal.connect(self.disable_crop_mode)
    self.handle_updates_signal.connect(self.handle_updates)
    self._handle_updates_signal.connect(self._handle_updates)
    self.log_signal.connect(self.log_slot)
    self.log = self.log_signal.emit

    self.sliderVolume.valueChanged.connect(self.set_volume)
    self.buttonPause.clicked.connect(self.pause)
    self.actionOpen.triggered.connect(self.open)
    self.menuRecent.aboutToShow.connect(self.refresh_recent_menu)
    self.actionClearRecent.triggered.connect(lambda: self.recent_files.clear())    # TODO why won't .clear work on its own?
    self.actionExploreMediaPath.triggered.connect(self.explore)
    self.actionCopyMediaPath.triggered.connect(self.copy)
    self.actionSave.triggered.connect(self.save)
    self.actionSaveAs.triggered.connect(self.save_as)
    self.actionStop.triggered.connect(self.stop)
    self.actionMinimize.triggered.connect(self.close)
    self.actionExit.triggered.connect(lambda: exit(self))
    self.actionSettings.triggered.connect(self.dialog_settings.exec)
    self.actionLoop.triggered.connect(self.buttonLoop.setChecked)
    self.actionAutoplay.triggered.connect(self.buttonAutoplay.setChecked)
    self.actionSnapshot.triggered.connect(lambda: self.snapshot(mode='full'))
    self.actionQuickSnapshot.triggered.connect(self.snapshot)
    self.actionSnapshotOpenLast.triggered.connect(lambda: self.snapshot(mode='open'))
    self.actionSnapshotOpenLastInDefault.triggered.connect(lambda: self.snapshot(mode='view'))
    self.actionSnapshotExploreLastPath.triggered.connect(lambda: self.explore(config.cfg.last_snapshot_path, 'Last snapshot'))
    self.actionSnapshotCopyLastPath.triggered.connect(lambda: self.copy(config.cfg.last_snapshot_path, 'Last snapshot'))
    self.actionMarkDeleted.triggered.connect(self.buttonMarkDeleted.setChecked)
    self.actionMarkDeleted.triggered.connect(self.mark_for_deletion)
    self.actionClearMarked.triggered.connect(self.clear_marked_for_deletion)
    self.actionShowDeletePrompt.triggered.connect(self.show_delete_prompt)
    self.actionDeleteImmediately.triggered.connect(self.delete)
    self.menuConcatenate.triggered.connect(self.concatenate)
    self.menuVideoTracks.aboutToShow.connect(lambda: self.refresh_track_menu(self.menuVideoTracks))
    self.menuSubtitles.aboutToShow.connect(lambda: self.refresh_track_menu(self.menuSubtitles))
    self.actionAddSubtitleFile.triggered.connect(self.browse_for_subtitle_file)
    self.menuRotate.triggered.connect(self.rotate_video)
    self.actionCrop.triggered.connect(self.set_crop_mode)
    self.actionResize.triggered.connect(self.resize_media)
    self.menuAudioTracks.aboutToShow.connect(lambda: self.refresh_track_menu(self.menuAudioTracks))
    self.actionRemoveAudio.triggered.connect(self.remove_track)
    self.actionRemoveVideo.triggered.connect(lambda: self.remove_track(audio=False))
    self.actionAmplifyVolume.triggered.connect(self.amplify_audio)
    self.actionReplaceAudio.triggered.connect(self.replace_audio)
    self.actionAddAudioTrack.triggered.connect(self.add_audio)
    self.actionShowMenuBar.triggered.connect(self.set_menubar_visible)
    self.actionShowStatusBar.triggered.connect(self.set_statusbar_visible)
    self.actionShowProgressBar.triggered.connect(self.set_progressbar_visible)
    self.actionShowAdvancedControls.triggered.connect(self.set_advancedcontrols_visible)
    self.actionFullscreen.triggered.connect(self.set_fullscreen)
    self.actionSnapSize.triggered.connect(self.snap_to_native_size)
    self.actionSnapRatio.triggered.connect(self.snap_to_player_size)
    self.actionSnapRatioShrink.triggered.connect(lambda: self.snap_to_player_size(shrink=True))
    self.actionCheckForUpdates.triggered.connect(self.handle_updates)
    self.actionViewLog.triggered.connect(lambda: qthelpers.openPath(constants.LOG_PATH))
    self.actionViewInstallFolder.triggered.connect(lambda: qthelpers.openPath(constants.CWD))
    self.actionAboutQt.triggered.connect(lambda: QtW.QMessageBox.aboutQt(None, 'About Qt'))
    self.actionAbout.triggered.connect(self.show_about_dialog)
    #self.check_clamp.stateChanged.connect(self.clamp)
    self.lineOutput.returnPressed.connect(self.save)
    self.lineCurrentTime.returnPressed.connect(self.manually_update_current_time)
    self.spinHour.valueChanged.connect(self.update_time_spins)
    self.spinMinute.valueChanged.connect(self.update_time_spins)
    self.spinSecond.valueChanged.connect(self.update_time_spins)
    self.spinFrame.valueChanged.connect(self.update_frame_spin)
    self.sliderProgress.actionTriggered.connect(self.page_step_slider)

    self.buttonTrimStart.toggled.connect(self.set_trim_start)
    self.buttonTrimEnd.toggled.connect(self.set_trim_end)
    self.buttonNext.clicked.connect(self.cycle_media)
    self.buttonPrevious.clicked.connect(lambda: self.cycle_media(next=False))
    self.buttonExploreMediaPath.clicked.connect(self.actionExploreMediaPath.trigger)
    self.buttonMarkDeleted.clicked.connect(self.actionMarkDeleted.trigger)
    self.buttonSnapshot.clicked.connect(self.actionQuickSnapshot.trigger)
    self.buttonLoop.clicked.connect(self.actionLoop.trigger)
    self.buttonAutoplay.clicked.connect(self.actionAutoplay.trigger)

    settings = self.dialog_settings
    settings.accepted.connect(self.update_title)
    settings.comboThemes.currentTextChanged.connect(self.set_theme)
    settings.buttonRefreshThemes.clicked.connect(self.refresh_theme_combo)
    settings.buttonBrowseDefaultOutputPath.clicked.connect(lambda: self.browse_for_directory_lineedit(settings.lineDefaultOutputPath, 'default output'))
    settings.default_snapshot_path_browse.clicked.connect(lambda: self.browse_for_directory_lineedit(settings.lineDefaultSnapshotPath, 'default snapshot'))
    settings.buttonHoverFontColor.clicked.connect(self.show_color_picker)
    settings.checkHighPrecisionProgress.toggled.connect(self.swap_slider_styles)
    settings.checkScaleFiltering.toggled.connect(self.gifPlayer.update)
    settings.buttonCheckForUpdates.clicked.connect(self.handle_updates)
    settings.checkZoomPrecise.toggled.connect(self.gifPlayer._updatePreciseZoom)
    settings.spinZoomMinimumFactor.valueChanged.connect(lambda: settings.checkZoomAutoDisable1x.setEnabled(settings.spinZoomMinimumFactor.value() == 1))
    settings.spinZoomSmoothFactor.valueChanged.connect(self.gifPlayer._updateSmoothZoomFactor)

    self.position_button_group = QtW.QButtonGroup(settings)
    for button in (settings.radioTextPosition0, settings.radioTextPosition1, settings.radioTextPosition2,
                   settings.radioTextPosition4, settings.radioTextPosition5, settings.radioTextPosition6,
                   settings.radioTextPosition8, settings.radioTextPosition9, settings.radioTextPosition10):
        self.position_button_group.addButton(button)
    self.position_button_group.buttonToggled.connect(self.vlc.set_text_position)
    settings.spinTextHeight.valueChanged.connect(self.vlc.set_text_height)
    settings.spinTextX.valueChanged.connect(self.vlc.set_text_x)
    settings.spinTextY.valueChanged.connect(self.vlc.set_text_y)
    settings.spinTextOpacity.valueChanged.connect(self.vlc.set_text_opacity)
    settings.comboScaleImages.currentIndexChanged.connect(self.gifPlayer._updateImageScale)
    settings.comboScaleArt.currentIndexChanged.connect(self.gifPlayer._updateArtScale)
    settings.comboScaleGifs.currentIndexChanged.connect(self.gifPlayer._updateGifScale)

    # NOTE: this looks weird if the gif has custom frame-by-frame delays, but it's perfectly fine
    self.gifPlayer.gif.frameChanged.connect(self.update_progress)
