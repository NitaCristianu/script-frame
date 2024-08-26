import pygame as pg
from utils.shapes import *
from classes.components.core.Text import getFont
from components.classes.node import *

class text(Node):
    
    def __init__(self, master, **args) -> None:
        super().__init__(master, **({
            'color' : pg.Color('white'),
            'text' : "", 
            'weight' : 'normal',
            'fontheight' : 64,
            'italic' : True,
            'font' : "Poppins",
            'centeredX' : False,
            'centeredY' : False,
            'centered' : False,
            } | args))
        self.w = lambda : self.calcsize()[0]
        self.h = lambda : self.calcsize()[0]
            

    def calcsize(self) -> None:
        fontobj = getFont(self.font(), self.italic(), self.weight(), self.fontheight())
        if not fontobj: return 0, 0
        text_surf = fontobj.render(self.text(), True, self.color())
        sw, sh = text_surf.get_size()
        return sw, sh
    def render(self) -> None:
        x,y,w,h = 0, 0, self.w(), self.h()
        parent = self
        while parent:
            x += parent.x()
            y += parent.y()
            parent = parent.parent
        
        self.fontobj = getFont(self.font(), self.italic(), self.weight(), self.fontheight())
        text_surf = self.fontobj.render(self.text(), True, self.color())
        text_rect = None

        if self.centered() or (self.centeredX() and self.centeredY()):
            text_rect = text_surf.get_rect(center = (x, y))
        elif self.centeredX() and not self.centeredY():
            text_rect = text_surf.get_rect(center = (x, y))
            text_rect.topleft = (text_rect.topleft[0], y)
        else:
            text_rect = text_surf.get_rect(topleft = (x,y))
        
        
        self.master.surf.blit(text_surf, text_rect)
        