import pygame as pg
from uuid import uuid4
from classes.components.Area import *
from typing import List, Optional


class Tab(Area):

    color: pg.Color
    b0: 0
    b1: 0
    b2: 0
    b3: 0

    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
        color: str = "#ffffff",
        borderValue=0,
    ) -> None:
        super().__init__(dimension, app)
        self.b0 = borderValue
        self.b1 = borderValue
        self.b2 = borderValue
        self.b3 = borderValue
        self.color = color

    def update(self):
        super().update()

    def setBorders(self, borderValue: int):
        self.b0 = borderValue
        self.b1 = borderValue
        self.b2 = borderValue
        self.b3 = borderValue

    def draw(self):
               
        pg.draw.rect(
            self.app.screen,
            self.color,
            pg.Rect(self.x, self.y, self.w, self.h),
            0,
            -1,
            self.b0,
            self.b1,
            self.b2,
            self.b3,
        )
        super().draw()
