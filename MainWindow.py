#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtCore, QtGui
from TreeWidgetTest import TreeWidgetTest
from Editor import Editor
from DialogNewTest import DialogNewTest
from ReadOrWriteFile import ReadOrWriteFile
from DataSql import DataSql

from Test import Test
from Question import Question
from Answer import Answer

#Todo Задать новый read and write setting
#Todo Обновление базы специальностей
#Todo Справка

#**************************************************************************************************
# class: MainWindow
#**************************************************************************************************

class MainWindow(QtGui.QMainWindow):
    """
    Главное окно
    """

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.__lstTests = []
        self.__lstQuestions = []
        self.__lstAnswers = []
        self.__dictImageQuestions = {}
        self.__dictImageAnswers = {}
        self.__document = QtGui.QTextDocument()
        self.__strCurrentFileName = ''
        self.__strTitle = 'TestTemplate'
        self.__strVersion = '2.0'
        # DataSql
        self.__dataSql = DataSql()
        self.__dataSql._connectDataBase('sqlite/db_specialties.sqlite')
        # TreeXml
        self.__treeXml = TreeWidgetTest()
        # Editor
        self.__editor = Editor()
        # DockWidget
        self.__descriptionDock = QtGui.QDockWidget(self.tr('Редактор'))
        self.__descriptionDock.setFeatures(QtGui.QDockWidget.DockWidgetClosable |
                                           QtGui.QDockWidget.DockWidgetMovable |
                                           QtGui.QDockWidget.DockWidgetFloatable |
                                           QtGui.QDockWidget.DockWidgetVerticalTitleBar)
        self.__descriptionDock.setWidget(self.__editor)
        # ReadOrWriteFile
        self.__readOrWriteFile = ReadOrWriteFile()
        # Button
        self.__buttonAddQuestion = QtGui.QPushButton(self.tr('Добавить вопрос'))
        self.__buttonAddQuestion.setEnabled(False)

        self.__buttonDeleteQuestion = QtGui.QPushButton(self.tr('Удалить вопрос'))
        self.__buttonDeleteQuestion.setEnabled(False)

        self.__buttonAddAnswer = QtGui.QPushButton(self.tr('Добавить ответ'))
        self.__buttonAddAnswer.setEnabled(False)

        self.__buttonDeleteAnswer = QtGui.QPushButton(self.tr('Удалить ответ'))
        self.__buttonDeleteAnswer.setEnabled(False)

        self.__buttonItemEdit = QtGui.QPushButton(self.tr('Редактировать'))
        self.__buttonItemEdit.setEnabled(False)
        # Layout
        self.__layoutVTree = QtGui.QVBoxLayout()
        self.__layoutVTree.addWidget(self.__buttonAddQuestion)
        self.__layoutVTree.addWidget(self.__buttonDeleteQuestion)
        self.__layoutVTree.addWidget(self.__buttonAddAnswer)
        self.__layoutVTree.addWidget(self.__buttonDeleteAnswer)
        self.__layoutVTree.addWidget(self.__buttonItemEdit)
        self.__layoutVTree.addStretch(10)

        self.__layoutHContent = QtGui.QHBoxLayout()
        self.__layoutHContent.addWidget(self.__treeXml)
        self.__layoutHContent.addLayout(self.__layoutVTree)
        # Functions
        self._createActions()
        self._createMenus()
        self._createToolBars()
        self._createContextMenuTreeWidget()
        self._createDockWindows()
        self._setVisibleWidgets(False)
        self._createStatusBar()
        self._readSettings()
        # Connect
        self.__treeXml.itemSelectionChanged.connect(self._treeItemSelection)

        self.__buttonAddQuestion.clicked.connect(self._addQuestion)
        self.__buttonDeleteQuestion.clicked.connect(self._deleteQuestion)

        self.__buttonAddAnswer.clicked.connect(self._addAnswer)
        self.__buttonDeleteAnswer.clicked.connect(self._deleteAnswer)

        self.__buttonItemEdit.clicked.connect(self._treeItemDoubleOrButtonClicked)
        # <<<Self>>>
        self.setWindowTitle('%s %s' % (self.__strTitle, self.__strVersion))
        self.setUnifiedTitleAndToolBarOnMac(True)

    def _createActions(self):
        # Action File
        self.__actionFileNew = QtGui.QAction(QtGui.QIcon('img/black/png/doc_new_icon&16.png'), self.tr('&Новый'),
            self, shortcut=QtGui.QKeySequence.New,
            statusTip=self.tr('Создать новый тест'), triggered=self._newTest)

        self.__actionFileOpen = QtGui.QAction(QtGui.QIcon('img/black/png/folder_icon&16.png'),
            self.tr('&Открыть'), self, shortcut=QtGui.QKeySequence.Open,
            statusTip=self.tr('Открыть тест'), triggered=self._openFile)

        self.__actionFileSave = QtGui.QAction(QtGui.QIcon('img/black/png/save_icon&16.png'),
            self.tr('&Сохранить'), self, shortcut=QtGui.QKeySequence.Save,
            statusTip=self.tr('Сохранить тест'), triggered=self._save)
        self.__actionFileSave.setEnabled(False)

        self.__actionFileSaveAs = QtGui.QAction(
            self.tr('&Сохранить как'), self, shortcut=QtGui.QKeySequence.SaveAs,
            triggered=self._saveAs)
        self.__actionFileSaveAs.setEnabled(False)

        #self.__actionFileClose = QtGui.QAction(QtGui.QIcon('img/black/png/app_window_cross&16.png'),
        #    self.tr('&Закрыть текущий тест'),
        #    self, shortcut=QtGui.QKeySequence.Close,
        #    triggered=self.reject)

        self.__actionFileExit = QtGui.QAction(
            self.tr('В&ыход'), self, shortcut=QtGui.QKeySequence.Quit,
            statusTip=self.tr('Выйти из программы'), triggered=self.close)
        # Action Edit
        self.__actionEditAddQuestion = QtGui.QAction(QtGui.QIcon('img/black/png/sq_plus_icon&16.png'),
            self.tr('&Добавить вопрос'), self,
            statusTip=self.tr('Добавить вопрос'), triggered=self._addQuestion)
        self.__actionEditAddQuestion.setEnabled(False)

        self.__actionEditDeleteQuestion = QtGui.QAction(QtGui.QIcon('img/black/png/sq_minus_icon&16.png'),
            self.tr('&Удалить выбранный вопрос'), self,
            statusTip=self.tr('Удалить выбранный вопрос'), triggered=self._deleteQuestion)
        self.__actionEditDeleteQuestion.setEnabled(False)

        self.__actionEditAddAnswer = QtGui.QAction(QtGui.QIcon('img/black/png/round_plus_icon&16.png'),
            self.tr('&Добавить ответ'), self,
            statusTip=self.tr('Добавить ответ'), triggered=self._addAnswer)
        self.__actionEditAddAnswer.setEnabled(False)

        self.__actionEditDeleteAnswer = QtGui.QAction(QtGui.QIcon('img/black/png/round_minus_icon&16.png'),
            self.tr('&Удалить выбранный ответ'), self,
            statusTip=self.tr('Удалить выбранный ответ'), triggered=self._deleteAnswer)
        self.__actionEditDeleteAnswer.setEnabled(False)

        self.__actionEditItem = QtGui.QAction(QtGui.QIcon('img/black/png/doc_edit_icon&16.png'),
            self.tr('&Редактировать'), self,
            statusTip=self.tr('Редактировать'), triggered=self._treeItemDoubleOrButtonClicked)
        self.__actionEditItem.setEnabled(False)
        # Action Help
        self.__actionHelpAbout = QtGui.QAction(self.tr('&О программе'), self,
            statusTip=self.tr('Показать информацию о программе'),
            triggered=self._about)
        # Action Dock
        self.__actionDockDescription = self.__descriptionDock.toggleViewAction()
        self.__actionDockDescription.setIcon(QtGui.QIcon('img/black/png/doc_edit_icon&16.png'))

    def _createMenus(self):
        fileMenu = self.menuBar().addMenu(self.tr('&Файл'))
        fileMenu.addAction(self.__actionFileNew)
        fileMenu.addAction(self.__actionFileOpen)
        fileMenu.addAction(self.__actionFileSave)
        fileMenu.addAction(self.__actionFileSaveAs)
        fileMenu.addSeparator()
        fileMenu.addAction(self.__actionFileExit)

        editMenu = self.menuBar().addMenu(self.tr('&Правка'))
        editMenu.addAction(self.__editor._actionEditUndo())
        editMenu.addAction(self.__editor._actionEditRedo())
        editMenu.addSeparator()
        editMenu.addAction(self.__editor._actionEditCut())
        editMenu.addAction(self.__editor._actionEditCopy())
        editMenu.addAction(self.__editor._actionEditPaste())
        editMenu.addSeparator()
        editMenu.addAction(self.__editor._actionEditSelectAll())
        editMenu.addSeparator()
        editMenu.addAction(self.__editor._actionEditItemEmpty())
        editMenu.addSeparator()
        editMenu.addAction(self.__actionEditAddQuestion)
        editMenu.addAction(self.__actionEditDeleteQuestion)
        editMenu.addSeparator()
        editMenu.addAction(self.__actionEditAddAnswer)
        editMenu.addAction(self.__actionEditDeleteAnswer)
        editMenu.addSeparator()
        editMenu.addAction(self.__actionEditItem)
        editMenu.addSeparator()

        self.__viewMenu = self.menuBar().addMenu(self.tr('&Вид'))
        self.__viewMenu.addAction(self.__descriptionDock.toggleViewAction())
        self.__viewMenu.addSeparator()

        insertMenu = self.menuBar().addMenu(self.tr('Вст&авка'))
        insertMenu.addAction(self.__editor._actionInsertImage())

        formatMenu = self.menuBar().addMenu(self.tr('Фо&рмат'))
        formatMenu.addAction(self.__editor._actionFormatBold())
        formatMenu.addAction(self.__editor._actionFormatItalic())
        formatMenu.addAction(self.__editor._actionFormatUnderline())
        formatMenu.addSeparator()
        formatMenu.addAction(self.__editor._actionFormatAlignLeft())
        formatMenu.addAction(self.__editor._actionFormatAlignCenter())
        formatMenu.addAction(self.__editor._actionFormatAlignRight())
        formatMenu.addAction(self.__editor._actionFormatAlignJustify())
        formatMenu.addSeparator()
        formatMenu.addAction(self.__editor._actionFormatColor())

        helpMenu = self.menuBar().addMenu(self.tr('&Помощь'))
        helpMenu.addAction(self.__actionHelpAbout)

    def _createToolBars(self):
        toolBar = self.addToolBar(self.tr('Панель инструментов'))
        toolBar.setMovable(False)
        toolBar.addAction(self.__actionFileNew)
        toolBar.addAction(self.__actionFileOpen)
        toolBar.addAction(self.__actionFileSave)
        toolBar.addSeparator()
        toolBar.addAction(self.__actionEditAddQuestion)
        toolBar.addAction(self.__actionEditDeleteQuestion)
        toolBar.addSeparator()
        toolBar.addAction(self.__actionEditAddAnswer)
        toolBar.addAction(self.__actionEditDeleteAnswer)
        toolBar.addSeparator()
        toolBar.addAction(self.__actionDockDescription)
        self.__viewMenu.addAction(toolBar.toggleViewAction())

    def _createContextMenuTreeWidget(self):
        self.__treeXml.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.__treeXml.addAction(self.__actionEditItem)
        self.__treeXml.addAction(self.__actionEditAddQuestion)
        self.__treeXml.addAction(self.__actionEditDeleteQuestion)
        self.__treeXml.addAction(self.__actionEditAddAnswer)
        self.__treeXml.addAction(self.__actionEditDeleteAnswer)

    def _createDockWindows(self):
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.__descriptionDock)

    def _createStatusBar(self):
        self.statusBar().showMessage(self.tr('Готово'))

    def _readSettings(self):
        settings = QtCore.QSettings('LevCorp', 'TestTemplate')
        pos = settings.value('pos', QtCore.QPoint(300, 100))
        size = settings.value('size', QtCore.QSize(800, 800))
        self.resize(size)
        self.move(pos)

    def _writeSettings(self):
        settings = QtCore.QSettings('LevCorp', 'TestTemplate')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def _setVisibleWidgets(self, bool):
        self.__treeXml.setVisible(bool)
        self.__buttonAddQuestion.setVisible(bool)
        self.__buttonDeleteQuestion.setVisible(bool)
        self.__buttonAddAnswer.setVisible(bool)
        self.__buttonDeleteAnswer.setVisible(bool)
        self.__buttonItemEdit.setVisible(bool)
        self.__descriptionDock.setVisible(bool)
        self.__actionEditAddQuestion.setEnabled(bool)
        self.__buttonAddQuestion.setEnabled(bool)

        if bool:
            self.__centralWidget = QtGui.QWidget()
            self.__centralWidget.setLayout(self.__layoutHContent)
            self.setCentralWidget(self.__centralWidget)
        else:
            label = QtGui.QLabel(self.tr('<h3>Нет открытых тестов</h3> '
                                         '<hr width="300" /> '
                                         '<ul type="square"> '
                                         '<li>Создать новый тест Ctrl+N  </li> '
                                         '<li>Открыть файл теста Ctrl+O</li> '
                                         '<li>Выйти из программы Ctrl+Q</li> '
                                         '</ul>'))
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.setCentralWidget(label)

    def _newTest(self):
        """
        Создание нового теста
        """
        if self._maybeSave(): # Если изменения сохранены либо их нет
            dialogNewTest = DialogNewTest(self.tr('Создание нового теста'))
            if dialogNewTest.exec_() == QtGui.QDialog.Accepted:
                self.__lstTests = []
                self.__lstQuestions = []
                self.__lstAnswers = []
                self.__treeXml.clear()
                self._setWindowTitle('')

                test = Test()
                test.author = dialogNewTest._authorLineEdit()
                test.subjectName = dialogNewTest._subjectNameLineEdit()
                test.attestation = dialogNewTest._attestationComboBox()
                test.lstSpecialties = dialogNewTest._specialtyListWidget()

                self.__lstTests.append(test)

                # _read([data], [], [])
                self.__treeXml._read(self.__lstTests, self.__lstQuestions, self.__lstAnswers)

                self._setVisibleWidgets(True)

                dialogNewTest.close()

    def _openFile(self):
        """
        Открыть тест
        """
        if self._maybeSave():
            fileName = QtGui.QFileDialog.getOpenFileName(self,
                self.tr('Открыть файл теста'), QtCore.QDir.homePath(),
                self.tr('ZTest файл (*.ztest)'))[0]

            if fileName:
                self._loadFile(fileName)

    def _loadFile(self, fileName):
        """
        Загрузка файлов
        """
        file = QtCore.QFile(fileName)

        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, self.tr(self.__strTitle),
                self.tr('Невозможно прочитать файл %s:\n%s.') % (fileName, file.errorString()))
            return

        if self.__readOrWriteFile._read(fileName):
            self.__lstTests = self.__readOrWriteFile._lstTests()
            self.__lstQuestions = self.__readOrWriteFile._lstQuestions()
            self.__lstAnswers = self.__readOrWriteFile._lstAnswers()
            self._setWindowTitle(file)
            self.statusBar().showMessage(self.tr('Файл загружен'), 2000)
        else:
            QtGui.QMessageBox.information(self.window(), self.tr(self.__strTitle),
                self.tr('Неверная структура файла.\nВозможно вы выбрали не тот файл.'))
            return False
        if not self.__treeXml._read(self.__lstTests, self.__lstQuestions, self.__lstAnswers):
            return False

        self._setVisibleWidgets(True)

        return True

    def _save(self):
        """
        Обработчик события triggered
        """
        if self.__strCurrentFileName:
            return self._saveFile(self.__strCurrentFileName)

        return self._saveAs()

    def _saveAs(self):
        """
        Сохранить как
        """
        fileName = QtGui.QFileDialog.getSaveFileName(self,
            self.tr('Сохранить файл теста'), QtCore.QDir.homePath(),
            self.tr('ZTest файл (*.ztest)'))[0]
        if fileName:
            return self._saveFile(fileName)

    def _saveFile(self, fileName):
        """
        Созранить файл
        """
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, self.tr(self.__strTitle),
                self.tr('Невозможно записать файл %s:\n%s.') % (fileName, file.errorString()))
            return False

        if self.__readOrWriteFile._create(
            fileName,
            self.__lstTests,
            self.__lstQuestions,
            self.__lstAnswers):
            self._setWindowTitle(file)
            self.statusBar().showMessage(self.tr('Файл сохранен'), 2000)
        else:
            return False

        return True

    def _maybeSave(self):
        """
        Проверить необходимость сохранения
        текущего документа
        """
        if self.isWindowModified():
            ret = QtGui.QMessageBox.warning(self, self.tr(self.__strTitle),
                self.tr('Тест был модифицирован.\nВы хотите сохранить '
                        'ваши изменения?'),
                QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                QtGui.QMessageBox.Cancel)
            if ret == QtGui.QMessageBox.Save:
                return self._save()
            elif ret == QtGui.QMessageBox.Cancel:
                return False
        return True

    def closeEvent(self, event):
        """
        Обработка события выхода из программы
        """
        if self._maybeSave():
            self._writeSettings()
            event.accept()
        else:
            event.ignore()

    def _about(self):
        """
        О программе
        """
        QtGui.QMessageBox.about(self, self.tr('О программе'),
            self.tr('Программа <u>TestTemplate</u> является частью '
                    'системы D-Test. Предназначенна для составления тестов и '
                    'их дальнейший экспорт.\n'
                    '<b><i>LevBravE</i></b>'))

    def _addQuestion(self):
        """
        Добавление вопроса
        """
        question = Question()
        question.document = QtGui.QTextDocument()

        self.__lstQuestions.append(question)
        self.__lstAnswers.append([])

        questionsIndex = len(self.__lstQuestions) - 1
        itemRoot = self.__treeXml.topLevelItem(0)

        if itemRoot:
            self.__treeXml._addQuestion(itemRoot, questionsIndex)

        self.setWindowModified(True)
        self.__actionFileSave.setEnabled(True)

    def _deleteQuestion(self):
        """
        Удаление вопроса
        """
        ret = QtGui.QMessageBox.warning(self, self.tr(self.__strTitle),
            self.tr('Вы действительно хотите удалить выбранный вопрос?'),
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)

        if ret == QtGui.QMessageBox.Ok:
            listItems = self.__treeXml.selectedItems()

            questionsIndex = int(listItems[0].text(1))

            self.__lstQuestions.pop(questionsIndex)
            self.__lstAnswers.pop(questionsIndex)

            self.__treeXml._deleteQuestion(questionsIndex, self.__lstQuestions)

            self.setWindowModified(True)
            self.__actionFileSave.setEnabled(True)

    def _addAnswer(self):
        """
        Добавить ответ
        """
        answer = Answer()
        answer.document = QtGui.QTextDocument()
        listItems = self.__treeXml.selectedItems()
        questionsIndex = int(listItems[0].text(1))

        self.__lstAnswers[questionsIndex].append(answer)

        answersIndex = len(self.__lstAnswers[questionsIndex]) - 1

        self.__treeXml._addAnswer(listItems[0], questionsIndex, answersIndex)
        self.__treeXml.setCurrentItem(listItems[0])

        self.setWindowModified(True)
        self.__actionFileSave.setEnabled(True)

    def _deleteAnswer(self):
        """
        Удалить ответ
        """
        ret = QtGui.QMessageBox.warning(self, self.tr(self.__strTitle),
            self.tr('Вы действительно хотите удалить выбранный ответ?'),
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)

        if ret == QtGui.QMessageBox.Ok:
            listItems = self.__treeXml.selectedItems()

            questionsIndex = int(listItems[0].text(1))
            answersIndex = int(listItems[0].text(2))

            self.__lstAnswers[questionsIndex].pop(answersIndex)
            parent = listItems[0].parent()
            lstAnswers = self.__lstAnswers[questionsIndex]

            self.__treeXml._deleteAnswer(parent, answersIndex, lstAnswers)

            self.setWindowModified(True)
            self.__actionFileSave.setEnabled(True)

    def _setWindowTitle(self, file):
        """
        Задать заголовок главному окну
        """
        if not self.__actionFileSaveAs.isEnabled():
            self.__actionFileSaveAs.setEnabled(True)

        if file:
            fileInfo = QtCore.QFileInfo(file)
            self.__strCurrentFileName = fileInfo.filePath()
            baseName = fileInfo.baseName()

            path = fileInfo.absoluteFilePath()

            self.setWindowTitle('%s[*] - [%s] - %s %s' % (baseName, path, self.__strTitle, self.__strVersion))

            self.setWindowModified(False)
            self.__actionFileSave.setEnabled(False)
        else:
            self.__strCurrentFileName = ''
            self.setWindowTitle('untitled[*] - TestTemplate 2.0')

            self.setWindowModified(True)
            self.__actionFileSave.setEnabled(True)

    def _readStyleSheet(self, fileName):
        """
        Загрузить файл стилей приложения
        """
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            return False
        self.setStyleSheet(str(file.readAll()))
        return True

    def _editorModified(self, bool):
        """
        Обработка события modificationChanged
        """
        if not self.isWindowModified() and bool:
            self.setWindowModified(True)
            self.__actionFileSave.setEnabled(True)

        listItems = self.__treeXml.selectedItems()
        # Selected Question
        if not listItems[0].text(2):
            flagType = True
            questionsIndex = int(listItems[0].text(1))

            question = self.__lstQuestions[questionsIndex]

            flagEmpty = question.document.toPlainText()
            self.__treeXml._setTextTreeItem(listItems[0], questionsIndex, flagType, flagEmpty)
        # Selected Answer
        else:
            flagType = False
            questionsIndex = int(listItems[0].text(1))
            answersIndex = int(listItems[0].text(2))

            answer = self.__lstAnswers[questionsIndex][answersIndex]
            #title = u'%s --> %s' % (listItems[0].parent().text(0), listItems[0].text(0))

            #if answer.right:
            #    self.__editor._setRight(QtCore.Qt.Checked)
            #else:
            #    self.__editor._setRight(QtCore.Qt.Unchecked)

            #answer.right = self.__editor._right()

            flagEmpty = answer.document.toPlainText()
            self.__treeXml._setTextTreeItem(listItems[0], answersIndex, flagType, flagEmpty)
            self.__treeXml._setIconTreeItem(listItems[0], answer.right)

    def _treeItemSelection(self):
        """
        Обработка события Selection
        """
        listItems = self.__treeXml.selectedItems()

        try:
            # Question
            if not listItems[0].text(2) and self.__treeXml.indexOfTopLevelItem(listItems[0]):
                # Action
                self.__actionEditDeleteQuestion.setEnabled(True)
                self.__actionEditAddAnswer.setEnabled(True)
                self.__actionEditDeleteAnswer.setEnabled(False)
                # Button
                self.__buttonDeleteQuestion.setEnabled(True)
                self.__buttonAddAnswer.setEnabled(True)
                self.__buttonDeleteAnswer.setEnabled(False)
                # Main
                questionIndex = int(listItems[0].text(1))
                document = self.__lstQuestions[questionIndex].document
                document.modificationChanged.connect(self._editorModified)
                self.__editor._setDocument(document)
            # Answer
            elif listItems[0].text(2):
                # Action
                self.__actionEditDeleteQuestion.setEnabled(False)
                self.__actionEditAddAnswer.setEnabled(False)
                self.__actionEditDeleteAnswer.setEnabled(True)
                # Button
                self.__buttonDeleteQuestion.setEnabled(False)
                self.__buttonAddAnswer.setEnabled(False)
                self.__buttonDeleteAnswer.setEnabled(True)
                # TextEdit
                questionIndex = int(listItems[0].text(1))
                answerIndex = int(listItems[0].text(2))
                document = self.__lstAnswers[questionIndex][answerIndex].document
                self.__editor._setDocument(document)
            # Root
            else:
                # Action
                self.__actionEditDeleteQuestion.setEnabled(False)
                self.__actionEditAddAnswer.setEnabled(False)
                self.__actionEditDeleteAnswer.setEnabled(False)
                # Button
                self.__buttonDeleteQuestion.setEnabled(False)
                self.__buttonAddAnswer.setEnabled(False)
                self.__buttonDeleteAnswer.setEnabled(False)
        except IndexError:
            pass
        self.__actionEditItem.setEnabled(True)
        self.__buttonItemEdit.setEnabled(True)
        #index = listItems[0].parent().indexOfChild(listItems[0])

    def _treeItemDoubleOrButtonClicked(self):
        """
        Обработка события DoubleClicked
        """
        listItems = self.__treeXml.selectedItems()

        try:
            if not self.__treeXml.indexOfTopLevelItem(listItems[0]):
                dialogNewTest = DialogNewTest(self.tr('Редактирование теста'))
                dialogNewTest._setAuthorLineEdit(self.__lstTests[0].author)
                dialogNewTest._setSubjectNameLineEdit(self.__lstTests[0].subjectName)
                dialogNewTest._setAttestationComboBox(int(self.__lstTests[0].attestation))
                dialogNewTest._setSpecialtyListWidget(self.__lstTests[0].lstSpecialties)

                if dialogNewTest.exec_() == QtGui.QDialog.Accepted:
                    if dialogNewTest._isModified():
                        self.__lstTests = []

                        test = Test()
                        test.author = dialogNewTest._authorLineEdit()
                        test.subjectName = dialogNewTest._subjectNameLineEdit()
                        test.attestation = dialogNewTest._attestationComboBox()
                        test.lstSpecialties = dialogNewTest._specialtyListWidget()

                        self.__lstTests.append(test)
                        self.__treeXml._read(self.__lstTests, self.__lstQuestions, self.__lstAnswers)
                        self.setWindowModified(True)
                        self.__actionFileSave.setEnabled(True)

                    dialogNewTest.close()
        except IndexError:
            pass