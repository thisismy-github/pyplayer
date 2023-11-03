''' An ever-growing list of helpful utility functions for Qt
    I've made over time to fulfill general or niche purposes.
    Uses camelCase like Qt so you can act like none of this
    ever had to be implemented manually in the first place.

    thisismy-github '''

from __future__ import annotations

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets as QtW
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
import os
import logging
import platform
import subprocess

# logger
logger = logging.getLogger('qthelpers.py')


# ----------------------
# Misc
# ----------------------
def openPath(path: str, explore: bool = False, fallback_to_parent: bool = None) -> None:
    ''' Attempts to open `path` with an appropriate application. If `explore`
        is True, `path`'s parent directory is opened in a file explorer with
        `path` pre-selected (if possible). If `fallback_to_parent` is True and
        `path` doesn't exist, its parent directory is opened directly. If False,
        -1 is returned. If None, `explore`'s value is used for `fallback`. '''
    if path:
        path = os.path.abspath(path)
    if fallback_to_parent is None:
        fallback_to_parent = explore        # if `fallback` is not specified, use `explore`
    try:
        if not path or not os.path.exists(path):
            if fallback_to_parent:          # ignore `explore` if path doesn't exist (open directory instead)
                path = os.path.dirname(path)
                if not os.path.exists(path):
                    return -1
            else:
                return -1
        elif explore:                       # open in explorer with file/directory pre-selected
            system = platform.system()      # FIXME: couldn't find a way to pre-select files in Linux
            if system == 'Windows':  return subprocess.Popen(f'explorer /select, "{path}"')
            elif system == 'Darwin': return subprocess.Popen(['open', '-R', path])
    except:                                 # error or system wasn't detected (Linux)...
        pass                                # ... -> allow Qt to open the path normally
    QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(path))


def deleteTempPath(path: str, noun: str = 'file', retry_delay: float = 0.5, retry_attempts: int = 2) -> bool:
    ''' Repeatedly tries to delete `path` once every `retry_delay` seconds,
        `retry_attempts` times (if provided) using `QTimer.singleShot()`. Logs
        it as a "temporary `noun`". Returns True if successful, otherwise False
        if the first attempt fails and multiple attempts are needed. '''
    try:
        logger.info(f'Deleting temporary {noun}: {path}')
        os.remove(path)
        return True
    except FileNotFoundError:               # `path` doesn't exist anymore
        return True
    except:
        if retry_attempts > 0 and retry_delay > 0:
            sec = '1 second' if retry_delay == 1.0 else f'{retry_delay} seconds'
            att = '1 attempt' if retry_attempts == 1 else f'{retry_attempts} attempts'
            logger.warning(f'(?) Failed to delete temporary {noun}, retrying in {sec} ({att} remaining)...')
            QtCore.QTimer.singleShot(
                retry_delay * 1000,
                Qt.CoarseTimer,
                lambda: deleteTempPath(path, noun, retry_delay, retry_attempts - 1)
            )
        else:
            logger.warning(f'(!) Failed to delete temporary {noun}. Giving up.')
        return False


def clampToScreen(
    window: QtW.QWidget,
    screen: QtGui.QScreen = None,
    resize: bool = True,
    move: bool = True,
    mouseFallback: bool = True,
    returnScreen: bool = False,
    strict: bool = False
) -> QtCore.QRect | QtGui.QScreen:
    ''' Clamps `window` to the boundaries of `screen`. If `screen` is None,
        the `window`'s current screen will be approximated if possible. If not
        possible and `mouseFallback` is True, the mouse's screen will be used.
        If still not possible or `mouseFallback` is False, the primary screen
        will be used. If `move` is True and `window` is a QWidget, it will be
        automatically moved to its new position. If `resize` is True,
        `window`'s size will be clamped to the final screen's size. If
        `returnScreen` is True, the final screen is returned, otherwise
        `window`'s final QRect is returned. If `strict` is True, clamping
        occurs even if `window` is maximized or in fullscreen mode. '''

    if not strict and (window.isMaximized() or window.isFullScreen()): return
    isRect = isinstance(window, QtCore.QRect)
    windowRect = window if isRect else window.frameGeometry()
    if screen is None:
        screen = getScreenForRect(windowRect, mouseFallback=mouseFallback)

    screenRect = screen.availableGeometry()                 # availableGeometry excludes the taskbar
    if not screenRect.contains(windowRect):                 # .contains for entire rect, .intersects for partial rect
        if resize and not isRect:
            screenSize = screenRect.size()
            windowSize = windowRect.size()                  # only resize if necessary
            if windowSize.height() > screenSize.height() or windowSize.width() > screenSize.width():
                window.resize(windowRect.size().boundedTo(screenRect.size()))
                windowRect = window.frameGeometry()
        offsetTopLeft = windowRect.topLeft() - screenRect.topLeft()
        windowRect.translate(-min(0, offsetTopLeft.x()), -min(0, offsetTopLeft.y()))
        offsetBottomRight = windowRect.bottomRight() - screenRect.bottomRight()
        windowRect.translate(-max(0, offsetBottomRight.x()), -max(0, offsetBottomRight.y()))
        if move and not isRect:
            window.move(windowRect.topLeft())               # .setGeometry() is sometimes wrong
    return screen if returnScreen else windowRect


