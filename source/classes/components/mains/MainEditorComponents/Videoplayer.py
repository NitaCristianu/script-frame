from classes.components.core.Rect import Rect
from config.projectData import *
from classes.components.core.Area import *

class VideoPlayer(Rect):
    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
    ) -> None:
        super().__init__(dimension, app)
        self.color = "#000000"
        size = (1600, 900)
        self.videosize = size
        self.oldvideosize = size
        
    def update(self):

        if self.app.keyUp(pg.K_SPACE):
            self.app.videorunning = not self.app.videorunning

        if self.app.videorunning:
            self.app.videotime += self.app.deltatime 
            self.drawContent()
            self.app.refresh(self.rect)
        if self.videosize != self.oldvideosize or self.app.resize:
            self.drawContent()
            self.app.refresh(self.rect)

        self.oldvideosize = self.videosize       
        super().update()

    def drawContent(self):
        if self.videosize == (0,0): return
        frame: pg.Surface = pg.Surface(self.videosize, pg.SRCALPHA, 32)
        t: int = self.app.videotime
        super().drawContent()
        elements.sort(key= lambda el: -el.layer)
        for element in elements:
            if t < element.start*1000 or t > element.end*1000: continue

            result: pg.Surface = element.instance.render(
                t/1000 - element.start,
                pg.Surface(tuple(x*2 for x in self.videosize), pg.SRCALPHA, 32)
            )
            frame.blit(
                result,
                (element.x, element.y)
            )
        
        scaled = None
        # B is video rect
        # A is video display rect

        # rescaling video to fit the screen``
        scale_width = self.w / self.videosize[0]
        scale_height = self.h / self.videosize[1]
        scale = min(scale_width, scale_height)
        scaledSize = (self.videosize[0] * scale, self.videosize[1] * scale)
        scaled = pg.transform.scale(frame, scaledSize)
        center = (self.x + self.w//2, self.y + self.h//2)
        topleft = (center[0] - scaledSize[0]//2, center[1] - scaledSize[1]//2)
        
        self.app.screen.blit(scaled, topleft)
            