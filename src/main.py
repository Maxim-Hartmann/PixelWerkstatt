import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

# Jede PySide6 Anwendung braucht genau eine QApplication Instanz.
app = QApplication(sys.argv)
# Hauptfenster erzeugen
window = MainWindow()
window.show()
# Fenstergröße
window.showMaximized()
# Event Loop starten, Fenster bleibt geöffnet und kann sauber geschlossen werden.
sys.exit(app.exec())
