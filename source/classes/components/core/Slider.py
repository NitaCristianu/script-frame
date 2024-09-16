from classes.components.core.Rect import *
from classes.components.core.Textbox import *
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
        self.add_child(Textbox(
            (self.x, self.y+3, self.w, 10),
            app,
            fontColor= "#1992e8",
            starterInput="0",
            autoHeight=False,
            fontHeight=8,
            
        ))
        
        def setText(text: Textbox):
            try:
                self.value = invLerp(*self.range , float(text.value))
                self.children[0].input = f'{round(lerp(*self.range, self.value)*100)/100}'
                if self.binds['changed']:
                    self.binds['changed'](self)
            except Exception as e:
                return
        self.children[0].binds['changed'] = setText
    
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
            self.children[0].input = f'{round(lerp(self.range[0], self.range[1], self.value)*100)/100}'
            if self.binds['changed']:
                self.binds['changed'](self)
            self.drawContent()
            self.app.refresh(self.rect) 

    def drawContent(self):
        if not self.enabled: return
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


