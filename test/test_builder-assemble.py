import os, sys, inspect
THISDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# Add ../lib to the import path 
sys.path.insert(0, os.path.dirname(THISDIR) + "/lib")
sys.path.insert(0, os.path.dirname(THISDIR) + "/Builder")


# Generate coverage data with py.test test\test_builder-assemble.py --cov=builder
# Get pretty output with coverage report or coverage html

import fileIO, assemble

assemble.CONFIG_M = THISDIR + "/testBuilderGenerateMethods.json"
assemble.CONFIG_G = THISDIR + "/testBuilderGeneral.json"
assemble.CONFIG_B = THISDIR + "/testBuilderBlocksAndItems.json"

assemble.DATA_AUTHOR, assemble.DATA_MODNAME, assemble.DATA_INPUT_FILE, assemble.DATA_OUTPUT_FILE = assemble.readGeneral()

assemble.DATA_INPUT_FILE = THISDIR + "/" + assemble.DATA_INPUT_FILE
assemble.DATA_OUTPUT_FILE = THISDIR + "/" + assemble.DATA_OUTPUT_FILE


# Generate Resources - Useful Constants 
ASSETS = assemble.DATA_INPUT_FILE + "/src/main/resources/assets/examplemod"
DATA = assemble.DATA_INPUT_FILE + "/src/main/resources/data"
META_INF = assemble.DATA_INPUT_FILE + "/src/main/resources/META-INF"

assemble.ASSETS_BLOCKSTATES = ASSETS + "/blockstates/" # decorations ore storage_block
assemble.ASSETS_LANG = ASSETS + "/lang/" # en_us 
assemble.ASSETS_MODELS = ASSETS + "/models/" # block(decorations ore storage_block) item([block] armour tools /)
assemble.ASSETS_TEXTURES = ASSETS + "/textures/" # block(decorations ore storage_block) item(armor tools /) models(armor)

assemble.DATA_MOD = DATA + "/examplemod/" # loot_tables(blocks(decorations ore storage_block))
#recipes(crafting(blocks(decorations /) items(armor tools /) smelting(blocks items(/) ))
assemble.DATA_FORGE = DATA + "/forge/tags/" # blocks(decorations ores storage_blocks) items([block] gems)
assemble.DATA_MINECRAFT = DATA + "/minecraft/"

assemble.LOOT_TABLES = assemble.DATA_MOD + "loot_tables/"
assemble.RECIPES = assemble.DATA_MOD + "recipes/"
assemble.RECIPES_CRAFTING = assemble.RECIPES + "crafting/"

def test_readGenerateMethods():
    assert(assemble.readGenerateMethods() == ("True", "True", "True"))



def test_readGeneral():
    assert(assemble.readGeneral() == ("testAuthor", "thisIsA", "testBuilderRes", "testBuilderOut"))


def test_readBlocksAndItems():
    assert(assemble.readBlocksAndItems()[1] == [{"names" : ["block_name0"],
    "types" : ["ore", "block", "bricks", "slab", "stairs", "brick_slab", 
    "brick_stairs", "tools", "armor", "shears", "bars", "door", "lamp", 
    "lamp_inverted"]}])


def test_genMethods111():
    assemble.SETTING_LIB, assemble.SETTING_REG, assemble.SETTING_MAIN = "True", "True", "True"
    assemble.genMethods()
    assert(fileIO.fileToString(assemble.DATA_OUTPUT_FILE + "/src/main/java/com/testAuthor/thisIsA/main.java") == 
    fileIO.fileToString(assemble.DATA_INPUT_FILE + "/src/main/java/com/example/examplemod/main.java")
    .replace("com.example.examplemod", "com." +assemble.DATA_AUTHOR+"."+assemble.DATA_MODNAME))



def test_genResFile():
    assemble.genResFile(assemble.DATA_INPUT_FILE + "/src/main/resources/assets/examplemod/models/item/testItem.json", "testItem")
    assert(fileIO.fileToString(assemble.DATA_OUTPUT_FILE + "/src/main/resources/assets/thisIsA/models/item/testItem.json") ==
    fileIO.fileToString(assemble.DATA_INPUT_FILE + "/src/main/resources/assets/examplemod/models/item/aquamarine.json")
    .replace("anothergemsmod", assemble.DATA_MODNAME).replace("aquamarine", "testItem"))


