from __future__ import annotations

"""
Haupteinstiegspunkt der PixelWerkstatt-Anwendung.
"""

import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main() -> None:
    """
    Startet die PySide6-Anwendung und öffnet das Hauptfenster.
    """

    app = QApplication(sys.argv)

    # Setzt die app_id
    app.setDesktopFileName("pixelwerkstatt")

    # Icon global für die gesamte Anwendung setzen
    assets_dir = Path(__file__).resolve().parent / "assets"
    app.setWindowIcon(QIcon(str(assets_dir / "Icon_chess.png")))

    window = MainWindow()
    window.setWindowTitle("PixelWerkstatt")
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
