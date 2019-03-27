import sys
import os
from appscript import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from preferences import Preferences
from file_handler import ConfigHandler
from about import About

# Creates tray icon and tray options
class TrayIcon(QApplication):

    def __init__(self, icon):
        super().__init__([])
        self._icon = QIcon(icon)
        self._tray = QSystemTrayIcon()
        self._tray.setIcon(self._icon)
        self._tray.setVisible(True)

        # Creates menu and button actions
        self._menu = QMenu()
        self._commandAction = QAction()
        self._commandAction.triggered.connect(self.run_command)
        self._preferenceAction = QAction("Preferences")
        self._preferenceAction.triggered.connect(self._configure)
        self._aboutAction = QAction("About")
        self._aboutAction.triggered.connect(self._about)
        self._quitAction = QAction("Quit")
        self._quitAction.triggered.connect(self._exit)
        
        self.refresh_UI()
        self._tray.setContextMenu(self._menu)


    # Launches Preferences when "Preferences" is selected in sys tray
    @QtCore.pyqtSlot()
    def _configure(self):
        Preferences(self)


   # Launches Preferences when "Preferences" is selected in sys tray
    @QtCore.pyqtSlot()
    def _about(self):
        About()


    # Runs command when "Run command" is selected in sys tray
    def run_command(self, command=None, terminal=True):
        if command == None or command == False:
            name, terminal, command = ConfigHandler().read_commands()
            if name == None and terminal == None and command == None:
                return
        if terminal == True:
            terminal = app('Terminal')
            terminal.launch()
            terminal.activate()
            terminal.do_script(command)
        else:
            os.system(command)


    # Refreshes sys tray options
    def refresh_UI(self):
        self._menu.clear()
        name, terminal, command = ConfigHandler().read_commands()
        if name == None and terminal == None and command == None:
            if '_commandAction' in locals():
                if self._commandAction:
                    self._menu.removeAction(self._commandAction)
        elif name == "":
            if command == "":
                if '_commandAction' in locals():
                    if self._commandAction:
                        self._menu.removeAction(self._commandAction)
            else:
                self._commandAction.setText("Run command")
                self._menu.addAction(self._commandAction)
                self._menu.addSeparator()
        else:
            self._commandAction.setText(name)
            self._menu.addAction(self._commandAction)
            self._menu.addSeparator()
        
        self._menu.addAction(self._preferenceAction)
        self._menu.addAction(self._aboutAction)
        self._menu.addAction(self._quitAction)


    # Closes app when "Quit" is selected in sys tray
    def _exit(self):
        sys.exit(0)