def getScreenForRect(
    rect: QtCore.QRect,
    defaultPos: QtCore.QPoint = None,
    mouseFallback: bool = False,
    strict: bool = False
) -> QtGui.QScreen:
    ''' WARNING: For window rects, pass in `.geometry()`, NOT `.rect()`.
        Returns the `QScreen` that `rect` is touching, if any. Tests the center
        of `rect` first unless `defaultPos` is given, then tests its corners.
        If `rect` is not touching any screen and `strict` is True, ValueError
        is raised. Otherwise if `mouseFallback` is True, the screen the mouse
        is on (if any) is returned. Otherwise, or if neither are True, the
        primary screen is returned. '''

    if defaultPos is None: pos = rect.center()
    else: pos = defaultPos
    qscreen = QtW.QApplication.screenAt(pos)

    if not qscreen:         # check if rect's center/corners are on a screen (unless defaultPos was None)
        if defaultPos is None: points = (rect.topLeft, rect.topRight, rect.bottomLeft, rect.bottomRight)
        else: points = (rect.center, rect.topLeft, rect.topRight, rect.bottomLeft, rect.bottomRight)
        for point in points:
            qscreen = QtW.QApplication.screenAt(point())
            if qscreen:
                break
        if not qscreen:     # no screen detected -> use mouse. if already used -> use primary screen
            if strict:        raise ValueError(f'Rect {rect} is not on any screen.')
            if mouseFallback: qscreen = QtW.QApplication.screenAt(QtGui.QCursor().pos())
            if not qscreen:   qscreen = QtW.QApplication.primaryScreen()
    return qscreen


def center(
    widget: QtW.QWidget,
    target=None,
    screen: bool = False,
    mouse: bool = False,
    strict: bool = False
) -> None:
    ''' Centers `widget` over `target`, which may be a widget, QRect, QPoint,
        or an (x, y) tuple. If only `screen` is True, `widget` is centered
        over `target`'s screen, or `widget`'s own screen if `target` is None.
        If only `mouse` is True, `widget` is centered over the mouse. If both
        are True, `widget` is centered over the mouse's screen. `widget` is
        clamped to its new screen if possible. `strict` controls whether or
        not to raise errors when `target` is believed to be invalid. '''

    pos = target
    targetRect = None
    if isinstance(target, QtW.QWidget):
        targetRect = target.geometry()
        pos = target.mapToGlobal(targetRect.center())
    elif isinstance(target, QtCore.QRect):
        targetRect = target
        pos = target.center()
    elif target is not None:
        try: pos = QtCore.QPoint(*target)
        except: raise TypeError('`target` must be a widget, QRect, QPoint, '
                                f'or an (x, y) tuple, not {type(target)}.')
    elif not mouse:                                         # only `widget` is set, center on its own screen
        screen = True

    if targetRect is None:
        targetRect = widget.geometry()

    if screen:
        if mouse:        pos = QtGui.QCursor().pos()
        elif not target: pos = widget.mapToGlobal(widget.rect().center())
        pos = getScreenForRect(targetRect, pos, mouse, strict).availableGeometry().center()
    elif mouse:
        pos = QtGui.QCursor().pos()

    # move widget first, then clamp to screen if possible
    widget.move(pos - widget.rect().center())               # move immediately and correct later
    if not screen:                                          # clamp is pointless if `screen` was set
        widgetRect = widget.frameGeometry()
        targetScreen = getScreenForRect(widgetRect, pos, mouse, strict)
        if targetScreen:
            screenRect = targetScreen.availableGeometry()   # availableGeometry excludes the taskbar
            if not screenRect.contains(widgetRect):
                offsetTopLeft = widgetRect.topLeft() - screenRect.topLeft()
                widgetRect.translate(-min(0, offsetTopLeft.x()), -min(0, offsetTopLeft.y()))
                offsetBottomRight = widgetRect.bottomRight() - screenRect.bottomRight()
                widgetRect.translate(-max(0, offsetBottomRight.x()), -max(0, offsetBottomRight.y()))
                widget.move(widgetRect.topLeft())           # .setGeometry() is sometimes wrong


