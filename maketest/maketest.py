#
#    MAKETEST
#    Copyright (C) 2019-2022 Eval Scuola
#    www.evalscuola.it
#    info@evalscuola.it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.00
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
import sys
import fileinput
import shutil

import copy


# to use random.sample()
import random

from pdfrw import PdfReader, PdfWriter



# https://csatlas.com/python-import-file-module/
# how to import module from a different directory
script_dir = os.path.dirname( __file__ )
# script_dir = os.path.dirname(os.path.abspath(__file__))
# print(script_dir)
modules_dir = os.path.join( script_dir, '..', 'modules' )
sys.path.append( modules_dir )
# print(modules_dir)

#from config import projectName, projectType, versionNumber, \
#                    questionListFileName, latexInputFileName, questionFolderName, \
#                    qNumberFileName, qCodeFileName, qAnswerOrderFileName, qKeyFileName, \
#                    qNumberFile, qCodeFile, qAnswerOrderFile, qKeyFile, \
#                    figureDimension, \
#                    copyFolderName, \
#                    questionListMatrix, \
#                    questionNumber

from module import removeExtension, transposed, csvFileToMatrix, matrixToCsvFile

from projectreader import getProjectFileName #createProjectDictionary , readProject



#import logging
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#logging.debug('This is a log message.')






# it deletes all the auxiliary files after creating the pdf file
# the command to delete the latex file is commented
def latexToPdf(latexFileName, latexFilePath):
    os.chdir(latexFilePath)
    # the LaTeX command is given twice in case LaTeX requires two passes
    os.system("pdflatex -interaction=batchmode " + latexFileName + " > log.log")
    os.system("pdflatex -interaction=batchmode " + latexFileName + " > log.log")
    # the following depends on the particular OS (in this case a Unix OS) - for Windows it has to be changed
    os.system("rm *.log \n rm *.aux")
    # os.system("rm " + latexFileName)
    os.chdir(mainpath)



# it takes a fileName, and a list of replacements,
# and replaces each element in the list with its replacement, producing a string
def replaceTag(fileName, filePath, replacementListMatrix):
    replacedString = ""
    #print len(replacementListMatrix)
    for line in fileinput.input( filePath + "/" + fileName ):
        newline = line

        for i in range(0,len(replacementListMatrix)):
            # print `replacementListMatrix[i][0]`
            newline = newline.replace(replacementListMatrix[i][0], replacementListMatrix[i][1] ) # ('a','b')

        replacedString = replacedString + newline

    return replacedString



# reorders the matrix of questions and adds more informations, namely the order of the answers,
# both in list form [1,2,3,4] and in string form 1234.
# TO BE ADDED: figures, as a number in the original questions
def reorderQuestionListMatrix(vNumber):

    #print `vNumber` + "\n"

    #print `vNumber == 0`

    # global questionListMatrix

    if vNumber == 0:
        order = list(range(1,questionNumber+1))
    else:
        order = random.sample(range(1,questionNumber+1), questionNumber)

    # this is done to avoid affecting the global variable
    #localQuestionListMatrix = [x[:] for x in questionListMatrix] # questionListMatrix.copy()
    localQuestionListMatrix = copy.deepcopy(questionListMatrix)

    #print localQuestionListMatrix

    reorderedQuestionListMatrix = []
    reorderedQuestionListMatrixLine = []


    for j in range(0,questionNumber):
        # questionListMatrixLine is each one of the lines forming reorderedQuestionListMatrix
        reorderedQuestionListMatrixLine = localQuestionListMatrix[order[j]-1]

        # print questionListMatrix[order[j]-1]

        qType = int(reorderedQuestionListMatrixLine[2])

        if vNumber == 0:
            answersOrderList = list(range(1,qType+1))
        else:
            answersOrderList = random.sample(range(1,qType+1), qType)

        reorderedQuestionListMatrixLine.append(answersOrderList)

        answersOrderString = ""
        for k in range(0,qType):
            answersOrderString = answersOrderString + repr(answersOrderList[k])
        reorderedQuestionListMatrixLine.append(answersOrderString)

        answersKey = ""
        if not answersOrderList:
            answersKey = 'X'
        elif answersOrderList[0] == 1:
            answersKey = 'A'
        elif answersOrderList[1] == 1:
            answersKey = 'B'
        elif answersOrderList[2] == 1:
            answersKey = 'C'
        elif answersOrderList[3] == 1:
            answersKey = 'D'
        elif answersOrderList[4] == 1:
            answersKey = 'E'

        reorderedQuestionListMatrixLine.append(answersKey)

        # print questionListMatrixLine
        reorderedQuestionListMatrix.append(reorderedQuestionListMatrixLine)

    #print reorderedQuestionListMatrix
    #print "\n"

    return reorderedQuestionListMatrix




