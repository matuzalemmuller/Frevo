import sys
from PyQt5.QtWidgets import *


class Preferences(QDialog):

    def __init__(self):
        super().__init__()
        # Textbox
        textbox = QLineEdit(self)
        textbox.move(20, 20)
        textbox.resize(400,20)
        # Save button
        button = QPushButton("Save", self)
        button.move(200,50)
        self.exec_()