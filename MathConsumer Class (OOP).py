#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       4/3/2019
#######################################################

# Import PyQt5 classes
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from calculator import *

class Consumer(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(Consumer, self).__init__(parent)
        self.setupUi(self)
        self.btnCalculate.clicked.connect(self.performOperation)

    def performOperation(self):
        calc_results = True
        if not(self.edtNumber1.text().isdigit()):
            try:
                float(self.edtNumber1.text())
            except:
                self.edtResult.setText("E")
                calc_results = False
        if not(self.edtNumber2.text().isdigit()):
            try:
                float(self.edtNumber2.text())
            except:
                self.edtResult.setText("E")
                calc_results = False
        if(calc_results):
            if self.cboOperation.currentText() == "+":
                result = str(float(self.edtNumber1.text()) + float(self.edtNumber2.text()))
                self.edtResult.setText(result)
            elif self.cboOperation.currentText() == "-":
                result = str(float(self.edtNumber1.text()) - float(self.edtNumber2.text()))
                self.edtResult.setText(result)
            elif self.cboOperation.currentText() == "*":
                result = str(float(self.edtNumber1.text()) * float(self.edtNumber2.text()))
                self.edtResult.setText(result)
            elif self.cboOperation.currentText() == "/":
                if float(self.edtNumber2.text()) == 0:
                    self.edtResult.setText("E")
                else:
                    result = str(float(self.edtNumber1.text()) / float(self.edtNumber2.text()))
                    self.edtResult.setText(result)
            else:
                self.edtResult.setText("E")

if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = Consumer()

    currentForm.show()
    currentApp.exec_()

