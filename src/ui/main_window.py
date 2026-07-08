from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QTextEdit,
)
from PySide6.QtCore import Qt
from ui.color_picker import ColorPicker
from ui.pixel_editor import PixelEditor
from core.encoding import *
from core.bit_analysis import *
from config import text_style


class MainWindow(QWidget):
    """
    Hauptfenster der Anwendung.
    Koordiniert die UI-Komponenten und steuert die aktive Codierung sowie Benutzerinteraktion.
    """

    def __init__(self):
        super().__init__()

        # aktive Codierung
        self.active_encode = 0

        # ----------------------------------------
        # Fenstereinstellungen
        # ----------------------------------------

        self.setWindowTitle("Komprimierung Tool")

        # ----------------------------------------
        # Layouts
        # ----------------------------------------

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

        # ----------------------------------------
        # Buttons
        # ----------------------------------------

        self.button_rgb = QPushButton(".rgb")
        self.button_rgb.setToolTip("RGB-Codierung")
        self.button_rle = QPushButton(".rle")
        self.button_rle.setToolTip("Lauflängen-Codierung")
        self.button_clr = QPushButton(".clr")
        self.button_clr.setToolTip("Indizierte-Farben-Codierung")
        self.button_s = QPushButton("6:8")
        self.button_l = QPushButton("9:12")
        self.button_new = QPushButton("Neu")
        self.button_save = QPushButton("Speichern")

        # ----------------------------------------
        # Button-Aufrufe
        # ----------------------------------------

        self.button_new.clicked.connect(self.new_image)
        self.button_s.clicked.connect(self.set_small)
        self.button_l.clicked.connect(self.set_large)
        self.button_save.clicked.connect(self.save_image)
        self.button_rgb.clicked.connect(self.rgb_clicked)
        self.button_rle.clicked.connect(self.rle_clicked)
        self.button_clr.clicked.connect(self.clr_clicked)

        # ----------------------------------------
        # Textfelder und Labels
        # ----------------------------------------

        self.text_sim = QTextEdit(f"<span style ={text_style}>Male etwas ...</span>")
        self.text_sim.setReadOnly(True)
        self.label_byte_bar = QLabel(
            "[________________________________________________]"
        )
        self.label_byte_percent = QLabel("#Prozentuale Datenersparnis")
        self.label_byte_comp = QLabel("#Kompressionsverhältnis")
        self.label_byte_size = QLabel("#Dateigröße")
        self.label_bits_pixel = QLabel("#Bit pro Pixel")
        self.label_byte_opt = QLabel()

        # ----------------------------------------
        # UI-Elemente
        # ----------------------------------------

        self.pixel_editor = PixelEditor()
        self.color_picker = ColorPicker()

        # ----------------------------------------
        # Widgets dem Layout hinzufügen
        # ----------------------------------------

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
        self.right_down_layout.addWidget(self.label_byte_bar)
        self.right_down_layout.addWidget(self.label_byte_percent)
        self.right_down_layout.addWidget(self.label_byte_comp)
        self.right_down_layout.addWidget(self.label_byte_size)
        self.right_down_layout.addWidget(self.label_bits_pixel)
        self.right_down_layout.addWidget(self.label_byte_opt)

        # ----------------------------------------
        # Layouts zuweisen
        # ----------------------------------------

        self.left_layout.addLayout(self.left_up_layout, 9)
        self.left_layout.addLayout(self.left_middle_layout, 1)
        self.left_layout.addLayout(self.left_down_layout, 1)
        self.right_layout.addLayout(self.right_up_layout, 2)
        self.right_layout.addLayout(self.right_down_layout, 1)
        self.main_layout.addLayout(self.left_layout, 3)
        self.main_layout.addLayout(self.right_layout, 2)
        self.setLayout(self.main_layout)

        # ----------------------------------------
        # Stylesheet
        # ----------------------------------------

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

                           QLabel {
                           color: gray;
                           font-size: 11pt;
                           font-family: Cascadia Code, Consolas, monospace;
                           padding: 5px;
                           }
                           
                           """)

        # ----------------------------------------
        # UI-Vermittlung
        # ----------------------------------------

        self.color_picker.new_color.connect(self.change_color)

    # ----------------------------------------
    # Funktionen für Button-Aufrufe
    # ----------------------------------------

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
        Setzt das Format auf "s".
        """
        self.pixel_editor.set_preset("s")

    def set_large(self):
        """
        Setzt das Format auf "l".
        """
        self.pixel_editor.set_preset("l")

    def save_image(self):
        """
        Speichert das Bild als Screenshot.
        """
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Pixel-Bild speichern",
            "Mein_Bild",
            "PNG (*.png);;JPEG (*.jpg);;Alle Dateien (*)",
        )
        if path:
            image = self.pixel_editor.grab()
            image.save(path)

    def rgb_clicked(self):
        """
        Zeigt die RGB-Codierung an.
        """
        self.active_encode = 0  # rgb
        rgb_text = f"{self.pixel_editor.rows:08b} <span style='color:gray'>#Höhe</span>, {self.pixel_editor.cols:08b} <span style='color:gray'>#Breite</span><br>"
        rgb_text += rgb_to_string(
            self.pixel_editor.pixel_data, self.pixel_editor.color_index
        )
        self.text_sim.setHtml(f"<span style ={text_style}>{rgb_text}</span>")
        rgb_bit_label = rgb_to_bit(
            self.pixel_editor.image_bits, self.pixel_editor.rows, self.pixel_editor.cols
        )
        self.set_label(rgb_bit_label)

    def rle_clicked(self):
        """
        Zeigt die Lauflängen-Codierungan an.
        """
        self.active_encode = 1  # rle
        rle_text = f"{self.pixel_editor.rows:08b} <span style='color:gray'>#Höhe</span>, {self.pixel_editor.cols:08b} <span style='color:gray'>#Breite</span><br>"
        rle_data = encode_rle(self.pixel_editor.pixel_data)
        rle_text += rle_to_string(rle_data, self.pixel_editor.color_index)
        self.text_sim.setHtml(f"<span style ={text_style}>{rle_text}</span>")
        run_length_count = len(rle_data)
        run_length_length = [count for count, _ in rle_data]
        rle_bit_label = rle_to_bit(
            self.pixel_editor.image_bits, run_length_count, run_length_length
        )
        self.set_label(rle_bit_label)

    def clr_clicked(self):
        """
        Zeigt die Indizierten-Farben-Codierung an.
        """
        self.active_encode = 2  # clr
        clr_data_codes = encode_clr(self.pixel_editor.pixel_data)
        clr_data = clr_data_codes[0]
        clr_codes = clr_data_codes[1]
        code_length = clr_data_codes[2]
        clr_text = f"{self.pixel_editor.rows:08b} <span style='color:gray'>#Höhe</span>, {self.pixel_editor.cols:08b} <span style='color:gray'>#Breite</span>, {len(clr_codes):08b} <span style='color:gray'>#Farb-Anzahl</span><br><br>"
        clr_text += clr_to_string(clr_data, clr_codes, self.pixel_editor.color_index)
        self.text_sim.setHtml(f"<span style ={text_style}>{clr_text}</span>")
        color_count = len(clr_codes)
        clr_bit_label = clr_to_bit(
            self.pixel_editor.image_bits,
            color_count,
            code_length,
            self.pixel_editor.rows,
            self.pixel_editor.cols,
        )
        self.set_label(clr_bit_label)

    def set_label(self, bit_label: tuple[str, str, str, str, str, str]):
        """
        Setzt die jeweiligen Strings auf die Label der Datenanzeige.

        Args:
            bit_label: Tupel aller Strings die als Label angezeigt werden sollen.
        """
        self.label_byte_bar.setText(bit_label[0])
        self.label_byte_percent.setText(bit_label[1])
        self.label_byte_comp.setText(bit_label[2])
        self.label_byte_size.setText(bit_label[3])
        self.label_bits_pixel.setText(bit_label[4])
        self.label_byte_opt.setText(bit_label[5])

    # ----------------------------------------
    # Funktionen für UI-Vermittlung
    # ----------------------------------------

    def change_color(self, color: int):
        """
        Wechselt zur neu ausgewählten Farbe.

        Args:
            color: Farbindex der aktuell ausgewählten Farbe.
        """
        self.pixel_editor.current_color = color
