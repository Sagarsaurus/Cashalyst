import NeuralNet
from random import randint
import matplotlib.pyplot as plt

def readCSV(filename):
    a = 0.0
    b = 1.0
    fo = open(filename, "r")
    prices = []   
    for line in fo:
        prices.append(float(line))

    minPrice = min(prices)
    maxPrice = max(prices)
    for i in range(len(prices)):
        prices[i] = a + (((prices[i] - minPrice) * (b - a)) / (maxPrice - minPrice))
#    prices.reverse()
    return minPrice, maxPrice, prices


def createTests3(pricesTrain, pricesTest):
    tests = []
    training = []

    numDays = 10
    for i in range(len(pricesTrain[0]) - numDays):
        temp = []
        temp.append(pricesTrain[0][i + 1])
        temp.append(pricesTrain[0][i + 1] - pricesTrain[0][i + numDays])
        temp.append(pricesTrain[1][i + 1])
        temp.append(pricesTrain[2][i + 1])
        training.append((temp, [pricesTrain[0][i]]))

    for i in range(len(pricesTest[0]) - numDays):
        temp = []
        temp.append(pricesTest[0][i + 1])
        temp.append(pricesTest[0][i + 1] - pricesTest[0][i + numDays])
        temp.append(pricesTest[1][i + 1])
        temp.append(pricesTest[2][i + 1])
        tests.append((temp, [pricesTest[0][i]]))
    return (training, tests)

def createTests2(pricesTrain, pricesTest):
    tests = []
    training = []
  
    numDays = 100
    for i in range(len(pricesTrain[0]) - numDays):
        temp = []
        temp.append(pricesTrain[0][i + 1])
        temp.append(pricesTrain[0][i + 1] - pricesTrain[0][i + numDays])
        training.append((temp, [pricesTrain[0][i]]))
  
    for i in range(len(pricesTest[0]) - numDays):
        temp = []
        temp.append(pricesTest[0][i + 1])
        temp.append(pricesTest[0][i + 1] - pricesTest[0][i + numDays])
        tests.append((temp, [pricesTest[0][i]])) 
    return (training, tests)

 
def createTests(pricesTrain, pricesTest):
    tests = []
    training = []

    numDays = 6
    for i in range(len(pricesTrain) - numDays):
        temp = []
        for j in range(i + 1, i + numDays + 1):
            temp.append(pricesTrain[j])
        training.append((temp, [pricesTrain[i]]))
    
    for i in range(len(pricesTest) - numDays):
        temp = []
        for j in range(i + 1, i + numDays + 1):
            temp.append(pricesTest[j])
        tests.append((temp, [pricesTest[i]])) 

    return (training, tests)  


allDataMin = []
allDataMax = []
allData = []

minPrice, maxPrice, prices = readCSV("ibm_open.csv")
#minBull, maxBull, bull = readCSV("google_bullish.csv")
#minBear, maxBear, bear = readCSV("google_bearish.csv")

allDataMin.append(minPrice)
allDataMax.append(maxPrice)
allData.append(prices)

#allDataMin.append(minBull)
#allDataMax.append(maxBull)
#allData.append(bull)

#allDataMin.append(minBear)
#allDataMax.append(maxBear)
#allData.append(bear)

testData = []
trainData = []

tempPrices = []
tempBull = []
tempBear = []
for i in range(0, min([len(prices)]) * 3 / 10):
    tempPrices.append(prices[i])
 #   tempBull.append(bull[i])
 #   tempBear.append(bear[i])

testData.append(tempPrices)
#trainData.append(tempBull)
#trainData.append(tempBear)

tempPrices = []
#tempBull = []
#tempBear = []
for i in range(min([len(prices)]) * 3 / 10, min([len(prices)])):
    tempPrices.append(prices[i])
 #   tempBull.append(bull[i])
  #  tempBear.append(bear[i])
trainData.append(tempPrices)
#testData.append(tempBull)
#testData.append(tempBear)

test = createTests2(trainData, testData)
#print test
#test = ([([0,0,0],[0]), ([0,0,1],[0]), ([0,1,1],[1]), ([1,0,1],[1])], [([1,0,0],[0]), ([1,0,1],[1]), ([0,0,0],[0]), ([0,1,1],[1])])

sizes = []
acc = []
plotNet = []
plotReal = []

#for r in range(10, 60, 5):
for i in range(0,1):
    results, nnet, accuracy = NeuralNet.buildNeuralNet(test, 0.1, 0.00008, [5])
#    acc.append(accuracy)
#sizes.append(acc)
    correct = 0
    incorrect = 0
    percentError = 0.0
    a = 0.0
    b = 1.0
    for r in results:
        nnetPrice = ((r[1] * (maxPrice - minPrice) - a) / (b - a)) + minPrice
        knownPrice = ((r[0] * (maxPrice - minPrice) - a) / (b - a)) + minPrice
        plotNet.append(nnetPrice)
        plotReal.append(knownPrice) 
        if nnetPrice - knownPrice < knownPrice * 0.015  and nnetPrice - knownPrice > -knownPrice * 0.015:
            correct += 1
        else:
            incorrect += 1
        percentError += abs((nnetPrice - knownPrice)) / knownPrice
    percentError /= len(results)
    print "PE: " + str(percentError)
    acc.append(float(correct) / (correct + incorrect))

    print "Price Correctness: " + str(float(correct) / (correct + incorrect))
print "Max: " + str(max(acc))
print "Min: " + str(min(acc))
print "Avg: " + str((sum(acc) / len(acc)))

plotNet.reverse()
plotReal.reverse()
plotX = range(len(plotNet))

#plt.plot(plotX,plotNet,"r--", plotX, plotReal, "bs")
#plt.show()

minPrice, maxPrice, prices = readCSV("ibm_open.csv")
temp = prices[(len(prices) * 3 / 10) - 100:(len(prices) * 3 / 10)]

plotReal = prices[0:len(prices) * 3 / 10 + 1]

plotNet = temp
plotNet.reverse()
plotReal.reverse()
print plotNet
print "-----------------------------------------------------------------------"
print plotReal
for i in range(99, len(plotReal) - 1):
    ret = nnet.feedForward([plotNet[i],plotNet[i] - plotNet[i - 100]])
    price = ret[len(ret) - 1][0]
   # price = price * (maxPrice - minPrice) + minPrice
    plotNet.append(price)

for i in range(len(plotNet)):
    plotNet[i] = plotNet[i] * (maxPrice - minPrice) + minPrice

for i in range(len(plotReal)):
    plotReal[i] = plotReal[i] * (maxPrice - minPrice) + minPrice
plotX = range(len(plotNet))
plt.plot(plotX,plotNet,"r--", plotX, plotReal, "bs")
plt.show()
