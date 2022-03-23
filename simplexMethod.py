from readAndSaveTxtInformation import *
from validationsBeforeMethodSelection import *
from utilityFunctions import *
from addIterationToSolutionFile import *

augmentedSolution = []

"""
Function: simplexMethod
Input:
Output:
Description: Function that solves a problem using the simplex method
"""
def simplexMethod():
    global augmentedSolution
    global bVIn
    global bVOut
    global pivotNumber
    #global optimal
    
    iterationNumber = 0
    boundedSolution = False                          #acotada
    degenerateSolution = False                       #degenerada

    #f = open(fileName[0] + "_solution" + ".txt","w")
    #createSimplexTabularForm()

    #print(restrictionsMatrix)
    #while optimal[0] != True:
    while iterationNumber < 2:                                                  #--------------------------ARREGLAR---------------------------
        #Si es la primera iteracion
        if iterationNumber == 0:
            optimal = isOptimal()                                               #Se pregunta si la solucion aumentada es optima 
            getAugmentedSolutionSimplex()                                       #Al ser primer estado simplemente se da la solucion aumentada e informacion de variables
            improveNumbersPresentation(restrictionsMatrix, rightSide)
            addIterationToFinalSolution(optimal,iterationNumber)              #Se agrega el estado 0 al archivo de salida txt
            iterationNumber += 1
            
        #optimal = isOptimal()
        #while optimal != True:
        else:
            pivotCol = np.argmin(restrictionsMatrix[0])
            #degenerateSolution = isDegenerateSolution(pivotCol)
            dividingNumbers = getColumnDividingNumbers(pivotCol)                            #numeros que dividen el lado derecho
            boundedSolution = validateSpecialCases("is bounded?",dividingNumbers)
            pivotRow = validateSpecialCases("pivot row position", dividingNumbers)
                
            pivotNumber = transposeMatrix(restrictionsMatrix)[pivotCol][pivotRow]                 #en la matriz transpuesta en la columa y fila del pivot encontramos el pivot       

            divideRestrictionNumbers(pivotRow, pivotNumber)                                 #se divide la fila del # pivot entre el numero pivot

            checkZerosInPivotColumn(restrictionsMatrix, pivotRow,pivotCol)         #se ponen 0's en la columna pivot y se obtienen indices/numeros para operar sobre renglones
                
            bVOutcoming = bV[pivotRow - 1]
            bV[pivotRow - 1] = "x" + str(pivotCol)                                              #se resta 1 a pivotRow porque en bV no esta la U, solo las X's

            getPivotAndVariablesInfo(bV[pivotRow - 1], bVOutcoming, pivotNumber)

            #print(restrictionsMatrix[pivotRow])
            rowOperations(restrictionsMatrix, restrictionsMatrix[pivotRow],pivotCol,pivotRow)

            resetOperableList()                                         #se resetean las listas de indices/numeros en caso de una siguiente iteracion. A PRUEBA!!!!!!!!!!!

            improveNumbersPresentation(restrictionsMatrix,rightSide)
            getAugmentedSolutionSimplex()                                       #Al ser primer estado simplemente se da la solucion aumentada e informacion de variables
            optimal = isOptimal()
            addIterationToFinalSolution(optimal,iterationNumber)              #Se agrega el estado 0 al archivo de salida txt
            
            iterationNumber += 1
                

            
        #print(augmentedSolution)
        print(optimal)



def getAugmentedSolutionSimplex():
    global augmentedSolution

    i = 0

    #primero se llena de ceros la solucion aumentada por facilidad
    while i <= contVariables[0] - 1:
        augmentedSolution.append(0)
        i += 1

    #Luego simplemente por cada variable basica se agrega a la solucion aumentada su valor correspondiente en el LD **A prueba, se necesitan varias iteraciones para comprobar
    #No se usan los GL ya que la estrategia es verificar las variables basicas para saber cual es la solucion aumentada 
    for variable in bV:
        augmentedSolution[(int(str(variable)[1]) - 1)] = rightSide[int(str(variable)[1]) - numberOfDecisionVariables[0]]


"""
Function: createTabularForm
Input: -
Output: -
Description: Function that takes the restrictions with the slack variables and converts them in to tabular form for simplex method
"""
def createSimplexTabularForm():

    global rightSide
    global restrictionsMatrix

    #Quita de las restricciones el numero que va en el lado derecho
    for restriction in restrictionsMatrix:
        rightSide.append(restriction[len(restriction) - 1])
        restriction.remove(restriction[len(restriction) - 1])

    #Se elimina el numero que queda de exceso
    for restriction in restrictionsMatrix:
        if restriction == restrictionsMatrix[0]:
            None
        else:
            restriction.pop(len(restriction) - 1)
    
    #print(restrictionsMatrix)
    modifyRestrictionsForTabularForm()


"""
Function: modifyRestrictionsForTabularForm
Input: -
Output: -
Description: Function that takes the restrictions and adds 0s and 1s based on the slack variables found
"""
def modifyRestrictionsForTabularForm():
    i = 0
    nextOnePosition = len(restrictionsMatrix[0])  
    while i <= len(restrictionsMatrix) - 1:
        contVariablesLeft = contVariables[0] - len(restrictionsMatrix[i])

        while contVariablesLeft != 0:

            restrictionsMatrix[i].append(0)
            contVariablesLeft -= 1

        i += 1

    i = 1
    while i <= len(restrictionsMatrix) - 1:

        restrictionsMatrix[i][nextOnePosition] = 1
        nextOnePosition += 1
        i += 1