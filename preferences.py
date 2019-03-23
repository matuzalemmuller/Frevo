import sys
from PyQt5.QtWidgets import *


class Preferences(QDialog):

    def __init__(self):
        super().__init__()
        self.width = 450
        self.height = 80
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("Preferences")
        
        # Textbox
        textbox = QLineEdit(self)
        textbox.move(20, 20)
        textbox.resize(self.width - 50,20)
        
        # Save button
        button = QPushButton("Save", self)
        button.setFixedWidth(80)
        button.move((self.width/2)-(button.width()/2),50)
        button.clicked.connect(self._save_command)
        
        self.exec_()


    def _save_command(self):
        print("File saved!")