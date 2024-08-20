import pygame as pg
from config.projectData import *
from components.classes.core import *
from components.classes.shapes.rect import *

class Main(Core):

    def start(self):
        super().start()
        self.add("A",Rect(
            x = 10,
            y = 10,
            w = 0,
            h = 900,
            color = "red"
        ))
 
    def render(self, t : float, surf : pg.Surface) -> None:
        super().render(t, surf)
        self.play(self.get("A").transform, totalTime=1.5, name = "color", value = "blue")
        self.play(self.get("A").transform, totalTime=1.5, name = "w", value = 1600)
        self.wait(2.7)
        return surf