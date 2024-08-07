from classes.components.Tab import Tab
from typing import List, Optional
from classes.components.Area import *

class VideoPlayer(Tab):
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