def setCursor(cursor: QtGui.QCursor | QtCore.Qt.CursorShape = QtCore.Qt.ArrowCursor) -> None:
    ''' Clears the cursor-stack and sets the top-level cursor to `cursor`,
        which can be a `QCursor` object or a `Qt.CursorShape` enum. '''
    app = QtW.qApp
    while app.overrideCursor():
        app.restoreOverrideCursor()
    app.setOverrideCursor(cursor)


def resetCursor() -> None:
    ''' Clears the cursor-stack to reset an overridden cursor. '''
    app = QtW.qApp
    while app.overrideCursor():
        app.restoreOverrideCursor()


def hideCursor() -> None:
    ''' Clears the cursor-stack then sets the top-level
        cursor to `Qt.BlankCursor`, hiding it. '''
    app = QtW.qApp
    while app.overrideCursor():
        app.restoreOverrideCursor()
    app.setOverrideCursor(QtCore.Qt.BlankCursor)


# ----------------------
# Window focus/flashing
# ----------------------
def showWindow(window: QtW.QWidget, aggressive: bool = False) -> None:
    ''' Shows, raises, and activates a `window`. If `aggressive` is True, a
        different technique for focusing is used that prevents Windows from
        blocking focus (no effect on other platforms). NOTE: `window` is
        expected to have properties named `last_window_size`, `last_window_pos`,
        and `close_was_spontaneous` as Qt's geometry tracking is inconsistent.
        Use `qthelpers.focusWindow` for a more general implementation. '''

    if not window.isVisible():
        if window.was_maximized:
            if window.close_was_spontaneous:
                window.resize(window.last_window_size)
                window.move(window.last_window_pos)
            window.showMaximized()
        else:
            window.show()
    elif window.isMinimized() and window.was_maximized:
        window.showMaximized()
    window.setWindowState(window.windowState() & ~Qt.WindowMinimized)
    window.raise_()

    # use COM to send input to window -> this tricks Windows into thinking "the calling...
    # ...process received the last input event", and thus allows PyPlayer to take focus
    # https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.sendkeys
    if aggressive and platform.system() == 'Windows':
        try:                                # https://stackoverflow.com/a/61180328
            import win32com.client          # '+' actually represents a SHIFT press
            win32com.client.Dispatch("WScript.Shell").SendKeys('+')
        except:
            pass
    window.activateWindow()                 # focus with Qt


def focusWindow(window: QtW.QWidget, aggressive: bool = False) -> None:
    ''' Shows, raises, and activates a `window`. If `aggressive` is True, a
        different technique for focusing is used that prevents Windows from
        blocking focus (no effect on other platforms). This implementation
        works, but tends to restore windows and save geometry inconsistently.
        Use `qthelpers.showWindow` for a more complete implementation. '''

    if not window.isVisible():
        window.show()
    window.setWindowState(window.windowState() & ~Qt.WindowMinimized)
    window.raise_()
    if aggressive and platform.system() == 'Windows':
        try:                                # https://stackoverflow.com/a/61180328
            import win32com.client          # '+' actually represents a SHIFT press
            win32com.client.Dispatch("WScript.Shell").SendKeys('+')
        except:
            pass
    window.activateWindow()                 # focus with Qt


def flashWindow(
    window: QtW.QWidget,
    count: int = -1,
    interval: int = 0,
    duration: int = 0,
    hold: bool = False
) -> None:
    ''' Flashes a `window`'s taskbar icon every `interval` milliseconds `count`
        times, or for `duration` milliseconds. If `hold` is True, `window` will
        not actually flash, but instead stay a solid orange, regardless of
        `count`. If `count` is -1, `window` flashes indefinitely until it's
        in focus (`duration` cannot be used in this case). If `count` is 0
        and `hold` is False, `qthelpers.stopFlashingWindow` is called. If
        `interval` is 0, the default cursor blink rate is used.
        NOTE: `duration` is clamped to a minimum of 1100.
        https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-flashwinfo '''

    if platform.system() != 'Windows': return
    import win32gui
    import win32con

    hwnd = window.winId()
    win32gui.FlashWindowEx(hwnd, win32con.FLASHW_STOP, 0, 0)
    if count == 0 and not hold:             # ^ stop flashing to avoid potential conflicts
        return
    elif hold:                              # hold orange highlight indefinitely
        win32gui.FlashWindow(hwnd, True)
    else:                                   # flash window `count` times
        flags = win32con.FLASHW_TRAY
        if count == -1:                     # flash indefinitely until focused
            if duration: flags |= win32con.FLASHW_TIMER
            else:        flags |= win32con.FLASHW_TIMERNOFG
        win32gui.FlashWindowEx(hwnd, flags, count, interval)

    # hold orange highlight for `duration` ms
    if duration and (hold or count != -1):
        QtCore.QTimer.singleShot(
            max(1100, duration),            # any faster than 1100ms and it just won't work
            lambda: win32gui.FlashWindowEx(hwnd, win32con.FLASHW_STOP, 0, 0)
        )


