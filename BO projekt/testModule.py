import BOpack as bo
import random
import matplotlib.pyplot as plt
import numpy as np
import os

def test(vectorOfIterNum,vectorOfPopulationSizes,vectorOfCrossChances,randomSeed):
# wykonanie algorytmu dla wszystkich kombinacji wartosci w wektorach

    numberOfThingsToCheck = len(vectorOfCrossChances) + len(vectorOfPopulationSizes) + len(vectorOfIterNum)
    thingsChecked = 1

    random.seed(randomSeed)
    distanceMatrix = bo.openCsvFile('tabelaOdleglosci.csv')
    goods = bo.generateGoodsList(112)
    priority = bo.generatePriorityList(112)
    data = []

    for eachIterNum in vectorOfIterNum:
        for eachPopSize in vectorOfPopulationSizes:
            for eachChance in vectorOfCrossChances:
                clear = lambda: os.system('cls')
                clear()
                print(' ',np.int16(100 * thingsChecked / numberOfThingsToCheck), '%')
                thingsChecked += 1
                data.append([
                    bo.doMagic(eachIterNum,eachPopSize,eachChance,distanceMatrix,goods,priority)[-1],
                    eachIterNum,
                    eachPopSize,
                    eachChance
                ])

    return data

def showTestResults(testResultsMatrix):
# prezentowanie wynikow testow
# ultra biedne
# TODO zapis do pliku w celu odczytania w Matlabie

    i = 1
    for each in testResultsMatrix:
        print('test#:',i)
        print('result:',np.int16(each[0]),'\nnum of interations: ',each[1],'\npopulation size:    ',each[2],'\nchance of crossover:',each[3],'\n')
        i += 1