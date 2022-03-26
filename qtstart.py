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
import logging
import argparse
import subprocess
from threading import Thread
from traceback import format_exc


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


# ---------------------
# Arguments
# ---------------------
parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='?', help='Specifies a filepath to open')     # '?' allows for optional positionals
parser.add_argument('--play-and-exit', action='store_true', help='Automatically exits at the conclusion of a media file')
args = parser.parse_args()
logging.info(f'Arguments: {args}')


# ---------------------
# System Tray Icon
# ---------------------
def exit(self: QtW.QMainWindow):
    logging.info('Exiting.')
    if self.dialog_settings.groupTray.isChecked() and not self.isHidden():
        self.close()
        if self.close_cancel_selected: return   # in case we show a file-deletion dialog and the user clicks cancel/X

    self.tray_icon.setVisible(False)
    logging.info('System tray icon stopped.')
    self.closed = True
    logging.info('self.closed set to True.')
    self.app.quit()
    logging.info('QApplication quit.')

    try: config.saveConfig(self, constants.CONFIG_PATH)
    except: logging.warning(f'Error saving configuration: {format_exc()}')
    logging.info('Configuration has been saved. Goodbye.')


def show(self):
    ''' Restores main window from tray icon. Main code is handled in GUI_Instance.showEvent, as manual show() calls are reported in
        showEvent.spontaneous() as False, making them easy to detect. If showNormal/showMaximized is placed here, it refuses to maximize
        for some reason. If called while window is already visible, focus is given to the window, unless it's maximized (see below). '''
    logging.info(f'Showing manually, either from system tray or from launcher:\nwinId={int(self.winId())} isVisible={self.isVisible()} isMaximized={self.isMaximized()}')
    if self.isVisible() and not self.isMaximized():     # this resets the maximized state?? -> just ignore maximized state for now
        return qthelpers.show_window(self.winId(), focus=True)
    self.show()
    #if not self.isVisible():
    #    if self.was_maximized: self.showMaximized()
    #    else: self.showNormal()
    #qthelpers.show_window(self.winId(), focus=True)


def get_tray_icon(self: QtW.QMainWindow) -> QtW.QSystemTrayIcon:
    ''' Generates the system tray icon. For a while I was using pystray because I genuinely forgot QSystemTrayIcon existed.
        QSystemTrayIcon has some issues, one being the fact that if placed in the "hidden icons" area on Windows, that area will
        close while the tray icon's context menu is open. That's not much of an issue with this very barebones tray icon, but it
        may become an issue if the tray icon is expanded upon. Pystray is still a decent (albeit heavy) fallback if necessary. '''

    def show_settings():
        ''' Displays the settings dialog. exec() and show_window don't play well together, so we call show_window first (which causes a blank
            window to appear briefly) or the dialog will simply ignore the focus and end up in a glitched state until manually interacted with. '''
        qthelpers.show_window(self.dialog_settings.winId(), focus=True)
        self.dialog_settings.exec()

    def handle_click(reason: QtW.QSystemTrayIcon.ActivationReason):
        if reason == QtW.QSystemTrayIcon.Context:
            action_show = QtW.QAction('Show PyPlayer')
            action_show.triggered.connect(lambda: show(self))
            action_settings = QtW.QAction('Settings')
            action_settings.triggered.connect(show_settings)
            action_exit = QtW.QAction('Exit')
            action_exit.triggered.connect(lambda: exit(self))
            menu = QtW.QMenu()
            menu.addAction(action_show)
            menu.addAction(action_settings)
            menu.addSeparator()
            menu.addAction(action_exit)
            return menu.exec(QtGui.QCursor.pos())
        if reason == QtW.QSystemTrayIcon.Trigger: return show(self)
        if reason == QtW.QSystemTrayIcon.MiddleClick: return exit(self)

    tray = QtW.QSystemTrayIcon(self.icon)
    tray.setToolTip('PyPlayer')
    tray.setVisible(True)
    tray.activated.connect(handle_click)
    return tray


# ---------------------
# GUI Setup
# ---------------------
def after_show_setup(self: QtW.QMainWindow):
    if args.file:                           # TODO should this stay in __init__ or here?
        if not os.path.exists(args.file): self.log(f'Command-line file {args.file} does not exist.')
        elif os.path.isdir(args.file):      # args.file is actually just a folder
            for filename in os.listdir(args.file):
                file = os.path.join(args.file, filename)
                if not os.stat(file).st_file_attributes & 2 and self.open(file) != -1:  # 2 -> stat.FILE_ATTRIBUTE_HIDDEN. do not use hidden files as the first file
                    self.checkAutoplay.setChecked(True)                                 # https://stackoverflow.com/questions/284115/cross-platform-hidden-file-detection
                    self.log(f'Opened {file} from folder {args.file} and enabled Autoplay.')
                    break
            else: self.log(f'No files in {args.file} were playable.')
        else:                               # args.file is (presumably) a media file
            try:
                logging.info(f'Opening pre-selected video: {args.file}')
                self.open(args.file)
                self.log(f'Command-line file opened: {args.file}')
            except:
                self.log(f'Failed to open pre-selected video: {args.file}')
                logging.error(format_exc())
    Thread(target=self.fast_start_interface_thread, daemon=True).start()
    self.update_title_signal.emit()
    #self.icon = Qtself.QIcon(os.path.join(CWD, 'bin', 'icon.ico'))   # loading QIcons is a very resource-intensive task
    #app.setWindowIcon(self.icon)
    connect_shortcuts(self)