# it takes a questionCode, identifying a question, and produces a questionString,
# a string containing the question in Latex form.
def makeQuestion(questionCode, questionType, answerOrder, figureNumber, tableNumber, textNumber):
    if questionType == 0:
        questionType = int(questionCode[6])

    questionString = r'\item' + "\n"
    questionFile = open( mainpath + "/input/" + questionFolderName + "/" + "q" + questionCode + ".tex", 'r' )
    questionString = questionString + questionFile.read() + "\n"   #.decode('latin1')
    questionFile.close()

    if questionType != 0:
        questionString = questionString + "\t"
        questionString = questionString + r'\begin{enumerate}[label=\protect\squared{\Alph*}]'
        questionString = questionString + "\n"
        for k in range(1,questionType+1):
            l = answerOrder[k-1]
            questionString = questionString + "\t\t"
            questionString = questionString + r'\item '
            answerFile = open( mainpath + "/input/" + questionFolderName + "/" + "q" + questionCode + "a" + repr(l) + ".tex", 'r' )
            questionString = questionString + answerFile.read()
            questionString = questionString + "\n"
        questionString = questionString + "\t"
        questionString = questionString + r'\end{enumerate}'

    if projectType == "BES":
        questionString = questionString + "\n" r'\filbreak' + "\n"

    questionString = questionString +  "\n\n"

    if projectType == "INFO":
        questionString = questionString + r'\emph{' + questionCode + r'}' + "\n\n"

    if not figureNumber == '':
        questionString = questionString.replace('@FIGURE@', repr(figureNumber) )

    if not tableNumber == '':
        questionString = questionString.replace('@TABLE@', repr(tableNumber) )

    if not textNumber == '':
        questionString = questionString.replace('@TEXT@', repr(textNumber) )


    return questionString



# it takes a questionCode, identifying the figure connected to a  question, and produces a figureString,
# a string containing the latex code for including the figure
def makeFigure(questionCode, figureNumber):


    if projectType == "BES":
        figureString = r'\noindent\begin{minipage}{\columnwidth}' + "\n"
        figureString = figureString + "\t" + r'\begin{center}' + "\n"
        figureString = figureString + "\t" + r'\includegraphics[width=7cm]{q' + questionCode + r'-fig.pdf}' +  "\n\n" #[width=4.4cm]
        figureString = figureString + "\t" + r'Figura ' + repr(figureNumber) +  "\n" #Figure
        figureString = figureString + "\t" + r'\end{center}' + "\n"
        figureString = figureString + r'\end{minipage}' + "\n\n\n" +r'\vspace{1cm}'
    else:
        figureString = r'\noindent\begin{minipage}{\columnwidth}' + "\n"
        figureString = figureString + "\t" + r'\begin{center}' + "\n"
        figureString = figureString + "\t" + r'\includegraphics[width=' + figureDimension
        figureString = figureString + r']{q' + questionCode + r'-fig.pdf}' +  "\n\n"
        figureString = figureString + "\t" + r'Figura ' + repr(figureNumber) +  "\n"
        figureString = figureString + "\t" + r'\end{center}' + "\n"
        figureString = figureString + r'\end{minipage}' + "\n\n\n"

    return figureString


# it takes a questionCode, identifying a question, and produces a questionString, a string containing the question.
def makeTable(questionCode, tableNumber):

    tableFile = open( mainpath + "/input/" + questionFolderName + "/" + "q" + questionCode + "-tab.tex", 'r' )
    tableString = tableFile.read() + "\n"
    tableFile.close()

    tableString = tableString.replace('@TABLE@', repr(tableNumber) )

    return tableString

