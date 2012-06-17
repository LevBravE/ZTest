# -*- coding: utf-8 -*-

__author__ = 'LevBravE'

from PySide import QtCore, QtGui
from FrameSeparator import FrameSeparator

#**************************************************************************************************
# class: DialogSettings
#**************************************************************************************************

class DialogSettings(QtGui.QDialog):
    """
    Диалоговое окно настройки приложения
    """

    def __init__(self, title):
        QtGui.QDialog.__init__(self)
        # LineEdit
        self.__urlServerLineEdit = QtGui.QLineEdit()
        # Button
        self.__dialogButtonBox = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.RestoreDefaults | QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        # Layout
        self.__layoutVMain = QtGui.QVBoxLayout()
        self.__layoutVMain.addWidget(QtGui.QLabel(self.tr('Адрес сервера - DstuTest')))
        self.__layoutVMain.addWidget(self.__urlServerLineEdit)
        self.__layoutVMain.addWidget(FrameSeparator(QtGui.QFrame.HLine, QtGui.QFrame.Sunken))
        self.__layoutVMain.addWidget(self.__dialogButtonBox)
        # Connect
        self.__dialogButtonBox.button(QtGui.QDialogButtonBox.RestoreDefaults).clicked.connect(self._reset)
        self.__dialogButtonBox.accepted.connect(self.accept)
        self.__dialogButtonBox.rejected.connect(self.reject)
        # <<<Self>>>
        self.setLayout(self.__layoutVMain)
        self.setModal(True)
        self.setWindowTitle(title)

    def _reset(self):
        self.__urlServerLineEdit.setText('http://dstutest.local/')

    # get and set (start)
    def _urlServer(self):
        return self.__urlServerLineEdit.text()

    def _setUrlServer(self, url):
        self.__urlServerLineEdit.setText(url)

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('UTF-8'))
    dialogSettings = DialogSettings(app.tr('Настройки'))
    sys.exit(dialogSettings.exec_())