from readAndSaveTxtInformation import *
from validationsBeforeMethodSelection import *
from utilityFunctions import *
from addIterationToSolutionFile import *

#global variable
augmentedSolution = []

"""
Function: simplexMethod
Input: -
Output: -
Description: Function that solves a problem using the simplex method. After obtaining the initial augmented solution, 
use simplexMethodAux() function for the other iterations
"""
def simplexMethod(twoPhaseFlag):
    global augmentedSolution
    global pivotNumber
    global nBV
    iterationNumber = 0
    degenerateCont = 0
    optimal = isOptimal()

    while optimal != True:                                        
        degenerateFlag = False

        if iterationNumber == 0:
            optimal = isOptimal()                                                   # checks if augmented solution is optimal
            getAugmentedSolutionSimplex()                                           # since its first iteration, we only write the augmented solution and variable information
            addIterationToFinalSolution(optimal,iterationNumber,augmentedSolution,degenerateFlag,False,False,False)   # prints first iteration to solution file
            iterationNumber += 1
            
        else:
            # checks if there is a complex number in the matrix
            if np.iscomplex(restrictionsMatrix).any():
                modifiedMatrix = np.array(restrictionsMatrix)
                sumofComplex = modifiedMatrix[0].real + modifiedMatrix[0].imag*10000    # multiplies by a big M to obtain the minimum value
                pivotCol = np.argmin(sumofComplex)
            else:
                pivotCol = np.argmin(restrictionsMatrix[0])
            
            dividingNumbers = getColumnDividingNumbers(pivotCol)                        # numbers that divide the right side
            nonBoundedSolution = validateSpecialCases("is non bounded?",dividingNumbers)

            if nonBoundedSolution == True:  
                print("\n")    
                printFinalSolution(augmentedSolution,optimal)                                    
                print("The next iteration has non bounded solution!.\nThe coefficients on the right side are negative or undefined.\nThe problem has no solution.\n")
                f[0].write("The next iteration has non bounded solution!.\nThe coefficients on the right side are negative or undefined.\nThe problem has no solution.\n")
                exit(0)
            
            else:
                pivotRow = validateSpecialCases("pivot row position", dividingNumbers)
                
                if (validateSpecialCases("is degenerate?", dividingNumbers) == True):   
                    degenerateFlag = True
                    degenerateCont += 1
                                                          

                pivotNumber = transposeMatrix(restrictionsMatrix)[pivotCol][pivotRow]   # finds pivot number in tranposed matrix from column and row of pivot

                divideRestrictionNumbers(pivotRow, pivotNumber)                         # pivot row is divided by pivot number
                
                checkZerosInPivotColumn(restrictionsMatrix, pivotRow,pivotCol)        # in pivot column we put 0's and we get indexes/numbers to operate on rows
                    
                bVOutcoming = bV[pivotRow - 1]
                bV[pivotRow - 1] = strTotalVariables[pivotCol]                         # subtract 1 from pivotRow since bV doesn't has the U, only X's

                uptadeNonBasicVariables(nBV)                                           # update non basic variables

                getPivotAndVariablesInfo(bV[pivotRow - 1], bVOutcoming, pivotNumber)

                rowOperations(restrictionsMatrix, restrictionsMatrix[pivotRow],pivotCol,pivotRow)   # Operations are performed on rows

                resetOperableList()                                                 # The lists of rows and numbers to operate are reset to avoid problems

                getAugmentedSolutionSimplex() 

                optimal = isOptimal()
                
                if any(var.startswith('a') for var in bV) and optimal:
                    addIterationToFinalSolution(optimal,iterationNumber,augmentedSolution,degenerateFlag,nonBoundedSolution,False,True)
                    print("\nThis problem has no feasible solution! \nAn artificial variable has a positive value in the final solution.\n")
                else:
                    addIterationToFinalSolution(optimal,iterationNumber,augmentedSolution,degenerateFlag,nonBoundedSolution,False,False)   
                iterationNumber += 1


    if twoPhaseFlag == True:                                              #If the flag is True, it waits for the final changes of the second phase to be made before continuing.
        #adaptationForTheFinalPhase()
        None
        
        

    else:
        simplexMethodAux(degenerateCont, nBV, augmentedSolution,iterationNumber + 1)

