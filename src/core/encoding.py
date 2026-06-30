from collections import Counter

def encode_rgb(pixel_data, color_index):
    """
    Konvertiert die Integer von pixel_data in einen String mit RGB-Codes um.
    """
    rgb_text = ""
    for row in pixel_data:
        for index in row:
            color = color_index[index]
            rgb_text += f"[{color.red():3}, {color.green():3}, {color.blue():3}]\n"
        # rgb_text += "\n" # Raster Form beibehalten
    return rgb_text

def encode_rle(pixel_data, color_index):
    """
    Setzt die Lauflängencodierung auf pixel_data an.
    Erst wird eine Liste von Tupeln (Anzahl, Farbindex) und dann ein String daraus erstellt.
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

    rle_text = ""
    for i, index in rle_data:
        color = color_index[index]
        rle_text += f"{i}: [{color.red():3}, {color.green():3}, {color.blue():3}]\n"
    return rle_text

def encode_clr(pixel_data, color_index):
    """
    Setzt die indizierten-Farben-Codierung auf pixel_data an.
    """
    pixel_data_list = array_to_list(pixel_data)
    pixel_data_count = Counter(pixel_data_list)
    rle_data = pixel_data_count.most_common()

    clr_text = ""
    for index, i in rle_data:
        color = color_index[index]
        clr_text += f"{i}: [{color.red():3}, {color.green():3}, {color.blue():3}]\n"
    return clr_text

def array_to_list(array):
    list = []
    for row in array:
        for i in row:
            list.append(i)
    return list