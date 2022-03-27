from validationsBeforeMethodSelection import *
from utilityFunctions import *
from readAndSaveTxtInformation import *

"""
Function: appropriateForm
Input: -
Output: -
Description: Function that turns the appropriate form of the row (0) / objective function
"""
def appropriateForm():
    objectiveFunction = restrictionsMatrix[0]
    artCounter = 0
    i = numberOfDecisionVariables[0]
    for var in strTotalVariables:
        if artificialVariables[artCounter][1] == var[1]:
            if optimization[0] == 'max':
                objectiveFunction.insert(i, 0+1j)
            else:
                objectiveFunction.insert(i, 0-1j)
            artCounter += 1
            i += 1
        elif int(var[1]) > i:
            objectiveFunction.insert(i, 0.0)
            i += 1
    restrictionsMatrix[0] = checkMinimization(objectiveFunction)
    print(restrictionsMatrix)


"""
Function: checkMinimization
Input: objective function
Output: transformed objective function
Description: Function that checks if the problem has to be multiplied by -1
"""
def checkMinimization(objectiveFunction):
    if optimization[0] == 'min':
        return [i * -1 for i in objectiveFunction]
    else:
        return objectiveFunction


"""
Function: createGreatMTabularForm
Input: -
Output: -
Description: Function that takes the restrictions and adds 0s and 1s based on the slack variables
"""
def createGreatMTabularForm():
    i = 1
    nextOnePosition = len(restrictionsMatrix[1]) - 1
    while i <= len(restrictionsMatrix) - 1:
        contVariablesLeft = contVariables[0] - len(restrictionsMatrix[i]) + 1
        
        while contVariablesLeft != 0:
            restrictionsMatrix[i].insert(nextOnePosition,0)
            contVariablesLeft -= 1
        i += 1

    i = 1
    j = 0
    while i <= len(restrictionsMatrix) - 1:
        if slackVariables[j][0] == 's':                                     # revisa si es variable de exceso
            restrictionsMatrix[i][int(slackVariables[j][1]) - 1] = -1
            j += 1
        if slackVariables[j][0] == 'a':                                     # revisa si es variable artificial
            restrictionsMatrix[i][int(slackVariables[j][1]) - 1] = 1
            j += 1
        i += 1
    
    appropriateForm()