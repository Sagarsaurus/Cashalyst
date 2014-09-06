import NeuralNet
from random import randint

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
       
def createTests(pricesTrain, pricesTest):
    tests = []
    training = []

    numDays = 60
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
     
minPrice, maxPrice, prices = readCSV("mutual_fund.csv")
testPrices = []
trainPrices = []

for i in range(0, len(prices) * 7 / 10):
    trainPrices.append(prices[i])
for i in range(len(prices) * 7 / 10, len(prices)):
    testPrices.append(prices[i])

    
test = createTests(trainPrices, testPrices)

#print test
#test = ([([0,0,0],[0]), ([0,0,1],[0]), ([0,1,1],[1]), ([1,0,1],[1])], [([1,0,0],[0]), ([1,0,1],[1]), ([0,0,0],[0]), ([0,1,1],[1])])

sizes = []
acc = []
#for r in range(10, 60, 5):
#for i in range(0,2):
results, nnet, accuracy = NeuralNet.buildNeuralNet(test, 0.1, 0.00005, [1])
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
        
    if nnetPrice - knownPrice < knownPrice * 0.035  and nnetPrice - knownPrice > -knownPrice * 0.035:
        correct += 1
    else:
        incorrect += 1
    percentError += abs((nnetPrice - knownPrice)) / knownPrice
percentError /= len(results)
print "PE: " + str(percentError)
#acc.append(float(correct) / (correct + incorrect))

print "Price Correctness: " + str(float(correct) / (correct + incorrect))
#print "Max: " + str(max(acc))
#print "Min: " + str(min(acc))
#print "Avg: " + str((sum(acc) / len(acc)))


#minPrice, maxPrice, prices = readCSV("google_open.csv")
#test = createTests(prices)
#correct = 0
#incorrect = 0
#for r in test[0]:
 #   ret = nnet.feedForward(r[0])
  #  price = ret[len(ret) - 1][0]
  #  price = price * (maxPrice - minPrice) + minPrice
  #  if price - (r[1][0] * (maxPrice - minPrice) + minPrice) < (r[1][0] * (maxPrice - minPrice) + minPrice) * 0.015 and price - (r[1][0] * (maxPrice - minPrice) + minPrice) < -(r[1][0] * (maxPrice - minPrice) + minPrice) * 0.015:
   #     correct += 1
   # else:
    #    incorrect += 1

#print "Price Correctness other: " + str(float(correct) / (correct + incorrect))
        



