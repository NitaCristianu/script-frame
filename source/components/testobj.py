import pygame as pg
from config.projectData import *
from components.classes.node import *
from components.classes.scene import *
from components.classes.shapes.rectangle import *
from components.classes.shapes.text import *

class Main(Scene):

    def __init__(self) -> None:
        super().__init__()
        self.bgr = self.add(rectangle(self,
                                    color = pg.Color("black"),
                                    w = 1600,
                                    h = 900,
                                    ))
        self.a = self.add(text(self,
                                    color = pg.Color("white"),
                                    # centered = True,
                                    weight = 'bold',
                                    fontheight = 100,
                                    centered = True,
                                    x = 800,
                                    y = 450
                                    ))

    def render(self):
        self.a.text("Lorem ipsum", 1)
        self.bgr.color(pg.Color("red"), 1)
        self.wait(2)
        self.a.text("Ipsum Lorem", .4, linear)
        self.bgr.color(pg.Color("blue"), 1)
        self.wait(1)
        self.playAudio("test3.wav")
        self.wait(2)