def stopFlashingWindow(window: QtW.QWidget) -> None:
    ''' Stops flashing `window` if it hasn't already. '''
    if platform.system() != 'Windows': return
    import win32gui
    import win32con
    win32gui.FlashWindowEx(window.winId(), win32con.FLASHW_STOP, 0, 0)


# ----------------------
# Generic dialogs
# ----------------------
def getPopup(
    title: str,
    text: str,
    textInformative: str = None,
    textDetailed: str = None,
    textDetailedAutoOpen: bool = True,
    buttons: int = QMessageBox.Ok,
    defaultButton: int = QMessageBox.Ok,
    icon: str | int = QMessageBox.Question,
    centerWidget: QtW.QWidget = None,
    centerScreen: bool = False,
    centerMouse: bool = False,
    sound: bool = True,
    modal: bool = True,
    opacity: float = 1.0,
    windowIcon=None,
    flags: int = None,
    cursor: QtGui.QCursor | QtCore.Qt.CursorShape = None,
    parent: QtW.QWidget = None
) -> QMessageBox:

    if not text: return                                     # kill popup if no text is passed
    if isinstance(icon, str):                               # allow common icons via a dictionary of strings
        icons = {'information': 1, 'info': 1, 'warning': 2, 'warn': 2, 'critical': 3, 'question': 4}
        icon = icons[icon.strip().lower()]

    def showEvent(event: QtGui.QShowEvent) -> None:
        ''' Plays default OS sound and centers
            the popup before showing if desired. '''
        if sound:
            QtW.QApplication.beep()
        if centerWidget or centerScreen or centerMouse:
            target = centerWidget or None
            screen = centerScreen or False
            mouse = centerMouse or False
            center(msg, target=target, screen=screen, mouse=mouse)

    def enterEvent(event: QtGui.QEnterEvent) -> None:
        ''' Resets the cursor-stack upon mousing over the popup, then
            sets the top-level cursor to `cursor` if provided. '''
        app = QtW.qApp
        while app.overrideCursor():
            app.restoreOverrideCursor()
        if cursor:
            app.setOverrideCursor(cursor)

    msg = QMessageBox(parent, icon=icon)
    msg.showEvent = showEvent
    msg.enterEvent = enterEvent
    msg.setWindowTitle(title)
    msg.setText(text)
    if textInformative: msg.setInformativeText(textInformative)
    if textDetailed:    msg.setDetailedText(textDetailed)
    if not modal:       msg.setWindowModality(Qt.WindowModal)
    if flags:           msg.setWindowFlags(flags)
    msg.setStandardButtons(buttons)                         # ^ invert modality for Qt bug(?) -> Qt.WindowModal = NOT modal
    msg.setDefaultButton(defaultButton)
    msg.setWindowOpacity(opacity)
    msg.setTextInteractionFlags(Qt.TextSelectableByMouse)   # allows copy/paste of popup text
    if isinstance(windowIcon, str):                         # windowIcon (the titlebar icon) is a filepath
        if os.path.exists(windowIcon):
            msg.setWindowIcon(QtGui.QIcon(windowIcon))
        else:   # icon is the name of a Qt icon -> https://www.pythonguis.com/faq/built-in-qicons-pyqt/
            try: msg.setWindowIcon(msg.style().standardIcon(getattr(QtW.QStyle, windowIcon)))
            except: pass
    if textDetailedAutoOpen:                                # auto-opens "Show Details..." button if present
        for button in msg.buttons():
            if button.text() == 'Show Details...':
                button.click()
    return msg


