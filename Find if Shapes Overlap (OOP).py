#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       2/27/2019
#######################################################

import os
import sys
import math

#######################################################

def pointInRect(point, rect):
    if point[0] > rect.lowerLeft[0] and point[0] < rect.upperRight[0]:
        if point[1] > rect.lowerLeft[1] and point[1] < rect.upperRight[1]:
            return True
    return False

class Rectangle:

    def __init__(self, llPoint, urPoint):
        if llPoint[0] >= urPoint[0] or llPoint[1] >= urPoint[1]:
            raise ValueError("Lower left point must be to the left and below upper right point")
        self.lowerLeft = llPoint
        self.upperRight = urPoint

    def isSquare(self):
        if self.upperRight[0] - self.lowerLeft[0] == self.upperRight[1] - self.lowerLeft[1]:
            return True
        else:
            return False

    def intersectsWith(self, rect):
        lowerRight = (rect.upperRight[0], rect.lowerLeft[1])
        upperLeft = (rect.lowerLeft[0], rect.upperRight[1])

        if pointInRect(lowerRight, self):
            return True
        if pointInRect(upperLeft, self):
            return True
        if pointInRect(rect.lowerLeft, self):
            return True
        if pointInRect(rect.upperRight, self):
            return True
        return False

    def __eq__(self, other):
        if not(isinstance(other, Rectangle)):
            raise TypeError("Rectangle objects must be compared to rectangle objects")
        bottom_side1 = self.upperRight[0] - self.lowerLeft[0]
        left_side1 = self.upperRight[1] - self.lowerLeft[1]
        area1 = bottom_side1*left_side1
        bottom_side2 = other.upperRight[0] - other.lowerLeft[0]
        left_side2 = other.upperRight[1] - other.lowerLeft[1]
        area2 = bottom_side2*left_side2
        if area1 == area2:
            return True
        else:
            return False

class Circle:

    def __init__(self, center, radius):
        if radius <= 0.0:
            raise ValueError("Radius must be greater than 0")
        self.center = center
        self.radius = radius

    def intersectsWith(self, other):
        if not(isinstance(other, Rectangle) or isinstance(other, Circle)):
            raise TypeError("Argument must be a Circle or Rectangle")

        if isinstance(other, Circle):
            center_distance = math.sqrt((self.center[0] - other.center[0]) ** 2 +
                                        (self.center[1] - other.center[1]) ** 2)
            if center_distance < self.radius + other.radius:
                return True
            else:
                return False

        if isinstance(other, Rectangle):
            if self.center[0] - self.radius > other.lowerLeft[0]:
                if self.center[0] + self.radius < other.upperRight[0]:
                    if self.center[1] + self.radius < other.upperRight[1]:
                        if self.center[1] - self.radius > other.lowerLeft[1]:
                            return True

            # check all 4 corners
            dist1 = math.sqrt((self.center[0] - other.lowerLeft[0])**2 + (self.center[1] - other.lowerLeft[1])**2)
            dist2 = math.sqrt((self.center[0] - other.lowerLeft[0])**2 + (self.center[1] - other.upperRight[1])**2)
            dist3 = math.sqrt((self.center[0] - other.upperRight[0])**2 + (self.center[1] - other.lowerLeft[1])**2)
            dist4 = math.sqrt((self.center[0] - other.upperRight[0])**2 + (self.center[1] - other.upperRight[1])**2)
            if dist1 < self.radius or dist2 < self.radius or dist3 < self.radius or dist4 < self.radius:
                return True

            return False
