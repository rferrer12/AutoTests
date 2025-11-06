from PyQt6.QtCore import QObject, pyqtSignal, QThread
from Constants import SERIAL_PORT
from Hardware import XYStage


class StageController(QObject):
    position = pyqtSignal(float, float)
    status = pyqtSignal(str)
    busy_state = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.stage = XYStage(SERIAL_PORT)
        self.thread = None
        self.worker = None

    def _start_worker(self, command, *args):
        if self.thread and self.thread.isRunning():
            print("Worker already running")
            return
        self.thread = QThread()
        self.worker = MotionWorker(self.stage, command, *args)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.move_command)
        self.worker.finished_state.connect(self._clear_thread)
        self.thread.start()

    def stage_home(self):
        self._start_worker("stage_home")

    def stage_stop(self):
        if self.worker:
            print("Stopping worker")
            self.worker.stop()

    def stage_move_to(self, pos: list[float], vel: list[float]):
        self._start_worker("stage_move_to", pos, vel)

    def stage_is_moving(self):
        if self.stage.connection.is_busy():
            return True
        else:
            return False

    def _clear_thread(self):
        self.thread.quit()
        self.thread.wait()
        self.thread = None
        self.worker = None

class MotionWorker(QObject):
    error_state = pyqtSignal(str)
    finished_state = pyqtSignal()

    def __init__(self, stage, command, *args):
        super().__init__()
        self.stage = stage
        self.command = command
        self.args = args
        self._stop_requested = False

    def move_command(self):
        try:
            if self.command == "stage_move_to":
                self._run_move_command(lambda: self.stage.move_to(100, 0))
            elif self.command == "stage_home":
                self._run_move_command(lambda: self.stage.home_all_axes())
        except Exception as e:
            self.error_state.emit(str(e))
        finally:
            self.finished_state.emit()

    def _run_move_command(self, func):
        for axis in self.stage.axes:
            if self._stop_requested:
                self.stage.stop_move()
                return
            func()

    def stop(self):
        self._stop_requested = True
        self.stage.stop_move()
