from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
import os
import platform
import subprocess

# ---------------------
# Misc
# ---------------------
def openPath(path: str, explore: bool = False, fallback: bool = None):
    ''' Attempts to open `path` with an appropriate application. If `explore`
        is True, `path`'s parent directory is opened in a file explorer with
        `path` pre-selected (if possible). If `fallback` is True and `path`
        does not exist, its parent directory is opened directly. If False, -1
        is returned. If None, `explore`'s value is used for `fallback`. '''
    path = os.path.abspath(path)
    if fallback is None: fallback = explore  # if `fallback` is not specified, use `explore`
    try:
        if not os.path.exists(path):         # ignore `explore` if path doesn't exist (open directory instead)
            if fallback:
                path = os.path.dirname(path)
                if not os.path.exists(path): return -1
            else: return -1
        elif explore:                        # open in explorer with file/directory pre-selected
            system = platform.system()       # couldn't find a way to pre-select files in Linux
            if system == 'Windows': return subprocess.Popen(f'explorer /select, "{path}"')
            elif system == 'Darwin': return subprocess.Popen(f'open -R "{path}"')
    except: pass    # if any error occurs or system wasn't detected (Linux), use Qt to open the path normally
    QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(path))

def showWindow(window: QtWidgets.QWidget) -> None:
    ''' Shows, raises, and activates a `window`. NOTE: `window`'s old geometry
        (`resizeEvent.oldSize/moveEvent.oldPos`), state (`WindowStateChange`),
        and the last `closeEvent.spontaneous` value must all be tracked, as
        Qt's tracking leads to many inconsistencies. `window` is expected to
        have `was_maximized`, `last_window_size`, `last_window_position`, and
        `close_was_spontaneous` attributes. Use `qthelpers.focusWindow` for a
        looser, more general implementation. '''
    if not window.isVisible():
        if window.was_maximized:
            if window.close_was_spontaneous:
                window.resize(window.last_window_size)
                window.move(window.last_window_pos)
            window.showMaximized()
        else: window.show()
    elif window.isMinimized() and window.was_maximized: window.showMaximized()
    window.setWindowState(window.windowState() & ~Qt.WindowMinimized)
    window.raise_()
    window.activateWindow()

def focusWindow(window: QtWidgets.QWidget) -> None:
    ''' Shows, raises, and activates a `window`. This implementation works,
        but tends to restore windows and save geometry inconsistently. Use
        `qthelpers.showWindow` for a more complete implementation. '''
    if not window.isVisible(): window.show()
    window.setWindowState(window.windowState() & ~Qt.WindowMinimized)
    window.raise_()
    window.activateWindow()

def clampToScreen(window, screen: QtGui.QScreen = None,
                  resize: bool = True, move: bool = True,
                  mouseFallback: bool = True, returnScreen: bool = False,
                  strict: bool = False):
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
    if isRect: windowRect = window
    else: windowRect = window.frameGeometry()
    if screen is None: screen = getScreenForRect(windowRect, mouseFallback=mouseFallback)
    screenRect = screen.availableGeometry()     # availableGeometry excludes the taskbar
    if not screenRect.contains(windowRect):     # .contains for entire rect, .intersects for partial rect
        if resize and not isRect:
            screenSize = screenRect.size()
            windowSize = windowRect.size()      # only resize if necessary
            if windowSize.height() > screenSize.height() or windowSize.width() > screenSize.width():
                window.resize(windowRect.size().boundedTo(screenRect.size()))
                windowRect = window.frameGeometry()
        offsetTopLeft = windowRect.topLeft() - screenRect.topLeft()
        windowRect.translate(-min(0, offsetTopLeft.x()), -min(0, offsetTopLeft.y()))
        offsetBottomRight = windowRect.bottomRight() - screenRect.bottomRight()
        windowRect.translate(-max(0, offsetBottomRight.x()), -max(0, offsetBottomRight.y()))
        if move and not isRect: window.move(windowRect.topLeft())   # .setGeometry() is sometimes wrong
    return screen if returnScreen else windowRect

