from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter
from config import colors, colors_rows, colors_cols, pixel_size_picker, pixel_gap_picker

class ColorPicker(QWidget):
    def __init__(self):
        super().__init__()

        # Widgetgröße passend zum Raster setzen
        self.setFixedSize(colors_cols * (pixel_size_picker + pixel_gap_picker), colors_rows * (pixel_size_picker + pixel_gap_picker))

    def paintEvent(self, event):
        painter = QPainter(self)
        # Zähler für colors
        i = 0
        for row in range(colors_rows):
            for col in range(colors_cols):
                color = colors[i]
                painter.fillRect(col * (pixel_size_picker + pixel_gap_picker), row * (pixel_size_picker + pixel_gap_picker), pixel_size_picker, pixel_size_picker, color)
                i += 1

    def mousePressEvent(self, event):
        print("\"klick\"")
        pos = event.position().toPoint()
        print("x: " + str(pos.x()) + ", y: " + str(pos.y()))
        col = pos.x() // 50
        row = pos.y() // 50
        