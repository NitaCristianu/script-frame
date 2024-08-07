import pygame as pg
from classes.components.Tab import *

FONTS = {
    'Poppins': {
        'italic': {
            'black': "Z:\\Projects\\Video-Editor\\assets\\font\\blackitalic.ttf",
            'extrabold': "Z:\\Projects\\Video-Editor\\assets\\font\\extrabolditalic.ttf",
            'bold': "Z:\\Projects\\Video-Editor\\assets\\font\\bolditalic.ttf",
            'semibold': "Z:\\Projects\\Video-Editor\\assets\\font\\semibolditalic.ttf",
            'medium': "Z:\\Projects\\Video-Editor\\assets\\font\\mediumitalic.ttf",
            'normal': "Z:\\Projects\\Video-Editor\\assets\\font\\italic.ttf",
            'thin': "Z:\\Projects\\Video-Editor\\assets\\font\\thinitalic.ttf",
            'light': "Z:\\Projects\\Video-Editor\\assets\\font\\lightitalic.ttf",
            'extralight': "Z:\\Projects\\Video-Editor\\assets\\font\\extralightitalic.ttf",
        },
        'normal': {
            'black': "Z:\\Projects\\Video-Editor\\assets\\font\\black.ttf",
            'extrabold': "Z:\\Projects\\Video-Editor\\assets\\font\\extrabold.ttf",
            'bold': "Z:\\Projects\\Video-Editor\\assets\\font\\bold.ttf",
            'semibold': "Z:\\Projects\\Video-Editor\\assets\\font\\semibold.ttf",
            'medium': "Z:\\Projects\\Video-Editor\\assets\\font\\medium.ttf",
            'normal': "Z:\\Projects\\Video-Editor\\assets\\font\\regular.ttf",
            'thin': "Z:\\Projects\\Video-Editor\\assets\\font\\thin.ttf",
            'light': "Z:\\Projects\\Video-Editor\\assets\\font\\light.ttf",
            'extralight': "Z:\\Projects\\Video-Editor\\assets\\font\\extralight.ttf",
        }
    }
}


class Text(Tab):

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
                 detectHover = False,
                 onHoverModifiedColor = 0.3,
                 ) -> None:
        super().__init__(dimension, app, color, borderValue, detectHover=detectHover, onHoverModifiedColor=onHoverModifiedColor)
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
        super().drawContent()
        text_surface = self.font.render(self.text, True, self.fontColor)
        h = self.autoHeight and self.fontHeight or self.h
        if (self.align == 'center'):
            text_rect = text_surface.get_rect(
                center=((self.x + (self.x + self.w))/2, (self.y + self.y + h)/2))
        else:
            text_rect = text_surface.get_rect(
                topleft=(self.x + self.padding, self.y+h/2 - self.fontHeight/2)
            )
        self.app.screen.blit(text_surface, text_rect)
