#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       1/25/2019
#######################################################

import os
import sys
from collections import Counter

# Module level Variables
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Prelab03')

#1
def getComponentCountByProject(projectID, componentSymbol):
    # remember to only count components once
    circuit_list = getCircuitIDsFromProjects(projectID)
    if len(circuit_list) == 0:
        raise ValueError('Error! The Project name does not exist!')

    components = set([])

    for circuit in circuit_list:
        components = components.union(set(getCircuitComponents(circuit)))

    if componentSymbol == "R":
        file_path = '/maps/resistors.dat'
    elif componentSymbol == "I":
        file_path = '/maps/inductors.dat'
    elif componentSymbol == "C":
        file_path = '/maps/capacitors.dat'
    elif componentSymbol == "T":
        file_path = '/maps/transistors.dat'
    else:
        raise ValueError('Error! Use component symbol "R", "I", "C", or "T"')

    count = countComponents(file_path, components)

    return count

#2
def getComponentCountByStudent(studentName, componentSymbol):
    result = 0
    student_id = getStudentID(studentName)
    if student_id == '':
        raise ValueError('Error! The student name does not exist')
    files = os.listdir(DataPath + '/circuits')
    components_used = set([])
    for file in files:
        components_used = components_used.union(getComponentFromID(student_id, file))

    if componentSymbol == "R":
        file_path = '/maps/resistors.dat'
    elif componentSymbol == "I":
        file_path = '/maps/inductors.dat'
    elif componentSymbol == "C":
        file_path = '/maps/capacitors.dat'
    elif componentSymbol == "T":
        file_path = '/maps/transistors.dat'
    else:
        raise ValueError('Error! Use component symbol "R", "I", "C", or "T"')

    result += countComponents(file_path, components_used)

    return result

#3
def getParticipationByStudent(studentName):
    result = set([])
    student_id = getStudentID(studentName)
    if student_id == '':
        raise ValueError('Error! The student name does not exist')
    files = os.listdir(DataPath + '/circuits')
    circuits = []
    for file in files:
        if getCircuitFromID(student_id, file):
            circuits.insert(0, file[8:15])

    result = result.union(getProjectsFromCircuits(circuits))

    return result

#4
def getParticipationByProject(projectID):
    circuits = getCircuitIDsFromProjects(projectID)
    if len(circuits) == 0:
        raise ValueError('Error! The Project name does not exist!')

    student_ids = set([])
    for circuit in circuits:
        student_ids = student_ids.union(getStudentIDfromCircuit(circuit))

    students = getStudentsFromID(student_ids)

    return students

#5
def getCostOfProjects():
    file = open(DataPath + '/maps/projects.dat', 'r')
    file.readline()
    file.readline()
    file_str = file.read()
    i = 21
    project_id = ''
    project_list = []
    while i < len(file_str): # gets list of projects
        if file_str[i:i + 36] != project_id:
            project_id = file_str[i:i + 36]
            project_list.insert(0, project_id)
        i += 58

    circuits = []
    for project in project_list:
        circuits.insert(0, getCircuitIDsFromProjects(project))

    component_list = []
    for proj_circuit in range(len(circuits)):
        component_list.insert(proj_circuit, [])
        for circuit in range(len(circuits[proj_circuit])):
            component_list[proj_circuit] += getCircuitComponents(circuits[proj_circuit][circuit])

    #component_list[0] has all of project 1's stuff in it
    component_dict = []
    for components in range(len(component_list)):
        component_dict.insert(components, Counter(component_list[components]))

    file = open(DataPath + '/maps/capacitors.dat', 'r')
    file.readline()
    file.readline()
    file.readline()
    cap_str = file.read()
    file.close()

    cap_dict = {}
    i = 0
    while i < len(cap_str):
        cap_dict[cap_str[i:i+7]] = float(cap_str[i+22:i+26])
        i += 27

    file = open(DataPath + '/maps/inductors.dat', 'r')
    file.readline()
    file.readline()
    file.readline()
    ind_str = file.read()
    file.close()

    ind_dict = {}
    i = 0
    while i < len(ind_str):
        ind_dict[ind_str[i:i+7]] = float(ind_str[i+22:i+26])
        i += 27

    file = open(DataPath + '/maps/resistors.dat', 'r')
    file.readline()
    file.readline()
    file.readline()
    res_str = file.read()
    file.close()

    res_dict = {}
    i = 0
    while i < len(res_str):
        res_dict[res_str[i:i+7]] = float(res_str[i+22:i+26])
        i += 27

    file = open(DataPath + '/maps/transistors.dat', 'r')
    file.readline()
    file.readline()
    file.readline()
    trans_str = file.read()
    file.close()

    trans_dict = {}
    i = 0
    while i < len(trans_str):
        trans_dict[trans_str[i:i+7]] = float(trans_str[i+22:i+26])
        i += 27

    cost_dict = {}
    cost_dict.update(cap_dict)
    cost_dict.update(ind_dict)
    cost_dict.update(res_dict)
    cost_dict.update(trans_dict)

    result_dict = {}

    for i in range(len(component_list)):
        cost = 0.0
        for comp in component_list[i]:
            cost += cost_dict[comp]*component_dict[i][comp]
        result_dict[project_list[i]] = round(cost, 2)


    return result_dict

