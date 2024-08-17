import pygame as pg
from pygame import gfxdraw

class Main():
    def __init__(self) -> None:
        self.props = {}
        
    def render(self, t : float, surf : pg.Surface) -> None:
        x = int(t/2 * 1600)
        gfxdraw.filled_circle(surf, x, 200, 100, (255, 255, 255))
        return surf
