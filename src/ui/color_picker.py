from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Signal
from config import colors, colors_cnt, pixel_size_picker, pixel_gap_picker, standard_color

class ColorPicker(QWidget):
    
    # Farbwechsel-Signal
    new_color = Signal(int)

    def __init__(self):
        super().__init__()

        # Widgetgröße passend zum Raster setzen
        self.setFixedSize(colors_cnt * (pixel_size_picker + pixel_gap_picker) - pixel_gap_picker, pixel_size_picker)

    def paintEvent(self, event):
        painter = QPainter(self)
        for color in range(colors_cnt):
            new_color = colors[color]
            painter.fillRect(color * (pixel_size_picker + pixel_gap_picker), 0, pixel_size_picker, pixel_size_picker, new_color)

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        color_pos = pos.x() // (pixel_size_picker + pixel_gap_picker)
        self.new_color.emit(color_pos)