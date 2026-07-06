from collections import Counter
import math

#----------------------------------------
# Codierungen
#----------------------------------------

def encode_rle(pixel_data):
    """
    Setzt die Lauflängencodierung auf pixel_data an.
    Erstellt eine Liste von Tupeln (Lauflänge identischer Farben, Farbindex).
    """

    rle_data = []

    #--------------------
    # 2D-Struktur
    #--------------------

    # for row in pixel_data:
    #     count = 1
    #     prev_pixel = row[0]
    #     for col in range(1, len(row)):
    #         pixel = row[col]
    #         if pixel == prev_pixel:
    #             count += 1
    #         else:
    #             rle_data.append((count, prev_pixel))
    #             count = 1
    #             prev_pixel = pixel
    #     rle_data.append((count, prev_pixel))

    #--------------------
    # 1D-Struktur
    #--------------------

    pixel_data_list = array_to_list(pixel_data)
    count = 1
    prev_pixel = pixel_data_list[0]
    for i in range(1, len(pixel_data_list)):
        pixel = pixel_data_list[i]
        if pixel == prev_pixel:
            count += 1
        else:
            rle_data.append((count, prev_pixel))
            count = 1
            prev_pixel = pixel
    rle_data.append((count, prev_pixel))
    return rle_data

def encode_clr_bits(clr_count):
    """
    Erstellt effiziente Farbcodes.
    erstellt eien Liste von Tupeln (Bit-Code, Farbindex)
    """
    

def encode_clr(pixel_data):
    """
    Setzt die indizierte-Farben-Codierung auf pixel_data an.
    """
    pixel_data_list = array_to_list(pixel_data)
    pixel_data_count = Counter(pixel_data_list)
    # Farben und ihre Häufigkeit
    clr_frequencies = pixel_data_count.most_common()
    # Farben und ihre Codes
    clr_codes = {}
    clr_count = len(clr_frequencies)
    bits = math.ceil(math.log2(clr_count))
    for i, (color, _) in enumerate(clr_frequencies):
        bit_code = f"{i:0{bits}b}"
        # bit_code = f"{i:b}" # keine führenden nullen
        clr_codes[color] = bit_code
    clr_data = []
    for row in pixel_data:
        new_row = []
        for color in row:
            new_row.append(clr_codes[color])
        clr_data.append(new_row)
    return clr_data, clr_codes

def array_to_list(array):
    list = []
    for row in array:
        for i in row:
            list.append(i)
    return list

#----------------------------------------
# to String
#----------------------------------------

def rgb_to_string(rgb_data, color_index):
    """
    Konvertiert pixel_data in einen String.
    """
    rgb_text = ""
    for row in rgb_data:
        for index in row:
            rgb_color = color_index[index][0]
            str_color = color_index[index][1]
            r = rgb_color.red()
            g = rgb_color.green()
            b = rgb_color.blue()
            rgb_text += f"<br>{r:08b} {g:08b} {b:08b}<span style='color:gray'> #{r:3} {g:3} {b:3}; {str_color}</span>"
        # rgb_text += "\n" # Raster Form beibehalten
    return rgb_text

def rle_to_string(rle_data, color_index):
    """
    Konvertiert rle_data in einen String.
    """
    rle_text = ""
    for i, index in rle_data:
        rgb_color = color_index[index][0]
        str_color = color_index[index][1]
        r = rgb_color.red()
        g = rgb_color.green()
        b = rgb_color.blue()
        rle_text += f"<br>{i:08b} <span style='color:gray'>#{i:<2}</span> {r:08b} {g:08b} {b:08b} <span style='color:gray'>#{r:3} {g:3} {b:3}; {str_color}</span>"
    return rle_text

def clr_to_string(clr_data, color_codes, color_index):
    """
    Konvertiert clr_data in einen String.
    """
    rgb_codes = {}
    clr_text = "<span style='color:gray'>#Code | #Farbe<br>----------------------------------<br></span>"
    for index, code in color_codes.items():
        rgb_color = color_index[index][0]
        str_color = color_index[index][1]
        rgb_codes[code] = (rgb_color, str_color)
        r = rgb_color.red()
        g = rgb_color.green()
        b = rgb_color.blue()
        clr_text += f"{code:>5} <span style='color:gray'>|</span> {r:08b} {g:08b} {b:08b} <span style='color:gray'>#{r:3} {g:3} {b:3}; {str_color}</span><br>"
    for row in clr_data:
        for code in row:
            rgb_color = rgb_codes[code][0]
            str_color = rgb_codes[code][1]
            r = rgb_color.red()
            g = rgb_color.green()
            b = rgb_color.blue()
            clr_text += f"<br>{code} <span style='color:gray'>#{r:3} {g:3} {b:3}; {str_color}</span>"
        # clr_text += "\n" # Raster Form beibehalten
    return clr_text