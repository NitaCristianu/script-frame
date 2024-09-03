import pygame as pg
from utils.shapes import *
from classes.components.core.Text import getFont
from components.classes.node import *
from components.utils.textutil import wrap_multi_line

class text(Node):
    
    def __init__(self, master, **args) -> None:
        super().__init__(master, **({
            'color' : pg.Color('white'),
            'text' : "", 
            'weight' : 'normal',
            'fontheight' : 64,
            'italic' : True,
            'font' : "Poppins",
            'wrap' : False
            } | args))
        if not self.wrap():
            self.w = Signal(lambda : self.calcsize()[0], self.master)
            self.h = Signal(lambda : self.calcsize()[0], self.master)
            

    def calcsize(self) -> None:
        if self.wrap(): return self.w, self.h
        fontobj = getFont(self.font(), self.italic(), self.weight(), self.fontheight())
        if not fontobj: return 0, 0
        text_surf = fontobj.render(self.text(), True, self.color())
        sw, sh = text_surf.get_size()
        return sw, sh


    def render(self) -> None:
        if len(self.text()) == 0: return
        rect = self.rect
        
        self.fontobj = getFont(self.font(), self.italic(), self.weight(), self.fontheight())
        if self.wrap() and rect.w > 0:
            sequences = wrap_multi_line(self.text(), self.fontobj, rect.w)
            for i, text in enumerate(sequences):
                offsetY = i * (self.fontheight() + 3)
                if self.centered():
                    offsetY -= (len(sequences)-1) * (self.fontheight() + 3) / 2
                text_surf = self.fontobj.render(text, True, self.color())
                text_rect = text_rect = text_surf.get_rect(center = (rect.centerx, rect.centery + offsetY))
                self.master.surf.blit(text_surf, text_rect)
        else:
            text_surf = self.fontobj.render(self.text(), True, self.color())
            text_rect = text_rect = text_surf.get_rect(center = rect.center)
            self.master.surf.blit(text_surf, text_rect)
        return super().render()