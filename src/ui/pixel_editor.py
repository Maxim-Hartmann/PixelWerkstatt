import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt

class PixelEditor(QWidget):
    # Editor wird initialisiert mit der Rastergröße (x, y) und der Pixelgröße
    def __init__(self, grid_size, pixel_size):
        super().__init__()
        # Reihen
        self.rows = grid_size[0]
        # Spalten
        self.cols = grid_size[1]
        # Pixelgröße
        self.pixel_size = pixel_size
        # Bearbeitbares Originalbild.
        # 3D-Array wird erstellt und mit Nullen gefüllt.
        # Reihen, Spalten und RGB-Farb-Tripel werden gespeichert, als 8-Bit-Integer (0-255).
        self.original = np.zeros((self.rows, self.cols, 3), dtype = np.uint8)
        # Größe wird erstellt
        self.setFixedSize(self.cols * self.pixel_size, self.rows * self.pixel_size)
