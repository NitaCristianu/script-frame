import pygame as pg
from config.consts import INITIAL_WIDTH, INITIAL_HEIGHT

class App():
    
    screen : pg.Surface
    width = INITIAL_WIDTH
    height = INITIAL_HEIGHT

    def __init__(self, screen : pg.Surface) -> None:
        self.screen = screen

    def processEvent(self, event: pg.event.Event) -> None:
        pass
    
    def update(self) -> None:
        pass
    
    def draw(self) -> None:
        pass