def test_genResFiles():
    assemble.genResFiles(assemble.DATA_INPUT_FILE + "/src/main/resources/assets/examplemod/models/item/", "secondTestItem")
    assert(fileIO.fileToString(assemble.DATA_OUTPUT_FILE + "/src/main/resources/assets/thisIsA/models/item/secondTestItem.json") ==
    fileIO.fileToString(assemble.DATA_INPUT_FILE + "/src/main/resources/assets/examplemod/models/item/aquamarine.json")
    .replace("anothergemsmod", assemble.DATA_MODNAME).replace("aquamarine", "secondTestItem"))




def test_setCraftingCombinationsFlagsBlockSlab():
    assert(assemble.setCraftingCombinationsFlags(["block", "slab"])["block_f_slab"])


def test_setCraftingCombinationsFlagsBricksSlab():
    assert(assemble.setCraftingCombinationsFlags(["bricks", "brick_slab"])["bricks_f_slab"])


def test_setCraftingCombinationsFlagsBricksBlock():
    assert(assemble.setCraftingCombinationsFlags(["bricks", "block"])["block_f_bricks"])



def test_setCraftingCombinationsFlagsSlabBrickSlab():
    assert(assemble.setCraftingCombinationsFlags(["slab", "brick_slab"])["slab_ft_brick_slab"])


def test_setCraftingCombinationsFlagsStairsBrickStairs():
    assert(assemble.setCraftingCombinationsFlags(["stairs", "brick_stairs"])["stairs_ft_brick_stairs"])


def test_addCraftingCombinations():
    flags = assemble.setCraftingCombinationsFlags(assemble.readBlocksAndItems()[1][0]["types"])
    assemble.addCraftingCombinations(flags, "testBlock")
    craftingDir = assemble.DATA_OUTPUT_FILE + "/src/main/resources/data/thisIsA/recipes/crafting/blocks"
    assert(set(fileIO.getListOfFiles(craftingDir, False)).issuperset(set([
        craftingDir + "\\decorations\\testBlock_brick_slab_from_slab.json", 
        craftingDir + "\\decorations\\testBlock_brick_stairs_from_stairs.json",
        craftingDir + "\\decorations\\testBlock_bricks_from_slab.json", 
        craftingDir + "\\decorations\\testBlock_slab_from_brick_slab.json",
        craftingDir + "\\decorations\\testBlock_stairs_from_brick_stairs.json", 
        craftingDir + "\\storage_blocks\\testBlock_block_from_bricks.json",
        craftingDir + "\\storage_blocks\\testBlock_block_from_slab.json"
    ])))



def test_addAdditionalBlockModelsDecorSlab():
    assemble.addAdditionalBlockModels("slab", "decorations/", "testBlock")
    parentDir = assemble.DATA_OUTPUT_FILE + "/src/main/resources/assets/thisIsA/models/block/decorations"
    assert(set(fileIO.getListOfFiles(parentDir, True)).issuperset(set([
        parentDir + "\\testBlock_slab_top.json"
        ])))


def test_addAdditionalBlockModelsDecorStairs():
    assemble.addAdditionalBlockModels("stairs", "decorations/", "testBlock")
    parentDir = assemble.DATA_OUTPUT_FILE + "/src/main/resources/assets/thisIsA/models/block/decorations"
    assert(set(fileIO.getListOfFiles(parentDir, True)).issuperset(set([
        parentDir + "\\testBlock_stairs_inner.json",
        parentDir + "\\testBlock_stairs_outer.json"
        ])))


def test_addAdditionalBlockModelsDecorHopper():
    assemble.addAdditionalBlockModels("hopper", "decorations/", "testBlock")
    parentDir = assemble.DATA_OUTPUT_FILE + "/src/main/resources/assets/thisIsA/models/block/decorations"
    assert(set(fileIO.getListOfFiles(parentDir, True)).issuperset(set([
        parentDir + "\\testBlock_hopper_side.json"
        ])))


def test_addAdditionalBlockModelsDecorLamp():
    assemble.addAdditionalBlockModels("lamp", "decorations/", "testBlock")
    parentDir = assemble.DATA_OUTPUT_FILE + "/src/main/resources/assets/thisIsA/models/block/decorations"
    assert(set(fileIO.getListOfFiles(parentDir, True)).issuperset(set([
        parentDir + "\\testBlock_lamp_on.json"
        ])))


def test_addAdditionalBlockModelsDecorBars():
    assemble.addAdditionalBlockModels("bars", "decorations/", "testBlock")
    parentDir = assemble.DATA_OUTPUT_FILE + "/src/main/resources/assets/thisIsA/models/block/decorations"
    assert(set(fileIO.getListOfFiles(parentDir, True)).issuperset(set([
        parentDir + "\\testBlock_bars_noside.json",
        parentDir + "\\testBlock_bars_noside_alt.json",
        parentDir + "\\testBlock_bars_post.json",
        parentDir + "\\testBlock_bars_side.json",
        parentDir + "\\testBlock_bars_side_alt.json"
        ])))


