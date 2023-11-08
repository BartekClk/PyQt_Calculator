import sys
import re
import json
import math
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QFormLayout, QMessageBox, QCheckBox, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QIcon
from pathlib import Path

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kalkulator")
        self.setFixedSize(350,400)
            
        appIcon = QIcon("./icons/icon.png")
        self.setWindowIcon(appIcon)

        calcHistory = []

        class Display:
            def __init__(self):
                self.obj = QLineEdit()
                self.obj.setReadOnly(True)
                self.obj.setFixedHeight(50)
                self.obj.setStyleSheet("font-size: 30px;")
                self.obj.setAlignment(Qt.AlignmentFlag.AlignRight)
                self.obj.setPlaceholderText("0")
                self.line = ""
                self.lastSign = ""
                self.commaUsed = False

            def calculate(self):
                print(self.line.find("x"))

            def addChar(self, char):

                def add(char):
                    self.line += char
                    self.lastSign = char

                allowAdd = True

                if (char == "/" or char == "x" or char == "-" or char == "+" or char == "²" or char == "√") and (self.lastSign == "²" or self.lastSign == "√"):
                    allowAdd = False
                if (char == "/" or char == "x" or char == "-" or char == "+") and (self.lastSign == "/" or self.lastSign == "x" or self.lastSign == "-" or self.lastSign == "+" or self.lastSign == ","):
                    self.line = self.line[:-1]
                if (char == "²" or char == "√" or char == "/" or char == "x" or char == "-" or char == "+" or char == "0") and self.line == "":
                    allowAdd = False
                if char == ",":
                    if self.lastSign == "" or self.lastSign == "²" or self.lastSign == "√" or self.lastSign == "/" or self.lastSign == "x" or self.lastSign == "-" or self.lastSign == "+":
                        add("0")
                    if self.commaUsed == True:
                        allowAdd = False
                    self.commaUsed = True
                
                
                if char == "C":
                    self.line = ""
                    self.commaUsed = False
                if char == "backspace":
                    allowAdd = False
                    if len(self.line) > 0:
                        if len(self.line) == 1:
                            self.lastSign = ""
                        if self.line[-1] == ",":
                            self.commaUsed = False

                        self.line = self.line[:-1]
                
                if allowAdd == True:
                    add(char)
                self.obj.setText(self.line)

            def getObj(self):
                return self.obj
            
        display = Display()
        self.display = display

        class Button:
            def __init__(self, text, type="def", clicked=None, icon="none", value=None):
                self.text = text
                self.type = type
                self.icon = QIcon(icon)
                self.obj = QPushButton(text)
                self.obj.setFixedHeight(50)
                self.obj.setFixedWidth(80)
                self.obj.setStyleSheet("font-size: 20px;")
                self.obj.setIcon(self.icon)
                self.obj.setIconSize(self.obj.sizeHint())
                if value == None:
                    self.value = text
                else:
                    self.value = value
                if(clicked != None):
                    if type == "Num" or type == "Sign" or type == "LowSign" or type == "backspace":
                        self.obj.clicked.connect(clicked(self))
                    else:
                        self.obj.clicked.connect(clicked)
                if type == "empty":
                    self.obj.setEnabled(False)

            def getObj(self):
                return self.obj
            
            def getType(self):
                return self.type

            def getValue(self):
                return self.value

        self.buttons = [
            {"empty1":Button("",type="empty"), "empty4":Button("",type="empty"), "C":Button("C"), "backspace":Button("", "backspace", self.inputDef, icon="./icons/backspace.png", value="backspace")},
            {"empty2":Button("",type="empty"), "square":Button("x²", "Num", self.inputDef, value="²"), "root":Button("√x", "Num", self.inputDef, value="√"), "divine":Button("/", "Num", self.inputDef)},
            {"7":Button("7", "Num", self.inputDef), "8":Button("8", "Num", self.inputDef), "9":Button("9", "Num", self.inputDef), "multiply":Button("x", "Num", self.inputDef)},
            {"4":Button("4", "Num", self.inputDef), "5":Button("5", "Num", self.inputDef), "6":Button("6", "Num", self.inputDef), "sub":Button("-", "Num", self.inputDef)},
            {"1":Button("1", "Num", self.inputDef), "2":Button("2", "Num", self.inputDef), "3":Button("3", "Num", self.inputDef), "add":Button("+", "Num", self.inputDef)},
            {"empty3":Button("",type="empty"), "0":Button("0", "Num", self.inputDef), "dot":Button(",", "Num", self.inputDef), "equal":Button("=", self.calcualte)}
        ]

        mainLayout = QVBoxLayout()
    
        btLayout = QGridLayout()

        def addButtons():
            row = 0
            col = 0
            for el in self.buttons:
                for e in el:
                    btLayout.addWidget(el[e].getObj(), row, col)
                    col += 1
                    if col == 4:
                        col = 0
                row += 1
        addButtons()

        mainLayout.addWidget(display.getObj())
        mainLayout.addLayout(btLayout)
        self.setLayout(mainLayout)

    def inputDef(self, button):
        def addValue():
            self.display.addChar(button.getValue())
        return addValue
    
    def calcualte(self):
        def findCalcReplace(toFind, string):
            signPlace = string.find(toFind)
            if signPlace != -1:
                pass #TODO
            




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()