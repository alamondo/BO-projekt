import os
import random

import BOpack as bo
import numpy as np


def test(vectorOfIterNum, vectorOfPopulationSizes, vectorOfCrossChances, randomSeed):
    # wykonanie algorytmu dla wszystkich kombinacji wartosci w wektorach

    numberOfThingsToCheck = len(vectorOfCrossChances) * len(vectorOfPopulationSizes) * len(vectorOfIterNum)
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
                print(' ', np.int16(100 * thingsChecked / numberOfThingsToCheck), '%')
                thingsChecked += 1
                temp = bo.testMagic(eachIterNum, eachPopSize, eachChance, distanceMatrix, goods, priority)
                result = temp[0]
                solution = temp[1]
                data.append([
                    np.int16(result),
                    eachIterNum,
                    eachPopSize,
                    eachChance,
                    bo.showRunDetails(solution, priority),
                ])

    return data


def showTestResults(testResultsMatrix):
    # prezentowanie wynikow testow
    # ultra biedne

    i = 1
    for each in testResultsMatrix:
        print('\ntest#:', i,
              '\nresult:                ', each[0],
              '\nnum of iterations:     ', each[1],
              '\npopulation size:       ', each[2],
              '\nchance of crossover:   ', each[3],
              '\nmean priority:         ', each[4][0],
              '\nfinal mean priority:   ', each[4][1],
              '\nnumber of useless runs:', each[4][2],
              '\n')
        i += 1
