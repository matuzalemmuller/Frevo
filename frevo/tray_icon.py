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
        self._commandAction = []
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
        name_list, terminal_list, command_list = ConfigHandler().read_commands()

        for i in range(len(command_list)):
            if command_list[i] == "":
                break
            self._commandAction.append(QAction())
            self._commandAction[i].triggered.connect(self.run_command)
            self._commandAction[i].setText(name_list[i])
            self._menu.addAction(self._commandAction[i])
    
        self._menu.addSeparator()
        self._menu.addAction(self._preferenceAction)
        self._menu.addAction(self._aboutAction)
        self._menu.addAction(self._quitAction)


    # Closes app when "Quit" is selected in sys tray
    def _exit(self):
        sys.exit(0)