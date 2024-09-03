from classes.components.core.Rect import *
from classes.components.core.Slider import *
from classes.components.core.ColorPicker import *
from classes.components.core.Textbox import *
from classes.components.core.Text import *
from config.projectData import *
from config.consts import *
from typing import Optional

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
        self.color = "#050505"
        app.event.add_listener(SELECT_ELEMENT_EVENT, lambda : self.setProps())

    def addProp(self, lastY, prop, element: Optional['Element'] = None) -> Area:
        obj = None
        title_size = 15
        x = self.x + padding
        y = lastY + gap + title_size
        w = self.w - padding * 2
        showtitle = True
        if prop['propType'] == 'slider':
            obj = Slider(
                (x, y, w, propSize*0.7),
                self.app,
                color="#050505",
                onHoverModifiedColor = 0
            )
            obj.range = (prop['min'], prop['max'])
            if not element:
                obj.value = invLerp(
                    prop['min'],
                    prop['max'],
                    prop['value']
                )
            elif element and element.type == 'audio':
                name = prop['name']
                if name == 'volume': name = 'volumemul'
                obj.value = invLerp(
                    prop['min'],
                    prop['max'],
                    getattr(element, name)
                )
            def set(slider):
                if element and element.type == "audio":
                    name = prop['name']
                    if name == 'volume': name = 'volumemul'
                    setattr(element, name, lerp(prop['min'], prop['max'], slider.value))
                elif not element:
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
                if element and element.type == "audio":
                    pass
                else:
                    color: pg.Color = colorpicker.value
                    prop['value'] = (color.r, color.b, color.g, color.a)
                self.app.event.fire_event(APPLY_PROPS)
            obj.binds['changed'] = set
        elif prop['propType'] == 'textbox':
            obj = Textbox(
                (x, y, w, propSize),
                self.app,
                starterInput = prop['value'],
                placeholder="enter text",
                fontHeight=15,
                autoHeight=False
            )
            def set(textbox):
                prop['value'] = textbox.value
                self.app.event.fire_event(APPLY_PROPS)
            obj.binds['changed'] = set
        
        
        if not showtitle:
            self.add_child(obj)
            return obj        
        obj2 = Rect(
            (x - padding/2, y-title_size - 5, w + padding, obj.h + 2 * title_size + 10),
            self.app,
            color="#050505",
            borderRadius=4
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
        if element.type == "audio":
            defaults: List['Prop'] = [
                *defaults,
                {
                    'name' : 'volume',
                    'value' : 1,
                    'propType' : 'slider',
                    'min' : 0.01,
                    'max' : 10
                }
            ]
        if element.type == "video":
            defaults: List['Prop'] = [
                *defaults,
                *element.instance.props,
                ]

        for prop in defaults:
            element_arg = None
            if element.type == 'audio': element_arg = element
            lastY += self.addProp(lastY, prop, element_arg).h + gap
        self.draw()
        self.app.refresh(self.rect)

    def update(self):
        
        super().update()

    def drawContent(self):
        super().drawContent()
