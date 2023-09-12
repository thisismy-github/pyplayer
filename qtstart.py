''' Contains several single-use bits of startup code that were originally in main.pyw.
    This file might be removed in the future, since it slightly overcomplicates things.

    thisismy-github 3/14/22 '''

from PyQt5 import QtGui
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
parser.add_argument('--minimized', action='store_true', help='Start minimized (to the tray, if enabled). Useful when used as a startup program')
parser.add_argument('-v', '--vlc', default='--gain=2.0', help='Specifies arguments to pass to the underlying VLC instance')
parser.add_argument('-d', '--debug', action='store_true', help='Outputs debug messages to the log file.')
args = parser.parse_args()
if args.exit: sys.exit(100)


# ---------------------
# Logging
# ---------------------
if os.path.exists(constants.LOG_PATH):                  # backup existing log and delete outdated logs
    sep = os.sep
    log_path = constants.LOG_PATH
    temp_dir = f'{constants.TEMP_DIR}{sep}logs'
    prefix, suffix = os.path.splitext(os.path.basename(log_path))
    p_len = len(prefix)
    s_len = len(suffix)
    if os.path.isdir(temp_dir):
        logs = [f for f in os.listdir(temp_dir) if f[:p_len] == prefix and f[-s_len:] == suffix]
        for outdated_log in logs[:-9]:
            try: os.remove(f'{temp_dir}{sep}{outdated_log}')
            except: pass
    new_name = f'{prefix}.{os.stat(log_path).st_mtime_ns}{suffix}'
    try: os.renames(log_path, f'{temp_dir}{sep}{new_name}')
    except: pass

file_handler = logging.FileHandler(constants.LOG_PATH, 'w', delay=False)
if not args.debug:                                      # don't save debug messages to file (if desired)
    file_handler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.DEBUG,
    force=True,
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
                if self.close_cancel_selected:          # in case we show a file-deletion dialog and the user clicks cancel/X
                    return
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
    ''' Generates a system tray icon. Uses `QSystemTrayIcon`, which has issues:
        - If the icon is in the overflow menu on Windows, the overflow menu will
          close itself while the icon's context menu is open.
        - Some Linux distros seem to not show this icon at all. Cause unknown.

        Originally the `pystray` library was used (I forgot `QSystemTrayIcon`
        existed) and may work as a decent (albeit heavy) fallback if the above
        issues cannot be resolved or we expand upon our barebones icon. '''

    def handle_click(reason: QtW.QSystemTrayIcon.ActivationReason):
        if reason == QtW.QSystemTrayIcon.Context:       # right-click
            action_show = QtW.QAction('&PyPlayer')
            action_show.triggered.connect(lambda: qthelpers.showWindow(self))
            menu = QtW.QMenu()
            menu.addAction(action_show)
            menu.addAction(self.actionSettings)
            menu.addMenu(self.menuRecent)
            menu.addSeparator()
            menu.addAction(self.actionViewLog)
            menu.addAction(self.actionViewInstallFolder)
            menu.addAction(self.actionViewLastDirectory)
            menu.addSeparator()
            menu.addAction(self.actionStop)
            menu.addAction(self.actionExit)
            return menu.exec(QtGui.QCursor.pos())
        if reason == QtW.QSystemTrayIcon.Trigger:       # left-click
            return qthelpers.showWindow(self)
        if reason == QtW.QSystemTrayIcon.MiddleClick:   # middle-click
            index = self.dialog_settings.comboTrayMiddleClick.currentIndex()
            return self.middle_click_tray_actions[index]()

    tray = QtW.QSystemTrayIcon(self.icons['window'])
    tray.setToolTip('PyPlayer')
    tray.setVisible(True)
    tray.activated.connect(handle_click)
    return tray


