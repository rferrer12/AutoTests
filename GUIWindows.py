from pathlib import Path
import subprocess
import time

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
        test1_button = self.pushButton_3
        test1_button.setCheckable(True)
        test1_button.pressed.connect(self.open_test_window)
        test2_button = self.pushButton_4
        test2_button.setCheckable(True)
        test2_button.pressed.connect(self.open_test_window)
        test3_button = self.pushButton_5
        test3_button.setCheckable(True)
        test3_button.pressed.connect(self.open_test_window)
        test4_button = self.pushButton_6
        test4_button.setCheckable(True)
        test4_button.pressed.connect(self.open_test_window)
        self.new_window = None

    def open_test_window(self):
        self.new_window = TestWindow()
        self.new_window.show()
        self.close()


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

class Test1(TestWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Test 1")

class FreeWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("FreeWindow.ui", self)
