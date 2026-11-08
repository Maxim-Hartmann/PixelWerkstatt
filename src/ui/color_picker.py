"""
Erstellt das Color-Picker-Widget zur Auswahl von Farben.
"""

from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent, QPaintEvent, QPainter
from PySide6.QtWidgets import QWidget

from config import COLORS, PICKER_GRID_SIZE


class ColorPicker(QWidget):
    """
    Widget zur Auswahl von Farben.

    Zeigt ein vorgefertigtes Raster an Farben, welche angeklickt werden können.
    Die ausgewählte Farbe wird als Signal emittiert.
    """

    #: Sendet den Farbindex (Integer) der neu ausgewählten Farbe.
    send_new_color = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        #: Kachelgröße der einzelnen Farbfelder in Pixeln.
        self.pixel_size = PICKER_GRID_SIZE["pixel_size"]

        #: Abstand zwischen den einzelnen Farbfeldern in Pixeln.
        self.pixel_gap = PICKER_GRID_SIZE["pixel_gap"]

        self.setFixedSize(
            len(COLORS) * (self.pixel_size + self.pixel_gap) - self.pixel_gap,
            self.pixel_size,
        )

    def paintEvent(self, paint_event: QPaintEvent) -> None:
        """
        Zeichnet die Farbauswahl.

        Farben werden als eine Reihe von farbigen Kacheln dargestellt.

        Args:
            paint_event: Informationen über das aktuelle Zeichenereignis.
        """
        with QPainter(self) as painter:
            for i, (color, _) in enumerate(COLORS):
                painter.fillRect(
                    i * (self.pixel_size + self.pixel_gap),
                    0,
                    self.pixel_size,
                    self.pixel_size,
                    color,
                )

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Ermittelt die angeklickte Farbe und sendet deren Index per Signal.

        Args:
            event: Informationen über das aktuelle Mausereignis.
        """
        pos = event.position().toPoint()
        color_pos = pos.x() // (self.pixel_size + self.pixel_gap)

        # Sicherstellen, dass nur gültige Farbindizes emittiert werden.
        if 0 <= color_pos < len(COLORS):
            self.send_new_color.emit(color_pos)
