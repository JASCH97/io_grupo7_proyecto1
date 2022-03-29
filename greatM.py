from validationsBeforeMethodSelection import *
from utilityFunctions import *
from readAndSaveTxtInformation import *
import numpy as np

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

    appropriateFormOperations()
    removeRightSide()

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
Function: appropriateFormOperations
Input: -
Output: -
Description: Function that performs operations on the rows with artificial variables
"""
def appropriateFormOperations():
    operationsMatrix = []
    positions = []

    counter = 0
    for num in restrictionsMatrix[0]:
        if num == 1j or num == -1j:
            positions.append(counter)
        counter += 1
    
    i = 1
    k = 0
    while i <= len(restrictionsMatrix) - 1:
        if restrictionsMatrix[i][positions[k]] == 1 or restrictionsMatrix[i][positions[k]] == -1:
            newRow = [i * -1j for i in restrictionsMatrix[i]]
            operationsMatrix.append(newRow)
            k += 1
        i += 1
    
    operationsMatrix.insert(0, restrictionsMatrix[0]) #siempre va a estar la función objetivo
    result = np.sum(operationsMatrix, axis=0)
    restrictionsMatrix[0] = result.tolist()

"""
Function: removeRightSide
Input: -
Output: -
Description: Function that takes the restrictions and separates the right side from the slack variables
"""
def removeRightSide():
    global rightSide
    global restrictionsMatrix

    #Quita de las restricciones el numero que va en el lado derecho
    for restriction in restrictionsMatrix:
        rightSide.append(restriction[len(restriction) - 1])
        restriction.remove(restriction[len(restriction) - 1])

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
        if slackVariables[j][0] == 'x':                                     # revisa si es variable normal
            restrictionsMatrix[i][int(slackVariables[j][1]) - 1] = 1
            j += 1
            i += 1
        if slackVariables[j][0] == 's':                                     # revisa si es variable de exceso
            restrictionsMatrix[i][int(slackVariables[j][1]) - 1] = -1
            j += 1
        if slackVariables[j][0] == 'a':                                     # revisa si es variable artificial
            restrictionsMatrix[i][int(slackVariables[j][1]) - 1] = 1
            j += 1
        i += 1
    
    appropriateForm()