from components.classes.shapes.rectangle import rectangle
from components.classes.customs.codeblock import codeblock
from components.classes.scene import *

class Main(Scene):

    def start(self) -> None:

        code ="""
style_dict = defaultdict(lambda : "#000000")
    for token, style in formatter.style:
        if style['color']:
            style_dict[token] = f"#{style['color']}"
"""

        self.bgr = self.add(rectangle(self, w = '100%', h = '100%', color = "#222222"))
        self.code = self.add(codeblock(self, code = code, fontheight = 60))
        
    def render(self):
        self.bgr.w('50%', 4)
        self.code.fontheight(10, 3)
        self.wait(5)
    