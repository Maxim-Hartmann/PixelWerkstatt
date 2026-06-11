import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from core.lauflaenge import lauf_code

class MainWindow(QWidget):
    # Fenster wird initialisiert mit Konstruktor der Elternklasse
    def __init__(self):
        super().__init__()

        # Titel
        self.setWindowTitle("Bildkompression")

        # Gräße
        self.showMaximized()

        # Layout, dass Widgets automatisch anordnet
        layout = QVBoxLayout()

        # einfache Textanzeige
        self.label = QLabel("Simulation")

        # Button wird initialisiert
        button = QPushButton("Klick")
        # Button wird geklickt
        button.clicked.connect(self.click)

        # Reihenfolge der Widgets (oben nach unten)
        layout.addWidget(self.label)
        layout.addWidget(button)

        # Layout dem Fenster zuweisen
        self.setLayout(layout)

    # Button wird geklickt
    def click(self):
        text = lauf_code()
        self.label.setText(text)
