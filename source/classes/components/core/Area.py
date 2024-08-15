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
    isHoveredCurrently: bool
    relative: bool
    detectHover: bool
    

    def __init__(
        self,
        dimension: dimension_type = (0, 0, 0, 0),
        app: any = None,  # this is App type, but can't write specifically due to circlular import
        detectHover=False
    ) -> None:
        # Give unique id and accces to the main screen
        self.id = str(uuid4())

        self.app = app
        self.x = self.y = self.w = self.h = 0
        self.mpos = 0
        self.relative = self.hovered = self.oldhovered = self.detectHover = False
        self.children = []
        self.detectHover = detectHover
        self.enabled = True
        self.parent = None

        self.computeDimension(dimension)

    @property
    def isHoveredCurrently(self):
        (x, y) = self.app.mpos
        return inRect(x, y, self.x, self.y, self.w, self.h)

    @property
    def clicked(self):
        if self.isHoveredCurrently and self.app.mup:
            # self.app.draw()
            return True
        return False

    @property
    def rect(self):
        return pg.Rect(self.x, self.y, self.w, self.h)

    @property
    def mup(self):
        if self.isHoveredCurrently and not self.app.mbuttons[0] and self.app.oldmbuttons[0]:
            return True
        return False

    @property
    def mdown(self):
        if self.isHoveredCurrently and self.app.mbuttons[0] and not self.app.oldmbuttons[0]:
            return True
        return False

    @property
    def onhoverStart(self):
        if not self.detectHover:
            print(f"onHoverStart can't be used if area's detectHover is false\nArea ID : {
                  self.id}")
        return self.hovered and not self.oldhovered and self.detectHover

    @property
    def onHoverEnd(self):
        if not self.detectHover:
            print(f"onHoverEnd can't be used if area's detectHover is false\nArea ID : {
                  self.id}")
        return not self.hovered and self.oldhovered and self.detectHover

    @property
    def isEnabled(self):
        if not self.enabled: return False
        el = self.parent
        if not el.enabled: return False
        while el.parent != None:
            el = el.parent
            if not el.enabled: return False
        return True
            

        

    def clearChildren(self):
        self.children.clear()

    def isRelative(self):
        return any(isinstance(item, str) for item in self.dimension)

    def computeDimension(self, dimension: Optional[dimension_type] = None):
        # if the dimension is a string, then it must be relative to the screen
        if dimension:
            self.dimension = dimension
        dimension = self.dimension

        if self.app:
            self.x = self.app.relative(str(dimension[0]), 0, self)
            self.y = self.app.relative(str(dimension[1]), 1, self)
            self.w = self.app.relative(str(dimension[2]), 2, self)
            self.h = self.app.relative(str(dimension[3]), 3, self)
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
        if not self.enabled: return False
        if self.relative:
            self.computeDimension()

        for child in self.children:
            child.update()

        if self.detectHover:
            self.oldhovered = self.hovered
            self.hovered = self.isHoveredCurrently

    def drawContent(self):
        """
        draws only the content whithout children
        """
        pass

    def draw(self):
        if not self.enabled: return False
        self.drawContent()
        for child in self.children:
            child.draw()
