from classes.components.core.Rect import *
from classes.components.core.Textbox import *
from config.consts import *
from utils.event import *
from config.projectData import *
import os


class ElementGallery(Rect):

    def __init__(self, dimension: tuple[int, int, int, int] = (0, 0, '1x', '1y'), app: any = None, color: str | tuple[int, int, int, int] = "#080807", borderValue=0, detectHover=False, onHoverModifiedColor=0.15) -> None:
        super().__init__(dimension, app, color, borderValue, detectHover, onHoverModifiedColor)

        self.add_child([
            Textbox(
                ('0.25x', '0.33y', '0.5x', '0.1y'),
                self.app,
                autoHeight = False,
                placeholder = "type module name",
                detectHover= True,
                borderRadius = .2,
                fontHeight=20,
                color="#080807",
                onHoverModifiedColor=0.025,
                align='center',
            ),
            Text(
                ('0.275x', '0.5y', '0.20x', '0.1y'),
                app = self.app,
                text = "Create",
                fontColor="#0066ff",
                detectHover= True,
                borderRadius = .2,
                fontHeight=20,
                color="#111111",
                onHoverModifiedColor=0.05,
                align='center',
                autoHeight=False

            ),
            Text(
                ('0.525x', '0.5y', '0.20x', '0.1y'),
                app = self.app,
                text = "Cancel",
                detectHover= True,
                borderRadius = .2,
                fontHeight=20,
                color="#111111",
                onHoverModifiedColor=0.05,
                align='center',
                autoHeight=False

            ),
            ]
        )
    
        self.fileExists = False
    
    def exit(self):
        self.elementNameBox.setInput("")
        self.app.setWindowMode(0)


    def update(self):
        if not self.enabled: return
        super().update()
        if self.CreateButton:
            pass

        if self.CancelButton.clicked: self.exit()
        
        if self.elementNameBox.changed:
            inp = self.elementNameBox.value + ".py"
            self.fileExists = False
            
            for filename in os.listdir(COMPONENTS_DIRECTORY):
                if inp == filename:
                    self.fileExists = True
                    break
            if self.fileExists:
                self.CreateButton.text = "Use"
            else:
                self.CreateButton.text = "Create"
            self.CreateButton.drawContent()
            self.app.refresh(self.rect)

        if self.CreateButton.clicked:
            filename = self.elementNameBox.value
            if not len(filename) > 0: return
            if self.fileExists:
                elements.append(Element(
                    name = filename,
                    source=filename
                ))
                self.app.event.fire_event(ADD_ELEMENT_EVENT)
                self.exit()
            else:
                pass

    @property
    def CreateButton(self)-> Text: return self.children[1]
    @property
    def CancelButton(self) -> Text: return self.children[2]
    @property
    def elementNameBox(self) -> Textbox: return self.children[0]
