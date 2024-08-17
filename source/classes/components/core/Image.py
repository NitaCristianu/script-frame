from typing import Any
from utils.colors import *
from classes.components.core.Rect import *
import pygame as pg


class Image(Rect):
    def __init__(self,
                 dimension: tuple[int, int, int, int],
                 app: any,
                 color: str | tuple[int, int, int, int] = "#00000000",
                 borderRadius=0,
                 detectHover=False,
                 onHoverModifiedColor=0.3,
                 pngSource="",
                 forceWidth=False,
                 forceHeight=False,
                 centerImage=False,
                 scale=(1, 1)
                 ) -> None:
        super().__init__(
            dimension,
            app,
            color,
            borderRadius,
            detectHover,
            onHoverModifiedColor,
        )
        self.centerImage = centerImage
        self.scale = scale
        self.forceWidth = forceWidth
        self.forceHeight = forceHeight
        self.pngSource = pngSource
        self.parsedSVGcolor = (0, 0, 0, 0)
        self.image = self.getImage()
        self.width = 0  # the actual width
        self.height = 0  # the actual height

    def getImage(self):
        self.computeDimension()
        if self.pngSource == "":
            return pg.Surface((0, 0))
        self.width = self.w
        self.height = self.h
        if self.forceWidth == self.forceHeight:
            return pg.transform.scale(
                pg.image.load("assets\\images\\" +
                              self.pngSource).convert_alpha(),
                (self.w * self.scale[0], self.h * self.scale[1])
            )
        if self.forceWidth:
            image = pg.image.load("assets\\images\\" +
                                  self.pngSource).convert_alpha()
            original_width, original_height = image.get_size()
            self.height = max(
                int(self.w * (original_height / original_width)), 0)
            self.width = max(0, self.w)
            return pg.transform.scale(
                image,
                (self.width * self.scale[0], self.height * self.scale[1])
            )
        if self.forceHeight:
            image = pg.image.load("assets\\images\\" +
                                  self.pngSource).convert_alpha()
            original_width, original_height = image.get_size()
            self.width = max(
                int(self.h * (original_width / original_height)), 0)
            self.height = max(self.h, 0)
            return pg.transform.scale(
                image,
                (self.width*self.scale[0], self.height*self.scale[1])
            )

    def update(self):
        if not self.enabled: return False
        if self.app.resize:
            self.image = self.getImage()
        return super().update()

    def drawContent(self):
        if not self.enabled: return False
        super().drawContent()
        borderRadius = self.borderRadius
        isCentered = self.centerImage
        if borderRadius > 0:
            cornered_surface = pg.Surface(
                (self.width, self.height), pg.SRCALPHA)

            pg.draw.rect(cornered_surface, (255, 255, 255, 255), pg.Rect(
                0, 0, self.width, self.height), 0, borderRadius)
            image_rect = self.image.get_rect(
                center=(self.x + self.w//2, self.y + self.h//2))
            if self.centerImage:
                cornered_surface.blit(
                    self.image, image_rect.topleft, special_flags=pg.BLEND_RGB_MULT)
            else:
                cornered_surface.blit(self.image, (0, 0),
                                      special_flags=pg.BLEND_RGB_MULT)
            self.app.screen.blit(cornered_surface, (self.x, self.y))
        else:
            if self.centerImage:
                image_rect = self.image.get_rect(
                    center=(self.x + self.w//2, self.y + self.h//2))
                self.app.screen.blit(self.image, image_rect.topleft)
            else:
                self.app.screen.blit(self.image, (self.x, self.y))
