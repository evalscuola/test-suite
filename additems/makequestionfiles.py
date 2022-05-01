#!/usr/bin/python


import os
import sys

import fileinput

#import copy

# imported for csv to datafame conversion
import pandas as pd


# https://csatlas.com/python-import-file-module/
# how to import module from a different directory
script_dir = os.path.dirname( __file__ )
# script_dir = os.path.dirname(os.path.abspath(__file__))
# print(script_dir)
modules_dir = os.path.join( script_dir, '..', 'modules' )
sys.path.append( modules_dir )
# print(modules_dir)

from module import csvFileToMatrix




# PLACE FOR csvFileToMatrix



# it takes a questionCode, identifying a question, and produces all the relevant files
# if they don't exist already
def makeQuestionFiles(questionCode):
    os.chdir(mainpath + "/questions")

    questionType = int(questionCode[6])

    fileNames = ["q" + questionCode + ".tex",  "q" + questionCode + "-info.csv", "q" + questionCode + "-sol.tex"]

    for i in range(1, questionType+1):
        fileNames.append("q" + questionCode + "a" + str(i) + ".tex")


    for fileName in fileNames:
        #fileName = questionCode + ".txt"
        if not os.path.exists(fileName):
            open(fileName, 'w').close()







def main():


    #### LIST OF CONSTANTS ####

    global mainpath
    mainpath = os.getcwd()

    #questionCode = "000000000000"

    # using csvFileToMatrix(csvFileName, csvFilePath) to read the list of the questions from file and make a matrix
    questionListFileName = "makequestionfilelist.csv"
    global questionListMatrix
    questionListMatrix = csvFileToMatrix(questionListFileName, mainpath + "/input" )
    # NUMBER OF QUESTIONS
    global questionNumber
    questionNumber = len(questionListMatrix)

    #if not sys.argv[1] == "":
    #    questionCode = sys.argv[1]
    #    makeQuestionFiles(questionCode)
    #else:

    for k in range(0,questionNumber):
        questionCode = questionListMatrix[k][0]
        #print questionCode
        #print questionCode[6]
        makeQuestionFiles(questionCode)


main()
