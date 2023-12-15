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
                self.calcStack = []
                self.stop = False

            def lineReload(self):
                self.line = ""
                for el in self.calcStack:
                    self.line += el
                self.obj.setText(self.line)

            def addChar(self, char):

                def add(char):
                    if((char.isnumeric() or char == ".") and char != "²"):
                        if(len(self.calcStack)==0 or (self.calcStack[-1][-1].isnumeric() == False and self.calcStack[-1][-1] != ".")):
                            self.calcStack.append(char)
                        elif(self.calcStack[-1][-1].isnumeric() or self.calcStack[-1][-1] == "."):
                            self.calcStack[-1] += char
                        self.lastSign = char
                    if(char == "²" or char == "√" or char == "/" or char == "x" or char == "-" or char == "+"):
                        self.calcStack.append(char)
                        self.commaUsed = False
                        self.lastSign = char
                
                allowAdd = True

                if ((char == "²" or char == "/" or char == "x" or char == "+") and self.lastSign == "√" ):
                    allowAdd = False
                if (char == self.lastSign and char.isnumeric() == False):
                    allowAdd = False
                if (char == "²") and (self.lastSign == "/" or self.lastSign == "x"or self.lastSign == "+"):
                    allowAdd = False
                if (char == "-" and self.lastSign == "√"):
                    allowAdd = False
                if (char.isnumeric() == False and self.lastSign == "."):
                        self.commaUsed = False
                if (char == "/" or char == "x" or char == "+") and (self.lastSign == "/" or self.lastSign == "x" or self.lastSign == "-" or self.lastSign == "+"):
                    if(char != self.lastSign):
                        self.calcStack.pop()
                    if(len(self.calcStack) > 1) and char == self.calcStack[-1]:
                        allowAdd = False
                if (char == "²" or char == "/" or char == "x" or char == "+") and len(self.calcStack)==0:
                    allowAdd = False
                if char.isnumeric() and self.lastSign == "²":
                    add("x")
                    self.lastSign = "x"
                if char == "√" and self.lastSign.isnumeric():
                    add("x")
                    self.lastSign = "x"
                if char == ".":
                    if self.lastSign == "" or self.lastSign == "²" or self.lastSign == "√" or self.lastSign == "/" or self.lastSign == "x" or self.lastSign == "-" or self.lastSign == "+":
                        add("0")
                    if(len(self.calcStack)!=0 and self.calcStack[-1].find(".")!=-1):
                        allowAdd = False
                        self.commaUsed = True
                
                
                
                
                if char == "C":
                    self.calcStack = ""
                    self.commaUsed = False
                if char == "backspace":
                    allowAdd = False
                    if len(self.calcStack) > 0:
                        if len(self.calcStack[-1]) > 1:
                            self.calcStack[-1] = self.calcStack[-1][:-1]
                            self.lastSign = self.calcStack[-1][-1]
                        else:
                            self.calcStack.pop()
                            if len(self.calcStack) == 0:
                                self.lastSign = ""
                            else:
                                if self.calcStack[-1][-1] == ".":
                                    self.commaUsed = False
                    self.lineReload()

                if allowAdd == True:
                    add(char)
                self.lineReload()


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
            {"empty1":Button("",type="empty"), "empty4":Button("",type="empty"), "C":Button("C", "C", self.clear()), "backspace":Button("", "backspace", self.inputDef, icon="./icons/backspace.png", value="backspace")},
            {"empty2":Button("",type="empty"), "square":Button("x²", "Num", self.inputDef, value="²"), "root":Button("√x", "Num", self.inputDef, value="√"), "divine":Button("/", "Num", self.inputDef)},
            {"7":Button("7", "Num", self.inputDef), "8":Button("8", "Num", self.inputDef), "9":Button("9", "Num", self.inputDef), "multiply":Button("x", "Num", self.inputDef)},
            {"4":Button("4", "Num", self.inputDef), "5":Button("5", "Num", self.inputDef), "6":Button("6", "Num", self.inputDef), "sub":Button("-", "Num", self.inputDef)},
            {"1":Button("1", "Num", self.inputDef), "2":Button("2", "Num", self.inputDef), "3":Button("3", "Num", self.inputDef), "add":Button("+", "Num", self.inputDef)},
            {"empty3":Button("",type="empty"), "0":Button("0", "Num", self.inputDef), "dot":Button(",", "Num", self.inputDef, value="."), "equal":Button("=", "equal", self.calcualte)}
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

    def alert(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Błąd")
        msg.setText(text)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        result = msg.exec()

    def inputDef(self, button):
        def addValue():
            self.display.addChar(button.getValue())
        return addValue
    
    def clear(self, hard=True):
        def clear():
            if hard == True: 
                self.display.calcStack.clear()
            self.display.lastSign = ""
            self.display.commaUsed = False
            self.display.lineReload()
        return clear

    def calcualte(self):
        self.display.stop = False
        def index(el, array):
            if el in array:
                return array.index(el)
            else:
                return -1

        def floatOrInt(el):
            if float(el) % 1 == 0:
                return str(int(float(el)))
            else:
                return round(float(el),4)
            
        def minusRewrite():
            for i in range(calcStack.count("-")):
                i = calcStack.index("-")
                if calcStack[i+1][0].isnumeric() == True:
                    calcStack[i+1] = "-" + calcStack[i+1]
                    if calcStack[i-1][-1].isnumeric() == True and i!=0:
                        calcStack[i] = "+"
                    else:
                        calcStack.pop(i)
            
        def calc(find):
            minusRewrite()
            index = calcStack.index(find)
            if find == "²":
                minus = False
                if calcStack[index][0] == "-":
                    minus = True
                calcStack[index-1] = str(floatOrInt(float(calcStack[index-1])**2))
                if minus == True:
                    calcStack.insert(index-1, "+")
                calcStack.pop(index)
            elif find == "√":
                calcStack[index+1] = str(floatOrInt(math.sqrt(float(calcStack[index+1]))))
                calcStack.pop(index)
            elif find == "x":
                calcStack[index] = str(floatOrInt(float(calcStack[index-1])*float(calcStack[index+1])))
                calcStack.pop(index-1)
                calcStack.pop(index)
            elif find == "/":
                if calcStack[index+1] == "0":
                    self.alert("Nie można dzielić przez 0")
                    self.display.stop = True
                else:
                    calcStack[index] = str(floatOrInt(float(calcStack[index-1])/float(calcStack[index+1])))
                    calcStack.pop(index-1)
                    calcStack.pop(index)
            elif find == "+":
                calcStack[index] = str(floatOrInt(float(calcStack[index-1])+float(calcStack[index+1])))
                calcStack.pop(index-1)
                calcStack.pop(index)
            minusRewrite()

                

            self.clear(False)

        def calcFirst(find):
            while find[0] in calcStack or find[1] in calcStack:
                if self.display.stop == True:
                    break
                if index(find[0], calcStack) == -1:
                    calc(find[1])
                elif index(find[1], calcStack) == -1:
                    calc(find[0])
                elif index(find[0], calcStack) < index(find[1], calcStack):
                    calc(find[0])
                else:
                    calc(find[1])

        calcStack = self.display.calcStack
        
        for i in range(calcStack.count("²")):
            calc("²")
        
        for i in range(calcStack.count("√")):
            calc("√")

        calcFirst(["x", "/"])

        for i in range(calcStack.count("+")):
            calc("+")

        self.display.lineReload()

            




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()