def getScreenForRect(rect: QtCore.QRect, defaultPos: QtCore.QPoint = None,
                     mouseFallback: bool = False, strict: bool = False) -> QtGui.QScreen:
    ''' WARNING: If you're checking a window, pass in geometry(), NOT rect().
        Returns the QScreen that `rect` is touching, if any. If `rect` is not
        touching any screen and `strict` is True, a ValueError is raised.
        Otherwise, if `mouseFallback` is True, the screen the mouse is on is
        returned. If the mouse isn't touching a screen either or neither are
        True, the primary screen is returned. `defaultPos` specifies the
        first QPoint to test before thoroughly testing `rect`. '''
    if defaultPos is None: pos = rect.center()
    else: pos = defaultPos
    qscreen = QtWidgets.QApplication.screenAt(pos)
    if not qscreen:   # check if rect's center (unless defaultPos was None) and corners are on a screen
        if defaultPos is None: points = (rect.topLeft, rect.topRight, rect.bottomLeft, rect.bottomRight)
        else: points = (rect.center, rect.topLeft, rect.topRight, rect.bottomLeft, rect.bottomRight)
        for point in points:
            qscreen = QtWidgets.QApplication.screenAt(point())
            if qscreen: break
        if not qscreen:   # no screen detected -> use mouse. if already used -> use primary screen
            if strict: raise ValueError(f'Rect {rect} is not on any screen.')
            if mouseFallback: qscreen = QtWidgets.QApplication.screenAt(QtGui.QCursor().pos())
            if not qscreen: qscreen = QtWidgets.QApplication.primaryScreen()
    return qscreen

def center(widget: QtWidgets.QWidget, target=None, screen: bool = False,
           mouse: bool = False, strict: bool = False) -> None:
    ''' Centers `widget` over `target`, which may be a widget, QRect, QPoint,
        or an (x, y) tuple. If only `screen` is True, `widget` is centered
        over `target`'s screen, or `widget`'s own screen is `target` is None.
        If only `mouse` is True, `widget` is centered over the mouse. If both
        are True, `widget` is centered over the mouse's screen. `widget` is
        clamped to its new screen if possible. `strict` controls whether or
        not to raise errors when `target` is believed to be invalid. '''
    pos = target
    targetRect = None
    if isinstance(target, QtWidgets.QWidget):
        targetRect = target.geometry()
        pos = target.mapToGlobal(targetRect.center())
    elif isinstance(target, QtCore.QRect):
        targetRect = target
        pos = target.center()
    elif target is not None:
        try: pos = QtCore.QPoint(*target)
        except: raise TypeError('`target` must be a widget, QRect, QPoint, '
                                f'or an (x, y) tuple, not {type(target)}.')
    elif not mouse: screen = True               # only `widget` is set, center on its own screen
    if targetRect is None: targetRect = widget.geometry()

    if screen:
        if mouse: pos = QtGui.QCursor().pos()
        elif not target: pos = widget.mapToGlobal(widget.rect().center())
        pos = getScreenForRect(targetRect, pos, mouse, strict).availableGeometry().center()
    elif mouse: pos = QtGui.QCursor().pos()

    # move widget first, then clamp to screen if possible
    widget.move(pos - widget.rect().center())   # move immediately and correct later
    if not screen:                              # clamp is pointless if `screen` was set
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


# ---------------------
# Generic dialogs
# ---------------------
def getPopup(title, text, textInformative=None, textDetailed=None, textDetailedAutoOpen=True,
             buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok, icon=QMessageBox.Question,
             centerWidget=None, centerScreen=False, centerMouse=False, sound=True,
             modal=True, opacity=1.0, windowIcon=None, parent=None) -> QMessageBox:
    if not text: return                                     # kill popup if no text is passed
    if isinstance(icon, str):                               # allow common icons via a dictionary of strings
        icons = {'information': 1, 'info': 1, 'warning': 2, 'warn': 2, 'critical': 3, 'question': 4}
        icon = icons[icon.strip().lower()]

    def showEvent(event):
        ''' Plays default OS sound and centers the popup before showing if desired. '''
        if sound: QtWidgets.QApplication.beep()
        if centerWidget or centerScreen or centerMouse:
            target = centerWidget or None
            screen = centerScreen or False
            mouse = centerMouse or False
            center(msg, target=target, screen=screen, mouse=mouse)

    msg = QMessageBox(parent, icon=icon)
    msg.showEvent = showEvent
    msg.setWindowTitle(title)
    msg.setText(text)
    if textInformative: msg.setInformativeText(textInformative)
    if textDetailed: msg.setDetailedText(textDetailed)
    if not modal: msg.setWindowModality(Qt.WindowModal)     # invert modality for Qt bug(?) -> Qt.WindowModal = NOT modal
    msg.setStandardButtons(buttons)
    msg.setDefaultButton(defaultButton)
    msg.setWindowOpacity(opacity)
    msg.setTextInteractionFlags(Qt.TextSelectableByMouse)   # allows copy/paste of popup text
    if isinstance(windowIcon, str):                         # windowIcon (the titlebar icon) is a filepath
        if os.path.exists(windowIcon): msg.setWindowIcon(QtGui.QIcon(windowIcon))
        else:   # icon is the name of a Qt icon -> https://www.pythonguis.com/faq/built-in-qicons-pyqt/
            try: msg.setWindowIcon(msg.style().standardIcon(getattr(QtWidgets.QStyle, windowIcon)))
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

