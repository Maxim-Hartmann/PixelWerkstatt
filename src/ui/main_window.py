from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QApplication, QMainWindow
from ui.pixel_editor import PixelEditor
from PySide6.QtCore import Qt

# Hauptfenster
class MainWindow(QWidget):
    def __init__(self):
        # Konstruktor der Elternklasse aufruft um das Fenster zu initialisieren.
        super().__init__()

        #-----------------------------------------
        # Fenstereinstellungen
        #-----------------------------------------

        # Fenstername
        self.setWindowTitle("Komprimierung Tool")

        #-----------------------------------------
        # Layouts
        #-----------------------------------------

        # Haupt-Layout
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # Layout für linke Seite
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(0)
        self.left_layout.setAlignment(Qt.AlignHCenter)

        # Layout für rechte Seite
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(10, 10, 10, 10)
        self.right_layout.setSpacing(10)

        #-----------------------------------------
        # Buttons
        #-----------------------------------------

        self.button_rle = QPushButton("Lauflaenge")
        self.button_farb = QPushButton("FARB")
        self.button_huffman = QPushButton("HUFFMAN")
        self.button_s = QPushButton("KLEIN")
        self.button_m = QPushButton("MITTEL")
        self.button_l = QPushButton("GROSS")
        self.button_new = QPushButton("NEU")
        self.button_save = QPushButton("SPEICHERN")
        
        #-----------------------------------------
        # Pixel Editor
        #-----------------------------------------

        self.pixel_editor = PixelEditor()

        #-----------------------------------------
        # Widgets dem Layout hinzufügen
        #-----------------------------------------

        self.left_layout.addStretch(1)
        self.left_layout.addWidget(self.pixel_editor)
        self.left_layout.addStretch(1)
        self.right_layout.addWidget(self.button_rle)
        self.right_layout.addWidget(self.button_farb)
        self.right_layout.addWidget(self.button_huffman)
        self.right_layout.addWidget(self.button_s)
        self.right_layout.addWidget(self.button_m)
        self.right_layout.addWidget(self.button_l)
        self.right_layout.addWidget(self.button_new)
        self.right_layout.addWidget(self.button_save)

        #-----------------------------------------
        # Layout dem Fenster zuweisen
        #-----------------------------------------

        self.main_layout.addLayout(self.left_layout, 2)
        self.main_layout.addLayout(self.right_layout, 1)
        self.setLayout(self.main_layout)