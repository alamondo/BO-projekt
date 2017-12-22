import BOpack as bo
import random
import numpy as np
import os

def test(vectorOfIterNum,vectorOfPopulationSizes,vectorOfCrossChances,randomSeed):
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
                print(' ',np.int16(100 * thingsChecked / numberOfThingsToCheck), '%')
                thingsChecked += 1
                temp = bo.doMagic(eachIterNum, eachPopSize, eachChance, distanceMatrix, goods, priority)
                result = temp[0]
                solution = temp[1]
                data.append([
                    np.int16(result),
                    eachIterNum,
                    eachPopSize,
                    eachChance,
                    bo.showRunDetails(solution,priority),
                ])

    return data
# TODO usprawnic showRunDetails (nie dzia w tej formie zwracania wyniku)
def showTestResults(testResultsMatrix):
# prezentowanie wynikow testow
# ultra biedne

    i = 1
    for each in testResultsMatrix:
        print('\ntest#:',i)
        print('result:                  ',each[0],
              '\nnum of interations:    ',each[1],
              '\npopulation size:       ',each[2],
              '\nchance of crossover:   ',each[3],
              '\nmean piority:          ',each[4][0],
              '\nfinal mean priority:   ',each[4][1],
              '\nnumber of useless runs:',each[4][2],
              '\n')
        i += 1