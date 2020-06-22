#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       1/23/2019
#######################################################

import os
import sys

# Module level Variables.
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Lab02')

def getCodeFor(stateName):
    result = []
    filename = DataPath + '/zip.dat'
    file = open(filename, 'r')
    file.readline()
    file.readline() # skips 2 lines that don't matter

    file_str = file.read()
    file.close()

    line = 0
    for all_lines in range(700):
        line_str = file_str[line:line+29]
        if line_str[0:len(stateName)] == stateName:
            sort_index = 0
            for i in range(len(result)):
                if int(result[i]) < int(line_str[24:29]):
                    sort_index += 1
                else:
                    break
            result.insert(sort_index, line_str[24:29])
        line += 30

    return result

def getMinLatitude(stateName):
    filename = DataPath + '/coordinates.dat'
    file = open(filename, 'r')
    file.readline()
    file.readline() # skips 2 lines that don't matter

    file_str = file.read()
    file.close()

    zipcodes = getCodeFor(stateName)

    line = 0
    min_latitude = None
    for all_lines in range(700):
        line_str = file_str[line:line+42]
        for zipcode in zipcodes:
            if line_str[37:42] == zipcode:
                latitude = float(line_str[0:7])
                if min_latitude is None or latitude < min_latitude:
                    min_latitude = latitude
        line += 43

    return min_latitude

def getMaxLongitude(stateName):
    filename = DataPath + '/coordinates.dat'
    file = open(filename, 'r')
    file.readline()
    file.readline() # skips 2 lines that don't matter

    file_str = file.read()
    file.close()

    zipcodes = getCodeFor(stateName)

    line = 0
    max_longitude = None
    for all_lines in range(700):
        line_str = file_str[line:line+42]
        for zipcode in zipcodes:
            if line_str[37:42] == zipcode:
                longitude = float(line_str[16:27])
                if max_longitude is None or longitude > max_longitude:
                    max_longitude = longitude
        line += 43

    return max_longitude

def getSubMatrixSum(startRowIndex, endRowIndex, startColumnIndex, endColumnIndex):
    filename = DataPath + '/matrix.dat'
    file = open(filename, 'r')
    file_str = file.read()
    file.close()

    matrix = []
    for i in range(100):
        matrix.insert(0, [])

    line = 0
    for i in range(100):
        line_str = file_str[line:line+299]
        for j in range(100):
            matrix[i].insert(len(matrix[i]),int(line_str[j*3:j*3+2]))
        line += 300

    sum = 0
    for i in range(startRowIndex, endRowIndex + 1):
        for j in range(startColumnIndex, endColumnIndex + 1):
            sum += matrix[i][j]

    return sum