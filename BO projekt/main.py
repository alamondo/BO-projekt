import BOpack as bo
import matplotlib.pyplot as plt
import testModule
import random

# TODO jakies inne krzyzowanie
# TODO dodanie wyświetlania srednich i najgorszych osobnikow populacji
# TODO testy dziwnych przypadkow
# TODO rozne parametry rozwiazan (nie zawartych w funkcji celu)
# TODO graficzna prezentacja wynikow

'''
temp = testModule.test([100],[150],[60],None)

testModule.showTestResults(temp)

bo.saveCsvFile(temp)

'''
random.seed(2137)
distanceMatrix = bo.openCsvFile('tabelaOdleglosci.csv')
goods = bo.generateGoodsList(112)
startPriorityList = bo.generatePriorityList(112)
#print(startPriorityList)
plotData = bo.doMagic(40, 25, 60, distanceMatrix, goods, startPriorityList )
#plt.plot(plotData)
#plt.title('temp')
#plt.show()
