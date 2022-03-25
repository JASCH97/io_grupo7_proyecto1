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
    global pivotNumber
    global nBV
    
    iterationNumber = 0
    degenerateCont = 0
    optimal = isOptimal()

    while optimal != True:                                        
        degenerateFlag = False

        if iterationNumber == 0:
            optimal = isOptimal()                                               #Se pregunta si la solucion aumentada es optima 
            getAugmentedSolutionSimplex()                                       #Al ser primer estado simplemente se da la solucion aumentada e informacion de variables
            improveNumbersPresentation(restrictionsMatrix, rightSide)
            improveNumbersPresentation(restrictionsMatrix, augmentedSolution)               #se hace un llamado extra para limpiar la solicion aumentada
            addIterationToFinalSolution(optimal,iterationNumber,augmentedSolution,degenerateFlag,False,False)              #Se agrega el estado 0 al archivo de salida txt
            iterationNumber += 1
            

        else:
            pivotCol = np.argmin(restrictionsMatrix[0])
            dividingNumbers = getColumnDividingNumbers(pivotCol)                            #numeros que dividen el lado derecho
            nonBoundedSolution = validateSpecialCases("is non bounded?",dividingNumbers)

            if nonBoundedSolution == True:  
                print("\n")    
                printFinalSolution(augmentedSolution,optimal)                                    
                print("The next iteration has non bounded solution!.\nThe coefficients on the right side are negative or undefined.\nThe problem has no solution.\n")
                #addIterationToFinalSolution(optimal, iterationNumber,augmentedSolution,degenerateFlag,True,False)
                f[0].write("The next iteration has non bounded solution!.\nThe coefficients on the right side are negative or undefined.\nThe problem has no solution.\n")
                exit(0)
            
            else:
                pivotRow = validateSpecialCases("pivot row position", dividingNumbers)
                
                if (validateSpecialCases("is degenerate?", dividingNumbers) == True):   
                    degenerateFlag = True
                    degenerateCont += 1
                                                          

                pivotNumber = transposeMatrix(restrictionsMatrix)[pivotCol][pivotRow]             #en la matriz transpuesta en la columa y fila del pivot encontramos el pivot       

                divideRestrictionNumbers(pivotRow, pivotNumber)                               #se divide la fila del # pivot entre el numero pivot

                checkZerosInPivotColumn(restrictionsMatrix, pivotRow,pivotCol)      #se ponen 0's en la columna pivot y se obtienen indices/numeros para operar sobre renglones
                    
                bVOutcoming = bV[pivotRow - 1]
                bV[pivotRow - 1] = "x" + str(pivotCol+1)                                        #se resta 1 a pivotRow porque en bV no esta la U, solo las X's

                uptadeNonBasicVariables(nBV)                                                    #Se actualizan las variables no basicas

                getPivotAndVariablesInfo(bV[pivotRow - 1], bVOutcoming, pivotNumber)


                rowOperations(restrictionsMatrix, restrictionsMatrix[pivotRow],pivotCol,pivotRow)

                resetOperableList()                                         

                improveNumbersPresentation(restrictionsMatrix,rightSide)
                getAugmentedSolutionSimplex() 
                                    
                optimal = isOptimal()
                   
                addIterationToFinalSolution(optimal,iterationNumber,augmentedSolution,degenerateFlag,nonBoundedSolution,False)   
                iterationNumber += 1

    simplexMethodAux(degenerateCont, nBV, augmentedSolution,iterationNumber + 1)


def simplexMethodAux(degenerateCont, nBV, augmentedSolution,iterationNumber):
    previousSolution = "Final Augmented Solution 1 -> "+ str(augmentedSolution) + "\n->  U = " + str(rightSide[0])
    degenerateFlag = False

    if degenerateCont > 0:
        print("While solving this problem one or more solutions were considered degenerate.\nIn the output file you will find in which iteration status occurs.\n")
        printFinalSolution(augmentedSolution,True)

    elif checkZerosInNonBasicVariables("zeros in nBV?", nBV) == True:

        pivotCol = checkZerosInNonBasicVariables("new pivot column?",nBV)
        dividingNumbers = getColumnDividingNumbers(pivotCol)                            #numeros que dividen el lado derecho
        nonBoundedSolution = validateSpecialCases("is non bounded?",dividingNumbers)

        if nonBoundedSolution == True:                                          
            print("\nThe next iteration has non bounded solution!.\nThe coefficients on the right side are negative or undefined.\nCannot continue.\n")
            addIterationToFinalSolution(optimal, iterationNumber,augmentedSolution,degenerateFlag,True,False)
            printFinalSolution(augmentedSolution,optimal)
            exit(0)
        
        else:
            pivotRow = validateSpecialCases("pivot row position", dividingNumbers)
            
            if (validateSpecialCases("is degenerate?", dividingNumbers) == True):   
                degenerateFlag = True
                degenerateCont += 1
                                                        

            pivotNumber = transposeMatrix(restrictionsMatrix)[pivotCol][pivotRow]                 #en la matriz transpuesta en la columa y fila del pivot encontramos el pivot       

            divideRestrictionNumbers(pivotRow, pivotNumber)                                 #se divide la fila del # pivot entre el numero pivot

            checkZerosInPivotColumn(restrictionsMatrix, pivotRow,pivotCol)         #se ponen 0's en la columna pivot y se obtienen indices/numeros para operar sobre renglones
                
            bVOutcoming = bV[pivotRow - 1]
            bV[pivotRow - 1] = "x" + str(pivotCol+1)                                              #se resta 1 a pivotRow porque en bV no esta la U, solo las X's

            uptadeNonBasicVariables(nBV)                                                    #Se actualizan las variables no basicas

            getPivotAndVariablesInfo(bV[pivotRow - 1], bVOutcoming, pivotNumber)

            rowOperations(restrictionsMatrix, restrictionsMatrix[pivotRow],pivotCol,pivotRow)

            resetOperableList()                                        

            improveNumbersPresentation(restrictionsMatrix,rightSide)
            getAugmentedSolutionSimplex() 
                                     #
            optimal = isOptimal()
                
            addIterationToFinalSolution(optimal,iterationNumber,augmentedSolution,degenerateFlag,nonBoundedSolution,True)     
 

            print("\nThis problem has multiple solutions. You will find more details in the output txt file.")
            print(previousSolution)
            print("Final Augmented Solution 2 -> "+ str(augmentedSolution) + "\n->  U = " + str(rightSide[0]))
            print("Both Are Optimal Solutions\n")

    else:
        printFinalSolution(augmentedSolution,True)

def getAugmentedSolutionSimplex():
    global augmentedSolution

    while augmentedSolution != []:              #se resetea para que no se acumulen valores con el append
        augmentedSolution.pop(0)

    i = 0

    #primero se llena de ceros la solucion aumentada por facilidad
    while i <= contVariables[0] - 1:
        augmentedSolution.append(0)
        i += 1
 
    #Luego simplemente por cada variable basica se agrega a la solucion aumentada su valor correspondiente en el LD **A prueba, se necesitan varias iteraciones para comprobar
    #No se usan los GL ya que la estrategia es verificar las variables basicas para saber cual es la solucion aumentada 
    k = 0
    rightSideValues = rightSide[1:]                             # se ignora el primer elemento del lado derecho ya que corresponde a la funcion objetivo

    while k <= len(bV) - 1:

        strXVariable = bV[k][1]
        augmentedSolution[int(strXVariable) - 1] = rightSideValues[k]

        k += 1

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

