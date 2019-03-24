import sys
from PyQt5.QtWidgets import *
from file_handler import FileHandler


class Preferences(QDialog):

    def __init__(self, tray):
        super().__init__()
        self.width = 450
        self.height = 80
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("Preferences")
        
        # Textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(self.width - 50,20)
        self.textbox.setText(self._read_command())
        
        # Save button
        self.button = QPushButton("Save", self)
        self.button.setFixedWidth(80)
        self.button.move((self.width/2)-(self.button.width()/2),50)
        self.button.clicked.connect(self._save_command)

        self.tray = tray
        
        self.exec_()


    def _save_command(self):
        if FileHandler().save_command(self.textbox.text()):
            self.tray._refresh_UI()
            self.close()


    def _read_command(self):
        return FileHandler().read_commands()