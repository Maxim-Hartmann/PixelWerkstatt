from __future__ import annotations

"""
Erstellt das Pixel-Editor-Widget zur Bearbeitung von Bildern.
"""

from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent, QPaintEvent, QPainter, QPen
from PySide6.QtWidgets import QWidget

from config import COLOR_INDEX, EDITOR_GRID_SIZE, SELECT_COLOR, STANDARD_COLOR


class PixelEditor(QWidget):
    """
    Widget zum Erstellen und Bearbeiten eines Pixelbildes.

    Zeigt ein vorgefertigtes Raster mit Kacheln an, die angeklickt werden können.
    Beim Klicken ändert sich die Farbe der Kachel im Raster.
    """

    #: Sendet ein Signal, wenn im Auswahlmodus ein Pixel angeklickt wurde.
    send_selected_pixel = Signal()

    #: Sendet ein Signal, wenn im Malmodus ein Pixel eingefärbt wurde.
    send_painted_pixel = Signal()

    def __init__(self, preset: str = "s", parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # Voreinstellungen für das Raster setzen.
        self.set_preset(preset)

        #: Aktuell gewählter Farbindex zum Zeichnen.
        self.current_color = STANDARD_COLOR

        #: Mapping: Farbindex -> (QColor, Farbname).
        self.color_index = COLOR_INDEX

        #: Betriebsmodus des Editors ('paint' für Zeichnen, 'select' für Auswahl).
        self.mode = "paint"

        #: Aktuell ausgewählter Pixel als Tupel (Zeile, Spalte) oder None.
        self.pixel_row_col: tuple[int, int] | None = None

        #: Liste von Koordinaten-Tupeln der aktuell hervorgehobenen Pixel.
        self.selected_pixels: list[tuple[int, int]] = []

        # Stift für das Markieren des hervorgehobenen Pixels.
        self.select_pen = QPen()
        self.select_pen_width = 2 * self.gap
        self.select_pen.setWidth(self.select_pen_width)
        self.select_pen.setColor(SELECT_COLOR[0])

    def paintEvent(self, paint_event: QPaintEvent) -> None:
        """
        Zeichnet und aktualisiert den Pixel-Editor.

        Das Raster wird anhand der in ``pixel_data`` gespeicherten Farbindizes gerendert.

        Args:
            paint_event: Informationen über das aktuelle Zeichenereignis.
        """
        with QPainter(self) as painter:
            for row in range(self.rows):
                for col in range(self.cols):
                    index = self.pixel_data[row][col]
                    color = self.color_index[index][0]
                    painter.fillRect(
                        col * (self.pixel_size + self.gap) + self.gap,
                        row * (self.pixel_size + self.gap) + self.gap,
                        self.pixel_size,
                        self.pixel_size,
                        color,
                    )

            if self.mode == "select" and self.pixel_row_col is not None:
                painter.setPen(self.select_pen)
                if self.selected_pixels:
                    for row, col in self.selected_pixels:
                        painter.drawRect(
                            col * (self.pixel_size + self.gap) + self.gap,
                            row * (self.pixel_size + self.gap) + self.gap,
                            self.pixel_size,
                            self.pixel_size,
                        )
                    self.selected_pixels = []
                else:
                    painter.drawRect(
                        self.pixel_row_col[1] * (self.pixel_size + self.gap) + self.gap,
                        self.pixel_row_col[0] * (self.pixel_size + self.gap) + self.gap,
                        self.pixel_size,
                        self.pixel_size,
                    )

    def set_preset(
        self, preset: str, pixel_data: list[list[int]] | None = None
    ) -> None:
        """
        Setzt oder aktualisiert die Voreinstellungen für das Raster.

        Args:
            preset: Schlüssel ("s" oder "l") für die Auswahl der Voreinstellung.
            pixel_data: 2D-Liste mit Farbindizes, die das Bild abbilden.
        """
        self.mode = "paint"
        self.preset = preset
        self.rows = EDITOR_GRID_SIZE[preset]["rows"]
        self.cols = EDITOR_GRID_SIZE[preset]["cols"]
        self.gap = EDITOR_GRID_SIZE[preset]["pixel_gap"]
        self.pixel_size = EDITOR_GRID_SIZE[preset]["pixel_size"]

        # Metadaten (2 Byte = Höhe & Breite) + Unkomprimierte RGB-Daten (3 Byte pro Pixel)
        # (2 * 8 Bit) + (Zeilen * Spalten * 8 Bit * 3)
        self.image_bits = (2 * 8) + (self.rows * self.cols * 8 * 3)

        if pixel_data is not None:
            self.pixel_data = pixel_data
        else:
            self.pixel_data = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        self.setFixedSize(
            self.cols * (self.pixel_size + self.gap) + self.gap,
            self.rows * (self.pixel_size + self.gap) + self.gap,
        )
        self.update()

    def mousePressEvent(self, mouse_event: QMouseEvent) -> None:
        """
        Ermittelt das angeklickte Feld und sendet das entsprechende Signal.

        Args:
            mouse_event: Informationen über das aktuelle Mausereignis.
        """
        pos = mouse_event.position().toPoint()
        row = pos.y() // (self.pixel_size + self.gap)
        col = pos.x() // (self.pixel_size + self.gap)

        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.mode == "paint":
                self.pixel_data[row][col] = self.current_color
                self.send_painted_pixel.emit()
            else:
                self.pixel_row_col = (row, col)
                self.send_selected_pixel.emit()
            self.update()

    def set_selected_pixels(self, selected_pixels: list[tuple[int, int]]) -> None:
        """
        Setzt die ausgewählten Pixel für die Hervorhebung im Raster.

        Args:
            selected_pixels: Liste mit Koordinaten-Tupeln (Zeile, Spalte).
        """
        self.selected_pixels = selected_pixels
        self.update()