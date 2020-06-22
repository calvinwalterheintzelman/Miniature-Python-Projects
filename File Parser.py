#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       2/6/2019
#######################################################

import os
import sys

# Module level Variables.
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Lab04')



def getDifference(provider1, provider2):
    providers = os.listdir(DataPath + '/providers/')
    if not(provider1 + '.dat' in providers):
        raise ValueError('Error! provider1 is not in the data folder!')
    if not(provider2 + '.dat' in providers):
        raise ValueError('Error! provider2 is not in the data folder!')

    result = set([])
    first_prov_list = []
    sec_prov_list = []
    file1 = open(DataPath + '/providers/' + provider1 + '.dat', 'r')
    file1.readline()
    file1.readline()
    file1.readline()
    file1_str = file1.read()
    file1.close()
    i = 0
    while i < len(file1_str):
        if file1_str[i:i+5] == 'Rasp.':
            j = i+6
            while file1_str[j] != ' ':
                j += 1
            first_prov_list.insert(0, file1_str[i:j])
        i += 1

    file2 = open(DataPath + '/providers/' + provider2 + '.dat', 'r')
    file2.readline()
    file2.readline()
    file2.readline()
    file2_str = file2.read()
    file2.close()
    i = 0
    while i < len(file2_str):
        if file2_str[i:i+5] == 'Rasp.':
            j = i+6
            while file2_str[j] != ' ':
                j += 1
            sec_prov_list.insert(0, file2_str[i:j])
        i += 1

    for sbc in first_prov_list:
        if not(sbc in sec_prov_list):
            result = result.union([sbc])

    return result

def getPriceOf(sbc, provider):
    result = ''
    providers = os.listdir(DataPath + '/providers/')
    if not (provider + '.dat' in providers):
        raise ValueError('Error! provider is not in the data folder!')

    file = open(DataPath + '/providers/' + provider + '.dat')
    file_str = file.read()
    file.close()
    if not(sbc in file_str):
        raise ValueError('Error! The SBC requested is not in the provider file!')

    i = file_str.index(sbc) + len(sbc)
    while file_str[i] != '$':
        i += 1
    i += 1
    while i < len(file_str) and ((file_str[i].isdigit() is True) or (file_str[i] == '.')):
        result += file_str[i]
        i += 1

    return float(result)

def checkAllPrices(sbcSet):
    result = {}
    providers = os.listdir(DataPath + '/providers/')

    for sbc in sbcSet:
        min_cost_list = []
        for provider in providers:
            file = open(DataPath + '/providers/' + provider, 'r')
            file_str = file.read()
            file.close()
            cost = -1.0
            if sbc in file_str:
                cost = ''
                i = file_str.index(sbc) + len(sbc)
                while file_str[i] != '$':
                    i += 1
                i += 1
                while i < len(file_str) and ((file_str[i].isdigit() is True) or (file_str[i] == '.')):
                    cost += file_str[i]
                    i += 1
                cost = float(cost)
            if cost != -1.0:
                min_cost_list.insert(0, (cost, provider))

        min_cost_entry = min(min_cost_list)
        i = 0
        while True:
            if min_cost_entry[1][i:i+4] == '.dat':
                break
            i += 1
        min_cost_entry = (min_cost_entry[0], min_cost_entry[1][0:i])

        result[sbc] = min_cost_entry

    return result

def getFilter():
    result = {} # the dictionary where the key is a 3 digit string and the value is the only phone number containing it
    file = open(DataPath + '/phones.dat', 'r')
    file_str = file.read()

    phone_num_list = []
    i = 0
    while i < len(file_str):
        if file_str[i] == '(':
            phone_num_list.insert(0, file_str[i+1:i+4] + file_str[i+6:i+9] + file_str[i+10:i+14])
        i += 1

    valid_num = ''

    for i in range(1000):
        count = 0
        if i < 10:
            j = '0' + '0' + str(i)
        elif i < 100:
            j = '0' + str(i)
        else:
            j = str(i)
        for number in phone_num_list:
            if j in number:
                valid_num = number
                count += 1
        if count == 1:
            result[str(j)] = '(' + valid_num[0:3] + ')' + ' ' + valid_num[3:6] + '-' + valid_num[6:10]

    return result

#print(getDifference('provider2', 'provider4'))
#print(getPriceOf('Rasp. Pi-4710HQ', 'provider2'))
#print(checkAllPrices(set(['Rasp. Pi-4710HQ', 'Rasp. Pi-6700', 'Rasp. Pi-6700TE'])))
#print(getFilter())
