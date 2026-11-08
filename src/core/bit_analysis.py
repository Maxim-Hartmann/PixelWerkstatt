"""
Enthält Funktionen zur Berechnung und Darstellung von Bits und Kennzahlen.
"""

# --------------------------------------------------------------------------------------
# Bit-Berechnungen
# --------------------------------------------------------------------------------------


def rgb_to_bit(
    image_bits: int, rows: int, cols: int
) -> tuple[str, str, str, str, str, str]:
    """
    Erzeugt lesbare Informationen der RGB-Codierung für die Datenanzeige.

    Args:
        image_bits: Größe des Bildes in Bits in der RGB-Codierung.
        rows: Anzahl der Zeilen des Bildes.
        cols: Anzahl der Spalten des Bildes.

    Returns:
        Ein Tupel mit formatierten Strings für die UI-Labels:

        - Kompressionsanzeige (Fortschrittsbalken)
        - Prozentuale Datenersparnis
        - Kompressionsverhältnis
        - Dateigröße
        - Bit pro Pixel
        - Anzahl der Pixel des Bildes
    """
    byte_bar = (
        "<span style='color: white;'>"
        "██████████████████████████████████████████████████</span>"
    )
    byte_percent = "<span style='color: white;'>0%</span> Prozentuale Datenersparnis"
    byte_comp = "<span style='color: white;'>1:1 (= 1)</span> Kompressionsverhältnis"
    byte_size = (
        f"<span style='color: white;'>{image_bits} Bit "
        f"({image_bits / 8:.1f} Byte)</span> Dateigröße"
    )
    bits_pixel = "<span style='color: white;'>24 Bit (3 Byte)</span> Bit pro Pixel"
    resolution = f"<span style='color: white;'>{rows * cols}</span> Anzahl Pixel"

    return byte_bar, byte_percent, byte_comp, byte_size, bits_pixel, resolution


def rle_to_bit(
    image_bits: int,
    run_length_count: int,
    run_length_length: list[int],
    rows: int,
    cols: int,
) -> tuple[str, str, str, str, str, str]:
    """
    Erzeugt lesbare Informationen der RLE-Codierung für die Datenanzeige.

    Args:
        image_bits: Größe des Bildes in Bits in der RGB-Codierung.
        run_length_count: Anzahl der vorkommenden Lauflängen.
        run_length_length: Längen der vorkommenden Lauflängen.
        rows: Anzahl der Zeilen des Bildes.
        cols: Anzahl der Spalten des Bildes.

    Returns:
        Ein Tupel mit formatierten Strings für die UI-Labels:

        - Kompressionsanzeige (Fortschrittsbalken)
        - Prozentuale Datenersparnis
        - Kompressionsverhältnis
        - Dateigröße
        - Anzahl der Lauflängen
        - Durchschnittliche Lauflänge
    """
    # Metadaten werden als jeweils ein Byte gespeichert (Höhe und Breite):
    # (Höhe + Breite) + (Anzahl Lauflängen * 8 Bit * (3 Byte RGB + 1 Byte Lauflängenzähler))
    rle_bits = (2 * 8) + (run_length_count * 8 * 4)
    comp = rle_bits / image_bits
    percent = (1 - comp) * 100

    byte_size = bit_to_size(rle_bits)
    byte_comp = bit_to_comp(comp, image_bits, rle_bits)
    byte_percent = bit_to_percent(percent)
    byte_bar = bit_to_bar(percent)

    run_len_count_str = (
        f"<span style='color: white;'>{run_length_count}</span> " f"Anzahl Lauflängen"
    )
    avg_len = sum(run_length_length) / run_length_count if run_length_count > 0 else 0.0
    avg_run_len_float = round(avg_len, 1)
    avg_run_length = (
        f"<span style='color: white;'>{avg_run_len_float}</span> "
        f"Durchschnittliche Lauflänge"
    )

    return (
        byte_bar,
        byte_percent,
        byte_comp,
        byte_size,
        run_len_count_str,
        avg_run_length,
    )


