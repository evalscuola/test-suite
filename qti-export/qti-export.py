#!/usr/bin/python

#------------------------------------------------------------------------------#
#                                                                              #
#                                                                              #
#                        QTI-EXPORT based on MAKETEST                          #
#                            (Mac OS X version)                                #
#                               Antonio Ricco                                  #
#                                                                              #
#------------------------------------------------------------------------------#


import os
import sys
import fileinput
import shutil

import copy

# to add command line options
import argparse

# to use random.sample()
import random

from pdfrw import PdfReader, PdfWriter

from latex2mathmlMOD.converterMOD import convert


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


#import logging
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#logging.debug('This is a log message.')




# https://rosettacode.org/wiki/Strip_comments_from_a_string#Python
def remove_comments(line, sep):
    for s in sep:
        i = line.find(s)
        if i >= 0:
            line = line[:i]
    return line.strip()



# it takes a latex string and eliminates comments and substitutes $...$ with \(...\) (String)
def cleanLatex(latexString):

    # print(latexString)

    latexStrings = latexString.split("\n")
    # print(latexStrings)

    cleanLatexStrings = []
    for line in latexStrings:
        line = line.replace("\%", "&#37;" )
        line = remove_comments(line, "%")
        line = line.replace("&#37;", "%" )
        line = " " + line + " "

        line = line.replace('\)', '$')
        line = line.replace('\(', '$')
        line = line.replace('\displaystyle ', "")
        # line = line.replace('$ ', '\) ' )
        # line = line.replace('$.', '\).' )
        # line = line.replace('$;', '\);' )
        # line = line.replace('$:', '\):' )
        # line = line.replace('$,', '\),' )
        # line = line.replace(' $', ' \(' ) # \displaystyle{}
        line = line.replace("$^","${\ }^")
        line = line.replace(r"\begin{matrix}", r"")
        line = line.replace(r"\end{matrix}", r"")
        line = line.replace(r"\begin{array}{l}", r"")
        line = line.replace(r"\end{array}", r"")
        line = line.replace(r"\\", r"")
        line = line.replace(r"\left\{", r"")
        line = line.replace(r"\right.", r"")
        line = line.replace(r"\right)", r")")
        line = line.replace(r"\left(", r"(")

        line = line.replace(r"\emph", r"")


        line = line.replace(r"\ ", r"\;")



        # line = line.replace(r"\begin{matrix}", r"\begin{array}{l}")
        # line = line.replace(r"\end{matrix}", r"\end{array}")


        line = line.replace(" alla fine del testo", "" )
        line = line.replace('&', "&amp;" )
        line = line.replace('<', "&lt;" )
        line = line.replace('>', "&gt;" )
        line = line.replace('\euro', "€" )




        line = line.lstrip(" ")
        line = line.rstrip(" ")
        line = line + " "

        cleanLatexStrings.append(line)
    # print(cleanLatexStrings)

    cleanLatexString = "".join(cleanLatexStrings)

    # print(cleanLatexString)
    return cleanLatexString


# it only cleans the latex string
def convertLatexStringToMathML2(latexString):

    return cleanLatex(latexString)



def convertLatexStringToMathML(latexString):

    latexString  = cleanLatex(latexString)

    latexStrings = []
    newLatexStrings = []
    convertedStrings = []
    # latexStrings.append("")


    while (latexString != ""):
        latexStrings = latexString.partition("$")
        # print(latexStrings[2])
        newLatexStrings.append(latexStrings[0])
        newLatexStrings.append(latexStrings[1])
        latexString = latexStrings[2]

    # print(convertedStrings)

    counter = 0
    for string in newLatexStrings:
        # print(string)
        if (string == "$"):
            counter = counter + 1
        else:
            if (counter % 2 == 0):
                string = string.replace("{", "")
                string = string.replace("}", "")
                string = string.replace("\dots", "…" )
                convertedStrings.append(string)
            else:
                newstring = string
                # print(string)
                newstring = convert(string)
                beginstring = r'<m:math>' + "\n" + '<m:semantics>' + "\n" + '<m:mstyle displaystyle="true" scriptlevel="0">'
                newstring = newstring.replace(r'<m:math>', beginstring)
                # newstring = newstring.replace('</m:mrow></m:math>', r'</m:mrow></m:mstyle><m:annotation encoding="latex">' + string + r'</m:annotation></m:semantics></m:math>')
                # newstring = newstring.replace('<m:math xmlns="http://www.w3.org/1998/Math/MathML">', r'<m:math><m:semantics><m:mstyle displaystyle="true" scriptlevel="0">')
                # newstring = newstring.replace('</m:math>', r'</m:mstyle><m:annotation encoding="latex">' + string + r'</m:annotation></m:semantics></m:math>')
                # newstring = newstring.replace('<m:math xmlns="http://www.w3.org/1998/Math/MathML">', '<m:math xmlns="http://www.w3.org/1998/Math/MathML">')
                # newstring = newstring.replace('</m:math>', '</m:math>')

                # newstring = newstring.replace('<m:math xmlns="http://www.w3.org/1998/Math/MathML">', '<m:math xmlns="http://www.w3.org/1998/Math/MathML"><m:mstyle displaystyle="true">') #
                endstring =  r'</m:mstyle>' + "\n" + r'<m:annotation encoding="latex">' + string + r'</m:annotation>' + "\n"
                endstring = endstring + r'</m:semantics>' + "\n" + r'</m:math>'
                newstring = newstring.replace('</m:math>', endstring)
                # <m:annotation encoding="latex">' + string + '</m:annotation>
                # newstring = newstring.replace('<m:mrow>', '<m:mrow class="MJX-TeXAtom-ORD">') # <m:annotation encoding="latex">' + string + '</m:annotation>


                # newstring = newstring.replace("&#x02212;", "−")
                # newstring = newstring.replace("&#x00028;", "(")
                # newstring = newstring.replace("&#x00029;", ")")

                convertedStrings.append(newstring)

    # print(convertedStrings)


    convertedString  = "".join(convertedStrings)
    # print(convertedString)

    return convertedString