def getPopupOkCancel(*args, **kwargs): return getPopup(*args, buttons=QMessageBox.Ok | QMessageBox.Cancel, **kwargs)
def getPopupYesNo(*args, **kwargs): return getPopup(*args, buttons=QMessageBox.Yes | QMessageBox.No, **kwargs)
def getPopupYesNoCancel(*args, **kwargs): return getPopup(*args, buttons=QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, **kwargs)
def getPopupRetryCancel(*args, **kwargs): return getPopup(*args, buttons=QMessageBox.Retry | QMessageBox.Cancel, **kwargs)
def getPopupAbortRetryIgnore(*args, **kwargs): return getPopup(*args, buttons=QMessageBox.Abort | QMessageBox.Retry | QMessageBox.Ignore, **kwargs)


def getDialogFromUiClass(
    uiClass,
    parent: QtW.QWidget = None,
    centerWidget: QtW.QWidget = None,
    centerScreen: bool = False,
    centerMouse: bool = False,
    modal: bool = False,
    opacity: float = 1.0,
    sound: bool = False,
    deleteOnClose: bool = False,
    flags: int = Qt.WindowCloseButtonHint,
    cursor: QtGui.QCursor | QtCore.Qt.CursorShape = None
) -> QtW.QDialog:
    ''' Returns a persistent dialog based on a `uiClass`, likely provided by
        a converted Qt Designer file. Can be used repeatedly. '''

    class QPersistentDialog(QtW.QDialog, uiClass):
        def __init__(self):
            super().__init__(parent, flags)
            if not modal:
                self.setWindowModality(Qt.WindowModal)      # invert modality for Qt bug(?) -> Qt.WindowModal = NOT modal
            self.setAttribute(Qt.WA_DeleteOnClose, deleteOnClose)
            self.setWindowOpacity(opacity)
            self.setParent(parent)
            self.setupUi(self)

        def showEvent(self, event: QtGui.QShowEvent) -> None:
            ''' Plays default OS sound and centers
                dialog before showing (if desired). '''
            if sound:
                QtW.QApplication.beep()
            if centerWidget or centerScreen or centerMouse:
                target = centerWidget or None
                screen = centerScreen or False
                mouse = centerMouse or False
                center(self, target=target, screen=screen, mouse=mouse)
            return super().showEvent(event)

        def enterEvent(self, event: QtGui.QEnterEvent) -> None:
            ''' Resets the cursor-stack upon mousing over the dialog, then
                sets the top-level cursor to `cursor` if provided. '''
            app = QtW.qApp
            while app.overrideCursor():
                app.restoreOverrideCursor()
            if cursor:
                app.setOverrideCursor(cursor)

    return QPersistentDialog()


