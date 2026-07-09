"""
Startmodul.

Initialisiert die PySide6-Anwendung, erstellt das Hauptfenster und startet die Ereignisschleife.
"""

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main() -> None:
    # Jede PySide6 Anwendung braucht genau eine QApplication Instanz.
    app = QApplication(sys.argv)
    # Hauptfenster erzeugen.
    window = MainWindow()
    window.show()
    window.showMaximized()
    # Event Loop starten: Fenster bleibt geöffnet und kann sauber geschlossen werden.
    sys.exit(app.exec())


# Verhindert das automatische Starten beim Import des Moduls.
if __name__ == "__main__":
    main()
