# ----------------------------------------
# Bit-Berechnungen
# ----------------------------------------


def rgb_to_bit(
    image_bits: int, rows: int, cols: int
) -> tuple[str, str, str, str, str, str]:
    """
    Erzeugt lesbare Informationen der CLR-Codierung für die Datenanzeige.

    Args:
        image_bits: Größe des Bildes in Bits in der RGB-Codierung.
        rows: Anzahl der Reihen des Bildes.
        cols: Anzahl der Spalten des Bildes.

    Returns:
        Formatierte Informationen zur CLR-Codierung:
        Kompressionsanzeige, prozentuale Datenersparnis, Kompressionsverhältnis,
        Dateigröße, Bit pro Pixel, Anzahl der Pixel des Bildes.
    """
    byte_bar = "<span style='color: white;'>██████████████████████████████████████████████████</span>"
    byte_percent = "<span style='color: white;'>0%</span> #Prozentuale Datenersparnis"
    byte_comp = "<span style='color: white;'>1:1 (= 1)</span> #Kompressionsverhältnis"
    byte_size = f"<span style='color: white;'>{image_bits} Bit ({image_bits / 8} Byte)</span> #Dateigröße"
    bits_pixel = "<span style='color: white;'>24 Bit (3 Byte)</span> #Bit pro Pixel"
    resolution = f"<span style='color: white;'>{rows * cols}</span> #Anzahl Pixel"
    return byte_bar, byte_percent, byte_comp, byte_size, bits_pixel, resolution


def rle_to_bit(
    image_bits: int, run_length_count: int, run_length_length: list[int]
) -> tuple[str, str, str, str, str, str]:
    """
    Erzeugt lesbare Informationen der RLE-Codierung für die Datenanzeige.

    Args:
        image_bits: Größe des Bildes in Bits in der RGB-Codierung.
        run_length_count: Anzahl der vorkommenden Lauflängen.
        run_length_length: Längen der vorkommenden Lauflängen.

    Returns:
        Formatierte Informationen zur RLE-Codierung:
        Kompressionsanzeige, prozentuale Datenersparnis, Kompressionsverhältnis,
        Dateigröße, Bit pro Pixel, durchschnittlische Lauflänge.
    """
    # Meta-Daten werden als jeweils ein Byte gespeichert (Höhe und Breite)
    # (Höhe + Breite) + (Anzahl Lauflängen * 8 Bit * (3 RGB + 1 Lauflängenzähler))
    rle_bits = (2 * 8) + (run_length_count * 8 * 4)
    comp = rle_bits / image_bits
    comp_help = image_bits / rle_bits
    percent = (1 - comp) * 100
    byte_size = bit_to_size(rle_bits)
    byte_comp = bit_to_comp(comp, comp_help)
    byte_percent = bit_to_percent(percent)
    byte_bar = bit_to_bar(percent)
    bits_pixel = "<span style='color: white;'>24 Bit (3 Byte)</span> #Bit pro Pixel"
    avg_run_length = f"<span style='color: white;'>{round(sum(run_length_length) / run_length_count, 1)}</span> #Durchschnittlische Lauflänge"
    return byte_bar, byte_percent, byte_comp, byte_size, bits_pixel, avg_run_length


