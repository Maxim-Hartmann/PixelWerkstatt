import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from app.main_window import MainWindow

# QApplication initialisieren
app = QApplication(sys.argv)
# Hauptfenster erzeugen
window = MainWindow()
window.show()
# Event Loop starten, Fenster bleibt geöffnet
sys.exit(app.exec())