def makeQTIFigure(questionCode):

    figureString = r'<div> </div>' + "\n"
    figureString = figureString + r'<div><img src="' + questionCode + r'-fig.png"'
    figureString = figureString + r'alt="' + questionCode + r' fig" width="61%" type="image/png"/></div>'

    return figureString


# it takes a questionCode, identifying a question, and produces a QTIQuestionString, a string containing the xml QTI version of the question.
# based on makeQuestion
def makeQTIQuestion(questionCode, questionType, figureCode):
    if questionType == 0:
        questionType = int(questionCode[6])

    QTIModelFile = open( mainpath + "/input/" + "qti-model.xml", 'r' )
    QTIQuestionString = QTIModelFile.read()
    QTIModelFile.close()

    questionString = "\n" + "\t\t" + r'<prompt>' # <m:math></m:math>
    questionFile = open( mainpath + "/input/" + questionFolderName + "/" + "q" + questionCode + ".tex", 'r' )
    questionString = questionString + convertLatexStringToMathML(questionFile.read()) + "\n"   #.decode('latin1') cleanLatex(questionFile.read())
    questionFile.close()

    if not figureCode == 'xxxxxxxxxxxx':
        questionString = questionString + makeQTIFigure(figureCode) + "\n"

    questionString = questionString + r'</prompt>' + "\n"

    choices = ["A","B","C","D","E","F"]
    if questionType != 0:
        # questionString = questionString + "\t"
        # questionString = questionString + r'\begin{enumerate}[label=\protect\squared{\Alph*}]'
        # questionString = questionString + "\n"
        for k in range(1,questionType+1):
            # l = answerOrder[k-1]
            questionString = questionString + "\t\t"
            questionString = questionString + r'<simpleChoice identifier="' + choices[k-1] + r'" fixed="false" showHide="show">'
            answerFile = open( mainpath + "/input/" + questionFolderName + "/" + "q" + questionCode + "a" + repr(k) + ".tex", 'r' )
            questionString = questionString + convertLatexStringToMathML(answerFile.read())   # cleanLatex(answerFile.read())
            questionString = questionString + r'</simpleChoice>' + "\n"
        # questionString = questionString + "\t"
        # questionString = questionString + r'\end{enumerate}'

    # questionString = questionString +  "\n\n"
    # print questionString

    # @IDENTIFIER@, @TITLE@, @LABEL@, @QUESTION@


    # if projectType == "INFO":
    #     questionString = questionString + r'\emph{' + questionCode + r'}' + "\n\n"

    # if not figureNumber == '':
    questionString = questionString.replace('@FIGURE@', "" )

    # if not tableNumber == '':
    questionString = questionString.replace('@TABLE@', "" )

    # if not textNumber == '':
    questionString = questionString.replace('@TEXT@', "" )

    # @IDENTIFIER@, @TITLE@, @LABEL@, @QUESTION@
    QTIQuestionString = QTIQuestionString.replace('@IDENTIFIER@', questionCode )
    QTIQuestionString = QTIQuestionString.replace('@TITLE@', "domanda" )
    QTIQuestionString = QTIQuestionString.replace('@LABEL@', questionCode )

    QTIQuestionString = QTIQuestionString.replace('@QUESTION@', questionString )
    #print QTIQuestionString

    return QTIQuestionString





