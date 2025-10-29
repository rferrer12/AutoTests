from pathlib import Path
import subprocess
import time

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt6.QtCore import QThread, QEvent, Qt, pyqtSignal
from PyQt6 import uic

import sys

from ui_MainWindow import Ui_MainWindow


#from .ui import MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        test_button = self.pushButton_3
        test_button.setCheckable(True)
        test_button.pressed.connect(self.openTestWindow)
        self.new_window = None

    def openTestWindow(self):
        self.new_window = TestWindow()
        self.new_window.show()
        self.hide()


class TestWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("TestWindow.ui", self)

class FreeWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("FreeWindow.ui", self)
