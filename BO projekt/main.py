import BOpack as bo
import matplotlib.pyplot as plt

bo.random.seed(12)

distanceMatrix = bo.openCsvFile('tabelaOdleglosci.csv')
goods = bo.generateGoodsList(112)
priority = bo.generatePriorityList(112)

exSol = bo.generateExampleSolution(200, 2, goods)

print(exSol)

bo.prepareSolution(exSol)

#plotData = bo.doMagic(100,20, distanceMatrix, goods, priority)

#plt.plot(plotData)
#plt.show()