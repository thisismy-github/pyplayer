from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
import os
import time
import platform
import subprocess

# ---------------------
# Misc
# ---------------------
def getUniquePath(path: str, start: int = 2, key: str = None, zeros: int = 0, strict: bool = False) -> str:
    ''' Returns a unique `path`. If `path` already exists, version-numbers starting from `start` are added. If a
        keyword `key` is provided and exists within `path`, it is replaced with the version number with `zeros`
        padded zeros. Otherwise, Windows-style naming is used with no padding: "(base) (version).(ext)".
        The `strict` parameter forces `key` paths to always have version numbers included, even if `path`
        was unique to begin with. This does not apply to Windows-style naming. '''
    # TODO: add ignore_extensions parameter that uses os.path.splitext and glob(basepath.*)
    start_time = time.time()
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
    print(f'Unique path in {time.time() - start_time:.4f} seconds: {path}')
    return path

def addPathSuffix(path: str, suffix: str, unique: bool = False) -> str:
    ''' Returns a path with `suffix` added between the basename and extension. If `unique` is set,
        the new path will be run through getUniquePath with default arguments before returning. '''
    base, ext = os.path.splitext(path)
    return f'{base}{suffix}{ext}' if not unique else getUniquePath(f'{base}{suffix}{ext}')

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

def getFromPATH(filename: str) -> str:
    ''' Returns the full path to a `filename` if it exists in
        the user's PATH, otherwise returns an empty string. '''
    for path in os.environ.get('PATH', '').split(';' if platform.system() == 'Windows' else ':'):
        try:
            if filename in os.listdir(path):
                return os.path.join(path, filename)
        except: pass
    return ''

def showWindow(window: QtWidgets.QWidget) -> None:
    ''' Shows, restores, raises, and activates a `window`. '''
    if not window.isVisible(): window.show()
    window.setWindowState(window.windowState() & ~Qt.WindowMinimized)
    window.raise_()
    window.activateWindow()

def getHMS(seconds: float) -> tuple:
    ''' Converts seconds to the hours, minutes, seconds, and milliseconds it represents. '''
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int((seconds % 3600) % 60)
    ms = int(round((seconds - int(seconds)) * 100, 4))  # round to account for floating point imprecision
    return h, m, s, ms


# ---------------------
# Generic dialogs
# ---------------------
def getPopup(title, text, textInformative=None, textDetailed=None, textDetailedAutoOpen=False,
             buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok, modal=True, opacity=1.0,
             icon=QMessageBox.Question, windowIcon=None) -> QMessageBox:
    if not text: return                                             # kill popup if no text is passed
    if isinstance(icon, str):                                       # allow common icons via a dictionary of strings
        icons = {'information': 1, 'info': 1, 'warning': 2, 'warn': 2, 'critical': 3, 'question': 4}
        icon = icons[icon.strip().lower()]
    msg = QMessageBox(icon=icon)
    msg.setWindowTitle(title)
    msg.setText(text)
    if textInformative: msg.setInformativeText(textInformative)
    if textDetailed: msg.setDetailedText(textDetailed)
    if not modal: msg.setWindowModality(Qt.WindowModal)             # invert modality for Qt bug(?) -> Qt.WindowModal = NOT modal
    msg.setStandardButtons(buttons)
    msg.setDefaultButton(defaultButton)
    msg.setWindowOpacity(opacity)
    msg.setTextInteractionFlags(Qt.TextSelectableByMouse)           # allows copy/paste of popup text
    if isinstance(windowIcon, str):                                 # windowIcon (the titlebar icon) is a filepath
        if os.path.exists(windowIcon): msg.setWindowIcon(QtGui.QIcon(windowIcon))
        else:   # icon is the name of a Qt icon -> https://www.pythonguis.com/faq/built-in-qicons-pyqt/
            try: msg.setWindowIcon(msg.style().standardIcon(getattr(QtWidgets.QStyle, windowIcon)))
            except: pass
    if textDetailedAutoOpen:                                        # auto-opens "Show Details..." button if present
        for button in msg.buttons():
            if button.text() == 'Show Details...':
                button.click()
    return msg

