from typing import Any
from components.classes.core import *
from components.utils.easing import *
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

    def _transform_number(self, keys, time):
        return keys[0][0] + (keys[1][0] - keys[0][0]) * time

    def _transform_tuple(self, keys, time):
        a = isinstance(keys[0][0], pg.Color) and keys[0][0] or (isinstance(keys[0][0], tuple) and pg.Color(*keys[0][0]) or pg.Color(keys[0][0]))
        b = isinstance(keys[0][1], pg.Color) and keys[0][1] or (isinstance(keys[1][0], tuple) and pg.Color(*keys[1][0]) or pg.Color(keys[1][0]))
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

                time = keys[1][1](invLerp(times[0], times[1], t))
                if isinstance(value, (int, float)):
                    result = self._transform_number(keys, time)
                if isinstance(value, pg.Color) or isinstance(value, tuple) and all(isinstance(i, (int, float)) for i in value) or isinstance(value, str):
                    result = self._transform_tuple(keys, time)
                setattr(self, name, result)
                    
            
        return totalTime

    def remove(self):
        self.enabled = False