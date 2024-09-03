import inspect
import pygame as pg
from typing import Any, TypeVar, Generic, Callable
from components.utils.easing import *
from utils.math import *

T = TypeVar("T")
class Signal(Generic[T]):
    
    def __init__(self, value : T | Callable[[], T], master : any) -> None:
        self._value = value
        self._lastval = value
        self.default = value
        self.master = master
        self.keyframes = {}
        self.shared = False
        self.name = ""


    def isprocentage(self, val = None):
        if val == None:
            val = self.extract(self._value)
        if isinstance(val, str) and val.endswith("%"):
            number_part = val[:-1]
            if number_part.startswith('-'):
                number_part = number_part[1:]
            if number_part.replace('.', '', 1).isdigit() and number_part.count('.') <= 1:
                return True
        return False

    def getrelative(self, mul: float, val = None):
        if val == None:
            val = self.extract(self._value)
        if self.isprocentage(val):
            return float(val[:-1]) / 100 * mul
        return val

    def share(self, signalName : str, propType: str, **kargs):
        self.shared = True
        self.name = signalName
        self.master.setProperty(self, propType, **kargs)
        return self


    def extract(self, val: T | Callable[[], T]) -> T:
        if inspect.isfunction(val) or isinstance(val, Signal): return val()
        return val

    def transform_text(self, a, b, t):
        # Determine the length of the result string
        max_len = max(len(a), len(b))
        
        # Pad the shorter strings with spaces
        a = a.ljust(max_len)
        b = b.ljust(max_len)
        
        # Create the blended string
        blended = []
        for i in range(max_len):
            if t < i / max_len:
                blended.append(a[i])
            else:
                blended.append(b[i])
        
        return ''.join(blended)

    def transform_val(self, a, b, t):
        # note:
        # you can't convert procentage to actual float at the moment
        if isinstance(a, (int, float)): 
            return lerp(a, b, t)
        elif self.isprocentage(a) and self.isprocentage(b):
            return f"{lerp(float(a[:-1]),float(b[:-1]),t)}%"
        elif isinstance(a, pg.Color) or (isinstance(a, str) and len(a) > 0 and a[0] == "#"):
            return pg.Color(a).lerp(pg.Color(b), t)
        elif isinstance(a, (str)): 
            return self.transform_text(a,b,t)

    def __call__(self, *args: Any) -> Any:
        """
        Handles different cases based on the number of arguments:

        1. **No arguments**:
         - returns the current signal value.
         - ```signal()```

        2. **One argument**:
        - Sets the signal to the provided value and returns it.
         - ```signal(newvalue)```

        3. **Two or three arguments**:
        - Transitions from the last value to the first argument's value over the duration specified by the second argument.
        - Optionally applies an easing function (third argument) during the transition. Defaults to a cubic easing function.
        - Returns the interpolated value.
        - ```signal(newvalue, time, ease)```

        Args:
            *args: Variable length argument list:
                - No arguments: Returns the current signal value.
                - One argument: Sets and returns the new signal value.
                - Two arguments: Transition with the specified duration.
                - Three arguments: Transition with the specified duration and easing function.

        Returns:
            Any: The current or updated signal value, or the interpolated value based on transition.
        """
        if self.shared:
            return self.master.getProperty(self)
        if not args:
            value = self.extract(self._value)
            return value
        elif len(args) == 1:
            return self(args[0], 0.0001, linear)
        elif len(args) > 1:
            # set keyframe using ease func
            valueB = self.extract(args[0])
            valueA = self.extract(self._lastval)
            time = args[1]
            ease = args[2] if len(args) > 2 else inoutcubic
            animstart = self.master.reqtime
            animfinish = animstart + time 
            if self.master.t > animfinish:
                self._lastval = args[0]
            elif self.master.t > animstart and self.master.t <= animfinish:
                t = invLerp(self.master.reqtime, animfinish, self.master.t)
                t = ease(t)
                self._value = self.transform_val(valueA, valueB, t)
                return self._value

    def reset(self):
        self(self.default)