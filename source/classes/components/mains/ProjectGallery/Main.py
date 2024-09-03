import os
import re
from pathlib import Path
from config.consts import *
from classes.components.core.Rect import *
from classes.components.core.Text import *
from classes.components.core.Textbox import *

class ProjectGallery(Rect):
    def __init__(self, dimension: tuple[int, int, int, int] = (0,0,'1x','1y'), app: any = None, color: str | tuple[int, int, int, int] = "#ffffff", borderRadius=0, detectHover=False, onHoverModifiedColor=0.15) -> None:
        super().__init__(dimension, app, color, borderRadius, detectHover, onHoverModifiedColor)
        self.color = "#050505"

        self.title = self.add_child(
            Text(
                (0, 0,'1x', 70),
                self.app,
                weight="bold",
                text = "ENTER PROJECT",
                autoHeight=False,
                fontColor="#525252",
                fontHeight=25
            )
        )

        self.version = self.add_child(
            Textbox(
                (0, '.9y','1x', '.1y'),
                self.app,
                weight="light",
                starterInput= "0",
                autoHeight=False,
                fontColor="#525252",
                color = "#050505",
                fontHeight=20
            )
        )

        self.projecttabs = []
    
    def getlatestversion(self, projectName):
        directory = Path(f"versions\\{projectName}")
        pattern = re.compile(r'v(\d+)\.json')
        files = os.listdir(directory)
        numbers = [int(pattern.match(f).group(1)) for f in files if pattern.match(f)]
        latestversion = -1
        if len(numbers) > 0:
            latestversion = max(numbers)
        return latestversion


    def enterproject(self, projectname, version):
        self.app.loadproject(projectname, version)
        self.app.event.fire_event(ADD_ELEMENT_EVENT)
        self.app.event.fire_event(SELECT_ELEMENT_EVENT)
        self.app.event.fire_event(APPLY_PROPS)
        self.app.setWindowMode(0)


    def setprojects(self):
        self.projecttabs.clear() 
        projects =[str(entry) for entry in os.listdir("versions") if os.path.isdir(os.path.join("versions", entry))]

        y = 70
        x = '.1x'
        bottom = self.app.relative('.8y', 3)
        for projectname in projects:
            
            if y > bottom:
                y = 70
                x += ' + .3x'
            lastversion = str(self.getlatestversion(projectname))

            label = Text(
                dimension=(x, y, '.2x', 80),
                app = self.app,
                fontColor = "#383838",
                text = f"{projectname} ({lastversion})",
                autoHeight=False,
                fontHeight=20,
                weight="bold",
                onHoverModifiedColor=0.05,
                detectHover=True,
                color="#141414"
            )
            label.props['project'] = projectname
            label.binds['onclick'] = lambda x : self.enterproject(x.props['project'], int(self.version.value))
            y += 90
            
            self.projecttabs.append(label)
        self.add_child(self.projecttabs)

    def draw(self):
        self.setprojects()
        return super().draw()