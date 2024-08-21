import pygame as pg
from config.projectData import *
from components.classes.core import *
from components.classes.shapes.rectangle import *
from components.classes.shapes.text import *

class Main(Core):

    def start(self):
        super().start()
        self.setProp("x", 0, "slider", min = 0, max = 500)
        self.add("B",Rectangle(
            x = 0,
            y = 0,
            w = 1600,
            h = 900,
            color = "#ff00ff"
        ))
        self.add("A",Rectangle(
            x = 0,
            y = 50,
            w = 0,
            h = 700,
            color = "#ffaaaaa0",
            borderRadius = 15
        ))
        self.add("titlu", Text(
            text = "Hello World12",
            weight = "bold",
            x = 0,
            y = 200,
            color = pg.Color(255,255,255),
        ))
 
    def render(self, t : float, surf : pg.Surface) -> None:
        super().render(t, surf)
        x = self.getProp("x")
        self.play(self.get("A").transform, totalTime=2.5, name = "color", value = "#bb5b5a80")
        self.play(self.get("A").transform, totalTime=2.5, name = "w", value = 1600)
        self.play(self.get("titlu").transform, totalTime=1.5, name = "x", value = x)
        self.play(self.get("titlu").transform, totalTime=1.5, name = "text", value = "Hello Matei Oprea")
        self.wait(2.5)
        self.play(self.get("titlu").transform, totalTime=1.5, name = "x", value = 0)
        self.wait(1.5)
        self.play(self.get("titlu").transform, totalTime=1.5, name = "x", value = 1600)
        self.wait(1.5)
        return surf