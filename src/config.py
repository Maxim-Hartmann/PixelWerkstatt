from PySide6.QtGui import QColor

#----------------------------------------
# color_picker config
#----------------------------------------

# Mit Liste aus Farben initialisieren
colors = [

    QColor(255, 255, 255),  # weiß
    QColor(0, 0, 0),        # schwarz
    QColor(140, 140, 140),  # grau
    QColor(190, 20, 30),    # rot
    QColor(130, 50, 10),    # braun
    QColor(220, 110, 50),   # orange
    QColor(210, 160, 130),  # hellbraun
    QColor(230, 220, 0),    # gelb
    QColor(0, 160, 0),      # grün
    QColor(0, 100, 50),     # dunkelgrün
    QColor(0, 180, 210),    # hellblau
    QColor(0, 60, 150),     # blau
    QColor(80, 40, 110),    # lila
    QColor(200, 0, 200),    # pink
    QColor(200, 90, 140),   # magenta
    QColor(150, 140, 190),  # lavendel
    
]

# Anzahl der Farben
colors_cnt = len(colors)

# Pixelgröße der Farbkacheln
pixel_size_picker = 40
# Pixelabstand der Farbkacheln
pixel_gap_picker = 6

# befüllt color_codes mit colors
def fill_codes():
    codes = {}
    i = 0
    for color in range(colors_cnt):
        codes[i] = colors[color]
        i += 1
    return codes

color_codes = fill_codes()

#----------------------------------------
# pixel_editor config
#----------------------------------------

# Größen des Pixelrasters: Reihen, Spalten, Pixelgröße, Pixelabstand
grid_size = {"s": {"rows": 6, "cols": 8, "pixel_size": 90, "pixel_gap": 2},
             "l": {"rows": 9, "cols": 12, "pixel_size": 60, "pixel_gap": 2}}

standard_color = 0 # erste Farbe (weiß)