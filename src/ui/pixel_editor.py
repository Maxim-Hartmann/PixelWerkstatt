from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter
import numpy as np
from config import editor_grid_size, standard_color, color_index


class PixelEditor(QWidget):
    """
    Widget zum erstellen eines Pixelbildes.

    Zeigt ein vorgefärtigtes Raster mit Kacheln die angeklickt werden können.
    Beim klicken ändert sich die Farbe des Rasters.
    """

    def __init__(self, preset="s"):
        super().__init__()

        # Voreinstellungen für das Raster setzen
        self.set_preset(preset)

        # aktuelle Farbe
        self.current_color = standard_color
        # Farbindex
        self.color_index = color_index

    def paintEvent(self, event):
        """
        Zeichnet/Updatet den Pixel-Editor.
        Das Raster wird durch die Informationen in pixel_data gezeichnet.
        """
        painter = QPainter(self)
        for row in range(self.rows):
            for col in range(self.cols):
                index = self.pixel_data[row][col]
                color = self.color_index[index][0]
                painter.fillRect(
                    col * (self.pixel_size + self.gap),
                    row * (self.pixel_size + self.gap),
                    self.pixel_size,
                    self.pixel_size,
                    color,
                )

    def set_preset(self, preset):
        """
        Setzt die Voreinstellungen für das Raster
        """
        self.preset = preset
        self.rows = editor_grid_size[preset]["rows"]
        self.cols = editor_grid_size[preset]["cols"]
        self.gap = editor_grid_size[preset]["pixel_gap"]
        self.pixel_size = editor_grid_size[preset]["pixel_size"]
        # Meta-Daten werden als jeweils ein Byte gespeichert (Höhe und Breite)
        # (Höhe + Breite) + (Reihen * Spalten * 8 Bit * 3 RGB)
        self.image_bits = (2 * 8) + (self.rows * self.cols * 8 * 3)
        # Pixel-Datenliste erstellen und mit 0en füllen
        self.pixel_data = np.zeros((self.rows, self.cols), dtype=int)
        self.setFixedSize(
            self.cols * (self.pixel_size + self.gap) - self.gap,
            self.rows * (self.pixel_size + self.gap) - self.gap,
        )
        self.update()

    def mousePressEvent(self, event):
        """
        Ermittelt das angeklickte Raster und ändert die Farbe zur aktuell ausgewählten
        """
        pos = event.position().toPoint()
        row = pos.y() // (self.pixel_size + self.gap)
        col = pos.x() // (self.pixel_size + self.gap)
        self.pixel_data[row][col] = self.current_color
        self.update()
