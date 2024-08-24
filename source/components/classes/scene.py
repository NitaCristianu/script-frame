import pygame as pg
from components.classes.node import *
from components.utils.signal import *
from config.projectData import *

class Scene:

    def __init__(self) -> None:
        self.father = Node(self)
        self.surf = self.getSurface()
        self.props: List['Prop'] = []
        self.reqtime = 0
        self.t = 0
        self.lenght = 0
    
    def getProperty(self, signal : Signal) -> None:
        prop = next((prop for prop in self.props if prop['name'] == signal.name), None)
        return prop['value'] if prop else signal._value

    def setProperty(self, signal: Signal, propType : str, **kargs):
        name = signal.name
        found = False
        for prop in self.props:
            if prop['name'] == name:
                found = True
                break
        if not found:
            self.props.append({'name' : name, 'value' : signal(), 'propType' : propType, **kargs})

    @property
    def add(self):
        return self.father.add

    @property
    def children(self):
        return self.father.children

    @property
    def size(self):
        """
        returns the size in which every child fits
        """
        w, h = 0,0
        
        for child in self.children:
            w = max(child.x() + child.w(), w)
            h = max(child.y() + child.h(), h)

        return w,h

    def wait(self, time : float):
        self.reqtime += time

    def getSurface(self):
        return pg.Surface(self.size, pg.SRCALPHA, 32)

    def centerFather(self):
        w,h = self.surf.get_size()
        self.father.x(w//2)
        self.father.y(h//2)

    def render_start(self, t : int):
        self.t = t
        self.reqtime = 0
        self.surf = pg.Surface(self.size, pg.SRCALPHA, 32)
        self.father.reset()
        self.centerFather()
        self.render()

    def render(self):
        pass
    
    def render_end(self):
        self.father.render()
        self.lenght = self.reqtime
        return self.surf
        