def linear(t: float):
    return t

def inoutcubic(t : float):
    return t < 0.5 and 4 * t * t * t or 1 - pow(-2 * t + 2, 3) / 2
