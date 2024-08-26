from typing import Any, List, Optional, Union
from components.utils.easing import *
from components.utils.signal import *
from utils.math import *
import pygame as pg

class Node:
    def __init__(self, master, **args) -> None:
        
        self.children : List['Node'] = []
        self.parent : Optional['Node'] = None
        self.master = master

        self.attributes = {
            'x' : 0,
            'y' : 0,
            'w' : 0,
            'h' : 0
        } | args

        for key, value in self.attributes.items():
            setattr(self, key, Signal(value, master))
        
    def reset(self):
        for key in self.attributes.keys():
            signal = getattr(self, key)
            if not isinstance(signal, Signal): continue
            signal.reset()
        for child in self.children:
            child.reset()
        
    def add(self, *nodes : tuple['Node']):
        for node in nodes:
            node.parent = self
            self.children.append(node)
        return node

    def render(self) -> None:
        for child in self.children:
            child.render()