import os
import csv
import random
import copy
import numpy as np


def generateGoodsList(goodsListSize):
# stworzenie listy ID produktów 
    
    temp = []
    
    for i in range(goodsListSize):
        temp.append(i+1)
    
    return temp



def generateExampleSolution(maxWeight, maxNumCourses,goodsList):
# stworzenie losowego przebiegu
# sklep i magazyn s¹ jednakowe (lustrzane odbicie)
    
    tempMatrix = np.zeros((maxNumCourses,maxWeight), dtype=np.int16 )
    
    for i in range(maxNumCourses):
        for j in range(maxWeight):
            tempMatrix[i][j] = goodsList[random.randint(0,len(goodsList) - 1)]
    
    return tempMatrix



def generatePriorityList(problemSize):
# generowanie maksymalnych ilosci towarów na pó³kach
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
# mutacja pojedyñczego przebiegu poprzez podmiane pojedyñczego produktu na inny (b¹dŸ taki sam) wybrany losowo 
# TO DO poprawienie rozwi¹zañ po mutacji (jakieœ sortowanie czy coœ)
# moœ soœ
    
    x = random.randint(0,genome[:,1].size-1)
    y = random.randint(0,genome[1,:].size-1)
    genome[x][y] = goodsList[random.randint(0,len(goodsList) - 1)]
    solution = prepareSolution(genome)
    return solution
        
def packIntoNpArray( numberOfCols, numberOfRows):
    print('cols: ',numberOfCols,' rows: ',numberOfRows)
        
def prepareSolution(solution):
# polepaszanie rozwi¹zania
# TO DO chyba wszystko by tu trzeba zrobic
    
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
# otwieroanie pliku csv o zadanej w ciele funkcji wielkoœci 
# w tym wypadku jest to tabela z odleg³oœciami pomiêdzy poszczególnymi produktami
    
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
# obliczania wskaŸnika 'fitu' dla pojedyñczego przebiegu
# obliczany jest on tylko dla jednej czêœi
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
# tu siê dzieje magia
# glowna czesc programu 
# tworzymy pule X osobnikow 
# nastepnie mutujemy podczas Y iteracji
# TO DO wybor osobnikow po dokonaniu mutacji (teraz robimy dla nich konkurs)
    
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
        
        tempList.sort(key=lambda list1: list1[0]) # sortowanie tylko po wartoœci fitu array z np nie nadaje siê do sortowania     
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