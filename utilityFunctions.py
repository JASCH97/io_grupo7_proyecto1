import numpy as np
from readAndSaveTxtInformation import *
from validationsBeforeMethodSelection import *


rightSide = []
rowsToOperateOn = []
numbersToOperateOn = []

"""
Function: validateSpecialCases
Input: request, dividing numbers
Output: boolean or position of row
Description: Function that validates special cases
"""
def validateSpecialCases(request,dividingNumbers):
    totalDivisionResults = []
    numbersToDivide = rightSide[1:]
    numbersDivisionResults = []

    i = 0
    j = 0
    while i <= len(dividingNumbers) - 1:

        if dividingNumbers[i] < 0 or dividingNumbers[i] == 0:
            totalDivisionResults.append("invalidNumber")    # if dividing number is negative, it becomes "invalid"
            i += 1
        
        else:
            if numbersToDivide[i] < 0:                      # if dividing number is negative, it becomes "invalid"
                totalDivisionResults.append("invalidNumber")                                  
                i += 1
            else:           
                totalDivisionResults.append(round((numbersToDivide[i] / dividingNumbers[i]), 5))
                numbersDivisionResults.append(round((numbersToDivide[i] / dividingNumbers[i]) , 5))
                i += 1


    if request == "is non bounded?":
        if numbersDivisionResults == []:
            return True
        else:
            return False
    
    elif request == "is degenerate?": 
        minorNumber = totalDivisionResults[np.argmin(totalDivisionResults)]             
        
        if(totalDivisionResults.count(minorNumber)) > 1:          # validates if minimum number from results of division appears more than once
            return True
        else:
            return False
            
    else:  
        maxValue = max(numbersDivisionResults)
        k = 0
        while k <= len(totalDivisionResults) - 1:
            if type(totalDivisionResults[k]) == str:
                totalDivisionResults[k] = maxValue
                k += 1
            k += 1

        pivotRowPosition = np.argmin(totalDivisionResults) + 1

        return pivotRowPosition

     
"""
Function: getColumnDividingNumbers
Input: minimum position of number
Output: list of numbers that divide the right side
Description: Function that returns the column of numbers to divide by
"""
def getColumnDividingNumbers(minNumberPosition):
    dividingNumbers = []

    i = 1
    while i <= len(restrictionsMatrix) - 1:
        dividingNumbers.append(restrictionsMatrix[i][minNumberPosition])

        i += 1

    return dividingNumbers


"""
Function: isOptimal
Input: -
Output: boolean value
Description: Function that returns if the current answer is optimal
"""
def isOptimal():
    if selectedMethod[0] == 0:
        firstRestriction = restrictionsMatrix[0]
        minPosNumber = np.argmin(firstRestriction)
        
        minNumber = restrictionsMatrix[0][minPosNumber]
    else:
        firstRestriction = np.array(restrictionsMatrix[0])
        minPosNumber = np.argmin(firstRestriction.imag)
        minNumber = firstRestriction.imag[minPosNumber]

    if minNumber > 0 or minNumber == 0:
        return True
    
    else:
        return False

"""
Function: transposeMatrix
Input: some matrix
Output: matrix transposed
Description: Function that returns a matrix in its transposed form
"""
def transposeMatrix(matrix):
    transposedMatrix = []

    numberOfRows = len(matrix)
    numberOfCols = len(matrix[0])

    for j in range(numberOfCols):

        transposedMatrix.append([])

        for i in range(numberOfRows):
            transposedMatrix[j].append(matrix[i][j])

    return transposedMatrix

"""
Function: divideRestrictionNumbers
Input: position and pivot number
Output: -
Description: Function that divides the numbers in the restriction matrix by the pivot number
"""
def divideRestrictionNumbers(position,pivotNumber):

    i = 0

    while i <= len(restrictionsMatrix[position]) - 1:
        restrictionsMatrix[position][i] = round(restrictionsMatrix[position][i] / pivotNumber , 5)

        i += 1
    
    rightSide[position] = rightSide[position] / pivotNumber     # the number on right side is divided too

"""
Function: checkZerosInPivotColumn
Input: matrix, row and column
Output: -
Description: Function that fills pivot column with zeros and 1 in the position of pivot number
"""
def checkZerosInPivotColumn(matrix, row, column):
    global rowsToOperateOn
    global numbersToOperateOn

    i = 0

    while i <= len(matrix) - 1:                                   # pivot column is filled with zeros

        if matrix[i][column] != 0:
            if i != row:                                          # save restrictions' indexes where row operations need to be done
                rowsToOperateOn.append(i)                         # we also save the values in the indexes before changing so we can calculate later
                numbersToOperateOn.append(matrix[i][column])

            matrix[i][column] = 0
        i += 1

    matrix[row][column] = 1                                       # pivot number turns to 1
    
