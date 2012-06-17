#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtCore, QtGui
from TreeWidgetTest import TreeWidgetTest
from Editor import Editor
from DialogNewTest import DialogNewTest
from DialogDBUpdate import DialogDBUpdate
from DialogSettings import DialogSettings
from DialogHelpTopics import DialogHelpTopics
from ReadOrWriteFile import ReadOrWriteFile
from AnimationLabel import AnimationLabel
from ClickableLabel import ClickableLabel
from SynchronizationThread import SynchronizationThread
from DataSql import DataSql

from Test import Test
from Question import Question
from Answer import Answer

#Todo Обновление базы данных приложения
#TODO Реализовать отправление тестов на сервер
#TODO Завершить внешний вид страницы "Приветствия"
#TODO Улучшить окно "О программе"
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
        self.__APPLICATION_CORP = 'LevCorp'
        self.__APPLICATION_NAME = 'zTest'
        self.__VERSION = '1.0'
        self.__MAX_RECENT_FILES = 5
        # Thread
        self.__synchronizationThread = SynchronizationThread()
        # Timer
        self.__synchronizationTimer = QtCore.QTimer()
        # DataSql
        self.__dataSql = DataSql()
        self.__dataSql._connectDataBase('sqlite/db_ztest.sqlite')
        # Label
        # bug in qt 4.7.4 при прямой загрузке отдельных png файлов
        self.__imageHeadLabel = QtGui.QLabel()
        self.__imageHeadLabel.setPixmap('img/head_image.jpg')
        self.__imageHeadLabel.setAlignment(QtCore.Qt.AlignTop)

        self.__quickStartLabel = QtGui.QLabel(self.tr('<h1 style="color: indigo"><b>Быстрый старт</b></h1>'))

        strStyleSheetLabelButton = 'QLabel { padding: 5px; } '\
                                   'QLabel:hover { background: gainsboro; }'

        strStyleSheetLabelIcon = 'QLabel { padding: 5px; }'

        self.__newTestLabel = ClickableLabel(self.tr('<h3 style="color: indigo"><u>Создать новый тест</u></h3>'))
        self.__newTestLabel.setCursor(QtCore.Qt.PointingHandCursor)
        self.__newTestDescLabel = QtGui.QLabel(self.tr('Создание нового теста'))
        self.__newTestButtonLabel = ClickableLabel()
        self.__newTestButtonLabel.setPixmap('img/new_test48x48.png')
        self.__newTestButtonLabel.setCursor(QtCore.Qt.PointingHandCursor)
        self.__newTestButtonLabel.setStyleSheet(strStyleSheetLabelButton)

        self.__openTestLabel = ClickableLabel(self.tr('<h3 style="color: indigo"><u>Открыть тест</u></h3>'))
        self.__openTestLabel.setCursor(QtCore.Qt.PointingHandCursor)
        self.__openTestDescLabel = QtGui.QLabel(self.tr('Открыть существующий файл теста'))
        self.__openTestButtonLabel = ClickableLabel()
        self.__openTestButtonLabel.setPixmap('img/open_test48x48.png')
        self.__openTestButtonLabel.setCursor(QtCore.Qt.PointingHandCursor)
        self.__openTestButtonLabel.setStyleSheet(strStyleSheetLabelButton)

        self.__documentationLabel = QtGui.QLabel(self.tr('<h1 style="color: indigo"><b>Документация</b></h1>'))

        self.__readHelpLabel = ClickableLabel(self.tr('<h3 style="color: indigo"><u>Справка</u></h3>'))
        self.__readHelpLabel.setCursor(QtCore.Qt.PointingHandCursor)
        self.__readHelpDescLabel = QtGui.QLabel(self.tr('Читать справку'))
        self.__readHelpButtonLabel = ClickableLabel()
        self.__readHelpButtonLabel.setPixmap('img/read_help48x48.png')
        self.__readHelpButtonLabel.setCursor(QtCore.Qt.PointingHandCursor)
        self.__readHelpButtonLabel.setStyleSheet(strStyleSheetLabelButton)

        self.__recentLabel = QtGui.QLabel(self.tr('<h1 style="color: indigo"><b>Недавние тесты</b></h1>'))

        self.__lstLabelFileRecent = []
        for index in range(self.__MAX_RECENT_FILES):
            self.__lstLabelFileRecent.append(ClickableLabel())
            self.__lstLabelFileRecent[index].setCursor(QtCore.Qt.PointingHandCursor)
            self.__lstLabelFileRecent[index].clicked.connect(self._openRecentFile)
            self.__lstLabelFileRecent[index].setVisible(False)

        self.__recentTestIconLabel = QtGui.QLabel()
        self.__recentTestIconLabel.setAlignment(QtCore.Qt.AlignTop)
        self.__recentTestIconLabel.setPixmap('img/recent_test48x48.png')
        self.__recentTestIconLabel.setStyleSheet(strStyleSheetLabelIcon)

        self.__statusDstuTest = QtGui.QLabel()
        self.__statusDstuTest.setAlignment(QtCore.Qt.AlignHCenter)
        self.__statusDstuTest.setTextInteractionFlags(
            self.__statusDstuTest.textInteractionFlags() | QtCore.Qt.LinksAccessibleByMouse)
        self.__statusDstuTest.setOpenExternalLinks(True)
        # AnimationLabel
        self.__synchronizationAnimationLabel = AnimationLabel('img/loader_refresh.gif')
        # TreeXml
        self.__treeXml = TreeWidgetTest()
        # Editor
        self.__editor = Editor()
        # DockWidget
        self.__editorDock = QtGui.QDockWidget(self.tr('Редактор'))
        self.__editorDock.setFeatures(QtGui.QDockWidget.DockWidgetClosable |
                                      QtGui.QDockWidget.DockWidgetMovable |
                                      QtGui.QDockWidget.DockWidgetFloatable)
        self.__editorDock.setWidget(self.__editor)
        # ReadOrWriteFile
        self.__readOrWriteFile = ReadOrWriteFile()
        # Layout
        # Not open test
        # New Test block (start)
        self.__layoutVLabelsNewTest = QtGui.QVBoxLayout()
        self.__layoutVLabelsNewTest.addWidget(self.__newTestLabel)
        self.__layoutVLabelsNewTest.addWidget(self.__newTestDescLabel)
        self.__layoutVLabelsNewTest.addStretch(10)

        self.__layoutHNewTest = QtGui.QHBoxLayout()
        self.__layoutHNewTest.addWidget(self.__newTestButtonLabel)
        self.__layoutHNewTest.addLayout(self.__layoutVLabelsNewTest)
        self.__layoutHNewTest.addStretch(10)
        # New Test block (end)
        # Open Test block (start)
        self.__layoutVLabelsOpenTest = QtGui.QVBoxLayout()
        self.__layoutVLabelsOpenTest.addWidget(self.__openTestLabel)
        self.__layoutVLabelsOpenTest.addWidget(self.__openTestDescLabel)
        self.__layoutVLabelsOpenTest.addStretch(10)

        self.__layoutHOpenTest = QtGui.QHBoxLayout()
        self.__layoutHOpenTest.addWidget(self.__openTestButtonLabel)
        self.__layoutHOpenTest.addLayout(self.__layoutVLabelsOpenTest)
        self.__layoutHOpenTest.addStretch(10)
        # Open Test block (end)
        # Read help block (start)
        self.__layoutVLabelsReadHelp = QtGui.QVBoxLayout()
        self.__layoutVLabelsReadHelp.addWidget(self.__readHelpLabel)
        self.__layoutVLabelsReadHelp.addWidget(self.__readHelpDescLabel)
        self.__layoutVLabelsReadHelp.addStretch(10)

        self.__layoutHReadHelp = QtGui.QHBoxLayout()
        self.__layoutHReadHelp.addWidget(self.__readHelpButtonLabel)
        self.__layoutHReadHelp.addLayout(self.__layoutVLabelsReadHelp)
        self.__layoutHReadHelp.addStretch(10)
        # Read help block (end)
        # Recent Test block (start)
        self.__layoutVLabelsRecentTest = QtGui.QVBoxLayout()
        for labelItem in self.__lstLabelFileRecent:
            self.__layoutVLabelsRecentTest.addWidget(labelItem)
        self.__layoutVLabelsRecentTest.addStretch(10)

        self.__layoutHRecentTest = QtGui.QHBoxLayout()
        self.__layoutHRecentTest.addWidget(self.__recentTestIconLabel)
        self.__layoutHRecentTest.addLayout(self.__layoutVLabelsRecentTest)
        self.__layoutHRecentTest.addStretch(10)
        # Recent Test block (end)
        self.__layoutVQuickStart = QtGui.QVBoxLayout()
        self.__layoutVQuickStart.addWidget(self.__quickStartLabel)
        self.__layoutVQuickStart.addLayout(self.__layoutHNewTest)
        self.__layoutVQuickStart.addLayout(self.__layoutHOpenTest)

        self.__layoutVDocumentation = QtGui.QVBoxLayout()
        self.__layoutVDocumentation.addWidget(self.__documentationLabel)
        self.__layoutVDocumentation.addLayout(self.__layoutHReadHelp)
        self.__layoutVDocumentation.addStretch(10)

        self.__layoutVRecent = QtGui.QVBoxLayout()
        self.__layoutVRecent.addWidget(self.__recentLabel)
        self.__layoutVRecent.addLayout(self.__layoutHRecentTest)

        self.__layoutHTagsMain = QtGui.QHBoxLayout()
        self.__layoutHTagsMain.addLayout(self.__layoutVQuickStart)
        self.__layoutHTagsMain.addLayout(self.__layoutVDocumentation)

        self.__layoutVTagsMain = QtGui.QVBoxLayout()
        self.__layoutVTagsMain.addLayout(self.__layoutHTagsMain)
        self.__layoutVTagsMain.addLayout(self.__layoutVRecent)

        self.__layoutVMain = QtGui.QVBoxLayout()
        self.__layoutVMain.addWidget(self.__imageHeadLabel)
        self.__layoutVMain.addLayout(self.__layoutVTagsMain)
        self.__layoutVMain.addStretch(10)
        # Open test
        self.__layoutHContent = QtGui.QHBoxLayout()
        self.__layoutHContent.addWidget(self.__treeXml)
        self.__layoutHContent.setContentsMargins(0, 0, 0, 0)
        # Widget
        self.__centralWidgetNotOpenTest = QtGui.QWidget()
        self.__centralWidgetNotOpenTest.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.__centralWidgetNotOpenTest.setLayout(self.__layoutVMain)

        self.__centralWidgetOpenTest = QtGui.QWidget()
        self.__centralWidgetOpenTest.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.__centralWidgetOpenTest.setLayout(self.__layoutHContent)
        # StackedWidget
        self.__stackedWidget = QtGui.QStackedWidget()
        self.__stackedWidget.addWidget(self.__centralWidgetNotOpenTest)
        self.__stackedWidget.addWidget(self.__centralWidgetOpenTest)
        # Functions
        self._createActions()
        self._createToolBars()
        self._createMenus()
        self._updateRecentFileActions()
        self._createContextMenuTreeWidget()
        self._createDockWindows()
        self._setVisibleWidgets(False)
        self._createStatusBar()
        self._synchronizationServer()
        self._readSettings()
        # Connect
        self.__synchronizationTimer.timeout.connect(self._synchronizationAutoServer)

        self.__synchronizationThread.finished.connect(self._checkAvailabilityServer)

        self.__newTestLabel.clicked.connect(self._newTest)
        self.__newTestButtonLabel.clicked.connect(self._newTest)

        self.__openTestLabel.clicked.connect(self._openTest)
        self.__openTestButtonLabel.clicked.connect(self._openTest)

        self.__readHelpLabel.clicked.connect(self._helpTopics)
        self.__readHelpButtonLabel.clicked.connect(self._helpTopics)

        self.__treeXml.itemSelectionChanged.connect(self._treeItemSelection)

        self.__editor._checkBox().clicked.connect(self._currentStateChanged)
        # Timer every 1 min
        self.__synchronizationTimer.start(60000)
        # <<<Self>>>
        self.setWindowTitle('%s %s' % (self.__APPLICATION_NAME, self.__VERSION))
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.setCentralWidget(self.__stackedWidget)

    def _createActions(self):
        # Action File
        self.__actionFileNew = QtGui.QAction(QtGui.QIcon('img/black/png/doc_new_icon&16.png'), self.tr('&Новый'),
            self, shortcut=QtGui.QKeySequence.New,
            statusTip=self.tr('Новый тест'), triggered=self._newTest)

        self.__actionFileOpen = QtGui.QAction(QtGui.QIcon('img/black/png/folder_icon&16.png'),
            self.tr('&Открыть'), self, shortcut=QtGui.QKeySequence.Open,
            statusTip=self.tr('Открыть тест'), triggered=self._openTest)

        self.__actionFileSave = QtGui.QAction(QtGui.QIcon('img/black/png/save_icon&16.png'),
            self.tr('&Сохранить'), self, shortcut=QtGui.QKeySequence.Save,
            statusTip=self.tr('Сохранить тест'), triggered=self._save)

        self.__actionFileSaveAs = QtGui.QAction(
            self.tr('&Сохранить как'), self, shortcut=QtGui.QKeySequence.SaveAs,
            triggered=self._saveAs)

        self.__lstActionFileRecent = []

        for index in range(self.__MAX_RECENT_FILES):
            self.__lstActionFileRecent.append(QtGui.QAction(
                self, visible=False, triggered=self._openRecentFile))

        self.__actionFileClose = QtGui.QAction(
            self.tr('&Закрыть текущий тест'), self, shortcut=QtGui.QKeySequence.Close,
            triggered=self._closeCurrentTest)

        self.__actionFileSettings = QtGui.QAction(QtGui.QIcon('img/black/png/wrench_plus_2_icon&16.png'),
            self.tr('&Настройки'), self, shortcut='Ctrl+Alt+S',
            statusTip=self.tr('Настройки приложения'), triggered=self._settingsApp)

        self.__actionFileSynchronization = QtGui.QAction(QtGui.QIcon('img/black/png/refresh_icon&16.png'),
            self.tr('&Синхронизация'), self, shortcut='Ctrl+Alt+Y',
            statusTip=self.tr('Синхронизация с сервером'), triggered=self._synchronizationServer)

        self.__actionFileDBUpdate = QtGui.QAction(QtGui.QIcon('img/black/png/db_icon&16.png'),
            self.tr('&Обновление базы данных'), self, shortcut='Ctrl+Alt+U',
            statusTip=self.tr('Обновление базы данных специальностей'), triggered=self._updateDBApp)

        self.__actionFileExit = QtGui.QAction(
            self.tr('В&ыход'), self, shortcut=QtGui.QKeySequence.Quit,
            statusTip=self.tr('Выйти из программы'), triggered=self.close)
        # Action Edit
        self.__actionEditAddQuestion = QtGui.QAction(QtGui.QIcon('img/black/png/sq_plus_icon&16.png'),
            self.tr('&Добавить вопрос'), self, shortcut='Ctrl+W',
            statusTip=self.tr('Добавить вопрос'), triggered=self._addQuestion)

        self.__actionEditDeleteQuestion = QtGui.QAction(QtGui.QIcon('img/black/png/sq_minus_icon&16.png'),
            self.tr('&Удалить вопрос'), self, shortcut='Ctrl+D',
            statusTip=self.tr('Удалить выбранный вопрос'), triggered=self._deleteQuestion)

        self.__actionEditAddAnswer = QtGui.QAction(QtGui.QIcon('img/black/png/round_plus_icon&16.png'),
            self.tr('&Добавить ответ'), self, shortcut='Ctrl+Alt+W',
            statusTip=self.tr('Добавить ответ'), triggered=self._addAnswer)

        self.__actionEditDeleteAnswer = QtGui.QAction(QtGui.QIcon('img/black/png/round_minus_icon&16.png'),
            self.tr('&Удалить ответ'), self, shortcut='Ctrl+Alt+D',
            statusTip=self.tr('Удалить выбранный ответ'), triggered=self._deleteAnswer)

        self.__actionTestParameters = QtGui.QAction(
            self.tr('&Параметры теста'), self,
            statusTip=self.tr('Параметры теста'), triggered=self._editTestParameters)
        # Action Help
        self.__actionHelpTopics = QtGui.QAction(QtGui.QIcon('img/help.png'),
            self.tr('&Справка'), self, shortcut=QtGui.QKeySequence.HelpContents,
            statusTip=self.tr('Справочная информация по программе'), triggered=self._helpTopics)

        self.__actionHelpAbout = QtGui.QAction(
            self.tr('&О программе'), self,
            statusTip=self.tr('Показать информацию о программе'),
            triggered=self._about)
        # Action Dock
        self.__actionDockDescription = self.__editorDock.toggleViewAction()
        self.__actionDockDescription.setIcon(QtGui.QIcon('img/black/png/doc_edit_icon&16.png'))

    def _createToolBars(self):
        self.__toolBar = self.addToolBar(self.tr('Панель инструментов'))
        self.__toolBar.setMovable(False)
        self.__toolBar.addAction(self.__actionFileNew)
        self.__toolBar.addAction(self.__actionFileOpen)
        self.__toolBar.addAction(self.__actionFileSave)
        self.__toolBar.addSeparator()
        self.__toolBar.addAction(self.__actionEditAddQuestion)
        self.__toolBar.addAction(self.__actionEditDeleteQuestion)
        self.__toolBar.addSeparator()
        self.__toolBar.addAction(self.__actionEditAddAnswer)
        self.__toolBar.addAction(self.__actionEditDeleteAnswer)
        self.__toolBar.addSeparator()
        self.__toolBar.addAction(self.__actionDockDescription)
        self.__toolBar.addSeparator()
        self.__toolBar.addAction(self.__actionFileSettings)
        self.__toolBar.addSeparator()
        self.__toolBar.addAction(self.__actionFileSynchronization)
        self.__toolBar.addSeparator()
        self.__toolBar.addAction(self.__actionFileDBUpdate)
        self.__toolBar.addSeparator()
        self.__toolBar.addAction(self.__actionHelpTopics)

    def _createMenus(self):
        fileMenu = self.menuBar().addMenu(self.tr('&Файл'))
        fileMenu.addAction(self.__actionFileNew)
        fileMenu.addAction(self.__actionFileOpen)
        fileMenu.addAction(self.__actionFileSave)
        fileMenu.addAction(self.__actionFileSaveAs)
        fileMenu.addAction(self.__actionFileClose)
        fileMenu.addSeparator()
        for actionItem in self.__lstActionFileRecent:
            fileMenu.addAction(actionItem)
        fileMenu.addSeparator()
        fileMenu.addAction(self.__actionFileSettings)
        fileMenu.addSeparator()
        fileMenu.addAction(self.__actionFileSynchronization)
        fileMenu.addSeparator()
        fileMenu.addAction(self.__actionFileDBUpdate)
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
        editMenu.addAction(self.__actionTestParameters)
        editMenu.addSeparator()

        self.__viewMenu = self.menuBar().addMenu(self.tr('&Вид'))
        self.__viewMenu.addAction(self.__editorDock.toggleViewAction())
        self.__viewMenu.addSeparator()
        self.__viewMenu.addAction(self.__toolBar.toggleViewAction())

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
        helpMenu.addAction(self.__actionHelpTopics)
        helpMenu.addSeparator()
        helpMenu.addAction(self.__actionHelpAbout)

    def _createContextMenuTreeWidget(self):
        self.__treeXml.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.__treeXml.addAction(self.__actionEditAddQuestion)
        self.__treeXml.addAction(self.__actionEditDeleteQuestion)
        self.__treeXml.addAction(self.__actionEditAddAnswer)
        self.__treeXml.addAction(self.__actionEditDeleteAnswer)
        self.__treeXml.addAction(self.__actionTestParameters)

    def _createDockWindows(self):
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.__editorDock)

    def _createStatusBar(self):
        self.statusBar().showMessage(self.tr('Готово'))
        self.statusBar().addPermanentWidget(self.__synchronizationAnimationLabel)
        self.statusBar().addPermanentWidget(self.__statusDstuTest)

    def _synchronizationAutoServer(self):
        settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
        addressServer = settings.value('addressServer', 'http://dstutest.local/')

        self.__synchronizationThread._setHostName('%sxmlrpc/' % addressServer)
        self.__synchronizationThread.start()

    def _synchronizationServer(self):
        settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
        addressServer = settings.value('addressServer', 'http://dstutest.local/')

        self.__synchronizationThread._setHostName('%sxmlrpc/' % addressServer)
        self.__synchronizationThread.start()
        self.__synchronizationAnimationLabel._start()

    def _checkAvailabilityServer(self):
        self.__synchronizationAnimationLabel._stop()

        if self.__synchronizationThread._response() == 100:
            strStatusDstuLabel = '<p style="font-size: 12px"> '\
                                 '<img width="11" height="11" src="img/circle_green.png"> '\
                                 '<a href="http://google.ru/">DstuTest</a></p>'
            self.__statusDstuTest.setText(strStatusDstuLabel)
            self.__statusDstuTest.setToolTip(self.tr('Сервер DstuTest, доступен'))

            return True
        else:
            strStatusDstuLabel = '<p style="font-size: 12px"> '\
                                 '<img width="11" height="11" src="img/circle_red.png"> '\
                                 'DstuTest</p>'
            self.__statusDstuTest.setText(strStatusDstuLabel)
            self.__statusDstuTest.setToolTip(self.tr('Сервер DstuTest, недоступен'))

            return False

    def _readSettings(self):
        settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
        pos = settings.value('pos', QtCore.QPoint(200, 100))
        size = settings.value('size', QtCore.QSize(960, 500))

        self.resize(size)
        self.move(pos)

    def _writeSettings(self):
        settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def _setVisibleWidgets(self, bool):
        # Visible
        self.__toolBar.setVisible(bool)
        self.__editorDock.setVisible(bool)
        self.__editor._checkBox().setVisible(False)
        # Enabled
        self.__editorDock.toggleViewAction().setEnabled(bool)
        self.__toolBar.toggleViewAction().setEnabled(bool)

        self.__actionFileSaveAs.setEnabled(bool)
        self.__actionTestParameters.setEnabled(bool)
        self.__actionEditAddQuestion.setEnabled(bool)
        self.__actionFileClose.setEnabled(bool)
        self.__actionEditDeleteQuestion.setEnabled(False)
        self.__actionEditAddAnswer.setEnabled(False)
        self.__actionEditDeleteAnswer.setEnabled(False)
        self.__actionFileSave.setEnabled(False)

        self.__editor._actionEditPaste().setEnabled(bool)
        self.__editor._actionEditSelectAll().setEnabled(bool)
        self.__editor._actionEditItemEmpty().setEnabled(bool)
        self.__editor._actionFormatBold().setEnabled(bool)
        self.__editor._actionFormatItalic().setEnabled(bool)
        self.__editor._actionFormatUnderline().setEnabled(bool)
        self.__editor._actionFormatAlignLeft().setEnabled(bool)
        self.__editor._actionFormatAlignCenter().setEnabled(bool)
        self.__editor._actionFormatAlignRight().setEnabled(bool)
        self.__editor._actionFormatAlignJustify().setEnabled(bool)
        self.__editor._actionFormatColor().setEnabled(bool)
        self.__editor._actionInsertImage().setEnabled(bool)
        self.__editor._actionEditUndo().setEnabled(False)
        self.__editor._actionEditRedo().setEnabled(False)
        self.__editor._actionEditCut().setEnabled(False)
        self.__editor._actionEditCopy().setEnabled(False)

        self._updateRecentFileLabels(bool)
        self.setWindowModified(False)

        if bool:
            self.__editor._clear()
            self.__editor._setDocument(QtGui.QTextDocument())
            self.__stackedWidget.setCurrentIndex(1)
        else:
            self.setWindowTitle('%s %s' % (self.__APPLICATION_NAME, self.__VERSION))

            self.__stackedWidget.setCurrentIndex(0)

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
                test.chair = dialogNewTest._chairComboBox()
                test.author = dialogNewTest._authorLineEdit()
                test.subjectName = dialogNewTest._subjectNameLineEdit()
                test.attestation = dialogNewTest._attestationComboBox()
                test.lstSpecialties = dialogNewTest._specialtyListWidget()

                self.__lstTests.append(test)

                # _read([data], [], [])
                self.__treeXml._read(self.__lstTests, self.__lstQuestions, self.__lstAnswers)

                self._setVisibleWidgets(True)
                self.setWindowModified(True)
                self.__actionFileSave.setEnabled(True)

                dialogNewTest.close()

    def _openTest(self):
        """
        Открыть тест
        """
        if self._maybeSave():
            fileName = QtGui.QFileDialog.getOpenFileName(self,
                self.tr('Открыть файл теста'), QtCore.QDir.homePath(),
                self.tr('ZTest файл (*.ztest)'))[0]

            if fileName:
                self._loadFile(fileName)

    def _openRecentFile(self):
        obj = self.sender()

        if obj:
            self._loadFile(obj.data())

    def _loadFile(self, fileName):
        """
        Загрузка файлов
        """
        file = QtCore.QFile(fileName)

        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, self.tr('Внимание'),
                self.tr('Невозможно прочитать файл %s:\n%s.') % (fileName, file.errorString()))
            return

        ok = self.__readOrWriteFile._read(fileName)

        if ok == 2:
            QtGui.QMessageBox.information(self.window(), self.tr('Информация'),
                self.tr('Версия выбранного файла *.ztest\nданным приложением не поддерживается.'))
            return False
        elif ok:
            self.__lstTests = self.__readOrWriteFile._lstTests()
            self.__lstQuestions = self.__readOrWriteFile._lstQuestions()
            self.__lstAnswers = self.__readOrWriteFile._lstAnswers()
            self._setWindowTitle(file)
            self.statusBar().showMessage(self.tr('Файл загружен'), 2000)
        else:
            QtGui.QMessageBox.information(self.window(), self.tr('Информация'),
                self.tr('Неверная структура файла.\nВозможно вы выбрали не тот файл.'))
            return False

        if not self.__treeXml._read(self.__lstTests, self.__lstQuestions, self.__lstAnswers):
            return False

        self._createConnectsDocument()
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
            QtGui.QMessageBox.warning(self, self.tr(self.__APPLICATION_NAME),
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

    def _closeCurrentTest(self):
        """
        Закрыть текущий тест
        """
        if self._maybeSave():
            self._setVisibleWidgets(False)

    def _settingsApp(self):
        """
        Настройки приложения
        """
        settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
        addressServer = settings.value('addressServer', 'http://dstutest.local/')

        dialogSettings = DialogSettings(self.tr('Настройки'))
        dialogSettings._setUrlServer(addressServer)

        if dialogSettings.exec_() == QtGui.QDialog.Accepted:
            settings.setValue('addressServer', dialogSettings._urlServer())
            dialogSettings.close()

    def _updateDBApp(self):
        """
        Обновление базы данных приложения
        """
        lstDataTime = self.__dataSql._queryCreateDataOrChair('SELECT datatime FROM create_data')
        dialogDBUpdate = DialogDBUpdate(
            self.tr('Обновление базы данных специальностей'),
            lstDataTime[0],
            self._checkAvailabilityServer(),
        )

        if dialogDBUpdate.exec_() == QtGui.QDialog.Accepted:
            #dialogDBUpdate._path()
            dialogDBUpdate.close()

    def _maybeSave(self):
        """
        Проверить необходимость сохранения
        текущего документа
        """
        if self.isWindowModified():
            ret = QtGui.QMessageBox.warning(self, self.tr(self.__APPLICATION_NAME),
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

    def _helpTopics(self):
        """
        Справка
        """
        fileInfo = QtCore.QFileInfo('help/index.html')
        path = fileInfo.absoluteFilePath()

        dialogHelpTopics = DialogHelpTopics(self.tr('Справка'), QtCore.QUrl.fromLocalFile(path))
        dialogHelpTopics.exec_()

    def _about(self):
        """
        О программе
        """
        QtGui.QMessageBox.about(self, self.tr('О программе'),
            self.tr('Программа <u>zTest</u> является частью '
                    'системы dTest. Предназначенна для составления тестов и '
                    'их дальнейший экспорт.\n'
                    '<p><b><i>LevBravE</i></b> специально для ИОВНФОиКТ'))

    def _updateRecentFileLabels(self, bool):
        if not bool:
            settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
            files = settings.value('filesRecent')

            filesCount = 0
            if files:
                for fileName in files:
                    if not QtCore.QFileInfo(fileName).exists():
                        files.remove(fileName)

                filesCount = len(files)

            numRecentFiles = min(filesCount, self.__MAX_RECENT_FILES)

            for index in range(numRecentFiles):
                strLabel = '<p><u style="font-size: 10pt">%d</u>. '\
                           '<b><u style="font-size: 10pt; color: indigo">%s</u></b>'\
                           '<path style="color: gray"> %s</path></p>' % (index + 1,
                                                                         QtCore.QFileInfo(files[index]).fileName(),
                                                                         files[index])
                self.__lstLabelFileRecent[index].setText(strLabel)
                self.__lstLabelFileRecent[index].setData(files[index])
                self.__lstLabelFileRecent[index].setVisible(True)
        else:
            for index in range(self.__MAX_RECENT_FILES):
                self.__lstLabelFileRecent[index].setVisible(False)

    def _updateRecentFileActions(self):
        settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
        files = settings.value('filesRecent')

        filesCount = 0
        if files:
            for fileName in files:
                if not QtCore.QFileInfo(fileName).exists():
                    files.remove(fileName)

            filesCount = len(files)

        numRecentFiles = min(filesCount, self.__MAX_RECENT_FILES)

        for index in range(numRecentFiles):
            text = '&%d %s' % (index + 1, QtCore.QFileInfo(files[index]).baseName())
            self.__lstActionFileRecent[index].setText(text)
            self.__lstActionFileRecent[index].setData(files[index])
            self.__lstActionFileRecent[index].setVisible(True)

    def _addQuestion(self):
        """
        Добавление вопроса
        """
        question = Question()
        question.document = QtGui.QTextDocument()

        self.__lstQuestions.append(question)
        self.__lstAnswers.append([])

        document = question.document
        document.contentsChanged.connect(self._editorModified)

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
        ret = QtGui.QMessageBox.warning(self, self.tr(self.__APPLICATION_NAME),
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

        document = answer.document
        document.contentsChanged.connect(self._editorModified)

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
        ret = QtGui.QMessageBox.warning(self, self.tr(self.__APPLICATION_NAME),
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
        if file:
            fileInfo = QtCore.QFileInfo(file)
            self.__strCurrentFileName = fileInfo.filePath()
            baseName = fileInfo.baseName()

            path = fileInfo.absoluteFilePath()

            self.setWindowTitle('%s[*] - [%s] - %s %s' % (baseName, path, self.__APPLICATION_NAME, self.__VERSION))

            settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
            files = settings.value('filesRecent')

            if files:
                # Delete path of file
                try:
                    files.remove(path)
                except ValueError:
                    pass

                files.insert(0, path)
                del files[self.__MAX_RECENT_FILES:]
            else:
                files = [path]

            settings.setValue('filesRecent', files)

            for widget in QtGui.QApplication.topLevelWidgets():
                if isinstance(widget, MainWindow):
                    widget._updateRecentFileActions()

            self.setWindowModified(False)
            self.__actionFileSave.setEnabled(False)
        else:
            self.__strCurrentFileName = ''
            self.setWindowTitle('untitled[*] - %s %s' % (self.__APPLICATION_NAME, self.__VERSION))

            self.setWindowModified(True)
            self.__actionFileSave.setEnabled(True)

    def _currentStateChanged(self):
        """
        Обработка сигнала stateChanged
        """
        listItems = self.__treeXml.selectedItems()
        try:
            if listItems[0].text(2):
                questionsIndex = int(listItems[0].text(1))
                answersIndex = int(listItems[0].text(2))

                answer = self.__lstAnswers[questionsIndex][answersIndex]

                if self.__editor._checkBox().checkState():
                    answer.right = True
                else:
                    answer.right = False

                if not self.isWindowModified():
                    self.setWindowModified(True)
                    self.__actionFileSave.setEnabled(True)

                self.__treeXml._setIconTreeItem(listItems[0], answer.right)
        except IndexError:
            pass

    def _createConnectsDocument(self):
        for questionsIndex, questionItem in enumerate(self.__lstQuestions):
            document = questionItem.document
            document.contentsChanged.connect(self._editorModified)

            for answersItem in self.__lstAnswers[questionsIndex]:
                document = answersItem.document
                document.contentsChanged.connect(self._editorModified)

    def _editorModified(self):
        """
        Обработка сигнала contentsChanged
        """
        listItems = self.__treeXml.selectedItems()
        try:
            # Selected Question
            if not listItems[0].text(2):
                flagType = True
                questionsIndex = int(listItems[0].text(1))

                question = self.__lstQuestions[questionsIndex]

                if not self.isWindowModified() and question.document.isModified():
                    self.setWindowModified(True)
                    self.__actionFileSave.setEnabled(True)

                flagEmpty = question.document.toPlainText()
                self.__treeXml._setTextTreeItem(listItems[0], questionsIndex, flagType, flagEmpty)
            # Selected Answer
            else:
                flagType = False
                questionsIndex = int(listItems[0].text(1))
                answersIndex = int(listItems[0].text(2))

                answer = self.__lstAnswers[questionsIndex][answersIndex]

                if not self.isWindowModified() and answer.document.isModified():
                    self.setWindowModified(True)
                    self.__actionFileSave.setEnabled(True)

                flagEmpty = answer.document.toPlainText()
                self.__treeXml._setTextTreeItem(listItems[0], answersIndex, flagType, flagEmpty)
                self.__treeXml._setIconTreeItem(listItems[0], answer.right)
        except IndexError:
            pass

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
                # Main
                self.__editor._checkBox().setVisible(False)
                questionIndex = int(listItems[0].text(1))
                document = self.__lstQuestions[questionIndex].document
                self.__editor._setDocument(document)
                self.__treeXml.setHeaderLabel('> %s' % listItems[0].text(0))
            # Answer
            elif listItems[0].text(2):
                # Action
                self.__actionEditDeleteQuestion.setEnabled(False)
                self.__actionEditAddAnswer.setEnabled(False)
                self.__actionEditDeleteAnswer.setEnabled(True)
                # Main
                self.__editor._checkBox().setVisible(True)
                questionIndex = int(listItems[0].text(1))
                answerIndex = int(listItems[0].text(2))
                answer = self.__lstAnswers[questionIndex][answerIndex]
                self.__editor._setDocument(answer.document)

                if answer.right:
                    self.__editor._checkBox().setCheckState(QtCore.Qt.Checked)
                else:
                    self.__editor._checkBox().setCheckState(QtCore.Qt.Unchecked)

                parent = listItems[0].parent()
                self.__treeXml.setHeaderLabel('> %s > %s' % (parent.text(0), listItems[0].text(0)))
            # Root
            else:
                self.__editor._checkBox().setVisible(False)
                # Action
                self.__actionEditDeleteQuestion.setEnabled(False)
                self.__actionEditAddAnswer.setEnabled(False)
                self.__actionEditDeleteAnswer.setEnabled(False)
                self.__treeXml.setHeaderLabel('>')
        except IndexError:
            pass

    def _editTestParameters(self):
        """
        Редактирование параметров теста
        """
        dialogNewTest = DialogNewTest(self.tr('Параметры теста'))
        dialogNewTest._setChairComboBox(int(self.__lstTests[0].chair))
        dialogNewTest._setAuthorLineEdit(self.__lstTests[0].author)
        dialogNewTest._setSubjectNameLineEdit(self.__lstTests[0].subjectName)
        dialogNewTest._setAttestationComboBox(int(self.__lstTests[0].attestation))
        dialogNewTest._setSpecialtyListWidget(self.__lstTests[0].lstSpecialties)

        if dialogNewTest.exec_() == QtGui.QDialog.Accepted:
            if dialogNewTest._isModified():
                self.__lstTests = []

                test = Test()
                test.chair = dialogNewTest._chairComboBox()
                test.author = dialogNewTest._authorLineEdit()
                test.subjectName = dialogNewTest._subjectNameLineEdit()
                test.attestation = dialogNewTest._attestationComboBox()
                test.lstSpecialties = dialogNewTest._specialtyListWidget()

                self.__lstTests.append(test)
                self.__treeXml._read(self.__lstTests, self.__lstQuestions, self.__lstAnswers)
                self.setWindowModified(True)
                self.__actionFileSave.setEnabled(True)

            dialogNewTest.close()