# ---------------------
# GUI Setup
# ---------------------
def after_show_setup(self: QtW.QMainWindow):
    ''' Additional setup for `self` (our main window/GUI class)
        that is most appropriate to do after the window is shown. '''

    # check for/download/validate pending updates
    self.handle_updates_signal.emit(True)

    # open file if desired (we only get this far if no other sessions were open)
    if args.file:
        if not os.path.exists(args.file):
            self.refresh_title_signal.emit()
            self.log_on_statusbar_signal.emit(f'Command-line file {args.file} does not exist.')
        else:
            try:
                logging.info(f'Opening pre-selected path: {args.file}')
                self.open(args.file)
                self.log_on_statusbar_signal.emit(f'Command-line path opened: {args.file}')
            except:
                self.refresh_title_signal.emit()
                self.log_on_statusbar_signal.emit(f'Failed to open pre-selected path: {args.file}')
                logging.error(format_exc())
    else:
        self.refresh_title_signal.emit()

    # set last window size/pos if window still has default geometry after loading config
    if self.last_window_size is None: self.last_window_size = self.size()
    if self.last_window_pos is None: self.last_window_pos = self.pos()

    # populate recent files list
    recent_files_count = self.dialog_settings.spinRecentFiles.value()
    files = config.cfg.load('recent_files', '', '<|>', section='general')
    if recent_files_count > 25:
        self.recent_files += files[-recent_files_count:]
    else:
        recent_files = self.recent_files
        append = recent_files.append
        abspath = os.path.abspath
        for file in files:
            if os.path.isfile(file) and file not in recent_files:
                append(abspath(file))
            if len(recent_files) == recent_files_count:
                break

    # start system tray icon
    if config.cfg.grouptray:
        logging.info('Creating system tray icon...')
        self.app.setQuitOnLastWindowClosed(False)   # ensure qt does not exit until we tell it to
        self.tray_icon = get_tray_icon(self)

    # enable taskbar extensions if desired
    if constants.IS_WINDOWS:
        self.taskbar.setWindow(self.windowHandle())
        self.enable_taskbar_controls(checked=config.cfg.checktaskbarcontrols)

    # manually refresh various settings after config is fully loaded
    settings = self.dialog_settings
    self.set_trim_mode(self.trim_mode_action_group.checkedAction())
    self.gifPlayer._imageScale = settings.comboScaleImages.currentIndex()
    self.gifPlayer._artScale = settings.comboScaleArt.currentIndex()
    self.gifPlayer._gifScale = settings.comboScaleGifs.currentIndex() + 1
    self.vlc.set_text_height(settings.spinTextHeight.value())
    self.vlc.set_text_x(settings.spinTextX.value())
    self.vlc.set_text_y(settings.spinTextY.value())

    # setup/connect hotkeys, manually refresh various parts of UI
    connect_shortcuts(self)
    self.refresh_shortcuts()
    self.refresh_volume_tooltip()
    self.refresh_autoplay_button()
    self.refresh_snapshot_button_controls()
    self.refresh_confusing_zoom_setting_tooltip(settings.spinZoomMinimumFactor.value())

    # start command interface thread
    Thread(target=self.external_command_interface_thread, daemon=True).start()


