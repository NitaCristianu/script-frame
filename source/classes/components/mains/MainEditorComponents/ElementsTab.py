from classes.components.core.Text import *
from classes.components.core.Textbox import typing
from classes.components.core.Image import *
from classes.components.core.Rect import *
from config.projectData import *
from math import floor
from utils.event import *
from config.consts import *

element_size = 30
btn_color = "#110f01"

def selectElementById(id: str, self : any):
    if not self.app.holdingCtrl:
        for element in elements:
            element.selected = False

    matching_element = next((element for element in elements if element.id == id), None)
    matching_element.selected = not matching_element.selected
    self.app.event.fire_event(SELECT_ELEMENT_EVENT)

class ElementsTab(Rect):

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
                 color="#0a0a0a", borderRadius=4)
        )
        self.tabIndex = 0
        self.color = "#050505"
        
        app.event.add_listener(ADD_ELEMENT_EVENT, lambda : (self.setElements(), self.app.event.fire_event(SELECT_ELEMENT_EVENT)))
        app.event.add_listener(APPLY_PROPS, lambda : (self.setElements()))

    def setElements(self):
        pad = self.pad
        self.children[0].clearChildren()
        self.app.refresh()
        maxheight = self.h + self.y - pad * 2 - 65
        self.elements_per_page = 0
        index = 0
        while True:
            y = 50 * (index + 1) + pad * (index + 1) + pad  # including height
            if y > maxheight:
                self.elements_per_page = index
                break
            index += 1
        if self.elements_per_page == 0: self.elements_per_page = 0 + 0.0001 # avoid division by 0

        self.num_of_pages = floor(len(elements) / self.elements_per_page)
        self.page = min(self.page, self.num_of_pages)
        firstElement = int(self.page*self.elements_per_page)
        lastElement = int(min(firstElement + self.elements_per_page, len(elements)))
        for i in range(firstElement, lastElement):
            index = i - firstElement
            element = elements[i]
            y = 50 * index + pad/2 * index + pad * 1.5
            w = self.w - pad * 2
            text = Text( 
                dimension=(pad*1.5, y, w - pad, 50),
                app=self.app,
                text=element.name,
                fontHeight=20,
                padding=60,
                detectHover=True,
                borderRadius=4,
                color=saturate(hex_to_rgb(element.color), .3),
                fontColor=modifyRGB(saturate(hex_to_rgb(element.color), .3),0.65),
                onHoverModifiedColor=0.15,
                align='left',
                autoHeight=False

            )
            text.props['id'] = element.id
            text.binds['onclick'] = lambda text: selectElementById(text.props['id'], self)
            text.add_child(Image(
                app=self.app,
                dimension=(pad + 20, y + pad, 30, 30),
                pngSource="customicon.png",
                borderRadius=0,

            ))
            self.children[0].add_child([text])

        top = maxheight - pad + 20
        height = abs(top - maxheight) + 45
        if (self.elements_per_page < len(elements)):
            dimension = (pad*2, top, (self.w-pad*6) /
                         3, height)

            leftArrowIndex = len(self.children[0].children)
            self.children[0].add_child(Rect(
                dimension=dimension,
                app=self.app,
                color=btn_color,
                borderRadius=4,
                detectHover=True,
                onHoverModifiedColor=0.07

            ))
            dimension = (pad*3 + (self.w-pad*6)/3, top, (self.w-pad*6) /
                         3, height)

            self.children[0].add_child(Rect(
                dimension=dimension,
                app=self.app,
                color=btn_color,
                borderRadius=4,
                detectHover=True,
                onHoverModifiedColor=0.07

            ))

            self.leftArrow = self.children[0].children[leftArrowIndex]
            self.rightArrow = self.children[0].children[leftArrowIndex + 1]

            self.rightArrow.add_child(Image(
                (self.rightArrow.dimension[0], self.rightArrow.dimension[1],
                 self.rightArrow.dimension[2], self.rightArrow.dimension[3]),
                self.app,
                pngSource="right.png",
                forceHeight=True,
                centerImage=True,
                scale=(0.8, 0.8)
            ))
            self.leftArrow.add_child(Image(
                (self.leftArrow.dimension[0], self.leftArrow.dimension[1],
                 self.leftArrow.dimension[2], self.leftArrow.dimension[3]),
                self.app,
                pngSource="left.png",
                forceHeight=True,
                centerImage=True,
                scale=(0.8, 0.8)
            ))
        else:
            self.leftArrow = None
            self.rightArrow = None

        createbuttonIndex = len(self.children[0].children)
        if self.leftArrow:
            dimension = (pad*4 + (self.w-pad*6)/3*2, top, (self.w-pad*6) /
                         3, height)
        else:
            dimension = (pad*2, top, self.w-pad*4, height)

        self.children[0].add_child(Rect(
            dimension=dimension,
            app=self.app,
            color=btn_color,
            borderRadius=4,
            detectHover=True,
            onHoverModifiedColor=0.07

        ))
        self.createButton = self.children[0].children[createbuttonIndex]
        if not self.leftArrow:
            self.createButton.add_child(
                Text(
                    self.createButton.dimension,
                    self.app,
                    text="Create",
                    padding= 50,
                    autoHeight=False,
                    fontColor="#f7cd04",
                    align="center",
                    weight='bold',
                    fontHeight= 30,
                )
            )
        else:
            self.createButton.add_child(Image(
                self.createButton.dimension,
                self.app,
                pngSource="create.png",
                forceHeight=True,
                centerImage=True,
                scale=(0.5, 0.5)
            ))

        self.draw()
        self.app.refresh()

    def update(self):
        super().update()

        if (self.app.keyUp(pg.K_r)) and not typing():
            for el in (el for el in elements if el.selected):
                el.reset()

        if self.app.keyUp(pg.K_DELETE) and not typing():
            
            foundOne = False
            while True:
                found = False
                for element in elements:
                    if element.selected:
                        found = True
                        foundOne = True
                        elements.remove(element)
                        break
                if not found: break
            if foundOne:
                self.draw()
                self.app.refresh(self.rect)
                self.app.event.fire_event(ADD_ELEMENT_EVENT)
        
        if self.rightArrow and self.rightArrow.clicked:
            self.page = min(self.page+1, self.num_of_pages)
            self.setElements()

        if self.leftArrow and self.leftArrow.clicked:
            self.page = max(self.page-1, 0)
            self.setElements()

        if self.createButton and self.createButton.clicked:
            self.app.setWindowMode(1)

        if self.app.resize:
            self.setElements()

    def drawContent(self):
        super().drawContent()
