from components.classes.shape import *
from utils.shapes import *
from math import ceil

class Rectangle(Shape):
    def __init__(self, **args) -> None:
        self.color = (255, 255, 255, 0)
        self.w = 0
        self.h = 0
        self.borderRadius = 0
        super().__init__(**args)

    def surf(self):
        surf =  super().surf()
        
        AAfilledRoundedRect(
            surf,
            pg.Rect(
                ceil(self.x),
                ceil(self.y),
                ceil(self.w),
                ceil(self.h),
            ),
            self.color,
            self.borderRadius
        )
        return surf