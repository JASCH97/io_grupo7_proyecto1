import sys

#global variables
fileName = ""
firstLine = []
secondLine = []
numberOfDecisionVariables = 0
numberOfRestrictions = 0
objectiveFunction = []
stringRestrictions = []
restrictionsMatrix = []
restrictionsInequalities = []
bV = []
nBV = []
strTotalVariables = ""
intBvariables = []
intTotalVariables = []
contVariables = 0
slackVariables = []                                
rightSide = []
augmentedSolution = []
helpMessage = """\nFor this program to work properly, a file in .txt format is required. 
This file should contain the parameters needed to solve a problem using the normal simplex method, the Big M method 
or the two-phase method.

These parameters must be organized by lines in the txt file and following the following order:
First line:
       -> Method to use, Optimization (max or min), Number of decision variables and Number of constraints
Second line:
       -> Coefficients of the objective function
Following lines:
       -> Coefficients of the restrictions and sign of restriction 
                  
Example:
    0,max,2,3
    3,5
    2,1,<=,6
    -1,3,<=,9
    0,1,<=,4

NOTE: Each parameter must be separated by a comma. Also, make sure the .txt file is inside the same folder as 
this program. Remember to write the name correctly, otherwise it won't work. 
"""

"""
Function: validateInputFile
Input: -
Output: -
Description: This function takes the name of the input file and checks if the -h parameter was passed or not 
             If all it's ok, another function is called to store the information 
"""
def validateInputFile():
    global fileName

    if len(sys.argv) == 2 and sys.argv[1] == "-h":       #it only wants to read the help message, the file is not given as a parameter
        print(helpMessage)
        exit()

    elif len(sys.argv) == 3 and sys.argv[1] == "-h":     #the file was entered as a parameter and it requires the help message
        print(helpMessage)
        inputFileName = sys.argv[2]
        fileName = inputFileName[2:len(inputFileName) - 4]
        #print(fileName)
        saveInformationFromFile(sys.argv[2])

    elif len(sys.argv) == 2 and sys.argv[1] != "-h":     #the file was entered as a parameter and does NOT require the help message
        inputFileName = sys.argv[1]
        fileName = inputFileName[0:len(inputFileName) - 4]       
        #print(fileName)
        saveInformationFromFile(sys.argv[1])

    else:
        print("You have entered the commands for the operation of this program incorrectly. Try again!")


"""
Function: saveInformationFromFile
Input: Name of the file with the information of the problem to solve
Output: - 
Description: This function saves the information of the .txt file in data structures to be able to manipulate them
"""
def saveInformationFromFile(fileName):
    global firstLine
    global secondLine
    global stringRestrictions
    global numberOfDecisionVariables
    global numberOfRestrictions
    global objectiveFunction

    i = 2
    information = []

    with open(fileName) as file:
        lines = file.readlines()

        if len(lines) < 3:
            print("Insufficient information in the .txt file \nPlease try again!")
            exit() 

        else:
            for line in lines:
                information.append(line.strip('\n'))
        
        firstLine = information[0]
        secondLine = information[1]
        numberOfDecisionVariables = int(firstLine[6:7])
        numberOfRestrictions = int(firstLine[8:9])

        while i <= len(lines) -1:
            stringRestrictions = stringRestrictions + [information[i]]
            i+=1
        
        i = 0
        newObjectiveFunctionForm = secondLine.split(sep=',')

        while i <= len(newObjectiveFunctionForm) - 1:
            objectiveFunction.append(float(newObjectiveFunctionForm[i]) * -1)
            i+=1
        
        objectiveFunction.append(0)                                                 #Se agrega el 0 del lado derecho

        restrictionsMatrix.append(objectiveFunction)


"""
Function: extractInformationFromRestrictions
Input: -
Output: -
Description: Function that extracts the restrictions that are in string format and passes them in a matrix with operable 
             numbers, also saves the inequalities in a list
"""
def extractInformationFromRestrictions():
    global stringRestrictions
    global restrictionsMatrix
    global restrictionsInequalities


    while stringRestrictions != []:
        i = 0
        newRestictionForm = stringRestrictions[0].split(sep=',')                            #.split(sep=',') separate all elements after a comma in a str

        while i <= len(newRestictionForm) - 1:

            if newRestictionForm[i] == "<=" or newRestictionForm[i] == ">=" or newRestictionForm[i] == "=":
                restrictionsInequalities.append(newRestictionForm[i])
                newRestictionForm.remove(newRestictionForm[i])

            newRestictionForm[i] = float(newRestictionForm[i])
            i+=1
    

        stringRestrictions.pop(0)
        restrictionsMatrix.append(newRestictionForm)

