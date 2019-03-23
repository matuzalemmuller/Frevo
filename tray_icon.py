import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from preferences import Preferences

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

        self.preferenceAction = QAction("Preferences")
        self.menu.addAction(self.preferenceAction)
        self.preferenceAction.triggered.connect(self._configure)

        self.quitAction = QAction("Quit")
        self.menu.addAction(self.quitAction)
        self.quitAction.triggered.connect(self._exit)

        self.tray.setContextMenu(self.menu)

    @QtCore.pyqtSlot()
    def _configure(self):
        Preferences()

    def _exit(self):
        sys.exit(0)