def connect_shortcuts(self: QtW.QMainWindow):
    # TODO add standardShortcuts | TODO are these noticably slower than using keyPressEvent or am I crazy?
    def increment_subtitle_delay(value: int = 50):
        if (self.player.video_get_spu_count() - 1) <= 0: return self.marquee('No subtitles available', marq_key='SubtitleDelay', log=False)
        new_delay = self.player.video_get_spu_delay() + (value * 1000)
        self.player.video_set_spu_delay(new_delay)
        if new_delay == 0: self.marquee('Subtitle delay 0ms', marq_key='SubtitleDelay', log=False)
        else: self.marquee(f'Subtitle delay {new_delay/ 1000:.0f}ms ({"later" if new_delay > 0 else "sooner"})', marq_key='SubtitleDelay', log=False)

    def toggle_loop():
        self.marquee(f'Looping {"disabled" if self.actionLoop.isChecked() else "enabled"}', marq_key='Loop', log=False),
        self.actionLoop.trigger()

    settings = self.dialog_settings
    shortcut_actions = {      # NOTE: having empty rows in tabHotkeys's formLayout causes actions below empty rows to not work
        'pause':              self.pause,
        'stop':               self.stop,
        'plus1':              lambda: self.navigate(forward=True,  seconds_spinbox=settings.spinNavigation1),
        'minus1':             lambda: self.navigate(forward=False, seconds_spinbox=settings.spinNavigation1),
        'plus2':              lambda: self.navigate(forward=True,  seconds_spinbox=settings.spinNavigation2),
        'minus2':             lambda: self.navigate(forward=False, seconds_spinbox=settings.spinNavigation2),
        'plus3':              lambda: self.navigate(forward=True,  seconds_spinbox=settings.spinNavigation3),
        'minus3':             lambda: self.navigate(forward=False, seconds_spinbox=settings.spinNavigation3),
        'plus4':              lambda: self.navigate(forward=True,  seconds_spinbox=settings.spinNavigation4),
        'minus4':             lambda: self.navigate(forward=False, seconds_spinbox=settings.spinNavigation4),
        'plusframe':          self.spinFrame.stepUp,
        'minusframe':         self.spinFrame.stepDown,
        'plusspeed':          lambda: self.set_playback_speed(self.playback_speed + 0.05),
        'minusspeed':         lambda: self.set_playback_speed(self.playback_speed - 0.05),
        'plus5volume':        lambda: self.sliderVolume.setValue(self.sliderVolume.value() + 5),
        'minus5volume':       lambda: self.sliderVolume.setValue(self.sliderVolume.value() - 5),
        'plusvolumeboost':    lambda: self.set_volume_boost(0.5, increment=True),
        'minusvolumeboost':   lambda: self.set_volume_boost(-0.5, increment=True),
        'mute':               self.toggle_mute,
        'fullscreen':         self.actionFullscreen.trigger,
        'maximize':           self.toggle_maximized,
        'crop':               self.actionCrop.trigger,
        'loop':               toggle_loop,
        'nextmedia':          self.cycle_media,
        'nextmediamime':      lambda: self.cycle_media(valid_mime_types=(self.mime_type,)),
        'previousmedia':      lambda: self.cycle_media(next=False),
        'previousmediamime':  lambda: self.cycle_media(next=False, valid_mime_types=(self.mime_type,)),
        'randommedia':        self.shuffle_media,
        'randommediamime':    lambda: self.shuffle_media(valid_mime_types=(self.mime_type,)),
        'forward':            lambda: self.cycle_recent_files(forward=True),
        'back':               lambda: self.cycle_recent_files(forward=False),
        'plussubtitledelay':  increment_subtitle_delay,
        'minussubtitledelay': lambda: increment_subtitle_delay(-50),
        'cyclesubtitles':     lambda: self.cycle_track('subtitle'),
        'cycleaudio':         lambda: self.cycle_track('audio'),
        'cyclevideo':         lambda: self.cycle_track('video'),
        'markdeleted':        self.actionMarkDeleted.trigger,
        'deleteimmediately':  self.delete,
        'snapshot':           lambda: self.snapshot(mode='full'),
        'quicksnapshot':      self.snapshot,
    }
    self.shortcuts = {action_name: (QtW.QShortcut(self, context=3), QtW.QShortcut(self, context=3)) for action_name in shortcut_actions}
    #self.shortcuts = {action_name: (Qtself.QKeySequence(), Qtself.QKeySequence()) for action_name in shortcut_actions}

    get_refresh_shortcuts_lambda = lambda widget: lambda: self.refresh_shortcuts(widget)    # lambda-in-iterable workaround
    for layout in qthelpers.formGetItemsInColumn(self.dialog_settings.formKeys, 1):
        for keySequenceEdit in qthelpers.layoutGetItems(layout):
            name = keySequenceEdit.objectName()
            index = 0 if name[-1] != '_' else 1
            name = name.rstrip('_')
            self.shortcuts[name][index].activated.connect(shortcut_actions[name])
            keySequenceEdit.editingFinished.connect(get_refresh_shortcuts_lambda(keySequenceEdit))


