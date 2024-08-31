from config.projectData import *
from components.classes.scene import *
from components.classes.shapes.rectangle import *

class Main(Scene):

    def __init__(self) -> None:
        super().__init__()
        self.bgr = self.add(rectangle(
            self,
            w = 1920,
            h = 1080,
            color = pg.Color("blue")
        ))
    

    def render(self):
        self.wait(3)