def getDialogFromUiClass(uiClass, parent=None, **kwargs):
    ''' Returns a persistent dialog based on a `uiClass`, likely provided by
        a converted Qt Designer file. Can be used repeatedly, as a persistent
        dialog. Accepts `modal`, `deleteOnClose/delete`, and
        `centerWidget/centerScreen/centerMouse` keyword parameters. '''
    class QPersistentDialog(QtWidgets.QDialog, uiClass):
        def __init__(self, parent, **kwargs):
            super().__init__(parent)
            if 'delete' in kwargs: kwargs['deleteOnClose'] = kwargs['delete']    # accept both 'delete' and 'deleteOnClose'
            self.setAttribute(Qt.WA_DeleteOnClose, kwargs.get('deleteOnClose', False))
            modal = kwargs.get('modal', False) or kwargs.get('blocking', False)  # accept both 'modal' and 'blocking'
            if not modal: self.setWindowModality(Qt.WindowModal)    # invert modality for Qt bug(?) -> Qt.WindowModal = NOT modal
            self.setParent(parent)
            self.setupUi(self)

        def showEvent(self, event):
            ''' Plays default OS sound and centers dialog before showing if desired. '''
            if kwargs.get('sound', False): QtWidgets.QApplication.beep()
            centerWidget = kwargs.get('centerWidget', None)
            centerScreen = kwargs.get('centerScreen', False)
            centerMouse = kwargs.get('centerMouse', False)
            if centerWidget or centerScreen or centerMouse:
                target = centerWidget or None
                screen = centerScreen or False
                mouse = centerMouse or False
                center(self, target=target, screen=screen, mouse=mouse)
            return super().showEvent(event)
    return QPersistentDialog(parent, **kwargs)

def getDialog(parent=None, title='Dialog', icon='SP_MessageBoxInformation',
              centerWidget=None, centerScreen=False, centerMouse=False,
              size=None, fixedSize=None, modal=False, opacity=1.0,
              sound=False, deleteOnClose=True, flags=Qt.WindowCloseButtonHint) -> QtWidgets.QDialog:
    ''' Returns a temporary dialog, designed to be finished manually. Uses an on-the-fly subclass called QDialogHybrid
        which serves to add QMessageBox-style functionality to the dialog, allowing easy standard-button access, as
        opposed to the 1 or 0 QDialogBox normally returns. QDialogHyrbid adds the methods dialog.select(choice) and
        dialog.addButtons(layout, *buttons (comma-separated)), and stores the selected StandardButton in dialog.choice. '''
    getButtonCallback = lambda this, button: lambda: this.select(button)  # workaround for python bug/oddity involving creating lambdas in iterables

    class QDialogHybrid(QtWidgets.QDialog):
        def select(self, choice):
            ''' Sets the selected option to self.choice. `choice` can be any
                type and is accessed/manipulated after dialog execution. '''
            self.choice = choice

        def addButtons(self, layout, *buttons):             # https://stackoverflow.com/questions/17451688/connecting-a-slot-to-a-button-in-qdialogbuttonbox
            ''' Adds QDialogButtonBox to `layout` with a COMMA SEPARATED list of `buttons`, connecting them to
                the self.select() method in order to access the user's choice after execution. QDialogButtonBox
                is connected to the .accept() and .reject() methods for a more typical QDialog use-case. '''
            buttonBox = QtWidgets.QDialogButtonBox(self)
            buttonBox.accepted.connect(self.accept)         # connect buttonBox to accept/reject in case we don't care about the buttons themselves
            buttonBox.rejected.connect(self.reject)
            for button in buttons:                          # connect buttons to a callback so we can access our selected button later
                buttonBox.addButton(button)
                buttonBox.button(button).clicked.connect(getButtonCallback(self, button))     # buttons cannot be connected directly
            layout.addWidget(buttonBox)

        def showEvent(self, event):
            ''' Plays default OS sound and centers the popup before showing if desired. '''
            if sound: QtWidgets.QApplication.beep()
            if centerWidget or centerScreen or centerMouse:
                target = centerWidget or None
                screen = centerScreen or False
                mouse = centerMouse or False
                center(self, target=target, screen=screen, mouse=mouse)
            return super().showEvent(event)

    dialog = QDialogHybrid(parent)
    dialog.setWindowFlags(flags)
    dialog.setWindowTitle(title)
    dialog.setAttribute(Qt.WA_DeleteOnClose, deleteOnClose)
    if isinstance(icon, str):
        if os.path.exists(icon): icon = QtGui.QIcon(icon)   # icon is a path to an icon file
        else:   # https://www.pythonguis.com/faq/built-in-qicons-pyqt/ icon is the name of a Qt icon
            try: icon = dialog.style().standardIcon(getattr(QtWidgets.QStyle, icon))
            except AttributeError: icon = None              # invalid Qt icon, replace with nothing
    if icon: dialog.setWindowIcon(icon)
    if size: dialog.resize(*size)
    if fixedSize: dialog.setFixedSize(*fixedSize)           # TODO add width/height?
    if not modal: dialog.setWindowModality(Qt.WindowModal)  # invert modality for Qt bug(?) -> Qt.WindowModal = NOT modal
    dialog.setWindowOpacity(opacity)
    #dialog.setToolTip()
    return dialog


