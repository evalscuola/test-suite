

#from config import projectName, projectType, versionNumber, \
#                    questionListFileName, latexInputFileName, questionFolderName, \
#                    qNumberFileName, qCodeFileName, qAnswerOrderFileName, qKeyFileName, \
#                    qNumberFile, qCodeFile, qAnswerOrderFile, qKeyFile, \
#                    figureDimension, \
#                    copyFolderName, \
#                    questionListMatrix, \
#                    questionNumber

# to add command line options
import argparse


from module import csvFileToMatrix


def getProjectFileName():

    #### COMMAND LINE OPTIONS ####
    parser = argparse.ArgumentParser()
    # parser.parse_args()
    parser.add_argument("project", help="the project filename")
    args = parser.parse_args()
    projectFileName = args.project
    # pprint args.project
    print("projectFileName: " + projectFileName + "\n")
    return projectFileName




class ProjectClass(): #projectreader

    def __init__(self, projectFileName, projectFilePath):

        self.matrix = csvFileToMatrix(projectFileName, projectFilePath)
        #print("projectMatrix: \n" + repr(projectMatrix) + "\n\n")

        self.dictionary = createProjectDictionary(self.matrix)

        projectMatrix = self.matrix

        # PROJECT NAME, TYPE AND TOTAL NUMBER OF VERSIONS
        # TO DO: (da separare e verificare anche questionNumber, confrontando con il numero di domande in questionListMatrix )
        self.name = projectMatrix[0][1]
        self.type = projectMatrix[1][1]
        self.versionNumber = int(projectMatrix[2][1])

        # INPUT FILE NAMES
        self.questionListFileName = projectMatrix[5][1]
        self.latexInputFileName = projectMatrix[6][1]
        self.questionFolderName = projectMatrix[7][1]

        #OUTPUT FILE NAMES
        self.qNumberFileName = projectMatrix[11][1]
        self.qCodeFileName = projectMatrix[12][1]
        self.qAnswerOrderFileName = projectMatrix[13][1]
        self.qKeyFileName = projectMatrix[14][1]

        #OUTPUT FILE OBJECTS
        self.qNumberFile = open( projectFilePath + "/output/" + self.qNumberFileName, 'w' )
        self.qCodeFile = open( projectFilePath + "/output/" + self.qCodeFileName, 'w' )
        self.qAnswerOrderFile = open( projectFilePath + "/output/" + self.qAnswerOrderFileName, 'w' )
        self.qKeyFile = open( projectFilePath + "/output/" + self.qKeyFileName, 'w' )

        # dimension of the figures inside the latex text
        self.figureDimension = projectMatrix[21][1]

        # the full content of the folder copyFolderName will be copied to the latex folder
        self.copyFolderName = projectMatrix[23][1]

        # using csvFileToMatrix(csvFileName, csvFilePath) to read the list of the questions from file and make a matrix
        self.questionListMatrix = csvFileToMatrix(self.questionListFileName, projectFilePath + "/input" )

        # NUMBER OF QUESTIONS
        self.questionNumber = len(self.questionListMatrix)

        #### END LIST OF CONSTANTS ####





def createProjectDictionary(projectMatrix):

    projectDictionary = {}

    for line in projectMatrix:
        if len(line) > 1:
            projectDictionary[line[0]] = line[1]

    # print(projectDictionary)
