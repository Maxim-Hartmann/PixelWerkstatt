"""
Erstellt das Color-Picker-Widget zur Auswahl von Farben.
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPaintEvent
from PySide6.QtCore import Signal
from config import colors, picker_grid_size


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

        self.pixel_size = picker_grid_size["pixel_size"]
        self.pixel_gap = picker_grid_size["pixel_gap"]

        self.setFixedSize(
            len(colors) * (self.pixel_size + self.pixel_gap) - self.pixel_gap,
            self.pixel_size,
        )

    def paintEvent(self, paint_event: QPaintEvent) -> None:
        """
        Zeichnet die Farb-Auswahl.
        Farben werden als eine Reihe von farbigen Kacheln dargestellt.

        Args:
            paint_event: Informationen über aktuelles Zeichenereignis.
        """
        painter = QPainter(self)
        for i, (color, _) in enumerate(colors):
            painter.fillRect(
                i * (self.pixel_size + self.pixel_gap),
                0,
                self.pixel_size,
                self.pixel_size,
                color,
            )

    def mousePressEvent(self, paint_event: QPaintEvent) -> None:
        """
        Ermittelt die angeklickte Farbe und gibt diese an main_window weiter.

        Args:
            paint_event: Informationen über aktuelles Zeichenereignis.
        """
        pos = paint_event.position().toPoint()
        color_pos = pos.x() // (self.pixel_size + self.pixel_gap)
        self.new_color.emit(color_pos)