def connect_shortcuts(self: QtW.QMainWindow):
    # TODO add standardShortcuts | TODO are these noticably slower than using keyPressEvent or am I crazy?
    def increment_volume_boost(value=0.5):
        self.volume_boost = min(self.volume_boost + value, 5)
        self.set_volume(self.get_volume_slider())
        self.log_on_screen(f'{self.volume_boost:.1f}x volume multiplier', marq_key='VolumeBoost', log=False)

    def increment_subtitle_delay(value=50):
        if (self.player.video_get_spu_count() - 1) <= 0: return self.log_on_screen('No subtitles available', marq_key='SubtitleDelay', log=False)
        new_delay = self.player.video_get_spu_delay() + (value * 1000)
        self.player.video_set_spu_delay(new_delay)
        if new_delay == 0: self.log_on_screen('Subtitle delay 0ms', marq_key='SubtitleDelay', log=False)
        else: self.log_on_screen(f'Subtitle delay {new_delay/ 1000:.0f}ms ({"later" if new_delay > 0 else "sooner"})', marq_key='SubtitleDelay', log=False)

    def toggle_loop():
        self.log_on_screen(f'Looping {"disabled" if self.actionLoop.isChecked() else "enabled"}', marq_key='Loop', log=False),
        self.actionLoop.activate(qthelpers.TRIGGER)

    shortcut_actions = {      # NOTE: having empty rows in tabKeys's formLayout (in QtDesigner) causes actions below empty rows to not work
        'pause':              self.pause,
        'plus5seconds':       self.navigate,
        'minus5seconds':      lambda: self.navigate(forward=False, seconds=5),
        'plus10seconds':      lambda: self.navigate(forward=True, seconds=10),
        'minus10seconds':     lambda: self.navigate(forward=False, seconds=10),
        'plusframe':          self.frame_spin.stepUp,
        'minusframe':         self.frame_spin.stepDown,
        'plusspeed':          lambda: self.set_playback_speed(self.playback_speed + 0.05),
        'minusspeed':         lambda: self.set_playback_speed(self.playback_speed - 0.05),
        'plus5volume':        lambda: self.increment_volume(5),
        'minus5volume':       lambda: self.increment_volume(-5),
        'plusvolumeboost':    increment_volume_boost,
        'minusvolumeboost':   lambda: increment_volume_boost(-0.5),
        'mute':               self.toggle_mute,
        'fullscreen':         lambda: self.actionFullscreen.activate(qthelpers.TRIGGER),
        'crop':               lambda: self.actionCrop.activate(qthelpers.TRIGGER),
        'loop':               toggle_loop,
        'nextmedia':          self.cycle_media,
        'previousmedia':      lambda: self.cycle_media(next=False),
        'plussubtitledelay':  increment_subtitle_delay,
        'minussubtitledelay': lambda: increment_subtitle_delay(-50),
        'cyclesubtitles':     self.cycle_subtitle_track,
        'markdeleted':        lambda: self.actionMarkDeleted.activate(qthelpers.TRIGGER),
        'deleteimmediately':  lambda: self.mark_for_deletion(modifiers=Qt.ControlModifier),
        'snapshot':           lambda: self.snapshot(modifiers=Qt.ControlModifier),
        'quicksnapshot':      self.snapshot,
    }
    self.shortcuts = {action_name: (QtW.QShortcut(self, context=3), QtW.QShortcut(self, context=3)) for action_name in shortcut_actions}
    #self.shortcuts = {action_name: (Qtself.QKeySequence(), Qtself.QKeySequence()) for action_name in shortcut_actions}

    for widget in qthelpers.formGetItemsInColumn(self.dialog_settings.tabKeys.layout(), 1):
        for keySequenceEdit in qthelpers.layoutGetItems(widget):
            name = keySequenceEdit.objectName()
            index = 0 if name[-1] != '_' else 1
            name = name.rstrip('_')
            self.shortcuts[name][index].activated.connect(shortcut_actions[name])
    get_refresh_shortcuts_lambda = lambda widget: lambda: self.refresh_shortcuts(widget)
    for layout in qthelpers.formGetItemsInColumn(self.dialog_settings.tabKeys.layout(), 1):
        for child in qthelpers.layoutGetItems(layout):
            child.editingFinished.connect(get_refresh_shortcuts_lambda(child))  # workaround for python bug/oddity involving creating lambdas in iterables
    self.refresh_shortcuts()


