#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtCore, QtGui
from LineEditAutoComplete import LineEditAutoComplete
from DataSql import DataSql
from FrameSeparator import FrameSeparator

#**************************************************************************************************
# class: DialogAddSpecialty
#**************************************************************************************************

class DialogAddSpecialty(QtGui.QDialog):
    """
    Диалоговое окно добавления специальности
    """

    def __init__(self, title):
        QtGui.QDialog.__init__(self)
        # DataSql
        self.__dataSql = DataSql()
        # ComboBox
        self.__qualificationComboBox = QtGui.QComboBox()
        self.__qualificationComboBox.insertItem(0, self.tr('<<вбрать квалификацию>>'))
        self.__qualificationComboBox.insertItem(1, self.tr('Бакалавр'), 62)
        self.__qualificationComboBox.insertItem(2, self.tr('Дипломированный специалист'), 65)
        self.__qualificationComboBox.insertItem(3, self.tr('Магистр'), 68)
        # LineEditAutoComplete
        self.__lineEditAutoComplete = LineEditAutoComplete([])
        self.__lineEditAutoComplete.setEnabled(False)
        self.__lineEditAutoComplete.setPlaceholderText(self.tr('010101.68 Математика'))
        # Button
        self.__dialogButtonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        # Layout
        self.__layoutVMain = QtGui.QVBoxLayout()
        self.__layoutVMain.addWidget(QtGui.QLabel(self.tr('Выберите: уровень подготовки')))
        self.__layoutVMain.addWidget(self.__qualificationComboBox)
        self.__layoutVMain.addWidget(QtGui.QLabel(self.tr('Введите: номер специальности')))
        self.__layoutVMain.addWidget(self.__lineEditAutoComplete)
        self.__layoutVMain.addWidget(FrameSeparator(QtGui.QFrame.HLine, QtGui.QFrame.Sunken))
        self.__layoutVMain.addWidget(self.__dialogButtonBox)
        # Connect
        self.__qualificationComboBox.currentIndexChanged.connect(self._currentIndexChanged)
        self.__dialogButtonBox.accepted.connect(self._verification)
        self.__dialogButtonBox.rejected.connect(self.reject)
        # <<<Self>>>
        self.setLayout(self.__layoutVMain)
        self.setModal(True)
        self.setWindowTitle(title)

    def _verification(self):
        """
        Проверка правильности поступающих данных.
        """
        errorString = ''

        if not self.__qualificationComboBox.currentIndex():
            errorString += 'Выберите: уровень подготовки.\n'
        if not self.__lineEditAutoComplete.text():
            errorString += 'Введите: номер специальности.'
        else:
            stringLineEdit = self.__lineEditAutoComplete.text()

            if stringLineEdit[-1:] != '\n':
                errorString += 'Нет такой специальности.'

        if errorString:
            QtGui.QMessageBox.warning(self, self.tr('Внимание!'),
                self.tr(errorString))
            return

        # Удачное завершение работы диалогового окна
        self.accept()

    def _lstSpecialty(self, qualification):
        """
        Получает список специальностей
        """
        querySpecialty = 'SELECT code, type, name '\
                         'FROM specialty '\
                         'WHERE type LIKE %s'
        querySpecialty = querySpecialty.replace('%s', str(qualification))
        lstSpecialty = self.__dataSql._querySpecialty(querySpecialty)

        if lstSpecialty:
            return lstSpecialty
        else:
            QtGui.QMessageBox.critical(self, self.tr('Ошибка'),
                self.tr('Критическая ошибка!\n'
                        'Необходимо обратиться к разработчику.'))
            return []

    def _currentIndexChanged(self):
        """
        Генерация автодополнения по выбранной квалификации
        """
        self.__lineEditAutoComplete.clear()
        if self.__qualificationComboBox.currentIndex():
            lstSpecialty = self._lstSpecialty(
                self.__qualificationComboBox.itemData(self.__qualificationComboBox.currentIndex())
            )
            self.__lineEditAutoComplete._setModel(lstSpecialty)
            self.__lineEditAutoComplete.setEnabled(True)
            self.__lineEditAutoComplete.setFocus()
        else:
            self.__lineEditAutoComplete.setEnabled(False)

    def _lineEditAutoComplete(self): return self.__lineEditAutoComplete.text()[:-1]


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    DataSql()._connectDataBase('sqlite/db_ztest.sqlite')
    QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('UTF-8'))
    dialogAddSpecialty = DialogAddSpecialty(app.tr('Добавить специальность'))
    sys.exit(dialogAddSpecialty.exec_())
