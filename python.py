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

        calHistory = []

        class Button:
            def __init__(self, text, icon="none", type="def", clicked=None):
                self.text = text
                self.type = type
                self.icon = QIcon(icon)
                self.obj = QPushButton(text)
                self.obj.setFixedHeight(50)
                self.obj.setFixedWidth(80)
                self.obj.setStyleSheet("font-size: 20px;")
                self.obj.setIcon(self.icon)
                self.obj.setIconSize(self.obj.sizeHint())
                if(clicked != None):
                    self.obj.clicked.connect(clicked)
                if clicked != None:
                    print("tak")
                if type == "empty":
                    self.obj.setEnabled(False)

            def getObj(self):
                return self.obj

        self.buttons = [
            {"empty1":Button("",type="empty"), "CE":Button("CE"), "C":Button("C"), "backspace":Button("", icon="./icons/backspace.png")},
            {"empty2":Button("",type="empty"), "square":Button("x²"), "root":Button("√x"), "divine":Button("/")},
            {"7":Button("7"), "8":Button("8"), "9":Button("9"), "multiply":Button("x")},
            {"4":Button("4"), "5":Button("5"), "6":Button("6"), "sub":Button("-")},
            {"1":Button("1"), "2":Button("2"), "3":Button("3"), "add":Button("+")},
            {"empty3":Button("",type="empty"), "0":Button("0"), "dot":Button(","), "equal":Button("=")}
        ]

        mainLayout = QVBoxLayout()
    
        btLayout = QGridLayout()

        display = QLineEdit()
        display.setReadOnly(True)
        display.setFixedHeight(50)
        display.setStyleSheet("font-size: 30px;")
        display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display = display

        self.display.setText("0")

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

        mainLayout.addWidget(display)
        mainLayout.addLayout(btLayout)
        self.setLayout(mainLayout)




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()