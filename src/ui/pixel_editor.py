from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter
import numpy as np
from config import grid_size, standard_color, color_index


class PixelEditor(QWidget):
    def __init__(self,  preset="s"):
        super().__init__()

        # Voreinstellungen für das Raster setzen
        self.set_preset(preset)

        # aktuelle Farbe
        self.current_color = standard_color

        # Farbcodes
        self.color_index = color_index

    # wird aufgerufen um das Widget zu zeichnen
    def paintEvent(self, event):
        # QPainter Objekt erstellen, um auf dem Widget zu zeichnen
        painter = QPainter(self)
        # Quadrat-Raster wird gezeichnet
        for row in range(self.rows):
            for col in range(self.cols):
                index = self.pixel_data[row][col]
                color = self.color_index[index]
                painter.fillRect(col * (self.pixel_size + self.gap), row * (self.pixel_size + self.gap), self.pixel_size, self.pixel_size, color)

    # Voreinstellungen für das Raster setzen
    def set_preset(self, preset):
        # Speichern der Preset-Auswahl
        self.preset = preset
        # Reihen und Spalten
        self.rows = grid_size[preset]["rows"]
        self.cols = grid_size[preset]["cols"]
        # Pixelabstände
        self.gap = grid_size[preset]["pixel_gap"]
        # Pixelgröße
        self.pixel_size = grid_size[preset]["pixel_size"]
        # Pixel-Datenliste erstellen
        self.pixel_data = np.zeros((self.rows, self.cols), dtype = int)
        # Widgetgröße passend zum Raster setzen
        self.setFixedSize(self.cols * (self.pixel_size + self.gap) - self.gap, self.rows * (self.pixel_size + self.gap) - self.gap)
        self.update()

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        # print("x: " + str(pos.x()) + ", y: " + str(pos.y()))
        row = pos.y() // (self.pixel_size + self.gap)
        col = pos.x() // (self.pixel_size + self.gap)
        # print("row: " + str(row) + ", col: " + str(col))
        self.pixel_data[row][col] = self.current_color
        # print(self.pixel_data)
        self.update()