# -*- coding: utf-8 -*-

__author__ = 'LevBravE'

from PySide import QtCore, QtGui
from AnimationLabel import AnimationLabel
from FrameSeparator import FrameSeparator

#**************************************************************************************************
# class: DialogDBUpdate
#**************************************************************************************************

class DialogDBUpdate(QtGui.QDialog):
    """
    Диалоговое окно загрузки нового файла базы данных
    """

    def __init__(self, title, updateData, flagCheckServer):
        QtGui.QDialog.__init__(self)
        # RadioButton
        self.__autoRadioButton = QtGui.QRadioButton(self.tr('Обновить базу данных с сервера'))
        self.__manualRadioButton = QtGui.QRadioButton(self.tr('Указать путь к файлу базы данных'))
        # ButtonGroup
        self.__buttonGroup = QtGui.QButtonGroup()
        self.__buttonGroup.addButton(self.__autoRadioButton)
        self.__buttonGroup.addButton(self.__manualRadioButton)
        # LineEdit
        self.__pathLineEdit = QtGui.QLineEdit()
        # AnimationLabel
        self.__animationLabel = AnimationLabel('img/loader.gif')
        #self.__animationLabel._start()
        # Label
        strUpdateData = QtCore.QDateTime().fromString(updateData, QtCore.Qt.ISODate).toString('dd.MM.yyyy hh:mm')
        self.__updateDataLabel = QtGui.QLabel(self.tr('Дата последнего обновления: %s') % strUpdateData)
        # Button
        self.__buttonUpdate = QtGui.QPushButton(self.tr('Обновить'))
        self.__buttonUpdate.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        self.__buttonOpenFile = QtGui.QPushButton('...')
        self.__buttonOpenFile.setShortcut('Shift+Enter')
        self.__buttonOpenFile.setToolTip(self.tr('Shift+Enter'))

        self.__dialogButtonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        # Layout
        self.__layoutHButton = QtGui.QHBoxLayout()
        self.__layoutHButton.setAlignment(QtCore.Qt.AlignHCenter)
        self.__layoutHButton.addWidget(self.__buttonUpdate)

        self.__layoutVUpdate = QtGui.QVBoxLayout()
        self.__layoutVUpdate.setAlignment(QtCore.Qt.AlignHCenter)
        self.__layoutVUpdate.addWidget(self.__animationLabel)
        self.__layoutVUpdate.addLayout(self.__layoutHButton)

        self.__layoutHPath = QtGui.QHBoxLayout()
        self.__layoutHPath.addWidget(self.__pathLineEdit)
        self.__layoutHPath.addWidget(self.__buttonOpenFile)

        self.__layoutVMain = QtGui.QVBoxLayout()
        self.__layoutVMain.addWidget(self.__autoRadioButton)
        self.__layoutVMain.addLayout(self.__layoutVUpdate)
        self.__layoutVMain.addWidget(self.__manualRadioButton)
        self.__layoutVMain.addLayout(self.__layoutHPath)
        self.__layoutVMain.addWidget(self.__updateDataLabel)
        self.__layoutVMain.addWidget(FrameSeparator(QtGui.QFrame.HLine, QtGui.QFrame.Sunken))
        self.__layoutVMain.addWidget(self.__dialogButtonBox)
        # Function
        self._checkServer(flagCheckServer)
        # Connect
        self.__buttonGroup.buttonClicked.connect(self._buttonClicked)

        self.__buttonUpdate.clicked.connect(self._updateDB)

        self.__buttonOpenFile.clicked.connect(self._openFile)

        self.__dialogButtonBox.accepted.connect(self.accept)
        self.__dialogButtonBox.rejected.connect(self.reject)
        # <<<Self>>>
        self.setLayout(self.__layoutVMain)
        self.setModal(True)
        self.setWindowTitle(title)
        self.resize(350, 200)

    def _checkServer(self, check):
        if check:
            self.__autoRadioButton.setChecked(True)
            self.__pathLineEdit.setEnabled(False)
            self.__buttonOpenFile.setEnabled(False)
        else:
            self.__autoRadioButton.setEnabled(False)
            self.__manualRadioButton.setChecked(True)
            self.__buttonUpdate.setEnabled(False)

    def _updateDB(self):
        self.__animationLabel._stop()

    def _buttonClicked(self):
        if self.__buttonGroup.checkedId() == -3:
            self.__pathLineEdit.setEnabled(True)
            self.__buttonOpenFile.setEnabled(True)

            self.__buttonUpdate.setEnabled(False)
        else:
            self.__buttonUpdate.setEnabled(True)

            self.__pathLineEdit.setEnabled(False)
            self.__buttonOpenFile.setEnabled(False)

    def _openFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
            self.tr('Выбрать файл базы данных'), QtCore.QDir.homePath(),
            self.tr('SQLite файл (*.sqlite)'))[0]

        self.__pathLineEdit.setText(fileName)

    def _path(self):
        return self.__pathLineEdit.text()

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('UTF-8'))
    dialogDBUpdate = DialogDBUpdate(app.tr('Обновление базы данных специальностей'), '04.06.2012 13:40', True)
    sys.exit(dialogDBUpdate.exec_())