# it takes a questionCode, identifying a question, and produces a questionString, a string containing the question.
def makeText(questionCode, textNumber):

    textFile = open( mainpath + "/input/" + questionFolderName + "/" + "q" + questionCode + "-text.tex", 'r' )
    textString = textFile.read() + "\n"
    textFile.close()

    textString = textString.replace('@TEXT@', repr(textNumber) )

    return textString


def makeLatexFile(latexOutputFileName, vNumber, transposedReorderedQuestionListMatrix):

    questionNumberList, questionCodeList, questionTypeList, questionVersionNumberList, \
        questionFigureList, questionTableList, questionTextList, \
        questionAnswerOrderList, questionAnswerOrderString, questionKeyList = transposedReorderedQuestionListMatrix

    # qNumber = len(questionCodeList)

    # it creates a dictionary that to each figure associates its number
    # it creates a dictionary that to each table associates its number
    # it creates a dictionary that to each text associates its number
    # it creates the strings of questions, figures and tables
    figureNumber = 0
    figureDictionary = {}
    figureDictionary['xxxxxxxxxxxx'] = ''

    tableNumber = 0
    tableDictionary = {}
    tableDictionary['xxxxxxxxxxxx'] = ''

    textNumber = 0
    textDictionary = {}
    textDictionary['xxxxxxxxxxxx'] = ''

    # allTableString, allQuestionString, allFigureString contain LaTeX code to be added
    # inside latexInputFile to create latexOutputFile
    allQuestionString = ""
    allFigureString = ""
    allTableString = ""
    allTextString = ""

    for j in range(0,questionNumber):
        if not questionFigureList[j] == 'xxxxxxxxxxxx' and not questionFigureList[j] in figureDictionary:
            figureNumber = figureNumber + 1
            #print figureNumber
            #print questionFigureList[j]
            figureDictionary[questionFigureList[j]] = figureNumber
            newFigureString = makeFigure(questionFigureList[j], figureNumber)
            allFigureString = allFigureString + newFigureString

        if not questionTableList[j] == 'xxxxxxxxxxxx' and not questionTableList[j] in tableDictionary:
            tableNumber = tableNumber + 1
            #print tableNumber
            #print questionTableList[j]
            tableDictionary[questionTableList[j]] = tableNumber
            newTableString = makeTable(questionTableList[j], tableNumber)
            allTableString = allTableString + newTableString

        if not questionTextList[j] == 'xxxxxxxxxxxx' and not questionTextList[j] in textDictionary:
            textNumber = textNumber + 1
            #print tableNumber
            #print questionTableList[j]
            textDictionary[questionTextList[j]] = textNumber
            newTextString = makeText(questionTextList[j], textNumber)
            allTextString = allTextString + newTextString

        newQuestionString = makeQuestion(questionCodeList[j], int(questionTypeList[j]), questionAnswerOrderList[j],
                                         figureDictionary[questionFigureList[j]], tableDictionary[questionTableList[j]],
                                         textDictionary[questionTextList[j]])
        allQuestionString = allQuestionString + newQuestionString    #encode('latin1')
    #print figureDictionary
    #print tableDictionary



    replacementListMatrix = [["@ver@",repr(vNumber)],["@QUESTIONS@", allQuestionString],
                             ["@FIGURES@", allFigureString],["@TABLES@", allTableString],
                             ["@TEXTS@", allTextString]]
    latexOutputFileString = replaceTag(latexInputFileName, mainpath + "/input/", replacementListMatrix)

    #print latexOutputFileString

    latexOutputFile = open( mainpath + "/output/latex/" + latexOutputFileName, 'w' )
    latexOutputFile.write(latexOutputFileString)    #.decode('latin1')



