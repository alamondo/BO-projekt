import copy
import csv
import datetime
import random
import sys

import matplotlib.pyplot as plt
import numpy as np


def generateGoodsList(goodsListSize):
    # stworzenie listy ID produktow

    temp = []

    for i in range(goodsListSize):
        temp.append(i + 1)

    return temp


def generateExampleSolution(maxWeight, maxNumCourses, goodsList):
    # stworzenie losowego przebiegu
    # sklep i magazyn sa jednakowe (lustrzane odbicie)

    tempMatrix = np.zeros((maxNumCourses, maxWeight), dtype=np.int16)

    for i in range(maxNumCourses):
        for j in range(maxWeight):
            tempMatrix[i][j] = goodsList[random.randint(0, len(goodsList) - 1)]

    return tempMatrix


def generatePriorityList(problemSize):
    # generowanie maksymalnych ilosci towarow na plkach
    # generowanie obecnego stanu sklepu
    # obliczanie piorytetu

    prioList = []

    for _ in range(problemSize):
        tempTuple = []
        tempTuple.append(random.randint(1, 20))
        tempTuple.append(random.randint(0, tempTuple[0]))
        tempTuple.append(tempTuple[1] / tempTuple[0])
        prioList.append(tempTuple)

    return prioList


def mutate(genome, goodsList):
    # mutacja pojedynczego przebiegu poprzez podmiane pojedynczego produktu na inny (badz taki sam) wybrany losowo

    x = random.randint(0, genome[:, 1].size - 1)
    y = random.randint(0, genome[1, :].size - 1)
    genome[x][y] = goodsList[random.randint(0, len(goodsList) - 1)]
    solution = prepareSolution(genome)

    return solution


def mutatention(genome, goodsList):
    # mutacja pojedynczego przebiegu poprzez podmiane pojedynczego produktu wystepujacy obok

    x = random.randint(0, genome[:, 1].size - 1)
    y = random.randint(0, genome[1, :].size - 1)

    if x == 0 and y == 0:
        genome[x + 1][y + 1] = genome[x][y]
    elif x == 0 and (y == genome[1, :].size - 1):
        genome[x + 1][y - 1] = genome[x][y]
    elif (x == genome[:, 1].size - 1) and y == 0:
        genome[x - 1][y + 1] = genome[x][y]
    else:
        genome[x - 1][y - 1] = genome[x][y]

    solution = prepareSolution(genome)

    return solution


def crossover(genome1, genome2):
    # skrzyzowanie dwoch osobnikow poprzez przeciecie ich w polowie
    # a nastepnie dolozenie drugiej czesci drugiego osobnika do pierwszej pierszego
    # nastepnie poprawiamy rozwiazanie

    numCourses = genome1[:, 1].size
    newGenome = copy.deepcopy(genome1)
    cutPoint = np.int16(np.floor(numCourses / 2))

    for i in range(cutPoint, numCourses):
        newGenome[i, :] = genome2[i, :]

    solution = prepareSolution(newGenome)

    return solution


def prepareSolution(solution):
    # polepaszanie rozwiazania
    # sortowanie zrobione
    # grupuje produkty i ustawia je w kolejnosci wedlug pierwszego wystapiena

    numberOfRows = solution[:, 1].size
    numberOfCols = solution[1, :].size
    tempSolution = np.zeros((numberOfRows, numberOfCols), dtype=np.int16)
    orderOfTransportedGoods = []

    for eachRow in solution:
        for eachCell in eachRow:
            if not (eachCell in orderOfTransportedGoods):
                orderOfTransportedGoods.append(eachCell)

    stupidTempList = []

    for each in orderOfTransportedGoods:
        for _ in range(np.count_nonzero(solution == each)):
            stupidTempList.append(each)

    stupidTempList.reverse()

    for i in range(numberOfRows):
        for j in range(numberOfCols):
            tempSolution[i][j] = stupidTempList.pop()

    return tempSolution


def openCsvFile(fileName):
    # otwieroanie pliku csv o zadanej w ciele funkcji wielkosci
    # w tym wypadku jest to tabela z odleglosciami pomiedzy poszczegolnymi produktami

    with open(fileName, 'rt') as csvfile:

        tempList = []
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in spamreader:
            tempList.append(row)

        tempMatrix = np.zeros((112, 112), dtype=np.int16)

        for i in (range(len(tempList))):
            for j in (range(len(tempList))):
                tempMatrix[i][j] = tempList[i][j]

        return tempMatrix
    return None


