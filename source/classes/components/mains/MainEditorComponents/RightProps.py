from classes.components.core.Rect import Rect
from classes.components.core.Slider import *
from config.projectData import *
from config.consts import *
from typing import Union

class RightPropsTab(Rect):
    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
    ) -> None:
        super().__init__(dimension, app)
        self.color = "#1e1e24"
        app.event.add_listener(SELECT_ELEMENT_EVENT, lambda : self.setProps())

    def setProps(self, element = None):
        if element == None:
            for aelement in elements:
                if aelement.selected:
                    element = aelement
        self.children.clear()
        if element == None :
            self.draw()
            self.app.refresh(self.rect)
            return
        lastY = 0
        gap = 15
        bottom = self.h
        padding = 15
        lenght = abs(element.end - element.start)
        propSize = 50
        # default props
        props: List['Prop'] = [*element.instance.props,
            {
                'name' : 'lenght',
                'value' : lenght,
                'propType' : 'slider',
                'additional' : {
                    'min' : 0.0001,
                    'max' : lenght * 5
                }
            }]
        for prop in props:
            if prop['propType'] == 'slider':
                slider = Slider(
                    (self.x + padding, lastY + gap, self.w - padding * 2, propSize),
                    self.app,
                    self.color,
                    onHoverModifiedColor = 0
                )
                self.add_child(slider)
                lastY += propSize + gap
        self.draw()
        self.app.refresh(self.rect)

    def update(self):
        
        super().update()

    def drawContent(self):
        super().drawContent()
