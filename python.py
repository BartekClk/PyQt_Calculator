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

            def addChar(self, char):
                allowAdd = True

                if (char == "/" or char == "x" or char == "-" or char == "+" or char == "²" or char == "√") and (self.lastSign == "²" or self.lastSign == "√"):
                    allowAdd = False
                if (char == "/" or char == "x" or char == "-" or char == "+") and (self.lastSign == "/" or self.lastSign == "x" or self.lastSign == "-" or self.lastSign == "+" or self.lastSign == ","):
                    self.line = self.line[:-1]
                if (char == "²" or char == "√" or char == "/" or char == "x" or char == "-" or char == "+" or char == "0") and self.line == "":
                    allowAdd = False
                if char == ",":
                    if self.commaUsed == True:
                        allowAdd = False
                    self.commaUsed = True
                if allowAdd == True:
                    self.line += char
                    self.lastSign = char
                if char == "C":
                    self.line = ""
                    self.commaUsed = False
                if char == "backspace":
                    if self.line[-1] == ",":
                        self.commaUsed = False
                    self.line = self.line[:-1]
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
                    if type == "Num" or type == "Sign" or type == "LowSign":
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
            {"empty1":Button("",type="empty"), "empty4":Button("",type="empty"), "C":Button("C"), "backspace":Button("", icon="./icons/backspace.png")},
            {"empty2":Button("",type="empty"), "square":Button("x²", "Num", self.inputNumber, value="²"), "root":Button("√x", "Num", self.inputNumber, value="√"), "divine":Button("/", "Num", self.inputNumber)},
            {"7":Button("7", "Num", self.inputNumber), "8":Button("8", "Num", self.inputNumber), "9":Button("9", "Num", self.inputNumber), "multiply":Button("x", "Num", self.inputNumber)},
            {"4":Button("4", "Num", self.inputNumber), "5":Button("5", "Num", self.inputNumber), "6":Button("6", "Num", self.inputNumber), "sub":Button("-", "Num", self.inputNumber)},
            {"1":Button("1", "Num", self.inputNumber), "2":Button("2", "Num", self.inputNumber), "3":Button("3", "Num", self.inputNumber), "add":Button("+", "Num", self.inputNumber)},
            {"empty3":Button("",type="empty"), "0":Button("0", "Num", self.inputNumber), "dot":Button(",", "Num", self.inputNumber), "equal":Button("=")}
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

    def inputNumber(self, button):
        def addValue():
            self.display.addChar(button.getValue())
        return addValue




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()