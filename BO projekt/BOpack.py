import os
import csv
import random
import copy
import numpy as np


def generateGoodsList(goodsListSize):
# stworzenie listy ID produktow
    
    temp = []
    
    for i in range(goodsListSize):
        temp.append(i+1)
    
    return temp



def generateExampleSolution(maxWeight, maxNumCourses,goodsList):
# stworzenie losowego przebiegu
# sklep i magazyn sa jednakowe (lustrzane odbicie)
    
    tempMatrix = np.zeros((maxNumCourses,maxWeight), dtype=np.int16 )
    
    for i in range(maxNumCourses):
        for j in range(maxWeight):
            tempMatrix[i][j] = goodsList[random.randint(0,len(goodsList) - 1)]
    
    return tempMatrix



def generatePriorityList(problemSize):
# generowanie maksymalnych ilosci towarow na plkach
# generowanie obecnego stanu sklepu
# obliczanie piorytetu 
    
    tempList = []
    
    for _ in range(problemSize):
        tempTuple = []
        tempTuple.append(random.randint(1, 20))
        tempTuple.append(random.randint(0,tempTuple[0]))
        tempTuple.append(tempTuple[1]/tempTuple[0])
        tempList.append(tempTuple)
    
    return tempList


def mutate(genome,goodsList):
# mutacja pojedynczego przebiegu poprzez podmiane pojedynczego produktu na inny (beda taki sam) wybrany losowo
# TODO poprawienie rozwiazan po mutacji (jakies sortowanie czy cos)
    
    x = random.randint(0,genome[:,1].size-1)
    y = random.randint(0,genome[1,:].size-1)
    genome[x][y] = goodsList[random.randint(0,len(goodsList) - 1)]
    solution = prepareSolution(genome)
    return solution
        
def packIntoNpArray( numberOfCols, numberOfRows):
    print('cols: ',numberOfCols,' rows: ',numberOfRows)
        
def prepareSolution(solution):
# polepaszanie rozwiazania
# sortowanie zrobione
# grupuje produkty i ustawia je w kolejnosci wedlug pierwszego wystapiena
    
    numberOfRows = solution[:,1].size
    numberOfCols = solution[1,:].size
    tempSolution = np.zeros((numberOfRows,numberOfCols), dtype=np.int16)
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
            
        tempMatrix = np.zeros((112,112), dtype=np.int16) 
        
        for i in (range(len(tempList))):
            
            for j in (range(len(tempList))):
                
                tempMatrix[i][j] = tempList[i][j]
        
        return tempMatrix
    return None
    
    
    
def getFitness(solution, distanceMatrix, startPriorityList):
# obliczania wskaznika 'fitu' dla pojedynczego przebiegu
# obliczany jest on tylko dla jednej czesci
# postac tego wskaznika: suma odleglosci poamiedzy produktami w pojedynczych wyjazdach
# (bez powrotu do bazy)
# dodano wskaznik piorytetu 
# TODO rozbudowac
    
    endPriorityList = copy.deepcopy(startPriorityList)
    
    for eachRow in solution:
        for eachCell in eachRow:
            endPriorityList[eachCell-1][1] += 1
            endPriorityList[eachCell-1][2] = endPriorityList[eachCell-1][1]/endPriorityList[eachCell-1][0]
    
    sumOfPriority = 0        
    
    for each in startPriorityList:
        sumOfPriority = sumOfPriority + each[2]
    
    averagePriority = sumOfPriority / len(startPriorityList)
    dist = 0
    
    for i in range(solution[:,1].size): # ilosc powtorzen
        for j in range(solution[1,:].size-1): # masa  przewioziona
            dist = dist + distanceMatrix[solution[i][j]-1][solution[i][j+1]-1]
        dist = dist + 10
    
    return (dist * 0.1) / (averagePriority**2)



def doMagic(numberOfIterations,numberOfIndividuals, distanceMatrix, goodsList, startPriorityList):
# tu sie dzieje magia
# glowna czesc programu 
# tworzymy pule X osobnikow 
# nastepnie mutujemy podczas Y iteracj
# TODO wybor osobnikow po dokonaniu mutacji (teraz robimy dla nich konkurs)
    
    genomeList = []
    bestGenomesList = []

    for _ in range(0,numberOfIndividuals):
        
        tempSol = generateExampleSolution(20,50,goodsList)
        genomeList.append([getFitness(tempSol,distanceMatrix,startPriorityList),tempSol])

    for i in range(0,numberOfIterations):
        
        tempList = []
        tempList.append(genomeList[0])
        
        for j in range(0,numberOfIndividuals-1):
        
            tempSol = mutate(genomeList[j][1],goodsList)
            tempList.append([getFitness(tempSol,distanceMatrix,startPriorityList),tempSol])
        
        tempList.sort(key=lambda list1: list1[0]) # sortowanie tylko po warto�ci fitu array z np nie nadaje si� do sortowania     
        tempListFin = []
        tempListFin.append(tempList[0])
        
        while len(tempListFin) <= len(tempList):
            
            index = random.randint(0,len(tempList)-1)
            index2 = index
            
            while index2 == index:
                index2 = random.randint(0,len(tempList)-1)
            
            if tempList[index][0] <= tempList[index2][0]:
                tempListFin.append(tempList[index])
            else:
                tempListFin.append(tempList[index2])
        
        genomeList = copy.deepcopy(tempListFin)
        bestGenomesList.append((genomeList[0])[0])
        clear = lambda: os.system('cls')
        clear()
        print (' ',(100*i/numberOfIterations),'%')
    
    print('end')
    print ((genomeList[0])[0])
    return bestGenomesList