def test_addAdditionalBlockModelsDecorDoor():
    assemble.addAdditionalBlockModels("door", "decorations/", "testBlock")
    parentDir = assemble.DATA_OUTPUT_FILE + "/src/main/resources/assets/thisIsA/models/block/decorations"
    assert(set(fileIO.getListOfFiles(parentDir, True)).issuperset(set([
        parentDir + "\\testBlock_door_bottom.json",
        parentDir + "\\testBlock_door_bottom_hinge.json",
        parentDir + "\\testBlock_door_top.json",
        parentDir + "\\testBlock_door_top_hinge.json"
        ])))


def test_addAdditionalItemTools():
    assemble.addAdditionalItem("tools", "testItem",assemble.RECIPES_CRAFTING)
    parentDir = assemble.DATA_OUTPUT_FILE + "/src/main/resources/data/thisIsA/recipes/crafting/items/tools"
    assert(set(fileIO.getListOfFiles(parentDir, True)).issuperset(set([
        parentDir + "\\testItem_hoe.json",
        parentDir + "\\testItem_pickaxe.json",
        parentDir + "\\testItem_sword.json",
        parentDir + "\\testItem_shovel.json"
        ])))



def test_addAdditionalItemArmor():
    assemble.addAdditionalItem("armor", "testItem",assemble.RECIPES_CRAFTING)
    parentDir = assemble.DATA_OUTPUT_FILE + "/src/main/resources/data/thisIsA/recipes/crafting/items/armor"
    assert(set(fileIO.getListOfFiles(parentDir, True)).issuperset(set([
        parentDir + "\\testItem_chest.json",
        parentDir + "\\testItem_leggings.json",
        parentDir + "\\testItem_boots.json",
        ])))



def test_gesResNamespaceItemsOre():
    assert(assemble.gesResNamespace("items", "ore") == (["item", "items"], "ores/", "ore"))
    

def test_gesResNamespaceItemsBlock():
    assert(assemble.gesResNamespace("items", "block") == (["item", "items"], "storage_blocks/", "block"))


def test_gesResNamespaceItemsBricks():
    assert(assemble.gesResNamespace("items", "bricks") == (["item", "items"], "decorations/", "bricks"))


def test_gesResNamespaceItemsArmor():
    assert(assemble.gesResNamespace("items", "armor") == (["item", "items"], "armor/", "helm"))


def test_gesResNamespaceItemsTools():
    assert(assemble.gesResNamespace("items", "tools") == (["item", "items"], "tools/", "axe"))


def test_gesResNamespaceItemsShears():
    assert(assemble.gesResNamespace("items", "shears") == (["item", "items"], "tools/", "shears"))


def test_gesResNamespaceNotItemsOre():
    assert(assemble.gesResNamespace("", "ore") == (["block", "blocks"], "ores/", "ore"))


def test_gesResNamespaceNotItemsBlock():
    assert(assemble.gesResNamespace("", "block") == (["block", "blocks"], "storage_blocks/", "block"))


def test_gesResNamespaceNotItemsBricks():
    assert(assemble.gesResNamespace("", "bricks") == (["block", "blocks"], "decorations/", "bricks"))


def test_gesResNamespaceNotItemsArmor():
    assert(assemble.gesResNamespace("", "armor") == (["item", "items"], "armor/", "helm"))


def test_gesResNamespaceNotItemsTools():
    assert(assemble.gesResNamespace("", "tools") == (["item", "items"], "tools/", "axe"))


def test_gesResNamespaceNotItemsShears():
    assert(assemble.gesResNamespace("", "shears") == (["item", "items"], "tools/", "shears"))

'''
Test wrappers as genRes function is intended to be acesseed through these
'''
def test_genDataResBlock():
    assemble.genDataRes("blocks", assemble.readBlocksAndItems()[0])
    pass


def test_genDataResItem():
    assemble.genDataRes("items", assemble.readBlocksAndItems()[2])
    pass


def test_genAssetResResOrItem():
    assemble.genAssetRes("resources", assemble.readBlocksAndItems()[0])

    pass


def test_genAssetResBlock():
    assemble.genAssetRes("blocks", assemble.readBlocksAndItems()[0])

    pass


def test_genAssetResItem():
    assemble.genAssetRes("items", assemble.readBlocksAndItems()[2])

    pass

