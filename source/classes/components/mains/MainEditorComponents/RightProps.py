from classes.components.core.Rect import *
from classes.components.core.Slider import *
from classes.components.core.ColorPicker import *
from classes.components.core.Text import *
from config.projectData import *
from config.consts import *
from typing import Union

gap = 15
padding = 15
title_size = 20
propSize = 50

class RightPropsTab(Rect):
    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
    ) -> None:
        super().__init__(dimension, app)
        self.color = "#1e1e24"
        app.event.add_listener(SELECT_ELEMENT_EVENT, lambda : self.setProps())

    def addProp(self, lastY, prop) -> Area:
        obj = None
        title_size = 15
        x = self.x + padding
        y = lastY + gap + title_size
        w = self.w - padding * 2
        showtitle = True
        if prop['propType'] == 'slider':
            obj = Slider(
                (x, y, w, propSize),
                self.app,
                color="#232323",
                onHoverModifiedColor = 0
            )
            obj.value = invLerp(
                prop['min'],
                prop['max'],
                prop['value']
            )
            def set(slider):
                prop['value'] = lerp(prop['min'], prop['max'], slider.value)
                self.app.event.fire_event(APPLY_PROPS)
            obj.binds['changed'] = set
        elif prop['propType'] == 'consttext1':
            obj = Text(
                (x, y-20, w, propSize/4),
                self.app,
                onHoverModifiedColor= 0,
                fontHeight=propSize/3,
                autoHeight=True,
                text=prop['value']
            )
            showtitle = False
        elif prop['propType'] == 'color1':
            obj = ColorPicker(
                (x, y+5, w, w/2),
                self.app,
                color = prop['value']
            )
            def set(colorpicker):
                prop['value'] = colorpicker.value
                self.app.event.fire_event(APPLY_PROPS)
            obj.binds['changed'] = set
        
        
        if not showtitle:
            self.add_child(obj)
            return obj        
        obj2 = Rect(
            (x - padding/2, y-title_size - 5, w + padding, obj.h + 2 * title_size + 10),
            self.app,
            color="#232323",
            borderRadius=16
        )
        obj2.add_child(Text(
            (x, y-title_size, w, 0),
            app = self.app,
            text = prop["name"],
            fontHeight=title_size,
            fontColor="#9a9a9a",
        ))
        obj2.add_child(obj)
        self.add_child(obj2)
        
        return obj2

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
        bottom = self.h
        # default props
        defaults: List['Prop'] = [
            {
                'name' : 'name',
                'value' : element.name,
                'propType' : 'consttext1',
            },
        ]
        props: List['Prop'] = [
            *element.instance.props,
            ]

        for prop in defaults:
            lastY += self.addProp(lastY, prop).h + gap
        for prop in props:
            lastY += self.addProp(lastY, prop).h + gap
        self.draw()
        self.app.refresh(self.rect)

    def update(self):
        
        super().update()

    def drawContent(self):
        super().drawContent()
