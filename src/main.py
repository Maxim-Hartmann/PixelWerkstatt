"""
Haupteinstiegspunkt der PixelWerkstatt-Anwendung.
"""

import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main() -> None:
    """
    Startet die PySide6-Anwendung und öffnet das Hauptfenster.
    """

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
