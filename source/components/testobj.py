import pygame as pg
from config.projectData import *
from components.classes.node import *
from components.classes.scene import *
from components.classes.shapes.rectangle import *
from components.classes.shapes.text import *

class Main(Scene):

    def __init__(self) -> None:
        super().__init__()
        self.a = self.add(text(self,
                                    color = pg.Color("white"),
                                    # centered = True,
                                    weight = 'bold',
                                    fontheight = 100,
                                    centered = True,
                                    x = 800,
                                    y = 450
                                    ))
        self.a.color.share("rect color", "color1")
        self.signalA = Signal("Scrie ceva", self).share("textA", "textbox")

    def render(self):
        self.a.text("Scrie Ceva", 1)
        self.wait(2)
        self.a.text(self.signalA(), .4, linear)
        self.wait(2)
