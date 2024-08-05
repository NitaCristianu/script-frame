import pygame as pg
from typing import List, Optional, Union
from uuid import uuid4
from utils.math import inRect

dimension_type = tuple[
    Union[str, int], Union[str, int], Union[str, int], Union[str, int]
]


class Area:

    w: int
    h: int
    x: int
    y: int
    id: Optional[str]
    dimension: dimension_type
    app: any  # App
    children: List["Area"]
    parent: Optional["Area"]

    mpos: tuple[int, int]
    hoverable: bool
    relative: bool

    def __init__(
        self,
        dimension: dimension_type,
        app: any,  # this is App type, but can't write specifically due to circlular import
    ) -> None:
        # Give unique id and accces to the main screen
        self.id = uuid4()
        self.app = app

        self.x = self.y = self.w = self.h = 0
        self.mpos = 0
        self.relative = self.hoverable = False
        self.children = []
        self.parent = None

        self.computeDimension(dimension)

    @property
    def hovered(self):
        if not self.hoverable:
            return self.hoverable
        (x, y) = self.app.mpos
        return inRect(x, y, self.x, self.y, self.w, self.h)

    @property
    def clicked(self):
        if self.hovered and self.app.mup:
            # self.app.draw()
            return True
        return False

    def isRelative(self):
        return any(isinstance(item, str) for item in self.dimension)

    def computeDimension(self, dimension: Optional[dimension_type] = None):
        # if the dimension is a string, then it must be relative to the screen
        if dimension:
            self.dimension = dimension
        dimension = self.dimension

        if self.app:
            self.x = self.app.relative(str(dimension[0]),0, self)
            self.y = self.app.relative(str(dimension[1]),1, self)
            self.w = self.app.relative(str(dimension[2]),2, self)
            self.h = self.app.relative(str(dimension[3]),3, self)
        else:
            self.x = self.y = self.w = self.h = 0

        self.relative = self.isRelative()

    def add_child(self, child: "Area" | List["Area"]):
        if isinstance(child, list):
            self.children.extend(child)
        else:
            self.children.append(child)
        for child in self.children:
            child.parent = self

    def update(self):
        # only recalculates if self is relative
        if self.relative:
            self.computeDimension()

        # An Area is hovered if its parent is hovered
        if self.parent:
            self.hoverable = self.parent.hoverable
        else:
            # If it doesn't have any parent then the hovered is calculated
            # based on inRect and mouse position
            (x, y) = self.app.mpos
            if inRect(x, y, self.x, self.y, self.w, self.h):
                self.hoverable = True
            else:
                self.hoverable = False

        for child in self.children:
            child.update()

    def draw(self):
        for child in self.children:
            child.draw()
