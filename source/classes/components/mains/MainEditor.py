from classes.components.core.Area import *
from classes.components.core.Area import dimension_type
from classes.components.mains.MainEditorComponents.BottomProps import *
from classes.components.mains.MainEditorComponents.ElementsTab import *
from classes.components.mains.MainEditorComponents.RightProps import *
from classes.components.mains.MainEditorComponents.Videoplayer import *

class MainEditor(Area):
    def __init__(self, dimension: tuple[str | int, str | int, str | int, str | int] = (0, 0, '1x', '1y'), app: any = None, detectHover=False) -> None:
        super().__init__(dimension, app, detectHover)
        self.add_child([
            ElementsTab((0, 0, "0.25x", "1y"), self.app),
            VideoPlayer(("0.25x", 0, "0.5x", "0.5y"), self.app),
            BottomPropsTab(("0.25x", "0.5y", "0.5x", "0.5y"), self.app),
            RightPropsTab(("0.75x", 0, "0.25x", "1y"), self.app)
        ])
    
