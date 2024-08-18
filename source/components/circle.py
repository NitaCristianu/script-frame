import pygame as pg
from pygame import gfxdraw

class Main():
    def __init__(self) -> None:
        self.props = [
            {
                'name' : 'name',
                'value' : 1,
                'propType' : 'slider',
                'min' : 0.001,
                'max' : 5
               
            },
        ]
        

    def render(self, t : float, surf : pg.Surface) -> None:
        w,h = surf.get_size()
        x = int(t/self.props[0]['value'] * 1800 - 100) + w // 2
        gfxdraw.filled_circle(surf, x, int (h * 0.75), 100, (255, 255, 255))
        self.lenght = self.props[0]['value']
        return surf
