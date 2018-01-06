from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QInputDialog, QApplication, QMainWindow,
                             QAction, qApp, QLabel,QFormLayout,QHBoxLayout,
                             QFileDialog, QSpinBox, QTabWidget)
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

import BOpack as bo
import sys
import random
import os
import matplotlib.pyplot as plt
import numpy as np
import testModule

class NormalRunThread(QThread):

    finishedSig = pyqtSignal()

    def __init__(self,parameterVector):

        QThread.__init__(self)
        self.list = parameterVector
        self.numIter = parameterVector[0]
        self.numPop = parameterVector[1]
        self.chance = parameterVector[2]
        self.pathString = parameterVector[3]
        self.stateString = parameterVector[4]

    def __del__(self):
        self.wait()

    def run(self):
        random.seed(None)
        distanceMatrix = bo.openCsvFile(self.pathString)
        goods = bo.generateGoodsList(112)

        if self.stateString == 'Random':
            startPriorityList = bo.generatePriorityList(112)
        else:
            startPriorityList = bo.generatePriorityListFromCSV(self.stateString)

        try:
            temp = bo.doMagic(self.numIter, self.numPop, self.chance, distanceMatrix, goods, startPriorityList)
        except:
            print('ERROR: run failed to complete')
            print('t acc')

        try:

            bo.saveSingleRunToCSV('single_run_result', temp, startPriorityList)
            clear = lambda: os.system('cls')
            clear()
            print(temp[0])
            self.finishedSig.emit()
            print('Results saved sucessfully')


        except:
            print('\nERROR: run completed but failed to save')

class TestRunThread(QThread):

    testFinSig = pyqtSignal('PyQt_PyObject')

    def __init__(self,parameterVector):

        QThread.__init__(self)

        self.randSeedInput = parameterVector[0]
        print(self.randSeedInput)
        self.iterVectorInput = parameterVector[1]
        self.populationVectorInput = parameterVector[2]
        self.chanceVectorInput = parameterVector[3]

    def __del__(self):

        self.wait()

    def run(self):

        iV = []
        pV = []
        cV = []

        try:

            if self.randSeedInput == 'None':
                print(1)
                randSeed = None
                print('2')
            else:
                randSeed = int(self.randSeedInput)
            for each in self.iterVectorInput.split(','):
                iV.append(int(each))
            for each in self.populationVectorInput.split(','):
                pV.append(int(each))
            for each in self.chanceVectorInput.split(','):
                cV.append(int(each))

            try:
                print(testModule.test(iV, pV, cV, randSeed))
                testResults = testModule.test(iV, pV, cV, randSeed)
                # clear = lambda: os.system('cls')
                # clear()
                print('tests finished')
                self.testFinSig.emit(testResults)
            except:
                print('ERROR: testModule error')

        except:
            print('ERROR: input cannot be prased')

