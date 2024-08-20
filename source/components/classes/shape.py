from typing import Any
from components.classes.core import *
from components.utils.easing import *
from utils.colors import *
from utils.math import *
import pygame as pg

class Shape:
    
    def __init__(self, **args) -> None:
        self.enabled = True
        self.keyframes = {}

        self.x = self.y = 0
        self.start = 0
        for key, value in args.items():
            self.add_keyframe(0, key, value)
            setattr(self, key, value)
    
    def add_keyframe(self, t: float, name: str, val:str, ease = inoutcubic):
        t = str(float(t))
        if t not in self.keyframes:
            self.keyframes[t] = {}
            self.keyframes[t][name] = (val, ease)
        else:
            self.keyframes[t][name] = (val, ease)

    def get_keyframes(self, name: str, t : float):
        keyframe_times = list(float(x) for x in self.keyframes.keys())
        a_time = str(max((num for num in keyframe_times if name in self.keyframes[str(num)] and num < t), default=0))
        b_time = str(min((num for num in keyframe_times if name in self.keyframes[str(num)] and num >= t), default=a_time))
        a = self.keyframes[a_time][name]
        b = self.keyframes[b_time][name]
        
        return {a_time : a, b_time : b}

    def surf(self) -> pg.Surface :
        return self.master._surf.copy() 
    
    def render(self):
        master = self.master
        w,h = master._surf.get_size()
        x = self.x + w / 2
        y = self.y + h / 2
        master._surf.blit(self.surf(), (x, y))

    def _transform_text(self, a, b, time):
        # Determine the length of the result string
        max_len = max(len(a), len(b))
        
        # Pad the shorter strings with spaces
        a = a.ljust(max_len)
        b = b.ljust(max_len)
        
        # Create the blended string
        blended = []
        for i in range(max_len):
            if time < i / max_len:
                blended.append(a[i])
            else:
                blended.append(b[i])
        
        return ''.join(blended)

    def _transform_number(self, a, b, time):
        return a + (b - a) * time

    def _transform_tuple(self, a, b, time):
        a = isinstance(a, pg.Color) and a or (isinstance(a, tuple) and pg.Color(*a) or pg.Color(a))
        b = isinstance(b, pg.Color) and b or (isinstance(b, tuple) and pg.Color(*b) or pg.Color(b))
        return a.lerp(b, time)
        

    def transform(self, name: str, value: any, totalTime : float = 1, ease = inoutcubic, t : float = 0) -> float:
        """
        Creates a transition if played
        takes name and value
        optionals : totalTime, ease
        return the total time it takes for the animation to finish
        """
        
        properties = isinstance(name, tuple) and [*name] or [name]
        for name in properties:
            if hasattr(self, name):
                if t == 0:
                    setattr(self, name, self.keyframes['0.0'][name][0])
                    return
                self.add_keyframe(self.master._reqtime + totalTime, name, value, ease)

                
                data = self.get_keyframes(name, t)
                times = tuple(float(t) for t in list(data.keys()))
                keys = tuple(data.values())
                ab = (keys[0][0], keys[1][0])
                time = keys[1][1](invLerp(times[0], times[1], t))
                if isinstance(value, (int, float)):
                    result = self._transform_number(*ab, time)
                elif isinstance(value, pg.Color) or isinstance(value, tuple) and all(isinstance(i, (int, float)) for i in value) or isStringAColor(value):
                    result = self._transform_tuple(*ab, time)
                elif isinstance(value, str):
                    result = self._transform_text(*ab, time)
                setattr(self, name, result)
                    
            
        return totalTime

    def remove(self):
        self.enabled = False