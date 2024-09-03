from components.classes.customs.codeblock import *
from components.classes.shapes.rectangle import *
from components.classes.scene import *
from components.utils.signal import *


class Main(Scene):

    def __init__(self) -> None:
        super().__init__()

        w, h = 1920, 1080


        self.codestr = Signal("""print("Hello me, meet the real me")""", self)

        self.code = self.add(codeblock(self,
                                       x=0,
                                       y=0,
                                       w=w,
                                       h=h,
                                       centered = False,
                                       fontHeight = 50,
                                       code=self.codestr,


                                       ))

    def render(self):
        self.codestr('print("Hello me, meet the real me ")', 2)
        self.wait(2)
        self.codestr('print("Hello world!")', 2)
        self.wait(4)
