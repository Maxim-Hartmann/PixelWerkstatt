"""
Enthält Funktionen zur Codierung und Darstellung von Bild-Daten.
"""

from collections import Counter
from PySide6.QtGui import QColor
import math
from config import select_color

# ----------------------------------------
# Codierungen
# ----------------------------------------


def encode_rle(
    pixel_data: list[list[int]], rle_lines_on: bool
) -> tuple[list[tuple[int, int]], dict[tuple[int, int], int]]:
    """
    Setzt die RLE-Codierung (Lauflängen) auf das Bild an.

    Args:
        pixel_data: 2D-Array mit Farbindizes.
        rle_lines_on: True -> Zeilenübergriff, False -> kein Zeilenübergriff.

    Returns:
        - Liste mit Tupeln (Lauflänge, Farbindex).
        - Dictionary (Reihe, Spalte -> Lauflängen-Nummer)
    """
    pos_to_number = {}
    rle_data = []
    rle_number = 0
    if rle_lines_on:
        pixel_data_list = array_to_list(pixel_data)
        # Zählt die Länge der Lauflänge.
        count_len = 1
        # Farbe des aktuellen Pixels.
        current_pixel = pixel_data_list[0]
        cols = len(pixel_data[0])
        pos_to_number[(0, 0)] = rle_number
        for i in range(1, len(pixel_data_list)):
            row_pos = i // cols
            col_pos = i % cols
            # Farbe des folgenden Pixels.
            next_pixel = pixel_data_list[i]
            if next_pixel == current_pixel:
                count_len += 1
            else:
                rle_data.append((count_len, current_pixel))
                count_len = 1
                rle_number += 1
                current_pixel = next_pixel
            pos_to_number[(row_pos, col_pos)] = rle_number
        rle_data.append((count_len, current_pixel))
    else:
        for row_pos, row in enumerate(pixel_data):
            count_len = 1
            current_pixel = row[0]
            pos_to_number[(row_pos, 0)] = rle_number
            for col_pos in range(1, len(row)):
                next_pixel = row[col_pos]
                if next_pixel == current_pixel:
                    count_len += 1
                else:
                    rle_data.append((count_len, current_pixel))
                    count_len = 1
                    rle_number += 1
                    current_pixel = next_pixel
                pos_to_number[(row_pos, col_pos)] = rle_number
            rle_data.append((count_len, current_pixel))
            rle_number += 1
    return rle_data, pos_to_number


def encode_clr(pixel_data: list[list[int]]) -> tuple[list[int], dict[int, str], int]:
    """
    Setzt die CLR-Codierung (indizierte-Farben) auf das Bild an.

    Args:
        pixel_data: 2D-Array mit Farbindizes.

    Returns:
        Informationen zur CLR-Codierung.

        - pixel_data-Kopie mit Farbcodes
        - Dictionary mit (Farbindex, Farbcode)
        - Anzahl benötigter Bits pro Pixel
    """
    pixel_data_list = array_to_list(pixel_data)
    pixel_data_count = Counter(pixel_data_list)
    # Farbindizes und ihre Häufigkeit.
    clr_frequencies = pixel_data_count.most_common()
    # Mapt Farbindizes zu Farbcodes.
    clr_codes = {}
    clr_count = len(clr_frequencies)
    # Anzahl der benötigten Bits für Farbcodes (Mindestens 1, auch bei einer Farbe).
    bits = max(1, math.ceil(math.log2(clr_count)))
    for i, (color, _) in enumerate(clr_frequencies):
        bit_code = f"{i:0{bits}b}"
        clr_codes[color] = bit_code

    clr_data = []
    for row in pixel_data:
        new_row = []
        for color in row:
            new_row.append(clr_codes[color])
        clr_data.append(new_row)
    return clr_data, clr_codes, bits


def array_to_list(array) -> list[int]:
    """
    Nimmt ein 2D-Array und strukturiert es in eine Liste

    Args:
        array: 2D-Array

    Returns:
        Liste
    """
    list = []
    for row in array:
        for i in row:
            list.append(i)
    return list


# ----------------------------------------
# to String
# ----------------------------------------


