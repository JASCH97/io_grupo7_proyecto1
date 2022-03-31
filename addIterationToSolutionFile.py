from validationsBeforeMethodSelection import *
from utilityFunctions import *
from readAndSaveTxtInformation import fileOut as f

#global variables
bVIn = [0]
bVOut = [0]
pivotNumber = [0]
nonBoundedSolution = [False]

"""
Function: addIterationToFinalSolution
Input: is optimal, iteration number, augmented, degenerate, not bounded and multiple solutions
Output: -
Description: Function that writes the iterations in the output file
"""
def addIterationToFinalSolution(optimal,iterationNumber,augmentedSolution,degenerateSolution,nonBoundedSolution,multipleSolutions,notFeasible):

    # adds more space if the problem has complex numbers
    if selectedMethod[0] == 0:
        spaceBetweenX = 5
        spaceForEachX = 6
        f[0].write("\nStatus: " + str(iterationNumber) + "\n\n")
        f[0].write("BV |   ")
        
        for variable in strTotalVariables:
            if variable == strTotalVariables[len(strTotalVariables) - 1]:
                f[0].write(str(variable))
            else:
                f[0].write(str(variable) +"         ")

        f[0].write("       | RS\n") 

        f[0].write("---|")
        f[0].write( (11* (contVariables[0])) * "-")
        f[0].write("-|---------\n")
    else:
        spaceBetweenX = 11
        spaceForEachX = 12
        f[0].write("\nStatus: " + str(iterationNumber) + "\n\n")
        f[0].write("BV |   ")
        
        for variable in strTotalVariables:
            if variable == strTotalVariables[len(strTotalVariables) - 1]:
                f[0].write(str(variable))
            else:
                f[0].write(str(variable) +"                     ")

        f[0].write("                     | RS\n") 

        f[0].write("---|")
        f[0].write( (11* (contVariables[0])) * "-")
        f[0].write("---------------------------------------------------------------------------|------\n")


    contBvLeft = len(bV) - 1
    j = 0

    while j <= len(restrictionsMatrix) - 1:

        if j == 0:
            f[0].write("U  |   ")

        elif j != 0 and j-1 <= contBvLeft:
            f[0].write(bV[j-1] + " |   ")

        i = 0
        while i <= len(restrictionsMatrix[j]) - 1:
            
            if i == len(restrictionsMatrix[j]) - 1:
                f[0].write(str(restrictionsMatrix[j][i]))
                i += 1

            else:
                f[0].write(str(restrictionsMatrix[j][i]))
                spaceNeeded = spaceBetweenX + (spaceForEachX - len(str(restrictionsMatrix[j][i])))

                while spaceNeeded != 0: 
                    f[0].write(" ")
                    spaceNeeded -=1

                i += 1
        
        finalSpace = spaceForEachX - len(str(restrictionsMatrix[j][len(restrictionsMatrix[j])-1])) + 3
        if selectedMethod[0] != 0:
            finalSpace = spaceForEachX - len(str(restrictionsMatrix[j][len(restrictionsMatrix[j])-1])) + 11
        
        f[0].write((finalSpace * " ") + "| " + str(rightSide[j]))
        
        
        # dividing line 
        f[0].write("\n---|")
        f[0].write( (11* (contVariables[0])) * "-")
        if selectedMethod[0] == 0:
            f[0].write("-|---------\n")
        else:
            f[0].write("---------------------------------------------------------------------------|------\n")
        
        j += 1


    if iterationNumber == 0:
        f[0].write("\nAugmented Initial Solution:  ")
    
    elif iterationNumber > 0:
        f[0].write("\nAugmented Solution:  ")

    f[0].write("(")


    k = 0

    while k <= len(augmentedSolution) - 1:
        if k == len(augmentedSolution) - 1:
            f[0].write(" " + str(augmentedSolution[k]) + " )")
            k += 1
        
        else:
            f[0].write(" " + str(augmentedSolution[k]) + ",")
            k += 1


    f[0].write("  -->    U = " + str(rightSide[0]))

    
    if degenerateSolution == True:
        f[0].write("\nThe solution is degenerate.\nThere are two or more minimum coefficients on the right side with the same value")
    
    if(optimal == False):
        f[0].write("\nNot Optimal Result")
        if iterationNumber > 0:
            f[0].write("\nBV incoming = " + bVIn[0] + "\nBV outcoming = " + bVOut[0] + "\nPivot Number = " + str(pivotNumber[0]))
        
    elif(optimal == True):
        f[0].write("\nOptimal Result")

    f[0].write("\nBasic Variables = ")
    for variable in bV:
        f[0].write(str(variable) + "  ")
        
    f[0].write("\nNon Basic Variables = ")
    for variable in nBV:
        f[0].write(str(variable) + "  ")

    
    if nonBoundedSolution == True:
        f[0].write("\nThis problem has non bounded solution!.\nThe coefficients on the right side are negative or undefined.\nCannot continue.")
        f[0].write("\n")

    if multipleSolutions == True:
        f[0].write("\nIn one of the non-basic variables of the previous iteration, a 0 is found.\nThat is why this problem has multiple solutions.")
        f[0].write("\n")
    
    if notFeasible == True:
        f[0].write("\n\nThis problem has no feasible solution!\nAn artificial variable has a positive value in the final solution.")

    f[0].write("\n")
    
    # don't close file, since its needed for further iterations

"""
Function: getPivotAndVariablesInfo
Input: incoming and outcoming variables, pivot number
Output: -
Description: Function that assigns corresponding values when changing in and outcoming variables
"""
def getPivotAndVariablesInfo(incoming,outcoming,pivot):
    global bVIn
    global bVOut
    global pivotNumber

    bVIn[0] = incoming
    bVOut[0] = outcoming
    pivotNumber[0] = pivot
