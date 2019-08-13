'''
Author FredHappyface
Date 2019/07/22

assemble.py read settings files as in /config and outputs blocks/ resources
and items with those properties. Can be used to generate boilerplate code and 
data files for your mod
'''

import os, sys, inspect
# Add ../lib to the import path 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))) + "/lib")

import fileIO

CONFIG_M = "config/generateMethods.json"
CONFIG_G = "config/general.json"
CONFIG_B = "config/blocksAndItems.json"

# Read generateMethods.json
def readGenerateMethods():
    data = fileIO.readJSON(CONFIG_M)
    lib = data["generate-java-lib"]
    registers = data["generate-java-registers"]
    main = data["generate-java-main-files"]
    return lib, registers, main

# Read general.json
def readGeneral():
    data = fileIO.readJSON(CONFIG_G)
    author = data["author"]
    mod_name = data["mod-name"]
    input_file = data["input-file"]
    output_file = data["output-file"]
    return author, mod_name, input_file, output_file

# Read blocksAndItems.json
def readBlocksAndItems():
    data = fileIO.readJSON(CONFIG_B)
    '''
    eg. resources = [ [[res1, res2, res3], [ore, block, bricks, tools]],
    [[res4], [ore, tools]]]
    '''
    resources = data["resources"]
    blocks = data["blocks"]
    items = data["items"]
    return resources, blocks, items 




# Generate Methods
def genMethods():
    print(SETTING_REG)

    LIB_FILES, REG_FILES, MAIN_FILES = list(), list(), list()
    if (SETTING_LIB == "True"):
        LIB_FILES = fileIO.getListOfFiles(DATA_INPUT_FILE + "/src/main/java/com/example/examplemod/lib", False)

    if (SETTING_REG == "True"):
        REG_FILES = fileIO.getListOfFiles(DATA_INPUT_FILE + "/src/main/java/com/example/examplemod/registers", False)
    if (SETTING_MAIN == "True"):
        MAIN_FILES = fileIO.getListOfFiles(DATA_INPUT_FILE + "/src/main/java/com/example/examplemod", True)

    ALL_JAVA_FILES = LIB_FILES + REG_FILES + MAIN_FILES

    for file in ALL_JAVA_FILES:
        print(file)
        fileContentsStr = fileIO.fileToString(file)
        fileContentsStr = fileContentsStr.replace("com.example.examplemod","com."
                                                +DATA_AUTHOR+"."+DATA_MODNAME)
        fileIO.stringToFile(file.replace("com/example/examplemod", "com/"+DATA_AUTHOR+"/"+
                                DATA_MODNAME, 1).replace(DATA_INPUT_FILE, DATA_OUTPUT_FILE),fileContentsStr)
        


'''
Generate a resource file using a copy under res
'''
def genResFile(file, name):
    print(file)
    fileContentsStr = fileIO.fileToString(file.replace(name, "aquamarine", 1))
    fileContentsStr = fileContentsStr.replace("aquamarine",name).replace("anothergemsmod",DATA_MODNAME)

    fileIO.stringToFile(file.replace("examplemod", DATA_MODNAME, 1).replace(DATA_INPUT_FILE, DATA_OUTPUT_FILE, 1),fileContentsStr)

'''
Currently unused simple utility method to generate multiple resource files in a 
directory
'''
def genResFiles(files, name):
    files = fileIO.getListOfFiles(files, False)
    for file in files:
        genResFile(file.replace("aquamarine", name, 1), name)


'''
Set flags for additional crafting combinations and write them to a dictionary 
to improve readability - using a list would make this harder to read
'''
def setCraftingCombinationsFlags(TYPES):

    flags = {"block_f_slab" : False,
    "bricks_f_slab": False,
    "block_f_bricks" : False,
    "slab_ft_brick_slab" : False,
    "stairs_ft_brick_stairs": False}


    if ("block" in TYPES and "slab" in TYPES):
        flags["block_f_slab"] = True
    if ("bricks" in TYPES and "brick_slab" in TYPES):
        flags["bricks_f_slab"] = True

    if ("bricks" in TYPES and "block" in TYPES):
        flags["block_f_bricks"] = True

    if ("slab" in TYPES and "brick_slab" in TYPES):
        flags["slab_ft_brick_slab"] = True
    if ("stairs" in TYPES and "brick_stairs" in TYPES):
        flags["stairs_ft_brick_stairs"] = True

    return flags

