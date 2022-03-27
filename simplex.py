from readAndSaveTxtInformation import *
from validationsBeforeMethodSelection import *
from simplexMethod import *
from greatM import *

validateInputFile()
extractInformationFromRestrictions()     # se lee el documento y se extraen en listas toda la informacion necesaria

if selectedMethod[0] == 0 and verifyInequalities() == "simplex":                              #Se valida que se pueda simplex
    
    augmentedForm(0)
    defineStarterBasicAndNoBasicVariables(0)
    createSimplexTabularForm()
    simplexMethod()

elif selectedMethod[0] == 1 and verifyInequalities() == "no simplex":
    augmentedFormGreatM() # para gran M
    defineStarterBasicAndNoBasicVariables(1)
    createGreatMTabularForm()
    #simplexMethod()
#NOTA IMPORTANTE: Declarar varaibles e igualarlas a alguna otra no funciona de manera global, con append si!!