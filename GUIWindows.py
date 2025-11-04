from pathlib import Path
import subprocess
import time
import Constants

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt6.QtCore import QThread, QEvent, Qt, pyqtSignal
from PyQt6 import uic

import sys

from ui_MainWindow import Ui_MainWindow
from ui_TestWindow import Ui_MainWindow as Ui_TestWindow


#from .ui import MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Home Window")
        self.pushButton.setCheckable(True)
        self.pushButton.pressed.connect(self.home_all_axes)
        self.pushButton_3.pressed.connect(lambda: self.open_test_window("Test 1"))
        self.pushButton_4.pressed.connect(lambda: self.open_test_window("Test 2"))
        self.pushButton_5.pressed.connect(lambda: self.open_test_window("Test 3"))
        self.pushButton_6.pressed.connect(lambda: self.open_test_window("Test 4"))
        self.new_window = None

    def open_test_window(self, name):
        self.new_window = TestWindow()
        self.new_window.setWindowTitle(name)
        self.new_window.show()
        self.close()

    def home_all_axes(self):
        self.pushButton.hide()

class TestWindow(QMainWindow, Ui_TestWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        home_button = self.pushButton
        home_button.setCheckable(True)
        home_button.pressed.connect(self.open_main_window)
        self.new_window = None

    def open_main_window(self):
        self.new_window = MainWindow()
        self.new_window.show()
        self.close()

class FreeWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("FreeWindow.ui", self)
