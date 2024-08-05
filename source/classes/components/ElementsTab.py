from classes.components.Tab import Tab
from typing import List, Optional
from classes.components.Area import *
from config.projectData import *


class ElementsTab(Tab):

    oldElements: Optional[List[Element]]

    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
    ) -> None:
        super().__init__(dimension, app)
        
        self.add_child(
            Tab((10, 80, '1x - 20' , '1y - 90'), app, color = "#a51516", borderValue=16)
        )
        self.color = "#0d0d12"
        self.oldElements = elements

        

    def setElements():
        pass

    def update(self):
        super().update()
        if self.oldElements != elements:
            self.setElements()

    def draw(self):
        super().draw()
