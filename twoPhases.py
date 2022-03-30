from validationsBeforeMethodSelection import *
from utilityFunctions import *
from readAndSaveTxtInformation import *
import numpy as np

phaseTwoRow = []

"""
Function: appropriateFormTwoPhases
Input: -
Output: -
Description: Function that turns the appropriate form of the row (0) / objective function
"""
def appropriateFormTwoPhases():
    global phaseTwoRow
    
    phaseOneRow = []
    phaseTwoRow = restrictionsMatrix[0]
    artCounter = 0
    i = numberOfDecisionVariables[0]
    for var in strTotalVariables:
        if int(var[1]) > i :
            phaseTwoRow.insert(i, 0)
            i += 1
        if artificialVariables[artCounter][1] == var[1]:
            phaseOneRow.insert(i, 1)
            artCounter += 1
            i += 1
        else:
            phaseOneRow.insert(i, 0)
    
    # deletes the artifical variables from phase two
    for art in artificialVariables:
        phaseTwoRow.pop()

    # append the right side
    phaseTwoRow.append(0)
    phaseOneRow.append(0)

    phaseTwoRow = checkMinimization(objectiveFunction)

    restrictionsMatrix.pop(0)
    restrictionsMatrix.insert(0, phaseOneRow)
    
    appropriateFormOperationsTwoPhases()
    removeRightSideMethod()

"""
Function: appropriateFormOperationsTwoPhases
Input: -
Output: -
Description: Function that performs operations on the rows with artificial variables
"""
def appropriateFormOperationsTwoPhases():
    operationsMatrix = []
    positions = []

    counter = 0
    for num in restrictionsMatrix[0]:
        if num == 1:
            positions.append(counter)
        counter += 1

    i = 1
    k = 0
    while i <= len(restrictionsMatrix) - 1:
        if restrictionsMatrix[i][positions[k]] == 1:
            newRow = [i * -1 for i in restrictionsMatrix[i]]
            operationsMatrix.append(newRow)
            k += 1
        i += 1
    
    operationsMatrix.insert(0, restrictionsMatrix[0])   # artificial row will always be in operations matrix
    result = np.sum(operationsMatrix, axis=0)
    restrictionsMatrix[0] = result.tolist()
