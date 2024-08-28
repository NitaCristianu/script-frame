from typing import List
import pygame as pg
from uuid import uuid4
from typing import List, Literal
from utils.audio import *
from config.consts import *
import wave

class Prop:
    name : str
    value : any
    propType : str

    def __init__(self, name: str, value: any, propType: str) -> None:
        self.name = name
        self.value = value
        self.propType = propType


class Element:

    source : str
    name : str
    icon : str
    instance : any
    color : pg.Color
    start : float
    end : float
    layer : int
    x: int
    y: int
    selected : bool
    id : str
    type : str
 
    def __init__(self, name: str, **args) -> None:
        self.name = name
        self.source = ""
        self.icon = "customicon.png"
        self.layer = 0
        self.start = self.end = 0
        self.x = self.y = 0
        self.id = uuid4().hex
        self.type: Literal['video', 'audio'] = 'video'
        self.selected = False
        self.dragging = False

        for key, val in args.items():
            if hasattr(self, key): setattr(self, key, val)
        if len(self.source) == 0: self.source = self.name
        self.color = "#364799" if self.type == "video" else "#7c1d77"

        if len(self.source) > 0:
            self.instance = self.getInstance()
        
        if self.type == 'audio':
            self.volumemul = 1

    def getFullSource(self):
        if self.type == 'audio':
            return COMPONENTS_DIRECTORY + f'\\audio\\{self.source}'
        else:
            return COMPONENTS_DIRECTORY + f'\\{self.source}.py'


    def getInstance(self):
        if self.type == "audio":
            self.instance: wave.Wave_read = wave.open(self.getFullSource(), "rb")
            self.pygamesound: pg.mixer.Sound = pg.mixer.Sound(self.getFullSource())

            self.freq = self.instance.getframerate()
            self.nframes = self.instance.getnframes()
            self.lenght = self.nframes / self.freq
        
            self.data, self.framerate = read_wav(self.getFullSource(), downsample_factor=10)

            self.end = self.start + self.lenght
            
            self.instance.close()
            return
        import importlib.util
        import sys
        from pathlib import Path

        file_path = Path(self.getFullSource())
        module_name = self.source
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        Class = getattr(module, 'Main')

        return Class()

pg.mixer.init()
elements: List["Element"] = [
    Element("testobj", layer = 1),
    Element("test.wav", type = "audio")
]