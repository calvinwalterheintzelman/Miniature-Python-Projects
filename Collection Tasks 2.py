#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       2/1/2019
#######################################################

import os
import sys

# Module level Variables.
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Prelab04')

def getIDFromTechnician():
    file = open(DataPath + '/maps/technicians.dat', 'r')
    file.readline()
    file.readline()
    file_str = file.read()
    file.close()

    ID_dict = {}

    i = 0
    while i < len(file_str):
        space_count = 0
        name = ''
        j = i
        while space_count < 2:
            name += file_str[j]
            j += 1
            if file_str[j] == ' ':
                space_count += 1
        ID_dict[name] = file_str[i+44:i+55]
        i += 56

    return ID_dict

def getTechnicianFromID():
    technician_dict = {}
    ID_dict = getIDFromTechnician()
    for name in ID_dict:
        technician_dict[ID_dict[name]] = name

    return technician_dict

def getCostFromVirusID():
    file = open(DataPath + '/maps/viruses.dat')
    file.readline()
    file.readline()
    file_str = file.read()
    cost_dict = {}
    file.close()

    i = 40
    while i < len(file_str):
        cost_dict[file_str[i:i+9]] = float(file_str[i+31:i+35])
        i += 76
    return cost_dict

def getVirusNamefromVirusID():
    file = open(DataPath + '/maps/viruses.dat')
    file.readline()
    file.readline()
    file_str = file.read()
    name_dict = {}
    file.close()

    i = 0
    while i < len(file_str):
        j = i
        name = ''
        while file_str[j] != ' ':
            name += file_str[j]
            j += 1
        name_dict[file_str[i+40:i+49]] = name
        i += 76
    return name_dict

# User ID: XXXXX-XXXXX

def getTechWork(techName):
    ID_dict = getIDFromTechnician()
    techID = ID_dict[techName]

    virus_dict = {}

    reports = os.listdir(DataPath + '/reports')
    for report in reports:
        file = open(DataPath + '/reports/' + report, 'r')
        if techID in file.readline():
            file.readline()
            file.readline()
            file.readline()
            file_str = file.read()
            i = 21
            while i < len(file_str):
                j = i + 9
                virus = file_str[i:j]
                virus_units = ''
                while file_str[j] == ' ':
                    j += 1
                while j < i + 40:
                    virus_units += file_str[j]
                    j += 1

                if virus in virus_dict:
                    virus_dict[virus] += int(virus_units)
                else:
                    virus_dict[virus] = int(virus_units)
                i += 62
        file.close()

    return virus_dict

def getStrainConsumption(virusName):
    tech_virus_dict = {}
    ID_tech_dict = getTechnicianFromID()

    reports = os.listdir(DataPath + '/reports')
    for report in reports:
        file = open(DataPath + '/reports/' + report, 'r')
        file_str = file.read()
        file.close()
        if virusName in file_str:
            virus_num = ''
            technician = ID_tech_dict[file_str[9:20]]
            index = file_str.find(virusName) + 9
            while file_str[index] == ' ':
                index += 1
            while index < len(file_str) and file_str[index].isdigit():
                virus_num += file_str[index]
                index += 1
            # next find the number to the right, Calvin! :D
            if technician in tech_virus_dict:
                tech_virus_dict[technician] += int(virus_num)
                # add value
            else:
                tech_virus_dict[technician] = int(virus_num)
                # it becomes the value
    return tech_virus_dict

def getTechSpending():
    tech_ID_dict = getTechnicianFromID()
    cost_dect = getCostFromVirusID()
    tech_spending_dect = {}

    reports = os.listdir(DataPath + '/reports')
    for report in reports:
        file = open(DataPath + '/reports/' + report, 'r')
        first_line = file.readline()
        technician = tech_ID_dict[first_line[9:20]]
        file.readline()
        file.readline()
        file.readline()
        file_str = file.read()
        file.close()
        if not(technician in tech_spending_dect):
            tech_spending_dect[technician] = 0.0

        i = 21
        while i < len(file_str):
            virus_name = file_str[i:i+9]
            units = ''
            j = i + 9
            while file_str[j] == ' ':
                j += 1
            while j < len(file_str) and file_str[j].isdigit():
                units += file_str[j]
                j += 1
            cost = cost_dect[virus_name]
            tech_spending_dect[technician] += cost*float(units)
            i += 62
    for some_technician in tech_spending_dect:
        tech_spending_dect[some_technician] = round(tech_spending_dect[some_technician], 2)

    return tech_spending_dect

def getStrainCost():
    strain_cost_dict = {}
    virus_name_dict = getVirusNamefromVirusID()
    cost_dect = getCostFromVirusID()

    reports = os.listdir(DataPath + '/reports')
    for report in reports:
        file = open(DataPath + '/reports/' + report, 'r')
        file.readline()
        file.readline()
        file.readline()
        file.readline()
        file_str = file.read()
        file.close()

        i = 21
        while i < len(file_str):
            virus_name = virus_name_dict[file_str[i:i+9]]
            units = ''
            j = i + 9
            while file_str[j] == ' ':
                j += 1
            while j < len(file_str) and file_str[j].isdigit():
                units += file_str[j]
                j += 1
            cost = cost_dect[file_str[i:i+9]]
            total_cost = cost * float(units)
            if virus_name in strain_cost_dict:
                strain_cost_dict[virus_name] += total_cost
            else:
                strain_cost_dict[virus_name] = total_cost
            i += 62

    for virus in strain_cost_dict:
        strain_cost_dict[virus] = round(strain_cost_dict[virus], 2)

    return strain_cost_dict

def getAbsentTechs():
    absent_techs = set([])
    tech_ID_dict = getTechnicianFromID()
    ID_tech_dict = getIDFromTechnician()

    reports = os.listdir(DataPath + '/reports')
    for report in reports:
        file = open(DataPath + '/reports/' + report, 'r')
        first_line = file.readline()
        technician = tech_ID_dict[first_line[9:20]]
        if technician in ID_tech_dict:
            del ID_tech_dict[technician]
        file.close()

    for tech in ID_tech_dict:
        absent_techs = absent_techs.union(set([tech]))

    return absent_techs

def getUnusedStrains():
    unused_strains = set([])
    virus_names = getVirusNamefromVirusID()

    reports = os.listdir(DataPath + '/reports')
    for report in reports:
        file = open(DataPath + '/reports/' + report, 'r')
        file.readline()
        file.readline()
        file.readline()
        file.readline()
        file_str = file.read()
        file.close()

        i = 21
        while i < len(file_str):
            if file_str[i:i+9] in virus_names:
                del virus_names[file_str[i:i+9]]
            i += 62

    for virus in virus_names:
        unused_strains = unused_strains.union(set([virus_names[virus]]))

    return unused_strains

#print(getTechWork('Young, Frank'))
#print(getStrainConsumption('PHE-99329'))
#print(getTechSpending())
#print(getStrainCost())
#print(getAbsentTechs())
#print(getUnusedStrains())
