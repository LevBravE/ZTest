#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

import random
from PySide import QtCore, QtGui
from TextEditInsertImage import TextEditInsertImage
from DataSql import DataSql

#**************************************************************************************************
# class: Editor
#**************************************************************************************************

class Editor(QtGui.QWidget):
    """
    Диалоговое окно редактора
    """

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.__changeCheckBox = False
        # DataSql
        self.__dataSql = DataSql()
        # TextEdit
        self.__textEdit = TextEditInsertImage()
        # QCheckBox
        self.__checkBox = QtGui.QCheckBox(self.tr('это правильный ответ'))
        # ToolBar
        self.__oneLineToolBar = QtGui.QToolBar()
        # ComboBox
        self.__sizeComboBox = QtGui.QComboBox()
        db = QtGui.QFontDatabase()
        for size in db.standardSizes():
            self.__sizeComboBox.addItem(str(size))
            # Layout
        self.__layoutVMain = QtGui.QVBoxLayout()
        self.__layoutVMain.addWidget(self.__oneLineToolBar)
        self.__layoutVMain.addWidget(self.__textEdit)
        self.__layoutVMain.addWidget(self.__checkBox)
        self.__layoutVMain.setSpacing(0)
        self.__layoutVMain.setContentsMargins(0, 0, 0, 0)
        # Functions
        self._createActions()
        self._adjustActions()
        self._createToolBars()
        self._createContextMenuTreeWidget()
        self._fontChanged(self.__textEdit.font())
        self._colorChanged(self.__textEdit.textColor())
        self._sizeChanged(QtGui.QApplication.font().pointSize())
        self._textSize()
        # Connect
        self.__textEdit.currentCharFormatChanged.connect(self._currentCharFormatChanged)
        self.__textEdit.undoAvailable.connect(self.__actionEditUndo.setEnabled)
        self.__textEdit.redoAvailable.connect(self.__actionEditRedo.setEnabled)
        self.__textEdit.copyAvailable.connect(self.__actionEditCut.setEnabled)
        self.__textEdit.copyAvailable.connect(self.__actionEditCopy.setEnabled)

        self.__sizeComboBox.activated.connect(self._textSize)
        # <<<Self>>>
        self.setLayout(self.__layoutVMain)
        #self.setFocus()

    def _checkBox(self):
        return self.__checkBox

    def _createActions(self):
        # Action Edit
        self.__actionEditUndo = QtGui.QAction(QtGui.QIcon('img/black/png/undo_icon&16.png'),
            self.tr('Отменить'),
            self, shortcut=QtGui.QKeySequence.Undo,
            triggered=self.__textEdit.undo)

        self.__actionEditRedo = QtGui.QAction(QtGui.QIcon('img/black/png/redo_icon&16.png'),
            self.tr('Вернуть'),
            self, shortcut=QtGui.QKeySequence.Redo,
            triggered=self.__textEdit.redo)

        self.__actionEditCut = QtGui.QAction(QtGui.QIcon('img/black/png/clipboard_cut_icon&16.png'),
            self.tr('Вырезат&ь'),
            self, shortcut=QtGui.QKeySequence.Cut,
            triggered=self.__textEdit.cut)

        self.__actionEditCopy = QtGui.QAction(QtGui.QIcon('img/black/png/clipboard_copy_icon&16.png'),
            self.tr('&Копировать'), self, shortcut=QtGui.QKeySequence.Copy,
            triggered=self.__textEdit.copy)

        self.__actionEditPaste = QtGui.QAction(QtGui.QIcon('img/black/png/clipboard_past_icon&16.png'),
            self.tr('&Вставить'), self, shortcut=QtGui.QKeySequence.Paste,
            triggered=self.__textEdit.paste)

        self.__actionEditSelectAll = QtGui.QAction(self.tr('Вы&делить всё'), self,
            shortcut=QtGui.QKeySequence.SelectAll,
            triggered=self.__textEdit.selectAll)

        self.__actionEditItemEmpty = QtGui.QAction(QtGui.QIcon('img/black/png/doc_empty_icon&16.png'),
            self.tr('&Очистить'),
            self, shortcut=QtGui.QKeySequence.New,
            triggered=self._newDocument)
        # Action Format
        self.__actionFormatBold = QtGui.QAction(QtGui.QIcon('img/black/png/font_bold_icon&16.png'),
            self.tr('Полужирный'), self, shortcut=QtGui.QKeySequence.Bold,
            triggered=self._textBold)
        self.__actionFormatBold.setCheckable(True)

        self.__actionFormatItalic = QtGui.QAction(QtGui.QIcon('img/black/png/font_italic_icon&16.png'),
            self.tr('Курсив'), self, shortcut=QtGui.QKeySequence.Italic,
            triggered=self._textItalic)
        self.__actionFormatItalic.setCheckable(True)

        self.__actionFormatUnderline = QtGui.QAction(QtGui.QIcon('img/black/png/font_underline_icon&16.png'),
            self.tr('Подчеркнутый'), self, shortcut=QtGui.QKeySequence.Underline,
            triggered=self._textUnderline)
        self.__actionFormatUnderline.setCheckable(True)

        self.__actionFormatAlignLeft = QtGui.QAction(QtGui.QIcon('img/black/png/align_left_icon&16.png'),
            self.tr('По левому краю'), self,
            triggered=self._textAlignLeft)

        self.__actionFormatAlignCenter = QtGui.QAction(QtGui.QIcon('img/black/png/align_center_icon&16.png'),
            self.tr('По центру'), self,
            triggered=self._textAlignCenter)

        self.__actionFormatAlignRight = QtGui.QAction(QtGui.QIcon('img/black/png/align_right_icon&16.png'),
            self.tr('По правому краю'), self,
            triggered=self._textAlignRight)

        self.__actionFormatAlignJustify = QtGui.QAction(QtGui.QIcon('img/black/png/align_just_icon&16.png'),
            self.tr('По ширине'), self,
            triggered=self._textAlignJustify)

        pixmap = QtGui.QPixmap(16, 16)
        pixmap.fill(QtCore.Qt.black)
        self.__actionFormatColor = QtGui.QAction(pixmap,
            self.tr('Цвет текста'), self,
            triggered=self._textColor)
        # Action Insert
        self.__actionInsertImage = QtGui.QAction(QtGui.QIcon('img/black/png/picture_icon&16.png'),
            self.tr('Добавить рисунок'), self,
            triggered=self._insertImageLocale)

    def _adjustActions(self):
        # Enable
        self.__actionEditUndo.setEnabled(self.__textEdit.document().isUndoAvailable())
        self.__actionEditRedo.setEnabled(self.__textEdit.document().isRedoAvailable())
        self.__actionEditCut.setEnabled(False)
        self.__actionEditCopy.setEnabled(False)

    def _createToolBars(self):
        self.__oneLineToolBar.setMovable(False)
        self.__oneLineToolBar.addAction(self.__actionEditItemEmpty)
        self.__oneLineToolBar.addSeparator()
        self.__oneLineToolBar.addAction(self.__actionEditUndo)
        self.__oneLineToolBar.addAction(self.__actionEditRedo)
        self.__oneLineToolBar.addSeparator()
        self.__oneLineToolBar.addAction(self.__actionEditCut)
        self.__oneLineToolBar.addAction(self.__actionEditCopy)
        self.__oneLineToolBar.addAction(self.__actionEditPaste)
        self.__oneLineToolBar.addSeparator()
        self.__oneLineToolBar.addAction(self.__actionFormatBold)
        self.__oneLineToolBar.addAction(self.__actionFormatItalic)
        self.__oneLineToolBar.addAction(self.__actionFormatUnderline)
        self.__oneLineToolBar.addSeparator()
        self.__oneLineToolBar.addAction(self.__actionFormatAlignLeft)
        self.__oneLineToolBar.addAction(self.__actionFormatAlignCenter)
        self.__oneLineToolBar.addAction(self.__actionFormatAlignRight)
        self.__oneLineToolBar.addAction(self.__actionFormatAlignJustify)
        self.__oneLineToolBar.addSeparator()
        self.__oneLineToolBar.addAction(self.__actionFormatColor)
        self.__oneLineToolBar.addSeparator()
        self.__oneLineToolBar.addWidget(self.__sizeComboBox)
        self.__oneLineToolBar.addSeparator()
        self.__oneLineToolBar.addAction(self.__actionInsertImage)

    def _clear(self):
        self.__textEdit.clear()

    # MENU Get (Start)
    def _actionEditUndo(self): return self.__actionEditUndo

    def _actionEditRedo(self): return self.__actionEditRedo

    def _actionEditCut(self): return self.__actionEditCut

    def _actionEditCopy(self): return self.__actionEditCopy

    def _actionEditPaste(self): return self.__actionEditPaste

    def _actionEditSelectAll(self): return self.__actionEditSelectAll

    def _actionEditItemEmpty(self): return self.__actionEditItemEmpty

    def _actionInsertImage(self): return self.__actionInsertImage

    def _actionFormatBold(self): return self.__actionFormatBold

    def _actionFormatItalic(self): return self.__actionFormatItalic

    def _actionFormatUnderline(self): return self.__actionFormatUnderline

    def _actionFormatAlignLeft(self): return self.__actionFormatAlignLeft

    def _actionFormatAlignCenter(self): return self.__actionFormatAlignCenter

    def _actionFormatAlignRight(self): return self.__actionFormatAlignRight

    def _actionFormatAlignJustify(self): return self.__actionFormatAlignJustify

    def _actionFormatColor(self): return self.__actionFormatColor

    def _createContextMenuTreeWidget(self):
        self.__textEdit.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.__textEdit.addAction(self.__actionEditUndo)
        self.__textEdit.addAction(self.__actionEditRedo)
        self.__textEdit.addAction(self.__actionEditCut)
        self.__textEdit.addAction(self.__actionEditCopy)
        self.__textEdit.addAction(self.__actionEditPaste)
        self.__textEdit.addAction(self.__actionEditSelectAll)

    def _mergeFormatOnWordOrSelection(self, formatText):
        cursor = self.__textEdit.textCursor()

        if not cursor.hasSelection():
            cursor.select(QtGui.QTextCursor.WordUnderCursor)

        cursor.mergeCharFormat(formatText)
        self.__textEdit.mergeCurrentCharFormat(formatText)

    def _fontChanged(self, font):
        self.__actionFormatBold.setChecked(font.bold())
        self.__actionFormatItalic.setChecked(font.italic())
        self.__actionFormatUnderline.setChecked(font.underline())

    def _colorChanged(self, color):
        pixmap = QtGui.QPixmap(16, 16)
        pixmap.fill(color)
        self.__actionFormatColor.setIcon(pixmap)

    def _sizeChanged(self, size):
        self.__sizeComboBox.setCurrentIndex(self.__sizeComboBox.findText(str(int(size))))

    def _currentCharFormatChanged(self, formatText):
        if not formatText.fontPointSize():
            self._sizeChanged(QtGui.QApplication.font().pointSize())
            self._textSize()
        else:
            self._fontChanged(formatText.font())
            self._colorChanged(formatText.foreground().color())
            self._sizeChanged(formatText.fontPointSize())

    def _newDocument(self):
        self.__textEdit.clear()

    def _textBold(self):
        formatText = QtGui.QTextCharFormat()
        formatText.setFontWeight(QtGui.QFont.Bold if self.__actionFormatBold.isChecked() else QtGui.QFont.Normal)
        self._mergeFormatOnWordOrSelection(formatText)

    def _textItalic(self):
        formatText = QtGui.QTextCharFormat()
        formatText.setFontItalic(self.__actionFormatItalic.isChecked())
        self._mergeFormatOnWordOrSelection(formatText)

    def _textUnderline(self):
        formatText = QtGui.QTextCharFormat()
        formatText.setFontUnderline(self.__actionFormatUnderline.isChecked())
        self._mergeFormatOnWordOrSelection(formatText)

    def _textSize(self):
        pointSize = int(self.__sizeComboBox.currentText())
        formatText = QtGui.QTextCharFormat()
        formatText.setFontPointSize(pointSize)
        self._mergeFormatOnWordOrSelection(formatText)

    def _textColor(self):
        color = QtGui.QColorDialog.getColor(self.__textEdit.textColor())

        if not color.isValid():
            return

        formatText = QtGui.QTextCharFormat()
        formatText.setForeground(color)
        self._mergeFormatOnWordOrSelection(formatText)
        self._colorChanged(color)

    def _textAlignLeft(self):
        self.__textEdit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignAbsolute)

    def _textAlignCenter(self):
        self.__textEdit.setAlignment(QtCore.Qt.AlignHCenter)

    def _textAlignRight(self):
        self.__textEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignAbsolute)

    def _textAlignJustify(self):
        self.__textEdit.setAlignment(QtCore.Qt.AlignJustify)


    def _insertImageLocale(self):
        filters = self.tr('Common Graphics (*.png *.jpg *.jpeg *.gif);;'
                          'Portable Network Graphics (PNG) (*.png);;'
                          'JPEG (*.jpg *.jpeg);;'
                          'Graphics Interchange Format (*.gif)')

        fileName = QtGui.QFileDialog.getOpenFileName(self,
            self.tr('Открыть рисунок'), QtCore.QDir.currentPath(),
            filters)[0]

        if not fileName:
            return

        if not QtCore.QFile.exists(fileName):
            return

        url = QtCore.QUrl('image%s' % random.random())
        image = QtGui.QImageReader(fileName).read()

        textDocument = self.__textEdit.document()
        textDocument.addResource(QtGui.QTextDocument.ImageResource, url, image)

        cursor = self.__textEdit.textCursor()

        imageFormat = QtGui.QTextImageFormat()
        imageFormat.setWidth(image.width())
        imageFormat.setHeight(image.height())
        imageFormat.setName(url.toString())
        cursor.insertImage(imageFormat)

    def _setDocument(self, document):
        self.__textEdit.setDocument(document)
        self.__textEdit.document().setModified(False)

if __name__ == '__main__':
    import sys

    QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('UTF-8'))
    app = QtGui.QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())