# it makes the latex and pdf files for the version and adds a line for all relevant files
def makeVersionFiles(vNumber):

    # print questionListMatrix

    reorderedQuestionListMatrix = reorderQuestionListMatrix(vNumber)
    # print reorderedQuestionListMatrix

    transposedReorderedQuestionListMatrix = transposed(reorderedQuestionListMatrix)
    # print transposedReorderedQuestionListMatrix

    questionNumberList, questionCodeList, questionTypeList, questionVersionNumberList, \
        questionFigureList, questionTableList, questionTextList, \
        questionAnswerOrderList, questionAnswerOrderString, questionKeyList = transposedReorderedQuestionListMatrix

    # for version 0 it adds the beginning to all the relevant output files
    if vNumber == 0:
        qNumberFile.write ( "Ordine delle domande \n versione \t" )
        qCodeFile.write ( "Lista delle domande \n versione \t" )
        qAnswerOrderFile.write ( "Ordine delle risposte \n versione \t" )
        qKeyFile.write ( "Lista delle soluzioni \n versione \t" )

        for k in range(0,questionNumber):
            qNumberFile.write ( "q" + repr(k+1) + "\t" )
            qCodeFile.write ( "q" + repr(k+1) + "\t" )
            qAnswerOrderFile.write ( "q" + repr(k+1) + "\t" )
            qKeyFile.write ( "q" + repr(k+1) + "\t" )

        qNumberFile.write ( "\n" )
        qCodeFile.write ( "\n" )
        qAnswerOrderFile.write ( "\n" )
        qKeyFile.write ( "\n" )


    # Adding a line for this version to all the relevant output files
    qNumberFile.write ( repr(vNumber) + "\t" )
    qCodeFile.write ( repr(vNumber) + "\t" )
    qAnswerOrderFile.write ( repr(vNumber) + "\t" )
    qKeyFile.write ( repr(vNumber) + "\t" )

    for k in range(0,questionNumber):
        qNumberFile.write ( questionNumberList[k] + "\t" )
        qCodeFile.write ( questionCodeList[k] + "\t" )
        qAnswerOrderFile.write ( questionAnswerOrderString[k] + "\t" )
        qKeyFile.write ( questionKeyList[k] + "\t" )

    qNumberFile.write ( "\n" )
    qCodeFile.write ( "\n" )
    qAnswerOrderFile.write ( "\n" )
    qKeyFile.write ( "\n" )

    latexOutputFileName = projectName + "-" + repr(vNumber) + ".tex"
    makeLatexFile(latexOutputFileName, vNumber, transposedReorderedQuestionListMatrix)
    latexToPdf(latexOutputFileName, mainpath+"/output/latex")
    # the latex file could be deleted by latexToPdf after creating the pdf file (commented now)
    # os.system("rm " + mainpath +  "/output/latex/" +  projectName + "-" + `vNumber` + ".tex")


    # USES pdfrw
    testWriter.addpages(PdfReader(mainpath + "/output/latex/" +  projectName + "-" + repr(vNumber) + ".pdf").pages)

    # all files in latex folder deleted after
    # os.system("rm " + mainpath + "/output/latex/" +  projectName + "-" + `vNumber` + ".pdf")


# it creates the latex folder that will be deleted on exiting
def makeLatexFolder():

    if not os.path.exists(mainpath + "/output/latex/"):
        os.makedirs(mainpath + "/output/latex/")

    # copying the figures and other files in the /output/latex directory
    # NOTICE: option to copy other files, like other figures, from folder copyFolderName
    # shutil.copyfile( mainpath + "/input/buon-compito.pdf",
    #                          mainpath + "/output/latex/buon-compito.pdf")
    for j in range(0,questionNumber):
        if os.path.exists( mainpath + "/input/" + questionFolderName + "/" + "q" + questionListMatrix[j][1] + "-fig.pdf" ):
            #print j+1
            shutil.copyfile( mainpath + "/input/" + questionFolderName + "/" + "q" + questionListMatrix[j][1] + "-fig.pdf" ,
                             mainpath + "/output/latex/" + "q" + questionListMatrix[j][1] + "-fig.pdf")

    if not os.path.exists(mainpath + "/input/" + copyFolderName + "/"):
        print("Error: missing copy folder.")
    elif not copyFolderName == "":
        sourceFiles = os.listdir(mainpath + "/input/" + copyFolderName + "/")
        # print sourceFiles
        for fileName in sourceFiles:
            fullFileName = os.path.join(mainpath + "/input/" + copyFolderName + "/", fileName)
            # print fullFileName
            if (os.path.isfile(fullFileName)):
                shutil.copy(fullFileName, mainpath + "/output/latex/")

        #shutil.copyfile(src, dst)
        #newQuestionString = makeQuestion(questionCodeList[j], int(questionTypeList[j]), questionAnswerOrderList[j])
        #allQuestionString = allQuestionString + newQuestionString    #encode('latin1')





