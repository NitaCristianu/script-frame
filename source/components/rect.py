import pygame as pg
from config.projectData import *
from components.classes.core import *
from components.classes.shapes.rect import *
from pygame import gfxdraw

class Main(Core):

    def render(self, t : float, surf : pg.Surface) -> None:
        super().render(t)
        self.rect = Rect(
            x = 10,
            y = 10,
            w = 300,
            h = 300
        )
        self.wait(0.5)
        return surf