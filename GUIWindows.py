from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QPushButton, QDialogButtonBox, QMessageBox, QFileDialog
from PyQt6.QtCore import QThread, QEvent, Qt, pyqtSignal
from PyQt6 import uic
from zaber_motion import Units

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
        self.pushButton_3.pressed.connect(lambda: self.open_test_window("Test 1"))
        self.pushButton_4.pressed.connect(lambda: self.open_test_window("Test 2"))
        self.pushButton_5.pressed.connect(lambda: self.open_test_window("Test 3"))
        self.pushButton_6.pressed.connect(lambda: self.open_test_window("Test 4"))
        self.pushButton_7.pressed.connect(lambda: controller.stage_stop())
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
        dlg = DialogWindow()
        dlg.textBrowser.setText("Please ensure that the tool will not collide with the workpiece or other materials.")
        if dlg.exec():
            self.new_window = FreeWindow()
            self.new_window.setWindowTitle(name)
            self.new_window.show()
            self.close()

    def open_test_window(self, name):
        self.close()
        self.new_window = TestWindow()
        self.new_window.setWindowTitle(name)
        self.new_window.show()

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
        home_button = self.homeButton
        home_button.setCheckable(True)
        home_button.pressed.connect(self.open_main_window)
        self.new_window = None
        self.minPos1Label.setText(str(controller.stage.axes[0]["limits"][0]))
        self.maxPos1Label.setText(str(controller.stage.axes[0]["limits"][1]))
        self.axis1Slider.setRange(controller.stage.axes[0]["limits"][0], controller.stage.axes[0]["limits"][1])
        self.axis1Slider.sliderReleased.connect(lambda: self.move_to_pos([float(self.axis1Slider.value())], [10.0]))
        self.axis1Slider.valueChanged.connect(lambda: self.pos1lineEdit.setText(str(self.axis1Slider.value())))
        self.axis1Slider.sliderPressed.connect(lambda: self.pos1lineEdit.setText(str(self.axis1Slider.value())))
        self.axis1Slider.setValue(controller.stage.axes[0]["axis"].get_position(unit = Units.LENGTH_MILLIMETRES))
        stop_button = self.stopButton
        stop_button.pressed.connect(lambda: controller.stage_stop())
        stop_button.pressed.connect(lambda: self.axis1Slider.setValue(controller.stage.axes[0]["axis"].get_position(unit = Units.LENGTH_MILLIMETRES)))
        if len(controller.stage.axes) == 2:
            self.minPos2Label.setText(str(controller.stage.axes[1]["limits"][0]))
            self.maxPos2Label.setText(str(controller.stage.axes[1]["limits"][1]))
            self.axis2Slider.setRange(controller.stage.axes[1]["limits"][0], controller.stage.axes[1]["limits"][1])
            self.axis2Slider.sliderReleased.connect(lambda: self.move_to_pos([float(self.axis1Slider.value())], [10.0]))
            self.axis2Slider.valueChanged.connect(lambda: self.pos1lineEdit.setText(str(self.axis1Slider.value())))
            self.axis2Slider.sliderPressed.connect(lambda: self.pos1lineEdit.setText(str(self.axis1Slider.value())))
        else:
            self.minPos2Label.setText(str("NA"))
            self.maxPos2Label.setText(str("NA"))
            self.axis2Slider.setEnabled(False)
            self.setPos2Button.setEnabled(False)
            self.pos2lineEdit.setText(str("NA"))
            self.pos2lineEdit.setEnabled(False)
        controller.movement_started.connect(self.on_movement_started)
        controller.movement_finished.connect(self.on_movement_finished)

    def open_main_window(self):
        self.new_window = MainWindow()
        self.new_window.show()
        self.close()

    def move_to_pos(self, pos: list[float], vel: list[float]):
        controller.stage_move_to(pos, vel)

    def on_movement_started(self):
        self.axis1Slider.setEnabled(False)
        self.setPos1Button.setEnabled(False)

    def on_movement_finished(self):
        self.axis1Slider.setEnabled(True)
        self.setPos1Button.setEnabled(True)

class DialogWindow(QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

