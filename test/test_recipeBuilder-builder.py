import os, sys, inspect
THISDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# Add ../lib to the import path 
sys.path.insert(0, os.path.dirname(THISDIR) + "/lib")
sys.path.insert(0, os.path.dirname(THISDIR) + "/RecipeBuilder")


# Generate coverage data with py.test test\test_recipeBuilder-builder.py --cov=recipebuilder
# Get pretty output with coverage report or coverage html

import fileIO, builder

builder.CONFIG = THISDIR + "/testRecipeBuilder.json"
builder.AUTHOR, builder.NAMESPACE, builder.NAME_FROM_INGREDIENT, builder.RECIPES, builder.IMPLEMENTATIONS = builder.readConfig()
builder.RESDIR = THISDIR + "/testRecipeBuilderInput"
builder.OUTDIR = THISDIR + "/"

'''
Assumption: if the field 'author' is parsed correctly (and is as expected) then
the entire config has been parsed correctly
'''
def test_readConfig():
    author, namespace, name_from_ingredient, recipes, implementations = builder.readConfig()
    assert(author == "testAuthor")


def test_getRecipe():
    assert(builder.getRecipe("test0") == {"id": "test0", "pattern": ["A  ", " A ", "  A"],
    "predef_ingredients": [], "group": "test_group0","count": 1})


def test_getRecipeTypePattern():
    assert(builder.getRecipeType(builder.getRecipe("test0")) == "pattern")


def test_getRecipeTypeShapeless():
    assert(builder.getRecipeType(builder.getRecipe("test1")) == "shapeless")

def test_getRecipeTypeUndefined():
    assert(builder.getRecipeType(builder.getRecipe("test2")) == "")

'''
Assumption: if the field 'pattern' is parsed correctly (and is as expected) then
the recipe has been assembled and written correctly
'''
def test_assembleRecipePattern():
    builder.assembleRecipe("pattern", {"id": "test0", "pattern": ["A  ", " A ", "  A"],
    "predef_ingredients": [], "group": "test_group0","count": 1}, "thisIsA:result", ["thisIsA:ingredient"])
    assert(fileIO.readJSON(THISDIR + "/result_from_ingredient.json")["pattern"] == ["A  ", " A ", "  A"])


def test_assembleRecipeShapeless():
    builder.assembleRecipe("shapeless", {"id": "test1","shapeless": ["A", "B"],
        "predef_ingredients": [{"A": "thisIsA:ingredient"}],"group": "test_group1","count": 1},
         "thisIsA:result", ["thisIsA:notherIngredient"])
    assert(fileIO.readJSON(THISDIR + "/result_from_notherIngredient.json")["group"] == "thisIsA:test_group1")


def test_getAllImplementationsPattern():
    builder.IMPLEMENTATIONS = [{"usesid": "test0","ingredients": [["thisIsA:result", ["thisIsA:ingredient"]]]}]
    builder.getAllImplementations()
    assert(fileIO.readJSON(THISDIR + "/result_from_ingredient.json")["pattern"] == ["A  ", " A ", "  A"])



def test_getAllImplementationsShapeless():
    builder.IMPLEMENTATIONS = [{"usesid": "test1","ingredients": [["thisIsA:result", ["thisIsA:notherIngredient"]]]}]
    builder.getAllImplementations()
    assert(fileIO.readJSON(THISDIR + "/result_from_notherIngredient.json")["group"] == "thisIsA:test_group1")



def test_getNamespacedIngredientSpecified():
    assert(builder.getNamespacedIngredient("thisIsA:test") == "thisIsA:test")


def test_getNamespacedIngredientNotSpecified():
    assert(builder.getNamespacedIngredient("test") == "thisIsA:test")


def test_stripNamespaceSpecified():
    assert(builder.stripNamespace("thisIsA:test") == "test")


def test_stripNamespaceNotSpecified():
    assert(builder.stripNamespace("test") == "test")