def connect_widget_signals(self: QtW.QMainWindow):
    self._open_signal.connect(self._open)
    self.open_signal.connect(self.open)
    self.fast_start_open_signal.connect(self.fast_start_open)
    self.restart_signal.connect(self.restart)
    self.update_progress_signal.connect(self.update_progress_slot)
    self.update_title_signal.connect(self.update_title)
    self.show_save_progress_signal.connect(self.save_progress_bar.setVisible)
    self.disable_crop_mode_signal.connect(self.disable_crop_mode)
    self._handle_updates_signal.connect(self._handle_updates)
    self.log_signal.connect(self.log_slot)
    self.log = self.log_signal.emit

    self.volume_slider.valueChanged.connect(self.set_volume)
    self.pause_button.clicked.connect(self.pause)
    self.actionOpen.triggered.connect(self.open)
    self.menuRecent.aboutToShow.connect(self.refresh_recent_menu)
    self.actionOpenMediaLocation.triggered.connect(lambda: subprocess.Popen(f'explorer /select,"{os.path.abspath(self.video if self.video else config.cfg.lastdir)}"', shell=True))
    self.actionSave.triggered.connect(self.save)
    self.actionSaveAs.triggered.connect(self.save_as)
    self.actionStop.triggered.connect(self.stop)
    self.actionMinimize.triggered.connect(self.close)
    self.actionExit.triggered.connect(lambda: exit(self))
    self.actionSettings.triggered.connect(self.dialog_settings.exec)
    self.actionLoop.triggered.connect(lambda: self.toolButtonLoop.setText('↺'))
    self.actionMarkDeleted.triggered.connect(self.mark_for_deletion)
    self.actionDeleteImmediately.triggered.connect(lambda: self.mark_for_deletion(modifiers=Qt.ControlModifier))
    self.actionEmptyRecycleBin.triggered.connect(self.show_delete_prompt)
    self.menuConcatenate.triggered.connect(self.concatenate)
    self.menuVideoTracks.aboutToShow.connect(lambda: self.refresh_track_menu(self.menuVideoTracks))
    self.menuSubtitles.aboutToShow.connect(lambda: self.refresh_track_menu(self.menuSubtitles))
    self.actionAddSubtitleFile.triggered.connect(self.browse_subtitle_file)
    self.actionSnapshot.triggered.connect(lambda: self.snapshot(modifiers=Qt.ControlModifier))
    self.actionQuickSnapshot.triggered.connect(self.snapshot)
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
    self.actionShowAdvancedControls.triggered.connect(self.frameAdvancedControls.setVisible)
    self.actionFullscreen.triggered.connect(self.set_fullscreen)
    self.actionCheckForUpdates.triggered.connect(self.handle_updates)
    self.actionViewLog.triggered.connect(lambda: os.startfile(constants.LOG_PATH))
    self.actionViewInstallFolder.triggered.connect(lambda: os.startfile(constants.CWD))
    self.actionAboutQt.triggered.connect(lambda: QtW.QMessageBox.aboutQt(None, 'About Qt'))
    self.actionAbout.triggered.connect(self.show_about_dialog)
    #self.check_clamp.stateChanged.connect(self.clamp)
    self.output_lineedit.returnPressed.connect(self.save)
    self.current_time_lineedit.returnPressed.connect(self.manually_update_current_time)
    self.hour_spin.valueChanged.connect(self.update_time_spins)
    self.minute_spin.valueChanged.connect(self.update_time_spins)
    self.second_spin.valueChanged.connect(self.update_time_spins)
    self.frame_spin.valueChanged.connect(self.update_frame_spin)
    self.progress_slider.actionTriggered.connect(self.page_step_slider)
    self.trim_start_button.toggled.connect(self.set_trim_start)
    self.trim_end_button.toggled.connect(self.set_trim_end)
    self.next_video_button.clicked.connect(self.cycle_media)
    self.prev_video_button.clicked.connect(lambda: self.cycle_media(next=False))

    settings = self.dialog_settings
    settings.accepted.connect(self.update_title)
    settings.theme_combo.currentTextChanged.connect(self.set_theme)
    settings.theme_refresh_button.clicked.connect(self.refresh_theme_combo)
    settings.default_path_browse.clicked.connect(self.browse_default_path_output)
    settings.default_snapshot_path_browse.clicked.connect(self.browse_default_snapshot_path_output)
    settings.buttonHoverFontColor.clicked.connect(self.open_color_picker)
    settings.checkHighPrecisionProgress.toggled.connect(self.swap_slider_styles)
    settings.buttonCheckForUpdates.clicked.connect(self.handle_updates)

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