"""
Function: checkNegativesOnRightSide
Input: -
Output: -
Description: Function that checks if there are negative numbers on the right side of the equation
"""
def checkNegativesOnRightSide():
    global restrictionsMatrix
    global restrictionsInequalities

    restrictionsIndex = []
    i = 0
    while i <= len(restrictionsMatrix) - 1:
        if restrictionsMatrix[i][len(restrictionsMatrix[i]) -1] < 0:
            restrictionsIndex.append(i-1)

        i+=1

    while restrictionsIndex != []:

        restrictionsMatrix[restrictionsIndex[0] + 1] = changeSignsOfRestriction(restrictionsMatrix[restrictionsIndex[0] + 1])
        if restrictionsInequalities[restrictionsIndex[0]] == ">=":
             restrictionsInequalities[restrictionsIndex[0]] = "<="
        
        else:
             restrictionsInequalities[restrictionsIndex[0]] = ">="
        
        restrictionsIndex.pop(0)


"""
Function: changeSignsOfRestriction
Input: -
Output: -
Description: Function that multiplies a restriction by (-1) to change the sign of its variables
"""
def changeSignsOfRestriction(restriction):
    newRestriction = []
    for number in restriction:
        if number == 0:
            newRestriction.append(0)
        else:
            newRestriction.append(number * (-1))

    return newRestriction


"""
Function: selectMethod
Input: -
Output: -
Description: Function that selects which method to use to solve the problem
"""
#Funcion que selecciona el método mediante el cual se va a resolver el problema
def selectMethod():
    if firstLine[0] == "0" and verifyInequalities() == "simplex":                              #Se valida que se pueda simplex
        augmentedForm(0)
        defineStarterBasicAndNoBasicVariables()
        simplexMethod()

    #elif firstLine[0] == "0" and verifyInequalities() == "no simplex":                         #El usuario pide simplex pero hay un >= o un =, se procede a gran M
        #gran M
    
    #elif firstLine[0] == "1" and verifyInequalities() == "simplex":                            #El usuario pide gran M pero todas las restricciones son <=, se hace simplex
        #simplexMethod(firstLine[2:5])

    #elif firstLine[0] == "1" and verifyInequalities() == "no simplex":
        #gran M

    #agregar los casos de dos fases


"""
Function: verifyInequalities
Input: -
Output: -
Description: Function that checks the list of inequalities to know which method should be used
"""
#Simple Version. improve later
def verifyInequalities():
    verificationFlag = "simplex"

    for inequality in restrictionsInequalities:
        if inequality != "<=":
            verificationFlag = "no simplex"

    return verificationFlag  


"""
Function: augmentedForm
Input: -
Output: -
Description: Function that takes the restrictions matrix and passes it to its augmented form 
             (adding the slack variables)
"""
def augmentedForm(method):
    global restrictionsMatrix
    global slackVariables
    global intBvariables
    
    #Only the slack variables are added
    if method == 0:                                                             #For simplex method
        contSlackAdded = numberOfDecisionVariables                              #Slack variables are created using the number of decision variables
        i = 1

        while i <= len(restrictionsMatrix) - 1:
            restrictionsMatrix[i].insert(len(restrictionsMatrix[i]) -1,1)
            i +=1
            contSlackAdded += 1
            slackVariables.append("x" + str(contSlackAdded))
            intBvariables.append(contSlackAdded)


    #Excess, artificial and M variables are added
    #elif method == 1:                                                           #For big M method


    #else:                                                                       #For two-phase method


"""
Function: defineBasicAndNoBasicVariables
Input: -
Output: -
Description: Function that defines which are the basic and non-basic variables at the beginning of the problem.
"""
def defineStarterBasicAndNoBasicVariables():
    global bV
    global nBV
    global strTotalVariables
    global contVariables
    global intTotalVariables

    bV = slackVariables
    i = 1
    
    while i <= numberOfDecisionVariables:
        nBV.append("x" + str(i))
        i+=1 
    
    for variable in nBV:
        strTotalVariables = strTotalVariables + variable
        contVariables = contVariables + 1

    for variable in bV: 
        strTotalVariables = strTotalVariables + variable 
        contVariables = contVariables + 1

    j = 1
    while j <= contVariables:
        intTotalVariables.append(j)
        j += 1


