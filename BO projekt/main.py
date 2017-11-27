import BOpack as bo
import matplotlib.pyplot as plt
import numpy as np

bo.random.seed(112)

distanceMatrix = bo.openCsvFile('tabelaOdleglosci.csv')
goods = bo.generateGoodsList(112)
priority = bo.generatePriorityList(112)

plotData = bo.doMagic(100,50, distanceMatrix, goods, priority)

plt.plot(plotData)
plt.show()