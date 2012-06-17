#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtCore, QtGui
from FrameSeparator import FrameSeparator
from DialogAddSpecialty import DialogAddSpecialty
from DataSql import DataSql

#**************************************************************************************************
# class: DialogNewTest
#**************************************************************************************************

class DialogNewTest(QtGui.QDialog):
    """
    Диалоговое окно создания/редактирования теста знаний
    """

    def __init__(self, title):
        QtGui.QDialog.__init__(self)
        self.__changeChair = False
        self.__changeAttestation = False
        self.__changeSpecialty = False
        # DataSql
        self.__dataSql = DataSql()
        # LineEdit
        self.__authorLineEdit = QtGui.QLineEdit()
        self.__authorLineEdit.setPlaceholderText(self.tr('Иванов Иван Иванович'))
        self.__subjectNameLineEdit = QtGui.QLineEdit()
        self.__subjectNameLineEdit.setPlaceholderText(self.tr('Математический анализ'))
        # ListView
        self.__specialtyListWidget = QtGui.QListWidget()
        # ComboBox
        self.__chairComboBox = QtGui.QComboBox()
        self.__chairComboBox.insertItem(0, self.tr('.::вбрать кафедру::.'))
        self.__chairComboBox.addItems(self._lstChair())

        self.__attestationComboBox = QtGui.QComboBox()
        self.__attestationComboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.__attestationComboBox.insertItem(0, self.tr('.::вбрать аттестацию::.'))
        self.__attestationComboBox.insertItem(1, self.tr('Аттестация №1'))
        self.__attestationComboBox.insertItem(2, self.tr('Аттестация №2'))
        self.__attestationComboBox.insertItem(3, self.tr('Аттестация №3'))
        # Icon
        self.__iconNewSpecialty = QtGui.QIcon()
        self.__iconNewSpecialty.addPixmap(QtGui.QPixmap('img/black/png/round_plus_icon&16.png'))

        self.__iconDeleteSpecialty = QtGui.QIcon()
        self.__iconDeleteSpecialty.addPixmap(QtGui.QPixmap('img/black/png/round_minus_icon&16.png'))

        self.__iconPrevSpecialty = QtGui.QIcon()
        self.__iconPrevSpecialty.addPixmap(QtGui.QPixmap('img/black/png/rnd_br_up_icon&16.png'))

        self.__iconNextSpecialty = QtGui.QIcon()
        self.__iconNextSpecialty.addPixmap(QtGui.QPixmap('img/black/png/rnd_br_down_icon&16.png'))
        # Button
        self.__buttonAddSpecialty = QtGui.QPushButton(self.__iconNewSpecialty, '')
        self.__buttonAddSpecialty.setToolTip(self.tr('Добавить специальность'))

        self.__buttonDeleteSpecialty = QtGui.QPushButton(self.__iconDeleteSpecialty, '')
        self.__buttonDeleteSpecialty.setToolTip(self.tr('Удалить выбранную специальность'))
        self.__buttonDeleteSpecialty.setEnabled(False)

        self.__buttonPrevSpecialty = QtGui.QPushButton(self.__iconPrevSpecialty, '')
        self.__buttonPrevSpecialty.setStatusTip(self.tr('Выбрать предыдущую специальность'))
        self.__buttonPrevSpecialty.setEnabled(False)

        self.__buttonNextSpecialty = QtGui.QPushButton(self.__iconNextSpecialty, '')
        self.__buttonNextSpecialty.setStatusTip(self.tr('Выбрать следующую специальность'))
        self.__buttonNextSpecialty.setEnabled(False)

        self.__specialtyButtonBox = QtGui.QDialogButtonBox(QtCore.Qt.Vertical)
        self.__specialtyButtonBox.addButton(self.__buttonAddSpecialty, QtGui.QDialogButtonBox.ActionRole)
        self.__specialtyButtonBox.addButton(self.__buttonDeleteSpecialty, QtGui.QDialogButtonBox.ActionRole)
        self.__specialtyButtonBox.addButton(self.__buttonPrevSpecialty, QtGui.QDialogButtonBox.ActionRole)
        self.__specialtyButtonBox.addButton(self.__buttonNextSpecialty, QtGui.QDialogButtonBox.ActionRole)

        self.__dialogButtonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        # Layout
        self.__layoutVChair = QtGui.QVBoxLayout()
        self.__layoutVChair.addWidget(QtGui.QLabel(self.tr('Выберите: кафедру по наименованию')))
        self.__layoutVChair.addWidget(self.__chairComboBox)
        self.__layoutVChair.addStretch(10)

        self.__layoutVContentLeft = QtGui.QVBoxLayout()
        self.__layoutVContentLeft.addWidget(QtGui.QLabel(self.tr('Введите: фамилию имя отчество')))
        self.__layoutVContentLeft.addWidget(self.__authorLineEdit)
        self.__layoutVContentLeft.addStretch(10)
        self.__layoutVContentLeft.addWidget(QtGui.QLabel(self.tr('Введите: наименование предмета')))
        self.__layoutVContentLeft.addWidget(self.__subjectNameLineEdit)
        self.__layoutVContentLeft.addStretch(10)
        self.__layoutVContentLeft.addWidget(QtGui.QLabel(self.tr('Выберите: номер аттестации')))
        self.__layoutVContentLeft.addWidget(self.__attestationComboBox)

        self.__layoutHContentRightContent = QtGui.QHBoxLayout()
        self.__layoutHContentRightContent.addWidget(self.__specialtyListWidget)
        self.__layoutHContentRightContent.addWidget(self.__specialtyButtonBox)

        self.__layoutVContentRight = QtGui.QVBoxLayout()
        self.__layoutVContentRight.addWidget(QtGui.QLabel(self.tr('Добавте: перечень специальностей')))
        self.__layoutVContentRight.addLayout(self.__layoutHContentRightContent)

        self.__layoutHContent = QtGui.QHBoxLayout()
        self.__layoutHContent.addLayout(self.__layoutVContentLeft)
        self.__layoutHContent.addLayout(self.__layoutVContentRight)

        self.__layoutVMain = QtGui.QVBoxLayout()
        self.__layoutVMain.addLayout(self.__layoutVChair)
        self.__layoutVMain.addLayout(self.__layoutHContent)
        self.__layoutVMain.addWidget(FrameSeparator(QtGui.QFrame.HLine, QtGui.QFrame.Sunken))
        self.__layoutVMain.addWidget(self.__dialogButtonBox)
        # Connect
        self.__chairComboBox.currentIndexChanged.connect(self._currentChangeChair)

        self.__attestationComboBox.currentIndexChanged.connect(self._currentChangedAttestation)

        self.__specialtyListWidget.itemSelectionChanged.connect(self._enabledButtonDelete)

        self.__buttonAddSpecialty.clicked.connect(self._addSpecialty)
        self.__buttonDeleteSpecialty.clicked.connect(self._deleteSpecialty)
        self.__buttonPrevSpecialty.clicked.connect(self._previousSpecialty)
        self.__buttonNextSpecialty.clicked.connect(self._nextSpecialty)

        self.__dialogButtonBox.accepted.connect(self._verification)
        self.__dialogButtonBox.rejected.connect(self.reject)
        # <<<Self>>>
        self.setLayout(self.__layoutVMain)
        self.setModal(True)
        self.setWindowTitle(title)
        self.setFocus()
        self.resize(self.width(), self.minimumHeight())

    def _verification(self):
        """
        Проверка правильности поступающих данных.
        """
        errorString = ''

        if not self.__chairComboBox.currentIndex():
            errorString += 'Выберите: кафедру\n'
        if not self.__authorLineEdit.text():
            errorString += 'Введите: фамилию имя отчество\n'
        if not self.__subjectNameLineEdit.text():
            errorString += 'Введите: наименование предмета\n'
        if not self.__attestationComboBox.currentIndex():
            errorString += 'Выберите: номер аттестации\n'
        if not self.__specialtyListWidget.count():
            errorString += 'Добавьте: перечень специальностей'

        if errorString:
            QtGui.QMessageBox.warning(self, self.tr('Внимание!'),
                self.tr(errorString))
            return

        self.accept()

    def _lstChair(self):
        """
        Получает список кафедр
        """
        queryChair = 'SELECT name FROM chair'
        lstChair = self.__dataSql._queryCreateDataOrChair(queryChair)

        if lstChair:
            return lstChair
        else:
            QtGui.QMessageBox.critical(self, self.tr('Ошибка'),
                self.tr('Критическая ошибка!\n'
                        'Необходимо обратиться к разработчику.'))
            return []

    def _chairComboBox(self): return self.__chairComboBox.currentIndex()

    def _authorLineEdit(self): return self.__authorLineEdit.text()

    def _subjectNameLineEdit(self): return self.__subjectNameLineEdit.text()

    def _attestationComboBox(self): return self.__attestationComboBox.currentIndex()

    def _specialtyListWidget(self):
        """
        Создание списка специальностей
        """
        items = self.__specialtyListWidget.findItems('*', QtCore.Qt.MatchWrap | QtCore.Qt.MatchWildcard)
        lstSpecialties = []
        for element in items:
            lstSpecialties.append(element.text())

        return lstSpecialties

    def _setChairComboBox(self, chair):
        self.__chairComboBox.setCurrentIndex(chair)
        self.__changeChair = False

    def _setAuthorLineEdit(self, author):
        self.__authorLineEdit.setText(author)

    def _setSubjectNameLineEdit(self, subjectName):
        self.__subjectNameLineEdit.setText(subjectName)

    def _setAttestationComboBox(self, attestation):
        self.__attestationComboBox.setCurrentIndex(attestation)
        self.__changeAttestation = False

    def _setSpecialtyListWidget(self, lstSpecialties):
        for element in lstSpecialties:
            item = QtGui.QListWidgetItem(element)
            item.setToolTip(element)
            self.__specialtyListWidget.addItem(item)

    def _isModified(self):
        if self.__changeChair:
            return True
        elif self.__authorLineEdit.isModified():
            return True
        elif self.__subjectNameLineEdit.isModified():
            return True
        elif self.__changeAttestation:
            return True
        elif self.__changeSpecialty:
            return True

        return False

    def _currentChangeChair(self):
        self.__changeChair = True
        print self.__chairComboBox.currentIndex()

    def _currentChangedAttestation(self):
        self.__changeAttestation = True

    def _currentChangedSpecialty(self):
        self.__changeSpecialty = True

    def _enabledButtonDelete(self):
        self.__buttonDeleteSpecialty.setEnabled(True)

    def _addSpecialty(self):
        self.__dialogAddSpecialty = DialogAddSpecialty(self.tr('Добавить специальность'))

        if self.__dialogAddSpecialty.exec_() == QtGui.QDialog.Accepted:
            stringItem = self.__dialogAddSpecialty._lineEditAutoComplete()

            if not self.__specialtyListWidget.findItems(stringItem, QtCore.Qt.MatchFixedString):
                item = QtGui.QListWidgetItem(stringItem)
                item.setToolTip(stringItem)
                self.__specialtyListWidget.addItem(item)
                self._currentChangedSpecialty()
            else:
                QtGui.QMessageBox.warning(self.window(), self.tr('DSTU-TestTemplate'),
                    self.tr('Специальность с таким названием уже существует.\nБудьте внимательны.'))

            if self.__specialtyListWidget.count() > 1:
                self.__buttonPrevSpecialty.setEnabled(True)
                self.__buttonNextSpecialty.setEnabled(True)

            self.__dialogAddSpecialty.destroy()

    def _deleteSpecialty(self):
        currentRow = self.__specialtyListWidget.currentRow()
        item = self.__specialtyListWidget.takeItem(currentRow)
        del item
        self._currentChangedSpecialty()

        if not self.__specialtyListWidget.count():
            self.__buttonDeleteSpecialty.setEnabled(False)

        if self.__specialtyListWidget.count() <= 1:
            self.__buttonPrevSpecialty.setEnabled(False)
            self.__buttonNextSpecialty.setEnabled(False)

    def _previousSpecialty(self):
        if self.__specialtyListWidget.currentRow() <= 0:
            self.__specialtyListWidget.setCurrentRow(self.__specialtyListWidget.count() - 1)
        else:
            self.__specialtyListWidget.setCurrentRow(self.__specialtyListWidget.currentRow() - 1)

    def _nextSpecialty(self):
        if self.__specialtyListWidget.currentRow() == (self.__specialtyListWidget.count() - 1):
            self.__specialtyListWidget.setCurrentRow(0)
        else:
            self.__specialtyListWidget.setCurrentRow(self.__specialtyListWidget.currentRow() + 1)


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    DataSql()._connectDataBase('sqlite/db_ztest.sqlite')
    QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('UTF-8'))
    dialogNewTest = DialogNewTest('Hellow World!')
    sys.exit(dialogNewTest.exec_())



