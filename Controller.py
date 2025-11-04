from PyQt6.QtCore import QObject, pyqtSignal
import Hardware
import Constants
from Constants import SERIAL_PORT
from Hardware import XYStage


class StageController(QObject):
    position = pyqtSignal(float, float)
    status = pyqtSignal(str)
    busy_state = pyqtSignal(bool)

    def __init__(self, port: str = SERIAL_PORT):
        super().__init__()
        self.stage = XYStage(port)


