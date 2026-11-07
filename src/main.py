"""
Startmodul.

Initialisiert die PySide6-Anwendung, erstellt das Hauptfenster
und startet die Ereignisschleife.
"""

import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main() -> None:
    # Jede PySide6-Anwendung braucht genau eine QApplication-Instanz.
    app = QApplication(sys.argv)

    # Hauptfenster erzeugen und maximiert anzeigen.
    window = MainWindow()

    # als Fenster
    window.show()
    # als maximiertes Fenster
    # window.showMaximized()

    # Ereignisschleife (Event Loop) starten.
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
