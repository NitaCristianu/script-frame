from components.utils.easing import *

def inRect(ax = 0, ay = 0, x = 0, y = 0, w = 0, h = 0):
    return ax > x and ax < x + w and ay > y and ay < y + h 

def invLerp(a, b, v):
    if b == a: return 0
    return (v-a) / (b-a)

def lerp(a,b,t):
    return a + (b-a) * t

def lerpMap(a0,b0,a1,b1,v, ease = linear):
    """
    returns from a0 - b0 space
    to a1 b1 space
    """
    return lerp(a1,b1,ease(invLerp(a0,b0,v)))

def clamp(x: float, mi : float, ma : float):
    return min(max(x, mi), ma)

def distPoints(ax, ay, bx, by):

    return (bx - ax) * (bx - ax) + (by - ay) * (by - ay)