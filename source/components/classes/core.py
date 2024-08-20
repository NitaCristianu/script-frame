from typing import Any, Dict
from components.classes.shape import *
import pygame as pg

class Core:
    def __init__(self) -> None:
        self.start()

    def start(self) -> None:
        self._totallenght = 0
        self._reqtime = 0
        self._last_cliplenght = 0
        self.props = []
        self._surf = pg.Surface((0,0))
        self._elements : Dict[str, 'Shape'] = {}
        self._t = 0

    @property
    def lenght(self): return self._reqtime

    def get(self, objectName) -> Shape: return self._elements[objectName]

    def wait(self, time : float) -> None:
        self._reqtime += time

    def play(self, callback, totalTime = 1, **args) -> None:
        if self._t >= self._reqtime and self._t <= self._reqtime + totalTime:
            callback(totalTime = totalTime, t = self._t, **args)
        # if self._t < self._reqtime:
        #     callback(totalTime = totalTime, t = 1, **args)

    def add(self, name: str, value: Any) -> None:
        if not hasattr(self._elements, name) and self._t >= self._reqtime:
            value.master = self
            self._elements[name] = value
            return
        return super().__setattr__(name, value)

    def render(self, t : float, surf: pg.Surface):
        self._reqtime = 0
        self._t = t
        self._surf = surf

        for element in self._elements.values():
            if element.enabled: element.render()
    