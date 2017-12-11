import BOpack as bo
import random
import matplotlib.pyplot as plt
import numpy as np

def test(a,b):

    random.seed(None)
    distanceMatrix = bo.openCsvFile('tabelaOdleglosci.csv')
    goods = bo.generateGoodsList(112)
    priority = bo.generatePriorityList(112)
    plotData = []
    for i in range(2,a):
        for j in range(2,b):
            print('dupa')
            plotData.append(bo.doMagic(i, j, distanceMatrix, goods, priority))
            #plt.plot(plotData)
            #@plt.show()

    for each in plotData:
        plt.plot(each)
        plt.show()
