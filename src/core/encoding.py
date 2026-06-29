
def encode_rgb(pixel_data, color_index):
    """
    Konvertiert die Integer von pixel_data in einen String mit RGB-Codes um.
    """

    rgb_text = ""
    for row in pixel_data:
        for index in row:
            color = color_index[index]
            rgb_text += f"[{color.red():3}, {color.green():3}, {color.blue():3}]  "
        rgb_text += "\n"
    return rgb_text

def encode_rle(pixel_data):
    return

def encode_clr(pixel_data):
    return