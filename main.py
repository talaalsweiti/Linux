# Shahd Abu-Daghash 1191448
# Tala Alsweiti 1191068

import csv
import os
from os import walk
import re
import optparse
import pathlib
from abc import ABC, abstractmethod
from pathlib import Path


# This is an abstract class with all methods needed in the child class (Course )
class abstract(ABC):

    @abstractmethod
    def getNumberOfStudents(self):
        pass

    @abstractmethod
    def setNumberOfStudents(self, enteredNumber):
        pass

    @abstractmethod
    def getAbsenceList(self):
        pass

    @abstractmethod
    def addToAbsenceList(self, key, value):
        pass

    @abstractmethod
    def getChatList(self):
        pass

    @abstractmethod
    def addToChatList(self, key, value):
        pass

    @abstractmethod
    def getStudentList(self):
        pass

    @abstractmethod
    def addToStudentList(self, key, value):
        pass

    @abstractmethod
    def readStudentList(self, path):
        pass

    @abstractmethod
    def validFileName(self, name, zeroForAR):
        pass

    @abstractmethod
    def readCSV(self, path, p=0):
        pass

    @abstractmethod
    def readTXT(self, path, Tb=0, Te=0):
        pass


##################################################################################

# Parent class for all courses
class Course(abstract):
    # A constructor to initialize the properties we used in the class
    def __init__(self):
        self._studentList = {}
        self._numberOfStudents = 0
        self._attendanceList = {}
        self._chatList = {}

    # Setters and getters for the properties
    def getNumberOfStudents(self):
        return self._numberOfStudents

    def setNumberOfStudents(self, enteredNumber):
        self._numberOfStudents = enteredNumber

    def getAbsenceList(self):
        return self._attendanceList

    def addToAbsenceList(self, key, value):
        self._attendanceList[key] = value

    def getChatList(self):
        return self._chatList

    def addToChatList(self, key, value):
        self._chatList[key] = value

    def getStudentList(self):
        return self._studentList

    def addToStudentList(self, key, value):
        self._studentList[key] = value

    # A method to read the student list sheet and store the student's id as a key and their name as a value in a
    # dictionary
    def readStudentList(self, path):
        # Open the student list file
        with open(Path(path)) as studentListFile:
            # Built-in function to read all rows from a csv file
            csv_reader = csv.reader(studentListFile, delimiter=',')
            lineCount = 0
            for studentRecord in csv_reader:
                if lineCount >= 1:
                    self.addToStudentList(studentRecord[0], studentRecord[1])
                    self.setNumberOfStudents(self.getNumberOfStudents() + 1)
                lineCount += 1

    # A method to check if the name of the file is of the right format
    def validFileName(self, nameToCheck, zeroForAR):
        # Split the name into a list to check each part
        nameList = re.split("-", nameToCheck)
        # Normal file consists of 5 parts when splitting the name
        if len(nameList) != 5:
            return False
        passed = 0
        # Generally check for course code and override this function for other names
        if nameList[0] == "CourseCode":
            passed += 1
        # Check if it has a valid date
        if 1 <= int(nameList[1]) <= 12 and 1 <= int(nameList[2]) <= 31 and 1 <= int(nameList[3]) <= 2021:
            passed += 1
        # Check for the right file tail
        if (nameList[4] == "AR" and zeroForAR == 0) or (nameList[4] == "PR" and zeroForAR == 1):
            passed += 1
        if passed != 3:
            return False
        return True

    # A method that reads the csv-AR files
    def readCSV(self, path, p=0):
        # Variable for the output file name
        nameOfASheet = ""
        # List all files in the path directory
        for dirPath, dirNames, filenames in walk(path):
            # Loop through all files
            for CSVFile in filenames:
                # Get the name and the extension of the file and check if it is a valid file name
                # With a csv extension
                nameOfCSVFile, extensionOfCSVFile = os.path.splitext(CSVFile)
                if extensionOfCSVFile != ".csv" or not self.validFileName(nameOfCSVFile, 0):
                    continue
                # Split the file name to get the date and the course name
                nameSegments = nameOfCSVFile.split("-")
                # Store the date of the file
                dateOFFile = nameSegments[1] + "-" + nameSegments[2] + "-" + nameSegments[3]

                # Path and name for the file of non valid data
                nonValidFileName = str(path) + "\\" + str(nameOfCSVFile) + '-NV.csv'
                nameOfASheet = nameSegments[0] + "-AttendanceSheet.csv"

                #  Write the columns names in the file
                with open(nonValidFileName, 'w', encoding='UTF8', newline='') as nonValidFile:
                    writer = csv.writer(nonValidFile)
                    writer.writerow(["Name", "Duration"])

                # Reserve dictionaries for the dates in absence list
                if dateOFFile not in self.getAbsenceList().keys():
                    self.addToAbsenceList(dateOFFile, {})

                # Set all students to absent before reading
                for studentID in self.getStudentList().keys():
                    self.getAbsenceList()[dateOFFile][studentID] = "a"

                # Open the csv file for reading
                with open(CSVFile) as FileToRead:
                    csv_reader = csv.reader(FileToRead, delimiter=',')
                    lineCount = 0
                    for dataLine in csv_reader:
                        if lineCount >= 1:
                            # Store the id of the student if exists
                            IDOfStudent = re.sub("[^0-9]", "", dataLine[0])
                            isNumberCheck = False
                            # Check if the id of the student is in the student list
                            for studentNumber in self.getStudentList().keys():
                                if IDOfStudent == studentNumber:
                                    isNumberCheck = True

                            # Split the username of the student into a list
                            studentNameList = re.sub("[^A-za-z ]_", "", dataLine[0]).lower().split(" ")
                            nameFound = False
                            # Check if the name exists in the student list
                            # if the id is found , dont check the name
                            if isNumberCheck and int(dataLine[1]) >= p:
                                self.getAbsenceList()[dateOFFile][IDOfStudent] = "x"
                                nameFound = True
                            else:
                                for studentIDNumber in self.getStudentList():
                                    numOfMatches = 0
                                    for n in studentNameList:
                                        if n in re.sub("[^A-za-z ]", "",self.getStudentList()[studentIDNumber].lower()):
                                            numOfMatches = numOfMatches + 1
                                    # If the name or the id of the student was found and the time is greater than or
                                    # equal to p Set the student to attendee
                                    if numOfMatches == len(studentNameList) and int(dataLine[1]) >= p:
                                        self.getAbsenceList()[dateOFFile][studentIDNumber] = "x"
                                        nameFound = True
                                    if int(dataLine[1]) < p:
                                        nameFound = False
                            # Store the name in the non valid report if it wasn't found in the student list
                            if not nameFound:
                                with open(nonValidFileName, 'a', encoding='UTF8', newline='') as nonValidFile:
                                    writer = csv.writer(nonValidFile)
                                    writer.writerow(dataLine)

                        lineCount += 1
        # Write the absence list in an output file
        header = ["Student ID", "StudentName"]
        for lectureDate in self.getAbsenceList().keys():
            header.append(lectureDate)
        rowsToAddToFile = []
        for student in self.getStudentList():
            r = [student, self.getStudentList()[student]]
            for dateOFFile in self.getAbsenceList():
                r.append(self.getAbsenceList()[dateOFFile][student])
            rowsToAddToFile.append(r)

        with open(nameOfASheet, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rowsToAddToFile)

    # A method that reads the txt-PR files
    def readTXT(self, path, Tb=0, Te=0):
        # Convert tb and te times to seconds
        TBTime = 60 * Tb
        TETime = 60 * Te
        # Variable for the output file name
        nameOfPSheet = ""
        # List all files in the path directory
        for dirpath, dirnames, filenames in walk(path):
            # Loop through all files
            for file in filenames:
                # Get the name and the extension of the file and check if it is a valid file name
                # With a txt extension
                nameOfTXTFile, extensionOfTXTFile = os.path.splitext(file)
                if extensionOfTXTFile != ".txt" or not self.validFileName(nameOfTXTFile, 1):
                    continue
                # Path and name for the file of non valid data
                nonValidName = str(path) + "\\" + nameOfTXTFile + "-NV.txt"

                # Clear the file
                nonValidFile = open(nonValidName, "w", encoding="utf-8")
                nonValidFile.write("")
                nonValidFile.close()

                # Split the file name to get the date and the course name
                nameSegments = file.split("-")
                # Store the date of the file
                dateOFFile = nameSegments[1] + "-" + nameSegments[2] + "-" + nameSegments[3]
                nameOfPSheet = nameSegments[0] + "-ParticipationSheet.csv"

                # Reserve dictionaries for the dates in chat list
                if dateOFFile not in self.getChatList().keys():
                    self.addToChatList(dateOFFile, {})

                TXTReader = open(file, 'r', encoding='utf-8')
                linesOfTXTFile = TXTReader.readlines()
                TXTReader.close()

                # Calculate the time for the first message and convert it to seconds
                firstMessageList = re.split(":", re.split('From|to| : ', linesOfTXTFile[0])[0])
                firstTime = 3600 * int(firstMessageList[0]) + 60 * int(firstMessageList[1]) + int(firstMessageList[2])

                # Calculate the time for the last message and convert it to seconds
                lastMessageList = re.split(":", re.split('From|to| : ', linesOfTXTFile[len(linesOfTXTFile) - 1])[0])
                lastTime = 3600 * int(lastMessageList[0]) + 60 * int(lastMessageList[1]) + int(lastMessageList[2])

                for messageLine in linesOfTXTFile:
                    messageLineList = re.split('From|to| : ', messageLine)
                    if len(messageLineList) > 2:
                        timeList = re.split(":", re.sub(" ", "", messageLineList[0]))
                        timeOfMessage = 3600 * int(timeList[0]) + 60 * int(timeList[1]) + int(timeList[2])

                        # Check if the time is in the right period
                        if firstTime + TBTime <= timeOfMessage <= lastTime - TETime:
                            # Store the id of the student if exists
                            IDOfStudent = re.sub("[^0-9]", "", messageLineList[1])
                            isNumberCheck = False

                            # Check if the id of the student is in the student list
                            for studentNumber in self.getStudentList().keys():
                                if IDOfStudent == studentNumber:
                                    isNumberCheck = True

                            # Split the username of the student into a list
                            studentNameList = re.sub("[^A-za-z ]_", "", messageLineList[1]).lower().split(" ")
                            nameFound = False
                            # if the id is found , don't check the name
                            if isNumberCheck:
                                if IDOfStudent not in self.getChatList()[dateOFFile].keys():
                                    self.getChatList()[dateOFFile][IDOfStudent] = 1
                                    nameFound = True
                                # If the key is found in the chat list increment the value for it
                                elif IDOfStudent in self.getChatList()[dateOFFile].keys():
                                    self.getChatList()[dateOFFile][IDOfStudent] += 1
                                    nameFound = True

                            else:
                                for studentIDNumber in self.getStudentList():
                                    numOfMatches = 0

                                    # Check if the name exists in the student list
                                    for subName in studentNameList:
                                        if subName in re.sub("[^A-za-z ]", "",
                                                             self.getStudentList()[studentIDNumber].lower()):
                                            numOfMatches = numOfMatches + 1
                                    #  Store the id of the student as a key and set the value of
                                    #  to 1  if the name or the id of was found in the student list
                                    #  and is not sorted yet int the chat list
                                    if numOfMatches == len(studentNameList) and studentIDNumber not in \
                                            self.getChatList()[dateOFFile].keys():
                                        self.getChatList()[dateOFFile][studentIDNumber] = 1
                                        nameFound = True
                                    # If the key is found in the chat list increment the value for it
                                    elif numOfMatches == len(studentNameList):
                                        self.getChatList()[dateOFFile][studentIDNumber] += 1
                                        nameFound = True
                                    elif studentIDNumber not in self.getChatList()[dateOFFile].keys():
                                        self.getChatList()[dateOFFile][studentIDNumber] = 0


                            # Store the name in the non valid report if it wasn't found in the student list
                            if not nameFound:
                                nonValidFile = open(nonValidName, "a", encoding="utf-8")
                                nonValidFile.write(messageLine)
                                nonValidFile.close()
                        else:
                            nonValidFile = open(nonValidName, "a", encoding="utf-8")
                            nonValidFile.write(messageLine)
                            nonValidFile.close()
                            pass
        # Write the participant list in an output file
        header = ["Student ID", "StudentName"]
        for lectureDate in self.getChatList().keys():
            header.append(lectureDate)
        rowsToAddToFile = []
        for student in self.getStudentList():
            row = [student, self.getStudentList()[student]]

            for dateOFFile in self.getChatList():
                if self.getChatList()[dateOFFile]:
                    row.append(self.getChatList()[dateOFFile][student])
            rowsToAddToFile.append(row)
        with open(nameOfPSheet, 'w', encoding='UTF8', newline='') as TXTReader:
            writer = csv.writer(TXTReader)
            writer.writerow(header)
            writer.writerows(rowsToAddToFile)


