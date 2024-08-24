from typing import List
import pygame as pg
from uuid import uuid4
from typing import TypedDict, Union, List

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
        self.color = "#364799"
        self.x = self.y = 0
        self.id = uuid4().hex
        self.type = "video"
        self.selected = False
        self.dragging = False

        for key, val in args.items():
            if hasattr(self, key): setattr(self, key, val)
        if len(self.source) == 0: self.source = self.name

        if self.type == "video" and len(self.source) > 0 :
            self.instance = self.getClassInstance()
        else:
            self.instance = None

    def getClassInstance(self):
        import importlib.util
        import sys
        from pathlib import Path

        file_path = Path(f'source\\components\\{self.source}.py')
        module_name = self.source
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        Class = getattr(module, 'Main')

        return Class()

elements: List["Element"] = [
    Element("testobj"),
    Element("testobj", layer = 1),
]