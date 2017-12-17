import BOpack as bo
import matplotlib.pyplot as plt
import testModule
import random
import numpy as np

# TODO jakies inne mutowanie
# TODO jakies inne krzyzowanie
'''
temp = testModule.test([100,200,300],[25,25,50,50,25],[70],None)

testModule.showTestResults(temp)

bo.saveCsvFile(temp)

'''
random.seed(12)
distanceMatrix = bo.openCsvFile('tabelaOdleglosci.csv')
goods = bo.generateGoodsList(112)
priority = bo.generatePriorityList(112)

plotData = bo.doMagic(250, 100, 70, distanceMatrix, goods, priority)

plt.plot(plotData)
plt.title('temp')
plt.show()
