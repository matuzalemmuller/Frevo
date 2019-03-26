import sys
import re
from PyQt5.QtWidgets import *
from file_handler import FileHandler
from PyQt5 import QtGui
from PyQt5 import QtCore

# Manages Preferences window
class Preferences(QDialog):

    def __init__(self, tray):
        super().__init__()
        self._tray = tray
        self._width = 720
        self._height = 80
        self.setFixedSize(self._width, self._height)
        self.setWindowTitle("Preferences")
        validator=QtCore.QRegExp("[A-Za-z0-9- _]+")
        self._nameValidator = QtGui.QRegExpValidator(validator)
        name, terminal, command = self._read_command()

        # Name textbox
        self._nameTextbox = QLineEdit(self)
        self._nameTextbox.move(20, 20)
        self._nameTextbox.resize(80,20)
        self._nameTextbox.setText(name)
        self._nameTextbox.setMaxLength(15)
        self._nameTextbox.setValidator(self._nameValidator)

        # Command textbox
        self._commandTextbox = QLineEdit(self)
        self._commandTextbox.move(120, 20)
        self._commandTextbox.resize(self._width - 415,20)
        self._commandTextbox.setText(command)
        
        # Clear button
        self._clearButton = QPushButton("Clear", self)
        self._clearButton.setFixedWidth(70)
        self._clearButton.move(self._width - 280,15)
        self._clearButton.clicked.connect(self._clear_text) 

        # Run button
        self._runButton = QPushButton("Run", self)
        self._runButton.setFixedWidth(60)
        self._runButton.move(self._width - 220,15)
        self._runButton.clicked.connect(self._run)

        # Checkbox to run in terminal
        self._terminalCheckbox = QCheckBox("Launch in Terminal", self)
        if terminal == None:
            self._terminalCheckbox.setChecked(True)
        else:
            self._terminalCheckbox.setChecked(terminal)
        self._terminalCheckbox.move(self._width-150,20)
       
        # Save button
        self._saveButton = QPushButton("Save", self)
        self._saveButton.setFixedWidth(80)
        self._saveButton.move(self._width/2,50)
        self._saveButton.clicked.connect(self._save_command)

        # Cancel button
        self._cancelButton = QPushButton("Cancel", self)
        self._cancelButton.setFixedWidth(80)
        self._cancelButton.move((self._width/2)-self._cancelButton.width(),50)
        self._cancelButton.clicked.connect(self._cancel_command)
        self._cancelButton.setDefault(True)

        # Name & Command text above fields
        self._commandDesc = QLabel(self)
        self._commandDesc.setText("Name")
        self._commandDesc.move(20,3)
        self._nameDesc = QLabel(self)
        self._nameDesc.setText("Command")
        self._nameDesc.move(120,3)

        self.activateWindow()
        self.exec_()


    # Cancel button action
    def _cancel_command(self):
        self.close()


    # Save button action
    def _save_command(self):
        if re.search('[a-zA-Z]', self._commandTextbox.text()):
            if FileHandler().save_command(self._nameTextbox.text(),
                                        self._terminalCheckbox.isChecked(),
                                        self._commandTextbox.text()):
                self._tray.refresh_UI()
                self.close()
        else:
            if FileHandler().save_command("",True,""):
                self._tray.refresh_UI()
                self.close()


    # Read commands from commands file
    def _read_command(self):
        name, terminal, command = FileHandler().read_commands()
        return name, terminal, command
    

    # Clear button action
    def _clear_text(self):
        self._commandTextbox.clear()
        self._nameTextbox.clear()
        # Unfortunately there is a bug in PyQt where clearing the textbox
        # still shows some trash, so hide/show resolves the issue
        self._commandTextbox.hide()
        self._commandTextbox.show()
        self._nameTextbox.hide()
        self._nameTextbox.show()


    # Run button action
    def _run(self):
        self._tray.run_command(self._commandTextbox.text(),
                               self._terminalCheckbox.isChecked())
        self.activateWindow()
