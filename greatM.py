from validationsBeforeMethodSelection import *
from utilityFunctions import *
from readAndSaveTxtInformation import *

"""
Function: appropriateForm
Input: -
Output: -
Description: Function that turns the appropriate form of the row (0) / objective function
"""
def appropriateForm():
    objectiveFunction = restrictionsMatrix[0]
    artCounter = len(artificialVariables) - 1
    i = numberOfDecisionVariables[0]
    for var in strTotalVariables:
        if artificialVariables[artCounter][1] == var[1]:
            if optimization[0] == 'max':
                objectiveFunction.insert(i, 0+1j)
            else:
                objectiveFunction.insert(i, 0-1j)
            artCounter -= 1
        elif int(var[1]) > i:
            objectiveFunction.insert(i, 0.0)
            i += 1
    print(objectiveFunction)
    # se debe hacer la resta con el renglón que tiene la variable artificial.
