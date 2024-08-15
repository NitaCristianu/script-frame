from  classes.components.core.Rect import Rect
from classes.components.core.Area import *

class BottomPropsTab(Rect):
    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
    ) -> None:
        super().__init__(dimension, app)
        self.color = "#1e1e24"

        self.add_child([
            Rect((5, 45, '1x - 10', '1y-50'), self.app, color = "#060606", borderValue=4)
        ])

    def update(self):
        super().update()

    def drawContent(self):
        super().drawContent()
