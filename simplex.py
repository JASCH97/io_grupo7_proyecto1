from readAndSaveTxtInformation import *
from validationsBeforeMethodSelection import *
from simplexMethod import *
from greatM import *

validateInputFile()
extractInformationFromRestrictions()     # reads file and extracts information in lists

if selectedMethod[0] == 0 and verifyInequalities() == "simplex":     # validates if simplex method can be used
    
    augmentedForm()
    defineStarterBasicAndNoBasicVariables()
    createSimplexTabularForm()
    simplexMethod()

elif selectedMethod[0] == 1 and verifyInequalities() == "no simplex":
    
    augmentedForm()
    defineStarterBasicAndNoBasicVariables()
    createGreatMTabularForm()
    simplexMethod()

# IMPORTANT: declaring variables and matching them to another doesn't work globally, only with append