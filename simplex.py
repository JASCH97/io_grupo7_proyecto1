from readAndSaveTxtInformation import *
from validationsBeforeMethodSelection import *
from simplexMethod import *
from greatM import *
from twoPhases import *

validateInputFile()
extractInformationFromRestrictions()     # reads file and extracts information in lists

if selectedMethod[0] == 0 and verifyInequalities() == "simplex":     # validates if simplex method can be used
    f[0].write("Using Simplex Method...\n")
    augmentedForm()
    defineStarterBasicAndNoBasicVariables()
    createSimplexTabularForm()
    simplexMethod(False)

elif selectedMethod[0] == 1 and verifyInequalities() == "no simplex":
    f[0].write("Using Big M Method...\n")
    augmentedForm()
    defineStarterBasicAndNoBasicVariables()
    createTabularForm()
    appropriateFormGreatM()
    simplexMethod(False)

elif selectedMethod[0] == 2 and verifyInequalities() == "no simplex":
    f[0].write("Using Two-Phase Method...\nFirst phase\n")
    augmentedForm()
    defineStarterBasicAndNoBasicVariables()
    createTabularForm()
    saveFirstObjectiveFunction()                        
    appropriateFormTwoPhases()
    simplexMethod(True)                                 
    print(restrictionsMatrix)
    print(nBV)
    print(bV)
    print(rightSide)
    print(strTotalVariables)
    print(intTotalVariables)
    #simplexMethod(False)                                #se itera hasta obtener resultado optimo o no

#crear los otros casos, ejemplo -> si pone que se resuelva con simplex pero las restricciones tienen signos >= o =


# IMPORTANT: declaring variables and matching them to another doesn't work globally, only with append