#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtCore, QtGui, QtXml
from Test import Test
from Question import Question
from Answer import Answer
from HtmlContent import HtmlContent
from ZipArchive import ZipArchive

#**************************************************************************************************
# class: ReadOrWriteFile
#**************************************************************************************************

class ReadOrWriteFile(QtXml.QDomDocument):
    """
    API Xml
    """

    def __init__(self):
        QtXml.QDomDocument.__init__(self)
        self.__strFileName = ''
        self.__lstTests = []
        self.__lstQuestions = []
        self.__lstAnswers = []
        self.__dictImageNames = {}
        # HtmlContent
        self.__htmlContent = HtmlContent()

    # Get (Start)
    def _lstTests(self):
        return self.__lstTests

    def _lstQuestions(self):
        return self.__lstQuestions

    def _lstAnswers(self):
        return self.__lstAnswers

        # Get (End)

    def _dictAddImage(self, imageName, imageData):
        byteArray = QtCore.QByteArray()
        buf = QtCore.QBuffer(byteArray)
        buf.open(QtCore.QIODevice.WriteOnly)

        if not imageData.save(buf, 'png'):
            return False

        self.__dictImageNames[imageName] = buf.buffer()

        return True

    def _imageCreate(self, document):
        block = document.begin()

        while block.isValid():
            iterator = block.begin()

            while not iterator.atEnd():
                currentFragment = iterator.fragment()

                if currentFragment.isValid():
                    if currentFragment.charFormat().isImageFormat():
                        # Найден блок с картинкой
                        # Выясняется формат картинки
                        imageFormat = currentFragment.charFormat().toImageFormat()
                        # Из формата выясняется имя картинки
                        imageName = imageFormat.name()
                        # Из ресурса вытягивается картинка
                        imageData = document.resource(
                            QtGui.QTextDocument.ImageResource, QtCore.QUrl(imageName))

                        if not self._dictAddImage(imageName, imageData):
                            return False

                iterator += 1

            block = block.next()

        return True

    def _write(self):
        """
        Запись xml документа
        """
        indentSize = 4
        self.__dictImageNames[u'main.xml'] = self.toByteArray(indentSize)

        # Write Zip
        zipFile = ZipArchive(self.__strFileName, 'a', encoding='UTF-8')

        if not zipFile._write(self.__dictImageNames):
            return False

        zipFile.close()

        return True

    def _create(self, *args):
        """
        Создание xml документа
        Parameters:
        args[0] - strFileName
        args[1] - lstTests
        args[2] - lstQuestions
        args[3] - lstAnswers
        """
        self.clear()
        self.__strFileName = args[0]
        self.__lstTests = args[1]
        self.__lstQuestions = args[2]
        self.__lstAnswers = args[3]
        self.__dictImageNames = {}

        root = self.createElement('test')
        root.setAttribute('version', u'1.0')
        root.setAttribute('author', self.__lstTests[0].author)
        root.setAttribute('subjectName', self.__lstTests[0].subjectName)
        root.setAttribute('attestation', self.__lstTests[0].attestation)

        if self.__lstTests[0].lstSpecialties:
            for elementSpecialty in self.__lstTests[0].lstSpecialties:
                specialty = self.createElement('specialty')
                specialty.setAttribute('code', elementSpecialty[:6])
                specialty.setAttribute('qualification', elementSpecialty[7:9])
                specialty.setAttribute('name', elementSpecialty[10:])

                root.appendChild(specialty)

        if self.__lstQuestions:
            for questionsIndex, questionItem in enumerate(self.__lstQuestions):
                question = self.createElement('question')
                question.setAttribute('typeQuestion', questionItem.typeQuestion)
                question.setAttribute('weight', questionItem.weight)

                self.__htmlContent._clear()
                self.__htmlContent.feed(questionItem.document.toHtml())

                title = self.createElement('title')
                title.appendChild(self.createTextNode(self.__htmlContent._content()))

                # Image Question (Start)
                try:
                    self._imageCreate(questionItem.document)
                except KeyError:
                    pass
                    # Image Question (End)
                root.appendChild(question)
                question.appendChild(title)
                if self.__lstAnswers[questionsIndex]:
                    for answersIndex, answerItem in enumerate(self.__lstAnswers[questionsIndex]):
                        answer = self.createElement('answer')
                        if answerItem.right:
                            answer.setAttribute('right', 1)
                        else:
                            answer.setAttribute('right', 0)
                            # Image Answer (Start)
                        self.__htmlContent._clear()
                        self.__htmlContent.feed(answerItem.document.toHtml())

                        try:
                            self._imageCreate(answerItem.document)
                        except KeyError:
                            pass
                            # Image Answer (End)
                        answer.appendChild(self.createTextNode(self.__htmlContent._content()))
                        question.appendChild(answer)

        self.appendChild(root)

        if not self._write():
            return False

        return True

    def _parse(self, root):
        """
        Анализ xml документа
        """
        test = Test()
        test.author = root.attribute('author')
        test.subjectName = root.attribute('subjectName')
        test.attestation = root.attribute('attestation')

        childTestSpecialty = root.firstChildElement('specialty')

        if not childTestSpecialty:
            return False

        lstSpecialties = []
        while not childTestSpecialty.isNull():
            if childTestSpecialty.tagName() == 'specialty':
                strSpecialty = ''
                strSpecialty += childTestSpecialty.attribute('code')
                strSpecialty += '.' + childTestSpecialty.attribute('qualification')
                strSpecialty += ' ' + childTestSpecialty.attribute('name')

                lstSpecialties.append(strSpecialty)

            childTestSpecialty = childTestSpecialty.nextSiblingElement()

        test.lstSpecialties = lstSpecialties

        self.__lstTests.append(test)

        childTestQuestion = root.firstChildElement('question')

        while not childTestQuestion.isNull():
            if childTestQuestion.tagName() == 'question':
                question = Question()
                question.typeQuestion = childTestQuestion.attribute('typeQuestion')
                question.weight = childTestQuestion.attribute('weight')
                question.document = QtGui.QTextDocument()
                question.document.setHtml(childTestQuestion.firstChildElement('title').text())

                self.__lstQuestions.append(question)

                lstAnswers = []

                childQuestionAnswer = childTestQuestion.firstChildElement('answer')

                while not childQuestionAnswer.isNull():
                    if childQuestionAnswer.tagName() == 'answer':
                        answer = Answer()

                        if int(childQuestionAnswer.attribute('right')):
                            answer.right = True

                        answer.document = QtGui.QTextDocument()
                        answer.document.setHtml(childQuestionAnswer.text())

                        lstAnswers.append(answer)

                        childQuestionAnswer = childQuestionAnswer.nextSiblingElement()

                self.__lstAnswers.append(lstAnswers)

            childTestQuestion = childTestQuestion.nextSiblingElement()

        return True

    def _read(self, fileName):
        """
        Чтение xml документа
        """
        self.clear()
        self.__strFileName = fileName
        self.__lstTests = []
        self.__lstQuestions = []
        self.__lstAnswers = []
        # Read Zip
        zipFile = ZipArchive(self.__strFileName, encoding='UTF-8')

        self.__dictImageNames = zipFile._read()

        if not self.__dictImageNames:
            return False

        fileMainName = u'main.xml'
        byteArray = QtCore.QByteArray(self.__dictImageNames[fileMainName])

        ok, errorStr, errorLine, errorColumn = self.setContent(byteArray, True)
        if not ok:
            return False

        root = self.documentElement()
        if root.tagName() != 'test' and root.attribute('version') == u'1.0':
            return False

        if not self._parse(root):
            return False

        if self.__lstQuestions:
            for questionsIndex, questionItem in enumerate(self.__lstQuestions):
                # Image Question (Start)
                self.__htmlContent._clear()
                self.__htmlContent.feed(questionItem.document.toHtml())

                for imageName in self.__htmlContent._img():
                    imageData = QtGui.QImage()
                    imageData.loadFromData(self.__dictImageNames[imageName])
                    questionItem.document.addResource(
                        QtGui.QTextDocument.ImageResource, QtCore.QUrl(imageName), imageData)
                    # Image Question (End)
                if self.__lstAnswers[questionsIndex]:
                    for answersIndex, answerItem in enumerate(self.__lstAnswers[questionsIndex]):
                        # Image Answers (Start)
                        self.__htmlContent._clear()
                        self.__htmlContent.feed(answerItem.document.toHtml())

                        lstImages = self.__htmlContent._img()

                        if lstImages:
                            for imageName in lstImages:
                                imageData = QtGui.QImage()
                                imageData.loadFromData(self.__dictImageNames[imageName])
                                answerItem.document.addResource(
                                    QtGui.QTextDocument.ImageResource, QtCore.QUrl(imageName), imageData)
                                # Image Answers (End)

        zipFile.close()

        return True


if __name__ == '__main__':
    lstSpecialties = [u'280103.65 Защита в чрезвычайных ситуациях',
                      u'280104.65 Пожарная безопасность',
                      u'280401.65 Мелиорация, рекультивация и охрана земель']

    lstTests = [Test(u'Тарланов Арслан Тарланович', lstSpecialties, u'Математика', 1)]

    lstQuestions = [Question(u'Сколько будет 2 + 2', 1),
                    Question(u'Сколько будет 5 + 1', 1),
                    Question(u'Сколько будет 3 + 3', 1)]

    lstAnswers = [
        [Answer(u'Знаю', True),
         Answer(u'Незнаю')],
        [Answer(u'Знаю', True),
         Answer(u'Незнаю')],
        [Answer(u'Знаю', True),
         Answer(u'Незнаю')]]

    file = QtCore.QFile('hellow.xml')
    if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
        print 'Error: Create File'

    domXml = ReadOrWriteFile()
    if not domXml._create(file, lstTests, lstQuestions, lstAnswers):
        print 'Error: Create Xml'

