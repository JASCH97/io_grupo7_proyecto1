from validationsBeforeMethodSelection import *
from utilityFunctions import *
from readAndSaveTxtInformation import *
import numpy as np

# Global variables
phaseTwoRow = []
phaseTwoRowBackUp = []
"""
Function: appropriateFormTwoPhases
Input: -
Output: -
Description: Function that turns the appropriate form of the row (0) / objective function
"""
def appropriateFormTwoPhases():
    global phaseTwoRow
    
    i = numberOfDecisionVariables[0]
    phaseOneRow = [0]*i
    phaseTwoRow = restrictionsMatrix[0]
    for var in slackVariables:
        i = int(var[1]) - 1
        if var[0] == 'a':
            phaseOneRow.insert(i, 1)
        else:
            phaseOneRow.insert(i, 0)
            phaseTwoRow.insert(i, 0)
    
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

#This function create a backUp of the objective function
def saveFirstObjectiveFunction():
    global phaseTwoRowBackUp

    for number in restrictionsMatrix[0]:
        phaseTwoRowBackUp.append(number)

# This function eliminate the artificial columns and insert the main objective function
def adaptationForTheFinalPhase():
    global rightSide
    global nBV
    artificialColumns = []
    newObjectiveFunction = []
    strArtificials = []
    
    for variable in nBV:
        if variable[0] == "a":
            artificialColumns.append(int(variable[1]) - 1)
            strArtificials.append(variable)

  
    k = 0
    while strArtificials != []:

        for variable in nBV:
            if variable == strArtificials[0]:
                nBV.remove(variable)

            for strVariable in strTotalVariables:
                if strVariable == strArtificials[0]:
                    strTotalVariables.remove(strVariable)

        strArtificials.pop(0)

    
    j = 0

    while j <= len(artificialColumns) - 1:
        intTotalVariables.pop(len(intTotalVariables) - 1)

        j += 1

    for variable in phaseTwoRowBackUp:
        newObjectiveFunction.append(variable * -1)

    print(artificialColumns)
    for variable in bV:
        newObjectiveFunction[int(variable[1]) - 1] = newObjectiveFunction[int(variable[1]) - 1]

    
    artificialColumns.sort(reverse=True)                        # The list is sorted from largest to smallest to avoid problems
    for restriction in restrictionsMatrix:

        for column in artificialColumns:

            restriction.pop(column)

    restrictionsMatrix.pop(0)
    newObjectiveFunction.pop(len(newObjectiveFunction) - 1)      
    restrictionsMatrix.insert(0, newObjectiveFunction)
    
    newNumbersToOperateOn = []
    for variable in bV:
        newNumbersToOperateOn.append(restrictionsMatrix[0][int(variable[1]) - 1])
    

    newRowsToOperateOn = restrictionsMatrix[1:]
    rightSideValues = rightSide[1:]

    for restriction in newRowsToOperateOn:

        k = 0

        while k <= len(restrictionsMatrix[0]) - 1:

            restrictionsMatrix[0][k] = round(restrictionsMatrix[0][k] + (newNumbersToOperateOn[0] * -1) * restriction[k] , 4)

            k += 1

        rightSide[0] = round(rightSide[0] + (newNumbersToOperateOn[0] * -1) * rightSideValues[0] , 4)
        newNumbersToOperateOn.pop(0)  
        rightSideValues.pop(0)







