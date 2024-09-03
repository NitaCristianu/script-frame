import pygame as pg
from utils.shapes import *
from components.classes.node import *

class rectangle(Node):
    
    def __init__(self, master, **args) -> None:
        super().__init__(master, **({'color' : 'white', 'radius' : 0} | args))

    def render(self) -> None:
        pg.draw.rect(self.master.surf, self.color(), self.rect, 0, int(self.radius()))

        return super().render()