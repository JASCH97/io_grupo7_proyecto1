from readAndSaveTxtInformation import *

bV = []
nBV = []
slackVariables = []
intBvariables = []
intTotalVariables = []
contVariables = []
strTotalVariables = []

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
"""
def augmentedForm(method):
    global restrictionsMatrix
    global slackVariables
    global intBvariables
    
    #Only the slack variables are added
    if method == 0:                                                             #For simplex method
        contSlackAdded = numberOfDecisionVariables[0]                              #Slack variables are created using the number of decision variables
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
def defineStarterBasicAndNoBasicVariables(method):
    global bV
    global nBV
    global strTotalVariables
    global contVariables
    global intTotalVariables

    if method == 0:                                                 #si el metodo es simplex, se usan las variables de holgura para definir variables basicas
        for variable in slackVariables:
            bV.append(variable)

        i = 1
        
        while i <= numberOfDecisionVariables[0]:
            nBV.append("x" + str(i))
            i+=1 
        
        for variable in nBV:
            strTotalVariables.append(variable)
            #contVariables = contVariables + 1

        for variable in bV: 
            strTotalVariables.append(variable)
            #contVariables = contVariables + 1

        contVariables.append(len(strTotalVariables))

        j = 1
        while j <= contVariables[0]:
            intTotalVariables.append(j)
            j += 1

    
    #elif method == 1:                                                  #si el metodo es gran M...


    #else:                                                              #si el metodo es dos fases...


"""
Function: selectMethod
Input: -
Output: -
Description: Function that selects which method to use to solve the problem
"""
"""
#Funcion que selecciona el método mediante el cual se va a resolver el problema
def selectMethod():
    if selectedMethod[0] == 0 and verifyInequalities() == "simplex":                              #Se valida que se pueda simplex
        augmentedForm(0)
        defineStarterBasicAndNoBasicVariables(0)
        simplexMethod()




    #elif firstLine[0] == "0" and verifyInequalities() == "no simplex":                         #El usuario pide simplex pero hay un >= o un =, se procede a gran M
        #gran M
    
    #elif firstLine[0] == "1" and verifyInequalities() == "simplex":                            #El usuario pide gran M pero todas las restricciones son <=, se hace simplex
        #simplexMethod(firstLine[2:5])

    #elif firstLine[0] == "1" and verifyInequalities() == "no simplex":
        #gran M

    #agregar los casos de dos fases  """