from typing import List
import pygame as pg
from uuid import uuid4
from typing import TypedDict, Union, List

class Prop:
    name : str
    value : any
    propType : str


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
 
    def __init__(self, name: str, icon = "customicon.png", source = None, startend = (0, 1), layer = 0) -> None:
        if source == None: source = name
        self.name = name
        self.icon = icon
        self.source = source
        self.instance = self.getClassInstance()
        self.x = self.y = 0
        self.start = startend[0]
        self.layer = layer
        self.end = startend[1]
        self.color = "#cdced3"
        self.selected = False
        self.id = uuid4().hex

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
    Element("circle", startend=(0, 2), layer = 0),
    Element("rect", startend=(0, 3), layer = 1),
]