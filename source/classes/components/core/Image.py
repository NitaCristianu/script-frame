from typing import Any
from utils.colors import *
from classes.components.core.Rect import *
import pygame as pg


class Image(Rect):
    def __init__(self,
                 dimension: tuple[int, int, int, int],
                 app: any,
                 color: str | tuple[int, int, int, int] = "#00000000",
                 borderValue=0,
                 detectHover=False,
                 onHoverModifiedColor=0.3,
                 pngSource="",
                 forceWidth=False,
                 forceHeight=False,
                 ) -> None:
        super().__init__(
            dimension,
            app,
            color,
            borderValue,
            detectHover,
            onHoverModifiedColor
        )
        self.forceWidth = forceWidth
        self.forceHeight = forceHeight
        self.pngSource = pngSource
        self.parsedSVGcolor = (0, 0, 0, 0)
        self.image = self.getImage()
        self.width = 0 # the actual width
        self.height = 0 # the actual height

    def getImage(self):
        self.computeDimension()
        if self.pngSource == "":
            return pg.Surface((0, 0))
        if self.forceWidth == self.forceHeight:
            return pg.transform.scale(
                pg.image.load("assets\\images\\" +
                              self.pngSource).convert_alpha(),
                (self.w, self.h)
            )
        if self.forceWidth:
            image = pg.image.load("assets\\images\\" +
                                  self.pngSource).convert_alpha()
            original_width, original_height = image.get_size()
            self.height = max(int(self.w * (original_height / original_width)), 0)
            self.width = max(0, self.w)
            return pg.transform.scale(
                image,
                (self.width, self.height)
            )
        if self.forceHeight:
            image = pg.image.load("assets\\images\\" +
                                  self.pngSource).convert_alpha()
            original_width, original_height = image.get_size()
            self.width = max(int(self.h * (original_width / original_height)), 0)
            self.height = max(self.h, 0)
            return pg.transform.scale(
                image,
                (self.width, self.height)
            )

    def update(self):
        if self.app.resize:
            self.image = self.getImage()
        return super().update()

    def drawContent(self):
        super().drawContent()
        self.app.screen.blit(self.image, (self.x, self.y))
