from classes.components.core.Text import *
from classes.components.core.Image import *
from classes.components.core.Rect import *
from typing import List, Optional
from config.projectData import *
from math import ceil, floor

element_size = 30


class ElementsTab(Rect):

    oldElements: Optional[List[Element]]
    pad = 0
    page = 0
    elements_per_page = 0
    num_of_pages = 0
    
    leftArrow = None
    rightArrow = None
    createButton = None

    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
    ) -> None:
        super().__init__(dimension, app)

        self.pad = 10
        self.add_child(
            Rect((self.pad, 1 * self.pad, f'1x - {2*self.pad}', f'1y - {self.pad*2}'), app,
                 color="#18181b", borderValue=16)
        )
        self.tabIndex = 0
        self.color = "#0d0d12"
        self.oldElements = elements

    def setElements(self):
        pad = self.pad
        self.children[0].clearChildren()
        self.app.refresh()
        maxheight = self.h + self.y - pad * 2 - 50
        self.elements_per_page = 0
        index = 0
        while True:

            y = 50 * (index + 1) + pad * (index + 1) + pad  # including height
            if y > maxheight:
                self.elements_per_page = index
                break
            index += 1
        self.num_of_pages = floor(len(elements) / self.elements_per_page) 
        self.page = min(self.page, self.num_of_pages)
        firstElement = self.page*self.elements_per_page
        lastElement = min(firstElement + self.elements_per_page, len(elements))
        for i in range(firstElement, lastElement):
            index = i - firstElement
            element = elements[i]
            y = 50 * index + pad * (index + 1) + pad
            w = self.w - pad * 2
            text = Text(
                dimension=(pad*2, y, w - pad * 2, 50),
                app=self.app,
                text=element.name,
                fontHeight=20,
                padding=60,
                detectHover=True,
                borderValue=8,
                color="#222221",
                onHoverModifiedColor=0.15,
                align='left',
                autoHeight=False

            )
            text.add_child(Image(
                app=self.app,
                dimension=(pad + 20, y + pad, 30, 30),
                pngSource="customicon.png",
                borderValue=0,

            ))
            self.children[0].add_child([text])
        if (self.elements_per_page < len(elements)):
            top = max(y + 50 + pad, maxheight - 25)
            height = abs(top - maxheight) + 50
            dimension = (pad*2, top, (self.w-pad*6) /
                         3, height)

            leftArrowIndex = len(self.children[0].children)
            self.children[0].add_child(Rect(
                dimension=dimension,
                app=self.app,
                color="#222221",
                borderValue=8,
                detectHover=True,
                onHoverModifiedColor=0.07

            ))
            dimension = (pad*3 + (self.w-pad*6)/3, top, (self.w-pad*6) /
                         3, height)

            self.children[0].add_child(Rect(
                dimension=dimension,
                app=self.app,
                color="#222221",
                borderValue=8,
                detectHover=True,
                onHoverModifiedColor=0.07

            ))

            dimension = (pad*4 + (self.w-pad*6)/3*2, top, (self.w-pad*6) /
                         3, height)

            self.children[0].add_child(Rect(
                dimension=dimension,
                app=self.app,
                color="#222221",
                borderValue=8,
                detectHover=True,
                onHoverModifiedColor=0.07

            ))

            self.leftArrow = self.children[0].children[leftArrowIndex]
            self.rightArrow = self.children[0].children[leftArrowIndex + 1]
            self.createButton = self.children[0].children[leftArrowIndex + 2]
        else:
            self.leftArrow = None
            self.rightArrow = None
            self.createButton = None
        self.draw()
        self.app.refresh()

    def update(self):
        super().update()
        
        if self.rightArrow and self.rightArrow.clicked:
            self.page = min(self.page+1, self.num_of_pages)
            self.setElements()
        if self.leftArrow and self.leftArrow.clicked:
            self.page = max(self.page-1, 0)
            self.setElements()
        
        if self.app.resize:
            self.setElements()
        if self.oldElements != elements:
            self.setElements()

    def drawContent(self):
        super().drawContent()
