"""
Enthält Funktionen zur Codierung und Darstellung von Bild-Daten.
"""

from collections import Counter, defaultdict
import math

from PySide6.QtGui import QColor

from config import SELECT_COLOR

# --------------------------------------------------------------------------------------
# Codierungen
# --------------------------------------------------------------------------------------


def encode_rle(
    pixel_data: list[list[int]], rle_lines_on: bool
) -> tuple[
    list[tuple[int, int]], dict[tuple[int, int], int], dict[int, list[tuple[int, int]]]
]:
    """
    Führt die RLE-Codierung (Lauflängencodierung) auf dem Bild aus.

    Args:
        pixel_data: 2D-Liste mit Farbindizes.
        rle_lines_on: True für zeilenübergreifend, False für zeilenweise Codierung.

    Returns:
        Ein Tupel bestehend aus:

        - Liste mit Tupeln (Lauflänge, Farbindex).
        - Dictionary (Zeile, Spalte) -> Lauflängen-Nummer.
        - Dictionary Lauflängen-Nummer -> Liste von (Zeile, Spalte).
    """
    # Zum Erstellen der Markierungen im Text/String.
    pos_to_number: dict[tuple[int, int], int] = {}
    # Zum Erstellen der Markierungen im Pixel-Editor.
    number_to_pos: dict[int, list[tuple[int, int]]] = defaultdict(list)
    # Speichert (Lauflänge, Farbindex).
    rle_data: list[tuple[int, int]] = []
    # Zählt die Lauflängen durch.
    rle_count = 0

    # Falls RLE zeilenübergreifend laufen soll:
    if rle_lines_on:
        pixel_data_list = array_to_list(pixel_data)
        count_len = 1
        current_pixel = pixel_data_list[0]
        cols = len(pixel_data[0])

        pos_to_number[(0, 0)] = rle_count
        number_to_pos[rle_count].append((0, 0))

        for i in range(1, len(pixel_data_list)):
            row_pos = i // cols
            col_pos = i % cols
            next_pixel = pixel_data_list[i]

            if next_pixel == current_pixel:
                count_len += 1
            else:
                rle_data.append((count_len, current_pixel))
                count_len = 1
                rle_count += 1
                current_pixel = next_pixel

            pos_to_number[(row_pos, col_pos)] = rle_count
            number_to_pos[rle_count].append((row_pos, col_pos))

        rle_data.append((count_len, current_pixel))

    # Falls RLE nicht zeilenübergreifend laufen soll:
    else:
        for row_pos, row in enumerate(pixel_data):
            count_len = 1
            current_pixel = row[0]
            pos_to_number[(row_pos, 0)] = rle_count
            number_to_pos[rle_count].append((row_pos, 0))

            for col_pos in range(1, len(row)):
                next_pixel = row[col_pos]
                if next_pixel == current_pixel:
                    count_len += 1
                else:
                    rle_data.append((count_len, current_pixel))
                    count_len = 1
                    rle_count += 1
                    current_pixel = next_pixel

                pos_to_number[(row_pos, col_pos)] = rle_count
                number_to_pos[rle_count].append((row_pos, col_pos))

            rle_data.append((count_len, current_pixel))
            rle_count += 1

    return rle_data, pos_to_number, number_to_pos


def encode_clr(
    pixel_data: list[list[int]],
) -> tuple[list[list[str]], dict[int, str], int]:
    """
    Führt die CLR-Codierung (indizierte Farben) auf dem Bild aus.

    Args:
        pixel_data: 2D-Liste mit Farbindizes.

    Returns:
        Ein Tupel bestehend aus:

        - 2D-Liste mit Binär-Farbcodes pro Pixel (``list[list[str]]``).
        - Dictionary mit Mapping (Farbindex -> Farbcode).
        - Anzahl benötigter Bits pro Pixel.
    """
    pixel_data_list = array_to_list(pixel_data)
    pixel_data_count = Counter(pixel_data_list)
    clr_frequencies = pixel_data_count.most_common()

    clr_codes: dict[int, str] = {}
    clr_count = len(clr_frequencies)
    # Mindestens 1 Bit, selbst wenn nur eine Farbe verwendet wird.
    bits = max(1, math.ceil(math.log2(clr_count)))

    for i, (color, _) in enumerate(clr_frequencies):
        bit_code = f"{i:0{bits}b}"
        clr_codes[color] = bit_code

    clr_data: list[list[str]] = []
    for row in pixel_data:
        new_row = [clr_codes[color] for color in row]
        clr_data.append(new_row)

    return clr_data, clr_codes, bits


def array_to_list(array: list[list[int]]) -> list[int]:
    """
    Wandelt ein 2D-Array in eine eindimensionale Liste um.

    Args:
        array: 2D-Liste mit Integern.

    Returns:
        Eindimensionale Liste aller Elemente.
    """
    return [pixel for row in array for pixel in row]


# --------------------------------------------------------------------------------------
# String-Konvertierung (HTML-Ausgabe)
# --------------------------------------------------------------------------------------


