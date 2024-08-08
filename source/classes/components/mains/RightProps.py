from classes.components.core.Rect import Rect
from classes.components.core.Area import Area
from typing import List, Optional

class RightPropsTab(Rect):
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

    def drawContent(self):
        super().drawContent()
