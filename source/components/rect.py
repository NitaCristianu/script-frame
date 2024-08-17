import pygame as pg
from config.projectData import *
from pygame import gfxdraw

class Main():
    def __init__(self) -> None:
        self.props: List['Prop'] = [
            # {
            #     'name' : 'color',
            #     'value' : (255, 0, 0),
            #     'propType' : 'rgb',
            #     'additinoal' : []
            # }
        ]

    def render(self, t : float, surf : pg.Surface) -> None:
        pg.draw.rect(surf,(255, 0, 0), pg.Rect(0, 0, *(x/2 - 2 for x in surf.get_size())))
        return surf
