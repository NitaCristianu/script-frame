import pygame as pg
from uuid import uuid4
from classes.components.core.Area import *
from utils.shapes import *
from typing import Any, List, Optional
from utils.colors import hex_to_rgb, modifyRGB


class Rect(Area):

    color: pg.Color
    borderRadius: float # >= 0 and <= 1   

    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
        color: str | tuple[int, int, int, int] = "#ffffff",
        borderRadius=0,
        detectHover = False,
        onHoverModifiedColor = 0.15,
        
    ) -> None:
        super().__init__(dimension, app, detectHover=detectHover)
        self.borderRadius = borderRadius
        self.onHoverModifiedColor = onHoverModifiedColor
        self.color = color
        self.parsedColor = hex_to_rgb(color)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "color":
            self.parsedColor = hex_to_rgb(value)
        return super().__setattr__(name, value)

    def update(self):
        if not self.enabled: return False
        super().update()
        if self.detectHover and self.onHoverModifiedColor != 0:
            if self.onhoverStart or self.onHoverEnd or self.mup or self.mdown:
                self.draw()
                self.app.refresh(self.rect)

    def drawContent(self):
        if not self.enabled: return False
        super().drawContent()
        x,y,w,h = max(self.x, 0), max(self.y, 0), max(self.w, 0), max(self.h, 0)
        surface = pg.Surface((w, h), pg.SRCALPHA)

        color = self.parsedColor
        if self.hovered:
            color = modifyRGB(color, self.onHoverModifiedColor)
        if self.mdown:
            color = modifyRGB(color, self.onHoverModifiedColor*1.2)
        

        AAfilledRoundedRect(
            surface,
            pg.Rect(0,0,w,h),
            color,
            self.borderRadius
        )
        self.app.screen.blit(surface, (x, y))
