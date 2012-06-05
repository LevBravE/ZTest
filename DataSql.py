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
        ok = query.exec_('create table create_data('
                         'id integer primary key, '
                         'datatime text' # Дата и время создания
                         ')')
        if not ok:
            return False

        ok = query.exec_('create table specialty('
                         'id integer primary key, '
                         'name text, ' # Наименование
                         'code text, ' # Код
                         'type text' # Направление
                         ')')
        if not ok:
            return False

        ok = query.exec_('create table chair('
                         'id integer primary key, '
                         'name text, ' # Наименование
                         'code text' # Код
                         ')')
        if not ok:
            return False

        # Add data time in table update
        strCurrentDataTime = QtCore.QDateTime().currentDateTime().toString(QtCore.Qt.ISODate)
        if not query.exec_('INSERT INTO create_data (id, datatime) VALUES(1, "%s");' % strCurrentDataTime):
            return False
            # Чтение файла sql/db_ztest.sql и построчное выполнение команд находящихся в нем
        fileInsert = codecs.open('sql/db_ztest.sql', 'r', encoding='utf-8')
        for line in fileInsert:
            if not query.exec_(line):
                return False

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

    def _querySpecialty(self, selectText):
        """
        Запрос к базе данных table specialty
        """
        query = QtSql.QSqlQuery()
        ok = query.exec_(selectText)

        if not ok:
            return False

        lstResult = []

        while query.next():
            lstResult.append(unicode(query.value(0) + '.' + query.value(1) + ' ' + query.value(2)))

        return lstResult

    def _queryCreateDataOrChair(self, selectText):
        """
        Запрос к базе данных table chair
        """
        query = QtSql.QSqlQuery()
        ok = query.exec_(selectText)

        if not ok:
            return False

        lstResult = []

        while query.next():
            lstResult.append(unicode(query.value(0)))

        return lstResult

if __name__ == '__main__':
    import sys

    app = QtCore.QCoreApplication(sys.argv)
    dataSql = DataSql()
    if not dataSql._connectDataBase('sqlite/db_ztest.sqlite'):
        print 'Error: Not connect database'

    # Start _createDataBase wait(~1min)...
    if not dataSql._createDataBase():
        print 'Error: Not create database'

    lstSpecialties = dataSql._querySpecialty('SELECT code, type, name '
                                             'FROM specialty '
                                             'WHERE type LIKE 68')

    lstChair = dataSql._queryCreateDataOrChair('SELECT name FROM chair')

    lstDataTime = dataSql._queryCreateDataOrChair('SELECT datatime FROM create_data')

    print lstSpecialties[0]
    print lstChair[0]
    print lstDataTime[0]