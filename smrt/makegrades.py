
import math

# erfinv: inverse erf function
from scipy.special import erfinv



# it converts a numeric grade into an expression, e.g. 7.25 --> 7+, 7.5 --> 7 1/2
# INCOMPLETE
def computeLetterGrade(grade):
   int_, dec_ = math.modf(grade)
   return repr(int_)



# it computes the grades, i.e. the normalized scores
# the precision index is the inverse of precision,
# i.e. if precisionIndex=10 then the precision is on the decimal position
def makeGrades(number, scores, average, standardDev, precisionIndex = 4):
   # print number

   print(scores)

   scores.sort()
   #scores.sort(reverse=True)
   #print(scores)

   positions = []
   positions = [0 for k in range(0,number)]
   for k in range(0,number):
      positions[k:k+1] = [k+1]
   print(positions)

   # list with the number of repeated scores for each score
   repetitions = []
   repetitions = [0 for k in range(0,number)]
   for k in range(0,number):
       #repetedScore = float()
       repetitions[k:k+1] = [scores.count(scores[k])]
   # print repetitions

   # difference between successive scores
   delta = []
   delta = [0.0 for k in range(0,number-1)]
   for k in range(0,number-1):
       delta[k:k+1] = [scores[k+1]-scores[k]]
   # print delta


   floatPositions = []
   floatPositions = [float(k+1) for k in range(0,number)]
   #floatPositions[0:1] = [1.0]
   #floatPositions[number-1:number] = [float(number)]
   for k in range(1,number-1):
       if repetitions[k] == 1:
           floatPositions[k:k+1] = [float(k) + 1.0 - .5*(delta[k] - delta[k-1])/(delta[k] + delta[k-1])]
       else:
           if delta[k-1] != 0.0:
              av = 0.0 #float(positions[k])/float(repetitions[k]) partial average
              #print av
              for j in range(0,repetitions[k]):
                 av = av + float(positions[k+j])/float(repetitions[k]) # average over the repeated positions
              #print av
              if k + repetitions[k] +1 > number:
                 print("over")
              if k + repetitions[k] +1 < number:
                 for j in range(0,repetitions[k]):
                    floatPositions[k+j:k+j+1] = [av - (.5*repetitions[k])*(delta[k+repetitions[k]-1] - delta[k-1])/(delta[k+repetitions[k]-1] + delta[k-1])]
                 #[av - (.5/repetitions[k])*(delta[k+repetitions[k]-1] - delta[k-1])/(delta[k+repetitions[k]-1] + delta[k-1])]
              else:
                  for j in range(0,repetitions[k]):
                    floatPositions[k+j:k+j+1] = [av]
                 #[av - (.5/repetitions[k])*(delta[k+repetitions[k]-1] - delta[k-1])/(delta[k+repetitions[k]-1] + delta[k-1])]

   # print floatPositions


   grades = []
   grades = [0.0 for k in range(0,number)]
   roundgrades = []
   roundgrades = [0.0 for k in range(0,number)]



   for k in range(0,number):
      grades[k:k+1] = [math.sqrt(2)*standardDev*erfinv((2/float(number))*(floatPositions[k]-.5)-1.0)+average]
      roundgrades[k:k+1] = [round(precisionIndex*grades[k], 0)/precisionIndex]

      # print roundgrades[k]

   print("Grades without rounding: ")
   print(grades)
   print()
   # rounded to 0 decimals (entrance test)
   # return roundgrades0

   # rounded to 2 decimals (entrance test)
   # return roundgrades2

   # rounded in .25 steps (common test)
   return roundgrades

   # Grades without rounding
   #return grades
