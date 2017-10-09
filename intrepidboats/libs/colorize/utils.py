import webcolors
from PIL import Image
from PIL.ImageColor import getcolor, getrgb
from PIL.ImageOps import grayscale, colorize

TRANSPARENT = 0


def hard_light(old, new):
    float_new = new / 255.0
    float_old = old / 255.0
    value = None
    if float_new < 0.5:
        value = 2 * float_new * float_old * 255
    else:
        value = ((1 - (2 * (1 - float_new) * (1 - float_old))) * 255)
    return int(value)


def to_new_pixel(old_colors, new_colors, alpha):
    new_value = (
        hard_light(old_colors[0], new_colors[0]),
        hard_light(old_colors[1], new_colors[1]),
        hard_light(old_colors[2], new_colors[2]),
        alpha
    )
    return new_value


def get_new_pixel(image, coor, new_colors, alpha):
    old_colors = image.getpixel(coor)
    return to_new_pixel(old_colors, new_colors, alpha)


def get_pixel(pixel, new_colors):
    alpha = pixel[3]
    if alpha != TRANSPARENT:
        return to_new_pixel(pixel, new_colors, alpha)
    else:
        return pixel


def get_image_colorized(image, hex_color):
    """
    image: Image file
    hex_color: html hexadecimal color
    TODO: This is too slow, 1 sec aprox :V
    """
    new_colors = webcolors.hex_to_rgb(hex_color)
    width, height = image.size
    alpha_layer = image.split()[-1]
    for x_coor in range(width):
        for y_coor in range(height):
            alpha = alpha_layer.getpixel((x_coor, y_coor))
            if alpha != TRANSPARENT:
                new_pixel = get_new_pixel(image, (x_coor, y_coor), new_colors, alpha)
                image.putpixel((x_coor, y_coor), new_pixel)
    return image


def yatint_image(img, color):
    # Yet another tint image function
    # Record: 0.55s
    new_colors = webcolors.hex_to_rgb(color)
    all_data = img.getdata()
    img.putdata([get_pixel(pixel, new_colors) for pixel in all_data])
    return img


def tint_image(src, color="#FFFFFF"):
    """ Faster implementation of the above method """
    src.load()
    alpha = src.split()[3]  # r,g,b,alpha
    gray = grayscale(src)
    result = colorize(gray, (0, 0, 0, 0), color)
    result.putalpha(alpha)
    return result


def get_colorized(image_path, hex_color):
    """
    image_path: Full path to image
    hex_color: html hexadecimal color
    """
    original = Image.open(image_path).convert('RGBA')
    return get_image_colorized(image=original, hex_color=hex_color)


def merge_images(backgroud_path, ims_definitions):
    """
    backgroud_path: full path to background image
    ims_definitions: list if ImageDefinition dicts:
    ImageDefinition dict: a dict with two keys:
        "image_path": full path to Image
        "hex_color": html hexadecimal color
    """
    original = Image.open(backgroud_path).convert('RGBA')
    for definition in ims_definitions:
        image = get_colorized(definition['image_path'], definition['hex_color'])
        original.paste(image, (0, 0), image)
    return original
