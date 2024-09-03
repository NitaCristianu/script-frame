from utils.math import clamp
import pygame

def hex_to_rgb(hex_color):
    if isinstance(hex_color, pygame.Color):
        return (hex_color.r, hex_color.g, hex_color.b, hex_color.a)
    if isinstance(hex_color, tuple):
        return hex_color
    if isinstance(hex_color, list):
        return tuple(hex_color)
    hex_color = hex_color.lstrip('#')

    # Determine if the hex color includes alpha
    if len(hex_color) == 6:
        # Convert the hex string to an integer tuple (R, G, B)
        rgb_tuple = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (rgb_tuple[0], rgb_tuple[1], rgb_tuple[2], 255)
    elif len(hex_color) == 8:
        # Convert the hex string to an integer tuple (R, G, B, A)
        rgba_tuple = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4, 6))
        return rgba_tuple
    else:
        return hex_color

def saturate(rgb, n : float):
    col = pygame.Color(*rgb)
    col.hsla = (col.hsla[0], clamp(col.hsla[1] + n * col.hsla[1], 0, 100), col.hsla[2], col.hsla[3])
    return hex_to_rgb(col)

def modifyRGB(rgbColor: tuple[int, int, int] | tuple[int, int, int, int], n: float):
    if isinstance(rgbColor, str): return rgbColor
    return (
        tuple(int(clamp(i + n * 255, 0, 255)) for i in rgbColor)
    )

def invertColor(rgbColor:tuple[int, int, int] | tuple[int, int, int, int] ):
    if isinstance(rgbColor, str): return rgbColor
    return (
        255 - rgbColor[0],
        255 - rgbColor[1],
        255 - rgbColor[2],
        len(rgbColor) == 3 and 255 or rgbColor[3]
    )

VALID_COLORS = {
    'black', 'white', 'red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'gray', 
    'lightgray', 'darkgray', 'lightblue', 'darkblue', 'lightgreen', 'darkgreen', 
    'lightred', 'darkred', 'lightyellow', 'darkyellow', 'lightcyan', 'darkcyan', 
    'lightmagenta', 'darkmagenta', 'orange', 'purple', 'brown', 'pink'
}

def isStringAColor(a:any):
    if not isinstance(a, str): return False
    if (len(a) == 7 or len(a) == 9) and a[0] == "#": return True
    if a in VALID_COLORS: return True
    return False