def saveCsvFile(input):
    # zapisuje dane z testow do pliku csv z timestampem

    now = list(str(datetime.datetime.now()).split('.')[0])
    now[10] = '_'
    now[13] = '-'
    now[16] = '-'
    stamp = "".join(now)

    ofile = open('tests/' + stamp + '.csv', "w", newline='')
    writer = csv.writer(ofile, delimiter=',')
    writer.writerow(['fit', 'numOfIter', 'popSize', 'chance'])

    for row in input:
        data = []
        for each in row:
            data.append(str(each))

        writer.writerow(data)

    ofile.close()


def getFitness(solution):
    # obliczania wskaznika 'fitu' dla pojedynczego przebiegu
    # obliczany jest on tylko dla jednej czesci
    # postac tego wskaznika: suma odleglosci poamiedzy produktami w pojedynczych wyjazdach
    # (bez powrotu do bazy)
    # dodano wskaznik piorytetu

    global distMatrix
    global prioList

    punishment = 0
    endPriorityList = copy.deepcopy(prioList)

    for eachRow in solution:
        for eachCell in eachRow:
            if endPriorityList[eachCell - 1][1] < endPriorityList[eachCell - 1][0]:
                endPriorityList[eachCell - 1][1] += 1
                endPriorityList[eachCell - 1][2] = endPriorityList[eachCell - 1][1] / endPriorityList[eachCell - 1][0]
            else:
                punishment += 10

    sumOfPriority = 0

    for each in endPriorityList:
        sumOfPriority += each[2]

    averagePriority = sumOfPriority / len(endPriorityList)
    dist = 0

    for i in range(solution[:, 1].size):  # ilosc powtorzen
        for j in range(solution[1, :].size - 1):  # masa  przewioziona
            dist += distMatrix[solution[i][j] - 1][solution[i][j + 1] - 1]
        dist += 10

    return dist / averagePriority + punishment


def chooseNewListOfGenomes(oldList):
    # wybieranie nowej listy osobnikow
    # wyboru dokonujemy za pomoca turnieju
    # wyboru dokonujemy za pomoca rozkladu kwadratowego
    newList = []
    newList.append(oldList[0])
    oldListLen = len(oldList)

    while len(newList) <= oldListLen:
        index = np.int16(np.floor(np.sqrt(random.randint(1, oldListLen * oldListLen))))
        newList.append(oldList[oldListLen - index])

    '''
    while len(newList) <= len(oldList):
        [index,index2] = generateTwoRandIndx(oldList)
        if oldList[index][0] <= oldList[index2][0]:
            newList.append(oldList[index])
        else:
            newList.append(oldList[index2])
    '''
    genomeList = copy.deepcopy(newList)

    return genomeList


def generateTwoRandIndx(listOfGenomes):
    index = random.randint(0, len(listOfGenomes) - 1)
    index2 = index

    while index2 == index:
        index2 = random.randint(0, len(listOfGenomes) - 1)

    return [index, index2]


def generateSolFitnessTuple(solution, results, it):
    results[it] = [getFitness(solution), solution]
    return None


def showRunDetails(solution, prioList):
    endPriorityList = copy.deepcopy(prioList)
    sumOfPriority = 0
    for each in endPriorityList:
        sumOfPriority += each[2]

    averagePriority = sumOfPriority / len(endPriorityList)
    # print('\npoczatkowy sredni priorytet',averagePriority)
    numOfUselessRuns = 0
    for eachRow in solution:
        for eachCell in eachRow:
            if endPriorityList[eachCell - 1][1] < endPriorityList[eachCell - 1][0]:
                endPriorityList[eachCell - 1][1] += 1
                endPriorityList[eachCell - 1][2] = endPriorityList[eachCell - 1][1] / endPriorityList[eachCell - 1][0]
            else:
                numOfUselessRuns += 1

    sumOfPriority = 0
    for each in endPriorityList:
        sumOfPriority += each[2]

    finalAveragePriority = sumOfPriority / len(endPriorityList)
    # print('koncowy sredni priorytet', finalAveragePriority)
    # print('liczba niepotrzebnie przewiezionych towarow: ',numOfUselessRuns)
    # for i in range(len(endPriorityList)-1):
    #    print('bylo: %i jest: %i max: %i' %(prioList[i][1],endPriorityList[i][1],prioList[i][0]))

    return (averagePriority, finalAveragePriority, numOfUselessRuns)


def saveSingleRunToCSV(fpath,result):

    now = list(str(datetime.datetime.now()).split('.')[0])
    now[10] = '_'
    now[13] = '-'
    now[16] = '-'
    stamp = "".join(now)

    ofile = open('results/result_' + stamp + '.csv', "w", newline='')
    writer = csv.writer(ofile, delimiter=',')
    writer.writerow(['cost:',result[0]])

    for row in result[1]:
        data = []
        for each in row:
            data.append(str(each))

        writer.writerow(data)

    ofile.close()


