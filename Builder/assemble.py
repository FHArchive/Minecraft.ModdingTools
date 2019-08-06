'''
Author FredHappyface
Date 2019/07/22

assemble.py read settings files as in /config and outputs blocks/ resources
and items with those properties. Can be used to generate boilerplate code and 
data files for your mod
'''

import os

# Read json file
def readJSON(file_name):
    import json
    with open(file_name) as json_file:
        return json.load(json_file)


# Read generateMethods.json
def readGenerateMethods():
    data = readJSON("config/generateMethods.json")
    lib = data["generate-java-lib"]
    registers = data["generate-java-registers"]
    main = data["generate-java-main-files"]
    return lib, registers, main

# Read general.json
def readGeneral():
    data = readJSON("config/general.json")
    author = data["author"]
    mod_name = data["mod-name"]
    input_file = data["input-file"]
    output_file = data["output-file"]
    return author, mod_name, input_file, output_file

# Read blocksAndItems.json
def readBlocksAndItems():
    data = readJSON("config/blocksAndItems.json")
    '''
    eg. resources = [ [[res1, res2, res3], [ore, block, bricks, tools]],
    [[res4], [ore, tools]]]
    '''
    resources = data["resources"]
    blocks = data["blocks"]
    items = data["items"]
    return resources, blocks, items 


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
    import os 
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



    
SETTING_LIB, SETTING_REG, SETTING_MAIN = readGenerateMethods()
DATA_AUTHOR, DATA_MODNAME, DATA_INPUT_FILE, DATA_OUTPUT_FILE = readGeneral()
RESOURCES, BLOCKS, ITEMS = readBlocksAndItems()



# Generate Methods
print(SETTING_REG)

LIB_FILES, REG_FILES, MAIN_FILES = list(), list(), list()
if (SETTING_LIB == "True"):
    LIB_FILES = getListOfFiles(DATA_INPUT_FILE + "/src/main/java/com/example/examplemod/lib", False)
if (SETTING_REG == "True"):
    REG_FILES = getListOfFiles(DATA_INPUT_FILE + "/src/main/java/com/example/examplemod/registers", False)
if (SETTING_MAIN == "True"):
    MAIN_FILES = getListOfFiles(DATA_INPUT_FILE + "/src/main/java/com/example/examplemod", True)

ALL_JAVA_FILES = LIB_FILES + REG_FILES + MAIN_FILES

for file in ALL_JAVA_FILES:
    print(file)
    fileContentsStr = fileToString(file)
    fileContentsStr = fileContentsStr.replace("com.example.examplemod","com."
                                              +DATA_AUTHOR+"."+DATA_MODNAME)
    stringToFile(file.replace("com/example/examplemod", "com/"+DATA_AUTHOR+"/"+
                              DATA_MODNAME, 1).replace(DATA_INPUT_FILE, DATA_OUTPUT_FILE),fileContentsStr)
    
    
# Generate Resources - Useful Constants 
ASSETS = DATA_INPUT_FILE + "/src/main/resources/assets/examplemod"
DATA = DATA_INPUT_FILE + "/src/main/resources/data"
META_INF = DATA_INPUT_FILE + "/src/main/resources/META-INF"

ASSETS_BLOCKSTATES = ASSETS + "/blockstates/" # decorations ore storage_block
ASSETS_LANG = ASSETS + "/lang/" # en_us 
ASSETS_MODELS = ASSETS + "/models/" # block(decorations ore storage_block) item([block] armour tools /)
ASSETS_TEXTURES = ASSETS + "/textures/" # block(decorations ore storage_block) item(armor tools /) models(armor)

DATA_MOD = DATA + "/examplemod/" # loot_tables(blocks(decorations ore storage_block))
#recipes(crafting(blocks(decorations /) items(armor tools /) smelting(blocks items(/) ))
DATA_FORGE = DATA + "/forge/tags/" # blocks(decorations ores storage_blocks) items([block] gems)
DATA_MINECRAFT = DATA + "/minecraft/"

