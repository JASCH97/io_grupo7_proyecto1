import numpy as np
from readAndSaveTxtInformation import *
from validationsBeforeMethodSelection import *


rightSide = []
rowsToOperateOn = []
numbersToOperateOn = []

#Cambiar nombre de funcion
def validateSpecialCases(request,dividingNumbers):
    divisionResults = []
    numbersToDivide = rightSide[1:]
   
    i = 0
    j = 0
    while i <= len(dividingNumbers) - 1:

        if dividingNumbers[i] < 0 or dividingNumbers[i] == 0:
            divisionResults.append("invalidNumber")                                   # si el numero que se divide es negativo se agrega en esa posicion un "invalid"
            i += 1
        
        else:
            if numbersToDivide[i] < 0:                                                  #si el numero que se divide es negativo se agrega en esa posicion un "invalid"
                divisionResults.append("invalidNumber")                                  
                i += 1
            else:           
                divisionResults.append(numbersToDivide[i] / dividingNumbers[i])
                i += 1

    pivot = rightSide[np.argmin(divisionResults)]

    if request == "is bounded?":
        if divisionResults == []:
            return True
        else:
            return False
    
    #elif request == "is degenerate?":              #falta implementar
            #Abajo hay una funcion que verifica si es degenerada, REVISAR
            
    
    else:                                                                   #Se solicita la fila donde esta el numero pivot
        pivotRowPosition = np.argmin(divisionResults) + 1                       #obtiene el índice del minimo valor. Se le suma 1 ya que se ignora la restriccion en la pos 0
        return pivotRowPosition

def getColumnDividingNumbers(minNumberPosition):
    dividingNumbers = []

    i = 1
    while i <= len(restrictionsMatrix) - 1:
        dividingNumbers.append(restrictionsMatrix[i][minNumberPosition])

        i += 1

    return dividingNumbers

"""def getMinNumberPosition():                                             #funciona como columna del pivot
    objectiveFunction = restrictionsMatrix[0]
    i = 0

    while i <= len(objectiveFunction) - 1:
        if objectiveFunction[i] < 0:
            firstNumberFound = objectiveFunction[i]
            i = len(objectiveFunction)
        
        i += 1
    
    minorNumberFound = firstNumberFound
    minNumberPosition = 0
    j = 0
    while j <= len(objectiveFunction) - 1:
        if objectiveFunction[j] < minorNumberFound:
            minorNumberFound = objectiveFunction[j]
            minNumberPosition = j
            j += 1
        
        j += 1

    print(minorNumberFound, minNumberPosition)
    return minNumberPosition    """                                          #se devuelve la posicion en la que esta el menor numero encontrado. Si hay varios se da prioridad al de + a la izquierda

"""def isDegenerateSolution(minNumberPosition):

    contRepeatedNumbers = 0
    searchedNumber = restrictionsMatrix[0][minNumberPosition]

    for number in restrictionsMatrix[0]:
        if number == searchedNumber:
            contRepeatedNumbers += 1
    
    if contRepeatedNumbers > 1:                 #si hay mas de un numero repetido (el mismo), es solucion degenerada
        return True
    
    else:
        return False"""


def isOptimal():
    #optimal = True

    firstRestriction = restrictionsMatrix[0]
    minPosNumber = np.argmin(firstRestriction)

    minNumber = restrictionsMatrix[0][minPosNumber]

    if minNumber > 0 or minNumber == 0:
        return True
    
    else:
        return False

    """for number in restrictionsMatrix[0]:
        if number < 0:
            return False
    
    return True"""

"""    i = 0
    while i <= len(restrictionsMatrix[0]):
        if restrictionsMatrix[0][i] < 0:
            optimal = False
    
    return optimal"""
    




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
   # newRow = []

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
                    matrix[i][j] = float(matrix[i][j])
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
                list[k] = float(list[k])
                k += 1
            
        else:
            list[k] = int(list[k])
            k += 1