# -------------------------------------------------------
# File dialogs - https://doc.qt.io/qt-5/qfiledialog.html
# -------------------------------------------------------
def browseForDirectory(lastdir='.', caption='Select folder', directory=None, url=False):
    directory = directory if directory else lastdir
    _dir = (QFileDialog.getExistingDirectoryUrl if url else QFileDialog.getExistingDirectory)(
        caption=caption,
        directory=QtCore.QUrl.fromLocalFile(directory) if url else directory
    )
    try:
        path = _dir.url() if url else _dir
        if not path: return None, lastdir   # cancel selected
        lastdir = os.path.dirname(_dir.toLocalFile() if url else _dir)
        return _dir, lastdir
    except: return None, lastdir

def browseForFile(lastdir='.', caption='Select file', filter='All files (*)',
                  selectedFilter='', returnFilter=False,
                  directory=None, name=None, url=False):
    directory = os.path.join(directory or lastdir, name) if name else (directory or lastdir)
    file, filter = (QFileDialog.getOpenFileUrl if url else QFileDialog.getOpenFileName)(
        caption=caption,
        directory=QtCore.QUrl.fromLocalFile(directory) if url else directory,
        filter=filter,
        initialFilter=selectedFilter
    )
    try:
        path = file.url() if url else file
        if not path: return (None, '', lastdir) if returnFilter else (None, lastdir)
        lastdir = (os.sep).join((file.toLocalFile() if url else file).split('/')[:-1])
        return (file, filter, lastdir) if returnFilter else (file, lastdir)
    except: return (None, '', lastdir) if returnFilter else (None, lastdir)

def browseForFiles(lastdir='.', caption='Select files', filter='All files (*)',
                   selectedFilter='', returnFilter=False,
                   directory=None, name=None, url=False):
    directory = os.path.join(directory or lastdir, name) if name else (directory or lastdir)
    files, filter = (QFileDialog.getOpenFileUrls if url else QFileDialog.getOpenFileNames)(
        caption=caption,
        directory=QtCore.QUrl.fromLocalFile(directory) if url else directory,
        filter=filter,
        initialFilter=selectedFilter
    )
    try:
        if not files: return (tuple(), '', lastdir) if returnFilter else (tuple(), lastdir)
        lastdir = (os.sep).join((files[-1].toLocalFile() if url else files[-1]).split('/')[:-1])  # base lastdir on last file's directory
        return (files, filter, lastdir) if returnFilter else (files, lastdir)
    except: return (tuple(), '', lastdir) if returnFilter else (tuple(), lastdir)

def saveFile(lastdir='.', caption='Save file', filter='All files (*)',
             selectedFilter='', returnFilter=False,
             directory=None, name=None, url=False):
    directory = os.path.join(directory or lastdir, name) if name else (directory or lastdir)
    file, filter = (QFileDialog.getSaveFileUrl if url else QFileDialog.getSaveFileName)(
        caption=caption,
        directory=QtCore.QUrl.fromLocalFile(directory) if url else directory,
        filter=filter,
        initialFilter=selectedFilter
    )
    try:
        path = file.url() if url else file
        if not path: return (None, '', lastdir) if returnFilter else None, lastdir
        lastdir = (os.sep).join((file.toLocalFile() if url else file).split('/')[:-1])
        return (file, filter, lastdir) if returnFilter else (file, lastdir)
    except: return (None, '', lastdir) if returnFilter else (None, lastdir)


# ---------------------
# ListWidgets
# ---------------------
# Note -- lists can be cleared with listWidget.clear()
def listGetAllItems(listWidget):
    for i in range(listWidget.count()):
        yield listWidget.item(i)

