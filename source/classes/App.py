import pygame as pg
import json
from classes.components.core.Rect import *
from config.consts import INITIAL_WIDTH, INITIAL_HEIGHT
from classes.components.mains.MainEditor import *
from classes.components.mains.ElementGallery import *
from classes.components.mains.ProjectGallery.Main import *
from classes.components.mains.RenderMode import *
from typing import Callable
from utils.event import *


class App:

    #--------- app components
    display: pg.Surface
    screen: pg.Surface
    event = None

    #-------- app related
    windowMode = 3
    transformMode = False
    #                 0 - main editor
    #                 1 - element gallery
    #                 2 - render mode
    #                 3 - project gallery

    deltatime = 0  # time between 2 renders
    currentTime = 0 # total time
    resize = True
    clock = pg.time.Clock()
    width = INITIAL_WIDTH
    height = INITIAL_HEIGHT

    #----- inputs
    mbuttons = (False, False, False, False, False)
    oldmbuttons = (False, False, False, False, False)
    mpos: tuple[int, int]
    oldmpos: tuple[int, int]
    mup = False
    doubleclick = False
    dragging = False
    lastClick = 0

    #---- actions
    actions : list[
        tuple[
            Callable[[any], None],
            any
        ]
        ] = []
    action_i = -1

    #---- project related
    projectVersion = 0
    projectName = "default"

    #------ video related
    videotime = 0
    playbackspeed = 1
    videolenght = 5000 # 5000 ms
    videospeedmul = 1
    videorunning = False
    videoevents = []

    def __init__(self, screen: pg.Surface) -> None:
        self.display = screen
        self.screen = pg.Surface((INITIAL_WIDTH, INITIAL_HEIGHT), pg.SRCALPHA)
        self.keyboard = self.oldkeyboard = pg.key.get_pressed()
        self.resize = True
        self.event = EventManager()
        self.mpos = self.oldmpos = pg.mouse.get_pos()
        self.undoing = False
        self.setInput()

        self.MainEditor = MainEditor(app = self)
        self.ElementGallery = ElementGallery(app = self)
        self.ProjectGallery = ProjectGallery(app = self)
        self.RenderTab = RenderMode(app = self)
        self.setWindowMode(3, update = False)

    def addAction(self, callback, data):
        self.action_i += 1
        if self.undoing:
            self.actions.clear()
            self.action_i = 0
        self.actions.append((callback, data))

    def undoAction(self):
        if self.action_i == -1: return
        try:
            self.actions[self.action_i][0](*self.actions[self.action_i][1])
        except Exception as e:
            print(e)           
        self.action_i -= 1
        self.undoing = True
        self.draw()
        self.refresh()

    def setInput(self):
        self.doubleclick = False
        self.mup = self.oldmbuttons[0] and not self.mbuttons[0]
        self.oldkeyboard = self.keyboard
        self.keyboard = pg.key.get_pressed()
        self.oldmpos = self.mpos
        self.mpos = pg.mouse.get_pos()
        self.oldmbuttons = self.mbuttons
        self.mbuttons = pg.mouse.get_pressed()
        
        self.holdingShift = self.keyboard[pg.K_LSHIFT] or self.keyboard[pg.K_RIGHT]
        self.holdingCtrl = self.keyboard[pg.K_LCTRL] or self.keyboard[pg.K_LCTRL]

        if self.mup:
            if self.currentTime - self.lastClick <= 400:
                self.doubleclick = True
            self.lastClick = self.currentTime

    def getvideolenght(self):
        return int(max(tuple(el.end for el in elements)) * 1000)
        

    def loadproject(self, projectName : str, version: int):
        if version == -1:
            self.projectName = projectName
            self.projectVersion = version
            elements.clear()
            return
        versionjson = Path(f"versions\\{projectName}\\v{version}.json")
        with open(versionjson, 'r') as file:
            data = json.load(file)
            self.projectName = projectName
            self.projectVersion = version
            elements.clear()
            for el in data['elements']:
                name = el['name']
                del el['name']
                element = Element(name,**el)
                elements.append(element)
                if element and element.instance and element.type == 'video':
                    element.instance.props = el['props']
                
            setDirectory(data['directory'])



    def setWindowMode(self, mode : int, update = True):
        self.windowMode = mode
        self.MainEditor.enabled = mode == 0
        self.ElementGallery.enabled = mode == 1
        self.RenderTab.enabled = mode == 2
        self.ProjectGallery.enabled = mode == 3
        self.videorunning = False
        
        if update:
            self.update()
            self.draw()

    def relative(self, numcode: str | int | float, index=0, area: Area = None) -> int:
        """
        Returns the number relative to the screen.
        Example:
        0.4x represents 40% of the x axis.
        0.2y is 20% of y axis.


        index
        0 - position x
        1 - position y
        2 - size x
        3 - size y 
        """
        if isinstance(numcode, (float | int)):
            return int(numcode)

        if area and hasattr(area, "parent") and area.parent:
            # replace relative to parent
            # scaled to parent width and height
            # offset parent position

            numcode = numcode.replace(
                "x", f" * {self.relative(area.parent.w, index, area.parent)}  ")
            numcode = numcode.replace(
                "y", f" * {self.relative(area.parent.h, index, area.parent)}")

            if (index == 0):
                numcode += f" + {self.relative(area.parent.x, 0, area.parent)}"
            if (index == 1):
                numcode += f" + {self.relative(area.parent.y, 1, area.parent)}"

        else:
            # the regular case using screen position
            numcode = numcode.replace("x", f" * {self.width} ")
            numcode = numcode.replace("y", f" * {self.height} ")

        # Add more validation to avoid malicious code execution via eval
        allowed_chars = "0123456789. *+-/"
        if any(char not in allowed_chars for char in numcode):
            return 0

        try:
            result = int(eval(numcode))
            return result
        except ZeroDivisionError:
            return 0
        except Exception as e:
            return 0

    def keyUp(self, keyName):
        return self.keyboard[keyName] and not self.oldkeyboard[keyName]

    def update(self) -> None:
        # Initializing before update
        for element in elements:
            element.update()

        # update
        self.setInput()
        self.event.process_events()

        # handle undo
        if self.keyUp(pg.K_z) and self.holdingCtrl: self.undoAction()

        self.ElementGallery.update()
        self.ProjectGallery.update()
        self.MainEditor.update()
        self.RenderTab.update()
        
        self.resize = False
        self.deltatime = self.clock.tick(30)
        self.currentTime += self.deltatime


    def refresh(self, section: pg.Rect | None = None ) -> None:
        if section == None: section = pg.Rect(0, 0, self.width, self.height)
        
        self.display.blit(self.screen, (0, 0))
        pg.display.update(section)

    def draw(self) -> None:
        self.ElementGallery.draw()
        self.ProjectGallery.draw()
        self.MainEditor.draw()
        self.RenderTab.draw()
        self.refresh()
