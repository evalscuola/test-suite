#!/usr/bin/python

#------------------------------------------------------------------------------#
#                                                                              #
#                                                                              #
#                                  SMRT grader                                 #
#               Simple Method for Rating and grading Test results              #
#                                (Antonio Ricco)                               #
#                                                                              #
#------------------------------------------------------------------------------#


import os
import sys
import fileinput

# to add command line options
import argparse

#from Lib import statistics
import numpy


#print(sys.version_info)


# https://csatlas.com/python-import-file-module/
# how to import module from a different directory
script_dir = os.path.dirname( __file__ )
# script_dir = os.path.dirname(os.path.abspath(__file__))
# print(script_dir)
modules_dir = os.path.join( script_dir, '..', 'modules' )
sys.path.append( modules_dir )
# print(modules_dir)


from module import removeExtension, transposed, csvFileToMatrix, matrixToCsvFile

from projectreader import getProjectFileName #createProjectDictionary , readProject

from makegrades import makeGrades





def makeGradesMatrix(tSortedDataMatrix, grades):

   stringGrades = [repr(grade) for grade in grades]
   tSortedDataMatrix.append(stringGrades)


   gradesMatrix = transposed(tSortedDataMatrix)

   # for k in range(0, len(grades)):
   #    gradesLine = []
   #    gradesLine.append(`k+1`)
   #     # gradesLine.append(`grades[k]`)
   #     gradesLine.append(`roundgrades[k]`)
   #    # gradesLine.append(computeLetterGrade(grades[k]))
   #    gradesMatrix.append(gradesLine)

   print("Matrix of the grades: ")
   print(gradesMatrix)
   return gradesMatrix



def main():


        #### LIST OF CONSTANTS ####

    global mainpath
    mainpath = os.getcwd()

    projectFileName = getProjectFileName()

    global projectMatrix
    projectMatrix = csvFileToMatrix(projectFileName, mainpath)
    print("projectMatrix: \n" + repr(projectMatrix) + "\n\n")
    # sys.stdout
    # matrixToCsvFile(projectMatrix, `sys.stdout`, "")

    # PROJECT NAME, TYPE
    global projectName, projectType
    projectName = projectMatrix[0][1]
    projectType = projectMatrix[1][1]

    # AVERAGE AND STANDARD DEVIATION OF THE RESULTS
    global average, standardDev
    average = float(projectMatrix[2][1]) # 7.0
    print("Average: " + repr(average))
    standardDev = float(projectMatrix[3][1]) # 1.2
    print("Standard deviation: " + repr(standardDev))


    # INPUT FILE NAMES
    #dataFileName = raw_input("dataFileName: ")
    #dataFileName = "1A-verifica-mat2-data.csv"
    dataFileName = projectMatrix[7][1]
    print("File of data: " + dataFileName)

    #OUTPUT FILE NAMES
    dataFileOutName = projectMatrix[11][1]
    #print "File of data-out " + dataFileName + ":"


    # matrix with names and scores of the students from dataFile
    global dataMatrix
    dataMatrix = csvFileToMatrix(dataFileName, mainpath + "/input" )
    #print `dataMatrix` + "\n"
    #printMatrix(dataMatrix)

    # number of grades
    global number
    number = len(dataMatrix)
    print("Number of grades: " + repr(number) + "\n")

    #### END LIST OF CONSTANTS ####


    #tDataMatrix = transposed(dataMatrix)
    #print tDataMatrix

    #sortedDataMatrix = sorted(dataMatrix, key=lambda scores: float(scores[2]))
    #print sortedDataMatrix

    # tSortedDataMatrix = transposed(sortedDataMatrix)
    tSortedDataMatrix = transposed(sorted(dataMatrix, key=lambda scores: float(scores[2])))
    #print tSortedDataMatrix

    # names and scores to be transformed in grades, contained in datafile
    # names = tDataMatrix[1]
    scores = list(map(float, tSortedDataMatrix[2]))
    # print "Sorted scores: " + `scores` + "\n"

    print("Average score: " + repr(round(numpy.mean(scores),1))) # + "\n"
    print("Standard deviation of the scores: " + repr(numpy.std(scores, ddof=1)) + "\n")


    grades = makeGrades(number, scores, average, standardDev, precisionIndex = 4)
    #roundgrades = grades


    #gradesMatrix =
    #print makeGradesMatrix(grades)
    gradesMatrix = makeGradesMatrix(tSortedDataMatrix, grades)

    matrixToCsvFile(gradesMatrix, dataFileOutName, mainpath + "/output" )

    #print "Sorted grades: " + `grades`

    #printMatrix(grades)







print("***************  SMRT grader ****************\n")

main()