"""
Function: simplexMethod
Input:
Output:
Description: Function that solves a problem using the simplex method
"""
def simplexMethod():
    global augmentedSolution
    optimal = False
    GL = contVariables - numberOfRestrictions
    iterationNumber = 0
    boundedSolution = False                          #acotada
    degenerateSolution = False                       #degenerada
    f = open(fileName + "_solution" + ".txt","w")
    createTabularForm()
    
    #while optimal != True:
    #Si es la primera iteracion
    if iterationNumber == 0:
        optimal = isOptimal()                                               #Se pregunta si la solucion aumentada es optima 
        getAugmentedSolutionSimplex()                                       #Al ser primer estado simplemente se da la solucion aumentada e informacion de variables
        addIterationToFinalSolution(f,optimal,iterationNumber)              #Se agrega el estado 0 al archivo de salida txt
        iterationNumber += 1
    
    else:
        #preguntar si es optimo
        optimal = isOptimal()
        #si lo es -> ver si tiene soluciones multiples, de lo contrario fin.
        #si no es optimo: buscar el menor de la objetivo (si hay mas de uno poner que es acotada), seleccionar los valores de su columna y dividirlos por los del lado derecho. VERIFICAR SI EXISTEN CEROS
        if optimal == False:
            minNumberPosition = getMinNumberPosition()
        
            #degenerateSolution = isDegenerateSolution(minNumberPosition)
            dividingNumbers = getColumnDividingNumbers(minNumberPosition)                            #numeros que dividen el lado derecho
            boundedSolution = getPivotNumber("is bounded?",dividingNumbers)
            pivotNumber = getPivotNumber("pivot",dividingNumbers)
            pivotPosition = getPivotNumber("pivot position", dividingNumbers)


    print(augmentedSolution)
    print(optimal)


def getPivotNumber(request,dividingNumbers):
    pivot = 0
    pivotPosition = 0
    divisionResults = []
    numbersToDivide = rightSide[1:]
    validNumbersToDivide = []
    i = 0
    while i <= len(dividingNumbers) - 1:
        if dividingNumbers[i] < 0 or dividingNumbers[i] == 0:                                   # si los #'s que dividen son 0 o negativos se ignoran
            i += 1
        
        else:
            if numbersToDivide[i] < 0:
                i += 1
            else:
                divisionResults.append(numbersToDivide[i] / dividingNumbers[i])
                validNumbersToDivide.append(i)
                i += 1


    if request == "is bounded?":
        if divisionResults == []:
            return True
        else:
            return False
    
    elif request == "pivot":
        return min(divisionResults)
    
    else:
        """pivot = min(divisionResults)

        for pos in validDivisionPositions:
            if divisionResults[pos] == pivot:
                pivotPosition = pos"""
        #COMO OBTENER LA POS DEL NUMERO PIVOT ? (LA VARIABLE BASICA QUE CORRESPONDE A ESA FILA) **************************************************
        return pivotPosition


def getColumnDividingNumbers(minNumberPosition):
    dividingNumbers = []

    i = 1
    while i <= len(restrictionsMatrix) - 1:
        dividingNumbers.append(restrictionsMatrix[i][minNumberPosition])

        i += 1

    return dividingNumbers

def getMinNumberPosition():
    objectiveFunction = restrictionsMatrix[0]
    firstNumberFound = 0
    i = 0

    while i <= len(objectiveFunction) - 1:
        if objectiveFunction[i] != 0:
            firstNumberFound = objectiveFunction[i]
            i = len(objectiveFunction)
        
        i += 1
    
    minorNumberFound = firstNumberFound
    minNumberPosition = 0
    j = 0
    while j <= len(objectiveFunction) - 1:
        if objectiveFunction[j] < minorNumberFound and objectiveFunction[j] != 0:
            minorNumberFound = objectiveFunction[j]
            minNumberPosition = j
            j += 1
        
        j += 1

    return minNumberPosition                                              #se devuelve la posicion en la que esta el menor numero encontrado. Si hay varios se da prioridad al de + a la izquierda

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
    for number in restrictionsMatrix[0]:
        if number < 0:
            return False
        
        else:
            return True

def getAugmentedSolutionSimplex():
    global augmentedSolution

    i = 0

    #primero se llena de ceros la solucion aumentada por facilidad
    while i <= contVariables - 1:
        augmentedSolution.append(0)
        i += 1

    #Luego simplemente por cada variable basica se agrega a la solucion aumentada su valor correspondiente en el LD **A prueba, se necesitan varias iteraciones para comprobar
    for variable in bV:
        augmentedSolution[(int(str(variable)[1]) - 1)] = rightSide[int(str(variable)[1]) - numberOfDecisionVariables]



