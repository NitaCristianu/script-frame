def inRect(ax = 0, ay = 0, x = 0, y = 0, w = 0, h = 0):
    return ax > x and ax < x + w and ay > y and ay < y + h 

def clamp(x: float, mi : float, ma : float):
    return min(max(x, mi), ma)