"""
Function: simplexMethodAux
Input: degenerate counter, nBV, augmented solution and iteration number
Output: -
Description: Auxiliar function for simplex method
"""
def simplexMethodAux(degenerateCont, nBV, augmentedSolution,iterationNumber):
    previousSolution = "Final Augmented Solution 1 -> "+ str(augmentedSolution) + "\n->  U = " + str(rightSide[0])
    degenerateFlag = False

    if degenerateCont > 0:
        print("While solving this problem one or more solutions were considered degenerate.\nIn the output file you will find in which iteration status occurs.\n")
        printFinalSolution(augmentedSolution,True)

    elif checkZerosInNonBasicVariables("zeros in nBV?", nBV) == True:

        pivotCol = checkZerosInNonBasicVariables("new pivot column?",nBV)
        dividingNumbers = getColumnDividingNumbers(pivotCol)                                
        nonBoundedSolution = validateSpecialCases("is non bounded?",dividingNumbers)

        if nonBoundedSolution == True:                                          
            print("\nThe next iteration has non bounded solution!.\nThe coefficients on the right side are negative or undefined.\nCannot continue.\n")
            addIterationToFinalSolution(optimal, iterationNumber,augmentedSolution,degenerateFlag,True,False,False)
            printFinalSolution(augmentedSolution,optimal)
            exit(0)
        
        else:
            pivotRow = validateSpecialCases("pivot row position", dividingNumbers)
            
            if (validateSpecialCases("is degenerate?", dividingNumbers) == True):   
                degenerateFlag = True
                degenerateCont += 1
                                                        
            pivotNumber = transposeMatrix(restrictionsMatrix)[pivotCol][pivotRow]   

            divideRestrictionNumbers(pivotRow, pivotNumber)     

            checkZerosInPivotColumn(restrictionsMatrix, pivotRow,pivotCol)      
                
            bVOutcoming = bV[pivotRow - 1]
            bV[pivotRow - 1] = strTotalVariables[pivotCol]      

            uptadeNonBasicVariables(nBV)        

            getPivotAndVariablesInfo(bV[pivotRow - 1], bVOutcoming, pivotNumber)

            rowOperations(restrictionsMatrix, restrictionsMatrix[pivotRow],pivotCol,pivotRow)

            resetOperableList()                                        

            getAugmentedSolutionSimplex() 

            optimal = isOptimal()
                
            addIterationToFinalSolution(optimal,iterationNumber,augmentedSolution,degenerateFlag,nonBoundedSolution,True,False)     
 
            print("\nThis problem has multiple solutions. You will find more details in the output txt file.")
            print(previousSolution)
            print("Final Augmented Solution 2 -> "+ str(augmentedSolution) + "\n->  U = " + str(rightSide[0]))
            print("Both Are Optimal Solutions\n")

    else:
        printFinalSolution(augmentedSolution,True)

"""
Function: getAugmentedSolutionSimplex
Input: -
Output: -
Description: Function that calculates the augmented solution
"""
def getAugmentedSolutionSimplex():
    global augmentedSolution

    while augmentedSolution != []:  # resets lists since values from previous iterations remain
        augmentedSolution.pop(0)

    i = 0

    # augmentedSolution list is filled with ceros
    while i <= contVariables[0] - 1:
        augmentedSolution.append(0)
        i += 1
    
    # for each basic variable, add the value on the right side to the augmented solution
    k = 0
    rightSideValues = rightSide[1:]                                     # first value is ignored since its from the objective function

    while k <= len(bV) - 1:

        strXVariable = bV[k][1]
        augmentedSolution[int(strXVariable) - 1] = round(rightSideValues[k] , 4)

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

    # removes right side values from restrictions matrix
    for restriction in restrictionsMatrix:
        rightSide.append(restriction[len(restriction) - 1])
        restriction.pop(len(restriction) - 1)

    # remove the excess number that was added before
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
