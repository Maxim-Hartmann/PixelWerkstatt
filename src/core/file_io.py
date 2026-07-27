"""
Enthält Funktionen um PixelWerkstatt-Datein zu speichern und laden.
"""

import re
from config import binary_index


def read_file(path: str):
    """
    Liest die ausgewählte Datei aus und giebt sie zum auswerten weiter.

    Args:
        path: Pfad der ausgewählten Datei.

    Returns:
        Format und Array-Darstellung der geladenen Datei.
    """
    with open(path, "r", encoding="utf-8") as file:
        file_text: str = file.read()
    # Entfernt Kommentare, Tabellengerüst (CLR) und Whitespaces
    file_text = re.sub(r"\(.*?\)|[-|]|\s+", "", file_text)
    print(file_text)
    if path.endswith(".rgb"):
        preset, pixel_data = read_rgb(file_text)
    elif path.endswith(".rle"):
        read_rle(file_text)
    else:
        read_clr(file_text)
    return preset, pixel_data


def read_rgb(file_text: str):
    """
    Wertet eine RGB-Datei aus.

    Args:
        file_text: Text-Datei als String.

    Returns:
        Format und Array-Darstellung der geladenen Datei.
    """
    # print(file_text)
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


def read_rle(file_text: str):
    return


def read_clr(file_text: str):
    return
