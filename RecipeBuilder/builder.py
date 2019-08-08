'''
Author FredHappyface
Date 2019/07/22

builder.py read config.json defining recipes and generates recipe files 
'''
import os, sys, inspect
# Add ../lib to the import path 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))) + "/lib")

import fileIO

# Read generateMethods.json
def readConfig():
    data = fileIO.readJSON("config.json")
    author = data["author"]
    namespace = data["namespace"]
    name_from_ingredient = data["name-from-ingredient"]
    recipes = data["recipes"]
    implementations = data["implementations"]
    return author, namespace, name_from_ingredient, recipes, implementations

    
AUTHOR, NAMESPACE, NAME_FROM_INGREDIENT, RECIPES, IMPLEMENTATIONS = readConfig()
'''
Get a recipe from a string (eg for rec0 get rec0)
'''
def getRecipe(comparison):
    for recipe in RECIPES:
        if (recipe["id"] == comparison):
            return recipe

'''
Get the recipe type from a recipe in string form 
'''
def getRecipeType(recipe):
    try:
        recipe["pattern"]
        return "pattern"
    except:
        try:
            recipe["shapeless"]
            return "shapeless"
        except:
            print("undefined recipe type")

    return ""
    

'''
Assemble a recipe from recipeType, outRecipe, outResult, outIngredients, 
outGroup, outCount and produce a JSON file in the form result_from_ingredient
'''
def assembleRecipe(recipeType, outRecipe, outResult, outIngredients, outGroup, outCount):
    craftingRecipe = fileIO.fileToString("res/" + recipeType + ".json")

    craftingRecipe = craftingRecipe.replace("outRecipe", str(outRecipe[recipeType]).replace("\'", "\""), 1)
    craftingRecipe = craftingRecipe.replace("outResult", "\"" + outResult + "\"", 1)
    craftingRecipe = craftingRecipe.replace("outGroup", "\"" + outGroup + "\"", 1)
    craftingRecipe = craftingRecipe.replace("outCount", str(outCount), 1)

    ingredientsJson = ""
    pointer = 65
    for index in outIngredients:
        if (recipeType == "pattern"):
            ingredientsJson += "\"" + chr(pointer) + "\": { \"item\": \""+ index + "\" }, "
        if (recipeType == "shapeless"):
            ingredientsJson += "{ \"item\": \""+ index + "\" }, "
        pointer += 1
    ingredientsJson = ingredientsJson[:-2]

    craftingRecipe = craftingRecipe.replace("outIngredients", ingredientsJson, 1)

    fileIO.stringToFile("out/" + stripNamespace(outResult) + "_from_" + stripNamespace(outIngredients[NAME_FROM_INGREDIENT]) + ".json",craftingRecipe)



'''
Main function: loop through implementations and write a JSON file for each 
recipe 
'''
def getAllImplementations():
    for implementation in IMPLEMENTATIONS:
        outRecipe = getRecipe(implementation["usesid"])
        # Build a crafting recipe for each set of ingredients 
        listOfIngredients = implementation["ingredients"]
        for ingredients in listOfIngredients:
            outIngredients = []
            outResult = ""
            pointer = 65
            outGroup = outRecipe["group"]
            outCount = outRecipe["count"]
            # Not Supported Function - will require additional modification 
            if isinstance(ingredients, str):
                outIngredients.append(getNamespacedIngredient(ingredients))
                outResult = getNamespacedIngredient(ingredients)
            # Supported Function 
            else:
                '''
                Get predefined ingredients 

                Limitation can only have a predef ingredient occur once in shapeless
                '''
                lenPredefIngredients = len(outRecipe["predef_ingredients"])
                for index in range(lenPredefIngredients):
                    
                    outIngredients.append(outRecipe["predef_ingredients"][index][chr(pointer)])
                    pointer += 1

                # Get implementation ingredients 
                outRecipeType = getRecipeType(outRecipe)
                if outRecipeType == "pattern":
                    outIngredients.extend(ingredients[1])
                if outRecipeType == "shapeless":
                    '''
                    Assumptions: predef ingredients should refer starting at A 
                    and shapeless ingredients should be in ascending order eg. 
                    ["A", "B", "B", "C"]
                    '''
                    for item in range(len(outRecipe["shapeless"])):
                        # Convert each letter to a number and subtract the pointer
                        ingredientIndex = ord(outRecipe["shapeless"][item]) - pointer
                        if (ingredientIndex > -1):
                            outIngredients.append(ingredients[1][ingredientIndex])
                print (outIngredients)
                # Get output
                outResult = ingredients[0]

            assembleRecipe(outRecipeType,outRecipe, outResult, outIngredients, getNamespacedIngredient(outGroup), outCount)

         

'''
Get the namespaced ingredient if not already specified 
'''
def getNamespacedIngredient(ingredient):
    if ingredient.count(":") > 0:
        return ingredient
    else:
        return NAMESPACE + ":" + ingredient

'''
Strip the namespace from the ingredient name 
'''
def stripNamespace(ingredient):
    return ingredient.split(":")[1]


getAllImplementations()
