import os
import sys

import fileinput

#import copy

# imported for csv to datafame conversion
import pandas as pd

# imported for csv management
import csv




# - FROM MAKETEST2
def removeExtension(fileName):
    base=os.path.basename(fileName) # only filename without path
    removedExtensionFile = os.path.splitext(base)[0] # extension =  os.path.splitext(base)[1]
    return removedExtensionFile





# it takes a matrix list composed by string elements
# and writes on a .csv file exactly as it is with columns separated by \n
# and rows separated by \n
def printMatrix(inputMatrix):
    for j in range(0, len(inputMatrix)):
        for k in range(0, len(inputMatrix[j])-1):
            sys.stdout.write(inputMatrix[j][k] + "\t")
        sys.stdout.write(inputMatrix[j][len(inputMatrix[j])-1] + "\n" )
    sys.stdout.write("\n" )




# trasposition of matrices  - FROM MAKETEST2
# https://stackoverflow.com/questions/4937491/matrix-transpose-in-python#9622534
def transposed(lists):
   if not lists: return []
   return list(map(lambda *row: list(row), *lists))


# it takes a matrix list composed by string elements
# and writes on a .csv file exactly as it is with columns separated by \t
# and rows separated by \n
def matrixToCsvFile(inputMatrix, csvFileName, csvFilePath):
    outputCsvFile = open( csvFilePath + "/" + csvFileName, 'w' )

    for j in range(0, len(inputMatrix)):
        for k in range(0, len(inputMatrix[j])-1):
            outputCsvFile.write ( str(inputMatrix[j][k]) + "\t" )
        outputCsvFile.write ( str(inputMatrix[j][len(inputMatrix[j])-1]) + "\n" )

    outputCsvFile.close()



# it opens a .csv file with tab as separator and converts it in a matrix list
# it uses fileinput.input
def csvFileToMatrix(csvFileName, csvFilePath, skipRows = 0, skipColumns = 0, csvDelimiter = "\t"):
    outputMatrix = []

    fi = iter(fileinput.input( csvFilePath + "/" + csvFileName ))
    #print(list(fi))

    #print(range(skipRows))

    for i in range(skipRows):
        next(fi)
    #return p.next()

    for line in fi:
        outputMatrixLine = []
        for k in range(skipColumns,line.count(csvDelimiter)+1):
            outputMatrixLine.append(line.split(csvDelimiter)[k].rstrip())  # rstrip() removes \n, \r, etc.
        outputMatrix.append(outputMatrixLine)

    return outputMatrix



# it opens a .csv file with tab as separator and converts it in a matrix list
# WITH PANDAS
def csvFileToMatrix1(csvFileName, csvFilePath):

    df = pd.read_csv(csvFilePath + "/" + csvFileName, sep='\t', header = None ) #, \
            #names = ['item', 'difficulty', 'discrimination', \
            #'keys', 'A', 'B', 'C', 'D', 'empty'])

    # print(df)
    #df_transposed = df.transpose()
    #print(df_transposed)

    outputMatrix = df.values.tolist()

    return outputMatrix


# Creates a list with rows, i.e. a matrix, from a csv file
# FROM check.py
def createList(fileName, CSVDelimiter):
    with open(fileName, newline='') as f:
        reader = csv.reader(f, delimiter=CSVDelimiter)
        l = list(reader)
        # print(l)
        return l
