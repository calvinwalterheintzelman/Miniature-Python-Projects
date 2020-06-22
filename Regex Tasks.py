#######################################################
#    Author:        Calvin Walter Heintzelman
#    email:         cheintze@purdue.edu
#    ID:            ee364f17
#    Date:          2/17/2019
#######################################################
import os
import sys
import re
from uuid import UUID

# Module  level  Variables.
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Prelab06')

def getUrlParts(url):
    no_slashes = re.findall(r"([^/]+)", url)
    base_address = no_slashes[1]
    controller = no_slashes[2]
    action = re.search(r"([^?]+)", no_slashes[3])
    return (base_address, controller, action[0])

def getQueryParameters(url):
    q_string_on_right = re.findall(r"([^?]+)", url)
    q_string = q_string_on_right[1]
    parameters = re.findall(r"([^&]+)", q_string)
    result = []
    for parameter in parameters:
        elements = re.findall(r"([^=]+)", parameter)
        result.append((elements[0], elements[1]))
    return result

def getSpecial(sentence, letter):
    pattern = r"(\b{0}\w*[^{0}\W]\b|\b[^{0}\W]\w*{0}\b)".format(letter)
    words = re.findall(pattern, sentence, re.IGNORECASE)
    return words

def getRealMAC(sentence):
    pattern = r"(([a-f]|[0-9])([a-f]|[0-9]):([a-f]|[0-9])([a-f]|[0-9]):([a-f]|[0-9])([a-f]|[0-9]):([a-f]|[0-9])([a-f]|[0-9]):([a-f]|[0-9])([a-f]|[0-9]):([a-f]|[0-9])([a-f]|[0-9]))"
    address = re.search(pattern, sentence, re.IGNORECASE)
    if address is None:
        pattern = r"(([a-f]|[0-9])([a-f]|[0-9])-([a-f]|[0-9])([a-f]|[0-9])-([a-f]|[0-9])([a-f]|[0-9])-([a-f]|[0-9])([a-f]|[0-9])-([a-f]|[0-9])([a-f]|[0-9])-([a-f]|[0-9])([a-f]|[0-9]))"
        address = re.search(pattern, sentence, re.IGNORECASE)
        if address is None:
            return None
    return address[0]

def getData():
    file = open(DataPath + '/Employees.txt')

    line = file.readline()
    result = []
    while line != '':
        [name] = re.findall(r"(\A[a-z]+,[ ][a-z]+|\A[a-z]+[ ][a-z]+)", line, re.IGNORECASE)
        if ',' in name:
            [last, first] = re.findall(r"([a-z]+)", name, re.IGNORECASE)
            name = first + ' ' + last

        ID = re.findall(r"([0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12})", line, re.IGNORECASE)
        if len(ID) == 0:
            ID = None
        else:
            ID = str(UUID(ID[0]))

        number = re.findall(r"(,|\s|;)(\(?\d{3}\)?\s?-?\d{3}-?\d{4})(,|\s|;)", line)
        if len(number) != 0:
            number = number[0][1]
            if len(number) == 10:
                number = '(' + number[0:3] + ') ' + number[3:6] + '-' + number[6:10]
            if len(number) == 12:
                number = '(' + number[0:3] + ') ' + number[4:12]
        else:
            number = None

        state = re.findall(r"([a-z]+[ ]?[a-z]+)(\n)", line, re.IGNORECASE)
        if len(state) == 0:
            state = None
        else:
            state = state[0][0]

        result.append((name, ID, number, state))

        line = file.readline()

    return result

def getRejectedEntries():
    result = []
    data = getData()
    for entry in data:
        if entry[1] is None and entry[2] is None and entry[3] is None:
            result.append(entry[0])
    result.sort()
    return result

def getEmployeesWithIDs():
    result = {}
    data = getData()
    for entry in data:
        if not(entry[1] is None):
            result[entry[0]] = entry[1]
    return result

def getEmployeesWithoutIDs():
    result = []
    data = getData()
    for entry in data:
        if entry[1] is None and (not(entry[2] is None) or not(entry[3] is None)):
            result.append(entry[0])
    result.sort()
    return result

def getEmployeesWithPhones():
    result = {}
    data = getData()
    for entry in data:
        if entry[2] is not None:
            result[entry[0]] = entry[2]
    return result

def getEmployeesWithStates():
    result = {}
    data = getData()
    for entry in data:
        if entry[3] is not None:
            result[entry[0]] = entry[3]
    return result

def getCompleteEntries():
    result = {}
    data = getData()
    for entry in data:
        if entry[0] is not None and entry[1] is not None and entry[2] is not None and entry[3] is not None:
            result[entry[0]] = (entry[1], entry[2], entry[3])
    return result
