import pygame as pg
from components.classes.node import *
from components.utils.signal import *
from config.consts import *
from config.projectData import *

class Scene:

    def __init__(self) -> None:
        self.w = self.h = 0
        self.father = Node(self, x = lambda : self.w//2, y = lambda : self.h //2)
        self.surf = self.getSurface()
        self.props: List['Prop'] = []
        self.reqtime = 0
        self.sounds = []
        self.t = 0
        self.lenght = 0
        self.start()
    
    def start(self)->None:
        pass

    def playAudio(self, src: str, **args) -> None:
        sound = pg.mixer.Sound(AUDIO_DIRECTORY + "\\" + src)
        self.sounds.append((sound, self.reqtime))


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
            w = max(child.rect.right, w)
            h = max(child.rect.bottom, h)

        return w,h

    def wait(self, time : float):
        self.reqtime += time

    def getSurface(self):
        return pg.Surface(self.size, pg.SRCALPHA, 32)

    def render_start(self, t : int, videosize : tuple[int, int]):
        self.t = t
        self.reqtime = 0
        self.surf = pg.Surface(self.size, pg.SRCALPHA, 32)
        self.father.reset()
        self.sounds.clear()
        self.w, self.h = videosize

        self.render()

    def render(self):
        pass
    
    def render_end(self):
        self.father.render()
        self.lenght = self.reqtime
        return self.surf
        