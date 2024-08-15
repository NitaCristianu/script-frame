import pygame as pg

class Main():
    def __init__(self) -> None:
        pass

    def render(self, t : float, surf : pg.Surface) -> None:
        pg.draw.circle(surf, "red", (20 * t, 20), 800)
        return surf