"""
Function: createTabularForm
Input: -
Output: -
Description: Function that takes the restrictions with the slack variables and converts them in to tabular form
"""
def createTabularForm():

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

        contVariablesLeft = contVariables - len(restrictionsMatrix[i])

        while contVariablesLeft != 0:

            restrictionsMatrix[i].append(0)
            contVariablesLeft -= 1

        i += 1

    i = 1
    while i <= len(restrictionsMatrix) - 1:

        restrictionsMatrix[i][nextOnePosition] = 1
        nextOnePosition += 1
        i += 1

"""
Function:
Input:
Output:
Description: 
"""
#def bigMMethod():



"""
Function:
Input:
Output:
Description: 
"""
#def TwoPhaseMethod():



"""
Function:
Input:
Output:
Description: 
"""
def addIterationToFinalSolution(f,optimal,iterationNumber):
    spaceBetweenX = 5
    spaceForEachX = 6
    f.write("Status: " + str(iterationNumber) + "\n\n")
    f.write("BV |   ")
    
    for number in intTotalVariables:
        if number == intTotalVariables[len(intTotalVariables) - 1]:
            f.write("x"+str(number))
        else:
            f.write("x"+str(number)+"         ")

    f.write("       | RS\n") 

    f.write("---|")
    f.write( (11* (contVariables)) * "-")
    f.write("-|----\n")


    contBvLeft = len(bV) - 1
    j = 0

    while j <= len(restrictionsMatrix) - 1:

        if j == 0:
            f.write("U  |   ")

        elif j != 0 and j-1 <= contBvLeft:
            f.write(bV[j-1] + " |   ")

        i = 0
        while i <= len(restrictionsMatrix[j]) - 1:
            
            if i == len(restrictionsMatrix[j]) - 1:
                f.write(str(restrictionsMatrix[j][i]))
                i += 1

            else:
                f.write(str(restrictionsMatrix[j][i]))
                spaceNeeded = spaceBetweenX + (spaceForEachX - len(str(restrictionsMatrix[j][i])))

                while spaceNeeded != 0: 
                    f.write(" ")
                    spaceNeeded -=1

                i += 1
        
        finalSpace = spaceForEachX - len(str(restrictionsMatrix[j][len(restrictionsMatrix[j])-1])) + 3
        #print(finalSpace)
        f.write((finalSpace * " ") + "| " + str(rightSide[j]))
        
        
        #linea divisoria de abajo
        f.write("\n---|")
        f.write( (11* (contVariables)) * "-")
        f.write("-|----\n")
    
        j += 1


    if iterationNumber == 0:
        f.write("\nAugmented Initial Solution:\n")
    
    elif iterationNumber > 0:
        f.write("\nAugmented Solution:\n")

    f.write("(")
        
    zeroVariables = numberOfDecisionVariables
    while zeroVariables != 0:
        f.write(" 0" + ",")
        zeroVariables -= 1
        
    posNextSolutionValue = numberOfDecisionVariables - 1
    while posNextSolutionValue <= len(rightSide) - 1:
        if posNextSolutionValue ==  len(rightSide) - 1:
            f.write(" "+ str(rightSide[posNextSolutionValue]) + " )")
            posNextSolutionValue += 1
            
        else:
            f.write(" "+ str(rightSide[posNextSolutionValue]) + ",")
            posNextSolutionValue += 1

    f.write("          U = " + str(rightSide[0]))

    if(optimal == False):
        f.write("\nNot Optimal Result")
        
    elif(optimal == True):
        f.write("\nOptimal Result")

    f.write("\nBasic Variables = ")
    for variable in bV:
        f.write(str(variable) + "  ")
        
    f.write("\nNon Basic Variables = ")
    for variable in nBV:
        f.write(str(variable) + "  ")


    f.write("\n")

    #f.close()                                         #Si se le hace close no se puede escribir mas sobre el archivo en otras iteraciones



def main():
    validateInputFile()                                            
    extractInformationFromRestrictions()       
    checkNegativesOnRightSide() 
    selectMethod()                                            
    #solutionFile()                           
    #print(restrictionsMatrix)
    #print(rightSide)
    #print(intTotalVariables)
    #print(restrictionsInequalities)
    #print(bV)
    #print(nBV)
    #print(intBvariables)
    #print(intTotalVariables)
    #print(contVariables)    

main()
#It is assumed that the order of the x's will always come in order in the restrictions