def rgb_to_string(
    rows: int,
    cols: int,
    rgb_data: list[list[int]],
    color_index: dict[int, tuple[QColor, str]],
    pixel_row_col: tuple[int, int] | None,
) -> str:
    """
    Konvertiert ``rgb_data`` in einen HTML-formatierten Quelltext-String.

    Args:
        rows: Anzahl der Zeilen.
        cols: Anzahl der Spalten.
        rgb_data: 2D-Liste mit Farbindizes (``pixel_data``).
        color_index: Mapping Farbindex -> (QColor, Farbname).
        pixel_row_col: Zeile und Spalte des ausgewählten Pixels oder None.

    Returns:
        Formatiertes HTML mit Binär-/Dezimalwerten und Farbnamen.
    """
    rgb_text = (
        f"{rows:08b} <span style='color:gray'>(Höhe) </span>"
        f"{cols:08b} <span style='color:gray'>(Breite)</span><br>"
    )
    for row_pos, row in enumerate(rgb_data):
        for col_pos, index in enumerate(row):
            rgb_color = color_index[index][0]
            str_color = color_index[index][1]
            r = rgb_color.red()
            g = rgb_color.green()
            b = rgb_color.blue()

            if pixel_row_col == (row_pos, col_pos):
                rgb_text += (
                    f"<br><span style='background-color: {SELECT_COLOR[1]};'>"
                    f"{r:08b} {g:08b} {b:08b}"
                    f"<span style='color:gray'> ({r:3} {g:3} {b:3}; {str_color})</span>"
                    "</span>"
                )
            else:
                rgb_text += (
                    f"<br>{r:08b} {g:08b} {b:08b}"
                    f"<span style='color:gray'> ({r:3} {g:3} {b:3}; {str_color})</span>"
                )
    return rgb_text


def rle_to_string(
    rows: int,
    cols: int,
    rle_data: list[tuple[int, int]],
    color_index: dict[int, tuple[QColor, str]],
    pixel_row_col: tuple[int, int] | None,
    pos_to_number: dict[tuple[int, int], int],
) -> str:
    """
    Konvertiert ``rle_data`` in einen HTML-formatierten Quelltext-String.

    Args:
        rows: Anzahl der Zeilen.
        cols: Anzahl der Spalten.
        rle_data: Liste mit Tupeln (Lauflänge, Farbindex).
        color_index: Mapping Farbindex -> (QColor, Farbname).
        pixel_row_col: Zeile und Spalte des ausgewählten Pixels oder None.
        pos_to_number: Dictionary (Zeile, Spalte) -> Lauflängen-Nummer.

    Returns:
        Formatiertes HTML mit Lauflängen, Binär-/Dezimalwerten und Farbnamen.
    """
    rle_text = (
        f"{rows:08b} <span style='color:gray'>(Höhe) </span>"
        f"{cols:08b} <span style='color:gray'>(Breite)</span><br>"
    )
    selected_rle = None
    if pixel_row_col is not None:
        selected_rle = pos_to_number.get(pixel_row_col)

    for rle_count, (rle_len, index) in enumerate(rle_data):
        rgb_color = color_index[index][0]
        str_color = color_index[index][1]
        r = rgb_color.red()
        g = rgb_color.green()
        b = rgb_color.blue()
        rle_digits = len(str(rle_len))

        if selected_rle == rle_count:
            rle_text += (
                f"<br><span style='background-color: {SELECT_COLOR[1]};'>"
                f"{rle_len:08b} "
                f"<span style='color:gray'>({rle_len:<{rle_digits}}) </span>"
                f"{r:08b} {g:08b} {b:08b}"
                f"<span style='color:gray'> ({r:3} {g:3} {b:3}; {str_color})</span>"
                "</span>"
            )
        else:
            rle_text += (
                f"<br>{rle_len:08b} "
                f"<span style='color:gray'>({rle_len:<{rle_digits}}) </span>"
                f"{r:08b} {g:08b} {b:08b}"
                f"<span style='color:gray'> ({r:3} {g:3} {b:3}; {str_color})</span>"
            )
    return rle_text


def clr_to_string(
    rows: int,
    cols: int,
    clr_data: list[list[str]],
    clr_codes: dict[int, str],
    color_index: dict[int, tuple[QColor, str]],
    pixel_row_col: tuple[int, int] | None,
) -> str:
    """
    Konvertiert ``clr_data`` in einen HTML-formatierten Quelltext-String.

    Args:
        rows: Anzahl der Zeilen.
        cols: Anzahl der Spalten.
        clr_data: 2D-Liste mit Farbcodes (``list[list[str]]``).
        clr_codes: Mapping Farbindex -> Farbcode.
        color_index: Mapping Farbindex -> (QColor, Farbname).
        pixel_row_col: Zeile und Spalte des ausgewählten Pixels oder None.

    Returns:
        Formatiertes HTML mit Farbtabelle und Binär-Farbcodes pro Pixel.
    """
    rgb_codes: dict[str, tuple[QColor, str]] = {}
    clr_text = (
        f"{rows:08b} <span style='color:gray'>(Höhe) </span>"
        f"{cols:08b} <span style='color:gray'>(Breite) </span>"
        f"{len(clr_codes):08b} <span style='color:gray'>(Farb-Anzahl)</span><br><br>"
        "<span style='color:gray'>(Code) | (Farbe)"
        "<br>-----------------------------------<br></span>"
    )
    for index, code in clr_codes.items():
        rgb_color = color_index[index][0]
        str_color = color_index[index][1]
        rgb_codes[code] = (rgb_color, str_color)
        r = rgb_color.red()
        g = rgb_color.green()
        b = rgb_color.blue()
        clr_text += (
            f"{code:<7}<span style='color:gray'>| </span>"
            f"{r:08b} {g:08b} {b:08b} <span style='color:gray'>"
            f"({r:3} {g:3} {b:3}; {str_color})</span><br>"
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
                    f"<br><span style='background-color: {SELECT_COLOR[1]};'>"
                    f"{code} <span style='color:gray'>({r:3} {g:3} {b:3}; "
                    f"{str_color})</span>"
                    "</span>"
                )
            else:
                clr_text += (
                    f"<br>{code} <span style='color:gray'>({r:3} {g:3} {b:3}; "
                    f"{str_color})</span>"
                )
    return clr_text