LOOT_TABLES = DATA_MOD + "loot_tables/"
RECIPES = DATA_MOD + "recipes/"
RECIPES_CRAFTING = RECIPES + "crafting/"

'''
Generate a resource file using a copy under res
'''
def genResFile(file, name):
    print(file)
    fileContentsStr = fileToString(file.replace(name, "aquamarine", 1))
    fileContentsStr = fileContentsStr.replace("aquamarine",name).replace("anothergemsmod",DATA_MODNAME)

    stringToFile(file.replace("examplemod", DATA_MODNAME, 1).replace(DATA_INPUT_FILE, DATA_OUTPUT_FILE, 1),fileContentsStr)

'''
Currently unused simple utility method to generate multiple resource files in a 
directory
'''
def genResFiles(files, name):
    files = getListOfFiles(files, True)
    for file in files:
        genResFile(file, name)



'''
resType = (Resources, Blocks, Items)
resData = [{names: "", types: ""}]
genResNames(resType, resData)
'''
def genRes(resType, resData, alsoHasItem):
    
    # For each 'line'
    for resDataLine in resData:

        ''' Does the dataLine have specific combinations of types. If yes, add 
        additional crafting recipes. eg. if block and slabs exist add 
        name_block_from_slab recipe
        '''

        TYPES = resDataLine["types"]

        ADDITIONAL_RECIPE_BLOCK_F_SLAB = False
        ADDITIONAL_RECIPE_BRICKS_F_SLAB = False

        ADDITIONAL_RECIPE_BLOCK_F_BRICKS = False

        ADDITIONAL_RECIPE_SLAB_FT_BRICK_SLAB = False
        ADDITIONAL_RECIPE_STAIRS_FT_BRICK_STAIRS = False



        if ("block" in TYPES and "slab" in TYPES):
            ADDITIONAL_RECIPE_BLOCK_F_SLAB = True
        if ("bricks" in TYPES and "brick_slab" in TYPES):
            ADDITIONAL_RECIPE_BRICKS_F_SLAB = True

        if ("bricks" in TYPES and "block" in TYPES):
            ADDITIONAL_RECIPE_BLOCK_F_BRICKS = True

        if ("slab" in TYPES and "brick_slab" in TYPES):
            ADDITIONAL_RECIPE_SLAB_FT_BRICK_SLAB = True
        if ("stairs" in TYPES and "brick_stairs" in TYPES):
            ADDITIONAL_RECIPE_STAIRS_FT_BRICK_STAIRS = True


        # For each name
        for nameIndex in range(len(resDataLine["names"])):
            name = resDataLine["names"][nameIndex]
            '''
            If it is a resource, generate the gem/ ingot, for items gen item 
            with name
            '''
            if ((resType == "resources" or resType == "items")and alsoHasItem):
                print(name)
                file = ASSETS_MODELS + "item/" + name + ".json"
                genResFile(file, name)
                
            '''
            Add additional recipes 
            '''
            if (not alsoHasItem):
                if(ADDITIONAL_RECIPE_BLOCK_F_SLAB):
                    file = RECIPES_CRAFTING + "blocks/storage_blocks/" + name + "_block_from_slab.json"
                    genResFile(file, name)
                if(ADDITIONAL_RECIPE_BRICKS_F_SLAB):
                    file = RECIPES_CRAFTING + "blocks/decorations/" + name + "_bricks_from_slab.json"
                    genResFile(file, name)
                if(ADDITIONAL_RECIPE_BLOCK_F_BRICKS):
                    file = RECIPES_CRAFTING + "blocks/storage_blocks/" + name + "_block_from_bricks.json"
                    genResFile(file, name)
                if(ADDITIONAL_RECIPE_SLAB_FT_BRICK_SLAB):
                    file = RECIPES_CRAFTING + "blocks/decorations/" + name + "_slab_from_brick_slab.json"
                    genResFile(file, name)
                    file = RECIPES_CRAFTING + "blocks/decorations/" + name + "_brick_slab_from_slab.json"
                    genResFile(file, name)
                if(ADDITIONAL_RECIPE_STAIRS_FT_BRICK_STAIRS):
                    file = RECIPES_CRAFTING + "blocks/decorations/" + name + "_stairs_from_brick_stairs.json"
                    genResFile(file, name)
                    file = RECIPES_CRAFTING + "blocks/decorations/" + name + "_brick_stairs_from_stairs.json"
                    genResFile(file, name)

            

            # For every type 
            RTYPE_DECORATIONS = ["bricks", "slab", "stairs", "brick_slab", 
            "brick_stairs", "hopper", "bars", "door", "lamp", "lamp_inverted"]
            RTYPE_ITEMS = ["armor", "tools", "shears"]





            for rtype in resDataLine["types"]:
                # Get resource namespace (item/ block)
                resname = "block/"
                resnames = "blocks/"
                if (resType == "items"):
                    resname = "item/"
                    resnames = "items/"
                ltype = ""
                if (rtype == "ore"):
                    ltype = "ores/"
                if (rtype == "block"):
                    ltype = "storage_blocks/"
                if (rtype in RTYPE_DECORATIONS):
                    ltype = "decorations/"
                    
                if (rtype in RTYPE_ITEMS):
                    
                    resname = "item/"
                    resnames = "items/"
                if (rtype == "armor"):
                    ltype = "armor/"
                    rtype = "helm"
                if (rtype == "tools"):
                    ltype = "tools/"
                    rtype = "axe"
                if (rtype == "shears"):
                    ltype = "tools/"
                
                
                print(DATA_MODNAME + ":" + resname + ltype + name + "_" + rtype)


                if (alsoHasItem):

                    '''
                    Blocks Only: 
                    '''

                    # If block > blockstates
                    if (resname == "block/"):
                        file = ASSETS_BLOCKSTATES + ltype + name + "_" + rtype + ".json"
                        genResFile(file, name)
                        

                        # Stairs and slabs have more block decorations 
                        if (ltype == "decorations/"):
                            RTYPE_SLABS = ["slab", "brick_slab"]
                            RTYPE_STAIRS =  ["stairs", "brick_stairs"]
                            if (rtype in RTYPE_SLABS):
                                file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + "_top.json"
                                genResFile(file, name)
                            if (rtype in RTYPE_STAIRS):
                                file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + "_inner.json"
                                genResFile(file, name)
                                file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + "_outer.json"
                                genResFile(file, name)
                            if (rtype == "hopper"):
                                file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + "_side.json"
                                genResFile(file, name)
                            if (rtype == "lamp"):
                                file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + "_on.json"
                                genResFile(file, name)
                            if (rtype == "bars"):
                                file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + "_noside.json"
                                genResFile(file, name)
                                file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + "_noside_alt.json"
                                genResFile(file, name)
                                file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + "_post.json"
                                genResFile(file, name)
                                file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + "_side.json"
                                genResFile(file, name)
                                file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + "_side_alt.json"
                                genResFile(file, name)
                            if (rtype == "door"):
                                file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + "_bottom.json"
                                genResFile(file, name)
                                file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + "_bottom_hinge.json"
                                genResFile(file, name)
                                file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + "_top.json"
                                genResFile(file, name)
                                file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + "_top_hinge.json"
                                genResFile(file, name)
                               

                    '''
                    Items only 
                    '''
                    ASSETS_MODELS_ITEMS_ONLY = ["bars", "door", "lamp_inverted"]
                    if (resname == "item/"):
                        
                        
                        if (rtype in ASSETS_MODELS_ITEMS_ONLY):
                            file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + ".json"
                            genResFile(file, name)
                        

                        # Tools here
                        if (rtype == "axe"):
                            file = ASSETS_MODELS + resname + ltype + name + "_hoe.json"
                            genResFile(file, name)
                            file = ASSETS_MODELS + resname + ltype + name + "_pickaxe.json"
                            genResFile(file, name)
                            file = ASSETS_MODELS + resname + ltype + name + "_sword.json"
                            genResFile(file, name)
                            file = ASSETS_MODELS + resname + ltype + name + "_shovel.json"
                            genResFile(file, name)

                        # Armor here
                        if (rtype == "helm"):
                            file = ASSETS_MODELS + resname + ltype + name + "_chest.json"
                            genResFile(file, name)
                            file = ASSETS_MODELS + resname + ltype + name + "_leggings.json"
                            genResFile(file, name)
                            file = ASSETS_MODELS + resname + ltype + name + "_boots.json"
                            genResFile(file, name)


                        

                    '''
                    Everything apart from items only (as they do not have a block 
                    model eg. bars uses the item model for the block side )

                    exceptions bars door lamp_inverted (do not have a block )

                    '''
                                       
                    if (not rtype in ASSETS_MODELS_ITEMS_ONLY):
                        file = ASSETS_MODELS + resname + ltype + name + "_" + rtype + ".json"
                        genResFile(file, name)



                    '''
                    DATA FORGE 
                    '''
                    if (ltype == "decorations/"):
                        file = DATA_FORGE + resnames + ltype + name + "_" + rtype + ".json"
                        genResFile(file, name)
                    elif(not (ltype == "tools/" or ltype == "armor/")):
                        file = DATA_FORGE + resnames + ltype + name + ".json"
                        genResFile(file, name)
                    
                    


                   

                else:

                    '''
                    DATA CRAFTING RECIPES 
                    '''
                    # If not ore block
                    if (not (rtype == "ore")):
                        file = RECIPES_CRAFTING + resnames + ltype + name + "_" + rtype + ".json"
                        genResFile(file, name)


                    # Tools here
                    if (rtype == "axe"):
                        file = RECIPES_CRAFTING + resnames + ltype + name + "_hoe.json"
                        genResFile(file, name)
                        file = RECIPES_CRAFTING + resnames + ltype + name + "_pickaxe.json"
                        genResFile(file, name)
                        file = RECIPES_CRAFTING + resnames + ltype + name + "_sword.json"
                        genResFile(file, name)
                        file = RECIPES_CRAFTING + resnames + ltype + name + "_shovel.json"
                        genResFile(file, name)

                    # Armor here
                    if (rtype == "helm"):
                        file = RECIPES_CRAFTING + resnames + ltype + name + "_chest.json"
                        genResFile(file, name)
                        file = RECIPES_CRAFTING + resnames + ltype + name + "_leggings.json"
                        genResFile(file, name)
                        file = RECIPES_CRAFTING + resnames + ltype + name + "_boots.json"
                        genResFile(file, name)



                    '''
                    DATA LOOT TABLES
                    '''
                    # If block > blockstates
                    if (resname == "block/"):
                        file = LOOT_TABLES + resnames + ltype + name + "_" + rtype + ".json"
                        genResFile(file, name)

                    

                
'''
 Wrappers for each resource gen. Probably should move away from a monolithic 
 function but it works
 '''

def genDataRes(resType, resData):
    genRes(resType, resData, False)

def genAssetRes(resType, resData):
    genRes(resType, resData, True)


                    
# Generate data (loot tables and recipes )
genDataRes("resources", RESOURCES)
genDataRes("blocks", BLOCKS)
genDataRes("items", ITEMS)


'''
Generate models (models for blocks require an item too. eg. ore block needs 
an ore item)
'''
ITEMS.extend(RESOURCES)
ITEMS.extend(BLOCKS)

genAssetRes("resources", RESOURCES)
genAssetRes("blocks", BLOCKS)
genAssetRes("items", ITEMS)


