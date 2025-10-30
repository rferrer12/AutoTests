from pathlib import Path
import subprocess
import time

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt6.QtCore import QThread, QEvent, Qt, pyqtSignal
from PyQt6 import uic

from ui_MainWindow import Ui_MainWindow
from ui_TestWindow import Ui_MainWindow as Ui_TestWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        test_button = self.pushButton_3
        test_button.setCheckable(True)
        test_button.pressed.connect(self.open_test_window())
        self.new_window = None

    def open_test_window(self):
        self.new_window = TestWindow()
        self.new_window.show()
        self.hide()

class TestWindow(QMainWindow, Ui_TestWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        home_button = self.pushButton
        home_button.setCheckable(True)
        home_button.pressed.connect(self.open_main_window())
        self.new_window = None

    def open_main_window(self):
        self.new_window = MainWindow()
        self.new_window.show()
        self.hide()


class FreeWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("FreeWindow.ui", self)
