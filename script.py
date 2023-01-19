import csv
import sys
from typing import Dict, List

def readFromCSV(fileName) -> List:
    rows = []
    with open(fileName, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        
        # extracting each data row one by one
        for row in csvreader:
            if (len(row) == 0):
                continue
            row = [element.strip() for element in row]
            rows.append(row)

        return rows

def writeToCSV(fileName, data: Dict) -> None:
    with open(fileName, 'w', newline="") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        
        for subject, valueList in data.items():
            timeSlot, room = valueList
            dataToBeWritten = [subject, timeSlot, room]
            # writing the data row
            csvwriter.writerow(dataToBeWritten)

def backtrackingSearch(subjects_comp_or_opt: Dict, timeSlots: Dict, domains: Dict):
    csp = [subjects_comp_or_opt, timeSlots, domains]
    return recursiveBacktracking({}, csp)

def recursiveBacktracking(assignments, csp):

    subjects_comp_or_opt, timeSlots, domains = csp

    # Checking whether current assignment is complete
    if (len(subjects_comp_or_opt) == len(assignments)):
        return assignments

    # An unassigned subject will be assigned to this 'var' variable
    var = ""

    # All available subjects list
    subjectsList = list(subjects_comp_or_opt.keys())

    # Currently assigned subjects list
    assignedSubjectList = list(assignments.keys())
    for subject in subjectsList:
        if subject not in assignedSubjectList:
            var = subject
            break

    value_list = domains[var]

    for value in value_list:
        # Checks whether the current value of the domain is consistent with current assignment
        if isConsistent(var, value, assignments, csp):
            assignments[var] = value 
            result = recursiveBacktracking(assignments, csp)
            if result != False:
                return result
            del assignments[var]
    
    return False

# Returns whether the given subject (newSubject) and the its value (time slot room pair) is consistent with the given assignments
def isConsistent(newSubject, value, assignments, csp):

    # the dictionary which contains each subject type (compulsory or optional)
    subjects_comp_or_opt = csp[0]
    newTimeSlot, newRoom = value

    for currentSubject, currentValueList in assignments.items():
        currentTimeSlot, currentRoom = currentValueList
        
        if currentTimeSlot == newTimeSlot: # 2 subjects are assigned to the same time slot

            if (currentRoom == newRoom):
                return False # Since 2 subjects with same time slot cannot be assigned to the same room

            current_sub_comp_or_opt = subjects_comp_or_opt[currentSubject]
            new_sub_comp_or_opt = subjects_comp_or_opt[newSubject]

            if (current_sub_comp_or_opt == new_sub_comp_or_opt) and (current_sub_comp_or_opt == "c"): 
                return False # Since 2 compulsory subjects cannot be assigned to the same time slot
    return True

# input_file_name = "input.csv"
# output_file_name = "output.csv"
# file names
input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

allRows = readFromCSV(input_file_name)

rooms = allRows.pop(-1)

# A dictionary to save subject as the key and 'c' or 'o' as the value
# 'c' represents compulsory 
# 'o' represents optional   
subjects_comp_or_opt = {}

# A dictionary to save available time slots for each subject
# key is the subject name
# value is the list of available time slots for the particular subject 
timeSlots = {}

# Modelling as a CSP 
# Variables of CSP = subjects
# Domain of variables = list consisting of one time slot and a room. eg: [M1, R3] 
# Constraints:
#       1. A given subjects can be assigned only to one of the possible time slots given for that subject. 
#       2. Two compulsory subjects cannot be in the same time slot (optional subjects may). 
#       3. Two subjects cannot be assigned to the same room if they are assigned 

# A dictionary to save domains of each subject
# Key is the subject name
# Value is the domain (A list of lists - Each inner list consists of one time slot and a room. eg: [M1, R3])
domains = {}
for dataRow in allRows:
    subjects_comp_or_opt[dataRow[0]] = dataRow[1]
    timeSlots[dataRow[0]] = dataRow[2:]

    currentDomain = []
    for i in dataRow[2:]:
        for j in rooms:
            currentDomain.append([i,j])
    domains[dataRow[0]] = currentDomain

result = backtrackingSearch(subjects_comp_or_opt, timeSlots, domains)
print(result)
writeToCSV("output.csv", result)