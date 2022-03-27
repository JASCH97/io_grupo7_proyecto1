import numpy as np
from readAndSaveTxtInformation import *
from validationsBeforeMethodSelection import *


rightSide = []
rowsToOperateOn = []
numbersToOperateOn = []

def validateSpecialCases(request,dividingNumbers):
    totalDivisionResults = []
    numbersToDivide = rightSide[1:]
    numbersDivisionResults = []

    i = 0
    j = 0
    while i <= len(dividingNumbers) - 1:

        if dividingNumbers[i] < 0 or dividingNumbers[i] == 0:
            totalDivisionResults.append("invalidNumber")                                   # si el numero que se divide es negativo se agrega en esa posicion un "invalid"
            i += 1
        
        else:
            if numbersToDivide[i] < 0:                                                  #si el numero que se divide es negativo se agrega en esa posicion un "invalid"
                totalDivisionResults.append("invalidNumber")                                  
                i += 1
            else:           
                totalDivisionResults.append(numbersToDivide[i] / dividingNumbers[i])
                numbersDivisionResults.append(numbersToDivide[i] / dividingNumbers[i])
                i += 1


    if request == "is non bounded?":
        if numbersDivisionResults == []:
            return True
        else:
            return False
    
    elif request == "is degenerate?": 
        minorNumber = totalDivisionResults[np.argmin(totalDivisionResults)]             
        
        if(totalDivisionResults.count(minorNumber)) > 1:                 # si el menor numero de los resultados al dividir se encuentra mas de 1 vez
            return True
        
        else:
            return False
            

            
    
    else:                                                                   #Se solicita la fila donde esta el numero pivot
        pivotRowPosition = np.argmin(totalDivisionResults) + 1                       #obtiene el índice del minimo valor. Se le suma 1 ya que se ignora la restriccion en la pos 0
        return pivotRowPosition

def getColumnDividingNumbers(minNumberPosition):
    dividingNumbers = []

    i = 1
    while i <= len(restrictionsMatrix) - 1:
        dividingNumbers.append(restrictionsMatrix[i][minNumberPosition])

        i += 1

    return dividingNumbers



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


def transposeMatrix(matrix):
    transposedMatrix = []

    numberOfRows = len(matrix)
    numberOfCols = len(matrix[0])

    for j in range(numberOfCols):

        transposedMatrix.append([])

        for i in range(numberOfRows):
            transposedMatrix[j].append(matrix[i][j])

    return transposedMatrix


def divideRestrictionNumbers(position,pivotNumber):

    i = 0

    while i <= len(restrictionsMatrix[position]) - 1:
        restrictionsMatrix[position][i] = restrictionsMatrix[position][i] / pivotNumber

        i += 1
    
    rightSide[position] = rightSide[position] / pivotNumber                         #Se divide tambien el numero del lado derecho

def checkZerosInPivotColumn(matrix, row, column):
    global rowsToOperateOn
    global numbersToOperateOn

    i = 0

    while i <= len(matrix) - 1:                                         # se colocan 0's en toda la coluna pivot

        if matrix[i][column] != 0:
            if i != row:                                                # se guardan los indices de las restricciones a las que hay que aplicarles operaciones de renglon
                rowsToOperateOn.append(i)                               # tambien se guardan los valores que estaban en esos indices antes del cambio para poder operar luego
                numbersToOperateOn.append(matrix[i][column])

            matrix[i][column] = 0
        i += 1

    matrix[row][column] = 1                                             # se agrega un 1 en el lugar del numero pivot
    

def resetOperableList():
    global rowsToOperateOn
    global numbersToOperateOn

    rowsToOperateOn = []
    numbersToOperateOn = []


def rowOperations(matrix,restriction,mainColumn,mainRow):

    i = 0

    while i <= len(rowsToOperateOn) - 1:
        newRow = []
        j = 0
        while j <= len(matrix[0]) - 1:

            if j == mainColumn:
                newRow.append(matrix[rowsToOperateOn[i]][j])
                j += 1

            else:
                newRow.append(matrix[rowsToOperateOn[i]][j] + (numbersToOperateOn[i] * -1) * restriction[j]) 
                j += 1

        rightSide[rowsToOperateOn[i]] = rightSide[rowsToOperateOn[i]] + (numbersToOperateOn[i] * -1) * rightSide[mainRow]
        matrix[rowsToOperateOn[i]] = newRow
        i += 1
    

def improveNumbersPresentation(matrix,list):

    i = 0

    while i <= len(matrix) - 1:

        j = 0

        while j <= len(matrix[i]) - 1:

            strNumber = str(matrix[i][j])
            strNumber = strNumber.split(".")

            if len(strNumber) > 1:

                if(int(strNumber[1])) == 0:
                    matrix[i][j] = int(matrix[i][j])
                    j += 1
                
                else:
                    matrix[i][j] = float(round(matrix[i][j],5))
                    j += 1
            
            else:
                matrix[i][j] = int(matrix[i][j])

                j += 1

        i += 1
    

    k = 0

    while k <= len(list) - 1:

        strNumber = str(list[k])
        strNumber = strNumber.split(".")

        if len(strNumber) > 1:

            if (int(strNumber[1])) == 0:
                list[k] = int(list[k])
                k += 1
                
            else:
                list[k] = float(round(list[k],5))
                k += 1
            
        else:
            list[k] = int(list[k])
            k += 1


def uptadeNonBasicVariables(nBV):
    
    difVariables = []

    for variable in strTotalVariables:
        if variable not in bV:
            difVariables.append(variable)
    
    while nBV != []:
        nBV.pop(0)
    
    for variable in difVariables:
        nBV.append(variable)
    

def printFinalSolution(augmentedSolution, optimal):
    print("Final Augmented Solution -> "+ str(augmentedSolution))
    
    if optimal == True:
        print("Optimal Solution ->  U = " + str(rightSide[0]) + "\n")
    
    else:
        print("Not Optimal Solution ->  U = " + str(rightSide[0]) + "\n")

#se revisa si hay ceros en alguna variable no basica y se obtiene la posicion de una de ellas para usar oco pivot
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