def getDialog(
    parent: QtW.QWidget = None,
    title: str = 'Dialog',
    icon: str | int = 'SP_MessageBoxInformation',
    centerWidget: QtW.QWidget = None,
    centerScreen: bool = False,
    centerMouse: bool = False,
    size: tuple[int] = None,
    fixedSize: tuple[int] = None,
    modal: bool = False,
    opacity: float = 1.0,
    sound: bool = False,
    deleteOnClose: bool = True,
    flags: int = Qt.WindowCloseButtonHint,
    cursor: QtGui.QCursor | QtCore.Qt.CursorShape = None
) -> QtW.QDialog:
    ''' Returns a temporary dialog, designed to be finished manually.
        Uses an on-the-fly subclass called `QDialogHybrid` which serves
        to add `QMessageBox`-style functionality to the dialog, allowing easy
        standard-button access, as opposed to the 1 or 0 `QDialogBox` normally
        returns. `QDialogHyrbid` adds the methods `dialog.select(choice)` and
        `dialog.addButtons(layout, *buttons (comma-separated))`, and stores
        the selected StandardButton in dialog.choice. '''

    # workaround for python bug/oddity involving creating lambdas in iterables
    getButtonCallback = lambda this, button: lambda: this.select(button)

    class QDialogHybrid(QtW.QDialog):
        def select(self, choice):
            ''' Sets the selected option to self.choice. `choice` can be
                any type and is accessed/manipulated after dialog execution. '''
            self.choice = choice

        # https://stackoverflow.com/questions/17451688/connecting-a-slot-to-a-button-in-qdialogbuttonbox
        def addButtons(self, layout: QtW.QLayout, *buttons: QtW.QDialogButtonBox.StandardButton) -> QtW.QDialogButtonBox:
            ''' Adds `QDialogButtonBox` to `layout` with a COMMA SEPARATED list
                of `buttons`, connecting them to `self.select()` in order to
                access the user's choice after execution. `QDialogButtonBox` is
                connected to the `accept()` and `reject()` methods for a more
                typical `QDialog` use-case. Returns the `QDialogButtonBox`. '''
            buttonBox = QtW.QDialogButtonBox(self)
            buttonBox.accepted.connect(self.accept)         # connect `buttonBox` to accept/reject in case we don't care about the buttons themselves
            buttonBox.rejected.connect(self.reject)
            for button in buttons:                          # connect buttons to a callback so we can access our selected button later
                buttonBox.addButton(button)
                buttonBox.button(button).clicked.connect(getButtonCallback(self, button))
            if layout:                                      # ^ buttons cannot be connected directly
                layout.addWidget(buttonBox)
            return buttonBox

        def showEvent(self, event: QtGui.QShowEvent) -> None:
            ''' Plays default OS sound and centers the
                popup before showing if desired. '''
            if sound:
                QtW.QApplication.beep()
            if centerWidget or centerScreen or centerMouse:
                target = centerWidget or None
                screen = centerScreen or False
                mouse = centerMouse or False
                center(self, target=target, screen=screen, mouse=mouse)
            return super().showEvent(event)

        def enterEvent(self, event: QtGui.QEnterEvent) -> None:
            ''' Resets the cursor-stack upon mousing over the dialog, then
                sets the top-level cursor to `cursor` if provided. '''
            app = QtW.qApp
            while app.overrideCursor():
                app.restoreOverrideCursor()
            if cursor:
                app.setOverrideCursor(cursor)

    dialog = QDialogHybrid(parent)
    dialog.setWindowFlags(flags)
    dialog.setWindowTitle(title)
    dialog.setAttribute(Qt.WA_DeleteOnClose, deleteOnClose)
    if isinstance(icon, str):
        if os.path.exists(icon):                            # icon is a path to an icon file
            icon = QtGui.QIcon(icon)
        else:   # https://www.pythonguis.com/faq/built-in-qicons-pyqt/ icon is the name of a Qt icon
            try: icon = dialog.style().standardIcon(getattr(QtW.QStyle, icon))
            except AttributeError: icon = None              # invalid Qt icon, replace with nothing
    if icon:      dialog.setWindowIcon(icon)                # icon is an actual QIcon
    if size:      dialog.resize(*size)
    if fixedSize: dialog.setFixedSize(*fixedSize)           # TODO use `width`/`height` parameters instead?
    if not modal: dialog.setWindowModality(Qt.WindowModal)
    dialog.setWindowOpacity(opacity)                        # ^ invert modality for Qt bug(?) -> Qt.WindowModal = NOT modal
    #dialog.setToolTip()
    return dialog


# -------------------------------------------------------
# File dialogs - https://doc.qt.io/qt-5/qfiledialog.html
# -------------------------------------------------------
def browseForDirectory(
    lastdir: str = '.',
    caption: str = 'Select folder',
    directory: str = None,
    url: bool = False,
    lineEdit: QtW.QLineEdit = None
) -> tuple[str, str]:
    try:                                                    # this can be done with one `if url` but it's not worth it
        directory = directory or lastdir
        _dir = (QFileDialog.getExistingDirectoryUrl if url else QFileDialog.getExistingDirectory)(
            caption=caption,
            directory=QtCore.QUrl.fromLocalFile(directory) if url else directory
        )
        localPath = os.path.normpath(_dir.toLocalFile() if url else _dir)
        if localPath != '.':                                # '.' is only possible to get if cancel was selected
            lastdir = os.path.dirname(localPath)
            if lineEdit:                                    # apply text to `lineEdit` if provided
                lineEdit.setText(_dir.url() if url else localPath)
            return _dir if url else localPath, lastdir
    except:
        pass
    return None, lastdir


def browseForFile(
    lastdir: str = '.',
    caption: str = 'Select folder',
    filter: str = 'All files (*)',
    selectedFilter: str = '',
    returnFilter: bool = False,
    directory: str = None,
    name: str = None,
    url: bool = False,
    lineEdit: QtW.QLineEdit = None
) -> tuple[QtCore.QUrl | str, str] | tuple[QtCore.QUrl | str, str, str]:
    try:                                                    # this can be done with one `if url` but it's not worth it
        directory = os.path.join(directory or lastdir, name) if name else (directory or lastdir)
        file, filter = (QFileDialog.getOpenFileUrl if url else QFileDialog.getOpenFileName)(
            caption=caption,
            directory=QtCore.QUrl.fromLocalFile(directory) if url else directory,
            filter=filter,
            initialFilter=selectedFilter
        )
        localPath = os.path.normpath(file.toLocalFile() if url else file)
        if localPath != '.':                                # '.' is only possible to get if cancel was selected
            lastdir = os.path.dirname(localPath)
            if lineEdit:                                    # apply text to `lineEdit` if provided
                lineEdit.setText(file.url() if url else localPath)
            if not url:                                     # return raw `QUrl` object if `url` is True
                file = localPath
            return (file, filter, lastdir) if returnFilter else (file, lastdir)
    except:
        pass
    return (None, '', lastdir) if returnFilter else (None, lastdir)


