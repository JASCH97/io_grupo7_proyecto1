from readAndSaveTxtInformation import *
from validationsBeforeMethodSelection import *
from simplexMethod import *
from greatM import *

validateInputFile()
extractInformationFromRestrictions()     # se lee el documento y se extraen en listas toda la informacion necesaria

if selectedMethod[0] == 0 and verifyInequalities() == "simplex":                              #Se valida que se pueda simplex
    augmentedForm()
    defineStarterBasicAndNoBasicVariables()
    createSimplexTabularForm()
    #simplexMethod()

elif selectedMethod[0] == 1 or verifyInequalities() == "no simplex": ## nose que es selectedMethod, ask Joan
    augmentedForm() # para gran M
    defineStarterBasicAndNoBasicVariables()
    appropriateForm()
    #createGreatMTabularForm()
    #modifyRestrictionsForTabularForm()
#NOTA IMPORTANTE: Declarar varaibles e igualarlas a alguna otra no funciona de manera global, con append si!!