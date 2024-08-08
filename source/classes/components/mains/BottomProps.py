from  classes.components.core.Rect import Rect
from typing import List, Optional
from classes.components.core.Area import *

class BottomPropsTab(Rect):
    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
    ) -> None:
        super().__init__(dimension, app)
        self.add_child(Rect((0, '50', '1x', 50), app, color="green"))
        self.color = "#1e1e24"

    def update(self):
        super().update()

    def drawContent(self):
        super().drawContent()
