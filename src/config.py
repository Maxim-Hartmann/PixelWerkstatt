from PySide6.QtGui import QColor

# weiß (0),    rot (3),  gelb (6),    braun (9)
# grau (1),    blau (4), cyan (7),    hellblau (19)
# schwarz (2), grün (5), magenta (8), lila (11)
colors = {
    0: QColor(255, 255, 255), 1: QColor(255, 0, 0), 2: QColor(255, 255, 0), 3: QColor(100, 70, 30),
    4: QColor(120, 120, 120), 5: QColor(0, 255, 0), 6: QColor(0, 255, 255), 7: QColor(130, 200, 230),
    8: QColor(0, 0, 0),       9: QColor(0, 0, 255), 10: QColor(255, 0, 255), 11: QColor(90, 40, 120)
}

# Reihen und Spalten der Farbpalette
colors_rows = 3
colors_cols = 4

# Größen des Pixelrasters
grid_size = {"s": {"rows": 6, "cols": 8, "pixel_size": 90}, "l": {"rows": 9, "cols": 12, "pixel_size": 60}}