# Child class from the parent class (Courses)
class ENCS3130(Course):
    def __init__(self):
        super().__init__()

    # An overriding method to check the validation for the course code
    def validFileName(self, nameToCheck, zeroForAR):
        nameList = re.split("-", nameToCheck)
        if len(nameList) != 5:
            return False
        passed = 0
        if nameList[0] == "ENCS3130":
            passed += 1
        if 1 <= int(nameList[1]) <= 12 and 1 <= int(nameList[2]) <= 31 and 1 <= int(nameList[3]) <= 2021:
            passed += 1
        if (nameList[4] == "AR" and zeroForAR == 0) or (nameList[4] == "PR" and zeroForAR == 1):
            passed += 1
        if passed != 3:
            return False
        return True


##############################################################################

def main():
    # Store the current path to use it as a default value for the path parser options
    currentPath = pathlib.Path().absolute()
    parser = optparse.OptionParser(usage=__doc__)

    # pares options
    parser.add_option("-p", "--P", type="int", dest="numOfMinsAttend", default=0,
                      help="Only print students who attended more than P minutes")

    parser.add_option("-b", "--Tb", type="int", dest="numOfMinsChatTb", default=0,
                      help="drop some entries at the beginning of all Meeting Participation Reports")

    parser.add_option("-e", "--Te", type="int", dest="numOfMinsChatTe", default=0,
                      help="Drop some entries at the end of all Meeting Participation Reports")

    parser.add_option("-s", "--studentPath", dest="studentSheetPath", default='ENCS3130-StudentList.csv',
                      help="Path for the student list sheet")

    parser.add_option("-a", "--attendancePath", dest="attendancePath", default=currentPath,
                      help="Path for the students' attendance files")

    parser.add_option("-c", "--chatPath", dest="chatPath", default=currentPath,
                      help="Path for the students' chat files")

    (options, args) = parser.parse_args()
    # Create an object from the ENCS3130 course class
    linux = ENCS3130()
    linux.readStudentList(options.studentSheetPath)
    linux.readCSV(options.attendancePath, options.numOfMinsAttend)
    linux.readTXT(options.chatPath, options.numOfMinsChatTb, options.numOfMinsChatTe)


if __name__ == '__main__':
    main()