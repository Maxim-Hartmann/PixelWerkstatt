from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter


class PixelEditor(QWidget):
    def __init__(self):
        super().__init__()

        # Reihen und Spalten iniziieren
        self.rows = 9
        self.cols = 12
        # Pixelgröße
        self.pixel_size = 30
        # Fenstergröße passend zum Raster setzen
        #self.setFixedSize(self.cols * self.pixel_size, self.rows * self.pixel_size)
        self.setMinimumSize(self.cols * self.pixel_size, self.rows * self.pixel_size)

    # wird aufgerufen um das Widget zu zeichnen
    def paintEvent(self, event):
        # QPainter Objekt erstellen, um auf dem Widget zu zeichnen
        painter = QPainter(self)
        # Raster zeichnen
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.pixel_size
                y = row * self.pixel_size
                painter.drawRect(x, y, self.pixel_size, self.pixel_size)