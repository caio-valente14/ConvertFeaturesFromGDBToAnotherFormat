# -*- coding: utf-8 -*-

# Import packages
import os
import sys

# Import util functions
from util import getFormattedException, customPrint

# Import functions from functions
from functions import convertGDBsToAnotherFormat, moveGDBsFromCovertFolderToHistoric, deleteNotConvertedFolder

# Get arguments from cmd
argv = sys.argv
outputFormat = argv[1]


# Define main function
def main(outputFormat):
    try:
        runSuccessfully, message, convertedGDBs, notConvertedGDBs = convertGDBsToAnotherFormat(outputFormat)

        if not runSuccessfully:
            raise Exception(message)

        runSuccessfully, message = moveGDBsFromCovertFolderToHistoric(convertedGDBs)

        if not runSuccessfully:
            raise Exception(message)

        runSuccessfully, message = deleteNotConvertedFolder(notConvertedGDBs)

        if not runSuccessfully:
            raise Exception(message)

        return [True, message]

    except:
        formattedException = getFormattedException()

        return [False, 'There was a problem while running function main.\nError:\n{}'.format(formattedException)]


if __name__ == '__main__':
    runSuccessfully, message = main(outputFormat)

    if not runSuccessfully:
        type = 'ERROR'

    else:
        type = 'MESSAGE'

    customPrint(type, message)
