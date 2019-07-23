from PyQt5.QtWidgets import *
from PyQt5 import QtCore


# Shows information about project and developer
class About(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")

        self.layout = QVBoxLayout()

        # Project name
        self._git = QLabel("2019 <a href=\""+
                           "https://github.com/matuzalemmuller/Frevo\""+
                           ">Frevo</a>")
        self._git.setOpenExternalLinks(True)
        self._git.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self._git)

        # Developer
        self._developer = QLabel("by <a href=\""+
                           "https://www.linkedin.com/in/matuzalemmuller/\""+
                           ">Mat Muller</a>")
        self._developer.setOpenExternalLinks(True)
        self._developer.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self._developer)

        # Version
        self._developer = QLabel("v1.0.1")
        self._developer.setOpenExternalLinks(True)
        self._developer.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self._developer)

        self.setLayout(self.layout)

        self.exec_()
        self.activateWindow()
