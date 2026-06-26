from PySide6.QtGui import QColor

#----------------------------------------
# color_picker config
#----------------------------------------

# Mit einem x * y Block aus Farben initialisieren
colors = [
    [
        QColor(255, 255, 255),
        QColor(220, 220, 220),
        QColor(180, 180, 180),
        QColor(140, 140, 140),
        QColor(100, 100, 100),
        QColor(60, 60, 60),
        QColor(10, 10, 10),
        QColor(0, 0, 0),
    ],
    
    [
        QColor(255, 0, 0),
        QColor(255, 165, 0),
        QColor(255, 255, 0),
        QColor(0, 255, 0),
        QColor(0, 255, 255),
        QColor(0, 0, 255),
        QColor(128, 0, 255),
        QColor(255, 0, 255),
    ]
]

# Reihen und Spalten der Farbpalette
colors_cols = len(colors)
colors_rows = len(colors[0])

# Pixelgröße der Farbkacheln
pixel_size_picker = 40
# Pixelabstand der Farbkacheln
pixel_gap_picker = 10

# befüllt color_codes mit colors
def fill_codes():
    codes = {}
    i = 0
    for col in range(colors_cols):
        for row in range(colors_rows):
            codes[i] = colors[col][row]
            i += 1
    return codes

color_codes = fill_codes()

#----------------------------------------
# pixel_editor config
#----------------------------------------

# Größen des Pixelrasters: Reihen, Spalten, Pixelgröße, Pixelabstand
grid_size = {"s": {"rows": 6, "cols": 8, "pixel_size": 90, "pixel_gap": 2},
             "l": {"rows": 9, "cols": 12, "pixel_size": 60, "pixel_gap": 2}}