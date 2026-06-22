from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from ui.color_picker import ColorPicker
from ui.pixel_editor import PixelEditor

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
        # self.setStyleSheet("background-color: rgb(100, 100, 100);")

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

        self.left_up_layout = QVBoxLayout()
        self.left_up_layout.setContentsMargins(0, 0, 0, 0)
        self.left_up_layout.setSpacing(0)
        self.left_up_layout.setAlignment(Qt.AlignCenter)

        self.left_down_layout = QHBoxLayout()
        self.left_down_layout.setContentsMargins(0, 0, 0, 0)
        self.left_down_layout.setSpacing(0)
        self.left_down_layout.setAlignment(Qt.AlignCenter)

        # Layout für rechte Seite
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)

        self.right_up_layout = QVBoxLayout()
        self.right_up_layout.setContentsMargins(10, 10, 10, 10)
        self.right_up_layout.setSpacing(10)
        self.right_up_layout.setAlignment(Qt.AlignCenter)

        self.right_down_layout = QVBoxLayout()
        self.right_down_layout.setContentsMargins(10, 10, 10, 10)
        self.right_down_layout.setSpacing(10)
        self.right_down_layout.setAlignment(Qt.AlignCenter)

        #-----------------------------------------
        # Buttons
        #-----------------------------------------

        self.button_rle = QPushButton("Lauflaenge")
        self.button_clr = QPushButton("Code-Effizienz")
        self.button_s = QPushButton("6:8")
        self.button_l = QPushButton("9:12")
        self.button_new = QPushButton("Neu")
        self.button_save = QPushButton("Speichern")

        #-----------------------------------------
        # Button-Aufrufe
        #-----------------------------------------

        self.button_new.clicked.connect(self.new_image)
        self.button_s.clicked.connect(self.set_small)
        self.button_l.clicked.connect(self.set_large)

        #-----------------------------------------
        # Labels
        #-----------------------------------------

        self.label_data = QLabel("(Datenanzeige)")
        self.label_data.setFont(QFont("Arial", 20))

        #-----------------------------------------
        # Widgets
        #-----------------------------------------

        self.pixel_editor = PixelEditor()
        self.color_picker = ColorPicker()

        #-----------------------------------------
        # Widgets dem Layout hinzufügen
        #-----------------------------------------

        self.left_up_layout.addWidget(self.pixel_editor)
        self.left_down_layout.addWidget(self.button_clr)
        self.left_down_layout.addWidget(self.button_rle)
        self.left_down_layout.addWidget(self.button_s)
        self.left_down_layout.addWidget(self.button_l)
        self.left_down_layout.addWidget(self.button_new)
        self.left_down_layout.addWidget(self.button_save)
        self.right_down_layout.addWidget(self.label_data)
        self.right_up_layout.addWidget(self.color_picker)

        #-----------------------------------------
        # Layout dem Fenster zuweisen
        #-----------------------------------------

        self.left_layout.addLayout(self.left_up_layout, 9)
        self.left_layout.addLayout(self.left_down_layout, 1)
        self.right_layout.addLayout(self.right_up_layout, 1)
        self.right_layout.addLayout(self.right_down_layout, 1)
        self.main_layout.addLayout(self.left_layout, 2)
        self.main_layout.addLayout(self.right_layout, 1)
        self.setLayout(self.main_layout)

        #-----------------------------------------
        # Stylesheet
        #-----------------------------------------

        self.setStyleSheet("""

            QPushButton {
            background-color: rgb(60, 60, 60);
            color: white;
            padding: 6px;
            border: 1px solid black;
            }
                 
            QPushButton:hover {
                background-color: rgb(0, 0, 0);
            }
                           
            QPushButton:pressed {
                background-color: rgb(30, 30, 30);
            }

        """)

    #---------------------------------------------
    # Funktionen für Button-Aufrufe
    #---------------------------------------------

    def new_image(self):
        if self.pixel_editor.preset == "s":
            self.pixel_editor.set_preset("s")
        else:
            self.pixel_editor.set_preset("l")

    def set_small(self):
        self.pixel_editor.set_preset("s")

    def set_large(self):
        self.pixel_editor.set_preset("l")