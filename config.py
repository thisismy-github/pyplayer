from PyQt5 import QtGui
from PyQt5 import QtWidgets as QtW
from bin.configparsebetter import ConfigParseBetterQt
import qthelpers

import os
import time
import logging


logger = logging.getLogger('config.py')
cfg = ConfigParseBetterQt(autoread=False, autosave=True, autosaveCallback=False)


def loadConfig(gui, filename: str = None) -> ConfigParseBetterQt:
    start = time.time()
    load = cfg.load
    settings = gui.dialog_settings
    screen = gui.app.primaryScreen().size()

    if filename: cfg.setFilepath(filename)
    cfg.read(filename)

    cfg.setSection('window')
    gui.resize(*load('size', '871,600', ',', int, tuple))
    gui.move(*load('pos', f'{screen.width() / 2 - (gui.width() / 2):.0f},{screen.height() / 2 - (gui.height() / 2):.0f}', ',', int, tuple))
    if load('fullscreen', False):  # load fullscreen and last maximized state
        gui.actionFullscreen.activate(qthelpers.TRIGGER)
        gui.was_maximized = load('maximized', False)
    elif load('maximized', False): gui.showMaximized()
    gui.app.setStyle(str(load('windowstyle', 'WindowsVista')))
    load('lastupdatecheck')
    load('theme', 'Midnight')

    cfg.setSection('general')
    load('lastdir', '.')
    load('last_snapshot_path')
    load('last_snapshot_folder', '%USERPROFILE%\\Pictures')
    cfg.loadQt(gui.volume_slider, children=False)
    gui.checkDeleteOriginal.setCheckState(load('checkDeleteOriginal', 1))
    cfg.loadQt(gui.frameQuickChecks)
    load('ffmpegwarningignored', False)
    load('minimizedtotraywarningignored', False)
    gui.recent_videos = [file for file in load('recent_videos', '', ',') if os.path.exists(file)][-10:]

    cfg.setSection('settings')
    cfg.loadQt(settings.tabGeneral, ignore=('theme_combo',))
    hoverfontcolor = load('hoverfontcolor', '255,255,255', ',', int, tuple, fill_with_defaults=True, default=255)
    gui.progress_slider.hover_font_color = QtGui.QColor(*hoverfontcolor)
    settings.buttonHoverFontColor.setToolTip(str(hoverfontcolor))
    settings.buttonHoverFontColor.setStyleSheet('QPushButton {background-color: rgb' + str(hoverfontcolor) + ';border: 1px solid black;}')
    del hoverfontcolor

    cfg.setSection('keys')
    for widget in qthelpers.formGetItemsInColumn(gui.dialog_settings.tabKeys.layout(), 1):
        items = tuple(qthelpers.layoutGetItems(widget))
        name = items[0].objectName().rstrip('_')

        # <|> as delimiter to avoid accdientally reading sequences as delimiters and vice-versa
        default_keys = '<|>'.join(item.keySequence().toString() for item in items)
        keys = load(name, default_keys, '<|>', QtGui.QKeySequence, tuple, fill_with_fallback=True)
        items[0].setKeySequence(keys[0])
        items[1].setKeySequence(keys[1])

    # https://doc.qt.io/archives/qtjambi-4.5.2_01/com/trolltech/qt/gui/QAction.ActionEvent.html
    cfg.setSection('visible')   # simulate trigger-events on these menu items if we want to hide their associated widgets
    if not load('menubar', True): gui.actionShowMenuBar.activate(QtW.QAction.ActionEvent.Trigger)
    if not load('statusbar', True): gui.actionShowStatusBar.activate(QtW.QAction.ActionEvent.Trigger)
    if not load('progressbar', True): gui.actionShowProgressBar.activate(QtW.QAction.ActionEvent.Trigger)
    if not load('advancedcontrols', True): gui.actionShowAdvancedControls.activate(QtW.QAction.ActionEvent.Trigger)

    cfg.setSection('concatenate')
    load('open', True)
    load('explore', False)

    logger.info(f'It took {time.time() - start:.4f} seconds to load this config.\n')
    return cfg


def saveConfig(gui, filename: str = None):
    start = time.time()
    save = cfg.save

    cfg.setSection('window')
    save('fullscreen', gui.isFullScreen())  # FullScreen with a capital S
    save('maximized', gui.isMaximized() or (gui.isFullScreen() and gui.was_maximized))
    if not gui.isMaximized():               # preserve unmaximized size/position
        save('size', gui.size().width(), gui.size().height())
        save('pos', gui.pos().x(), gui.pos().y())
    else:
        save('size', gui.last_window_size.width(), gui.last_window_size.height())
        save('pos', gui.last_window_pos.x(), gui.last_window_pos.y())
    save('windowstyle', gui.app.style().objectName())

    cfg.setSection('general')
    save('recent_videos', gui.recent_videos, delimiter=',')

    cfg.setSection('settings')
    save('hoverfontcolor', gui.progress_slider.hover_font_color.getRgb(), delimiter=',')

    cfg.setSection('keys')
    for widget in qthelpers.formGetItemsInColumn(gui.dialog_settings.tabKeys.layout(), 1):
        items = tuple(qthelpers.layoutGetItems(widget))
        save(items[0].objectName().rstrip('_'), *(item.keySequence().toString() for item in items), delimiter='<|>')

    cfg.setSection('visible')
    save('menubar', gui.actionShowMenuBar.isChecked())
    save('statusbar', gui.actionShowStatusBar.isChecked())
    save('progressbar', gui.actionShowProgressBar.isChecked())
    save('advancedcontrols', gui.actionShowAdvancedControls.isChecked())

    cfg.write(filename)
    logger.info(f'It took {time.time() - start:.4f} seconds to save this config.')
