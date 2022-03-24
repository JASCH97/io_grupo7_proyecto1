from readAndSaveTxtInformation import *
from validationsBeforeMethodSelection import *
from simplexMethod import *

validateInputFile()
extractInformationFromRestrictions()     # se lee el documento y se extraen en listas toda la informacion necesaria

if selectedMethod[0] == 0 and verifyInequalities() == "simplex":                              #Se valida que se pueda simplex
    
    augmentedForm(0)
    defineStarterBasicAndNoBasicVariables(0)
    createSimplexTabularForm()
    simplexMethod()

#NOTA IMPORTANTE: Declarar varaibles e igualarlas a alguna otra no funciona de manera global, con append si!!