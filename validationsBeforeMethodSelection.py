from readAndSaveTxtInformation import *

bV = []
nBV = []
slackVariables = []
intBvariables = []
intTotalVariables = []
contVariables = []
strTotalVariables = []
artificialVariables = []

"""
Function: verifyInequalities
Input: -
Output: -
Description: Function that checks the list of inequalities to know which method should be used
"""
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
"""
def augmentedForm():
    global restrictionsMatrix
    global slackVariables
    global intBvariables
    global artificialVariables

    i = 1
    contSlackAdded = numberOfDecisionVariables[0]               # slack variables are created using the number of decision variables
    while i <= len(restrictionsMatrix) - 1:
        if selectedMethod[0] == 0:
            restrictionsMatrix[i].insert(len(restrictionsMatrix[i]) -1,1)
        if restrictionsInequalities[i - 1] == '<=':
            i += 1
            contSlackAdded += 1
            slackVariables.append("x" + str(contSlackAdded))
        elif restrictionsInequalities[i - 1] == '=':
            i += 1
            contSlackAdded += 1
            slackVariables.append("a" + str(contSlackAdded))
            artificialVariables.append("a" + str(contSlackAdded))
        elif restrictionsInequalities[i - 1] == '>=':
            i += 1
            contSlackAdded += 1
            slackVariables.append("s" + str(contSlackAdded))
            intBvariables.append(contSlackAdded)
            contSlackAdded += 1
            slackVariables.append("a" + str(contSlackAdded))
            artificialVariables.append("a" + str(contSlackAdded))
        intBvariables.append(contSlackAdded)


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

    # slack variables are used to define basic variables
    for variable in slackVariables:
        bV.append(variable)

    i = 1
    while i <= numberOfDecisionVariables[0]:
        nBV.append("x" + str(i))
        i+=1     

    for variable in nBV:
        strTotalVariables.append(variable)

    for variable in bV[:]:
        if variable[0] == 's':      # artificial variables take priority over slack variable so remove them from bV
            bV.remove(variable)
            nBV.append(variable)
        strTotalVariables.append(variable)
    
    contVariables.append(len(strTotalVariables))
    
    j = 1
    while j <= contVariables[0]:
        intTotalVariables.append(j)
        j += 1
