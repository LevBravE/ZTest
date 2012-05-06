#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

import codecs
from PySide import QtCore, QtSql

#**************************************************************************************************
# class: DataSql
#**************************************************************************************************

class DataSql(QtCore.QObject):
    """
    API Database
    """

    def __init__(self):
        QtCore.QObject.__init__(self)

    def _createDataBase(self):
        """
        Создание базы данных и заполнение её данными.
        """
        query = QtSql.QSqlQuery()
        ok = query.exec_('create table specialty('
                         'id integer primary key, '
                         'name text, ' # Наименование
                         'code text, ' # Код
                         'type text' # Направление
                         ')')
        if not ok:
            return False

        # Чтение файла sql/db_specialties.sql и построчное выполнение команд находящихся в нем
        fileInsert = codecs.open('sql/db_specialties.sql', 'r', encoding='utf-8')
        for line in fileInsert:
            query.exec_(line)

        fileInsert.close()

        return True

    def _connectDataBase(self, fileName):
        """
        Соединение с базой данных
        """
        self.__fileName = fileName
        dbSQLite = QtSql.QSqlDatabase()
        dataBase = dbSQLite.addDatabase('QSQLITE')
        dataBase.setDatabaseName(self.__fileName)
        if not dataBase.open():
            return False
        return True

    def _query(self, selectText):
        """
        Запрос к базе данных
        """
        query = QtSql.QSqlQuery()
        ok = query.exec_(selectText)

        if not ok:
            return False

        lstResult = []

        while query.next():
            lstResult.append(unicode(query.value(0) + '.' + query.value(1) + ' ' + query.value(2)))

        return lstResult

if __name__ == '__main__':
    dataSql = DataSql()
    if not dataSql._connectDataBase('sqlite/db_specialties.sqlite'):
        print 'Error: Not connect database'

    # Start _createDataBase wait(~5min)...
    #if not dataSql._createDataBase():
    #    print 'Error: Not create database'

    lstSpecialties = dataSql._query('SELECT code, type, name '
                                    'FROM specialty '
                                    'WHERE type LIKE 68')

    print lstSpecialties[0]