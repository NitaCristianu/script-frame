from classes.components.core.Rect import *
from classes.components.core.Text import *
from utils.math import *
from pygame import gfxdraw

class Slider(Rect):
    
    def __init__(self, dimension: tuple[int, int, int, int], app: any, color: str | tuple[int, int, int, int] = "#ffffff", borderRadius=0, detectHover=False, onHoverModifiedColor=0.15) -> None:
        super().__init__(dimension, app, color, borderRadius, detectHover, onHoverModifiedColor)
        self.value = 0.5
        self.padding = 10
        self.dragging = False
        self.range = (0, 1)
        self.binds['changed'] = None
        self.font = getFont(fontHeight=10, weight='light')
    
    def getValuePoint(self):
        r = self.h  // 6
        centerA = (int(r*1.5), int(self.h/2))
        centerB = (int(self.w - r*1.5), int(self.h/2))
        return (
            int(centerA[0] + (centerB[0] - centerA[0]) * self.value),
            int(centerA[1] + (centerB[1] - centerA[1]) * self.value)
        )


    def update(self):
        super().update()
        if not self.enabled: return
        center = self.getValuePoint()
        r = self.h // 6
        dist_Sqr = distPoints(*self.app.mpos, center[0] + self.x, center[1] + self.y)
        if self.app.mbuttons[0] and dist_Sqr < r * r:
            self.dragging = True
        if not self.app.mbuttons[0] and self.app.oldmbuttons[0]:
            self.dragging = False
            self.drawContent()
            self.app.refresh(self.rect) 

        if self.dragging:
            delta = self.app.mpos[0] - self.app.oldmpos[0]
            delta /= self.w - 2 * self.padding
            self.value += delta
            self.value = clamp(self.value, 0, 1)
            if self.binds['changed']:
                self.binds['changed'](self)
            self.drawContent()
            self.app.refresh(self.rect) 

    def drawContent(self):
        if not self.enabled: return
        super().drawContent()
        r = self.h  // 6
        color = hex_to_rgb("#1992e8")
        centerA = (int(r*1.5), int(self.h/2))
        centerB = (int(self.w - r*1.5), int(self.h/2))
        surf = pg.Surface((self.w, self.h), pg.SRCALPHA)
        AAfilledRoundedRect(surf, 
                            pg.Rect(centerA[0] - r//6,
                                    centerA[1] - r//6,
                                    centerB[0] - centerA[0],
                                    centerB[1] - centerA[1] + r//3),
                            color,
                            r
                            )
        
        text_surf = self.font.render(f'{round(lerp(self.range[0], self.range[1], self.value)*100)/100}', 1, color)
        text_rect = text_surf.get_rect(center = (self.x + self.w//2, self.y + self.h//4))                

        gfxdraw.filled_circle(surf,
                              *centerA,
                              int(r*0.6),
                              hex_to_rgb(self.color))
        gfxdraw.aacircle(surf,
                              *centerA,
                              int(r*0.5),
                              color)
        gfxdraw.filled_circle(surf,
                              *centerA,
                              int(r*0.5),
                              modifyRGB(color, 0))
        
        centerC = self.getValuePoint()

        modifier = self.dragging and .85 or .4

        gfxdraw.aacircle(surf,
                              *centerC,
                              int(r*.6),
                              modifyRGB(hex_to_rgb(self.color), modifier)
                              )

        gfxdraw.filled_circle(surf,
                              *centerC,
                              int(r*.6),
                              modifyRGB(hex_to_rgb(self.color), modifier)
                              )
                              
        self.app.screen.blit(surf, (self.x, self.y))
        self.app.screen.blit(text_surf, text_rect)


