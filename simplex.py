from readAndSaveTxtInformation import *
from validationsBeforeMethodSelection import *
from simplexMethod import *
from greatM import *
from twoPhases import *

validateInputFile()
extractInformationFromRestrictions()  

def selectSimplex():
    f[0].write("Using Simplex Method...\n")
    augmentedForm()
    defineStarterBasicAndNoBasicVariables()
    createSimplexTabularForm()
    simplexMethod(False)

def selectGreatM():
    f[0].write("Using Big M Method...\n")
    augmentedForm()
    defineStarterBasicAndNoBasicVariables()
    createTabularForm()
    appropriateFormGreatM()
    simplexMethod(False)

def selectTwoPhases():
    f[0].write("Using Two-Phase Method...\nFirst phase\n")
    augmentedForm()
    defineStarterBasicAndNoBasicVariables()
    createTabularForm()
    saveFirstObjectiveFunction()
    appropriateFormTwoPhases()
    simplexMethod(True)
    #simplexMethod(False)       
                         

if selectedMethod[0] == 0 and verifyInequalities() == "simplex":     # validates if simplex method can be used
    selectSimplex()

elif selectedMethod[0] == 0 and verifyInequalities() == "nosimplex":     # validates if simplex method can be used
    selectGreatM()

elif selectedMethod[0] == 1 and verifyInequalities() == "no simplex":
    selectGreatM()

elif selectedMethod[0] == 2 and verifyInequalities() == "no simplex":
    selectTwoPhases()

elif (selectedMethod[0] == 1 or selectedMethod[0] == 2) and verifyInequalities() == "simplex":
    selectSimplex()