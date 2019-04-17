import sys
import re
from functools import partial
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from file_handler import ConfigHandler


# Manages Preferences window
class Preferences(QDialog):

    def __init__(self, tray):
        super().__init__()
        self._tray = tray
        self.setWindowTitle("Preferences")
        validator=QtCore.QRegExp("[A-Za-z0-9- _]+")
        self._nameValidator = QtGui.QRegExpValidator(validator)

        self._windowLayout = self._createLayout()
        self._windowLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(self._windowLayout)

        self.exec_()
        self.activateWindow()


    # Cancel button action
    def _cancel_command(self):
        self.close()


    # Save button action: scans all commands & names and saved them to the
    # commands file. If no name is provided, command is saved as "Command N"
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


    # Reads commands from commands file
    def _read_command(self):
        name, terminal, command = ConfigHandler().read_commands()
        return name, terminal, command
    

    # Clear button action: clears selected name and command
    def _clear_text(self, name, command):
        name.clear()
        command.clear()
        command.setFocus()
        self.repaint()


    # Run button action
    def _run(self, command, terminal):
        if command.text() == "":
            return
        self._tray.run_command(command.text(),
                               terminal.isChecked())
        self.activateWindow()


    # Removes command layout: first removes all widgets and then dissociates
    # command layout from window layout
    def _remove_command(self, layout):
        nameDesc = layout.itemAtPosition(1,1).widget()
        nameDesc.setParent(None)
        nameDesc.deleteLater()
        commandDesc = layout.itemAtPosition(1,2).widget()
        commandDesc.setParent(None)
        commandDesc.deleteLater()
        nameTextbox = layout.itemAtPosition(2,1).widget()
        nameTextbox.setParent(None)
        nameTextbox.deleteLater()
        commandTextbox = layout.itemAtPosition(2,2).widget()
        commandTextbox.setParent(None)
        commandTextbox.deleteLater()
        clearButton = layout.itemAtPosition(2,3).widget()
        clearButton.setParent(None)
        clearButton.deleteLater()
        runButton = layout.itemAtPosition(2,4).widget()
        runButton.setParent(None)
        runButton.deleteLater()
        terminalCheckbox = layout.itemAtPosition(2,5).widget()
        terminalCheckbox.setParent(None)
        terminalCheckbox.deleteLater()
        removeButton = layout.itemAtPosition(2,6).widget()
        removeButton.setParent(None)
        removeButton.deleteLater()

        layout.setParent(None)
        layout.deleteLater()

        self.update()
        self.repaint()

        # If there's only a close widget, maintain size
        if self._windowLayout.count() == 1:
            self._windowLayout.setSizeConstraint(QLayout.SetDefaultConstraint)


    # Creates the commands and close layouts
    def _createLayout(self):
        name_list, terminal_list, command_list = ConfigHandler().read_commands()
        layout = []

        if command_list == None:
            name_list = " "
            command_list = " "
            terminal_list = [True]

        # Creates list of command layouts
        for i in range(len(command_list)):
            layout.append(self._create_command_layout(name_list[i],
                                                      command_list[i],
                                                      terminal_list[i]))
                                                      
        closeLayout = self._create_close_layout()
        
        windowLayout = QGridLayout()            # Combines all layouts in a
        windowLayout.setVerticalSpacing(0)      # single layout
        for i in range(len((layout))):
            windowLayout.addLayout(layout[i],i,1)
        windowLayout.addLayout(closeLayout,windowLayout.rowCount()+1,1,
                               QtCore.Qt.AlignCenter)
        windowLayout.setContentsMargins(10,5,5,5)

        return windowLayout

    
    # Creates command layout
    # * nameDesc, commandDesc = QLabel
    # * nameTextbox, commandTextbox = QLineEdit
    # * terminalCheckbox = QCheckBox
    # * clearButton, runButton, removeButton = QPushButton
    def _create_command_layout(self, name_list, command_list, terminal_list):
        layout = QGridLayout()
        
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

        # Remove button
        removeButton = QPushButton("Remove", self)
        removeButton.setFixedWidth(80)
        removeButton.clicked.connect(partial(self._remove_command,
                                             layout))       

        layout.addWidget(nameDesc, 1, 1)
        layout.addWidget(commandDesc, 1, 2)
        layout.addWidget(nameTextbox, 2, 1)
        layout.addWidget(commandTextbox, 2, 2)
        layout.addWidget(clearButton, 2, 3)
        layout.addWidget(runButton, 2, 4)
        layout.addWidget(terminalCheckbox, 2, 5)
        layout.addWidget(removeButton, 2, 6)
        layout.setContentsMargins(10,5,10,5)
        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(0)
        layout.setColumnMinimumWidth(2,300)

        return layout
    

    # Creates close layout:
    # * cancelButton, saveButton, addButton = QPushButton
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
    

    # Adds command layout to interface: removes close layout, adds command
    # layout and then re-add close layout
    def _add_command_layout(self):
        if self._windowLayout.count() == 1:
            self._windowLayout.setSizeConstraint(QLayout.SetFixedSize)

        # Deletes current close layout
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
