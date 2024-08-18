from typing import Any
from components.classes.core import *
import pygame as pg

class Shape:
    
    def __init__(self, **args) -> None:
        self.enabled = True
        print(args )
        for key, value in args.items():
            setattr(self, key, value)
    
    def surf(self) -> pg.Surface :
        return self.master.surf.copy() 
    
    def render(self):
        master = self.master
        w,h = master.get_size()
        x = (self.x or 0) + w / 2
        y = (self.y or 0) + h / 2
        master.surf.blit(self.surf, (x, y))

    def __getattribute__(self, name: str) -> Any:
        return hasattr(self, name) and self[name] or None

    def remove(self):
        self.enabled = False