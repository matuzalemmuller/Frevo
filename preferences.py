import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from file_handler import FileHandler


class Preferences(QDialog):

    def __init__(self, tray):
        super().__init__()
        self._tray = tray
        self._width = 500
        self._height = 80
        self.setFixedSize(self._width, self._height)
        self.setWindowTitle("Preferences")
        
        # Textbox
        self._textbot = QLineEdit(self)
        self._textbot.move(20, 20)
        self._textbot.resize(self._width - 160,20)
        self._textbot.setText(self._read_command())
        
        # Clear button
        self._clearButton = QPushButton("Clear", self)
        self._clearButton.setFixedWidth(80)
        self._clearButton.move(self._width - 140,15)
        self._clearButton.clicked.connect(self._clear_text) 

        # Run button
        self._runButton = QPushButton("Run", self)
        self._runButton.setFixedWidth(60)
        self._runButton.move(self._width - 60,15)
        self._runButton.clicked.connect(self._run)
        
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

        self.activateWindow()
        self.exec_()


    def _cancel_command(self):
        self.close()


    def _save_command(self):
        if FileHandler().save_command(self._textbot.text()):
            self._tray.refresh_UI()
            self.close()


    def _read_command(self):
        return FileHandler().read_commands()
    

    def _clear_text(self):
        self._textbot.clear()


    def _run(self):
        self._tray.run_command(self._textbot.text())
        self.activateWindow()