def clr_to_bit(
    image_bits: int, color_count: int, code_length: int, rows: int, cols: int
) -> tuple[str, str, str, str, str, str]:
    """
    Erzeugt lesbare Informationen der CLR-Codierung für die Datenanzeige.

    Args:
        image_bits: Größe des Bildes in Bits in der RGB-Codierung.
        color_count: Anzahl der verwendeten Farben.
        code_length: Anzahl der benötigten Bits der einzelnen Farbcodierungen.
        rows: Anzahl der Reihen des Bildes.
        cols: Anzahl der Spalten des Bildes.

    Returns:
        Formatierte Informationen zur CLR-Codierung:
        Kompressionsanzeige, prozentuale Datenersparnis, Kompressionsverhältnis,
        Dateigröße, Bit pro Pixel, Anzahl der verwendeten Farbe.
    """
    # Meta-Daten werden als jeweils ein Byte gespeichert (Höhe, Breite und Anzahl Farben)
    # (Höhe + Breite + Anzahl Farben) + (Anzahl Farben * 8 Bit * (3 RGB + 1 Farbcode)) + (Bit pro Code * Höhe * Länge)
    clr_bits = (3 * 8) + (color_count * 8 * 4) + (code_length * rows * cols)
    comp = clr_bits / image_bits
    comp_help = image_bits / clr_bits
    percent = (1 - comp) * 100
    byte_size = bit_to_size(clr_bits)
    byte_comp = bit_to_comp(comp, comp_help)
    byte_percent = bit_to_percent(percent)
    byte_bar = bit_to_bar(percent)
    bits_pixel = bit_to_pixel(code_length)
    color_count_string = (
        f"<span style='color: white;'>{color_count}</span> #Anzahl Farben"
    )
    return byte_bar, byte_percent, byte_comp, byte_size, bits_pixel, color_count_string


# ----------------------------------------
# to String
# ----------------------------------------


def bit_to_size(comp_bits: int) -> str:
    """
    Wandelt Dateigröße in einen lesbaren String um.

    Args:
        comp_bits: Größe des Bildes in Bits in der jeweiligen komprimierten Codierung.

    Returns:
        Informationen über die Dateigröße.
    """
    return f"<span style='color: white;'>{comp_bits} Bit ({round(comp_bits / 8, 1)} Byte)</span> #Dateigröße"


def bit_to_comp(comp: float, comp_help: float) -> str:
    """
    Wandelt Kompressionsverhältnis in einen lesbaren String um.

    Args:
        comp: Kompressionsverhältnis
        comp_help: (RGB-Codierung / komprimierte Codierung) = x -> 1:x.

    Returns:
        Informationen über das Kompressionsverhältnis.
    """
    return f"<span style='color: white;'>1:{round(comp_help, 1)} (= {round(comp, 4)})</span> #Kompressionsverhältnis"


def bit_to_percent(percent: float) -> str:
    """
    Wandelt prozentuale Datenersparnis in einen lesbaren String um.

    Args:
        percent: prozentuale Datenersparnis.

    Returns:
        Informationen über die prozentuale Datenersparnis.
    """
    return f"<span style='color: white;'>{round(percent, 1)}%</span> #Prozentuale Datenersparnis"


def bit_to_bar(percent: float) -> str:
    """
    Wandelt prozentuale Datenersparnis in eine visuelle Kompressionsanzeige um.

    Args:
        percent: prozentuale Datenersparnis.

    Returns:
        Visuelle Kompressionsanzeige.
    """
    # 50 Stellen auf dem (100%)-Balken, daher stellt jeder Balken 2% dar
    no_bars = int(percent / 2)
    bars = 50 - no_bars
    if bars <= 50:
        inside_bars = "█" * bars
        data_bar = f"<span style='color: white;'>{inside_bars}</span>"
        data_bar += "_" * (no_bars - 1)
        data_bar += "]"
    else:
        data_bar = "<span style='color: white;'>█████████████████████████████████████████████████</span>]"
        if bars < 60:
            extra_bars = "█" * (bars - 50)
            data_bar += f"<span style='color: red;'>{extra_bars}</span>"
        else:
            data_bar += "<span style='color: red;'>██████...</span>"
    return data_bar


def bit_to_pixel(code_length: int) -> str:
    """
    Wandelt Bit pro Pixel in einen lesbaren String um.

    Args:
        code_length: Bit pro Pixel.

    Returns:
        Informationen über die Bitanzahl pro Pixel.
    """
    return f"<span style='color: white;'>{code_length} Bit ({round(code_length / 8, 2)} Byte)</span> #Bit pro Pixel"
