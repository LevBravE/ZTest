#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtCore, QtGui

#**************************************************************************************************
# class: LineEditAutoComplete
#**************************************************************************************************

class LineEditAutoComplete(QtGui.QLineEdit):
    """
    LineEdit с автодополнением
    """

    def __init__(self, model):
        QtGui.QLineEdit.__init__(self)

        self.__model = model

        self.__completer = QtGui.QCompleter(self.__model)
        self.__completer.setWidget(self)
        self.__completer.activated.connect(self._insertCompletion)

        self.__keysToIgnore = [QtCore.Qt.Key_Enter,
                               QtCore.Qt.Key_Return,
                               QtCore.Qt.Key_Escape,
                               QtCore.Qt.Key_Tab]

    def _setModel(self, model):
        self.__model = model
        self.__completer = QtGui.QCompleter(self.__model)
        self.__completer.setWidget(self)
        self.__completer.activated.connect(self._insertCompletion)

    def _insertCompletion(self, completion):
        """
        Обработчик добавляет к введенной строке оставшуюся часть
        выбранную из выпадаюшего списка
        """
        extra = len(completion) - len(self.__completer.completionPrefix())
        extraText = completion[-extra:]

        extraText += '\n'

        self.setText(self.text() + extraText)

    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if self.__completer.popup().isVisible():
                if event.key() in self.__keysToIgnore:
                    event.ignore()
                    return False

            QtGui.QLineEdit.keyPressEvent(self, event)
            completionPrefix = self.text()

            if completionPrefix != self.__completer.completionPrefix():
                self._updateCompleterPopupItems(completionPrefix)
            if (len(event.text()) and len(completionPrefix)) > 0:
                self.__completer.complete()
            if not len(completionPrefix):
                self.__completer.popup().hide()

            palette = QtGui.QPalette()

            if self.__completer.completionCount() or not completionPrefix:
                palette.setColor(QtGui.QPalette.Text, QtCore.Qt.black)
                self.setPalette(palette)

            else:
                palette.setColor(QtGui.QPalette.Text, QtCore.Qt.red)
                self.setPalette(palette)
                self.setText(self.text()[:-1])
                QtGui.QToolTip.showText(self.mapToGlobal(QtCore.QPoint(self.width(), -14)),
                    self.tr('Нет такой специальности'))

            return True

        else:
            return QtGui.QLineEdit.event(self, event)

    def _updateCompleterPopupItems(self, completionPrefix):
        """
        Фильтрует элементы выпадающего списка, чтобы только
        показывать елементы с данной приставкой
        """
        self.__completer.setCompletionPrefix(completionPrefix)
        self.__completer.popup().setCurrentIndex(
            self.__completer.completionModel().index(0, 0)
        )


if __name__ == '__main__':
    import sys

    QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('UTF-8'))

    app = QtGui.QApplication(sys.argv)
    lstQuery = ['hellow dddd', 'dsdsdsd', 'rrrrr', 'hellod']
    window = QtGui.QWidget()
    editor = LineEditAutoComplete(lstQuery)
    hbox = QtGui.QHBoxLayout()
    hbox.addWidget(editor)
    window.setLayout(hbox)
    window.show()

    sys.exit(app.exec_())
