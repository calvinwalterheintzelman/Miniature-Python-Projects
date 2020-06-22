#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       4/17/2019
#######################################################

import os
import sys
from enum import Enum
from math import *
import copy
import re

# Module Level Variable
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Lab14')

def calculateDistance(zip1, zip2):
    """
    Calculates the distance between two zip codes and returns the result as a float in miles.
    :param zip1: A tuple holding the (latitude, longitude) values of the first zip code.
    :param zip2: A tuple holding the (latitude, longitude) values of the second zip code.
    :return: The distance between the two zip codes in miles.
    :raise: A ValueError if either of the zip codes is not a 2-tuple of floats.
    """

    if not isinstance(zip1, tuple) or not isinstance(zip2, tuple) or len(zip1) != 2 or len(zip2) != 2:
        raise ValueError("One or more input argument does not follow the right format.")

    lat_A, long_A, lat_B, long_B = [radians(v) for v in zip1 + zip2]
    distance = sin(lat_A) * sin(lat_B) + cos(lat_A) * cos(lat_B) * cos(long_A - long_B)

    distance = (degrees(acos(distance))) * 69.09

    return distance


class Direction(Enum):
    Incoming = "Incoming"
    Outgoing = "Outgoing"
    Both = "Both"

class Leg:
    def __init__(self, source, destination):
        self.source = source
        self.destination =destination

    def __str__(self):
        return f"{self.source[len(self.source)-5: len(self.source) ]} => {self.destination[len(self.destination)-5: len(self.destination) ]}"

    def calculateLength(self, locationMap):
        zip1 = self.source[len(self.source)-5: len(self.source) ]
        zip2 = self.destination[len(self.destination)-5: len(self.destination) ]
        return calculateDistance(locationMap[zip1], locationMap[zip2])

class Trip:
    def __init__(self, person, legs):
        self.person = person
        self.legs = legs

    def calculateLength(self, locationMap):
        sum = 0.0
        for leg in self.legs:
            sum += leg.calculateLength(locationMap)
        return sum

    def getLegsByZip(self, zip, dir):
        res = []
        for leg in self.legs:
            if dir.name == "Incoming" and zip in leg.destination:
                res.append(leg)
            elif dir.name == "Outgoing" and zip in leg.source:
                res.append(leg)
            elif dir.name == "Both" and (zip in leg.destination or zip in leg.source):
                res.append(leg)
        return res

    def getLegsByState(self, abr, dir):
        res = []
        for leg in self.legs:
            if dir.name == "Incoming" and abr in leg.destination:
                res.append(leg)
            elif dir.name == "Outgoing" and abr in leg.source:
                res.append(leg)
            elif dir.name == "Both" and (abr in leg.destination or abr in leg.source):
                res.append(leg)
        return res

    def __add__(self, other):
        if not(isinstance(other, Leg) or isinstance(other, Trip)):
            raise TypeError("Only add Trip to Trip or Leg to Trip")
        if isinstance(other, Leg):
            if self.legs[len(self.legs)-1].destination != other.source:
                raise ValueError("Source and destinations don't match")
            leg_copy = self.legs.copy()
            leg_copy.append(other)
            return Trip(self.person, leg_copy)
        if self.person != other.person:
            raise ValueError("Only add trips of same people")
        leg1_copy = self.legs.copy()
        leg2_copy = other.legs.copy()
        return Trip(self.person, leg1_copy + leg2_copy)

    def __radd__(self, other):
        self.__add__(other)

class RoundTrip(Trip):
    def __init__(self, person, legs):
        if not(len(legs) >= 2 and legs[0].source == legs[len(legs)-1].destination):
            raise ValueError("Not round trip")
        super().__init__(person, legs)

def getLatLong(addr):
    zip = addr[len(addr)-5: len(addr)]
    file = open(DataPath + '/locations.dat', 'r')
    line = file.readline()
    while line != "":
        if zip == line[1:6]:
            l_split = line.split('"')
            return (float(l_split[5]), float(l_split[7]))
        line = file.readline()
    file.close()
    return ()

def getShortestTrip(source, destination, stops):
    loc_s = getLatLong(source)
    loc_d = getLatLong(destination)
    stop_dist = 999999999999999999999999999999999999999999
    result = []
    for stop in stops:
        loc_stop = getLatLong(stop)
        dist = calculateDistance(loc_s, loc_stop) + calculateDistance(loc_stop, loc_d)
        if dist < stop_dist:
            stop_dist = dist
            result.append(Trip("", [Leg(source, stop), Leg(stop, destination)]))

    return result[len(result)-1]


def getTotalDistanceFor(person):
    file = open(DataPath + "/trips.dat")
    f_str = file.read()
    file.close()
    if not(person in f_str):
        raise ValueError("Person not in file")

    person_trips = re.findall(person + ".*\n", f_str)
    distance = 0.00000000000000000000000000000000000000000000000000000000
    for trip in person_trips:
        zips = re.findall("\d{5}", trip)
        loc = []
        for z in zips:
            loc.append(getLatLong(z))
        for i in range(len(loc) - 1):
            distance += calculateDistance(loc[i], loc[i+1])
    return round(distance, 2)

def getRoundTripCount():
    file = open(DataPath + "/trips.dat")
    line = file.readline()
    result = 0
    while line != '':
        split_list = line.split(':')[1].split(",")
        z1 = split_list[1]
        z2 = split_list[len(split_list)-1]
        z1 = z1[len(z1) - 6: len(z1) - 1]
        z2 = z2[len(z2) - 7: len(z2) - 2]
        if z1 == z2:
            result += 1
        line = file.readline()
    return result

def getClosestIn(sourceState, destinationState):
    file = open(DataPath + "/locations.dat")
    line = file.readline()
    s_zips = []
    d_zips = []
    while line != "":
        if sourceState == line[10:12]:
            s_zips.append(line[1:6])
        if destinationState == line[10:12]:
            d_zips.append(line[1:6])
        line = file.readline()
    file.close()
    shortest = 999999999999999999999999999999999999999999

    result = ()

    for s in s_zips:
        for d in d_zips:
            c = calculateDistance(getLatLong(s), getLatLong(d))
            if c < shortest:
                result = (s, d)
                shortest = c
    return result