def getPopupOkCancel(title, text, textInformative=None, textDetailed=None, textDetailedAutoOpen=False,
                     defaultButton=QMessageBox.Ok, icon=QMessageBox.Question, modal=True, opacity=1.0) -> QMessageBox:
    return getPopup(title, text, textInformative, textDetailed, textDetailedAutoOpen,
                    buttons=QMessageBox.Ok | QMessageBox.Cancel, defaultButton=defaultButton,
                    icon=icon, modal=modal, opacity=opacity)

def getPopupYesNo(title, text, textInformative=None, textDetailed=None, textDetailedAutoOpen=False,
                  defaultButton=QMessageBox.Yes, icon=QMessageBox.Question, modal=True, opacity=1.0) -> QMessageBox:
    return getPopup(title, text, textInformative, textDetailed, textDetailedAutoOpen,
                    buttons=QMessageBox.Yes | QMessageBox.No, defaultButton=defaultButton,
                    icon=icon, modal=modal, opacity=opacity)

def getPopupYesNoCancel(title, text, textInformative=None, textDetailed=None, textDetailedAutoOpen=False,
                        defaultButton=QMessageBox.Yes, icon=QMessageBox.Question, modal=True, opacity=1.0) -> QMessageBox:
    return getPopup(title, text, textInformative, textDetailed, textDetailedAutoOpen,
                    buttons=QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                    defaultButton=defaultButton, icon=icon, modal=modal, opacity=opacity)

def getDialogFromUiClass(uiClass, parent=None, **kwargs):
    ''' Returns a persistent dialog based on a `uiClass`, likely provided by a converted Qt Designer file. Can be
        used repeatedly, as a persistent dialog. Accepts the `modal` and `deleteOnClose/delete` keyword parameters. '''
    class QPersistentDialog(QtWidgets.QDialog, uiClass):
        def __init__(self, parent, **kwargs):
            super().__init__(parent)
            if 'delete' in kwargs: kwargs['deleteOnClose'] = kwargs['delete']    # accept both 'delete' and 'deleteOnClose'
            self.setAttribute(Qt.WA_DeleteOnClose, kwargs.get('deleteOnClose', False))
            modal = kwargs.get('modal', False) or kwargs.get('blocking', False)  # accept both 'modal' and 'blocking'
            if not modal: self.setWindowModality(Qt.WindowModal)    # # invert modality for Qt bug(?) -> Qt.WindowModal = NOT modal
            self.setParent(parent)
            self.setupUi(self)
    return QPersistentDialog(parent, **kwargs)

def getDialog(parent=None, title='Dialog', icon='SP_MessageBoxInformation', size=None, fixedSize=None,
              opacity=1.0, modal=False, deleteOnClose=True, flags=Qt.WindowCloseButtonHint):
    ''' Returns a temporary dialog, designed to be finished manually. Uses an on-the-fly subclass called QDialogHybrid
        which serves to add QMessageBox-style functionality to the dialog, allowing easy standard-button access, as
        opposed to the 1 or 0 QDialogBox normally returns. QDialogHyrbid adds the methods dialog.select(choice) and
        dialog.addButtons(layout, *buttons (comma-separated)), and stores the selected StandardButton in dialog.choice. '''
    get_button_callback = lambda this, button: lambda: this.select(button)  # workaround for python bug/oddity involving creating lambdas in iterables

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
                buttonBox.button(button).clicked.connect(get_button_callback(self, button))     # buttons cannot be connected directly
            layout.addWidget(buttonBox)

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
    if not modal: dialog.setWindowModality(Qt.WindowModal)  # # invert modality for Qt bug(?) -> Qt.WindowModal = NOT modal
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
    print('\n\n\nWHAT IS THE DIFFERENCE', lastdir, caption, filter, selectedFilter, returnFilter, directory, name, url)
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
