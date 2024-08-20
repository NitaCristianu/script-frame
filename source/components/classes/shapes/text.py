
from components.classes.shape import *
from classes.components.core.Text import *
from utils.shapes import *

class Text(Shape):
    def __init__(self, **args) -> None:
        self.color = (255, 255, 255, 0)
        self.fontHeight = 128
        self.italic = False
        self.text = ""
        self.font = "Poppins"
        self.weight = 'normal'
        
        super().__init__(**args)

    def getSize(self):
        font = getFont(self.font, self.italic, self.weight, self.fontHeight)
        text_surf = font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect(
            topleft = (self.x, self.y)
        ) 
        w,h = text_rect.w, text_rect.h
        return (w, h)

    def surf(self):
        
        surf =  super().surf()
        font = getFont(self.font, self.italic, self.weight, self.fontHeight)
        text_surf = font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect(
            topleft = (self.x, self.y)
        ) 
        surf.blit(text_surf, text_rect)

        return surf