def clr_to_bit(
    image_bits: int, color_count: int, code_length: int, rows: int, cols: int
) -> tuple[str, str, str, str, str, str]:
    """
    Erzeugt lesbare Informationen der CLR-Codierung für die Datenanzeige.

    Args:
        image_bits: Größe des Bildes in Bits in der RGB-Codierung.
        color_count: Anzahl der verwendeten Farben.
        code_length: Anzahl der benötigten Bits pro Farbsymbol.
        rows: Anzahl der Zeilen des Bildes.
        cols: Anzahl der Spalten des Bildes.

    Returns:
        Ein Tupel mit formatierten Strings für die UI-Labels:

        - Kompressionsanzeige (Fortschrittsbalken)
        - Prozentuale Datenersparnis
        - Kompressionsverhältnis
        - Dateigröße
        - Bit pro Pixel
        - Anzahl der verwendeten Farben
    """
    # Metadaten (3 Byte = Höhe, Breite und Anzahl Farben)
    # + Palettenspeicher (Anzahl Farben * 8 Bit * (3 Byte RGB + 1 Byte Index))
    # + Bilddaten (Bit pro Code * Höhe * Breite)
    clr_bits = (3 * 8) + (color_count * 8 * 4) + (code_length * rows * cols)
    comp = clr_bits / image_bits
    percent = (1 - comp) * 100

    byte_size = bit_to_size(clr_bits)
    byte_comp = bit_to_comp(comp, image_bits, clr_bits)
    byte_percent = bit_to_percent(percent)
    byte_bar = bit_to_bar(percent)
    bits_pixel = bit_to_pixel(code_length)
    color_count_string = (
        f"<span style='color: white;'>{color_count}</span> Anzahl Farben"
    )

    return byte_bar, byte_percent, byte_comp, byte_size, bits_pixel, color_count_string


# --------------------------------------------------------------------------------------
# String-Konvertierung (Formatierungshilfen)
# --------------------------------------------------------------------------------------


def bit_to_size(comp_bits: int) -> str:
    """
    Wandelt eine Dateigröße in Bits in einen formatierten String um.

    Args:
        comp_bits: Größe des Bildes in Bits.

    Returns:
        Formatierte Zeichenkette mit Bit- und Byte-Angabe.
    """
    comp_bytes = round(comp_bits / 8, 1)
    return (
        f"<span style='color: white;'>{comp_bits} Bit "
        f"({comp_bytes} Byte)</span> Dateigröße"
    )


def bit_to_comp(comp: float, image_bits: int, comp_bits: int) -> str:
    """
    Wandelt das Kompressionsverhältnis in einen formatierten String um.

    Args:
        comp: Kompressionsverhältnis (komprimiert / unkomprimiert).
        image_bits: Größe des unkomprimierten Bildes in Bits.
        comp_bits: Größe des komprimierten Bildes in Bits.

    Returns:
        Formatierte Zeichenkette mit Kompressionsverhältnis (z. B. ``1:2.5``).
    """
    comp_help = round(image_bits / comp_bits, 1) if comp_bits > 0 else 0.0
    comp_val = round(comp, 4)
    return (
        f"<span style='color: white;'>1:{comp_help} "
        f"(= {comp_val})</span> Kompressionsverhältnis"
    )


def bit_to_percent(percent: float) -> str:
    """
    Wandelt die prozentuale Datenersparnis in einen formatierten String um.

    Args:
        percent: Prozentuale Datenersparnis.

    Returns:
        Formatierte Zeichenkette mit Prozentangabe.
    """
    percent_val = round(percent, 1)
    return (
        f"<span style='color: white;'>{percent_val}%</span> Prozentuale Datenersparnis"
    )


def bit_to_bar(percent: float) -> str:
    """
    Wandelt die prozentuale Datenersparnis in einen visuellen Fortschrittsbalken um.

    Args:
        percent: Prozentuale Datenersparnis.

    Returns:
        Visuelle Kompressionsanzeige als HTML-String.
    """
    # 50 Stellen auf dem Balken (100%), daher entspricht jeder Block 2%
    no_bars = int(percent / 2)
    bars = 50 - no_bars

    if bars <= 50:
        inside_bars = "█" * max(0, bars)
        byte_bar = f"<span style='color: white;'>{inside_bars}</span>"
        byte_bar += "_" * max(0, no_bars - 1)
        byte_bar += "]"
    else:
        byte_bar = (
            "<span style='color: white;'>"
            "█████████████████████████████████████████████████</span>]"
        )
        if bars < 60:
            extra_bars = "█" * (bars - 50)
            byte_bar += f"<span style='color: red;'>{extra_bars}</span>"
        else:
            byte_bar += "<span style='color: red;'>██████...</span>"
    return byte_bar


def bit_to_pixel(bits: float) -> str:
    """
    Wandelt die Bitanzahl pro Pixel in einen formatierten String um.

    Args:
        bits: Bitanzahl pro Pixel.

    Returns:
        Formatierte Zeichenkette mit Bit- und Byte-Angabe pro Pixel.
    """
    num_bytes = round(bits / 8, 2)
    return f"<span style='color: white;'>{bits} Bit ({num_bytes} Byte)</span> Bit pro Pixel"
