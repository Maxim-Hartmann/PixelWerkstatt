from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter
from config import colors, colors_rows, colors_cols

class ColorPicker(QWidget):
    def __init__(self):
        super().__init__()

        # Pixelgröße
        self.pixel_size = 40
        # Widgetgröße passend zum Raster setzen
        self.setFixedSize(colors_cols * (self.pixel_size + 10), colors_rows * (self.pixel_size + 10))

    def paintEvent(self, event):
        painter = QPainter(self)
        # Zähler für colors
        i = 0
        for row in range(colors_rows):
            for col in range(colors_cols):
                color = colors[i]
                painter.fillRect(col * (self.pixel_size + 10), row * (self.pixel_size + 10), self.pixel_size, self.pixel_size, color)
                i += 1