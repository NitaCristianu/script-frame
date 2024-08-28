import copy
import moviepy.editor
from typing import List
import pygame
from uuid import uuid4
from typing import List, Literal
from utils.audio import *
from config.consts import *
import wave
from io import BytesIO


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
        self.dragging = False
        self.calcInstance = True  # determines if the isntance will be calculated

        for key, val in args.items():
            if hasattr(self, key):
                setattr(self, key, val)
        if len(self.source) == 0:
            self.source = self.name
        self.color = "#364799" if self.type == "video" else "#7c1d77"

        if len(self.source) > 0 and self.calcInstance:
            self.setInstance()

    def getFullSource(self):
        if self.type == 'audio':
            return COMPONENTS_DIRECTORY + f'\\audio\\{self.source}'
        else:
            return COMPONENTS_DIRECTORY + f'\\{self.source}.py'

    def splitaudio(self, t: float):
        if self.calcInstance:
            # this is original audio
            self.instance = wave.open(self.getFullSource(), "rb")
            self.sound_array = np.frombuffer(self.instance.readframes(-1), dtype=np.int16)
            self.framerate = self.instance.getframerate()
            self.nchannels = self.instance.getnchannels()
            self.samplewidth = self.instance.getsampwidth()
        if isinstance(self.sound_array, BytesIO): return
        print(self.sound_array)
        (wav1, wav1_data), (wav2, wav2_data) = splitaudio(self.sound_array, self.framerate, self.nchannels, self.samplewidth, t)
        print("Split 1 duration :", wav1.getnframes() / wav1.getframerate())
        print("Split 2 duration :", wav2.getnframes() / wav2.getframerate())
        original_end = self.lenght
        self.calcSoundProps(wav1, wav1_data)

        element2 = Element(name=self.name,
                           source=self.source,
                           icon=self.icon,
                           layer=self.layer,
                           start=self.end,
                           end=original_end,
                           type='audio',
                           selected=True,
                           volumemul=self.volumemul,
                           calcInstance=False
                           )
        
        element2.calcSoundProps(wav2, wav2_data)
        elements.append(element2)

    def calcSoundProps(self, wave_file, wave_data):
        self.instance = wave_file
        self.pygamesound = pg.mixer.Sound(wave_data)

        self.freq = self.instance.getframerate()
        self.samplewidth = self.instance.getsampwidth()
        self.sound_array = wave_data
        self.nchannels = self.instance.getnchannels()
        self.nframes = self.instance.getnframes()
        self.lenght = self.nframes / self.freq

        self.data, self.framerate = read_wav(
            self.getFullSource(), downsample_factor=10)

        self.end = self.start + self.lenght

    def setInstance(self):
        if self.type == "audio":
            self.instance: wave.Wave_read | wave.Wave_write = wave.open(
                self.getFullSource(), "rb")
            self.pygamesound: pg.mixer.Sound = pg.mixer.Sound(
                self.getFullSource())

            self.freq = self.instance.getframerate()
            self.samplewidth = self.instance.getsampwidth()
            self.nchannels = self.instance.getnchannels()
            self.nframes = self.instance.getnframes()

            self.sound_array = np.frombuffer(self.instance.readframes(-1), dtype=np.int16)
            self.lenght = self.nframes / self.freq

            self.data, self.framerate = read_wav(
                self.getFullSource(), downsample_factor=10)

            self.end = self.start + self.lenght
        elif self.type == "video":
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

            self.instance = Class()


pg.mixer.init()
elements: List["Element"] = [
    Element("testobj", layer=1),
    Element("test.wav", type="audio")
]
