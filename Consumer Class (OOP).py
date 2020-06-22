
#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       3/28/2019
#######################################################

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from BasicUI import *
import re

class Consumer(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super(Consumer, self).__init__(parent)
        self.setupUi(self)

        self.btnSave.setEnabled(False) # makes save button unusable

        self.names = [self.txtComponentName_1, self.txtComponentName_2, self.txtComponentName_3, self.txtComponentName_4,
                 self.txtComponentName_5, self.txtComponentName_6, self.txtComponentName_7, self.txtComponentName_8,
                 self.txtComponentName_9, self.txtComponentName_10, self.txtComponentName_11, self.txtComponentName_12,
                 self.txtComponentName_13, self.txtComponentName_14, self.txtComponentName_15, self.txtComponentName_16,
                 self.txtComponentName_17, self.txtComponentName_18, self.txtComponentName_19, self.txtComponentName_20]
        self.counts = [self.txtComponentCount_1, self.txtComponentCount_2,
                  self.txtComponentCount_3, self.txtComponentCount_4,
                  self.txtComponentCount_5, self.txtComponentCount_6,
                  self.txtComponentCount_7, self.txtComponentCount_8,
                  self.txtComponentCount_9, self.txtComponentCount_10,
                  self.txtComponentCount_11, self.txtComponentCount_12,
                  self.txtComponentCount_13, self.txtComponentCount_14,
                  self.txtComponentCount_15, self.txtComponentCount_16,
                  self.txtComponentCount_17, self.txtComponentCount_18,
                  self.txtComponentCount_19, self.txtComponentCount_20]
        for name in self.names:
            name.textChanged.connect(self.enableSave)
        for count in self.counts:
            count.textChanged.connect(self.enableSave)
        self.txtStudentID.textChanged.connect(self.enableSave)
        self.txtStudentName.textChanged.connect(self.enableSave)
        self.chkGraduate.stateChanged.connect(self.enableSave)
        self.cboCollege.activated.connect(self.enableSave)

        self.btnClear.clicked.connect(self.clear)

        self.btnSave.clicked.connect(self.save)

        self.btnLoad.clicked.connect(self.loadData)

    def save(self):
        grad = str(self.chkGraduate.isChecked()).lower()
        stud = self.txtStudentName.text()
        studID = self.txtStudentID.text()
        college = self.cboCollege.currentText()
        file = open('target.xml', 'w')
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write('<Content>\n')
        file.write('    <StudentName graduate="' + grad + '">' + stud + '</StudentName>\n')
        file.write('    <StudentID>' + studID + '</StudentID>\n')
        file.write('    <College>' + college + '</College>\n')
        file.write('    <Components>\n')
        for i in range(len(self.names)):
            if self.names[i].text != '' and self.counts[i].text() != '':
                n = self.names[i].text()
                c = self.counts[i].text()
                file.write('        <Component name="' + n + '" count="' + c + '" />\n')
        file.write('    </Components>\n')
        file.write('</Content>')
        file.close()

    def clear(self):
        for name in self.names:
            name.setText("")
        for count in self.counts:
            count.setText("")
        self.txtStudentName.setText("")
        self.txtStudentID.setText("")

        if self.chkGraduate.isChecked():
            self.chkGraduate.toggle()

        self.cboCollege.setCurrentIndex(0)

        self.btnSave.setEnabled(False)
        self.btnLoad.setEnabled(True)

    def enableSave(self, text):
        self.btnSave.setEnabled(True)
        self.btnLoad.setEnabled(False)

        #https://www.tutorialspoint.com/pyqt/pyqt_qpushbutton_widget.htm

    def loadData(self):
        """
        *** DO NOT MODIFY THIS METHOD! ***
        Obtain a file name from a file dialog, and pass it on to the loading method. This is to facilitate automated
        testing. Invoke this method when clicking on the 'load' button.

        You must modify the method below.
        """
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open XML file ...', filter="XML files (*.xml)")

        if not filePath:
            return

        self.loadDataFromFile(filePath)

    def loadDataFromFile(self, filePath):
        """
        Handles the loading of the data from the given file name. This method will be invoked by the 'loadData' method.
        
        *** YOU MUST USE THIS METHOD TO LOAD DATA FILES. ***
        *** This method is required for unit tests! ***
        """
        self.clear()
        file = open(filePath, 'r')
        file.readline()
        file.readline()

        grad_and_name = file.readline()
        grad = re.findall(r'(".*")', grad_and_name)[0]
        name = re.findall(r'(>.*<)', grad_and_name)[0]
        name = name[1:len(name) - 1]
        if grad == '"true"' and not(self.chkGraduate.isChecked()):
            self.chkGraduate.toggle()
        if grad == '"false"' and self.chkGraduate.isChecked():
            self.chkGraduate.toggle()
        self.txtStudentName.setText(name)

        ID_line = file.readline()
        ID = re.findall(r'(>.*<)', ID_line)[0]
        ID = ID[1:len(ID) - 1]
        self.txtStudentID.setText(ID)

        col_line = file.readline()
        col = re.findall(r'(>.*<)', col_line)[0]
        col = col[1:len(col) - 1]
        if col == "Aerospace Engineering":
            i = 1
        elif col == "Civil Engineering":
            i = 2
        elif col == "Computer Engineering":
            i = 3
        elif col == "Electrical Engineering":
            i = 4
        elif col == "Industrial Engineering":
            i = 5
        elif col == "Mechanical Engineering":
            i = 6
        else:
            i = 0
        self.cboCollege.setCurrentIndex(i)

        file.readline()
        line = file.readline()
        num = 0
        while line[0:8] == '        ' and num < 20:
            c_name = re.findall(r'(".*?")', line)[0]
            count = re.findall(r'(".*?")', line)[1]
            c_name = c_name[1:len(c_name) - 1]
            count = count[1:len(count) - 1]
            self.names[num].setText(c_name)
            self.counts[num].setText(count)
            line = file.readline()
            num += 1

        file.close()


if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = Consumer()

    currentForm.show()
    currentApp.exec_()