class StartWidget(QWidget):

    pathString = 'tabelaOdleglosci.csv'
    stateString = 'Random'

    def __init__(self):
        super().__init__()
        self.initUIsRun()

    def initUIsRun(self):

        self.btn = QPushButton('Chosse shop layout', self)
        self.btn.clicked.connect(self.showDialogLay)

        self.filebtn = QPushButton('Choose shop state', self)
        self.filebtn.clicked.connect(self.showDialogState)

        self.startbtn = QPushButton('Start')
        self.startbtn.clicked.connect(self.startWrapper)

        self.path = QLineEdit(self)
        self.path.setText(self.pathString)

        self.statepath = QLineEdit(self)
        self.statepath.setText('Random')

        self.numIter = QSpinBox(self)
        self.numIter.setRange(0,1000)
        self.numIter.setValue(10)

        self.numLbl = QLabel(self)
        self.numLbl.setText('Number of iterations')

        self.numPop = QSpinBox(self)
        self.numPop.setRange(0,1000)
        self.numPop.setValue(10)

        self.popLbl = QLabel(self)
        self.popLbl.setText('Size of population')

        self.chance = QSpinBox(self)
        self.chance.setRange(0,100)
        self.chance.setValue(70)

        self.chanceLbl = QLabel(self)
        self.chanceLbl.setText('Mutation chance')

        self.endLbl = QLabel(self)
        self.endLbl.hide()
        self.endLbl.setText('results saved sucessfully!')

        # form layout

        self.layout = QFormLayout()

        self.layout.addRow(self.btn,self.path)
        self.layout.addRow(self.filebtn,self.statepath)
        self.layout.addRow(self.numLbl,self.numIter)
        self.layout.addRow(self.popLbl,self.numPop)
        self.layout.addRow(self.chanceLbl,self.chance)
        self.layout.addRow(self.startbtn)
        self.layout.addRow(self.endLbl)

        '''
        buttonLayout = QHBoxLayout()

        buttonLayout.addWidget(self.startbtn)
        buttonLayout.addWidget(self.savebtn)

        layout.addRow(buttonLayout)
        '''
        self.setLayout(self.layout)

        self.repaint()

    def startWrapper(self):

        pList = [self.numIter.value(),self.numPop.value(),
                      self.chance.value(),self.pathString,
                      self.stateString]
        self.thread = NormalRunThread(pList)
        self.thread.finishedSig.connect(self.updateWidget)
        self.thread.start()

    def showDialogLay(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file')
            print(fname)
        except:
            self.pathString = self.path.get
        self.path.setText(fname[0])
        self.pathString = fname[0]

    def showDialogState(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file')
            print(fname)
        except:
            self.pathString = self.statepath.get
        self.statepath.setText(fname[0])
        self.stateString = fname[0]

    @pyqtSlot()
    def updateWidget(self):

        self.endLbl.show()
        self.repaint()

class TestWidget(QWidget):

    randSeed = 'None'
    pathString = 'tabelaOdleglosci.csv'
    stateString = 'Random'

    def __init__(self):
        super().__init__()

        self.initUITests()

    def testWrapper(self):

        pList = [self.randSeedInput.text(),
                 self.iterVectorInput.text(),
                 self.populationVectorInput.text(),
                 self.chanceVectorInput.text()]
        self.thread = TestRunThread(pList)
        self.thread.testFinSig.connect(self.updateWidget)
        self.thread.start()

    def startTest(self):

        iV = []
        pV = []
        cV = []

        try:

            if self.randSeedInput.text() == 'None':
                randSeed = None
            else:
                randSeed = int(self.randSeedInput.text())
            for each in self.iterVectorInput.text().split(','):
                iV.append(int(each))
            for each in self.populationVectorInput.text().split(','):
                pV.append(int(each))
            for each in self.chanceVectorInput.text().split(','):
                cV.append(int(each))


            try:
                print('no')
                #self.testResults = testModule.test(iV,pV,cV,randSeed)
                #clear = lambda: os.system('cls')
                #clear()
                print('tests finished')
            except:
                print('ERROR: testModule error')

        except:
            print('ERROR: input cannot be prased')

        testModule.test(iV, pV, cV, randSeed)

    def saveResults(self):

        try:
            bo.saveCsvFile(self.testResults)
            print('results saved sucessfully!')
        except:
            print('ERROR: data cannot be saved sucessfully')

    def initUITests(self):
        self.startbtn = QPushButton('Run Test', self)
        self.startbtn.move(10, 38)
        self.startbtn.clicked.connect(self.testWrapper)

        self.savebtn = QPushButton('Save Results', self)
        self.savebtn.move(10, 68)
        self.savebtn.clicked.connect(self.saveResults)

        self.itLbl = QLabel(self)
        self.itLbl.setText('Iteration Vector')

        self.iterVectorInput = QLineEdit(self)

        self.popLbl = QLabel(self)
        self.popLbl.setText('Population Vector')

        self.populationVectorInput = QLineEdit(self)

        self.chLbl = QLabel(self)
        self.chLbl.setText('Chance Vector')

        self.chanceVectorInput = QLineEdit(self)

        self.rndLbl = QLabel(self)
        self.rndLbl.setText('Seed')

        self.randSeedInput = QLineEdit(self)
        self.randSeedInput.setText(self.randSeed)

        self.btn = QPushButton('Chosse shop layout', self)
        self.btn.clicked.connect(self.showDialogLay)

        self.filebtn = QPushButton('Choose shop state', self)
        self.filebtn.clicked.connect(self.showDialogState)

        self.path = QLineEdit(self)
        self.path.setText(self.pathString)

        self.statepath = QLineEdit(self)
        self.statepath.setText('Random')

        # form layout

        layout = QFormLayout()

        layout.addRow(self.btn, self.path)
        layout.addRow(self.filebtn, self.statepath)
        layout.addRow(self.itLbl,self.iterVectorInput)
        layout.addRow(self.popLbl,self.populationVectorInput)
        layout.addRow(self.chLbl,self.chanceVectorInput)
        layout.addRow(self.rndLbl,self.randSeedInput)

        buttonLayout = QHBoxLayout()

        buttonLayout.addWidget(self.startbtn)
        buttonLayout.addWidget(self.savebtn)

        layout.addRow(buttonLayout)

        self.setLayout(layout)

        self.repaint()

    def showDialogLay(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file')
            print(fname)
        except:
            self.pathString = self.path.get
        self.path.setText(fname[0])
        self.pathString = fname[0]

    def showDialogState(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file')
            print(fname)
        except:
            self.pathString = self.statepath.get
        self.statepath.setText(fname[0])
        self.stateString = fname[0]

    @pyqtSlot('PyQt_PyObject')
    def updateWidget(self,data):
        print(data)
        self.testResults = data
        print('dupa')

class MainWindow(QTabWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.addTabs()
        self.adjustSize()
        self.setFixedSize(self.size())
        self.setWindowTitle('Generator trasy')

        self.show()

    def addTabs(self):

        self.tab1 = StartWidget()
        self.tab2 = TestWidget()

        self.addTab(self.tab1,'Single Run')
        self.addTab(self.tab2,'Tests')





