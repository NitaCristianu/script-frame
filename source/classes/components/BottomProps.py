from classes.components.Tab import Tab
from typing import List, Optional
from classes.components.Area import *

class BottomPropsTab(Tab):
    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
    ) -> None:
        super().__init__(dimension, app)
        self.add_child(Tab((0, '50', '1x', 50), app, color="green"))
        self.color = "#1e1e24"

    def update(self):
        super().update()

    def drawContent(self):
        super().drawContent()
