from components.classes.shape import *
from utils.shapes import *

class Rect(Shape):
    def __init__(self, **args) -> None:
        self.color = (255, 255, 255, 0)
        self.w = 0
        self.h = 0
        self.borderRadius = 32
        super().__init__(**args)

    def surf(self):
        surf =  super().surf()
        
        AAfilledRoundedRect(
            surf,
            pg.Rect(self.x, self.y, self.w, self.h),
            self.color,
            self.borderRadius
        )
        return surf