# it writes the files of the QTI questions, based on makeLatexFile
def makeQTIFiles():

    # print questionListMatrix

    questionNumberList, questionCodeList, questionTypeList, questionVersionNumberList, \
        questionFigureList, questionTableList, questionTextList = transposed(questionListMatrix)


    # # questionNumberList, questionCodeList, questionTypeList, questionVersionNumberList, \
    #     questionFigureList, questionTableList, questionTextList, \
    #     questionAnswerOrderList, questionAnswerOrderString, questionKeyList = transposedReorderedQuestionListMatrix

    # qNumber = len(questionCodeList)

    if not os.path.exists(mainpath + "/output/" + projectName + "-qti/"):
        os.makedirs(mainpath + "/output/" + projectName + "-qti/")

    resourceString = ""
    for j in range(0,questionNumber):
        # newQuestionString = makeQTIQuestion(questionCodeList[j], int(questionTypeList[j]), questionFigureList[j])
        newQuestionString = makeQTIQuestion(questionCodeList[j], int(questionTypeList[j]), "xxxxxxxxxxxx")
        QTIQuestionOutputFile = open( mainpath + "/output/" + projectName + "-qti/" + "q" + questionCodeList[j] + ".xml", 'w' )
        QTIQuestionOutputFile.write(newQuestionString)
        QTIQuestionOutputFile.close()

        resourceString = resourceString + "\t\t" + r'<resource identifier="q' + questionCodeList[j] + r'" type="imsqti_item_xmlv2p2" href="q' + \
                            questionCodeList[j] + r'.xml">'
        resourceString = resourceString + r'<file href="q' + questionCodeList[j] + r'.xml"/>' + "\n"


        # ADDING FIGURES
        # if os.path.exists( mainpath + "/input/" + questionFolderName + "/" + "q" + questionFigureList[j] + "-fig.png" ):
        #     #print j+1
        #     shutil.copyfile( mainpath + "/input/" + questionFolderName + "/" + "q" + questionFigureList[j] + "-fig.png" ,
        #                      mainpath + "/output/" + projectName + "-qti/" + "q" + questionFigureList[j] + "-fig.png")
        #     resourceString = resourceString + r'<file href="q' + questionFigureList[j] + r'-fig.png"/>' + "\n"

        resourceString = resourceString + r'</resource>' + "\n"

    # print(resourceString)

    IMSManifestModelFile = open( mainpath + "/input/" + "imsmanifest-model.xml", 'r' )
    IMSManifestString = IMSManifestModelFile.read()
    IMSManifestModelFile.close()

    IMSManifestString = IMSManifestString.replace('@MANIFEST-IDENTIFIER@', projectName )
    IMSManifestString = IMSManifestString.replace('@RESOURCES@', resourceString )
    # print(IMSManifestString)

    IMSManifestOutputFile = open( mainpath + "/output/" + projectName + "-qti/imsmanifest.xml", 'w' )
    IMSManifestOutputFile.write(IMSManifestString)
    IMSManifestOutputFile.close()

    os.chdir(mainpath + "/output")
    shutil.make_archive(projectName + "-qti", 'zip', mainpath + "/output/" + projectName + "-qti/")
    os.chdir(mainpath)

    # the folder is deleted on exiting
    shutil.rmtree(mainpath + "/output/" + projectName + "-qti/")

# <resource identifier="CP5401400020" type="imsqti_item_xmlv2p2" href="qCP5401400020.xml"><file href="qCP5401400020.xml"/></resource>
    #print figureDictionary
    #print tableDictionary






# it defines all the global variables associated to the project,
# such as projectMatrix, projectName, projectType, versionNumber, etc.
def readProject(projectFileName):

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
    #global qNumberFileName, qCodeFileName, qAnswerOrderFileName, qKeyFileName
    #qNumberFileName = projectMatrix[11][1]
    #qCodeFileName = projectMatrix[12][1]
    #qAnswerOrderFileName = projectMatrix[13][1]
    #qKeyFileName = projectMatrix[14][1]

    #OUTPUT FILE OBJECTS
    #global qNumberFile, qCodeFile, qAnswerOrderFile, qKeyFile
    #qNumberFile = open( mainpath + "/output/" + qNumberFileName, 'w' )
    #qCodeFile = open( mainpath + "/output/" + qCodeFileName, 'w' )
    #qAnswerOrderFile = open( mainpath + "/output/" + qAnswerOrderFileName, 'w' )
    #qKeyFile = open( mainpath + "/output/" + qKeyFileName, 'w' )

    # dimension of the figures inside the latex text
    #global figureDimension
    #figureDimension = projectMatrix[21][1]
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
    readProject(projectFileName)

    # creating the latex folder that will be deleted on exiting
    # makeLatexFolder()

    # global testWriter
    # testWriter = PdfWriter()

    # makeQTIQuestion("MA5301400010", 4)
    makeQTIFiles()


    # for vNumber in range(0,versionNumber+1):
    #     print "Now preparing version " + `vNumber` + " (of " + `versionNumber` + "+1)..."
    #     makeVersionFiles(vNumber)

    # print "Now binding together the .pdf files of the " + `versionNumber` + "+1 versions"

    # saving the pdf file
    # os.chdir(mainpath+"/output")
    # testWriter.write(projectName + ".pdf")
    # os.chdir(mainpath)

    # the latex directory is deleted on exiting
    # shutil.rmtree(mainpath + "/output/latex")

    # qNumberFile.close()
    # qCodeFile.close()
    # qAnswerOrderFile.close()
    # qKeyFile.close()


main()