"""
Function: resetOperableList
Input: -
Output: -
Description: Function that resets lists for each iteration
"""
def resetOperableList():
    global rowsToOperateOn
    global numbersToOperateOn

    rowsToOperateOn = []
    numbersToOperateOn = []

"""
Function: rowOperations
Input: matrix, restriction, column and row of pivor number
Output: -
Description: Function that performs operations on all rows
"""
def rowOperations(matrix,restriction,mainColumn,mainRow):

    i = 0
    if selectedMethod[0] == 0:
        rightSide[mainRow] = round(rightSide[mainRow], 5)
        while i <= len(rowsToOperateOn) - 1:
            newRow = []
            j = 0
            while j <= len(matrix[0]) - 1:

                if j == mainColumn:
                    newRow.append(round((matrix[rowsToOperateOn[i]][j]) , 5))
                    j += 1

                else:
                    newRow.append(round((matrix[rowsToOperateOn[i]][j] + (numbersToOperateOn[i] * -1) * restriction[j]) , 5)) 
                    j += 1

            rightSide[rowsToOperateOn[i]] = round((rightSide[rowsToOperateOn[i]] + (numbersToOperateOn[i] * -1) * rightSide[mainRow]) , 5)
            matrix[rowsToOperateOn[i]] = newRow
            i += 1
    
    elif selectedMethod[0] == 1:
        if type(rightSide[mainRow]) == complex:
            rightSide[mainRow] = roundComplex(rightSide[mainRow])
        else:
            rightSide[mainRow] = round(rightSide[mainRow], 5)
        while i <= len(rowsToOperateOn) - 1:
            newRow = []
            j = 0
            while j <= len(matrix[0]) - 1:

                if j == mainColumn:
                    if type(matrix[rowsToOperateOn[i]][j]) == complex:
                        newRow.append(roundComplex(matrix[rowsToOperateOn[i]][j]))
                    else:
                        newRow.append(round((matrix[rowsToOperateOn[i]][j]) , 5))
                    j += 1

                else:
                    if type(numbersToOperateOn[i]) == complex:
                        newRow.append(roundComplex(matrix[rowsToOperateOn[i]][j] + (numbersToOperateOn[i] * -1) * restriction[j]))
                    else:
                        newRow.append(round((matrix[rowsToOperateOn[i]][j] + (numbersToOperateOn[i] * -1) * restriction[j]) , 5)) 
                    j += 1

            if type(numbersToOperateOn[i]) == complex:
                rightSide[rowsToOperateOn[i]] = roundComplex(rightSide[rowsToOperateOn[i]] + (numbersToOperateOn[i] * -1) * rightSide[mainRow])
            else:
                
                rightSide[rowsToOperateOn[i]] = round((rightSide[rowsToOperateOn[i]] + (numbersToOperateOn[i] * -1) * rightSide[mainRow]), 5)
            matrix[rowsToOperateOn[i]] = newRow
            i += 1

"""
Function: roundComplex
Input: complex number
Output: rounded complex number
Description: Function that rounds a given complex number
"""
def roundComplex(number):
    return round(number.real, 4) + round(number.imag, 4) * 1j

"""
Function: uptadeNonBasicVariables
Input: non basic variables
Output: -
Description: Function that updates the nBV
"""
def uptadeNonBasicVariables(nBV):
    
    difVariables = []

    for variable in strTotalVariables:
        if variable not in bV:
            difVariables.append(variable)
    
    while nBV != []:
        nBV.pop(0)
    
    for variable in difVariables:
        nBV.append(variable)
    
"""
Function: printFinalSolution
Input: augmented solution and if its optimal
Output: -
Description: Function that prints the final solution
"""
def printFinalSolution(augmentedSolution, optimal):
    print("Final Augmented Solution -> "+ str(augmentedSolution))
    
    if optimal == True:
        print("Optimal Solution ->  U = " + str(rightSide[0]) + "\n")
    
    else:
        print("Not Optimal Solution ->  U = " + str(rightSide[0]) + "\n")

"""
Function: checkZerosInNonBasicVariables
Input: augmented solution and if its optimal
Output: -
Description: Function that checks if a nBV has ceros and gets its position to use as pivot
"""
def checkZerosInNonBasicVariables(request,nBV):
    newPivotColum = -1

    for variable in nBV:
        if restrictionsMatrix[0][int(variable[1]) - 1] == 0:
            newPivotColum = int(variable[1]) - 1
    
    if request == "new pivot column?":
        return newPivotColum
    
    else:
        if newPivotColum != -1:
            return True                     # si hay 0's en alguna de las variables no basicas
        
        else:                               # no hay 0's en las variables no basicas
            return False