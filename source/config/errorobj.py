from config.projectData import *
from components.classes.scene import *
from components.classes.shapes.rectangle import rectangle
from components.classes.shapes.text import text

class Main(Scene):

    def __init__(self) -> None:
        super().__init__()
        self.bgr = self.add(rectangle(
            self,
            x = 0,
            y = 0,
            w = 1920,
            h = 1080,
            color = pg.Color("red")
        ))
        self.errormessage = "error : unknown"
        self.font = self.add(text(self,
                                  x = 1920/2,
                                  y = 1080/2,
                                  text = "Error",
                                  centered = True,
                                  weight = 'bold'
                                  ))
        

    def render(self):
        self.font.text(self.errormessage, 1)
        self.wait(3)
