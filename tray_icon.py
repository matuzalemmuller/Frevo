import sys
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from preferences import Preferences
from file_handler import FileHandler

# Creates tray icon and tray options
class TrayIcon(QApplication):

    def __init__(self, icon):
        super().__init__([])
        self.icon = QIcon(icon)
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        # Creates menu and button actions
        self.menu = QMenu()
        self.commandAction = QAction("Run command")
        self.commandAction.triggered.connect(self._run_command)
        self.preferenceAction = QAction("Preferences")
        self.preferenceAction.triggered.connect(self._configure)
        self.quitAction = QAction("Quit")
        self.quitAction.triggered.connect(self._exit)
        self._refresh_UI()

        self.tray.setContextMenu(self.menu)


    @QtCore.pyqtSlot()
    def _configure(self):
        Preferences(self)


    def _run_command(self):
        pass


    def _refresh_UI(self):
        self.menu.clear()
        if FileHandler().read_commands():
            self.menu.addAction(self.commandAction)
            self.menu.addSeparator()
        else:
            if 'commandAction' in locals():
                if self.commandAction:
                    self.menu.removeAction(self.commandAction)
        
        self.menu.addAction(self.preferenceAction)
        self.menu.addAction(self.quitAction)


    def _exit(self):
        sys.exit(0)