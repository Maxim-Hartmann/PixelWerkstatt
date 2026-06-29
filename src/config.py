from PySide6.QtGui import QColor

#----------------------------------------
# color_picker configuration
#----------------------------------------

# Im System verfügbare Farben.
# "colors" kann mit einer Liste von Farben initialisiert werden.
# Diese werden im Anschluss im dictionary "color_index" gespeichert.
colors = [

    QColor(255, 255, 255),  # weiß (0)
    QColor(0, 0, 0),        # schwarz (1)
    QColor(140, 140, 140),  # grau (2)
    QColor(190, 20, 30),    # rot (3)
    QColor(130, 50, 10),    # braun (4)
    QColor(220, 110, 50),   # orange (5)
    QColor(210, 160, 130),  # hellbraun (6)
    QColor(230, 220, 0),    # gelb (7)
    QColor(0, 160, 0),      # grün (8)
    QColor(0, 100, 50),     # dunkelgrün (9)
    QColor(0, 180, 210),    # hellblau (10)
    QColor(0, 60, 150),     # blau (11)
    QColor(80, 40, 110),    # lila (12)
    QColor(200, 0, 200),    # pink (13)
    QColor(200, 90, 140),   # magenta (14)
    QColor(150, 140, 190),  # lavendel (15)
    
]

# Pixelgröße der Farbkacheln
pixel_size_picker = 40
# Pixelabstand der Farbkacheln
pixel_gap_picker = 6

# Mapping: Farbindex → QColor
# Wird verwendet, um aus "pixel_data" (2D-Array, dtype = int) echte Farben zu machen.
color_index = dict(enumerate(colors))

#----------------------------------------
# pixel_editor configuration
#----------------------------------------

# Größen des Pixelrasters: Reihen, Spalten, Pixelgröße, Pixelabstand
grid_size = {"s": {"rows": 6, "cols": 8, "pixel_size": 90, "pixel_gap": 2},
             "l": {"rows": 9, "cols": 12, "pixel_size": 60, "pixel_gap": 2}}

# Standardfarbe, wenn noch keine Farbe gewählt wurde
standard_color = 0