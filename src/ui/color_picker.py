from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter
from PySide6.QtCore import Signal
from config import colors, pixel_size_picker, pixel_gap_picker

class ColorPicker(QWidget):
    """
    Widget zur Auswahl von Farben.

    Zeigt ein vorgefärtigtes Raster an Farben, welche angeklickt werden können.
    Die ausgewählte Farbe wird an das System weitergegeben.
    """
    
    # Farbwechsel-Signal
    new_color = Signal(int)

    def __init__(self):
        super().__init__()

        self.setFixedSize(len(colors) * (pixel_size_picker + pixel_gap_picker) - pixel_gap_picker, pixel_size_picker)

    def paintEvent(self, event):
        """
        Zeichnet die Farb-Auswahl.
        Farben werden als eine Reihe von farbigen Kacheln dargestellt.
        """
        painter = QPainter(self)
        for i, color in enumerate(colors):
            painter.fillRect(i * (pixel_size_picker + pixel_gap_picker), 0, pixel_size_picker, pixel_size_picker, color)

    def mousePressEvent(self, event):
        """
        Ermittelt die angeklickte Farbe und gibt diese an main_window weiter
        """
        pos = event.position().toPoint()
        color_pos = pos.x() // (pixel_size_picker + pixel_gap_picker)
        self.new_color.emit(color_pos)