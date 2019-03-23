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

        self.action1 = QAction("Preferences")
        self.menu.addAction(self.action1)
        self.action1.triggered.connect(self._configure)

        self.action2 = QAction("Quit")
        self.menu.addAction(self.action2)
        self.action2.triggered.connect(self._exit)

        self.tray.setContextMenu(self.menu)

    @QtCore.pyqtSlot()
    def _configure(self):
        Preferences()

    def _exit(self):
        sys.exit(0)
