#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtCore

#**************************************************************************************************
# class: Question
# data:
#   document (object) - Текст вопроса
#   typeQuestion (int) - Тип вопроса
#   weight (int) - Вес вопроса
#**************************************************************************************************

class Question(QtCore.QObject):
    def __init__(self, document=None, typeQuestion=0, weight=1):
        QtCore.QObject.__init__(self)
        self.__document = document
        self.__typeQuestion = typeQuestion
        self.__weight = weight

    changed = QtCore.Signal()

    # Methods get and set (START)
    def _document(self): return self.__document

    def _typeQuestion(self): return self.__typeQuestion

    def _weight(self): return  self.__weight

    def _setDocument(self, document):
        self.__document = document
        self.changed.emit()

    def _setTypeQuestion(self, typeQuestion):
        self.__typeQuestion = typeQuestion
        self.changed.emit()

    def _setWeight(self, weight):
        self.__weight = weight
        self.changed.emit()

        # Methods get and set (END)

    document = QtCore.Property(object, _document, _setDocument, notify=changed)
    typeQuestion = QtCore.Property(int, _typeQuestion, _setTypeQuestion, notify=changed)
    weight = QtCore.Property(int, _weight, _setWeight, notify=changed)