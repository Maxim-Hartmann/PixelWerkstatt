from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
import numpy as np
from config import grid_size


class PixelEditor(QWidget):
    def __init__(self,  preset="s"):
        super().__init__()

        # Voreinstellungen für das Raster setzen
        self.set_preset(preset)

    # wird aufgerufen um das Widget zu zeichnen
    def paintEvent(self, event):
        # QPainter Objekt erstellen, um auf dem Widget zu zeichnen
        painter = QPainter(self)
        # Quadrat-Raster wird gezeichnet
        for row in range(self.rows):
            for col in range(self.cols):
                painter.fillRect(col * (self.pixel_size + 2), row * (self.pixel_size + 2), self.pixel_size, self.pixel_size, QColor(255, 255, 255))

    # Voreinstellungen für das Raster setzen
    def set_preset(self, preset):
        # Speichern der Preset-Auswahl
        self.preset = preset
        # Reihen und Spalten iniziieren
        self.rows = grid_size[preset]["rows"]
        self.cols = grid_size[preset]["cols"]
        # Pixelgröße
        self.pixel_size = grid_size[preset]["pixel_size"]
        # Liste erstellen
        self.pixel_data = np.zeros((self.rows, self.cols), dtype = int)
        # Widgetgröße passend zum Raster setzen
        self.setFixedSize(self.cols * (self.pixel_size + 2), self.rows * (self.pixel_size + 2))
        self.update()