def browseForFiles(
    lastdir: str = '.',
    caption: str = 'Select folder',
    filter: str = 'All files (*)',
    selectedFilter: str = '',
    returnFilter: bool = False,
    directory: str = None,
    name: str = None,
    url: bool = False
) -> tuple[list[QtCore.QUrl] | list[str], str] | tuple[list[QtCore.QUrl] | list[str], str, str]:
    try:
        directory = os.path.join(directory or lastdir, name) if name else (directory or lastdir)
        files, filter = (QFileDialog.getOpenFileUrls if url else QFileDialog.getOpenFileNames)(
            caption=caption,
            directory=QtCore.QUrl.fromLocalFile(directory) if url else directory,
            filter=filter,
            initialFilter=selectedFilter
        )
        if files:                                           # no files are returned if cancel is selected
            if url:
                lastdir = os.path.normpath(os.path.dirname(files[-1].toLocalFile()))
            else:                                           # normalize all paths in `files` (DON'T do this on urls)
                files = [os.path.normpath(f) for f in files]
                lastdir = os.path.dirname(files[-1])        # set `lastdir` to last file's directory
            return (files, filter, lastdir) if returnFilter else (files, lastdir)
    except:
        pass
    return (list(), '', lastdir) if returnFilter else (list(), lastdir)


def saveFile(
    lastdir: str = '.',
    caption: str = 'Select folder',
    filter: str = 'All files (*)',
    selectedFilter: str = '',
    returnFilter: bool = False,
    directory: str = None,
    name: str = None,
    url: bool = False,
    lineEdit: QtW.QLineEdit = None
) -> tuple[list[QtCore.QUrl] | list[str], str] | tuple[list[QtCore.QUrl] | list[str], str, str]:
    try:                                                    # this can be done with one `if url` but it's not worth it
        directory = os.path.join(directory or lastdir, name) if name else (directory or lastdir)
        file, filter = (QFileDialog.getSaveFileUrl if url else QFileDialog.getSaveFileName)(
            caption=caption,
            directory=QtCore.QUrl.fromLocalFile(directory) if url else directory,
            filter=filter,
            initialFilter=selectedFilter
        )
        localPath = os.path.normpath(file.toLocalFile() if url else file)
        if localPath != '.':                                # '.' is only possible to get if cancel was selected
            lastdir = os.path.dirname(localPath)
            if lineEdit:                                    # apply text to `lineEdit` if provided
                lineEdit.setText(file.url() if url else localPath)
            if not url:                                     # return raw `QUrl` object if `url` is True
                file = localPath
            return (file, filter, lastdir) if returnFilter else (file, lastdir)
    except:
        pass
    return (None, '', lastdir) if returnFilter else (None, lastdir)


# ----------------------
# QListWidget
# ----------------------
# Note -- lists can be cleared with listWidget.clear()
def listGetAllItems(listWidget: QtW.QListWidget):
    for i in range(listWidget.count()):
        yield listWidget.item(i)


def listRemoveSelected(listWidget: QtW.QListWidget, fromShortcut: bool = False) -> None:
    if fromShortcut and not listWidget.hasFocus(): return
    selected = [listWidget.row(item) for item in listWidget.selectedItems()]
    selected.sort(reverse=True)                             # sort list to delete higher indexes first
    for index in selected:
        garbage = listWidget.takeItem(index)
        del garbage                                         # delete items manually


# ----------------------
# QComboBox
# ----------------------
def comboRenameItem(comboBox: QtW.QComboBox, lineEdit: QtW.QLineEdit) -> None:
    if not lineEdit.isVisible():                            # rename started
        lineEdit.show()                                     # show `lineEdit` to rename
        lineEdit.setText(comboBox.currentText())            # start with original name
        lineEdit.selectAll()                                # start with text selected
        lineEdit.setFocus(Qt.NoFocusReason)                 # grab focus to type immediately
    else:                                                   # rename finished
        newName = lineEdit.text()
        if newName:                                         # if the `lineEdit` is blank, don't change the name
            comboBox.setItemText(comboBox.currentIndex(), newName)
        lineEdit.hide()                                     # hide `lineEdit`