#6
def getProjectByComponent(componentIDs):
    result = set([])
    circuits = set([])
    for component in componentIDs:
        circuits = circuits.union(getCircuitsFromComponent(component))

    for circuit in circuits:
        result = result.union(getProjectsFromCircuits([circuit[8:15]]))

    return result

#7
def getCommonByProject(projectID1, projectID2):
    circuitIDs1 = set(getCircuitIDsFromProjects(projectID1))
    if len(circuitIDs1) == 0:
        raise ValueError('Error! The Project name for project1 does not exist!')
    circuitIDs2 = set(getCircuitIDsFromProjects(projectID2))
    if len(circuitIDs2) == 0:
        raise ValueError('Error! The Project name for project2 does not exist!')

    component_set1 = set([])
    component_set2 = set([])

    for circuit in circuitIDs1:
        component_set1 = component_set1.union(getCircuitComponents(circuit))

    for circuit in circuitIDs2:
        component_set2 = component_set2.union(getCircuitComponents(circuit))

    result_set = component_set1.intersection(component_set2)
    result_list = list(result_set)
    result_list.sort()

    return result_list

#8
def getComponentReport(componentIDs):
    result_dict = {}
    circuits = {}
    for component in componentIDs:
        circuits[component] = list(getCircuitsFromComponent(component))
        result_dict[component] = 0

    file = open(DataPath + '/maps/projects.dat', 'r')
    file.readline()
    file.readline()
    file_str = file.read()

    i = 4
    while i < len(file_str):
        curr_circ = 'circuit_' + file_str[i:i+7] + '.dat'
        for component in componentIDs:
            for circuit in circuits[component]:
                if circuit == curr_circ:
                    result_dict[component] += 1
        i += 58

    return result_dict

#9
def getCircuitByStudent(studentNames):
    circuit_ids = set([])
    id_list = []
    for student in studentNames:
        id_list.insert(0, getStudentID(student))

    files = os.listdir(DataPath + '/circuits')

    for file in files:
        for ID in id_list:
            if getCircuitFromID(ID, file):
                circuit_ids = circuit_ids.union([file[8:15]])

    return circuit_ids

#10
def getCircuitByComponent(componentIDs):
    result = set([])
    for ID in componentIDs:
        result = result.union(getCircuitsFromComponent(ID))

    return result

# part 6 below

def getCircuitsFromComponent(componentID):
    files = os.listdir(DataPath + '/circuits')
    circuits = set([])
    for file in files:
        f = open(DataPath + '/circuits/' + file, 'r')
        file_str = f.read()
        f.close()
        for i in range(len(file_str)):
            if file_str[i:i+len(componentID)] == componentID:
                circuits = circuits.union([file])

    return circuits

# part 4 below

def getStudentsFromID(IDs):
    file = open(DataPath + '/maps/students.dat', 'r')
    file.readline()
    file.readline()
    file_str = file.read()
    file.close()

    students = set([])
    i = 44
    while i < len(file_str):
        for ID in IDs:
            if ID == file_str[i:i+11]:
                name = ''
                j = i - 44
                while file_str[j:j+2] != '  ':
                    name += file_str[j]
                    j += 1
                students = students.union([name])
                break
        i += 56

    return students

