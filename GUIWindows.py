from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QPushButton, QDialogButtonBox, QMessageBox
from PyQt6.QtCore import QThread, QEvent, Qt, pyqtSignal
from PyQt6 import uic

import sys

from Controller import StageController
from ui_MainWindow import Ui_MainWindow
from ui_TestWindow import Ui_MainWindow as Ui_TestWindow
from ui_FreeWindow import Ui_MainWindow as Ui_FreeWindow
from ui_DialogWarning import Ui_Dialog
import Controller


#from .ui import MainWindow
controller = StageController()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Home Window")
        self.pushButton.pressed.connect(self.home_all_axes)
        self.pushButton_2.pressed.connect(lambda: self.open_free_move("Free Move"))
        self.pushButton_3.pressed.connect(lambda: controller.stage_stop())
        self.pushButton_4.pressed.connect(lambda: self.open_test_window("Test 2"))
        self.pushButton_5.pressed.connect(lambda: self.open_test_window("Test 3"))
        self.pushButton_6.pressed.connect(lambda: self.open_test_window("Test 4"))
        self.new_window = None

    def home_all_axes(self):
        dlg = DialogWindow()
        dlg.textBrowser.setText("Please ensure that the tool will not collide with the workpiece or other materials.")
        if dlg.exec():
            controller.stage_home()
            print("Home all axes accepted")
        else:
            print("Home all axes rejected")

    def open_free_move(self, name):
        self.new_window = FreeWindow()
        self.new_window.setWindowTitle(name)
        self.new_window.show()
        self.close()

    def open_test_window(self, name):
        self.new_window = TestWindow()
        self.new_window.setWindowTitle(name)
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

class FreeWindow(QMainWindow, Ui_FreeWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        home_button = self.pushButton
        home_button.setCheckable(True)
        home_button.pressed.connect(self.open_main_window)
        self.new_window = None
        self.minPos_label.setText(str(controller.stage.axes[0]["limits"][0]))
        self.maxPos_label.setText(str(controller.stage.axes[0]["limits"][1]))

    def open_main_window(self):
        self.new_window = MainWindow()
        self.new_window.show()
        self.close()

class DialogWindow(QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

