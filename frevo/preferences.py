import sys
import re
from PyQt5.QtWidgets import *
from file_handler import ConfigHandler
from PyQt5 import QtGui
from PyQt5 import QtCore

# Manages Preferences window
class Preferences(QDialog):

    def __init__(self, tray):
        super().__init__()
        self._tray = tray
        self.setWindowTitle("Preferences")
        validator=QtCore.QRegExp("[A-Za-z0-9- _]+")
        self._nameValidator = QtGui.QRegExpValidator(validator)

        self._windowLayout = self._createLayout()        
        self.setLayout(self._windowLayout)

        self.activateWindow()
        self.exec_()


    # Cancel button action
    def _cancel_command(self):
        self.close()


    # Save button action
    def _save_command(self):
        if re.search('[a-zA-Z]', self._commandTextbox.text()):
            if ConfigHandler().save_command(self._nameTextbox.text(),
                                        self._terminalCheckbox.isChecked(),
                                        self._commandTextbox.text()):
                self._tray.refresh_UI()
        else:
            if ConfigHandler().save_command("",True,""):
                self._tray.refresh_UI()
        self.close()


    # Read commands from commands file
    def _read_command(self):
        name, terminal, command = ConfigHandler().read_commands()
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


    def _createLayout(self):
        name_list, terminal_list, command_list = ConfigHandler().read_commands()

        layout = []

        for i in range(len(command_list)):
            # Name & Command text above fields
            nameDesc = QLabel(self)
            nameDesc.setText("Name")
            commandDesc = QLabel(self)
            commandDesc.setText("Command")

            # Name textbox
            nameTextbox = QLineEdit(self)
            nameTextbox.resize(80,20)
            nameTextbox.setMaxLength(15)
            nameTextbox.setMaximumWidth(80)
            nameTextbox.setValidator(self._nameValidator)
            nameTextbox.setText(name_list[i])

            # Command textbox
            commandTextbox = QLineEdit(self)
            commandTextbox.resize(320,20)
            commandTextbox.setText(command_list[i])
            
            # Clear button
            clearButton = QPushButton("Clear", self)
            clearButton.setFixedWidth(70)
            clearButton.clicked.connect(self._clear_text)

            # Run button
            runButton = QPushButton("Run", self)
            runButton.setFixedWidth(60)
            runButton.clicked.connect(self._run)

            # Checkbox to run in terminal
            terminalCheckbox = QCheckBox("Launch in Terminal", self)
            if terminal_list[i] == None:
                terminalCheckbox.setChecked(True)
            else:
                terminalCheckbox.setChecked(terminal_list[i])

            layout.append(QGridLayout())
            layout[i].addWidget(nameDesc, 1, 1)
            layout[i].addWidget(commandDesc, 1, 2)
            layout[i].addWidget(nameTextbox, 2, 1)
            layout[i].addWidget(commandTextbox, 2, 2)
            layout[i].addWidget(clearButton, 2, 3)
            layout[i].addWidget(runButton, 2, 4)
            layout[i].addWidget(terminalCheckbox, 2, 5)
            layout[i].setContentsMargins(10,5,10,5)
            layout[i].setHorizontalSpacing(10)
            layout[i].setVerticalSpacing(0)
            layout[i].setColumnMinimumWidth(2,300)


        cancelButton = QPushButton("Cancel", self)
        cancelButton.setFixedWidth(80)
        cancelButton.clicked.connect(self._cancel_command)
        cancelButton.setDefault(True)

        # Save button
        saveButton = QPushButton("Save", self)
        saveButton.setFixedWidth(80)

        windowLayout = QGridLayout()
        windowLayout.setVerticalSpacing(0)

        for i in range(len((layout))):
            windowLayout.addLayout(layout[i],i,1)

        closeLayout = QGridLayout()
        closeLayout.addWidget(cancelButton, 1, 1)
        closeLayout.addWidget(saveButton, 1, 2)

        windowLayout.addLayout(closeLayout,windowLayout.rowCount()+1,1, QtCore.Qt.AlignCenter)
        windowLayout.setContentsMargins(10,5,5,5)

        return windowLayout