from PyQt6.QtCore import QObject, pyqtSignal, QThread, QMetaObject, Qt, Q_ARG, pyqtSlot
from Constants import SERIAL_PORT
from Hardware import XYStage


class StageController(QObject):
    status = pyqtSignal(str)
    movement_started = pyqtSignal()
    movement_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.stage = XYStage(SERIAL_PORT)
        self.axes_threads = []
        self.axes_workers = []
        for axis in self.stage.axes:
            thread = QThread()
            worker = AxisWorker(self.stage)
            worker.moveToThread(thread)
            thread.start()
            self.axes_threads.append(thread)
            self.axes_workers.append(worker)

    def stage_home_all(self):
        self.stage.home_all_axes()

    def stage_stop(self):
        for worker in self.axes_workers:
            print("Stopping worker")
            worker.stop()
        self.stage.stop_move()

    def stage_move_to(self, axis, pos, vel):
        QMetaObject.invokeMethod(self.axes_workers[axis], "move_to", Qt.ConnectionType.QueuedConnection,
                                 Q_ARG(int, axis), Q_ARG(float, pos), Q_ARG(float, vel))

class AxisWorker(QObject):
    error_state = pyqtSignal(str)
    busy_state = pyqtSignal()
    finished_state = pyqtSignal()

    def __init__(self, stage, *args):
        super().__init__()
        self.stop_requested = False
        self.stage = stage

    @pyqtSlot(int, float, float)
    def move_to(self, axis: int, pos: float, vel: float):
        try:
            self.busy_state.emit()
            self.stage.move_to(axis, pos, vel)
        except Exception as e:
            self.error_state.emit(str(e))
        finally:
            self.finished_state.emit()

    def stop(self):
        self.stop_requested = True
        self.finished_state.emit()
