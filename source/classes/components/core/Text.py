import pygame as pg
import os
from classes.components.core.Rect import *

FONTS = {
    'Poppins': {
        'italic': {
            'black': r"assets\font\poppins\blackitalic.ttf",
            'extrabold': r"assets\font\poppins\extrabolditalic.ttf",
            'bold': r"assets\font\poppins\bolditalic.ttf",
            'semibold': r"assets\font\poppins\semibolditalic.ttf",
            'medium': r"assets\font\poppins\mediumitalic.ttf",
            'normal': r"assets\font\poppins\italic.ttf",
            'thin': r"assets\font\poppins\thinitalic.ttf",
            'light': r"assets\font\poppins\lightitalic.ttf",
            'extralight': r"assets\font\poppins\extralightitalic.ttf",
        },
        'normal': {
            'black': r"assets\font\poppins\black.ttf",
            'extrabold': r"assets\font\poppins\extrabold.ttf",
            'bold': r"assets\font\poppins\bold.ttf",
            'semibold': r"assets\font\poppins\semibold.ttf",
            'medium': r"assets\font\poppins\medium.ttf",
            'normal': r"assets\font\poppins\regular.ttf",
            'thin': r"assets\font\poppins\thin.ttf",
            'light': r"assets\font\poppins\light.ttf",
            'extralight': r"assets\font\poppins\extralight.ttf",
        }
    },
    'FiraCode': {
        'normal': {
            'bold': r"assets\font\firacode\bold.ttf",
            'semibold': r"assets\font\firacode\semibold.ttf",
            'medium': r"assets\font\firacode\medium.ttf",
            'normal': r"assets\font\firacode\regular.ttf",
            'light': r"assets\font\firacode\light.ttf",
        },
        'italic': {
            'bold': r"assets\font\firacode\bold.ttf",
            'semibold': r"assets\font\firacode\semibold.ttf",
            'medium': r"assets\font\firacode\medium.ttf",
            'normal': r"assets\font\firacode\regular.ttf",
            'light': r"assets\font\firacode\light.ttf",
        }
    }
}


def getFont(font="Poppins",
            italic=False,
            weight='normal',
            fontHeight=25
            ) -> pg.font.Font:
    dir = FONTS[font][italic and "italic" or "normal"][weight]
    return pg.font.Font(dir, int(fontHeight))


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
                 borderRadius=0,
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
        super().__init__(dimension, app, color, borderRadius,
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
        self.font = getFont(font, italic, weight, fontHeight)

    def drawContent(self):
        if not self.enabled:
            return False
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
