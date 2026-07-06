from PySide6.QtGui import QColor

#----------------------------------------
# color_picker configuration
#----------------------------------------

# Größe des Farbwählers
picker_grid_size = {"pixel_size": 40,"pixel_gap": 6}

# Im System verfügbare Farben als QColor (RGB) und String (Farbname).
# Diese werden im Anschluss im dictionary color_index gespeichert.
colors = [

    (QColor(255, 255, 255), "weiß"),        # (0)
    (QColor(0, 0, 0), "schwarz"),           # (1)
    (QColor(140, 140, 140), "grau"),        # (2)
    (QColor(190, 20, 30), "rot"),           # (3)
    (QColor(130, 50, 10), "braun"),         # (4)
    (QColor(220, 110, 50), "orange"),       # (5)
    (QColor(210, 160, 130), "hellbraun"),   # (6)
    (QColor(230, 220, 0), "gelb"),          # (7)
    (QColor(0, 160, 0), "grün"),            # (8)
    (QColor(0, 100, 50), "dunkelgrün"),     # (9)
    (QColor(160, 210, 240), "hellblau"),    # (10)
    (QColor(0, 60, 150), "blau"),           # (11)
    (QColor(80, 40, 110), "lila"),          # (12)
    (QColor(200, 0, 200), "pink"),          # (13)
    (QColor(200, 90, 140), "magenta"),      # (14)
    (QColor(150, 140, 190), "lavendel")     # (15)

]

# Mapping: Farbindex → (QColor, Farbname)
color_index = dict(enumerate(colors))

#----------------------------------------
# pixel_editor configuration
#----------------------------------------

# Größen des Pixelrasters: Reihen, Spalten, Pixelgröße, Pixelabstand
editor_grid_size = {"s": {"rows": 6, "cols": 8, "pixel_size": 90, "pixel_gap": 2},
             "l": {"rows": 9, "cols": 12, "pixel_size": 60, "pixel_gap": 2}}

# Standardfarbe, wenn noch keine Farbe gewählt wurde
standard_color = 0

#----------------------------------------
# HTML configuration
#----------------------------------------

text_style = """
\"
font-family: Cascadia Code, Consolas, monospace;
white-space: pre;
font-size: 12pt;
\"
"""