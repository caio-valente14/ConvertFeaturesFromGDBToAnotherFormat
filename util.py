# -*- coding: utf-8 -*-

# Import packages
import os
import sys
import traceback
import shutil

# Import config variables
from config import PATHS as paths
historicFolder = paths['HISTORIC_FOLDER']
resultsFolder = paths['RESULTS_FOLDER']
toConvertFolder = paths['TO_CONVERT_FOLDER']


# Define util functions
def getFormattedException():
    excType, excValue, excTb = sys.exc_info()
    formattedException = traceback.format_exception(excType, excValue, excTb)

    return '\n'.join(formattedException)


def customPrint(type, message):
    print(f'{type}: {message}')

    return True


def listGDBs():
    filesNames = os.listdir(toConvertFolder)

    GDBs = []
    for fileName in filesNames:
        extension = os.path.splitext(fileName)[1]

        if extension == '.gdb':
            file = os.path.join(toConvertFolder, fileName)
            GDBs.append(file)

    message = 'All file geodatabases were successfully listed!\n'

    return [message, GDBs]


def createFolder(dir, folderName):
    folderToCreate = os.path.join(dir, folderName)

    if os.path.exists(folderToCreate):
        shutil.rmtree(folderToCreate)

    os.makedirs(folderToCreate)

    return folderToCreate







