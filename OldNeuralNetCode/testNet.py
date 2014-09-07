import NeuralNet
from random import randint

def writeCSV(a1, a2):
    fo = open("plot.csv", "w")
    temp = []
    temp.append(','.join(a1))
    temp.append(','.join(a2))
    fo.write(temp[0] + "\n")
    fo.write(temp[1])

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
    prices.reverse()
    return minPrice, maxPrice, prices

def createTests2(pricesTrain, pricesTest, dowTrain, dowTest):
    tests = []
    training = []

    numDays = 31
    for i in range(numDays, len(pricesTrain) - 150):
        temp = []
        for j in range(0, numDays):
            temp.append(pricesTrain[i - j])
        if dowTrain[i - numDays] == 0.0:
            temp.append(1)
        else:
            temp.append((dowTrain[i] - dowTrain[i - numDays]) / dowTrain[i - numDays])
        training.append((temp, [pricesTrain[i + 150]]))

    for i in range(numDays, len(pricesTest) - 150):
        temp = []
        for j in range(0, numDays):
            temp.append(pricesTest[i - j])
        if dowTest[i - numDays] == 0.0:
            temp.append(1)
        else:
            temp.append((dowTest[i] - dowTest[i - numDays]) / dowTest[i - numDays])
        tests.append((temp, [pricesTest[i + 150]]))

    return (training, tests)

def createTests(pricesTrain, pricesTest):
    tests = []
    training = []

    numDays = 20
    for i in range(numDays, len(pricesTrain) - 10):
        temp = []
        for j in range(0, numDays - 10):
            temp.append(pricesTrain[i - j])
        training.append((temp, [pricesTrain[i + 10]]))
    
    for i in range(numDays, len(pricesTest) - 10):
        temp = []
        for j in range(0, numDays - 10):
            temp.append(pricesTest[i - j])
        tests.append((temp, [pricesTest[i + 10]]))    

    return (training, tests)  


trainingPercent = 0.5

minPrice, maxPrice, prices = readCSV("ibm_open.csv")
minDow, maxDow, dow = readCSV("dow.csv")

testData = []
trainData = []

trainDow = []
testDow = []
for i in range(0, int(len(prices) * trainingPercent)):
    trainData.append(prices[i])
    trainDow.append(dow[i])

for i in range(int(len(prices) * trainingPercent) + 1, len(prices)):
    testData.append(prices[i])
    testDow.append(dow[i])


test = createTests2(trainData, testData, trainDow, testDow)
#print test
#test = ([([0,0,0],[0]), ([0,0,1],[0]), ([0,1,1],[1]), ([1,0,1],[1])], [([1,0,0],[0]), ([1,0,1],[1]), ([0,0,0],[0]), ([0,1,1],[1])])

sizes = []
acc = []
plotNet = []
plotReal = []

#for r in range(10, 60, 5):
for i in range(0,1):
<<<<<<< HEAD
    results, nnet, accuracy = NeuralNet.buildNeuralNet(test, 0.1, 0.0000002, [5])
=======
    results, nnet, accuracy = NeuralNet.buildNeuralNet(test, 0.1, 0.00001, [5])
>>>>>>> 26714c785f3a7fdf3a019eaee74b37fda9abbc0e
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
    acc.append(percentError)
    
    print "Price Correctness: " + str(float(correct) / (correct + incorrect))
print "Max: " + str(max(acc))
print "Min: " + str(min(acc))
print "Avg: " + str((sum(acc) / len(acc)))


for i in range(len(plotReal)):
    plotReal[i] = str(plotReal[i])

for i in range(len(plotNet)):
    plotNet[i] = str(plotNet[i])

writeCSV(plotReal, plotNet)
<<<<<<< HEAD
minPrice, maxPrice, prices = readCSV("ibm_open.csv")
=======

minPrice, maxPrice, prices = readCSV("sprint_open.csv")

>>>>>>> 26714c785f3a7fdf3a019eaee74b37fda9abbc0e
days = 31

plotNet = prices[int(len(prices) * trainingPercent): int(len(prices) * trainingPercent) + days]


plotReal = prices[int(len(prices) * trainingPercent): len(prices)]


for i in range(days - 1, len(plotReal) - 1):
    temp = []
    for j in range(i - days - 1, i):
        temp.append(plotNet[j])     
    ret = nnet.feedForward(temp)
    price = ret[len(ret) - 1][0]
   # price = price * (maxPrice - minPrice) + minPrice
    plotNet.append(price)


for i in range(len(plotNet)):
    plotNet[i] = plotNet[i] * (maxPrice - minPrice) + minPrice

for i in range(len(plotReal)):
    plotReal[i] = plotReal[i] * (maxPrice - minPrice) + minPrice

for i in range(len(plotReal)):
    plotReal[i] = str(plotReal[i])

for i in range(len(plotNet)):
    plotNet[i] = str(plotNet[i])

#writeCSV(plotReal, plotNet)
