import sys

fileName = []
fileOut = []
firstLine = []
secondLine = []
stringRestrictions = []
optimization = []
selectedMethod = []
numberOfDecisionVariables = []
numberOfRestrictions = []
objectiveFunction = []
restrictionsMatrix = []
restrictionsInequalities = []

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
    global fileOut

    if len(sys.argv) == 2 and sys.argv[1] == "-h":       #it only wants to read the help message, the file is not given as a parameter
        print(helpMessage)
        exit()

    elif len(sys.argv) == 3 and sys.argv[1] == "-h":     #the file was entered as a parameter and it requires the help message
        print(helpMessage)
        inputFileName = sys.argv[2]
        fileName.append(inputFileName[0:len(inputFileName) - 4])
        fileOut.append(open("./Solutions/" + fileName[0] + "_solution" + ".txt","w"))
        saveInformationFromFile("./Problems/"+sys.argv[2])

    elif len(sys.argv) == 2 and sys.argv[1] != "-h":     #the file was entered as a parameter and does NOT require the help message
        inputFileName = sys.argv[1]
        fileName.append(inputFileName[0:len(inputFileName) - 4]) 
        fileOut.append(open("./Solutions/" + fileName[0] + "_solution" + ".txt","w"))     
        saveInformationFromFile("./Problems/"+sys.argv[1])

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
    global selectedMethod

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
        separatedLine = firstLine.split(",")
        numberOfDecisionVariables.append(int(separatedLine[2]))
        numberOfRestrictions.append(int(separatedLine[3]))
        selectedMethod.append(int(separatedLine[0]))
        optimization.append(separatedLine[1])

        while i <= len(lines) -1:
            stringRestrictions = stringRestrictions + [information[i]]
            i+=1
        
        i = 0
        newObjectiveFunctionForm = secondLine.split(sep=',')

        while i <= len(newObjectiveFunctionForm) - 1:
            objectiveFunction.append(round(float(newObjectiveFunctionForm[i]) * -1 , 5))
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

            newRestictionForm[i] = round(float(newRestictionForm[i]) , 5)
            i+=1
    

        stringRestrictions.pop(0)
        restrictionsMatrix.append(newRestictionForm)