def connect_widget_signals(self: QtW.QMainWindow):
    self._open_cleanup_signal.connect(self._open_cleanup_slot)
    self._open_signal.connect(lambda kwargs: self.open(**kwargs))
    self._open_external_command_signal.connect(self._open_external_command_slot)
    self.restart_signal.connect(self.restart)
    self.force_pause_signal.connect(self.force_pause)
    self.show_ffmpeg_warning_signal.connect(constants._display_ffmpeg_warning)
    self.show_trim_dialog_signal.connect(self.show_trim_dialog)
    self.update_progress_signal.connect(self._update_progress_slot)
    self.refresh_title_signal.connect(self._refresh_title_slot)
    self.set_save_progress_visible_signal.connect(self.save_progress_bar.setVisible)
    self.set_save_progress_max_signal.connect(self.save_progress_bar.setMaximum)
    self.set_save_progress_current_signal.connect(self.save_progress_bar.setValue)
    self.set_save_progress_format_signal.connect(self.save_progress_bar.setFormat)
    self.disable_crop_mode_signal.connect(self.disable_crop_mode)
    self.handle_updates_signal.connect(self.handle_updates)
    self._handle_updates_signal.connect(self._handle_updates)
    self.log_on_statusbar_signal.connect(self._log_on_statusbar_slot)

    self.sliderVolume.valueChanged.connect(self.set_volume)
    self.buttonPause.clicked.connect(self.pause)
    self.actionOpen.triggered.connect(self.open)
    self.menuFile.aboutToShow.connect(self.refresh_copy_image_action)
    self.menuRecent.aboutToShow.connect(self.refresh_recent_menu)
    self.actionClearRecent.triggered.connect(lambda: self.recent_files.clear())    # TODO why won't .clear work on its own?
    self.actionExploreMediaPath.triggered.connect(self.explore)
    self.actionCopyMediaPath.triggered.connect(self.copy)
    self.actionCopyFile.triggered.connect(self.copy_file)
    self.actionCutFile.triggered.connect(lambda: self.copy_file(cut=True))
    self.actionCopyImage.triggered.connect(self.copy_image)
    self.actionSave.triggered.connect(self.save)
    self.actionSaveAs.triggered.connect(self.save_as)
    self.actionStop.triggered.connect(self.stop)
    self.actionMinimize.triggered.connect(self.close)
    self.actionExit.triggered.connect(lambda: exit(self))
    self.actionSettings.triggered.connect(self.dialog_settings.exec)
    self.actionLoop.triggered.connect(self.buttonLoop.setChecked)
    self.actionAutoplay.triggered.connect(self.refresh_autoplay_button)
    self.actionAutoplayShuffle.triggered.connect(self.refresh_autoplay_button)
    self.actionSnapshot.triggered.connect(lambda: self.snapshot(mode='full'))
    self.actionQuickSnapshot.triggered.connect(self.snapshot)
    self.actionSnapshotOpenLast.triggered.connect(lambda: self.snapshot(mode='open'))
    self.actionSnapshotOpenLastInDefault.triggered.connect(lambda: self.snapshot(mode='view'))
    self.actionSnapshotExploreLastPath.triggered.connect(lambda: self.explore(config.cfg.last_snapshot_path, 'Last snapshot'))
    self.actionSnapshotCopyLastPath.triggered.connect(lambda: self.copy(config.cfg.last_snapshot_path, 'Last snapshot'))
    self.actionSnapshotCopyLastFile.triggered.connect(lambda: self.copy_file(config.cfg.last_snapshot_path))
    self.actionSnapshotCutLastFile.triggered.connect(lambda: self.copy_file(config.cfg.last_snapshot_path, cut=True))
    self.actionSnapshotCopyLastImage.triggered.connect(lambda: self.copy_image(config.cfg.last_snapshot_path))
    self.actionSnapshotUndo.triggered.connect(lambda: self.snapshot(mode='undo'))
    self.actionMarkDeleted.triggered.connect(self.buttonMarkDeleted.setChecked)
    self.actionMarkDeleted.triggered.connect(self.mark_for_deletion)
    self.actionClearMarked.triggered.connect(self.clear_marked_for_deletion)
    self.actionShowDeletePrompt.triggered.connect(self.show_delete_prompt)
    self.actionDeleteImmediately.triggered.connect(self.delete)
    self.actionEditFileTimestamps.triggered.connect(self.show_timestamp_dialog)
    self.menuConcatenate.triggered.connect(self.concatenate)
    self.menuVideoTracks.aboutToShow.connect(lambda: self.refresh_track_menu(self.menuVideoTracks))
    self.menuSubtitles.aboutToShow.connect(lambda: self.refresh_track_menu(self.menuSubtitles))
    self.actionAddSubtitleFile.triggered.connect(self.browse_for_subtitle_files)
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
    self.actionViewLastDirectory.triggered.connect(lambda: qthelpers.openPath(config.cfg.lastdir))
    self.actionViewInstallFolder.triggered.connect(lambda: qthelpers.openPath(constants.CWD))
    self.actionViewProbeFile.triggered.connect(self.open_probe_file)
    self.actionDeleteProbeFile.triggered.connect(lambda: self.open_probe_file(delete=True))
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
    self.buttonNext.clicked.connect(self.handle_cycle_buttons)
    self.buttonPrevious.clicked.connect(lambda: self.handle_cycle_buttons(next=False))
    self.buttonExploreMediaPath.clicked.connect(self.actionExploreMediaPath.trigger)
    self.buttonMarkDeleted.clicked.connect(self.actionMarkDeleted.trigger)
    self.buttonSnapshot.clicked.connect(self.handle_snapshot_button)
    self.buttonLoop.clicked.connect(self.actionLoop.trigger)
    self.buttonAutoplay.clicked.connect(self.actionAutoplay.trigger)

    self.trim_mode_action_group = QtW.QActionGroup(self.menuTrimMode)
    self.trim_mode_action_group.addAction(self.actionTrimAuto)
    self.trim_mode_action_group.addAction(self.actionTrimPrecise)
    self.trim_mode_action_group.addAction(self.actionFadeBoth)
    self.trim_mode_action_group.addAction(self.actionFadeVideo)
    self.trim_mode_action_group.addAction(self.actionFadeAudio)
    self.trim_mode_action_group.triggered.connect(self.set_trim_mode)

    self.autoplay_direction_group = QtW.QActionGroup(self)
    self.autoplay_direction_group.addAction(self.actionAutoplayDirectionForwards)
    self.autoplay_direction_group.addAction(self.actionAutoplayDirectionBackwards)
    self.autoplay_direction_group.addAction(self.actionAutoplayDirectionDynamic)
    self.autoplay_direction_group.triggered.connect(self.refresh_autoplay_button)

    settings = self.dialog_settings
    settings.accepted.connect(self._refresh_title_slot)
    settings.comboThemes.currentTextChanged.connect(self.set_theme)
    settings.buttonRefreshThemes.clicked.connect(self.refresh_theme_combo)
    settings.buttonBrowseDefaultOutputPath.clicked.connect(lambda: self.browse_for_directory(settings.lineDefaultOutputPath, 'default output'))
    settings.buttonBrowseDefaultSnapshotPath.clicked.connect(lambda: self.browse_for_directory(settings.lineDefaultSnapshotPath, 'default snapshot'))
    settings.buttonHoverFontColor.clicked.connect(self.show_color_picker)
    settings.checkHighPrecisionProgress.toggled.connect(self.swap_slider_styles)
    settings.checkScaleFiltering.toggled.connect(self.gifPlayer.update)
    settings.buttonCheckForUpdates.clicked.connect(self.handle_updates)
    settings.checkZoomPrecise.toggled.connect(self.gifPlayer._updatePreciseZoom)
    settings.spinZoomMinimumFactor.valueChanged.connect(lambda: settings.checkZoomAutoDisable1x.setEnabled(settings.spinZoomMinimumFactor.value() == 1))
    settings.spinZoomSmoothFactor.valueChanged.connect(self.gifPlayer._updateSmoothZoomFactor)
    settings.comboSnapshotDefault.currentIndexChanged.connect(self.refresh_snapshot_button_controls)
    settings.comboSnapshotShift.currentIndexChanged.connect(self.refresh_snapshot_button_controls)
    settings.comboSnapshotCtrl.currentIndexChanged.connect(self.refresh_snapshot_button_controls)
    settings.comboSnapshotAlt.currentIndexChanged.connect(self.refresh_snapshot_button_controls)
    settings.checkTaskbarControls.toggled.connect(self.enable_taskbar_controls)
    settings.spinZoomMinimumFactor.valueChanged.connect(self.refresh_confusing_zoom_setting_tooltip)

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

    def refresh_navigation_labels():
        for label, spinbox in (
            (settings.labelNavigation1, settings.spinNavigation1),
            (settings.labelNavigation2, settings.spinNavigation2),
            (settings.labelNavigation3, settings.spinNavigation3),
            (settings.labelNavigation4, settings.spinNavigation4),
        ):
            seconds = spinbox.value()
            suffix = ' second' if seconds == 1 else ' seconds'
            label.setText(f'-{seconds}{suffix}')
            spinbox.setSuffix(suffix)

    settings.spinNavigation1.valueChanged.connect(refresh_navigation_labels)
    settings.spinNavigation2.valueChanged.connect(refresh_navigation_labels)
    settings.spinNavigation3.valueChanged.connect(refresh_navigation_labels)
    settings.spinNavigation4.valueChanged.connect(refresh_navigation_labels)

    # NOTE: this looks weird if the gif has custom frame-by-frame delays, but it's perfectly fine
    self.gifPlayer.gif.frameChanged.connect(self.update_gif_progress)
