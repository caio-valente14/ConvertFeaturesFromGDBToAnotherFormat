# -*- coding: utf-8 -*-

# Import packages
import os
import shutil
import fiona
import geopandas as gpd

# Import functions from util
from util import getFormattedException, listGDBs, customPrint, createFolder

# Import  config variables
from config import PATHS as paths, EXTENSION_DICT as extensionDict

historicFolder = paths['HISTORIC_FOLDER']
resultsFolder = paths['RESULTS_FOLDER']
toConvertFolder = paths['TO_CONVERT_FOLDER']


# Define functions
def convertGDBsToAnotherFormat(outputFormat):
    convertedGDBs = []
    notConvertedGDBs = []
    outputFormatUpper = outputFormat.upper()

    try:
        customPrint('MESSAGE', 'Listing only file geodatabases from folder {}...\n'.format(toConvertFolder))

        message, GDBs = listGDBs()

        customPrint('MESSAGE', message)

        extension = extensionDict[outputFormatUpper][0]
        driver = extensionDict[outputFormatUpper][1]

        for GDB in GDBs:
            GDBName = os.path.splitext(os.path.basename(GDB))[0]

            customPrint('MESSAGE', '--- Working on file geodatabase {} ---\n'.format(GDBName))

            GDBFolder = createFolder(resultsFolder, GDBName)

            customPrint('MESSAGE', 'Listing only feature datasets from file geodatabase {}...\n'.format(GDBName))

            try:
                featuresClassesNames = fiona.listlayers(GDB)

                for featureClassName in featuresClassesNames:
                    customPrint('MESSAGE',
                               '-- Working on feature class {} in the file geodatabase {} --\n'.format(
                                   featureClassName, GDBName))

                    featureClass_gdf = gpd.read_file(GDB, layer=featureClassName)

                    numberOfRows = int(featureClass_gdf.shape[0])

                    if numberOfRows == 0:
                        customPrint('WARNING', '-- Feature class {} in file geodatabase {} is empty, so it was not converted --\n'.format(featureClassName, GDBName))
                        continue

                    if outputFormatUpper == 'SHAPEFILE' or outputFormatUpper == 'GEOJSON':
                        outputFileName = featureClassName + extension
                        outputFile = os.path.join(GDBFolder, outputFileName)
                        featureClass_gdf.to_file(outputFile, driver=driver)

                    else:
                        outputFileName = GDBName + extension
                        outputFile = os.path.join(GDBFolder, outputFileName)
                        featureClass_gdf.to_file(outputFile, driver=driver)

                    customPrint('MESSAGE',
                               '-- Feature classe {} in file geodatabase {} was successfully converted --\n'.format(
                                   featureClassName, GDBName))
                convertedGDBs.append(GDB)

            except:
                formattedException = getFormattedException()
                customPrint('ERROR',
                    'There was a problem while converting feature classes from file geodatabase {}\nError:\n{}\n'.format(
                        GDBName, formattedException))
                notConvertedGDBs.append(GDB)

                continue

        message = 'All the features classes from file geodatabases were successfully converted!\n'

        return [True, message, convertedGDBs, notConvertedGDBs]

    except:
        formattedException = getFormattedException()

        message = "There was a problem while converting feature classes to shapefiles.\nError:\n{}\n".format(
            formattedException)

        return [False, message, convertedGDBs, notConvertedGDBs]


def moveGDBsFromCovertFolderToHistoric(convertedGDBs):
    try:
        for convertedGDB in convertedGDBs:
            GDBNameWithExtension = os.path.basename(convertedGDB)
            GDBDest = os.path.join(historicFolder, GDBNameWithExtension)

            shutil.move(convertedGDB, GDBDest)

        message = 'All GDBs which were converted were successfully moved to Historic folder\n'

        return [True, message]

    except:
        formattedException = getFormattedException()

        message = 'There was a problem while moving GDBs from To-Check folder to GDBs-Historic folder.\nError:\n{}\n'.format(
            formattedException)

        return [False, message]


def deleteNotConvertedFolder(notConvertedGDBs):
    try:
        for notConvertedGDB in notConvertedGDBs:
            GDBName = os.path.splitext(os.path.basename(notConvertedGDB))

            foldersNames = os.listdir(resultsFolder)

            for folderName in foldersNames:
                if GDBName == folderName:
                    folder = os.path.join(resultsFolder, folderName)
                    shutil.rmtree(folder)

                    continue

        message = "All folder created for file geodatabases which weren't converted were successfully deleted\n"

        return [True, message]

    except:
        formattedException = getFormattedException()

        message = 'There was a problem while deleting folders from Results folder from not converted GDBs.\nError:\n{}\n'.format(formattedException)

        return [False, message]
