"""
Konfigurationsdatei.

Enthält zentrale Konfigurationen für:
- Farbauswahl
- Pixelraster
- HTML-Darstellung
"""

from PySide6.QtGui import QColor

# --------------------------------------------------------------------------------------
# Color-Picker-Konfiguration
# --------------------------------------------------------------------------------------

# Größe des Farbwählers.
PICKER_GRID_SIZE = {"pixel_size": 40, "pixel_gap": 6}

# Im System verfügbare Farben als QColor (RGB) und String (Farbname).
COLORS = [
    (QColor(255, 255, 255), "weiß"),  # (0)
    (QColor(0, 0, 0), "schwarz"),  # (1)
    (QColor(140, 140, 140), "grau"),  # (2)
    (QColor(190, 20, 30), "rot"),  # (3)
    (QColor(130, 50, 10), "braun"),  # (4)
    (QColor(220, 110, 50), "orange"),  # (5)
    (QColor(210, 160, 130), "hellbraun"),  # (6)
    (QColor(230, 220, 0), "gelb"),  # (7)
    (QColor(0, 160, 0), "grün"),  # (8)
    (QColor(0, 100, 50), "dunkelgrün"),  # (9)
    (QColor(160, 210, 240), "hellblau"),  # (10)
    (QColor(0, 60, 150), "blau"),  # (11)
    (QColor(80, 40, 110), "lila"),  # (12)
    (QColor(200, 0, 200), "pink"),  # (13)
    (QColor(200, 90, 140), "magenta"),  # (14)
    (QColor(150, 140, 190), "lavendel"),  # (15)
]

# Mapping: Farbindex → (QColor, Farbname)
COLOR_INDEX = dict(enumerate(COLORS))

# Mapping: RGB-Binär-String → Farbindex
BINARY_INDEX = {
    "111111111111111111111111": 0,
    "000000000000000000000000": 1,
    "100011001000110010001100": 2,
    "101111100001010000011110": 3,
    "100000100011001000001010": 4,
    "110111000110111000110010": 5,
    "110100101010000010000010": 6,
    "111001101101110000000000": 7,
    "000000001010000000000000": 8,
    "000000000110010000110010": 9,
    "101000001101001011110000": 10,
    "000000000011110010010110": 11,
    "010100000010100001101110": 12,
    "110010000000000011001000": 13,
    "110010000101101010001100": 14,
    "100101101000110010111110": 15,
}

# --------------------------------------------------------------------------------------
# Pixel-Editor-Konfiguration
# --------------------------------------------------------------------------------------

# Größen des Pixelrasters: Zeilen, Spalten, Pixelgröße, Pixelabstand.
EDITOR_GRID_SIZE = {
    "s": {"rows": 6, "cols": 8, "pixel_size": 90, "pixel_gap": 2},
    "l": {"rows": 9, "cols": 12, "pixel_size": 60, "pixel_gap": 2},
}

# Standardfarbe, bevor eine Farbe gewählt wurde.
STANDARD_COLOR = 1

# Farbe für die Auswahl/Markierung: (QColor, HTML-RGB-String)
SELECT_COLOR = (QColor(180, 180, 50), "rgb(180, 180, 50)")

# --------------------------------------------------------------------------------------
# HTML-Konfiguration
# --------------------------------------------------------------------------------------

# Standard-Textformatierung: Schriftart, Leerzeichen-Verhalten, Schriftgröße.
TEXT_STYLE = """
font-family: 'Cascadia Code', Consolas, monospace;
white-space: pre;
font-size: 11pt;
"""
