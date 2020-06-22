#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       1/11/2019
#######################################################

import os
import math

# Module level Variables.
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Prelab01')

def find(pattern):
    sequence_file = os.path.join(DataPath, 'sequence.txt')
    f = open(sequence_file, 'r')
    sequence = f.read() # this variable has the entire file in it

    result = []

    for seq_num in range(len(sequence) - len(pattern) + 1):
        check_pattern = True
        for pat_num in range(len(pattern)):
            if pattern[pat_num] != 'X':
                if pattern[pat_num] != sequence[seq_num + pat_num]:
                    check_pattern = False
                    break
        if check_pattern == True:
            result.insert(0, sequence[seq_num: (seq_num+len(pattern)) ])
    f.close()
    return result
    # use list.insert(0, "hello") to add "hello" to the beginning of the list

def getStreakProduct(sequence, maxSize, product):
    result = []
    for seq_num in range(len(sequence) - 1):
        for total_digit_count in range(2, maxSize + 1):
            if seq_num + total_digit_count > len(sequence):
                break
            product_check = int(sequence[seq_num])
            curr_digit_count = 1
            while curr_digit_count < total_digit_count and product_check <= product:
                product_check *= int(sequence[seq_num + curr_digit_count])
                curr_digit_count += 1
            if(product_check == product):
                result.insert(0, sequence[seq_num: (seq_num + total_digit_count) ])

    return result

def writePyramids(filePath, baseSize, count, char):
    f = open(filePath, "w")
    pyramid_layers = []
    temp_string = ""

    total_char_added = baseSize
    spaces_added = 0
    while total_char_added > 0:
        for spaces in range(spaces_added):
            temp_string += ' '
        for chars in range(total_char_added):
            temp_string += char
        for spaces in range(spaces_added):
            temp_string += ' '

        pyramid_layers.insert(0, temp_string)
        temp_string = ""

        total_char_added -= 2
        spaces_added += 1

    for num_rows in range(len(pyramid_layers)):
        for num_pyramids in range(count):
            f.write(pyramid_layers[num_rows])
            if num_pyramids != count - 1:
                f.write(' ')
        f.write('\n')
    f.close()

def getStreaks(sequence, letters):
    result = []
    in_a_streak = False
    streak_count = 0
    curr_letter = '\0' # initialization is meaningless
    for element in range(len(sequence)): # each letter listed
        if in_a_streak == True and sequence[element] == curr_letter:
            result[streak_count] += curr_letter
        else:
            if in_a_streak == True:
                streak_count += 1
            in_a_streak = False
            for letter in range(len(letters)): # each letter in the sequence
                if letters[letter] == sequence[element]:
                    if in_a_streak == False:
                        result.insert(len(result), letters[letter])
                    else:
                        result[streak_count] += letters[letter]
                    in_a_streak = True
                    curr_letter = letters[letter]
                    break

    return result

def findNames(nameList, part, name):
    result = []
    if part != "F":
        if part != "L":
            if part != "FL":
                return result


    for some_name in range(len(nameList)): # every name in the list
        if part != "L":  # first name comparison
            valid_name = True
            for letter in range(len(name)): # every letter in the comparison name'
                if nameList[some_name][letter] != name[letter] and ord(nameList[some_name][letter]) + 32 != ord(name[letter]) and ord(nameList[some_name][letter]) != ord(name[letter]) + 32:
                    valid_name = False
                    break
            if valid_name == True:
                result.insert(len(result), nameList[some_name])
        if part != "F": # last name comparison
            valid_name = True
            space_loc = 0
            while(nameList[some_name][space_loc] != " "):
                space_loc += 1
            space_loc += 1
            for letter in range(len(name)):
                if nameList[some_name][letter + space_loc] != name[letter] and ord(nameList[some_name][letter + space_loc]) + 32 != ord(name[letter]) and ord(nameList[some_name][letter + space_loc]) != ord(name[letter]) + 32:
                    valid_name = False
                    break
            if valid_name == True:
                result.insert(len(result), nameList[some_name])

    return result

def convertToBoolean(num, size):
    result = []
    if isinstance(num, str) or isinstance(size, str):
        return result
    if (str(size)).isdigit() == False or (str(num)).isdigit() == False:
        return result

    size_decrement = size
    if num != 0:
        required_bits = math.floor(math.log(num, 2) + 1)
    else:
        required_bits = 1

    digit_value = num
    while(required_bits > 0 or size_decrement > 0):
        bit = digit_value % 2
        if bit == 1:
            result.insert(0, True)
        else:
            result.insert(0, False)
        required_bits -= 1
        size_decrement -= 1
        digit_value = math.floor(digit_value/2)

    return result

def convertToInteger(boolList):
    if isinstance(boolList, list) == False:
        return None
    if len(boolList) == 0:
        return None
    for element in range(len(boolList)):
        if isinstance(boolList[element], bool) == False:
            return None

    result = 0
    bit = len(boolList) - 1
    added_value = 1
    for element in range(len(boolList)):
        if boolList[bit] == True:
            result += added_value
        bit -= 1
        added_value *= 2

    return result