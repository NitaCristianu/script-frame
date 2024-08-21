import numpy as np
import threading
from config.projectData import *
from config.consts import *
from classes.components.mains.MainEditorComponents.Videoplayer import *
from classes.components.core.Rect import *
from classes.components.core.Text import *
from moviepy.editor import ImageSequenceClip

class RenderMode(Rect):
    def __init__(self, dimension: tuple[int, int, int, int] = (0, 0, '1x', '1y'), app: any = None, color: str | tuple[int, int, int, int] = "#0e0e0e00", borderRadius=0, detectHover=False, onHoverModifiedColor=0.15) -> None:
        super().__init__(dimension, app, color, borderRadius, detectHover, onHoverModifiedColor)

        n_frames = int(max(*tuple(el.end for el in elements)) * 1000 / 30)
        self.frm = pg.Surface((0,0))
        self.add_child(Rect(
            dimension=(0, 0, '1x', '1y'),
            app = app,
            color="#000000d0",
            

        ))
        self.add_child(Text(
            dimension=(0, '0.1y', '1x', '1y'),
            autoHeight=True,
            app = self.app,
            text= f"RENDERING : 0 / {n_frames}",
            weight="light",
            fontHeight=20
        ))
        self.add_child(Text(
            dimension=(0, '0.1y + 25', '1x', '1y'),
            autoHeight=True,
            app = self.app,
            text= f"press ESC to cancel",
            weight="light",
            fontHeight=14
        ))
        self.app.event.add_listener(RENDER_VIDEO, lambda : self.render() )
    
    def draw(self):
        if not self.enabled: return
        transformed = pg.transform.scale(self.frm, (self.w, self.h))
        self.app.screen.blit(transformed, (0,0))
        super().draw()

    def render(self):
        n_frames = int(max(*tuple(el.end for el in elements)) * 1000 / 30)
        frames = []
        self.children[2].text = "press ESC to cancel"
        for index in range(n_frames):
            events = pg.event.get()
            if next(iter(ev for ev in events if ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE), None):
                self.app.setWindowMode(0)
                return
            
            self.frm = renderFrame((1600, 900), index*30)

            array = pg.surfarray.array3d(self.frm)
            array = np.transpose(array, (0, 1, 2))
            array = np.flipud(array)
            array = np.rot90(array, k=-1) 
            

            self.children[1].text = f"Frame : {index} / {n_frames-1}"
            self.draw()
            self.app.refresh()
            frames.append(array)
        self.children[1].text = f"WRITING FILE"
        self.children[2].text = ""
        self.draw()
        self.app.refresh()

        clip = ImageSequenceClip(frames, fps = 30)
        clip.write_videofile("output.mp4", codec = "libx264")
        self.app.setWindowMode(0)
        