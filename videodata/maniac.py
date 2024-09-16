from components.classes.shapes.rectangle import rectangle
from components.classes.customs.codeblock import codeblock
from components.classes.scene import *

class Main(Scene):

    def start(self) -> None:

        code ="""print('You put him in control')"""

        self.bgr = self.add(rectangle(self, w = '100%', h = '100%', color = "#222222"))
        self.code: codeblock = self.add(codeblock(self, code = code, fontheight = 60))
        
    def render(self):
        self.wait(1)
        self.code.editat(0, 0)("warn", 0.4)
        self.wait(5)
    