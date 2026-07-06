from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QLabel, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from ui.color_picker import ColorPicker
from ui.pixel_editor import PixelEditor
from core.encoding import *
from config import text_style

# Hauptfenster
class MainWindow(QWidget):
    """
    Hauptfenster der Anwendung.

    Koordiniert die UI-Komponenten und steuert die aktive Codierung sowie Benutzerinteraktion.
    """

    def __init__(self):
        super().__init__()

        # aktive Codierung
        self.active_encode = None

        #----------------------------------------
        # Fenstereinstellungen
        #----------------------------------------

        self.setWindowTitle("Komprimierung Tool")

        #----------------------------------------
        # Layouts
        #----------------------------------------

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
        self.left_up_layout.setSpacing(10)
        self.left_up_layout.setAlignment(Qt.AlignCenter)

        self.left_middle_layout = QVBoxLayout()
        self.left_middle_layout.setContentsMargins(10, 10, 10, 10)
        self.left_middle_layout.setSpacing(0)
        self.left_middle_layout.setAlignment(Qt.AlignCenter)

        self.left_down_layout = QHBoxLayout()
        self.left_down_layout.setContentsMargins(0, 0, 0, 0)
        self.left_down_layout.setSpacing(10)
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

        #----------------------------------------
        # Buttons
        #----------------------------------------

        self.button_rgb = QPushButton("RGB")
        self.button_rle = QPushButton("Lauflaenge")
        self.button_clr = QPushButton("Indizierte Farbe")
        self.button_s = QPushButton("6:8")
        self.button_l = QPushButton("9:12")
        self.button_new = QPushButton("Neu")
        self.button_save = QPushButton("Speichern")

        #----------------------------------------
        # Button-Aufrufe
        #----------------------------------------

        self.button_new.clicked.connect(self.new_image)
        self.button_s.clicked.connect(self.set_small)
        self.button_l.clicked.connect(self.set_large)
        self.button_save.clicked.connect(self.save_image)
        self.button_rgb.clicked.connect(self.rgb_clicked)
        self.button_rle.clicked.connect(self.rle_clicked)
        self.button_clr.clicked.connect(self.clr_clicked)

        #----------------------------------------
        # Textfelder und Labels
        #----------------------------------------

        self.text_sim = QTextEdit("Zeichne ein Bild 🖌️")
        self.text_sim.setFont(QFont("Cascadia Code, Consolas, monospace", 20))
        self.text_sim.setReadOnly(True)
        self.label_data = QLabel("Datenanzeige")
        self.label_data.setFont(QFont("Cascadia Code, Consolas, monospace", 20, 1000))

        #----------------------------------------
        # UI-Elemente
        #----------------------------------------

        self.pixel_editor = PixelEditor()
        self.color_picker = ColorPicker()

        #----------------------------------------
        # Widgets dem Layout hinzufügen
        #----------------------------------------

        self.left_up_layout.addWidget(self.pixel_editor)
        self.left_middle_layout.addWidget(self.color_picker)
        self.left_down_layout.addWidget(self.button_rgb)
        self.left_down_layout.addWidget(self.button_rle)
        self.left_down_layout.addWidget(self.button_clr)
        self.left_down_layout.addSpacing(30)
        self.left_down_layout.addWidget(self.button_s)
        self.left_down_layout.addWidget(self.button_l)
        self.left_down_layout.addSpacing(30)
        self.left_down_layout.addWidget(self.button_new)
        self.left_down_layout.addWidget(self.button_save)
        self.right_up_layout.addWidget(self.text_sim)
        self.right_down_layout.addWidget(self.label_data)

        #----------------------------------------
        # Layouts zuweisen
        #----------------------------------------

        self.left_layout.addLayout(self.left_up_layout, 9)
        self.left_layout.addLayout(self.left_middle_layout, 1)
        self.left_layout.addLayout(self.left_down_layout, 1)
        self.right_layout.addLayout(self.right_up_layout, 1)
        self.right_layout.addLayout(self.right_down_layout, 1)
        self.main_layout.addLayout(self.left_layout, 3)
        self.main_layout.addLayout(self.right_layout, 2)
        self.setLayout(self.main_layout)

        #----------------------------------------
        # Stylesheet
        #----------------------------------------

        self.setStyleSheet("""

            QPushButton {
            background-color: rgb(60, 60, 60);
            color: white;
            padding: 5px;
            border: 1px solid black;
            }
                 
            QPushButton:hover {
                background-color: rgb(0, 0, 0);
            }
                           
            QPushButton:pressed {
                background-color: rgb(30, 30, 30);
            }

        """)

        #----------------------------------------
        # UI-Vermittlung
        #----------------------------------------        
        
        self.color_picker.new_color.connect(self.change_color)

    #----------------------------------------
    # Funktionen für Button-Aufrufe
    #----------------------------------------

    def new_image(self):
        """
        Stellt ein weißes Bild im ausgewähltem Format her.
        """
        if self.pixel_editor.preset == "s":
            self.pixel_editor.set_preset("s")
        else:
            self.pixel_editor.set_preset("l")

    def set_small(self):
        """
        setzt das Format auf "s".
        """
        self.pixel_editor.set_preset("s")

    def set_large(self):
        """
        setzt das Format auf "l".
        """
        self.pixel_editor.set_preset("l")

    def save_image(self):
        """
        Speichert das Pixel-Bild als Screenshot.
        """
        path, _ = QFileDialog.getSaveFileName(self,
        "Pixel-Bild speichern",
        "Mein_Bild",
        "PNG (*.png);;JPEG (*.jpg);;Alle Dateien (*)")
        if path:
            image = self.pixel_editor.grab()
            image.save(path)

    def rgb_clicked(self):
        """
        zeigt die RGB-Codierung an.
        """
        # self.active_encode = "rgb"
        # rgb_analysis = ...
        rgb_text = f"{self.pixel_editor.rows} <span style='color:gray'>#Höhe</span>, {self.pixel_editor.cols} <span style='color:gray'>#Breite</span><br><br>"
        rgb_text += rgb_to_string(self.pixel_editor.pixel_data, self.pixel_editor.color_index)
        self.text_sim.setHtml(f"<span style ={text_style}>{rgb_text}</span>")

    def rle_clicked(self):
        """
        zeigt die Lauflängen-Codierungan an.
        """
        # self.active_encode = "rle"
        rle_text = f"{self.pixel_editor.rows} <span style='color:gray'>#Höhe</span>, {self.pixel_editor.cols} <span style='color:gray'>#Breite</span><br><br>"
        rle_data = encode_rle(self.pixel_editor.pixel_data)
        # rle_analysis = ...
        rle_text += rle_to_string(rle_data, self.pixel_editor.color_index)
        self.text_sim.setHtml(f"<span style ={text_style}>{rle_text}</span>")

    def clr_clicked(self):
        """
        zeigt die Indizierten-Farben-Codierung an.
        """
        # self.active_encode = "clr"
        clr_data_and_codes = encode_clr(self.pixel_editor.pixel_data)
        clr_data = clr_data_and_codes[0]
        clr_codes = clr_data_and_codes[1]
        # clr_analysis = ...
        clr_text = f"{self.pixel_editor.rows} <span style='color:gray'>#Höhe</span>, {self.pixel_editor.cols} <span style='color:gray'>#Breite</span><br><br>"
        clr_text += clr_to_string(clr_data, clr_codes, self.pixel_editor.color_index)
        self.text_sim.setHtml(f"<span style ={text_style}>{clr_text}</span>")

    #----------------------------------------
    # Funktionen für UI-Vermittlung
    #----------------------------------------

    def change_color(self, color):
        """
        wechselt zur neu ausgewählten Farbe.
        """
        self.pixel_editor.current_color = color