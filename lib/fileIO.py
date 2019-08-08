
import os

# Read json file
def readJSON(file_name):
    import json
    with open(file_name) as json_file:
        return json.load(json_file)



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


'''
Adds a '/' if absent from a directory name (eg 'src' -> 'src/')
'''
def addSlashIfAbsent(name):
    if name.count("/") > 0:
        return name
    else:
        return name + "/"

'''
Generate a file name for use from a list of parts. The string at the end
of the list is assumed to be the file and so should not have a slash added.
Allows for lazy name building 
'''
def genFileName(parts):
    fileName = ""
    for index in range (len(parts) - 1):
        fileName += addSlashIfAbsent(parts[index])
    fileName += parts[len(parts)-1]
    return fileName

'''
Strip the leading 's' if present 
'''
def makeSingular(name):
    if name[len(name)-1] == "s":
        return name[:-1]
    return name

