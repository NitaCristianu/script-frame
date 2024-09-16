from typing import Any, List, Optional
from components.utils.easing import *
from components.utils.signal import *
from utils.math import *

class Node:
    def __init__(self, master, **args) -> None:
        
        self.children : List['Node'] = []
        self.parent : Optional['Node'] = None
        self.master = master

        self.attributes = {
            'x' : 0,
            'y' : 0,
            'w' : 0,
            'h' : 0,
            'centered' : True,
            'opacity' : 1
        } | args

        for key, value in self.attributes.items():
            setattr(self, key, Signal(value, master))
        
    def getabs_xy(self):
        x = 0
        y = 0
        parent = self.parent
        while (parent):
            x += parent.x.getrelative(self.master.w)
            y += parent.y.getrelative(self.master.h)
            parent = parent.parent
        return x,y
    
    def getabs_wh(self):
        return self.w.getrelative(self.master.w), self.h.getrelative(self.master.h)
    
    def getabs_coords(self):
        return self.getabs_xy(), self.getabs_wh()

    def get_opacity(self):
        opacity = self.opacity.getrelative(1) * 255
        parent = self.parent
        while parent:
            opacity *= self.parent.opacity.getrelative(1) * 255
            parent = parent.parent
        
        return round(opacity)

    @property
    def rect(self):
        r = pg.Rect(0, 0, *self.getabs_wh())
        if self.centered():
            r.center = self.getabs_xy()
        else:
            r.topleft = self.getabs_xy()
        return r

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
        if self.get_opacity() < 0.0001: return
        for child in self.children:
            child.render()