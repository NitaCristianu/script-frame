from classes.components.Tab import Tab
from typing import List, Optional
from classes.components.Area import *

class RightPropsTab(Tab):
    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
    ) -> None:
        super().__init__(dimension, app)
        self.color = "#1e1e24"

    def update(self):
        # print("X", self.children)
        super().update()

    def draw(self):
        super().draw()
