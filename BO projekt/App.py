from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QInputDialog, QApplication, QMainWindow,
                             QAction, qApp, QLabel,QFormLayout,QHBoxLayout,
                             QFileDialog, QSpinBox, QTabWidget)

import BOpack as bo
import sys
import random
import os
import matplotlib.pyplot as plt
import numpy as np
import testModule

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
        self.startbtn.clicked.connect(self.start)

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


        # form layout

        layout = QFormLayout()

        layout.addRow(self.btn,self.path)
        layout.addRow(self.filebtn,self.statepath)
        layout.addRow(self.numLbl,self.numIter)
        layout.addRow(self.popLbl,self.numPop)
        layout.addRow(self.chanceLbl,self.chance)
        layout.addRow(self.startbtn)

        '''
        buttonLayout = QHBoxLayout()

        buttonLayout.addWidget(self.startbtn)
        buttonLayout.addWidget(self.savebtn)

        layout.addRow(buttonLayout)
        '''
        self.setLayout(layout)

        self.repaint()

    def start(self):

        random.seed(None)
        distanceMatrix = bo.openCsvFile(self.pathString)
        goods = bo.generateGoodsList(112)

        if self.stateString == 'Random':
            startPriorityList = bo.generatePriorityList(112)
        else:
            startPriorityList = bo.generatePriorityListFromCSV(self.stateString)

        try:
            temp = bo.doMagic(self.numIter.value(), 10, 10, distanceMatrix, goods, startPriorityList)
        except:
            print('ERROR: run failed to complete')

        try:

            bo.saveSingleRunToCSV('single_run_result',temp,startPriorityList)
            clear = lambda: os.system('cls')
            clear()
            print(temp[0])
            print('results saved sucessfully')
        except:
            print('\nERROR: run completed but failed to save')

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

class TestWidget(QWidget):

    randSeed = 'None'
    pathString = 'tabelaOdleglosci.csv'
    stateString = 'Random'

    def __init__(self):
        super().__init__()

        self.initUITests()

    def startTest(self):

        iV = []
        pV = []
        cV = []

        try:

            if self.randSeedInput.text() == 'Random':
                randSeed = None
            else:
                randSeed = int(self.randSeedInput.text())
            print('tests finished')
            for each in self.iterVectorInput.text().split(','):
                iV.append(int(each))
            print('tests finished')
            for each in self.populationVectorInput.text().split(','):
                pV.append(int(each))
            print('tests finished')
            for each in self.chanceVectorInput.text().split(','):
                cV.append(int(each))


            try:
                print('no')
                self.testResults = testModule.test(iV,pV,cV,randSeed)
                #clear = lambda: os.system('cls')
                #clear()
                print('tests finished')
            except:
                print('ERROR: testModule error')

        except:
            print('ERROR: input cannot be prased')

    def saveResults(self):

        try:
            bo.saveCsvFile(self.testResults)
            print('results saved sucessfully!')
        except:
            print('ERROR: data cannot be saved sucessfully')

    def initUITests(self):
        self.startbtn = QPushButton('Run Test', self)
        self.startbtn.move(10, 38)
        self.startbtn.clicked.connect(self.startTest)

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