def doMagic(numberOfIterations, numberOfIndividuals, chanceOfCrossover, distanceMatrix, goodsList, startPriorityList):
    # tu sie dzieje magia
    # glowna czesc programu
    # nastepnie mutujemy podczas Y iteracji
    # wybieramy pomiedzy mutacja a krzyzowaniem za pomoca 'ruletki'
    # zachowujemy najlepszy osobnik z poprzedniej iteracji
    # wybieramy nowa liste osobnik

    global prioList
    prioList = startPriorityList

    global distMatrix
    distMatrix = distanceMatrix

    bestGenomesList = []

    # generowanie poczatkowej listy genowmow

    genomeList = []
    plt.ion()
    for _ in range(0, numberOfIndividuals):
        tempSol = generateExampleSolution(20, 20, goodsList)
        genomeList.append([getFitness(tempSol), tempSol])

    # wykonanie zadanej ilosci iteracji

    for i in range(0, numberOfIterations):
        start = datetime.datetime.now()
        tempList = []
        tempList.append(genomeList[0])

        # mutowanie badz krzyzowanie

        for j in range(1, numberOfIndividuals - 1):
            randomNumber = random.randint(1, 100)

            if randomNumber > chanceOfCrossover:
                tempSol = mutate(genomeList[j][1], goodsList)
            else:
                [index, index2] = generateTwoRandIndx(genomeList)
                tempSol = crossover(genomeList[index][1], genomeList[index2][1])

            # tempList.append(tempSol)                            # dla wielowatkowosci
            tempList.append([getFitness(tempSol), tempSol])  # zwyklego liczenia


        # sortowanie tylko po wartosci fitu
        # array z np nie nadaje sie do sortowania

        tempList.sort(key=lambda list1: list1[0])
        genomeList = chooseNewListOfGenomes(tempList)
        genomeList.sort(key=lambda list1: list1[0])
        bestGenomesList.append([(genomeList[0])[0], (genomeList[np.int16(np.floor(len(genomeList) / 2))])[0],
                                (genomeList[-1])[0]])  # zapisywanie najlepszego i najgorszego osobnika
        timeOfiteration = datetime.datetime.now() - start

        print('\r % 3.2f' % (100 * i / numberOfIterations), '% remaining time: ',
              ((numberOfIterations - i) * timeOfiteration).seconds, 's', end='')
        sys.stdout.flush()
        '''
        plt.plot(bestGenomesList,color='b')
        plt.title('temp')
        plt.show()
        plt.pause(0.0001)
        '''

    #return bestGenomesList
    return (genomeList[0])

def testMagic(numberOfIterations, numberOfIndividuals, chanceOfCrossover, distanceMatrix, goodsList,
              startPriorityList):

    # dawne doMagic w wersji do testów

    global prioList
    prioList = startPriorityList

    global distMatrix
    distMatrix = distanceMatrix

    bestGenomesList = []

    # generowanie poczatkowej listy genowmow

    genomeList = []
    plt.ion()
    for _ in range(0, numberOfIndividuals):
        tempSol = generateExampleSolution(20, 20, goodsList)
        genomeList.append([getFitness(tempSol), tempSol])

    # wykonanie zadanej ilosci iteracji

    for i in range(0, numberOfIterations):
        start = datetime.datetime.now()
        tempList = []
        tempList.append(genomeList[0])

        # mutowanie badz krzyzowanie

        for j in range(1, numberOfIndividuals - 1):
            randomNumber = random.randint(1, 100)

            if randomNumber > chanceOfCrossover:
                tempSol = mutate(genomeList[j][1], goodsList)
            else:
                [index, index2] = generateTwoRandIndx(genomeList)
                tempSol = crossover(genomeList[index][1], genomeList[index2][1])

            # tempList.append(tempSol)                            # dla wielowatkowosci
            tempList.append([getFitness(tempSol), tempSol])  # zwyklego liczenia

        # sortowanie tylko po wartosci fitu
        # array z np nie nadaje sie do sortowania

        tempList.sort(key=lambda list1: list1[0])
        genomeList = chooseNewListOfGenomes(tempList)
        genomeList.sort(key=lambda list1: list1[0])
        bestGenomesList.append([(genomeList[0])[0], (genomeList[np.int16(np.floor(len(genomeList) / 2))])[0],
                                (genomeList[-1])[0]])  # zapisywanie najlepszego i najgorszego osobnika
        timeOfiteration = datetime.datetime.now() - start

        print('\r % 3.2f' % (100 * i / numberOfIterations), '% remaining time: ',
              ((numberOfIterations - i) * timeOfiteration).seconds, 's', end='')
        sys.stdout.flush()
        '''
        plt.plot(bestGenomesList,color='b')
        plt.title('temp')
        plt.show()
        plt.pause(0.0001)
        '''

    # return bestGenomesList
    return (genomeList[0])