def getStudentIDfromCircuit(circuit):
    file = open(DataPath + '/circuits/circuit_' + circuit + '.dat', 'r')
    file_str = file.read()
    file.close()

    result = []
    i = 28
    while file_str[i] != '\n':
        result.insert(0, file_str[i:i+11])
        i += 12

    return set(result)
    # part 3 below

def getProjectsFromCircuits(circuits):
    f = open(DataPath + '/maps/projects.dat')
    file_str = f.read()
    f.close()

    result = []

    for circuit in circuits:
        for i in range(len(file_str)):
            if file_str[i:i+7] == circuit:
                project = file_str[i + 17:i + 53]
                result.insert(0, project)

    return set(result)

def getCircuitFromID(student_id, file):
    f = open(DataPath + '/circuits/' + file)
    file_str = f.read()
    f.close()

    i = 0
    while file_str[i] != 'C':
        if file_str[i:i + len(student_id)] == student_id:
            return True
        i += 1

    return False

# part 2 below

def getComponentFromID(student_id, file):
    f = open(DataPath + '/circuits/' + file)
    file_str = f.read()
    f.close()

    result = set([])
    valid_file = False
    i = 0
    while file_str[i] != 'C':
        if file_str[i:i+len(student_id)] == student_id:
            valid_file = True
        i += 1

    if valid_file:
        result = result.union(set(getCircuitComponents(file[8:15])))

    # getCircuitComponents(circuit)
    return result

def getStudentID(studentName):
    result = ''
    file = open(DataPath + '/maps/students.dat', 'r')
    file_str = file.read()
    file.close()

    for i in range(len(file_str)):
        if file_str[i:i+len(studentName)] == studentName:
            j = i+len(studentName)
            while file_str[j] == '|' or file_str[j] == ' ':
                j += 1
            for k in range(11):
                result += file_str[j]
                j += 1
            break

    return result

# part 1 below
def countComponents(file_path, components):
    result = 0
    file = open(DataPath + file_path, 'r')
    file_str = file.read()
    file.close()
    for component in components:
        for i in range(len(file_str)):
            if file_str[i:i+7] == component:
                result += 1

    return result

def getCircuitComponents(circuit):
    result = []
    file = open(DataPath + '/circuits/circuit_' + circuit + '.dat', 'r')

    char = file.read(1)
    while char != '-':
        char = file.read(1)
    file.readline()
    char = file.read(2)
    while char != '--':
        char = file.read(2)
    file.readline()

    file_str = file.read() + '\n'
    for i in range(len(file_str)//10):
        result.insert(0, file_str[10*i+2:10*i+9])

    file.close()
    return result

def getCircuitIDsFromProjects(projectID):
    result = []
    file = open(DataPath + '/maps/projects.dat', 'r')
    file.readline()
    file.readline() # skips first two irrelevant lines
    file_str = file.read()
    file_str += '\n'

    for i in range(len(file_str)//58):
        line_str = file_str[58*i:58*i + 57]
        if line_str[21:57] == projectID:
            result.insert(0, line_str[4:11])

    file.close()
    return result

#print(getComponentCountByProject('082D6241-40EE-432E-A635-65EA8AA374B6', 'C'))
#print(getComponentCountByStudent('Young, Frank', 'R'))
#print(getParticipationByStudent('Young, Frank'))
#print(getParticipationByProject('D230BAC0-249C-410F-84E4-41F9EDBFCB20'))
#print(getCostOfProjects())
#print(getProjectByComponent(set(['ZHT-034', 'CLQ-971'])))
#print(getCommonByProject('082D6241-40EE-432E-A635-65EA8AA374B6', '90BE0D09-1438-414A-A38B-8309A49C02EF'))
#print(getComponentReport(set(['ZHT-034', 'CLQ-971', 'TAK-481'])))
#print(getCircuitByStudent(set(['Adams, Keith', 'Allen, Amanda', 'Cox, Shirley', 'Young, Frank'])))
#print(getCircuitByComponent(set(['ZHT-034', 'CLQ-971', 'TAK-481'])))
