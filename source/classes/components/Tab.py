import pygame as pg
from uuid import uuid4
from classes.components.Area import *
from typing import Any, List, Optional
from utils.colors import hex_to_rgb


class Tab(Area):

    color: pg.Color
    b0: int
    b1: int
    b2: int
    b3: int

    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
        color: str | tuple[int, int, int, int] = "#ffffff",
        borderValue=0,
    ) -> None:
        super().__init__(dimension, app)
        self.b0 = borderValue
        self.b1 = borderValue
        self.b2 = borderValue
        self.b3 = borderValue
        self.color = color
        self.parsedColor = hex_to_rgb(color)

    def __setattr__(self, name: str, value: Any) -> None:
        if (name == "color"):
            self.parsedColor = hex_to_rgb(value)
        return super().__setattr__(name, value)

    def update(self):
        super().update()

    def setBorders(self, borderValue: int):
        self.b0 = borderValue
        self.b1 = borderValue
        self.b2 = borderValue
        self.b3 = borderValue

    def drawContent(self):
        super().drawContent()
        if (self.color == "#00000000"): return
        surface = pg.Surface((self.w, self.h), pg.SRCALPHA)
        pg.draw.rect(
            surface,
            self.parsedColor,
            pg.Rect(0, 0, self.w, self.h),
            0,
            -1,
            self.b0,
            self.b1,
            self.b2,
            self.b3,
        )
        self.app.screen.blit(surface, (self.x, self.y))
