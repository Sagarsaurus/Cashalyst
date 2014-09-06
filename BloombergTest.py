__author__ = 'kpahawa'


import csv

#Im giong to write you some headers which should guide you

#1. make a function that opens the file and returns the faile handler.
#   Parameters: fileName
#   Return: File object

def getFile():
    print("hello")
    f = open("sample.txt", "r")
    lines = f.readlines()
    for line in lines:
        if line[0:9] == "security ":
            dictName = line[12:len(line)-1]
        elif (line[0] == "d"):
            dictName["date"] = [line[7:len(line)-1]]
        elif (line[0] == "P"):
            dictName["PX_LAST"] = [line[8:len(line)-1]]
        elif(line[0] == "O"):
            dictName["OPEN"] = [line[6:len(line)-1]]
        elif (line[0] == "C"):
            dictName["CUR_MKT_CAP"] =  [line[14:len(line)-1]]
    f.close()
    return dictName




#2. This will be your CSV creater. Hint, do this last once all your dictionaries have been created and everything
# has been parsed.
#   Return: None
#   Parameters: *args

def writeToCSV(*args):
    return None

#3. Use this mthod to convert your file that you return from getFile to a readible csv. Use this as a HELPER function
# for the writeToCSV function
# Parameters: Takes in a file
# returns: Two things: could either be a changed file or be a a CSV file drectly that just gets aggreated into a giant
# CSV in WriteToCSV

def convertFile(aFile):
    return None


