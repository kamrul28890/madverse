"""
MadVerse — A Genre-Based, Randomized, GUI Mad Libs Game
Entry point
"""

import sys
import os

# Ensure the package root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("MadVerse")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("MadVerse Studios")

    # High-DPI scaling
    # app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
