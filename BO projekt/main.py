import BOpack as bo
import matplotlib.pyplot as plt
import numpy as np

bo.random.seed(112)

distanceMatrix = bo.openCsvFile('tabelaOdleglosci.csv')
goods = bo.generateGoodsList(112)
priority = bo.generatePriorityList(112)

#exSol = bo.generateExampleSolution(10, 2, goods)

#exSol = np.array([[2,3,5],[4,3,5]])

#print(exSol)

#print(bo.mutate(exSol,goods))

plotData = bo.doMagic(100,50, distanceMatrix, goods, priority)

plt.plot(plotData)
plt.show()