from PyQt6.QtCore import QObject, pyqtSignal
from Constants import SERIAL_PORT
from Hardware import XYStage


class StageController(QObject):
    position = pyqtSignal(float, float)
    status = pyqtSignal(str)
    busy_state = pyqtSignal(bool)

    def __init__(self, port: str = SERIAL_PORT):
        super().__init__()
        self.stage = XYStage(port)

    def stage_home(self):
        self.stage.home_all_axes()

    def stage_stop(self):
        self.stage.stop_move()

    def stage_move(self, pos: list[float], vel: list[float]):
        self.stage.move_to(pos, vel)

    def stage_is_moving(self):
        if self.stage.connection.is_busy():
            return True
        else:
            return False