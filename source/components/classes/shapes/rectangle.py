import pygame as pg
from utils.shapes import *
from components.classes.node import *

class rectangle(Node):
    
    def __init__(self, master, **args) -> None:
        super().__init__(master, **({'color' : 'white', 'radius' : 0} | args))

    def render(self) -> None:
        rect = self.rect
        opacity = self.get_opacity()
        if opacity < 0.001: return

        surf = pg.Surface(rect.size, pg.SRCALPHA, 32)
        pg.draw.rect(surf, self.color(), (0, 0, *rect.size), 0, int(self.radius()))
        
        if opacity < 1:
            surf.set_alpha(self.get_opacity())
        
        self.master.surf.blit(surf, rect.topleft)

        return super().render()