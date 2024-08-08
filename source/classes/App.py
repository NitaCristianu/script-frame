import pygame as pg
from classes.components.core.Rect import *
from config.consts import INITIAL_WIDTH, INITIAL_HEIGHT
from classes.components.mains.ElementsTab import ElementsTab
from classes.components.mains.Videoplayer import VideoPlayer
from classes.components.mains.BottomProps import BottomPropsTab
from classes.components.mains.RightProps import RightPropsTab


class App:

    display: pg.Surface
    screen: pg.Surface
    width = INITIAL_WIDTH
    height = INITIAL_HEIGHT
    mpos: tuple[int, int]
    events: pg.event.Event = []

    clock = pg.time.Clock()
    deltatime = 0  # time between 2 renders
    mbuttons = (False, False, False)
    oldmbuttons = (False, False, False)
    mup = False
    resize = True

    A: Rect
    B: Rect
    C: Rect
    D: Rect

    def __init__(self, screen: pg.Surface) -> None:
        self.display = screen
        self.screen = pg.Surface((INITIAL_WIDTH, INITIAL_HEIGHT), pg.SRCALPHA)
        self.A = ElementsTab((0, 0, "0.25x", "1y"), self)
        self.B = VideoPlayer(("0.25x", 0, "0.5x", "0.5y"), self)
        self.C = BottomPropsTab(("0.25x", "0.5y", "0.5x", "0.5y"), self)
        self.D = RightPropsTab(("0.75x", 0, "0.25x", "1y"), self)
        self.__setMousePos()
        self.resize = True

    def __setMousePos(self):
        self.mpos = pg.mouse.get_pos()
        self.oldmbuttons = self.mbuttons
        self.mbuttons = pg.mouse.get_pressed()

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
        self.mup = next(
            (True for event in self.events if event.type == pg.MOUSEBUTTONUP), False
        )

    def processEvents(self, events: pg.event.Event) -> None:
        self.events = events

    def update(self) -> None:
        self.__setMousePos()
        self.setMup()
        self.A.update()
        self.B.update()
        self.C.update()
        self.D.update()
        self.deltatime = self.clock.tick(30)
        self.resize = False

    def refresh(self, section: pg.Rect | None = None ) -> None:
        if section == None: section = pg.Rect(0, 0, self.width, self.height)
        
        self.display.blit(self.screen, (0, 0))
        pg.display.update(section)

    def draw(self) -> None:
        self.A.draw()
        self.B.draw()
        self.C.draw()
        self.D.draw()
        self.refresh()
