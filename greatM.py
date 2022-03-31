from validationsBeforeMethodSelection import *
from utilityFunctions import *
from readAndSaveTxtInformation import *
import numpy as np

"""
Function: appropriateFormGreatM
Input: -
Output: -
Description: Function that turns the appropriate form of the row (0) / objective function
"""
def appropriateFormGreatM():
    objectiveFunction = restrictionsMatrix[0]
    i = numberOfDecisionVariables[0]
    for var in slackVariables:
        i = int(var[1]) - 1
        if var[0] == 'a':
            if optimization[0] == 'max':
                objectiveFunction.insert(i, 0+1j)
            else:
                objectiveFunction.insert(i, 0-1j)
        else:
            objectiveFunction.insert(i, 0)
    restrictionsMatrix[0] = checkMinimization(objectiveFunction)

    appropriateFormOperationsGreatM()
    removeRightSideMethod()
    
"""
Function: appropriateFormOperationsGreatM
Input: -
Output: -
Description: Function that performs operations on the rows with artificial variables
"""
def appropriateFormOperationsGreatM():
    operationsMatrix = []
    positions = []

    counter = 0
    for num in restrictionsMatrix[0]:
        if num == 1j or num == -1j:
            positions.append(counter)
        counter += 1
    
    i = 1
    k = 0
    while i < len(restrictionsMatrix):
        if restrictionsMatrix[i][positions[k]] == 1 or restrictionsMatrix[i][positions[k]] == -1:
            newRow = [i * -1j for i in restrictionsMatrix[i]]
            operationsMatrix.append(newRow)
            if k+1 < len(positions):
                k += 1
        i += 1

    operationsMatrix.insert(0, restrictionsMatrix[0])   # objective function will always be in operations matrix
    result = np.sum(operationsMatrix, axis=0)
    restrictionsMatrix[0] = result.tolist()
