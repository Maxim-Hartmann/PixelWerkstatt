"""
Enthält Funktionen zum Speichern und Laden von PixelWerkstatt-Dateien.
"""

import re

from config import BINARY_INDEX


def read_file(path: str) -> tuple[str, list[list[int]]]:
    """
    Liest und wertet eine ausgewählte RGB-Datei (``*.rgb``) aus.

    Args:
        path: Pfad der zu ladenden Datei.

    Returns:
        Ein Tupel aus:

        - Preset-Bezeichnung ("s" für 6x8 oder "l" für 9x12).
        - 2D-Liste mit den rekonstruierten Farbindizes (``pixel_data``).
    """
    with open(path, "r", encoding="utf-8") as file:
        text: str = file.read()

    file_text = clean_all(text)

    # Höhe (Bits 0–7) und Breite (Bits 8–15) auslesen
    height = int(file_text[:8], 2)
    width = int(file_text[8:16], 2)

    preset = "l" if (height == 9 and width == 12) else "s"

    pixel_data: list[list[int]] = []
    row_list: list[int] = []
    count_col = 0

    # Ab Bit 16 folgen die RGB-Farbdaten (jeweils 24 Bit pro Pixel)
    for i in range(16, len(file_text), 24):
        rgb_str = file_text[i : i + 24]
        index = BINARY_INDEX[rgb_str]
        row_list.append(index)
        count_col += 1

        if count_col == width:
            pixel_data.append(row_list)
            row_list = []
            count_col = 0

    return preset, pixel_data


def clean_html(text: str) -> str:
    """
    Entfernt HTML-Tags aus dem übergebenen Text.

    Args:
        text: Eingabetext mit HTML-Syntax.

    Returns:
        Bereinigter Klartext.
    """
    return re.sub(r"\<.*?\>", "", text)


def clean_all(text: str) -> str:
    """
    Entfernt Kommentare, HTML-Syntax, Tabellenzeilen (CLR) und Whitespaces.

    Args:
        text: Eingabetext.

    Returns:
        Bereinigter Binär-String.
    """
    return re.sub(r"\(.*?\)|\<.*?\>|[-|]|\s+", "", text)
