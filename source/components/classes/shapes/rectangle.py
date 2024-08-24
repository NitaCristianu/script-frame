import pygame as pg
from utils.shapes import *
from components.classes.node import *

class rectangle(Node):
    
    def __init__(self, master, **args) -> None:
        super().__init__(master, **({'color' : 'white', 'radius' : 0} | args))

    def render(self) -> None:
        x,y,w,h = 0, 0, self.w(), self.h()
        parent = self
        while (parent):
            x += parent.x()
            y += parent.y()
            parent = parent.parent
        
        pg.draw.rect(self.master.surf, self.color(), pg.Rect(x,y,w,h), 0, int(self.radius()))