'''
Use the flags and the name of the item to add crafting combinations for it 
'''
def addCraftingCombinations(flags, name):
    if(flags["block_f_slab"]):
        file = RECIPES_CRAFTING + "blocks/storage_blocks/" + name + "_block_from_slab.json"
        genResFile(file, name)
    if(flags["bricks_f_slab"]):
        file = RECIPES_CRAFTING + "blocks/decorations/" + name + "_bricks_from_slab.json"
        genResFile(file, name)
    if(flags["block_f_bricks"]):
        file = RECIPES_CRAFTING + "blocks/storage_blocks/" + name + "_block_from_bricks.json"
        genResFile(file, name)
    if(flags["slab_ft_brick_slab"]):
        file = RECIPES_CRAFTING + "blocks/decorations/" + name + "_slab_from_brick_slab.json"
        genResFile(file, name)
        file = RECIPES_CRAFTING + "blocks/decorations/" + name + "_brick_slab_from_slab.json"
        genResFile(file, name)
    if(flags["stairs_ft_brick_stairs"]):
        file = RECIPES_CRAFTING + "blocks/decorations/" + name + "_stairs_from_brick_stairs.json"
        genResFile(file, name)
        file = RECIPES_CRAFTING + "blocks/decorations/" + name + "_brick_stairs_from_stairs.json"
        genResFile(file, name)

'''
Add additional block models as some block types have additional model files 
'''
def addAdditionalBlockModels(rtype, ltype, name):
    ltype = fileIO.addSlashIfAbsent(ltype)
    if (ltype == "decorations/"):
        RTYPE_SLABS = ["slab", "brick_slab"]
        RTYPE_STAIRS =  ["stairs", "brick_stairs"]
        partialFileName = fileIO.genFileName([ASSETS_MODELS, "block", ltype])
        if (rtype in RTYPE_SLABS):
            file = fileIO.genFileName([partialFileName, name + "_" + rtype + "_top.json"])
            genResFile(file, name)
        if (rtype in RTYPE_STAIRS):
            file = fileIO.genFileName([partialFileName, name + "_" + rtype + "_inner.json"])
            genResFile(file, name)
            file = fileIO.genFileName([partialFileName, name + "_" + rtype + "_outer.json"])
            genResFile(file, name)
        if (rtype == "hopper"):
            file = fileIO.genFileName([partialFileName, name + "_" + rtype + "_side.json"])
            genResFile(file, name)
        if (rtype == "lamp"):
            file = fileIO.genFileName([partialFileName, name + "_" + rtype + "_on.json"])
            genResFile(file, name)
        if (rtype == "bars"):
            file = fileIO.genFileName([partialFileName, name + "_" + rtype + "_noside.json"])
            genResFile(file, name)
            file = fileIO.genFileName([partialFileName, name + "_" + rtype + "_noside_alt.json"])
            genResFile(file, name)
            file = fileIO.genFileName([partialFileName, name + "_" + rtype + "_post.json"])
            genResFile(file, name)
            file = fileIO.genFileName([partialFileName, name + "_" + rtype + "_side.json"])
            genResFile(file, name)
            file = fileIO.genFileName([partialFileName, name + "_" + rtype + "_side_alt.json"])
            genResFile(file, name)
        if (rtype == "door"):
            file = fileIO.genFileName([partialFileName, name + "_" + rtype + "_bottom.json"])
            genResFile(file, name)
            file = fileIO.genFileName([partialFileName, name + "_" + rtype + "_bottom_hinge.json"])
            genResFile(file, name)
            file = fileIO.genFileName([partialFileName, name + "_" + rtype + "_top.json"])
            genResFile(file, name)
            file = fileIO.genFileName([partialFileName, name + "_" + rtype + "_top_hinge.json"])
            genResFile(file, name)
                               
'''
Add additional crafting files/ model files for certain types of item 
currently tools and armor 
'''
def addAdditionalItem(ltype, name, fileLocation):

    ltype = fileIO.addSlashIfAbsent(ltype)

    resname = "item"
    if fileLocation == RECIPES_CRAFTING:
        resname = "items"

    partialFileName = fileIO.genFileName([fileLocation, resname, ltype])


     # Tools here
    if (ltype == "tools/"):
        
        file = fileIO.genFileName([partialFileName, name + "_hoe.json"])
        genResFile(file, name)
        file = fileIO.genFileName([partialFileName, name + "_pickaxe.json"])
        genResFile(file, name)
        file = fileIO.genFileName([partialFileName, name + "_sword.json"])
        genResFile(file, name)
        file = fileIO.genFileName([partialFileName, name + "_shovel.json"])
        genResFile(file, name)

    # Armor here
    if (ltype == "armor/"):
        file = fileIO.genFileName([partialFileName, name + "_chest.json"])
        genResFile(file, name)
        file = fileIO.genFileName([partialFileName, name + "_leggings.json"])
        genResFile(file, name)
        file = fileIO.genFileName([partialFileName, name + "_boots.json"])
        genResFile(file, name)



