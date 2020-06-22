#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       2/27/2019
#######################################################

import os
import sys
import math
import copy
from functools import total_ordering
import collections
from enum import Enum

#######################################################

@total_ordering
class Datum:

    def __init__(self, *args):
        storage = []
        for arg in args:
            if not(isinstance(arg, float)):
                raise TypeError("arguments must only be floats")
            storage.append(arg) # do something to add arg to this tuple, Calvin
        self._storage = tuple(storage)

    def __str__(self):
        str_list = '('
        for thing in self._storage:
            str_list += f"{thing:.02f}, "
        str_list = str_list[0:len(str_list) - 2]
        str_list += ')'
        return str_list

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self._storage)

    def distanceFrom(self, datum):
        if not(isinstance(datum, Datum)):
            raise TypeError("argument must be of type Datum")
        len1 = len(self._storage)
        len2 = len(datum._storage)
        big = max(len1, len2)
        distance = 0.0
        for i in range(big):
            value1 = 0.0
            if i < len1:
                value1 += self._storage[i]
            value2 = 0.0
            if i < len2:
                value2 += datum._storage[i]
            distance += (value1 - value2) ** 2
        return math.sqrt(distance)

    def clone(self):
        return copy.deepcopy(self)

    def __contains__(self, item):
        if not(isinstance(item, float)):
            raise TypeError("You idiot use a float")
        for thing in self._storage:
            if thing == item:
                return True
        return False

    def __len__(self):
        return len(self._storage)

    def __iter__(self):
        return iter(self._storage)

    def __neg__(self):
        neg_list = []
        for thing in range(len(self._storage)):
            neg_list.append(self._storage[thing] * -1.0)
        return Datum(*neg_list)

    def __getitem__(self, item):
        return self._storage[item]

    def __add__(self, other):
        if not(isinstance(other, Datum)) and not(isinstance(other, float)):
            raise TypeError("You're so stupid you can only add Datum or floats to Datum")
        if isinstance(other, Datum):
            len1 = len(self._storage)
            len2 = len(other._storage)
            big = max(len1, len2)
            sum_list = []
            for i in range(big):
                Sum = 0.0
                if i < len1:
                    Sum += self._storage[i]
                if i < len2:
                    Sum += other._storage[i]
                sum_list.append(Sum)
            return Datum(*sum_list)
        if isinstance(other, float):
            sum_list = []
            for i in range(len(self._storage)):
                sum_list.append(self._storage[i] + other)
            return Datum(*sum_list)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if not(isinstance(other, Datum)) and not(isinstance(other, float)):
            raise TypeError("You're so stupid you can only add Datum or floats to Datum")
        if isinstance(other, Datum):
            len1 = len(self._storage)
            len2 = len(other._storage)
            big = max(len1, len2)
            dif_list = []
            for i in range(big):
                if i < len1:
                    dif = self._storage[i]
                else:
                    dif = 0
                if i < len2:
                    dif -= other._storage[i]
                dif_list.append(dif)
            return Datum(*dif_list)

        if isinstance(other, float):
            dif_list = []
            for i in range(len(self._storage)):
                dif_list.append(self._storage[i] - other)
            return Datum(*dif_list)

    def __mul__(self, other):
        if not(isinstance(other, float)):
            raise TypeError("You idiot use a float")
        mul_list = []
        for i in range(len(self._storage)):
            mul_list.append(self._storage[i] * other)
        return Datum(*mul_list)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not(isinstance(other, float)):
            raise TypeError("You idiot use a float")
        div_list = []
        for i in range(len(self._storage)):
            div_list.append(self._storage[i] / other)
        return Datum(*div_list)

    def __eq__(self, other):
        if not(isinstance(other, Datum)):
            raise TypeError("Compare it to a Datum you Dunderbutt!!!")
        if self.distanceFrom(Datum()) == other.distanceFrom(Datum()):
            return True
        return False

    def __lt__(self, other):
        if not(isinstance(other, Datum)):
            raise TypeError("Compare it to a Datum you Dunderbutt!!!")
        if self.distanceFrom(Datum()) < other.distanceFrom(Datum()):
            return True
        return False

class Data(collections.UserList):

    def __init__(self, initial=None):
        if initial == None:
            super().__init__([])
        else:
            for thing in initial:
                if not(isinstance(thing, Datum)):
                    raise TypeError("You stupid idiot you have to put Datum in the list")
            super().__init__(initial)

    def computeBounds(self):
        max_len = 0
        for thing in self:
            if len(thing) > max_len:
                max_len = len(thing)
        minDatum = []
        maxDatum = []
        for j in range(len(self)):
            for i in range(max_len):
                if j == 0:
                    if i < len(self[j]):
                        maxDatum.append(self[j][i])
                        minDatum.append(self[j][i])
                    else:
                        maxDatum.append(0.0)
                        minDatum.append(0.0)
                else:
                    if i < len(self[j]):
                        if self[j][i] > maxDatum[i]:
                            maxDatum[i] = self[j][i]
                        else:
                            minDatum[i] = self[j][i]

        return (Datum(*minDatum), Datum(*maxDatum))

    def computeMean(self):
        max_len = 0
        for thing in self:
            if len(thing) > max_len:
                max_len = len(thing)
        tot_datum = len(self)

        mean_list = []
        for j in range(max_len):
            curr_mean = 0.0
            for i in range(len(self)):
                if j < len(self[i]):
                    curr_mean += self[i][j]
            mean_list.append(curr_mean / max_len)

        return Datum(*mean_list)

    def append(self, item):
        if not(isinstance(item, Datum)):
            raise TypeError("*sigh* just use a Datum")
        else:
            super().append(item)

    def count(self, item):
        if not(isinstance(item, Datum)):
            raise TypeError("*sigh* just use a Datum")
        else:
            return super().count(item)

    def index(self, item, *args):
        if not(isinstance(item, Datum)):
            raise TypeError("*sigh* just use a Datum")
        else:
            return super().index(item, *args)

    def insert(self, i, item):
        if not(isinstance(item, Datum)):
            raise TypeError("*sigh* just use a Datum")
        else:
            super().insert(i, item)

    def remove(self, item):
        if not(isinstance(item, Datum)):
            raise TypeError("*sigh* just use a Datum")
        else:
            super().remove(item)

    def __setitem__(self, key, value):
        if not(isinstance(value, Datum)):
            raise TypeError("*sigh* just use a Datum")
        else:
            super().__setitem__(key, value)

    def extend(self, other):
        if not(isinstance(other, Data)):
            raise TypeError("I hate you. Use Data")
        else:
            super().extend(other)

class DataClass(Enum):
    Class1 = 'Class1'
    Class2 = 'Class2'

class DataClassifier:

    def __init__(self, group1, group2):
        if not(isinstance(group1, Data) and isinstance(group2, Data)):
            raise TypeError("Only initialize with Data classes, stupid!")
        if len(group1) == 0 or len(group2) == 0:
            raise ValueError("You need values in your Data, dummy!")
        self._class1 = group1
        self._class2 = group2

    def classify(self, datum):
        if not(isinstance(datum, Datum)):
            raise TypeError("input must piabe Datum, ugly!")

        mean1 = self._class1.computeMean()
        mean2 = self._class2.computeMean()

        dist1 = mean1.distanceFrom(datum)
        dist2 = mean2.distanceFrom(datum)

        if dist1 < dist2:
            return DataClass.Class1.name
        else:
            return DataClass.Class2.name