def rgb_to_string(
    rgb_data: list[list[int]],
    color_index: dict[int, tuple[QColor, str]],
    pixel_row_col: tuple[int, int] | None,
) -> str:
    """
    Konvertiert pixel_data in einen String.

    Args:
        rgb_data: 2D-Array mit Farbindizes (pixel_data).
        color_index: Mapt Farbindex zu Farbe (Qcolor, Farbname).
        pixel_row_col: Reihe und Spalte des ausgewählten Pixels.

    Returns:
        RGB-Werte (Binär, Dezi) sowie Farbnamen.
    """
    rgb_text = ""
    for row_pos, row in enumerate(rgb_data):
        for col_pos, index in enumerate(row):
            rgb_color = color_index[index][0]
            str_color = color_index[index][1]
            r = rgb_color.red()
            g = rgb_color.green()
            b = rgb_color.blue()
            if pixel_row_col == (row_pos, col_pos):
                rgb_text += (
                    f"<br><span style='background-color: {select_color[1]};'>"
                    f"{r:08b} {g:08b} {b:08b}"
                    f"<span style='color:gray'> #{r:3} {g:3} {b:3}; {str_color}</span>"
                    "</span>"
                )
            else:
                rgb_text += (
                    f"<br>{r:08b} {g:08b} {b:08b}"
                    f"<span style='color:gray'> #{r:3} {g:3} {b:3}; {str_color}</span>"
                )
    return rgb_text


def rle_to_string(
    rle_data: list[tuple[int, int]],
    color_index: dict[int, tuple[QColor, str]],
    pixel_row_col: tuple[int, int] | None,
    pos_to_number: dict[tuple[int, int], int],
) -> str:
    """
    Konvertiert rle_data in einen String.

    Args:
        rle_data: Liste mit Tupeln (Lauflänge, Farbindex).
        color_index: Mapt Farbindex zu Farbe (Qcolor, Farbname).
        pixel_row_col: Reihe und Spalte des ausgewählten Pixels.
        pos_to_number: Dictionary (Reihe, Spalte -> Lauflängen-Nummer).

    Returns:
        Anzahl der Farbwiderholung, RGB-Werte (Binär, Dezi) sowie Farbnamen.
    """
    rle_text = ""
    selected_rle = None
    if pixel_row_col is not None:
        selected_rle = pos_to_number[pixel_row_col]
    for rle_number, (rle_len, index) in enumerate(rle_data):
        rgb_color = color_index[index][0]
        str_color = color_index[index][1]
        r = rgb_color.red()
        g = rgb_color.green()
        b = rgb_color.blue()
        if selected_rle == rle_number:
            rle_text += (
                f"<br><span style='background-color: {select_color[1]};'>"
                f"{rle_len:08b} <span style='color:gray'>#{rle_len:<3}</span>"
                f"{r:08b} {g:08b} {b:08b}"
                f"<span style='color:gray'> #{r:3} {g:3} {b:3}; {str_color}</span>"
                "</span>"
            )
        else:
            rle_text += (
                f"<br>{rle_len:08b} <span style='color:gray'>#{rle_len:<3}</span>"
                f"{r:08b} {g:08b} {b:08b}"
                f"<span style='color:gray'> #{r:3} {g:3} {b:3}; {str_color}</span>"
            )
    return rle_text


def clr_to_string(
    clr_data: list[list[str]],
    color_codes: dict[int, str],
    color_index: dict[int, tuple[QColor, str]],
    pixel_row_col: tuple[int, int] | None,
) -> str:
    """
    Konvertiert clr_data in einen String.

    Args:
        clr_data: 2D-Array mit Farbcodes.
        color_codes: Mapt Farbindex zu Farbcode.
        color_index: Mapt Farbindex zu Farbe (Qcolor, Farbname).
        pixel_row_col: Reihe und Spalte des ausgewählten Pixels.

    Returns:
        - Tabelle mit Farbcode und RGB-Werten (Binär, Dezi) sowie Farbnamen.
        - Farbcodes, RGB-Werte (Dezi) sowie Farbnamen.
    """
    rgb_codes = {}
    clr_text = (
        "<span style='color:gray'>#Code | #Farbe"
        "<br>----------------------------------<br></span>"
    )
    for index, code in color_codes.items():
        rgb_color = color_index[index][0]
        str_color = color_index[index][1]
        rgb_codes[code] = (rgb_color, str_color)
        r = rgb_color.red()
        g = rgb_color.green()
        b = rgb_color.blue()
        clr_text += (
            f"{code:>5} <span style='color:gray'>|</span>"
            f" {r:08b} {g:08b} {b:08b} <span style='color:gray'>"
            f"#{r:3} {g:3} {b:3}; {str_color}</span><br>"
        )
    for row_pos, row in enumerate(clr_data):
        for col_pos, code in enumerate(row):
            rgb_color = rgb_codes[code][0]
            str_color = rgb_codes[code][1]
            r = rgb_color.red()
            g = rgb_color.green()
            b = rgb_color.blue()
            if pixel_row_col == (row_pos, col_pos):
                clr_text += (
                    f"<br><span style='background-color: {select_color[1]};'>"
                    f"{code} <span style='color:gray'>#{r:3} {g:3} {b:3}; "
                    f"{str_color}</span>"
                    "</span>"
                )
            else:
                clr_text += (
                    f"<br>{code} <span style='color:gray'>#{r:3} {g:3} {b:3}; "
                    f"{str_color}</span>"
                )
    return clr_text
