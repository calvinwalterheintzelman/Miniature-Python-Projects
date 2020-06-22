#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       3/6/2019
#######################################################

import os
import sys
from functools import total_ordering

#######################################################

@total_ordering
class TimeSpan:

    def __init__(self, weeks, days, hours):
        if weeks < 0 or days < 0 or hours < 0:
            raise ValueError("The arguments cannot be negative")

        self.hours = hours % 24
        self.days = (days + (hours // 24)) % 7
        self.weeks = weeks + (days + (hours // 24)) // 7

    def __str__(self):
        return f"{self.weeks:02d} {self.days:01d} {self.hours:02d}"

    def getTotalHours(self):
        return self.weeks * (7 * 24) + self.days * 24 + self.hours

    def __add__(self, other):
        if not(isinstance(other, TimeSpan)):
            raise TypeError("Only add a TimeSpan to a TimeSpan!")
        return TimeSpan(self.weeks + other.weeks, self.days + other.days, self.hours + other.hours)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if not(isinstance(other, int)) and not(isinstance(other, float)):
            raise TypeError("Only multiply a TimeSpan by an int or float!")

        if isinstance(other, int):
            if other <= 0:
                raise ValueError("Only multiply a TimeSpan by an int if the int is positive!")
            return TimeSpan(self.weeks * other, self.days * other, self.hours * other)

        if isinstance(other, float):
            if other <= 0.0:
                raise ValueError("Only multiply a TimeSpan by a float if the float is positive!")
            total_hours = round(self.getTotalHours() * other)
            new_weeks = total_hours // (24 * 7)
            total_hours %= 24 * 7
            new_days = total_hours // 24
            new_hours = total_hours % 24
            return TimeSpan(new_weeks, new_days, new_hours)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        if not(isinstance(other, TimeSpan)):
            raise TypeError("Only compare a TimeSpan to a TimeSpan!")
        return self.getTotalHours() == other.getTotalHours()

    def __lt__(self, other):
        if not(isinstance(other, TimeSpan)):
            raise TypeError("Only compare a TimeSpan to a TimeSpan!")
        return self.getTotalHours() < other.getTotalHours()
