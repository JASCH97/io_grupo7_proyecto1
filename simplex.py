import sys

#global variables
firstLine = []
secondLine = []
numberOfDecisionVariables = 0
numberOfRestrictions = 0
stringRestrictions = []
restrictionsMatrix = []
restrictionsInequalities = []
bV = []
nBV = []
strTotalVariables = ""
intTotalVariables = 0
slackVariables = []
#GL = 0                                 
#augmentedSolution = []
#optimal = False
rightSide = []

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
    if len(sys.argv) == 2 and sys.argv[1] == "-h":       #it only wants to read the help message, the file is not given as a parameter
        print(helpMessage)
        exit()

    elif len(sys.argv) == 3 and sys.argv[1] == "-h":     #the file was entered as a parameter and it requires the help message
        print(helpMessage)
        saveInformationFromFile(sys.argv[2])

    elif len(sys.argv) == 2 and sys.argv[1] != "-h":     #the file was entered as a parameter and does NOT require the help message
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
 
            else:
                newRestictionForm[i] = float(newRestictionForm[i])
                i+=1

        stringRestrictions.pop(0)
        restrictionsMatrix.append(newRestictionForm)


"""
Function: insertObjectiveFunction
Input: -
Output: -
Description: Function that inserts the objective function in the first place of the restrictions matrix
"""
def insertObjectiveFunction():
    global restrictionsMatrix
    global secondLine

    i = 0
    objectiveFunction = []
    newObjectiveFunctionForm = secondLine.split(sep=',')

    while i <= len(newObjectiveFunctionForm) - 1:
        objectiveFunction.append(float(newObjectiveFunctionForm[i]) * -1)
        i+=1
    
    objectiveFunction.append(0)
    restrictionsMatrix.append(objectiveFunction)


"""
Function: augmentedForm
Input: -
Output: -
Description: Function that takes the restrictions matrix and passes it to its augmented form 
             (adding the slack variables)
"""
def augmentedForm():
    global restrictionsMatrix
    global slackVariables
    contSlackAdded = numberOfDecisionVariables                              #Slack variables are created using the number of decision variables
    i = 1

    while i <= len(restrictionsMatrix) - 1:
        restrictionsMatrix[i].insert(len(restrictionsMatrix[i]) -1,1)
        i +=1
        contSlackAdded += 1
        slackVariables.append("x" + str(contSlackAdded))


"""
Function: defineBasicAndNoBasicVariables
Input: -
Output: -
Description: Function that defines which are the basic and non-basic variables at the beginning of the problem 
"""
def defineStarterBasicAndNoBasicVariables():
    global bV
    global nBV
    global strTotalVariables
    global intTotalVariables

    bV = slackVariables
    i = 1
    
    while i <= numberOfDecisionVariables:
        nBV.append("x" + str(i))
        i+=1 
    
    for variable in nBV:
        strTotalVariables = strTotalVariables + "    " + variable
        intTotalVariables = intTotalVariables + 1

    for variable in bV:
        strTotalVariables = strTotalVariables + "    " + variable
        intTotalVariables = intTotalVariables + 1


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
        simplexMethod(firstLine[2:5])

    #elif firstLine[0] == "0" and verifyInequalities() == "no simplex":                         #El usuario pide simplex pero hay un >= o un =, se procede a gran M
        #gran M
    
    #elif firstLine[0] == "1" and verifyInequalities() == "simplex":                            #El usuario pide gran M pero todas las restricciones son <=, se hace simplex
        #simplexMethod(firstLine[2:5])

    #elif firstLine[0] == "1" and verifyInequalities() == "no simplex":
        #gran M

    #agregar los casos de dos fases


"""
Function: simplexMethod
Input:
Output:
Description: Function that solves a problem using the simplex method
"""
def simplexMethod(optimization):
    if optimization == "max":
        print("max optimization")
        createTabularForm()


"""
Function: createTabularForm
Input: -
Output: -
Description: Function that takes the restrictions with the slack variables and converts them in to tabular form
"""
def createTabularForm():

    global rightSide
    global restrictionsMatrix

    for restriction in restrictionsMatrix:
        rightSide.append(restriction[len(restriction) - 1])
        restriction.remove(restriction[len(restriction) - 1])

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

        contVariablesLeft = intTotalVariables - len(restrictionsMatrix[i])

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
#def solutionFile():
    #f = open("output.txt","w")
    #f.write("VB | " + totalVariables + " | LD")
    #f.close()



def main():
    validateInputFile()                         
    insertObjectiveFunction()                    
    extractInformationFromRestrictions()        
    checkNegativesOnRightSide()                 
    augmentedForm()                             
    defineStarterBasicAndNoBasicVariables()      
    selectMethod()                              
    print(restrictionsMatrix)
    print(restrictionsInequalities)
    print(bV)
    print(nBV)
    print(intTotalVariables)    

main()
#It is assumed that the order of the x's will always come in order in the restrictions


