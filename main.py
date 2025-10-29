from pathlib import Path
import subprocess
import time

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtCore import QThread, QEvent, Qt, pyqtSignal
from PyQt6 import uic
import GUIWindows

import sys

#from .ui import MainWindow

def main():
    # Re-generate ui.py, if UI modified in QT Designer
    """
    current_ui, prev_ui = Path("MainWindow.ui"), Path("MainWindow_compare.ui")
    if current_ui.read_text(encoding="utf-8") != prev_ui.read_text(encoding="utf-8"):
        print("\nUpdating Python UI file:")
        prev_ui.unlink()
        prev_ui.write_bytes(current_ui.read_bytes())
        print(subprocess.check_output("UI_py_convert.bat"))
        raise SystemExit("UI Re-built. Please start again.")
    """

    app = QApplication(sys.argv)
    window = GUIWindows.MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    sys.exit(main())