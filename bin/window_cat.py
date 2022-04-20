# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bin\window_cat.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_catDialog(object):
    def setupUi(self, catDialog):
        catDialog.setObjectName("catDialog")
        catDialog.resize(421, 421)
        catDialog.setWindowTitle("Videos to concatenate")
        self.gridLayout = QtWidgets.QGridLayout(catDialog)
        self.gridLayout.setContentsMargins(-1, -1, -1, 6)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.down = QtWidgets.QPushButton(catDialog)
        self.down.setMaximumSize(QtCore.QSize(24, 16777215))
        self.down.setText("▼")
        self.down.setObjectName("down")
        self.gridLayout.addWidget(self.down, 5, 3, 1, 1)
        self.add = QtWidgets.QPushButton(catDialog)
        self.add.setMaximumSize(QtCore.QSize(24, 16777215))
        self.add.setText("+")
        self.add.setObjectName("add")
        self.gridLayout.addWidget(self.add, 5, 0, 1, 1)
        self.delete = QtWidgets.QPushButton(catDialog)
        self.delete.setMaximumSize(QtCore.QSize(24, 16777215))
        self.delete.setText("-")
        self.delete.setObjectName("delete")
        self.gridLayout.addWidget(self.delete, 5, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(catDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 4, 1, 1)
        self.up = QtWidgets.QPushButton(catDialog)
        self.up.setMaximumSize(QtCore.QSize(24, 16777215))
        self.up.setText("▲")
        self.up.setObjectName("up")
        self.gridLayout.addWidget(self.up, 5, 2, 1, 1)
        self.videoList = QVideoList(catDialog)
        self.videoList.setAcceptDrops(True)
        self.videoList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.videoList.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.videoList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.videoList.setMovement(QtWidgets.QListView.Free)
        self.videoList.setSelectionRectVisible(True)
        self.videoList.setObjectName("videoList")
        self.gridLayout.addWidget(self.videoList, 0, 0, 1, 5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 2)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.output = QtWidgets.QLineEdit(catDialog)
        self.output.setObjectName("output")
        self.horizontalLayout.addWidget(self.output)
        self.browse = QtWidgets.QPushButton(catDialog)
        self.browse.setMaximumSize(QtCore.QSize(26, 22))
        self.browse.setObjectName("browse")
        self.horizontalLayout.addWidget(self.browse)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.checkOpen = QtWidgets.QCheckBox(catDialog)
        self.checkOpen.setObjectName("checkOpen")
        self.horizontalLayout_2.addWidget(self.checkOpen)
        self.checkExplore = QtWidgets.QCheckBox(catDialog)
        self.checkExplore.setObjectName("checkExplore")
        self.horizontalLayout_2.addWidget(self.checkExplore)
        self.checkDelete = QtWidgets.QCheckBox(catDialog)
        self.checkDelete.setTristate(True)
        self.checkDelete.setObjectName("checkDelete")
        self.horizontalLayout_2.addWidget(self.checkDelete)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 5)

        self.retranslateUi(catDialog)
        self.buttonBox.accepted.connect(catDialog.accept)
        self.buttonBox.rejected.connect(catDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(catDialog)

    def retranslateUi(self, catDialog):
        _translate = QtCore.QCoreApplication.translate
        self.down.setShortcut(_translate("catDialog", "Del"))
        self.add.setShortcut(_translate("catDialog", "Ins"))
        self.delete.setShortcut(_translate("catDialog", "Del"))
        self.up.setShortcut(_translate("catDialog", "Del"))
        self.browse.setText(_translate("catDialog", "..."))
        self.checkOpen.setToolTip(_translate("catDialog", "If checked, the concatenated video will\n"
"automatically play in PyPlayer after saving."))
        self.checkOpen.setText(_translate("catDialog", "Play after save"))
        self.checkExplore.setToolTip(_translate("catDialog", "If checked, the concatenated video will\n"
"automatically open in explorer after saving."))
        self.checkExplore.setText(_translate("catDialog", "Explore after save"))
        self.checkDelete.setToolTip(_translate("catDialog", "Tristate:\n"
"\n"
"Partially checked - videos will be marked\n"
"for deletion after concatenation.\n"
"\n"
"Fully checked - videos will be immediately\n"
"deleted after successful concatenation.\n"
"\n"
"Note: File deletion/recycling\n"
"is dependent on your settings."))
        self.checkDelete.setText(_translate("catDialog", "Delete originals"))
from widgets import QVideoList


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    catDialog = QtWidgets.QDialog()
    ui = Ui_catDialog()
    ui.setupUi(catDialog)
    catDialog.show()
    sys.exit(app.exec_())
