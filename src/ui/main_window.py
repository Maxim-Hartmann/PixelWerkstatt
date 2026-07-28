"""
Führt alle Widgets im Hauptfenster zusammen.
"""

from PySide6.QtWidgets import (
    QFileDialog,
    QMenu,
    QHBoxLayout,
    QPushButton,
    QButtonGroup,
    QVBoxLayout,
    QWidget,
    QLabel,
    QTextEdit,
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt, Signal
from ui.color_picker import ColorPicker
from ui.pixel_editor import PixelEditor
from core.encoding import *
from core.bit_analysis import *
from core.file_io import read_file, clean_html
from config import text_style, select_color


class MainWindow(QWidget):
    """
    Hauptfenster der Anwendung.

    Koordiniert die UI-Komponenten und steuert die aktive Codierung
    sowie Benutzerinteraktion.
    """

    # Sendet alle Pixel einer ausgewählten Lauflänge an PixelEditor.
    send_selected_pixels = Signal(list)

    def __init__(self):
        super().__init__()

        # aktive Codierung
        self.active_encode = "rgb"
        # RLE Zeilenübergreifend
        self.rle_lines_on = True

        # ----------------------------------------
        # Fenstereinstellungen
        # ----------------------------------------

        self.setWindowTitle("PixelWerkstatt")
        self.setWindowIcon(QIcon("assets/Icon_chess.png"))

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

        self.button_settings = QPushButton("⚙️")
        self.button_settings.setToolTip("Einstellungen")

        self.button_detective = QPushButton("🔎")
        self.button_detective.setToolTip("Pixel-Detektiv")
        self.button_detective.setCheckable(True)

        self.button_rgb = QPushButton("RGB")
        self.button_rgb.setToolTip("RGB-Codierung")
        self.button_rgb.setCheckable(True)

        self.button_rle = QPushButton("RLE")
        self.button_rle.setToolTip("Lauflängen-Codierung")
        self.button_rle.setCheckable(True)

        self.button_clr = QPushButton("CLR")
        self.button_clr.setToolTip("Indizierte-Farben-Codierung")
        self.button_clr.setCheckable(True)

        self.button_new = QPushButton("Neu")
        self.button_save = QPushButton("Speichern")
        self.button_load = QPushButton("Laden")

        self.encode_buttons = QButtonGroup(self)
        self.encode_buttons.addButton(self.button_rgb)
        self.encode_buttons.addButton(self.button_rle)
        self.encode_buttons.addButton(self.button_clr)
        self.encode_buttons.setExclusive(True)

        # ----------------------------------------
        # Button-Aufrufe
        # ----------------------------------------

        self.button_settings.clicked.connect(self.set_settings)
        self.button_detective.clicked.connect(self.activate_select_mode)
        self.button_new.clicked.connect(self.new_image)
        self.button_save.clicked.connect(self.save_image)
        self.button_load.clicked.connect(self.load_image)
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
        self.label_byte_percent = QLabel()
        self.label_byte_comp = QLabel()
        self.label_byte_size = QLabel()
        self.label_bits_opt_a = QLabel()
        self.label_byte_opt_b = QLabel()

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
        self.left_down_layout.addWidget(self.button_settings)
        self.left_down_layout.addSpacing(10)
        self.left_down_layout.addWidget(self.button_detective)
        self.left_down_layout.addSpacing(10)
        self.left_down_layout.addWidget(self.button_rgb)
        self.left_down_layout.addWidget(self.button_rle)
        self.left_down_layout.addWidget(self.button_clr)
        self.left_down_layout.addSpacing(10)
        self.left_down_layout.addWidget(self.button_new)
        self.left_down_layout.addWidget(self.button_save)
        self.left_down_layout.addWidget(self.button_load)
        self.right_up_layout.addWidget(self.text_sim)
        self.right_down_layout.addWidget(self.label_byte_bar)
        self.right_down_layout.addWidget(self.label_byte_percent)
        self.right_down_layout.addWidget(self.label_byte_comp)
        self.right_down_layout.addWidget(self.label_byte_size)
        self.right_down_layout.addWidget(self.label_bits_opt_a)
        self.right_down_layout.addWidget(self.label_byte_opt_b)

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
        # UI-Vermittlung
        # ----------------------------------------

        self.color_picker.send_new_color.connect(self.change_color)
        self.pixel_editor.send_selected_pixel.connect(self.text_update)
        self.pixel_editor.send_painted_pixel.connect(self.text_update)
        self.send_selected_pixels.connect(self.pixel_editor.set_selected_pixels)

        # ----------------------------------------
        # Stylesheet
        # ----------------------------------------

        self.setStyleSheet("""
            QPushButton {
                font-weight: 800;
                background-color: rgb(80, 80, 80);
                color: white;
                padding: 5px;
                border-radius: 5px;
                border: 2px solid rgb(80, 80, 80);
            }
            QPushButton:hover {
                background-color: rgb(40, 40, 40);
            }
            QPushButton:pressed {
                background-color: rgb(20, 20, 20);
            }
            QPushButton:checked {
            background-color: rgb(80, 80, 80);
            border: 2px solid rgb(180, 180, 180);
            }
            QLabel {
                color: gray;
                font-size: 11pt;
                font-family: Cascadia Code, Consolas, monospace;
                padding: 5px;
            }
            """)

    # ----------------------------------------
    # Funktionen der UI-Vermittlung
    # ----------------------------------------

    def change_color(self, color: int) -> None:
        """
        Wechselt zur neu ausgewählten Farbe.

        Args:
            color: Farbindex der aktuell ausgewählten Farbe.
        """
        self.pixel_editor.current_color = color
        if self.pixel_editor.mode == "select":
            self.pixel_editor.mode = "paint"
            self.pixel_editor.pixel_row_col = None
            self.button_detective.setChecked(False)
            self.pixel_editor.update()
            self.text_update()

    # ----------------------------------------
    # Funktionen für Button-Aufrufe
    # ----------------------------------------

    def set_settings(self) -> None:
        """
        Ausgewählte Einstellungen können angepasst werden.

        - 6:8 Raster
        - 9:12 Raster
        - RLE Zeilenübergreifend an/aus
        """
        settings_menu = QMenu(self)
        action_s = QAction("6:8", self)
        action_l = QAction("9:12", self)
        action_rle = QAction("RLE Zeilenübergriff")
        action_rle.setCheckable(True)
        action_rle.setChecked(self.rle_lines_on)

        action_s.triggered.connect(self.set_small)
        action_l.triggered.connect(self.set_large)
        action_rle.triggered.connect(self.set_rle)
        settings_menu.addAction(action_s)
        settings_menu.addAction(action_l)
        settings_menu.addAction(action_rle)

        settings_pos = self.button_settings.rect().topLeft()
        window_pos = self.button_settings.mapToGlobal(settings_pos)
        window_pos.setY(window_pos.y() - 90)
        settings_menu.exec(window_pos)

    def set_rle(self, checked: bool) -> None:
        """
        Ändert den Zeilenübergriff der RLE-Codierung.

        Args:
            checked: True -> Zeilenübergriff, False -> kein Zeilenübergriff.
        """
        self.rle_lines_on = checked
        self.pixel_editor.update()
        self.text_update()

    def activate_select_mode(self) -> None:
        """
        De-/aktiviert den Select-Modus.
        """
        if self.pixel_editor.mode == "paint":
            self.button_detective.setChecked(True)
            self.pixel_editor.mode = "select"
        else:
            self.button_detective.setChecked(False)
            self.pixel_editor.mode = "paint"
            self.pixel_editor.pixel_row_col = None
        self.pixel_editor.update()
        self.text_update()

    def new_image(self) -> None:
        """
        Stellt ein weißes Bild im ausgewähltem Format her.
        """
        if self.pixel_editor.preset == "s":
            self.pixel_editor.set_preset("s")
        else:
            self.pixel_editor.set_preset("l")
        self.button_detective.setChecked(False)
        self.pixel_editor.mode = "paint"
        self.pixel_editor.pixel_row_col = None
        self.text_update()

    def set_small(self) -> None:
        """
        Setzt das Format auf "s".
        """
        self.pixel_editor.set_preset("s")
        self.button_detective.setChecked(False)
        self.pixel_editor.mode = "paint"
        self.pixel_editor.pixel_row_col = None
        self.text_update()

    def set_large(self) -> None:
        """
        Setzt das Format auf "l".
        """
        self.pixel_editor.set_preset("l")
        self.button_detective.setChecked(False)
        self.pixel_editor.mode = "paint"
        self.pixel_editor.pixel_row_col = None
        self.text_update()

    def save_image(self) -> None:
        """
        Speichert das Bild als Screenshot.
        """
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Pixel-Bild speichern",
            "Mein_Bild",
            "PixelWerkstatt-Datei (*.rgb);;PNG (*.png)",
        )
        if path:
            if path.endswith(".png"):
                file = self.pixel_editor.grab()
                file.save(path)
            else:
                rgb_text = rgb_to_string(
                    self.pixel_editor.rows,
                    self.pixel_editor.cols,
                    self.pixel_editor.pixel_data,
                    self.pixel_editor.color_index,
                    self.pixel_editor.pixel_row_col,
                )
                rgb_text = rgb_text.replace("<br>", "\n")
                file_text = clean_html(rgb_text)
                with open(path, "w", encoding="utf-8") as file:
                    file.write(file_text)

    def load_image(self) -> None:
        """
        Zeigt eine PixelWerkstatt-Datei im Editor an.
        """
        path, _ = QFileDialog.getOpenFileName(
            self, "Datei öffnen", "", "PixelWerkstatt-Datei (*.rgb)"
        )
        if path:
            preset, pixel_data = read_file(path)
            if self.pixel_editor.mode == "select":
                self.activate_select_mode()
            self.pixel_editor.set_preset(preset, pixel_data)
            self.text_update()

    def rgb_clicked(self) -> None:
        """
        Zeigt die RGB-Codierung an.
        """
        self.active_encode = "rgb"
        self.button_rgb.setChecked(True)

        rgb_text = rgb_to_string(
            self.pixel_editor.rows,
            self.pixel_editor.cols,
            self.pixel_editor.pixel_data,
            self.pixel_editor.color_index,
            self.pixel_editor.pixel_row_col,
        )
        self.text_sim.setHtml(f"<span style ={text_style}>{rgb_text}</span>")

        rgb_bit_label = rgb_to_bit(
            self.pixel_editor.image_bits, self.pixel_editor.rows, self.pixel_editor.cols
        )
        self.set_label(rgb_bit_label)

    def rle_clicked(self) -> None:
        """
        Zeigt die Lauflängen-Codierungan an.
        """
        self.active_encode = "rle"
        self.button_rle.setChecked(True)

        rle_data, pos_to_number, number_to_pos = encode_rle(
            self.pixel_editor.pixel_data, self.rle_lines_on
        )

        if (
            self.pixel_editor.mode == "select"
            and self.pixel_editor.pixel_row_col is not None
        ):
            selected_rle = pos_to_number[self.pixel_editor.pixel_row_col]
            selected_pixels = number_to_pos[selected_rle]
            self.send_selected_pixels.emit(selected_pixels)

        rle_text = rle_to_string(
            self.pixel_editor.rows,
            self.pixel_editor.cols,
            rle_data,
            self.pixel_editor.color_index,
            self.pixel_editor.pixel_row_col,
            pos_to_number,
        )
        self.text_sim.setHtml(f"<span style ={text_style}>{rle_text}</span>")

        run_length_count = len(rle_data)
        run_length_length = [count for count, _ in rle_data]
        rle_bit_label = rle_to_bit(
            self.pixel_editor.image_bits,
            run_length_count,
            run_length_length,
            self.pixel_editor.rows,
            self.pixel_editor.cols,
        )
        self.set_label(rle_bit_label)

    def clr_clicked(self) -> None:
        """
        Zeigt die Indizierten-Farben-Codierung an.
        """
        self.active_encode = "clr"
        self.button_clr.setChecked(True)

        clr_data, clr_codes, code_length = encode_clr(self.pixel_editor.pixel_data)

        clr_text = clr_to_string(
            self.pixel_editor.rows,
            self.pixel_editor.cols,
            clr_data,
            clr_codes,
            self.pixel_editor.color_index,
            self.pixel_editor.pixel_row_col,
        )
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

    def text_update(self) -> None:
        """
        Updatet gesammten Text. Simuliert einen Klick auf aktuelle Codierung.
        """
        if self.active_encode == "rgb":
            self.rgb_clicked()
        elif self.active_encode == "rle":
            self.rle_clicked()
        else:
            self.clr_clicked()

    def set_label(self, bit_label: tuple[str, str, str, str, str, str]) -> None:
        """
        Setzt die jeweiligen Strings auf die Label der Datenanzeige.

        Args:
            bit_label: Tupel aller Strings die als Label angezeigt werden sollen.
        """
        self.label_byte_bar.setText(bit_label[0])
        self.label_byte_percent.setText(bit_label[1])
        self.label_byte_comp.setText(bit_label[2])
        self.label_byte_size.setText(bit_label[3])
        self.label_bits_opt_a.setText(bit_label[4])
        self.label_byte_opt_b.setText(bit_label[5])
        self.pixel_editor.update()
