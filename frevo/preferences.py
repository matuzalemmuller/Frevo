import sys
import re
from PyQt5.QtWidgets import *
from file_handler import ConfigHandler
from PyQt5 import QtGui
from PyQt5 import QtCore
from functools import partial


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
    def _clear_text(self, name, command):
        # Unfortunately there is a bug in PyQt where clearing the textbox
        # still shows some trash, so hiding/showing the field resolves the issue
        name.clear()
        command.clear()
        name.hide()
        name.show()
        command.hide()
        command.show()
        command.setFocus()


    # Run button action
    def _run(self, command, terminal):
        self._tray.run_command(command.text(),
                               terminal.isChecked())
        self.activateWindow()


    def _createLayout(self):
        name_list, terminal_list, command_list = ConfigHandler().read_commands()
        layout = []
        nameDesc = []
        commandDesc = []
        nameTextbox = []
        commandTextbox = []
        clearButton = []
        runButton = []
        terminalCheckbox = []
        for i in range(len(command_list)):
            # Name & Command text above fields
            nameDesc.append(QLabel(self))
            nameDesc[i].setText("Name")
            commandDesc.append(QLabel(self))
            commandDesc[i].setText("Command")

            # Name textbox
            nameTextbox.append(QLineEdit(self))
            nameTextbox[i].resize(80,20)
            nameTextbox[i].setMaxLength(15)
            nameTextbox[i].setMaximumWidth(80)
            nameTextbox[i].setValidator(self._nameValidator)
            nameTextbox[i].setText(name_list[i])

            # Command textbox
            commandTextbox.append(QLineEdit(self))
            commandTextbox[i].resize(320,20)
            commandTextbox[i].setText(command_list[i])
            
            # Checkbox to run in terminal
            terminalCheckbox.append(QCheckBox("Launch in Terminal", self))
            if terminal_list[i] == None:
                terminalCheckbox[i].setChecked(True)
            else:
                terminalCheckbox[i].setChecked(terminal_list[i])

            # Clear button
            clearButton.append(QPushButton("Clear", self))
            clearButton[i].setFixedWidth(70)
            clearButton[i].clicked.connect(partial(self._clear_text, nameTextbox[i], commandTextbox[i]))

            # Run button
            runButton.append(QPushButton("Run", self))
            runButton[i].setFixedWidth(60)
            runButton[i].clicked.connect(partial(self._run, commandTextbox[i], terminalCheckbox[i]))

            layout.append(QGridLayout())
            layout[i].addWidget(nameDesc[i], 1, 1)
            layout[i].addWidget(commandDesc[i], 1, 2)
            layout[i].addWidget(nameTextbox[i], 2, 1)
            layout[i].addWidget(commandTextbox[i], 2, 2)
            layout[i].addWidget(clearButton[i], 2, 3)
            layout[i].addWidget(runButton[i], 2, 4)
            layout[i].addWidget(terminalCheckbox[i], 2, 5)
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

        closeLayout = QGridLayout()
        closeLayout.addWidget(cancelButton, 1, 1)
        closeLayout.addWidget(saveButton, 1, 2)

        windowLayout = QGridLayout()
        windowLayout.setVerticalSpacing(0)

        for i in range(len((layout))):
            windowLayout.addLayout(layout[i],i,1)

        windowLayout.addLayout(closeLayout,windowLayout.rowCount()+1,1,
                               QtCore.Qt.AlignCenter)
        windowLayout.setContentsMargins(10,5,5,5)

        return windowLayout