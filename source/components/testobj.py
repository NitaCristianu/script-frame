import pygame as pg
from config.projectData import *
from components.classes.node import *
from components.classes.scene import *
from components.classes.shapes.rectangle import *
from components.classes.shapes.text import *

class Main(Scene):

    def __init__(self) -> None:
        super().__init__()
        self.a = self.add(rectangle(self,
                                    color = pg.Color("blue")
                                    ))
        self.a.w.share("rect width", "slider", min = 0, max = 500)
        self.a.color.share("rect color", "color1")

    def render(self):
        self.a.radius(0, 1)
        self.a.h(700, 1)
        self.wait(2)
        self.a.radius(100, 1)
        self.wait(2)
