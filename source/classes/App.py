import pygame as pg
from classes.components.core.Rect import *
from config.consts import INITIAL_WIDTH, INITIAL_HEIGHT
from classes.components.mains.MainEditor import *
from classes.components.mains.ElementGallery import *
from utils.event import *


class App:

    display: pg.Surface
    screen: pg.Surface
    width = INITIAL_WIDTH
    height = INITIAL_HEIGHT
    mpos: tuple[int, int]

    clock = pg.time.Clock()
    deltatime = 0  # time between 2 renders
    mbuttons = (False, False, False)
    oldmbuttons = (False, False, False)
    mup = False
    resize = True
    event = None
    currentTime = 0
    windowMode = 0
    # 0 - main editor
    # 1 - element gallery

    def __init__(self, screen: pg.Surface) -> None:
        self.display = screen
        self.screen = pg.Surface((INITIAL_WIDTH, INITIAL_HEIGHT), pg.SRCALPHA)
        self.keyboard = self.oldkeyboard = pg.key.get_pressed()
        self.setInput()
        self.resize = True
        self.event = EventManager()

        self.MainEditor = MainEditor(app = self)
        self.ElementGallery = ElementGallery(app = self)

        self.setWindowMode(0, update = False)

    def setInput(self):
        self.setMup()
        self.oldkeyboard = self.keyboard
        self.keyboard = pg.key.get_pressed()
        self.mpos = pg.mouse.get_pos()
        self.oldmbuttons = self.mbuttons
        self.mbuttons = pg.mouse.get_pressed()
        self.holdingShift = self.keyboard[pg.K_LSHIFT] or self.keyboard[pg.K_RIGHT]
        self.holdingCtrl = self.keyboard[pg.K_LCTRL] or self.keyboard[pg.K_LCTRL]

    def setWindowMode(self, mode : int, update = True):
        self.windowMode = mode
        self.MainEditor.enabled = mode == 0
        self.ElementGallery.enabled = mode == 1
        
        if self.update:
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

    def setMup(self):
        self.mup = self.oldmbuttons[0] and self.mbuttons[0]

    def keyUp(self, keyName):
        return self.keyboard[keyName] and not self.oldkeyboard[keyName]

    def update(self) -> None:
        # Initializing
        self.setInput()
        self.event.process_events()
        self.deltatime = self.clock.tick(30)
        self.currentTime += self.deltatime

        self.ElementGallery.update()
        self.MainEditor.update()
        
        self.resize = False

    def refresh(self, section: pg.Rect | None = None ) -> None:
        if section == None: section = pg.Rect(0, 0, self.width, self.height)
        
        self.display.blit(self.screen, (0, 0))
        pg.display.update(section)

    def draw(self) -> None:
        self.MainEditor.draw()
        self.ElementGallery.draw()
        self.refresh()
