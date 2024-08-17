from typing import List
import pygame as pg

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
 
    def __init__(self, name: str, icon = "customicon.png", source = "circle") -> None:
        self.name = name
        self.icon = icon
        self.source = source
        self.instance = self.getClassInstance()
        self.x = self.y = 0
        self.start = 2
        self.layer = 0
        self.end = 4
        self.color = "#cdced3"
        self.selected = False

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
    Element("circle")
]