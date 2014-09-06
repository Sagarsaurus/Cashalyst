import NeuralNet
from random import randint

def readCSV():
    fo = open("ibm_open.csv", "r")
    prices = []   
    for line in fo:
        prices.append(float(line))

    minPrice = min(prices)
    maxPrice = max(prices)
    for i in range(len(prices)):
        prices[i] = (prices[i] - minPrice) / (maxPrice - minPrice)
    return minPrice, maxPrice, prices
       
def createTests(prices):
    tests = []
    training = []

    numDays = 60
    for i in range(len(prices) - numDays):
        randomint = randint(0,99)
        temp = []
        average = 0
        for j in range(i + 1, i + numDays + 1):
            temp.append(prices[j])
            average += prices[j]
        average /= numDays
        result = 0
        
 #       if average < prices[i]:
 #          result = 1                

        if randomint > 30:
            training.append((temp, [prices[i]]))
        else:
            tests.append((temp, [prices[i]])) 
    return (training, tests)  
     
minPrice, maxPrice, prices = readCSV()
#print prices
test = createTests(prices)

#print test
#test = ([([0,0,0],[0]), ([0,0,1],[0]), ([0,1,1],[1]), ([1,0,1],[1])], [([1,0,0],[0]), ([1,0,1],[1]), ([0,0,0],[0]), ([0,1,1],[1])])

sizes = []
acc = []
#for r in range(10, 60, 5):
#for i in range(0,10):
results, temp, accuracy = NeuralNet.buildNeuralNet(test, 0.1, 0.00008, [5])
#acc.append(accuracy)
#sizes.append(acc)
correct = 0
incorrect = 0
for r in results:
    print str((r[1] * (maxPrice - minPrice) + minPrice) - (r[0] * (maxPrice - minPrice) + minPrice))
    if (r[1] * (maxPrice - minPrice) + minPrice) - (r[0] * (maxPrice - minPrice) + minPrice) < 2:
        correct += 1
    else:
        incorrect += 1

print correct / (correct + incorrect)
#print "Max: " + str(max(acc))
#print "Min: " + str(min(acc))
#print "Avg: " + str((sum(acc) / len(acc)))
