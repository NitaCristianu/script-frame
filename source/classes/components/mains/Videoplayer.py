from classes.components.core.Rect import Rect
from typing import List, Optional
from classes.components.core.Area import *

class VideoPlayer(Rect):
    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
    ) -> None:
        super().__init__(dimension, app)
        self.color = "#ffffff"

    def update(self):
        super().update()

    def drawContent(self):
        super().drawContent()