def comboMoveItem(comboBox: QtW.QComboBox, direction: str) -> None:
    if not comboBox.hasFocus(): return
    try:
        portText = comboBox.currentText()
        portData = comboBox.currentData(3)
        portIndex = comboBox.currentIndex()
        maxIndex = comboBox.count() - 1
        newIndex = 0

        if direction   == 'up':     newIndex = portIndex - 1
        elif direction == 'down':   newIndex = portIndex + 1
        elif direction == 'top':    newIndex = 0
        elif direction == 'bottom': newIndex = maxIndex

        newIndex = max(min(newIndex, maxIndex), 0)
        comboBox.removeItem(portIndex)
        comboBox.insertItem(newIndex, portText)
        comboBox.setItemData(newIndex, portData, 3)
        comboBox.setCurrentIndex(newIndex)
    except:
        pass


# ----------------------
# QTableWidget
# ----------------------
#def tableGetAllItems(table: QtW.QTableWidget):
    #return [(item := table.item(*pos)).text() for pos in itertools.product(range(table.rowCount()), range(table.columnCount())) if item]
    #items = []
    #for position in itertools.product(range(table.rowCount()), range(table.columnCount())):
    #    #item = table.item(row, column)
    #    if item := table.item(*position) is not None: items.append(item)
    #return items

def tableGetAllRows(tableWidget: QtW.QTableWidget):
    for row in range(tableWidget.rowCount()):
        items = []
        valid_row = False
        for column in range(tableWidget.columnCount()):
            if (item := tableWidget.item(row, column)) is not None:
                valid_row = True
                items.append(item.text())
            else:
                items.append(None)
        if valid_row:
            yield items


# ----------------------
# QTreeWidget
# ----------------------
def treeGetItems(treeWidget: QtW.QTreeWidget):
    treeIter = QtW.QTreeWidgetItemIterator(treeWidget)
    while treeIter.value():
        yield treeIter.value()
        treeIter += 1

def treeGetSelectedItems(treeWidget: QtW.QTreeWidget):
    for item in treeGetItems(treeWidget):
        if item.isSelected():
            yield item

def treeGetSelectedItem(treeWidget: QtW.QTreeWidget) -> QtW.QTreeWidgetItem:
    for item in treeGetItems(treeWidget):
        if item.isSelected():
            return item
    return None

def treeGetItemIndex(treeWidget: QtW.QTreeWidget, item: QtW.QTreeWidgetItem = None) -> int:
    try: item = treeGetSelectedItem(treeWidget) if not item else item
    except: return -1
    return treeWidget.indexFromItem(item).row()

def treeGetTopLevelItem(treeWidget: QtW.QTreeWidget, item: QtW.QTreeWidgetItem = None) -> QtW.QTreeWidgetItem:
    try: item = treeGetSelectedItem(treeWidget) if not item else item
    except: return None
    while item.parent():        # if parent is None, it's a toplevelitem.
        item = item.parent()
    return item

def treeGetTopLevelItemIndex(treeWidget: QtW.QTreeWidget, item: QtW.QTreeWidgetItem = None) -> int:
    try: item = treeGetSelectedItem(treeWidget) if not item else item
    except: return None
    return treeWidget.indexFromItem(treeGetTopLevelItem(treeWidget, item))

def treeSetTopLevelItemIndex(treeWidget: QtW.QTreeWidget, new_index: int = 0, item: QtW.QTreeWidgetItem = None) -> None:
    try: item = treeGetSelectedItem(treeWidget) if not item else item
    except: return None
    old_index = treeWidget.indexOfTopLevelItem(item)
    treeWidget.insertTopLevelItem(new_index, treeWidget.takeTopLevelItem(old_index))


# ----------------------
# QLayout
# ----------------------
def layoutGetItems(layout: QtW.QLayout, start: int = 0, end: int = 0, allow_empty_items: bool = False):
    index = start
    if not end:
        end = layout.count()
    while index <= end:
        item = layout.itemAt(index)
        if not item:
            break
        index += 1

        # other layouts return "widgetItems"
        widget = item.widget()
        if widget or allow_empty_items:
            yield widget
        else:
            continue


def formGetItemsInColumn(formLayout: QtW.QFormLayout, column: int = 0, start: int = 0, end: int = 0):
    row_index = start
    if not end:
        end = formLayout.rowCount()
    while row_index <= end:
        item = formLayout.itemAt(row_index, column)
        if not item:
            break
        row_index += 1

        # forms return natural widgets
        yield item
