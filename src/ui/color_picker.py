from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter
from config import colors

class ColorPicker(QWidget):
    def __init__(self):
        super().__init__()

        # Reihen und Spalten inizieren
        self.rows = len(colors)
        self.cols = len(colors[0])
        # Pixelgröße
        self.pixel_size = 40
        # Widgetgröße passend zum Raster setzen
        self.setFixedSize(self.cols * (self.pixel_size + 10), self.rows * (self.pixel_size + 10))

    def paintEvent(self, event):
        painter = QPainter(self)
        for row in range(len(colors)):
            for col in range(len(colors[row])):
                color = colors[row][col]
                painter.fillRect(col * (self.pixel_size + 10), row * (self.pixel_size + 10), self.pixel_size, self.pixel_size, color)