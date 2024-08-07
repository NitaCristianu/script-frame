from classes.components.Text import Text
from classes.components.Tab import Tab
from typing import List, Optional
from classes.components.Area import *
from config.projectData import *

element_size = 30


class ElementsTab(Tab):

    oldElements: Optional[List[Element]]

    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
    ) -> None:
        super().__init__(dimension, app)

        self.add_child(
            Tab((10, 80, '1x - 20', '1y - 90'), app,
                color="#a51516", borderValue=16)
        )
        self.tabIndex = 0
        self.color = "#0d0d12"
        self.oldElements = elements
        self.setElements()

    def setElements(self):
        self.children[self.tabIndex].add_child([
            Text(
                dimension=(0, 0, '1x', '0.2y'),
                app=self.app,
                text="ABCDEFGH",
                align='left',
                fontHeight=20,
                padding=10,
                autoHeight=True
            ),

        ])

    def update(self):
        super().update()
        if self.oldElements != elements:
            self.setElements()

    def drawContent(self):
        super().drawContent()
