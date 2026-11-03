"""
Erstellt das Pixel-Editor-Widget zur Bearbeitung von Bildern.
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPaintEvent, QMouseEvent, QPen
from PySide6.QtCore import Signal
from config import editor_grid_size, standard_color, color_index, select_color


class PixelEditor(QWidget):
    """
    Widget zum erstellen eines Bildes.

    Zeigt ein vorgefärtigtes Raster mit Kacheln die angeklickt werden können.
    Beim klicken ändert sich die Farbe des Rasters.
    """

    # Sendet einen ausgewählten Pixel an MainWindow.
    send_selected_pixel = Signal()
    # Sendet einen bemalten Pixel an MainWindow.
    send_painted_pixel = Signal()

    def __init__(self, preset="s"):
        super().__init__()

        # Voreinstellungen für das Raster setzen
        self.set_preset(preset)
        # aktueller Farbindex
        self.current_color = standard_color
        # Farbindex → (QColor, Farbname)
        self.color_index = color_index
        # Mal- (paint) oder Auswähl-Modus (select)
        self.mode = "paint"
        # aktuell ausgewählter Pixel
        self.pixel_row_col = None
        # zugehörige Lauflänge vom aktuell ausgewählten Pixel.
        self.selected_pixels = []
        # Stift für das Markieren des hervorgehobenen Pixels
        self.select_pen = QPen()
        self.select_pen_width = 2 * self.gap
        self.select_pen.setWidth(self.select_pen_width)
        self.select_pen.setColor(select_color[0])

    def paintEvent(self, paint_event: QPaintEvent) -> None:
        """
        Zeichnet/Updatet den Pixel-Editor.
        Das Raster wird durch die Informationen in pixel_data gezeichnet.

        Args:
            paint_event: Informationen über aktuelles Zeichenereignis.
        """
        painter = QPainter(self)
        for row in range(self.rows):
            for col in range(self.cols):
                index = self.pixel_data[row][col]
                color = self.color_index[index][0]
                painter.fillRect(
                    col * (self.pixel_size + self.gap) + self.gap,
                    row * (self.pixel_size + self.gap) + self.gap,
                    self.pixel_size,
                    self.pixel_size,
                    color,
                )
        if self.mode == "select" and self.pixel_row_col is not None:
            painter.setPen(self.select_pen)
            if self.selected_pixels:
                for row, col in self.selected_pixels:
                    painter.drawRect(
                        col * (self.pixel_size + self.gap) + self.gap,
                        row * (self.pixel_size + self.gap) + self.gap,
                        self.pixel_size,
                        self.pixel_size,
                    )
                self.selected_pixels = []
            else:
                painter.drawRect(
                    self.pixel_row_col[1] * (self.pixel_size + self.gap) + self.gap,
                    self.pixel_row_col[0] * (self.pixel_size + self.gap) + self.gap,
                    self.pixel_size,
                    self.pixel_size,
                )

    def set_preset(self, preset: str, pixel_data: list[int] = []) -> None:
        """
        Setzt/Updatet die Voreinstellungen für das Raster.

        Args:
            preset: Key für die Auswahl der richtigen Voreinstellungen.
            pixel_data: Array, dass das Bild durch Farbindizes abbildet.
        """
        self.mode = "paint"
        self.preset = preset
        self.rows = editor_grid_size[preset]["rows"]
        self.cols = editor_grid_size[preset]["cols"]
        self.gap = editor_grid_size[preset]["pixel_gap"]
        self.pixel_size = editor_grid_size[preset]["pixel_size"]
        # Meta-Daten werden als jeweils ein Byte gespeichert -> (Höhe und Breite)
        # (Höhe + Breite) + (Reihen * Spalten * 8 Bit * 3 RGB)
        self.image_bits = (2 * 8) + (self.rows * self.cols * 8 * 3)
        if pixel_data:
            self.pixel_data = pixel_data
        else:
            self.pixel_data = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.setFixedSize(
            self.cols * (self.pixel_size + self.gap) + self.gap,
            self.rows * (self.pixel_size + self.gap) + self.gap,
        )
        self.update()

    def mousePressEvent(self, mouse_event: QMouseEvent) -> None:
        """
        Ermittelt das angeklickte Feld und sendet dieses an MainWindow.

        Args:
            mouse_event: Enthält Informationen über den Mausklick.
        """
        pos = mouse_event.position().toPoint()
        row = pos.y() // (self.pixel_size + self.gap)
        col = pos.x() // (self.pixel_size + self.gap)
        if self.mode == "paint":
            self.pixel_data[row][col] = self.current_color
            self.send_painted_pixel.emit()
        else:
            self.pixel_row_col = (row, col)
            self.send_selected_pixel.emit()
        self.update()

    def set_selected_pixels(self, selected_pixels: list[tuple[int, int]]) -> None:
        """
        Setzt die ausgewählten Pixel.

        Args:
            selected_pixels: Liste mit allen ausgewählten Pixeln (Reihe, Spalte).
        """
        self.selected_pixels = selected_pixels
        self.update()
