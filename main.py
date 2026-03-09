import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())