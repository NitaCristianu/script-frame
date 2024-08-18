from typing import Any, List
from components.classes.shape import *
import pygame as pg

class Core:
    def __init__(self) -> None:
        self._totallenght = 0
        self._reqtime = 0
        self._last_cliplenght = 0
        self.props = []
        self._surf = pg.Surface((0,0))
        self._elements : List['Shape'] = []
        self._t = 0

    @property
    def lenght(self): return self._reqtime

    def wait(self, time : float) -> None:
        self._reqtime += time

    def play(self, callback, animLenght = 0) -> None:
        if self._t >= self._reqtime and self._t <= self._reqtime + animLenght:
            callback()

    def __setattr__(self, name: str, value: Any) -> None:
        if not hasattr(self, name) and isinstance(value, Shape):
            value.master = self
            self._elements.append(name)
            setattr(self, name, value)
        return super().__setattr__(name, value)

    def render(self, t : float):
        self._reqtime = 0
        self._t = t
        for element in self._elements:
            if element.enabled: element.render()
    