from components.classes.shape import *

class Rect(Shape):
    def __init__(self, **args) -> None:
        super().__init__(**args)

    def surf(self):
        surf =  super().surf()
        pg.draw.rect(
            surf,
            self.color or (255, 255, 255, 0),
            pg.Rect(self.x or 0, self.y or 0, self.w or 0, self.h or 0)
        )
        return surf