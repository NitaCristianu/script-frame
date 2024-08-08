from classes.components.core.Text import *
from classes.components.core.Image import *
from classes.components.core.Rect import *
from typing import List, Optional
from config.projectData import *

element_size = 30


class ElementsTab(Rect):

    oldElements: Optional[List[Element]]

    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
    ) -> None:
        super().__init__(dimension, app)

        self.add_child(
            Rect((10, 80, '1x - 20', '1y - 90'), app,
                color="#18181b", borderValue=16)
        )
        self.tabIndex = 0
        self.color = "#0d0d12"
        self.oldElements = elements
        self.setElements()

    def setElements(self):
        for index, element in enumerate(elements):
            y = f"10 + 0.05y * {index} + 10 * {index}"
            text = Text(
                dimension=(10, y, '1x - 20', '0.05y'),
                app=self.app,
                text=element.name,
                fontHeight=20,
                padding=10,
                detectHover=True,
                borderValue=8,
                color="#272a50",
                onHoverModifiedColor=0.15,
                autoHeight=False

            )
            text.add_child(Image(
                app = self.app,
                dimension=(0, 0, 0, "1y"),
                pngSource="Cotrocen.png",
                forceHeight=True
            ))
            self.children[0].add_child([text])

    def update(self):
        super().update()
        if self.oldElements != elements:
            self.setElements()

    def drawContent(self):
        super().drawContent()
