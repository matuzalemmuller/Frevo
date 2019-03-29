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
        widgets = self._windowLayout.children()
        name_list = []
        terminal_list = []
        command_list = []

        if len(widgets) > 1:
            for i in range(len(widgets)-1):
                grid = widgets[i]
                name = grid.itemAtPosition(2,1).widget().text()
                terminal = grid.itemAtPosition(2,5).widget().isChecked()
                command = grid.itemAtPosition(2,2).widget().text()

                if re.search('[a-zA-Z]', command):
                    name_list.append(name)
                    terminal_list.append(terminal)
                    command_list.append(command + "\n")
                else:
                    continue
            ConfigHandler().save_commands(name_list, terminal_list, command_list)
        else:
            ConfigHandler().save_commands("",True,"")
        
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
        if command.text() == "" or :
            return
        self._tray.run_command(command.text(),
                               terminal.isChecked())
        self.activateWindow()


    def _createLayout(self):
        name_list, terminal_list, command_list = ConfigHandler().read_commands()
        layout = []

        if command_list == None: # needs to be fixed
            name_list = " "
            command_list = " "
            terminal_list = [True]

        for i in range(len(command_list)):
            layout.append(self._create_command_layout(name_list[i],
                                                      command_list[i],
                                                      terminal_list[i]))

        closeLayout = self._create_close_layout()
        
        windowLayout = QGridLayout()
        windowLayout.setVerticalSpacing(0)
        for i in range(len((layout))):
            windowLayout.addLayout(layout[i],i,1)
        windowLayout.addLayout(closeLayout,windowLayout.rowCount()+1,1,
                               QtCore.Qt.AlignCenter)
        windowLayout.setContentsMargins(10,5,5,5)

        return windowLayout

    
    def _create_command_layout(self, name_list, command_list, terminal_list):
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
        if name_list != " ":
            nameTextbox.setText(name_list) # needs to be fixed

        # Command textbox
        commandTextbox = QLineEdit(self)
        commandTextbox.resize(320,20)
        if command_list != " ":
            commandTextbox.setText(command_list) # needs to be fixed
        
        # Checkbox to run in terminal
        terminalCheckbox = QCheckBox("Launch in Terminal", self)
        terminalCheckbox.setChecked(terminal_list)

        # Clear button
        clearButton = QPushButton("Clear", self)
        clearButton.setFixedWidth(70)
        clearButton.clicked.connect(partial(self._clear_text,
                                            nameTextbox,
                                            commandTextbox))

        # Run button
        runButton = QPushButton("Run", self)
        runButton.setFixedWidth(60)
        runButton.clicked.connect(partial(self._run, commandTextbox,
                                                terminalCheckbox))

        layout = QGridLayout()
        layout.addWidget(nameDesc, 1, 1)
        layout.addWidget(commandDesc, 1, 2)
        layout.addWidget(nameTextbox, 2, 1)
        layout.addWidget(commandTextbox, 2, 2)
        layout.addWidget(clearButton, 2, 3)
        layout.addWidget(runButton, 2, 4)
        layout.addWidget(terminalCheckbox, 2, 5)
        layout.setContentsMargins(10,5,10,5)
        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(0)
        layout.setColumnMinimumWidth(2,300)

        return layout
    

    def _create_close_layout(self):
        # Cancel button
        cancelButton = QPushButton("Cancel", self)
        cancelButton.setFixedWidth(80)
        cancelButton.clicked.connect(self._cancel_command)
        cancelButton.setDefault(True)

        # Save button
        saveButton = QPushButton("Save", self)
        saveButton.setFixedWidth(80)
        saveButton.clicked.connect(self._save_command)

        # Add button
        addButton = QPushButton("Add command", self)
        addButton.setFixedWidth(120)
        addButton.clicked.connect(self._add_command_layout)

        closeLayout = QGridLayout()
        closeLayout.addWidget(addButton, 1, 5)
        closeLayout.addWidget(cancelButton, 2, 3)
        closeLayout.addWidget(saveButton, 2, 7)

        return closeLayout
    

    def _add_command_layout(self):
        # Delete bottom button layout
        widgets = self._windowLayout.children()
        buttons = widgets[-1]
        cancel = buttons.itemAtPosition(1,5).widget()
        cancel.setParent(None)
        cancel.deleteLater()
        save = buttons.itemAtPosition(2,3).widget()
        save.setParent(None)
        save.deleteLater()
        add = buttons.itemAtPosition(2,7).widget()
        add.setParent(None)
        add.deleteLater()
        buttons.setParent(None)
        buttons.deleteLater()

        layout = self._create_command_layout("", "", True)
        closeLayout = self._create_close_layout()

        self._windowLayout.addLayout(layout,len(widgets),1)
        self._windowLayout.addLayout(closeLayout,len(widgets)+1,1)

        self._windowLayout.update()
