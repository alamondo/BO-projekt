import random

import BOpack as bo
import matplotlib.pyplot as plt
import testModule

# TODO testy dziwnych przypadkow
# TODO graficzna prezentacja wynikow

'''
temp = testModule.test([100],[100],[0,10,20,30,40,50,60,70,80,90,100],None)

testModule.showTestResults(temp)

bo.saveCsvFile(temp)
'''
'''
random.seed(2137)
distanceMatrix = bo.openCsvFile('tabelaOdleglosci.csv')
goods = bo.generateGoodsList(112)
startPriorityList = bo.generatePriorityList(112)

plotData = bo.doMagic(150, 100, 10, distanceMatrix, goods, startPriorityList )
plt.plot(plotData,color='b')
plt.title('temp')
plt.show()
'''