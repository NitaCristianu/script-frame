from typing import List
from uuid import uuid4
from typing import List, Literal
from utils.audio import *
from config.consts import *
from config.errorobj import *
from pydub import AudioSegment
from math import ceil
import os 
import wave

def get_modification_time(file_path):
    return os.path.getmtime(file_path)

class Prop:
    name: str
    value: any
    propType: str

    def __init__(self, name: str, value: any, propType: str) -> None:
        self.name = name
        self.value = value
        self.propType = propType


class Element:

    source: str
    name: str
    icon: str
    instance: any
    color: pg.Color
    start: float
    end: float
    layer: int
    x: int
    y: int
    selected: bool
    id: str
    type: str
    lastmodified: float
    enabled : bool

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
        self.volumemul = 1
        self.lastmodified = 0
        self.dragging = False
        self.calcInstance = True  # determines if the isntance will be calculated
        self.enabled = False

        for key, val in args.items():
            if hasattr(self, key):
                setattr(self, key, val)
        if len(self.source) == 0:
            self.source = self.name
        self.color = "#364799" if self.type == "video" else "#7c1d77"

        if self.icon == "customicon.png" and self.type == "audio":
            self.icon = "musicnote.png"

        if len(self.source) > 0 and self.calcInstance:
            self.setInstance()

    def getfilename(self):
        return os.path.basename(self.getfullsource())

    def getfullsource(self):
        if self.source.startswith(AUDIO_DIRECTORY) or self.source.startswith(COMPONENTS_DIRECTORY): return self.source
        
        if self.type == 'audio':
            return f'{AUDIO_DIRECTORY}\\{self.source}'
        else:
            return  f'{COMPONENTS_DIRECTORY}\\{self.source}'

    def splitaudio(self, t: float):
        start = self.start
        end = self.end
        
        # cut times seconds
        diststart = t - start
        distend = end - t

        audio: AudioSegment = AudioSegment.from_wav(self.getfullsource())

        cut1 = audio[int(diststart*1000):]
        cut2 = audio[:ceil(-distend*1000)]
        dir1 = f"{AUDIO_DIRECTORY}\\r__{self.getfilename()}"
        dir2 = f"{AUDIO_DIRECTORY}\\l__{self.getfilename()}"

        cut1.export(dir1, format="wav")
        cut2.export(dir2, format="wav")

        element1 = Element(name=self.name, source=dir1, type="audio", start = diststart + self.start, volumemul = self.volumemul)
        element2 = Element(name=self.name, source=dir2, type="audio", start = self.start, volumemul = self.volumemul)
        elements.append(element1)
        elements.append(element2)

        elements.remove(self)
        del self

    def setInstance(self):
        if self.type == "audio":
            
            self.instance: wave.Wave_read | wave.Wave_write = wave.open(
                self.getfullsource(), "rb")
            self.pygamesound: pg.mixer.Sound = pg.mixer.Sound(
                self.getfullsource())

            self.freq = self.instance.getframerate()
            self.samplewidth = self.instance.getsampwidth()
            self.nchannels = self.instance.getnchannels() 
            self.nframes = self.instance.getnframes()

            self.sound_array = np.frombuffer(
                self.instance.readframes(-1), dtype=np.int16)
            self.lenght = self.nframes / self.freq

            self.data, self.framerate = read_wav(self.getfullsource())

            self.end = self.start + self.lenght
        elif self.type == "video":
            import importlib.util
            import sys
            from pathlib import Path

            try:
                file_path = Path(self.getfullsource())
                module_name = self.source
                spec = importlib.util.spec_from_file_location(
                    module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                Class = getattr(module, 'Main')
                self.instance = Class()
            except Exception as e:
                self.instance = Main()
                self.instance.errormessage = str(e)
                print(e)

    def update(self):
        new_modified_time = get_modification_time(self.getfullsource())
        if self.lastmodified != new_modified_time:
            self.lastmodified = get_modification_time(self.getfullsource())
            self.setInstance()

pg.mixer.init()
elements: List["Element"] = []
