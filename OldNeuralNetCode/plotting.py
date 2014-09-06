import matplotlib.pyplot as plt


def plotCSV(filename):
    fo = open(filename, "r") 
    count = 0
    for line in fo:
        if count == 0:
            listZero = line.split(",")
        else:
            listOne = line.split(",")
        count+=1

    print len(listZero)
    print len(listOne)
    plotX = range(len(listZero))
    print len(plotX)
    plt.plot(plotX, listZero, "bs", plotX, listOne, "r--")
    plt.show()

plotCSV("plot.csv")


#    prices.reverse()