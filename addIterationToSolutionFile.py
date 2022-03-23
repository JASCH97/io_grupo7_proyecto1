from validationsBeforeMethodSelection import *
from utilityFunctions import *
from readAndSaveTxtInformation import fileOut as f

bVIn = [0]
bVOut = [0]
pivotNumber = [0]

"""
Function:
Input:
Output:
Description: 
"""
def addIterationToFinalSolution(optimal,iterationNumber):

    spaceBetweenX = 5
    spaceForEachX = 6
    f[0].write("\nStatus: " + str(iterationNumber) + "\n\n")
    f[0].write("BV |   ")
    
    for number in intTotalVariables:
        if number == intTotalVariables[len(intTotalVariables) - 1]:
            f[0].write("x"+str(number))
        else:
            f[0].write("x"+str(number)+"         ")

    f[0].write("       | RS\n") 

    f[0].write("---|")
    f[0].write( (11* (contVariables[0])) * "-")
    f[0].write("-|----\n")


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
        #print(finalSpace)
        f[0].write((finalSpace * " ") + "| " + str(rightSide[j]))
        
        
        #linea divisoria de abajo
        f[0].write("\n---|")
        f[0].write( (11* (contVariables[0])) * "-")
        f[0].write("-|----\n")
    
        j += 1


    if iterationNumber == 0:
        f[0].write("\nAugmented Initial Solution:\n")
    
    elif iterationNumber > 0:
        f[0].write("\nAugmented Solution:\n")

    f[0].write("(")
        
    zeroVariables = numberOfDecisionVariables[0]
    while zeroVariables != 0:
        f[0].write(" 0" + ",")
        zeroVariables -= 1
        
    posNextSolutionValue = numberOfDecisionVariables[0] - 1
    while posNextSolutionValue <= len(rightSide) - 1:
        if posNextSolutionValue ==  len(rightSide) - 1:
            f[0].write(" "+ str(rightSide[posNextSolutionValue]) + " )")
            posNextSolutionValue += 1
            
        else:
            f[0].write(" "+ str(rightSide[posNextSolutionValue]) + ",")
            posNextSolutionValue += 1

    f[0].write("          U = " + str(rightSide[0]))

    if(optimal == False):
        f[0].write("\nNot Optimal Result")
        
    elif(optimal == True):
        f[0].write("\nOptimal Result")

    f[0].write("\nBasic Variables = ")
    for variable in bV:
        f[0].write(str(variable) + "  ")
        
    f[0].write("\nNon Basic Variables = ")
    for variable in nBV:
        f[0].write(str(variable) + "  ")

    if iterationNumber > 0:
        f[0].write("\nBV incoming = " + bVIn[0] + "\nBV outcoming = " + bVOut[0] + "\nPivote Number = " + str(pivotNumber[0]))


    f[0].write("\n")

    #f.close()                                         #Si se le hace close no se puede escribir mas sobre el archivo en otras iteraciones


def getPivotAndVariablesInfo(incoming,outcoming,pivot):
    global bVIn
    global bVOut
    global pivotNumber

    bVIn[0] = incoming
    bVOut[0] = outcoming
    pivotNumber[0] = pivot



