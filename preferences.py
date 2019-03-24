import sys
from PyQt5.QtWidgets import *
from file_handler import FileHandler


# Manages Preferences window
class Preferences(QDialog):

    def __init__(self, tray):
        super().__init__()
        self._tray = tray
        self._width = 600
        self._height = 80
        self.setFixedSize(self._width, self._height)
        self.setWindowTitle("Preferences")
        
        # Textbox
        self._textbot = QLineEdit(self)
        self._textbot.move(20, 20)
        self._textbot.resize(self._width - 300,20)
        terminal, command = self._read_command()
        self._textbot.setText(command)
        
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

        self.activateWindow()
        self.exec_()


    # Cancel button action
    def _cancel_command(self):
        self.close()


    # Save button action
    def _save_command(self):
        if FileHandler().save_command(self._terminalCheckbox.isChecked(),
                                      self._textbot.text()):
            self._tray.refresh_UI()
            self.close()


    # Read commands from commands file
    def _read_command(self):
        terminal, command = FileHandler().read_commands()
        return terminal, command
    

    # Clear button action
    def _clear_text(self):
        self._textbot.clear()


    # Run button action
    def _run(self):
        self._tray.run_command(self._textbot.text(),
                               self._terminalCheckbox.isChecked())
        self.activateWindow()