def gesResNamespace(resType, rtype):

    RTYPE_DECORATIONS = ["bricks", "slab", "stairs", "brick_slab", 
            "brick_stairs", "hopper", "bars", "door", "lamp", "lamp_inverted"]
    RTYPE_ITEMS = ["armor", "tools", "shears"]

    # Get resource namespace (item/ block)
    resname = ["block", "blocks"]
    if (resType == "items"):
        resname = ["item", "items"]
    ltype = ""
    if (rtype == "ore"):
        ltype = "ores/"
    if (rtype == "block"):
        ltype = "storage_blocks/"
    if (rtype in RTYPE_DECORATIONS):
        ltype = "decorations/"
        
    if (rtype in RTYPE_ITEMS):
        
        resname = ["item", "items"]
    if (rtype == "armor"):
        ltype = "armor/"
        rtype = "helm"
    if (rtype == "tools"):
        ltype = "tools/"
        rtype = "axe"
    if (rtype == "shears"):
        ltype = "tools/"
    
    return resname, ltype, rtype


                
'''
Generates data for a set of resources of type resType and with data resData
'''
def genDataRes(resType, resData):
        
    # For each 'line'
    for resDataLine in resData:

        ''' Does the dataLine have specific combinations of types. If yes, add 
        additional crafting recipes. eg. if block and slabs exist add 
        name_block_from_slab recipe
        '''
        FLAGS = setCraftingCombinationsFlags(resDataLine["types"])

        
        # For each name
        for nameIndex in range(len(resDataLine["names"])):
            name = resDataLine["names"][nameIndex]
             
            '''
            Add additional recipes 
            '''
            addCraftingCombinations(FLAGS, name)
                
            
            # For every type 
            for rtype in resDataLine["types"]:
                resname, ltype, rtype = gesResNamespace(resType, rtype)
                print(DATA_MODNAME + ":" + resname[0] + ltype + name + "_" + rtype)

                '''
                DATA CRAFTING RECIPES 
                '''
                # Ore does not have a crafting recipe 
                if (not (rtype == "ore")):
                    file = fileIO.genFileName([RECIPES_CRAFTING, resname[1], ltype, name + "_" + rtype + ".json"])
                    genResFile(file, name)


                addAdditionalItem(ltype, name, RECIPES_CRAFTING)
                

                '''
                DATA LOOT TABLES
                '''
                # If block > blockstates
                if (resname[0] == "block"):
                    file = fileIO.genFileName([LOOT_TABLES, resname[1], ltype, name + "_" + rtype + ".json"])
                    genResFile(file, name)

        
                
'''
Generates assets for a set of resources of type resType and with data resData
'''
def genAssetRes(resType, resData):
    # For each 'line'
    for resDataLine in resData:
        # For each name
        for nameIndex in range(len(resDataLine["names"])):
            name = resDataLine["names"][nameIndex]
            '''
            If it is a resource, generate the gem/ ingot, for items gen item 
            with name
            '''
            if (resType == "resources" or resType == "items"):
                print(name)
                file = fileIO.genFileName([ASSETS_MODELS, "item/", name + ".json"])
                genResFile(file, name)
                
            

            # For every type 
            for rtype in resDataLine["types"]:
                resname, ltype, rtype = gesResNamespace(resType, rtype)
                print(DATA_MODNAME + ":" + resname[0] + ltype + name + "_" + rtype)


                '''
                Blocks Only: 
                '''
                # If block > blockstates
                if (resname[0] == "block"):
                    file = fileIO.genFileName([ASSETS_BLOCKSTATES, ltype, name + "_" + rtype + ".json"])
                    genResFile(file, name)
                    
                    # Stairs and slabs have more block decorations 
                    addAdditionalBlockModels(rtype, ltype, name)

                
                '''
                Items only 
                '''
                if (resname[0] == "item"):
                    addAdditionalItem(ltype, name, ASSETS_MODELS)

                    

                '''
                Everything apart from items only (as they do not have a regular block 
                model "bars", "door", "lamp_inverted"). bars has variation models for the 
                block such as _noside and _noside alt. 
                '''
                ASSETS_MODELS_ITEMS_ONLY = ["bars", "door", "lamp_inverted"]
                if (rtype in ASSETS_MODELS_ITEMS_ONLY):
                    file = fileIO.genFileName([ASSETS_MODELS, "item", ltype, name + "_" + rtype + ".json"])
                    genResFile(file, name)
                else:
                    # (Everything else here)
                    file = fileIO.genFileName([ASSETS_MODELS, resname[0], ltype, name + "_" + rtype + ".json"])
                    genResFile(file, name)


                '''
                DATA FORGE 
                '''
                partialFileName = fileIO.genFileName([DATA_FORGE, resname[1], ltype])
                if (ltype == "decorations/"):
                    file = fileIO.genFileName([partialFileName, name + "_" + rtype + ".json"])
                    genResFile(file, name)
                elif(not (ltype == "tools/" or ltype == "armor/")):
                    file = fileIO.genFileName([partialFileName, name + ".json"])
                    genResFile(file, name)


    

if __name__ == "__main__": # pragma: no cover

    SETTING_LIB, SETTING_REG, SETTING_MAIN = readGenerateMethods()
    DATA_AUTHOR, DATA_MODNAME, DATA_INPUT_FILE, DATA_OUTPUT_FILE = readGeneral()
    RESOURCES, BLOCKS, ITEMS = readBlocksAndItems()


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


    genMethods()
                        
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

