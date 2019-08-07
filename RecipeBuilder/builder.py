'''
Author FredHappyface
Date 2019/07/22

builder.py read config.json defining recipes and generates recipe files 
'''

import os

# Read json file
def readJSON(file_name):
    import json
    with open(file_name) as json_file:
        return json.load(json_file)


# Read generateMethods.json
def readConfig():
    data = readJSON("config.json")
    author = data["author"]
    namespace = data["namespace"]
    name_from_ingredient = data["name-from-ingredient"]
    recipes = data["recipes"]
    implementations = data["implementations"]
    return author, namespace, name_from_ingredient, recipes, implementations


'''
Write a string to a file defined with a (relative) path
'''
def stringToFile(filepath, string):

    import re
    tok = re.split(' |/|\\\\',filepath)

    checkfile = ''
    for x in tok[:-1]:
        checkfile += x + '\\'
    os.makedirs(checkfile, exist_ok=True)
    file = open(filepath, "w+")
    file.write(string)
    file.close()
    return

'''
Return the contents of a file as a string using a (relative) filepath
'''
def fileToTokens(filepath):
    tokens = []
    file = open(filepath, "r")
    for line in file:
        tokens.append(line)
    return tokens

'''
For convenience, not particularly efficient in it's implementation but it's 
good enough for this application 
'''
def fileToString(filepath):
    outstr = ""
    tokens = fileToTokens(filepath)
    for line in tokens:
        outstr += line
    return outstr


'''
Gets a list of subfiles - useful for bulk copying 
'''
def getListOfFiles(dirName, childOnly):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            if not childOnly:
                allFiles = allFiles + getListOfFiles(fullPath, childOnly)
        else:
            allFiles.append(fullPath)
                
    return allFiles



    
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
    craftingRecipe = fileToString("res/" + recipeType + ".json")

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

    stringToFile("out/" + stripNamespace(outResult) + "_from_" + stripNamespace(outIngredients[NAME_FROM_INGREDIENT]) + ".json",craftingRecipe)



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
            pointer = 64
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
                    pointer += 1
                    outIngredients.append(outRecipe["predef_ingredients"][index][chr(pointer)])

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
                    for item in range(lenPredefIngredients, len(outRecipe["shapeless"])):
                        # Convert each letter to a number and subtract the pointer
                        #print(ord(outRecipe["shapeless"][index]) - pointer)
                        outIngredients.append(ingredients[1][ord(outRecipe["shapeless"][index]) - pointer])
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
