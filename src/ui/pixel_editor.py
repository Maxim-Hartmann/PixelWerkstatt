"""
Erstellt das Pixel-Editor-Widget zur Bearbeitung von Bildern.
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPaintEvent, QMouseEvent, QPen
from PySide6.QtCore import Signal
import numpy as np
from config import editor_grid_size, standard_color, color_index, select_color


class PixelEditor(QWidget):
    """
    Widget zum erstellen eines Bildes.

    Zeigt ein vorgefärtigtes Raster mit Kacheln die angeklickt werden können.
    Beim klicken ändert sich die Farbe des Rasters.
    """

    # Pixel-Auswahl-Signal.
    pixel_selected = Signal()
    # Pixel-Mal-Siganl
    pixel_painted = Signal()

    def __init__(self, preset="s"):
        super().__init__()

        # Voreinstellungen für das Raster setzen
        self.set_preset(preset)
        # aktuelle Farbe
        self.current_color = standard_color
        # Farbindex
        self.color_index = color_index
        # Mal- (paint) oder Auswähl-Modus (select)
        self.mode = "paint"
        # aktuell ausgewählter Pixel
        self.pixel_row_col = None
        # Stift für das Markieren des hervorgehobenen Pixels
        self.select_pen = QPen()
        self.select_pen_width = 2 * self.gap
        self.select_pen.setWidth(self.select_pen_width)
        self.select_pen.setColor(select_color[0])

    def paintEvent(self, paint_event: QPaintEvent) -> None:
        """
        Zeichnet/Updatet den Pixel-Editor.
        Das Raster wird durch die Informationen in pixel_data gezeichnet.

        Args:
            paint_event: Informationen über aktuelles Zeichenereignis.
        """
        painter = QPainter(self)
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
            painter.drawRect(
                self.pixel_row_col[1] * (self.pixel_size + self.gap) + self.gap,
                self.pixel_row_col[0] * (self.pixel_size + self.gap) + self.gap,
                self.pixel_size,
                self.pixel_size,
            )

    def set_preset(self, preset: str) -> None:
        """
        Setzt/Updatet die Voreinstellungen für das Raster.

        Args:
            preset: Key für die Auswahl der richtigen Voreinstellungen.
        """
        self.mode = "paint"
        self.preset = preset
        self.rows = editor_grid_size[preset]["rows"]
        self.cols = editor_grid_size[preset]["cols"]
        self.gap = editor_grid_size[preset]["pixel_gap"]
        self.pixel_size = editor_grid_size[preset]["pixel_size"]
        # Meta-Daten werden als jeweils ein Byte gespeichert -> (Höhe und Breite)
        # (Höhe + Breite) + (Reihen * Spalten * 8 Bit * 3 RGB)
        self.image_bits = (2 * 8) + (self.rows * self.cols * 8 * 3)
        # Pixel-Datenliste erstellen und mit 0en füllen
        self.pixel_data = np.zeros((self.rows, self.cols), dtype=int)
        self.setFixedSize(
            self.cols * (self.pixel_size + self.gap) + self.gap,
            self.rows * (self.pixel_size + self.gap) + self.gap,
        )
        self.update()

    def mousePressEvent(self, mouse_event: QMouseEvent) -> None:
        """
        Ermittelt das angeklickte Feld und gibt dieses an paint() oder select() weiter.

        Args:
            mouse_event: Enthält Informationen über den Mausklick.
        """
        pos = mouse_event.position().toPoint()
        row = pos.y() // (self.pixel_size + self.gap)
        col = pos.x() // (self.pixel_size + self.gap)
        if self.mode == "paint":
            self.paint(row, col)
        else:
            self.select(row, col)
        self.update()

    def paint(self, row, col):
        self.pixel_data[row][col] = self.current_color
        self.pixel_painted.emit()

    def select(self, row, col):
        self.pixel_row_col = (row, col)
        self.pixel_selected.emit()
