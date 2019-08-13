import os, sys, inspect
THISDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# Add ../lib to the import path 
sys.path.insert(0, os.path.dirname(THISDIR) + "/lib")

# Generate coverage data with py.test test\test_fileIO.py --cov=fileIO
# Get pretty output with coverage report or coverage html

import fileIO

def test_readJSON():
    testDictionary = {"myInt": 1234, "myString": "1234", "myFloat": 12.34, "myBool": True}
    assert(fileIO.readJSON(THISDIR + "/testFileIO.json") == testDictionary)


def test_stringToFile():
    testString = "this is a test"
    testFile = THISDIR + "/stringToFile.txt"
    fileIO.stringToFile(testFile, testString)
    assert(fileIO.fileToString(testFile) == testString)


def test_fileToTokens():
    testTokens = ["this\n", "is\n", "a\n", "test"]
    assert(fileIO.fileToTokens(THISDIR + "/testFileIO.txt") == testTokens)


def test_fileToString():
    testString = "this\nis\na\ntest"
    assert(fileIO.fileToString(THISDIR + "/testFileIO.txt") == testString)



def test_getListOfFilesChildOnly():
    testDir = THISDIR + "/testDir"
    testResults = [testDir + "\\a.txt", testDir + "\\b.txt"]
    assert(set(fileIO.getListOfFiles(testDir, True)) == set(testResults))

def test_getListOfFilesAll():
    testDir = THISDIR + "/testDir"
    testResults = [testDir + "\\a.txt", testDir + "\\b.txt", testDir + "\\c\\a.txt"]
    assert(set(fileIO.getListOfFiles(testDir, False)) == set(testResults))


def test_addSlashIfAbsentAbsent():
    assert(fileIO.addSlashIfAbsent("test") == "test/")

    
def test_addSlashIfAbsentNotAbsent():
    assert(fileIO.addSlashIfAbsent("test/") == "test/")


def test_genFileName():
    assert(fileIO.genFileName(["test", "file.txt"]) == "test/file.txt")


def test_makeSingularPlural():
    assert(fileIO.makeSingular("tests") == "test")


def test_makeSingularSingular():
    assert(fileIO.makeSingular("test") == "test")
