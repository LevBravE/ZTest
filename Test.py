#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtCore

#**************************************************************************************************
# class: Test
# data:
#   author (string) - Фамилия Имя Отчество автора теста
#   lstSpecialties (list) - Код дисциплины
#   subjectName (string) - Наименование дисциплины
#   attestation (int) - Номер аттестации
#**************************************************************************************************

class Test(QtCore.QObject):
    def __init__(self, author='', lstSpecialties=None, subjectName='', attestation=0):
        QtCore.QObject.__init__(self)
        self.__author = author
        self.__lstSpecialties = lstSpecialties
        self.__subjectName = subjectName
        self.__attestation = attestation

    changed = QtCore.Signal()

    # Methods get and set (START)
    def _author(self): return self.__author

    def _lstSpecialties(self): return self.__lstSpecialties

    def _subjectName(self): return  self.__subjectName

    def _attestation(self): return self.__attestation

    def _setAuthor(self, author):
        self.__author = author
        self.changed.emit()

    def _setLstSpecialties(self, lstSpecialties):
        self.__lstSpecialties = lstSpecialties
        self.changed.emit()

    def _setSubjectName(self, subjectName):
        self.__subjectName = subjectName
        self.changed.emit()

    def _setAttestation(self, attestation):
        self.__attestation = attestation
        self.changed.emit()

        # Methods get and set (END)

    author = QtCore.Property(str, _author, _setAuthor, notify=changed)
    lstSpecialties = QtCore.Property(list, _lstSpecialties, _setLstSpecialties, notify=changed)
    subjectName = QtCore.Property(str, _subjectName, _setSubjectName, notify=changed)
    attestation = QtCore.Property(int, _attestation, _setAttestation, notify=changed)
