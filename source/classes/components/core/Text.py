import pygame as pg
import os
from classes.components.core.Rect import *

FONTS = {
    'Poppins': {
        'italic': {
            'black': r"assets\font\blackitalic.ttf",
            'extrabold': r"assets\font\extrabolditalic.ttf",
            'bold': r"assets\font\bolditalic.ttf",
            'semibold': r"assets\font\semibolditalic.ttf",
            'medium': r"assets\font\mediumitalic.ttf",
            'normal': r"assets\font\italic.ttf",
            'thin': r"assets\font\thinitalic.ttf",
            'light': r"assets\font\lightitalic.ttf",
            'extralight': r"assets\font\extralightitalic.ttf",
        },
        'normal': {
            'black': r"assets\font\black.ttf",
            'extrabold': r"assets\font\extrabold.ttf",
            'bold': r"assets\font\bold.ttf",
            'semibold': r"assets\font\semibold.ttf",
            'medium': r"assets\font\medium.ttf",
            'normal': r"assets\font\regular.ttf",
            'thin': r"assets\font\thin.ttf",
            'light': r"assets\font\light.ttf",
            'extralight': r"assets\font\extralight.ttf",

        }
    }
}


class Text(Rect):

    text: str
    align: str
    fontColor: str
    fontHeight: int
    padding: int
    autoHeight: True

    def __init__(self,
                 dimension: tuple[int, int, int, int],
                 app: any,
                 color: str = "#00000000",
                 borderValue=0,
                 font="Poppins",
                 italic=False,
                 weight='normal',
                 fontHeight=25,
                 text="",
                 align="center",
                 fontColor="#ececec",
                 padding=0,
                 autoHeight=True,
                 detectHover=False,
                 onHoverModifiedColor=0.3,
                 ) -> None:
        super().__init__(dimension, app, color, borderValue,
                         detectHover=detectHover, onHoverModifiedColor=onHoverModifiedColor)
        self.setFont(font, italic, weight, fontHeight)
        self.text = text
        self.fontColor = fontColor
        self.align = align
        self.padding = padding
        self.fontHeight = fontHeight
        self.autoHeight = autoHeight

    def setFont(self,
                font="Poppins",
                italic=False,
                weight='normal',
                fontHeight=25
                ) -> None:
        self.font = pg.font.Font(
            FONTS[font][italic and "italic" or "normal"][weight], fontHeight)

    def drawContent(self):
        if not self.enabled: return False
        super().drawContent()
        text_surface = self.font.render(self.text, True, self.fontColor)
        h = self.autoHeight and self.fontHeight or self.h
        if (self.align == 'center'):
            text_rect = text_surface.get_rect(
                center=((self.x + self.w//2, self.y + h//2))
            )
        else:
            text_rect = text_surface.get_rect(
                topleft=(self.x + self.padding, self.y +
                         h/2 - self.fontHeight/1.5)
            )
        self.app.screen.blit(text_surface, text_rect)
