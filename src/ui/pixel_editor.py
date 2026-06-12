from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt


class PixelEditor(QWidget):
    def __init__(self):
        super().__init__()

        # Reihen und Spalten iniziieren
        self.rows = 16
        self.cols = 16
        # Pixelgröße
        self.pixel_size = 40
        # Fenstergröße passend zum Raster setzen
        #self.setFixedSize(self.cols * self.pixel_size, self.rows * self.pixel_size)
        self.setMinimumSize(self.cols * self.pixel_size + 40, self.rows * self.pixel_size + 40)

    # wird aufgerufen um das Widget zu zeichnen
    def paintEvent(self, event):
        # QPainter Objekt erstellen, um auf dem Widget zu zeichnen
        painter = QPainter(self)
        # Stiftoptionen für Raster
        pen_grid = QPen()
        pen_grid.setColor(Qt.lightGray)
        pen_grid.setWidth(1)
        # Stiftoptionen für Rahmen
        pen_frame = QPen()
        pen_frame.setColor(Qt.lightGray)
        pen_frame.setWidth(40)
        # # Rahmen zeichnen
        painter.setPen(pen_frame)
        painter.drawRect(0, 0, self.cols * self.pixel_size + 40, self.rows * self.pixel_size + 40)
        # # Raster zeichnen
        painter.setPen(pen_grid)
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.pixel_size + 20
                y = row * self.pixel_size + 20
                painter.drawRect(x, y, self.pixel_size, self.pixel_size)