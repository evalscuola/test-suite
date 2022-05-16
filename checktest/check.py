import os
import sys



import csv

# using transpose
import numpy as np



# https://csatlas.com/python-import-file-module/
# how to import module from a different directory
script_dir = os.path.dirname( __file__ )
# script_dir = os.path.dirname(os.path.abspath(__file__))
# print(script_dir)
modules_dir = os.path.join( script_dir, '..', 'modules' )
sys.path.append( modules_dir )
# print(modules_dir)


from module import transposed, createList




keyFileName = 'keyfile.csv'
responsesFileName = 'responses.csv'
pointsFileName = 'points.csv'
analysisFileName = 'analysis.csv'

CSVDelimiter = '\t'

percentageForDiscrimination = 27





# It creates a matrix containing the scores for each version and each question
# Simplified from evaluatest
def makePointsMatrix(responsesMatrix, keyList):

    pointsMatrix = []

    # print AnswersMatrix
    for j in range(0,len(responsesMatrix)):
        pointsLine = [1 for x in range(0,len(keyList))]
        for k in range(0,len(keyList)):
            if responsesMatrix[j][k] == keyList[k]:
                pointsLine[k:k+1] = [1] #
            else:
                pointsLine[k:k+1] = [0]

        pointsMatrix.append(pointsLine)
    # print(pointsMatrix)
    return pointsMatrix


def makePointsList(pointsMatrix):
    pointsList = []
    for i in range(len(pointsMatrix)):
        points = 0
        for j in range(len(pointsMatrix[i])):
            points = points + pointsMatrix[i][j]
        pointsList.append(points)
    # print(pointsList)
    return pointsList

# For each item is the average score
# eventually it should be divided by the score of the item
def makeDifficultyList(pointsMatrix):
    transposedPointsMatrix = transposed(pointsMatrix)
    difficultyList = []
    #print(transposedPointsMatrix)
    for i in range(len(transposedPointsMatrix)):
        questionSums = 0

        for j in range(len(transposedPointsMatrix[i])):
            questionSums = questionSums + transposedPointsMatrix[i][j]
            # print()
            # print(pointsMatrix[i][j])
        questionDifficulty = int(round(100*questionSums/(len(transposedPointsMatrix[i])), 0))

        difficultyList.append(questionDifficulty)

    # print(difficultyList)
    return difficultyList



def makeDiscriminationList(pointsMatrix, pointsList):

        # Numeber of top and bottom students to define discrimination index
        numberStudentsForDiscrimination = \
            int(round(numberStudents * percentageForDiscrimination/100,0))
        #print(numberStudentsForDiscrimination)

        index = np.argsort(pointsList)
        # print(index)

        #print(pointsMatrix)
        #for i in range(len(pointsMatrix)):
        #    print(pointsMatrix[index[i]])

        discriminationList = []
        transposedPointsMatrix = transposed(pointsMatrix)
        #print(transposedPointsMatrix)
        for i in range(len(transposedPointsMatrix)):
            questionDownSums = 0
            questionUpSums = 0

            for j in range(0, numberStudentsForDiscrimination):
                questionDownSums = questionDownSums + transposedPointsMatrix[i][index[j]]
                #print(questionDownSums)
                # if (i==6): print(questionDownSums)

            for j in range(0, numberStudentsForDiscrimination):
                questionUpSums = \
                    questionUpSums + \
                    transposedPointsMatrix[i][index[numberStudents-j-1]]
                # if (i==6): print(questionUpSums)
                # print()
                # print(pointsMatrix[i][j])
            #print(i+1)
            #print(questionDownSums)
            #print(questionUpSums)
            #print("\n")


            questionDiscrimination = \
                int(round(100*(questionUpSums-questionDownSums)/numberStudentsForDiscrimination, 0))

            discriminationList.append(questionDiscrimination)

        # print(discriminationList)
        return discriminationList



def makeCorrDiscriminationList(pointsMatrix, pointsList):
    corrDiscriminationList = []
    transposedPointsMatrix = transposed(pointsMatrix)
    #print(transposedPointsMatrix)
    np.seterr(divide='ignore', invalid='ignore')
    for i in range(len(transposedPointsMatrix)):
        corr=round(100*np.corrcoef(transposedPointsMatrix[i], pointsList)[0][1],0)
        #print(corr)
        if (np.isnan(corr)):
            questionCorrDiscrimination = 0
        else:
            questionCorrDiscrimination = int(corr)
        corrDiscriminationList.append(questionCorrDiscrimination)
    np.seterr(divide='warn', invalid='warn')

    return corrDiscriminationList
    # print(corrDiscriminationList)


