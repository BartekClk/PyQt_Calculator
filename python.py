python.py
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
        self.setFixedHeight(400)
        self.setMaximumWidth(400)
            
        appIcon = QIcon("./icons/icon.png")
        self.setWindowIcon(appIcon)

        calHistory = []

        class Button:
            def __init__(self, text, icon="none", type="def"):
                self.text = text
                self.type = type
                self.icon = icon
                self.obj = QPushButton(text)
                if type == "empty":
                    self.obj.setEnabled(False)

        buttons = [
            [Button("",type="empty"), Button("CE"), Button("C"), Button("", icon="./icons/icon.png")],
            [],
            [],
            [],
            [],
            []
        ]

    # for x in range(0,)



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()