#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       1/18/2019
#######################################################

import os
import sys

# Module level Variables.
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Prelab02')

def getMaxDifference(symbol):
    filename = DataPath + "/" + symbol + ".dat"
    try:
        file = open(filename, 'r')
    except FileNotFoundError:
        return None

    file.readline()
    file.readline() # skips first two irrelevant lines
    file_str = file.read()
    file.close()

    largest_dif = 0
    result = ""
    date = ""
    high = ""
    low = ""
    date_high_low = 0 # 0 when looking for date, 1 for high, 2 for low
    comma_count = 0

    for i in range(len(file_str)):
        if date_high_low == 0:
            if file_str[i] != ',':
                date += file_str[i]
            else:
                date_high_low = 1
        elif date_high_low == 1:
            if comma_count != 3 and file_str[i] == ',':
                comma_count += 1
            elif comma_count == 3:
                if file_str[i] == ',':
                    comma_count = 0
                    date_high_low = 2
                else:
                    high += file_str[i]
        else:
            if file_str[i] != '\n':
                low += file_str[i]
            else:
                if float(high) - float(low) > largest_dif:
                    largest_dif = float(high) - float(low)
                    result = date
                date_high_low = 0
                date = ""
                high = ""
                low = ""

    return result

def getGainPercent(symbol):
    filename = DataPath + "/" + symbol + ".dat"
    try:
        file = open(filename, 'r')
    except FileNotFoundError:
        return None

    file.readline()
    file.readline() # skips first two irrelevant lines
    file_str = file.read()
    file.close()

    comma_count = 0 # used to find
    close = ''
    opening = ''
    day_total = 0
    close_higher_than_open = 0

    for i in range(len(file_str)):
        if comma_count == 0 and file_str[i] == ',':
            comma_count += 1
        elif comma_count == 1:
            if file_str[i] != ',':
                close += file_str[i]
            else:
                comma_count += 1
        elif comma_count == 2 and file_str[i] == ',':
            comma_count += 1
        elif comma_count == 3:
            if file_str[i] != ',':
                opening += file_str[i]
            else:
                comma_count += 1
        elif comma_count == 4 and file_str[i] == '\n':
            if float(close) > float(opening):
                close_higher_than_open += 1
            comma_count = 0
            day_total += 1
            close = ''
            opening = ''

    return round(close_higher_than_open/day_total*100, 4)

def getVolumeSum(symbol, date1, date2):
    filename = DataPath + "/" + symbol + ".dat"
    try:
        file = open(filename, 'r')
    except FileNotFoundError:
        return None

    file.readline()
    file.readline() # skips first two irrelevant lines
    file_str = file.read()
    file.close()

    year1 = int(date1[0:4])
    year2 = int(date2[0:4])
    month1 = int(date1[5:7])
    month2 = int(date2[5:7])
    day1 = int(date1[8:10])
    day2 = int(date2[8:10])

    if year1 >= year2:
        if year1 == year2:
            if month1 >= month2:
                if month1 == month2:
                    if day1 >= day2:
                        return None
                else:
                    return None
        else:
            return None

    vol_str = ''
    trans_sum = 0
    comma_count = -1 # -1 means it's not counting
    last_one = False

    for i in range(len(file_str)):
        if comma_count == -1:
            if file_str[i:i+len(date2)] == date2:
                comma_count += 1
        elif comma_count == 0 or comma_count == 1:
            if file_str[i:i+len(date1)] == date1:
                last_one = True
            if file_str[i] == ',':
                comma_count += 1
        elif comma_count == 2:
            if file_str[i] != ',':
                vol_str += file_str[i]
            else:
                trans_sum += float(vol_str)
                comma_count = 3
                vol_str = ''
                if last_one == True:
                    break
        elif comma_count == 3 and file_str[i] == '\n':
            comma_count = 0

    return int(round(trans_sum))

def getBestGain(date):
    file_list = os.listdir(DataPath)
    gain = 0

    for f in file_list:
        file = open(DataPath + '/' + f, 'r')
        file_str = file.read()
        file.close()
        correct_line = False
        comma_count = 0
        closing = ''
        opening = ''

        for i in range(len(file_str)):
            if file_str[i:i+len(date)] == date:
                correct_line = True
            elif correct_line == True and comma_count == 0 and file_str[i] == ',':
                comma_count = 1
            elif comma_count == 1:
                if file_str[i] != ',':
                    closing += file_str[i]
                else:
                    comma_count = 2
            elif comma_count == 2 and file_str[i] == ',':
                comma_count = 3
            elif comma_count == 3:
                if file_str[i] != ',':
                    opening += file_str[i]
                else:
                    potential_gain = (float(closing) - float(opening)) / float(opening) * 100.0
                    if potential_gain > gain:
                        gain = potential_gain
                    break

    return round(gain, 4)

def getAveragePrice(symbol, year):
    filename = DataPath + "/" + symbol + ".dat"
    try:
        file = open(filename, 'r')
    except FileNotFoundError:
        return None

    file_str = file.read()
    file.close()
    closing = ''
    opening = ''

    daily_ave = []

    for i in range(len(file_str)):
        if file_str[i:i+5] == '\n' + str(year):
            # find value of close and open
            j = i + 12
            while file_str[j] != ',':
                closing += file_str[j]
                j += 1
            j += 1
            while file_str[j] != ',':
                j += 1
            j += 1
            while file_str[j] != ',':
                opening += file_str[j]
                j+= 1
            daily_ave.insert(0, round((float(closing) + float(opening)) / 2.0, 4))
        closing = ''
        opening = ''

    return round(sum(daily_ave)/len(daily_ave), 4)

def getCountOver(symbol, price):
    filename = DataPath + "/" + symbol + ".dat"
    try:
        file = open(filename, 'r')
    except FileNotFoundError:
        return None

    file.readline() # skips first irrelevant lines
    file_str = file.read()
    file.close()

    closing = ''
    volume = ''
    opening = ''
    high = ''
    low = ''
    total_days = 0

    for i in range(len(file_str)):
        if file_str[i:i+2] == '\n2':
            j = i+12
            while file_str[j] != ',':
                closing += file_str[j]
                j += 1
            if float(closing) >= price:
                j += 1
                while file_str[j] != ',':
                    volume += file_str[j]
                    j += 1
                if float(volume) >= price:
                    j += 1
                    while file_str[j] != ',':
                        opening += file_str[j]
                        j += 1
                    if float(opening) >= price:
                        j += 1
                        while file_str[j] != ',':
                            high += file_str[j]
                            j += 1
                        if float(high) >= price:
                            j += 1
                            while file_str[j] != '\n':
                                low += file_str[j]
                                j += 1
                            if float(low) >= price:
                                total_days += 1

        closing = ''
        volume = ''
        opening = ''
        high = ''
        low = ''

    return total_days
