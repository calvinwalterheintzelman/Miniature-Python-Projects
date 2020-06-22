#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       2/20/2019
#######################################################

import os
import sys
import re

def extractArguments(commandline):
    result = []
    #    switch = re.findall(r"([\\+][a-z]\s+[^\s\\+]\S*)", commandline)
    switch = re.findall(r"([\\+][a-z]\s+(([^\s\\+]\S*)|(\S[^a-z\s]\S*)|(\S{3}\S*)))", commandline)
    for i in range(len(switch)):
        switch[i] = switch[i][0]
    for arguments in switch:
        switch_letter = re.search(r"([a-z])", arguments)[0]
        switch_value = re.search(r"(\S+\Z)", arguments)[0]
        total_switch = (switch_letter, switch_value)
        result.append(total_switch)
    result.sort()
    return result

def extractNumerics(sentence):
    result = []
    numbers = re.findall(r"([+-]?\d\.\d+e[+-]?\d+)|([+-]?\d+\.\d+)|([+-]?\d+)", sentence, re.IGNORECASE)
    for triple in numbers:
        if triple[0] != '':
            result.append(triple[0])
        elif triple[1] != '':
            result.append(triple[1])
        else:
            result.append(triple[2])
    return result
