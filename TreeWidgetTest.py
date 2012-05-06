#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtCore, QtGui

#**************************************************************************************************
# class: TreeWidgetTest
#**************************************************************************************************

class TreeWidgetTest(QtGui.QTreeWidget):
    def __init__(self):
        QtGui.QTreeWidget.__init__(self)
        self.__lstTests = []
        self.__lstQuestions = []
        self.__lstAnswers = []
        self.__item = None

        # Icon
        self.__testIcon = QtGui.QIcon()
        self.__testIcon.addPixmap(QtGui.QPixmap('img/black/png/book_side_icon&16.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.__testIcon.addPixmap(QtGui.QPixmap('img/black/png/book_icon&16.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.On)

        self.__authorIcon = QtGui.QIcon()
        self.__authorIcon.addPixmap(QtGui.QPixmap('img/black/png/user_icon&16.png'))

        self.__attestationIcon = QtGui.QIcon()
        self.__attestationIcon.addPixmap(QtGui.QPixmap('img/black/png/calendar_1_icon&16.png'))

        self.__specialtyIcon = QtGui.QIcon()
        self.__specialtyIcon.addPixmap(QtGui.QPixmap('img/black/png/notepad_2_icon&16.png'))

        self.__specialtiesIcon = QtGui.QIcon()
        self.__specialtiesIcon.addPixmap(QtGui.QPixmap('img/black/png/wrench_icon&16.png'))

        self.__questionIcon = QtGui.QIcon()
        self.__questionIcon.addPixmap(QtGui.QPixmap('img/black/png/question_off.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.__questionIcon.addPixmap(QtGui.QPixmap('img/black/png/question_on.gif'),
            QtGui.QIcon.Normal, QtGui.QIcon.On)

        self.__answerIconFalse = QtGui.QIcon()
        self.__answerIconFalse.addPixmap(QtGui.QPixmap('img/black/png/round_delete_icon&16.png'))

        self.__answerIconTrue = QtGui.QIcon()
        self.__answerIconTrue.addPixmap(QtGui.QPixmap('img/black/png/round_checkmark_icon&16.png'))
        # <<<Self>>>
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Base, QtGui.QColor(QtCore.Qt.darkGray))
        self.header().setResizeMode(QtGui.QHeaderView.Stretch)
        self.setHeaderLabel(self.tr('Список вопросов'))
        palette = QtGui.QApplication.palette()
        self.setPalette(palette)
        #self.setBackgroundRole(QtGui.QPalette.Dark)

    # GET and SET (Start)
    def _lstTests(self): return self.__lstTests

    def _lstQuestions(self): return self.__lstQuestions

    def _lstAnswers(self): return self.__lstAnswers

    def _setLstTests(self, lstTests):
        self.__lstTests = lstTests

    def _setLstQuestions(self, lstQuestions):
        self.__lstQuestions = lstQuestions

    def  _setLstAnswers(self, lstAnswers):
        self.__lstAnswers = lstAnswers

        # GET and SET (End)

    def _read(self, lstTests, lstQuestions, lstAnswers):
        self._setLstTests(lstTests)
        self._setLstQuestions(lstQuestions)
        self._setLstAnswers(lstAnswers)

        self.clear()
        # It might not be connected.
        try:
            self.itemChanged.disconnect(self.reset)
        except:
            pass
        self._create()
        self.itemChanged.connect(self.reset)
        return True

    def _create(self, parentItem=None):
        # Test subjectName
        self.__item = self._createItem(parentItem)

        test = self.__lstTests[0].subjectName

        self.__item.setFlags(self.__item.flags() | QtCore.Qt.ItemIsSelectable)
        self.__item.setIcon(0, self.__testIcon)
        self.__item.setText(0, test)

        self.setItemExpanded(self.__item, True)
        # Test author
        itemAuthor = self._createItem(self.__item)

        author = self.__lstTests[0].author

        itemAuthor.setFlags(QtCore.Qt.NoItemFlags)
        itemAuthor.setIcon(0, self.__authorIcon)
        itemAuthor.setText(0, author)
        # Test attestation
        itemAttestation = self._createItem(self.__item)

        attestation = self.tr('аттестация №%s') % unicode(self.__lstTests[0].attestation)

        itemAttestation.setFlags(QtCore.Qt.NoItemFlags)
        itemAttestation.setIcon(0, self.__attestationIcon)
        itemAttestation.setText(0, attestation)
        # Test specialty
        itemSpecialty = self._createItem(self.__item)

        specialty = self.tr('специальности(%d)') % len(self.__lstTests[0].lstSpecialties)

        itemSpecialty.setFlags(QtCore.Qt.NoItemFlags)
        itemSpecialty.setIcon(0, self.__specialtyIcon)
        itemSpecialty.setText(0, specialty)

        for elementSpecialty in self.__lstTests[0].lstSpecialties:
            itemSpecialties = self._createItem(itemSpecialty)

            specialties = elementSpecialty
            itemSpecialties.setFlags(QtCore.Qt.NoItemFlags)
            itemSpecialties.setIcon(0, self.__specialtiesIcon)
            itemSpecialties.setText(0, specialties)

        font = QtGui.QFont()
        font.setItalic(True)

        if self.__lstQuestions:
            for questionsIndex, questionItem in enumerate(self.__lstQuestions):
                itemQuestion = self._createItem(self.__item)
                itemQuestion.setFlags(itemQuestion.flags() | QtCore.Qt.ItemIsSelectable)
                itemQuestion.setIcon(0, self.__questionIcon)
                number = questionsIndex + 1

                if questionItem.document.toPlainText():
                    itemQuestion.setText(0, self.tr('вопрос (%s)') % number)
                else:
                    itemQuestion.setFont(0, font)
                    itemQuestion.setText(0, self.tr('-задайте вопрос-'))

                itemQuestion.setText(1, str(questionsIndex))

                if self.__lstAnswers[questionsIndex]:
                    for answersIndex, answerItem in enumerate(self.__lstAnswers[questionsIndex]):
                        itemAnswer = self._createItem(itemQuestion)
                        itemAnswer.setFlags(itemAnswer.flags() | QtCore.Qt.ItemIsSelectable)

                        if answerItem.right:
                            itemAnswer.setIcon(0, self.__answerIconTrue)
                        else:
                            itemAnswer.setIcon(0, self.__answerIconFalse)

                        number = answersIndex + 1

                        if answerItem.document.toPlainText():
                            itemAnswer.setText(0, self.tr('ответ %s') % number)
                        else:
                            itemAnswer.setFont(0, font)
                            itemAnswer.setText(0, self.tr('-задайте ответ-'))

                        itemAnswer.setText(1, str(questionsIndex))
                        itemAnswer.setText(2, str(answersIndex))
                else:
                    itemAnswer = self._createItem(itemQuestion)
                    itemAnswer.setFlags(QtCore.Qt.NoItemFlags)
                    itemAnswer.setFont(0, font)
                    itemAnswer.setText(0, self.tr('пусто'))
        else:
            itemQuestionEmpty = self._createItem(self.__item)
            itemQuestionEmpty.setFlags(QtCore.Qt.NoItemFlags)
            itemQuestionEmpty.setFont(0, font)
            itemQuestionEmpty.setText(0, self.tr('пусто'))

    def _createItem(self, parentItem=None):
        if parentItem is not None:
            item = QtGui.QTreeWidgetItem(parentItem)
        else:
            item = QtGui.QTreeWidgetItem(self)

        return item

    def _setTextTreeItem(self, itemTree, itemIndex, flagType, flagEmpty):
        strType = ''
        strNumber = ''

        if flagType:
            strType = u'вопрос'
            strNumber = u'(%s)' % (itemIndex + 1)
        else:
            strType = u'ответ'
            strNumber = u'%s' % (itemIndex + 1)

        font = QtGui.QFont()

        if flagEmpty:
            font.setItalic(False)
            itemTree.setFont(0, font)
            itemTree.setText(0, self.tr('%s %s') % (strType, strNumber))
        else:
            font.setItalic(True)
            itemTree.setFont(0, font)
            itemTree.setText(0, self.tr('-задайте %s-') % strType)

        self.setItemExpanded(self.__item, True)
        self.setCurrentItem(itemTree)

    def _setIconTreeItem(self, itemTree, flagRight):
        if flagRight:
            itemTree.setIcon(0, self.__answerIconTrue)
        else:
            itemTree.setIcon(0, self.__answerIconFalse)

        self.setItemExpanded(self.__item, True)
        self.setItemExpanded(itemTree.parent(), True)
        self.setCurrentItem(itemTree)

    def _addQuestion(self, itemRoot, questionsIndex):
        item = itemRoot.child(3)
        if item.text(0) == u'пусто':
            item = itemRoot.takeChild(3)
            del item

        font = QtGui.QFont()
        font.setItalic(True)

        question = self.tr('-задайте вопрос-')
        itemQuestion = self._createItem(self.__item)
        itemQuestion.setFlags(itemQuestion.flags() | QtCore.Qt.ItemIsSelectable)
        itemQuestion.setIcon(0, self.__questionIcon)
        itemQuestion.setFont(0, font)
        itemQuestion.setText(0, question)
        itemQuestion.setText(1, str(questionsIndex))

        answer = self.tr('пусто')
        itemAnswer = self._createItem(itemQuestion)
        itemAnswer.setFlags(QtCore.Qt.NoItemFlags)
        itemAnswer.setFont(0, font)
        itemAnswer.setText(0, answer)

        self.addTopLevelItem(self.__item)
        self.setItemExpanded(self.__item, True)
        self.setCurrentItem(itemQuestion)

    def _deleteQuestion(self, questionsIndex, lstQuestions):
        if self.__item:
            item = self.__item.takeChild(questionsIndex + 3)
            del item

            font = QtGui.QFont()
            font.setItalic(True)

            if lstQuestions:
                iterator = QtGui.QTreeWidgetItemIterator(self.__item.child(3),
                    QtGui.QTreeWidgetItemIterator.HasChildren)
                number = 1

                while iterator.value():
                    if not lstQuestions[number - 1].document.toPlainText():
                        iterator.value().setText(0, self.tr('-задайте вопрос-'))
                    else:
                        iterator.value().setText(0, self.tr('вопрос (%s)') % number)

                    iterator.value().setText(1, str(number - 1))

                    number += 1
                    iterator += 1

                    if questionsIndex:
                        self.setCurrentItem(self.__item.child(questionsIndex + 2))
                    else:
                        self.setCurrentItem(self.__item.child(questionsIndex + 3))
            else:
                itemQuestionEmpty = self._createItem(self.__item)
                itemQuestionEmpty.setFlags(QtCore.Qt.NoItemFlags)
                itemQuestionEmpty.setFont(0, font)
                itemQuestionEmpty.setText(0, self.tr('пусто'))
                self.setCurrentItem(self.__item)

        self.setItemExpanded(self.__item, True)

    def _addAnswer(self, itemQuestion, questionsIndex, answersIndex):
        item = itemQuestion.child(0)
        if item.text(0) == u'пусто':
            item = itemQuestion.takeChild(0)
            del item

        font = QtGui.QFont()
        font.setItalic(True)

        answer = self.tr('-задайте ответ-')
        itemAnswer = self._createItem(itemQuestion)
        itemAnswer.setFlags(itemAnswer.flags() | QtCore.Qt.ItemIsSelectable)
        itemAnswer.setFont(0, font)
        itemAnswer.setText(0, answer)
        itemAnswer.setText(1, str(questionsIndex))
        itemAnswer.setText(2, str(answersIndex))

        self.addTopLevelItem(itemQuestion)
        self.setItemExpanded(self.__item, True)
        self.setItemExpanded(itemQuestion, True)
        self.setCurrentItem(itemAnswer)

    def _deleteAnswer(self, itemQuestion, answersIndex, lstAnswers):
        if itemQuestion:
            item = itemQuestion.takeChild(answersIndex)
            del item

            font = QtGui.QFont()
            font.setItalic(True)

            countChildItem = itemQuestion.childCount()

            if countChildItem:
                iterator = QtGui.QTreeWidgetItemIterator(itemQuestion, QtGui.QTreeWidgetItemIterator.NoChildren)
                number = 1

                while iterator.value():
                    if not lstAnswers[number - 1].document.toPlainText():
                        iterator.value().setText(0, self.tr('-задайте ответ-'))
                    else:
                        iterator.value().setText(0, self.tr('ответ %s') % number)

                    iterator.value().setText(1, itemQuestion.text(1))
                    iterator.value().setText(2, str(number - 1))

                    if number >= countChildItem:
                        break
                    number += 1
                    iterator += 1

                if answersIndex:
                    self.setCurrentItem(itemQuestion.child(answersIndex - 1))
                else:
                    self.setCurrentItem(itemQuestion.child(answersIndex))
            else:
                itemAnswer = self._createItem(itemQuestion)
                itemAnswer.setFlags(QtCore.Qt.NoItemFlags)
                itemAnswer.setFont(0, font)
                itemAnswer.setText(0, self.tr('пусто'))
                self.setCurrentItem(itemQuestion)

            self.setItemExpanded(self.__item, True)
            self.setItemExpanded(itemQuestion, True)




