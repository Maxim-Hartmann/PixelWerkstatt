from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
from PySide6.QtCore import Qt
from config import size


class PixelEditor(QWidget):
    def __init__(self,  preset="l"):
        super().__init__()

        # Voreinstellungen für das Raster setzen
        self.set_preset(preset)

    # wird aufgerufen um das Widget zu zeichnen
    def paintEvent(self, event):
        # QPainter Objekt erstellen, um auf dem Widget zu zeichnen
        painter = QPainter(self)
        # # Stiftoptionen für Hintergrund
        # brush_background = QBrush(QColor(160, 160, 160))
        # # Hintergrund zeichnen
        # painter.setBrush(brush_background)
        # painter.drawRect(0, 0, self.cols * self.pixel_size, self.rows * self.pixel_size)
        # # Stiftoptionen für Raster
        # pen_grid = QPen()
        # pen_grid.setColor(Qt.darkGray)
        # pen_grid.setWidth(3)
        # Raster zeichnen
        # painter.setPen(pen_grid)
        # for row in range(self.rows):
        #     for col in range(self.cols):
        #         x = col * self.pixel_size
        #         y = row * self.pixel_size
        #         painter.drawRect(x, y, self.pixel_size, self.pixel_size)
        for row in range(self.rows):
            for col in range(self.cols):
                painter.fillRect(col * (self.pixel_size + 2), row * (self.pixel_size + 2), self.pixel_size, self.pixel_size, Qt.white)

    # Voreinstellungen für das Raster setzen
    def set_preset(self, preset):
        # Speichern der Preset-Auswahl
        self.preset = preset
        # Reihen und Spalten iniziieren
        self.rows = size[preset]["rows"]
        self.cols = size[preset]["cols"]
        # Pixelgröße
        self.pixel_size = size[preset]["pixel_size"]
        # Widgetgröße passend zum Raster setzen
        self.setFixedSize(self.cols * (self.pixel_size + 2), self.rows * (self.pixel_size + 2))
        self.update()