def listRemoveSelected(listWidget, fromShortcut=False):
    if fromShortcut and not listWidget.hasFocus(): return
    selected = [listWidget.row(item) for item in listWidget.selectedItems()]
    selected.sort(reverse=True)     # sort list to delete higher indexes first
    for index in selected:
        garbage = listWidget.takeItem(index)
        del garbage                 # delete items manually


# ---------------------
# ComboWidgets
# ---------------------
def comboRenameItem(comboWidget, lineEdit):
    if not lineEdit.isVisible():    # rename started
        lineEdit.show()             # show lineEdit to rename
        lineEdit.setText(comboWidget.currentText())   # start with original name
        lineEdit.selectAll()        # start with text selected
        lineEdit.setFocus(Qt.NoFocusReason)   # grab focus to type immediately
    else:                           # rename finished
        newName = lineEdit.text()
        if newName:                 # if the lineEdit is blank, don't change the name
            comboWidget.setItemText(comboWidget.currentIndex(), newName)   # change name
        lineEdit.hide()             # hide lineEdit

def comboMoveItem(comboWidget, direction):
    if not comboWidget.hasFocus(): return
    try:
        portText = comboWidget.currentText()
        portData = comboWidget.currentData(3)
        portIndex = comboWidget.currentIndex()
        maxIndex = comboWidget.count() - 1
        newIndex = 0

        if direction   == 'up':     newIndex = portIndex - 1
        elif direction == 'down':   newIndex = portIndex + 1
        elif direction == 'top':    newIndex = 0
        elif direction == 'bottom': newIndex = maxIndex

        newIndex = max(min(newIndex, maxIndex), 0)
        comboWidget.removeItem(portIndex)
        comboWidget.insertItem(newIndex, portText)
        comboWidget.setItemData(newIndex, portData, 3)
        comboWidget.setCurrentIndex(newIndex)
    except: pass


# ---------------------
# TableWidgets
# ---------------------
#def tableGetAllItems(table):
    #return [(item := table.item(*pos)).text() for pos in itertools.product(range(table.rowCount()), range(table.columnCount())) if item]
    #items = []
    #for position in itertools.product(range(table.rowCount()), range(table.columnCount())):
    #    #item = table.item(row, column)
    #    if item := table.item(*position) is not None: items.append(item)
    #return items

def tableGetAllRows(table):
    for row in range(table.rowCount()):
        items = []
        valid_row = False
        for column in range(table.columnCount()):
            if (item := table.item(row, column)) is not None:
                valid_row = True
                items.append(item.text())
            else: items.append(None)
        if valid_row: yield items


# ---------------------
# TreeWidgets
# ---------------------
def treeGetItems(treeWidget):
    treeIter = QtWidgets.QTreeWidgetItemIterator(treeWidget)
    while treeIter.value():
        yield treeIter.value()
        treeIter += 1

def treeGetSelectedItems(treeWidget):
    for item in treeGetItems(treeWidget):
        if item.isSelected():
            yield item

def treeGetSelectedItem(treeWidget):
    for item in treeGetItems(treeWidget):
        if item.isSelected():
            return item
    return None

def treeGetItemIndex(treeWidget, item=None):
    try: item = treeGetSelectedItem(treeWidget) if not item else item
    except: return -1
    return treeWidget.indexFromItem(item).row()

def treeGetTopLevelItem(treeWidget, item=None):
    try: item = treeGetSelectedItem(treeWidget) if not item else item
    except: return None
    while item.parent():    # if parent is None, it's a toplevelitem.
        item = item.parent()
    return item

def treeGetTopLevelItemIndex(treeWidget, item=None):
    try: item = treeGetSelectedItem(treeWidget) if not item else item
    except: return None
    return treeWidget.indexFromItem(treeGetTopLevelItem(treeWidget, item))

def treeSetTopLevelItemIndex(treeWidget, new_index=0, item=None):
    try: item = treeGetSelectedItem(treeWidget) if not item else item
    except: return None
    old_index = treeWidget.indexOfTopLevelItem(item)
    treeWidget.insertTopLevelItem(new_index, treeWidget.takeTopLevelItem(old_index))


# ---------------------
# Layouts
# ---------------------
def layoutGetItems(layout, start=0, end=0):
    index = start
    if end == 0: end = layout.count()
    while index <= end:
        item = layout.itemAt(index)
        if not item: break
        yield item.widget()     # other layouts return "widgetItems"
        index += 1

def formGetItemsInColumn(formLayout, column=0, start=0, end=0):
    row_index = start
    if end == 0: end = formLayout.rowCount()
    while row_index <= end:
        item = formLayout.itemAt(row_index, column)
        if not item: break
        yield item              # forms return natural widgets
        row_index += 1
