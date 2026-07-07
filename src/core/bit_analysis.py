# ----------------------------------------
# Bit-Berechnungen
# ----------------------------------------


def rle_to_bit(image_bits, run_length_count):
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
    bits_pixel = "<span style='color: white;'>27 Bit (3 Byte)</span> #Bit pro Pixel"
    return byte_bar, byte_percent, byte_comp, byte_size, bits_pixel


def clr_to_bit(image_bits, color_count, code_length, rows, cols):
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
    return byte_bar, byte_percent, byte_comp, byte_size, bits_pixel


# ----------------------------------------
# to String
# ----------------------------------------


def rgb_to_bit(image_bits):
    byte_bar = "<span style='color: white;'>██████████████████████████████████████████████████</span>"
    byte_percent = "<span style='color: white;'>0%</span> #Prozentuale Datenersparnis"
    byte_comp = "<span style='color: white;'>1:1 (= 1)</span> #Kompressionsverhältnis"
    byte_size = f"<span style='color: white;'>{image_bits} Bit ({image_bits / 8} Byte)</span> #Dateigröße"
    bits_pixel = "<span style='color: white;'>27 Bit (3 Byte)</span> #Bit pro Pixel"
    return byte_bar, byte_percent, byte_comp, byte_size, bits_pixel


def bit_to_size(comp_bits):
    return f"<span style='color: white;'>{comp_bits} Bit ({round(comp_bits / 8, 1)} Byte)</span> #Dateigröße"


def bit_to_comp(comp, comp_help):
    return f"<span style='color: white;'>1:{round(comp_help, 1)} (= {round(comp, 4)})</span> #Kompressionsverhältnis"


def bit_to_percent(percent):
    return f"<span style='color: white;'>{round(percent, 1)}%</span> #Prozentuale Datenersparnis"


def bit_to_bar(percent):
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


def bit_to_pixel(code_length):
    return f"<span style='color: white;'>{code_length} Bit ({round(code_length / 8, 2)} Byte)</span> #Bit pro Pixel"
