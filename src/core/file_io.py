"""
Enthält Funktionen um PixelWerkstatt-Datein zu speichern und laden.
"""

import re
from config import binary_index


def read_file(path: str) -> tuple[str, list[list[int]]]:
    """
    Liest und wertet die ausgewählte RGB-Datei aus.

    Args:
        path: Pfad der ausgewählten Datei.

    Returns:
        Format und Array-Darstellung der geladenen Datei.
    """
    with open(path, "r", encoding="utf-8") as file:
        text: str = file.read()
    file_text = clean_all(text)
    pixel_data = []
    row_list = []
    count_col = 0
    height = int(file_text[:8], 2)
    width = int(file_text[9:16], 2)
    if height == 6 and width == 8:
        preset = "s"
    elif height == 9 and width == 12:
        preset = "l"
    for i in range(16, len(file_text), 24):
        rgb_str = file_text[i : i + 24]
        index = binary_index[rgb_str]
        row_list.append(index)
        count_col += 1
        if count_col == width:
            pixel_data.append(row_list)
            row_list = []
            count_col = 0
    return preset, pixel_data


def clean_html(text) -> str:
    """
    Entfernt HTML-Syntax.

    Args:
        text: Eingabetext.

    Returns:
        Bereinigter Text.
    """
    return re.sub(r"\<.*?\>", "", text)


def clean_all(text) -> str:
    """
    Entfernt Kommentare, HTML-Syntax, Tabellen (CLR) und Whitespaces.

    Args:
        text: Eingabetext.

    Returns:
        Bereinigter Text.
    """
    return re.sub(r"\(.*?\)|\<.*?\>|[-|]|\s+", "", text)