def makePercentageAnswerList(responsesMatrix, answer):
    percentageAnswerList = []

    transposedResponsesMatrix = transposed(responsesMatrix)
    #print(transposedResponsesMatrix)

    for i in range(len(transposedResponsesMatrix)):
        numberAnswer = 0
        for j in range(len(transposedResponsesMatrix[i])):
            if (transposedResponsesMatrix[i][j] == answer):
                numberAnswer = numberAnswer + 1
        percentageAnswer = int(round(numberAnswer/numberStudents*100,0))
        percentageAnswerList.append(percentageAnswer)

    # print(percentageAnswerList)


    return percentageAnswerList


def createAnalysisMatrix(difficultyList, corrDiscriminationList, keyList, \
                percentageAnswerListA, percentageAnswerListB, \
                percentageAnswerListC, percentageAnswerListD, \
                percentageAnswerListEmpty):

    analysisMatrix = []
    # For each item it appends to analysisMatrix all the relevant quantities
    #
    for i in range(numberItems):
        analysisItem = []
        analysisItem = analysisItem + [ i+1, #\
            difficultyList[i], corrDiscriminationList[i], keyList[i], \
            percentageAnswerListA[i], percentageAnswerListB[i], \
            percentageAnswerListC[i], percentageAnswerListD[i], \
            percentageAnswerListEmpty[i] ]
            # difficultySum

        analysisMatrix.append(analysisItem)

    averageDifficulty = int(round(np.mean(difficultyList),0))
    averageDiscrimination = int(round(np.mean(corrDiscriminationList),0))
    averageAnswerA = int(round(np.mean(percentageAnswerListA),0))
    averageAnswerB = int(round(np.mean(percentageAnswerListB),0))
    averageAnswerC = int(round(np.mean(percentageAnswerListC),0))
    averageAnswerD = int(round(np.mean(percentageAnswerListD),0))
    averageAnswerEmpty = int(round(np.mean(percentageAnswerListEmpty),0))



    analysisMatrix.append(["Av.", averageDifficulty, \
        averageDiscrimination, "-", averageAnswerA, averageAnswerB,\
        averageAnswerC, averageAnswerD, averageAnswerEmpty])

    #print(analysisMatrix)
    return analysisMatrix




def main():

    # responsesMatrix = createList(responsesFileName, CSVDelimiter)

    #numberStudents = len(responsesMatrix)
    #print(numberStudents)


    keyMatrix = createList(keyFileName, CSVDelimiter)
    #print(keyMatrix)
    keyList = []
    for i in range(len(keyMatrix)):
        keyList[i:i+1] = keyMatrix[i][0]
    #print(keyList)

    pointsMatrix = makePointsMatrix(responsesMatrix, keyList)
    #print(pointsMatrix)

    # Creates a file with pointsMatrix
    # with open(pointsFileName, 'w', newline='') as f:
    #     writer = csv.writer(f, delimiter=CSVDelimiter)
    #     writer.writerows(iter(pointsMatrix))

    pointsList = makePointsList(pointsMatrix)

    difficultyList = makeDifficultyList(pointsMatrix)

    #print(np.transpose(keyList)[1])
    #print(np.transpose(responsesList)[0][0])

    discriminationList = makeDiscriminationList(pointsMatrix, pointsList)

    corrDiscriminationList = makeCorrDiscriminationList(pointsMatrix, pointsList)

    percentageAnswerListA = makePercentageAnswerList(responsesMatrix, "A")
    percentageAnswerListB = makePercentageAnswerList(responsesMatrix, "B")
    percentageAnswerListC = makePercentageAnswerList(responsesMatrix, "C")
    percentageAnswerListD = makePercentageAnswerList(responsesMatrix, "D")
    percentageAnswerListEmpty = makePercentageAnswerList(responsesMatrix, "-")

    analysisMatrix = createAnalysisMatrix(difficultyList, \
        corrDiscriminationList, keyList, \
        percentageAnswerListA, percentageAnswerListB, \
        percentageAnswerListC, percentageAnswerListD, \
        percentageAnswerListEmpty)
    print(analysisMatrix)

    # Creates a file with analysisMatrix
    with open(analysisFileName, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=CSVDelimiter)
        writer.writerows(iter(analysisMatrix))




responsesMatrix = createList(responsesFileName, CSVDelimiter)

numberStudents = len(responsesMatrix)
#print(numberStudents)
numberItems = len(transposed(responsesMatrix))


main()
