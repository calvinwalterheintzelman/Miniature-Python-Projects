#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       2/21/2019
#######################################################

import os
import sys
from enum import Enum

class Level(Enum):
    Freshman = 1
    Sophomore = 2
    Junior = 3
    Senior = 4

class ComponentType(Enum):
    Resistor = 1
    Capacitor = 2
    Inductor = 3
    Transistor = 4

class Student:

    def __init__(self, ID, firstName, lastName, level):
        self.ID = ID
        self.firstName = firstName
        self.lastName = lastName
        valid_level = False
        for year in Level:
            if str(level) == str(year.name):
                self.level = level
                valid_level = True
                break
        if valid_level is False:
            raise TypeError('Fourth argument must be from the enum class "Level"')

    def __str__(self):
        return f"{self.ID}, {self.firstName} {self.lastName}, {self.level}"

class Component:

    def __init__(self, ID, ctype, price):
        self.ID = ID
        self.price = price
        valid_c = False
        for part in ComponentType:
            if str(ctype) == str(part.name):
                self.ctype = ctype
                valid_c = True
                break
        if valid_c is False:
            raise TypeError('Second argument must be from the enum class "ComponentType"')

    def __str__(self):
        return f"{self.ctype}, {self.ID}, ${self.price:.2f}"

    def __hash__(self):
        return hash(self.ID)

class Circuit:

    def __init__(self, ID, components):
        self.ID = ID
        self.cost = 0.0
        if not(components == set([])):
            for an_object in components:
                if not(str(type(an_object)) == "<class 'Component'>"):
                    raise TypeError('Second argument must be a set with members of class "Component"')
                self.cost += an_object.price
        self.components = components

    def __str__(self):
        r_total = 0
        c_total = 0
        i_total = 0
        t_total = 0
        for an_object in self.components:
            if an_object.ctype == "Resistor":
                r_total += 1
            elif an_object.ctype == 'Capacitor':
                c_total += 1
            elif an_object.ctype == 'Inductor':
                i_total += 1
            else:
                t_total += 1
        return f"{self.ID}: (R = {r_total:02d}, C = {c_total:02}, I = {i_total:02}, T = {t_total:02}), Cost = ${self.cost:.2f}"

    def getByType(self, ctype_enum):
        valid_ctype = False
        for part in ComponentType:
            if ctype_enum == part.name:
                valid_ctype = True
                break
        if valid_ctype is False:
            raise ValueError('Input is not a "Resistor", "Capacitor", "Inductor", or "Transistor"')
        result = set([])
        for comp in self.components:
            if comp.ctype == ctype_enum:
                result = result.union([comp])
        return result

    def __contains__(self, item):
        if str(type(item)) != "<class 'Component'>":
            raise TypeError("Argument must be a 'Component' object")
        return item in self.components

    def __add__(self, other):
        if str(type(other)) != "<class 'Component'>":
            raise TypeError("Argument must be a 'Component' object")
        if not(other in self.components):
            self.cost += other.price
            self.components = self.components.union([other])
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if str(type(other)) != "<class 'Component'>":
            raise TypeError("Argument must be a 'Component' object")
        if other in self.components:
            self.cost -= other.price
            self.components = self.components.difference([other])
        return self

    def __eq__(self, other):
        if str(type(other)) != "<class 'Circuit'>":
            raise TypeError("Argument must be a 'Circuit' object")
        return self.cost == other.cost

    def __lt__(self, other):
        if str(type(other)) != "<class 'Circuit'>":
            raise TypeError("Argument must be a 'Circuit' object")
        return self.cost < other.cost

    def __gt__(self, other):
        if str(type(other)) != "<class 'Circuit'>":
            raise TypeError("Argument must be a 'Circuit' object")
        return self.cost > other.cost

class Project:

    def __init__(self, ID, participants, circuits):
        self.ID = ID
        for person in participants:
            if str(type(person)) != "<class 'Student'>":
                raise TypeError("Second Argument must be set of 'Student' objects")
        self.participants = participants
        for circuit in circuits:
            if str(type(circuit)) != "<class 'Circuit'>":
                raise TypeError("Third argument must be list of 'Circuit' objects")
        self.circuits = circuits
        self.cost = 0.0
        for circuit in circuits:
            self.cost += circuit.cost

    def __str__(self):
        return f"{self.ID}: ({len(self.circuits):02d} Circuits, {len(self.participants):02d} Participants), Cost = ${self.cost:.02f}"

    def __contains__(self, item):
        if str(type(item)) == "<class 'Component'>":
            for circuit in self.circuits:
                for comp in circuit.components:
                    if comp == item:
                        return True
            return False
        elif str(type(item)) == "<class 'Circuit'>":
            for circuit in self.circuits:
                if circuit.ID == item.ID:
                    return True
            return False
        elif str(type(item)) == "<class 'Student'>":
            for student in self.participants:
                if student.ID == item.ID:
                    return True
            return False
        else:
            raise TypeError("Must check if a 'Component', 'Circuit', or 'Student' is in this Project")

    def __add__(self, other):
        if str(type(other)) != "<class 'Circuit'>":
            raise TypeError("Can only add a Circuit to this Project")
        if not(other in self.circuits):
            self.circuits.append(other)
            self.cost += other.cost
        return self

    def __sub__(self, other):
        if str(type(other)) != "<class 'Circuit'>":
            raise TypeError("Can only add a Circuit to this Project")
        if other in self.circuits:
            self.circuits.remove(other)
            self.cost -= other.cost
        return self

    def __getitem__(self, item):
        for circuit in self.circuits:
            if item == circuit.ID:
                return circuit
        raise KeyError("ID in not any of the Project's circuits")

class Capstone(Project):

    def __init__(self, ID_or_project, participants=0, circuits=0):
        if str(type(ID_or_project)) == "<class 'Project'>":
            for student in ID_or_project.participants:
                if student.level != 'Senior':
                    raise ValueError("All students must be Seniors")
            super().__init__(ID_or_project.ID, ID_or_project.participants, ID_or_project.circuits)
        else:
            if participants == 0 or circuits == 0:
                raise TypeError("There must be a 2nd and 3rd argument if the 1st argument is not a Projects")
            for student in participants:
                if student.level != 'Senior':
                    raise ValueError("All students must be Seniors")
            super().__init__(ID_or_project, participants, circuits)
