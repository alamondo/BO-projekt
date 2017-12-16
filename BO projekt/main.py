import BOpack as bo
import matplotlib.pyplot as plt
import testModule
import random

# TODO jakies inne mutowanie
# TODO jakies inne krzyzowanie
# TODO testy / dodanie zapisu wynikow do pliku

temp = testModule.test([20],[20],[0,10,20,30,40,50,60,70,80,90,100],None)

testModule.showTestResults(temp)

'''
random.seed(12)
distanceMatrix = bo.openCsvFile('tabelaOdleglosci.csv')
goods = bo.generateGoodsList(112)
priority = bo.generatePriorityList(112)


exSol1 = bo.generateExampleSolution(10,10,goods)
exSol2 = bo.generateExampleSolution(10,10,goods)


cross = bo.crossover(exSol1,exSol2)

print('genom 1:\n',bo.prepareSolution(exSol1),'\ngenom 2:\n',bo.prepareSolution(exSol2),'\nwynik krzyzowania:\n',cross)


plotData = bo.doMagic(50, 50, 30, distanceMatrix, goods, priority)

plt.plot(plotData)
plt.title('temp')
plt.show()
'''