# it defines all the global variables associated to the project,
# such as projectMatrix, projectName, projectType, versionNumber, etc.
def readProject(projectFileName, mainpath):

        #### LIST OF CONSTANTS ####

    global projectMatrix
    projectMatrix = csvFileToMatrix(projectFileName, mainpath)
    print("projectMatrix: \n" + repr(projectMatrix) + "\n\n")
    # sys.stdout
    #matrixToCsvFile(projectMatrix, `sys.stdout`, "")

    # PROJECT NAME, TYPE AND TOTAL NUMBER OF VERSIONS
    # TO DO: (da separare e verificare anche questionNumber, confrontando con il numero di domande in questionListMatrix )
    global projectName, projectType, versionNumber
    projectName = projectMatrix[0][1]
    projectType = projectMatrix[1][1]
    versionNumber = int(projectMatrix[2][1])

    # INPUT FILE NAMES
    global questionListFileName, latexInputFileName, questionFolderName
    questionListFileName = projectMatrix[5][1]
    latexInputFileName = projectMatrix[6][1]
    questionFolderName = projectMatrix[7][1]

    #OUTPUT FILE NAMES
    global qNumberFileName, qCodeFileName, qAnswerOrderFileName, qKeyFileName
    qNumberFileName = projectMatrix[11][1]
    qCodeFileName = projectMatrix[12][1]
    qAnswerOrderFileName = projectMatrix[13][1]
    qKeyFileName = projectMatrix[14][1]

    #OUTPUT FILE OBJECTS
    global qNumberFile, qCodeFile, qAnswerOrderFile, qKeyFile
    qNumberFile = open( mainpath + "/output/" + qNumberFileName, 'w' )
    qCodeFile = open( mainpath + "/output/" + qCodeFileName, 'w' )
    qAnswerOrderFile = open( mainpath + "/output/" + qAnswerOrderFileName, 'w' )
    qKeyFile = open( mainpath + "/output/" + qKeyFileName, 'w' )

    # dimension of the figures inside the latex text
    global figureDimension
    figureDimension = projectMatrix[21][1]
    # print figureDimension

    # the full content of the folder will be copied to the latex folder
    global copyFolderName
    copyFolderName = projectMatrix[23][1]
    # print copyFolderName

    # using csvFileToMatrix(csvFileName, csvFilePath) to read the list of the questions from file and make a matrix
    global questionListMatrix
    questionListMatrix = csvFileToMatrix(questionListFileName, mainpath + "/input" )

    # NUMBER OF QUESTIONS
    global questionNumber
    questionNumber = len(questionListMatrix)
    #print qNumber

    #### END LIST OF CONSTANTS ####


def main():

    global mainpath
    mainpath = os.getcwd()

    projectFileName = getProjectFileName()

    # readProject defines all the global variables associated to the project
    readProject(projectFileName, mainpath)

    # creating the latex folder that will be deleted on exiting
    makeLatexFolder()

    global testWriter
    testWriter = PdfWriter()

    for vNumber in range(0,versionNumber+1):
        print("Now preparing version " + repr(vNumber) + " (of " + repr(versionNumber) + "+1)...")
        makeVersionFiles(vNumber)

    print("Now binding together the .pdf files of the " + repr(versionNumber) + "+1 versions")

    # saving the pdf file
    os.chdir(mainpath+"/output")
    testWriter.write(projectName + ".pdf")
    os.chdir(mainpath)

    # the latex directory is deleted on exiting
    shutil.rmtree(mainpath + "/output/latex")

    qNumberFile.close()
    qCodeFile.close()
    qAnswerOrderFile.close()
    qKeyFile.close()


main()
