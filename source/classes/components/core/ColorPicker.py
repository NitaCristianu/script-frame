from classes.components.core.Rect import *
from utils.math import *

class ColorPicker(Rect):

    def __init__(self, dimension: tuple[int, int, int, int], app: any, color: str | tuple[int, int, int, int] = "#ffffff", borderRadius=0, detectHover=True, onHoverModifiedColor=0.15) -> None:
        super().__init__(dimension, app, color, borderRadius, detectHover, onHoverModifiedColor)
        self.binds['changed'] = None
        self.value = pg.Color(color)
        self.huepos = lerpMap(0, 360, 0, self.w, self.value.hsla[0])
        self.satpos = lerpMap(0, 100, 0, self.w, self.value.hsla[1])
        self.lumpos = lerpMap(0, 100, 0, self.w, self.value.hsla[2])

    def update(self):
        super().update()
        x,y = self.app.mpos
        if self.app.mbuttons[0] and x >= self.x and x <= self.x + self.w and y >= self.y+self.h*0.75 and y <= self.y+self.h:
            x = self.app.mpos[0] - self.x
            color = pg.Color(0)
            color.hsla = (int(360 * x / self.w), self.value.hsla[1], self.value.hsla[2], 100)
            self.value = color
            self.huepos = x
            if self.binds['changed']:
                self.binds['changed'](self)
        elif self.app.mbuttons[0] and x >= self.x and x <= self.x + self.w and y >= self.y and y <= self.y + self.h * 0.75:
            xt = clamp(int(invLerp(self.x, self.x+self.w, x)*100), 0, 100)
            yt = clamp(int(100 - linear(invLerp(self.y, (self.y+self.h*0.75), y))*100), 0, 100)
            self.satpos = x - self.x
            self.lumpos = y - self.y
            hue = max(0, min(100, int(self.value.hsla[0])))
            print(hue)
            color = pg.Color(0)
            color.hsla = (hue, xt, yt, 100)
            self.value = color
            if self.binds['changed']:
                self.binds['changed'](self)

            
    def drawContent(self):
        if not self.enabled: return
        super().drawContent()
        
        colorpicker_height = self.h * 0.75

        surf = pg.Surface((self.w,colorpicker_height), pg.SRCALPHA, 32)

        surf1 = pg.Surface((1, 2), pg.SRCALPHA, 32)
        surf1.fill((255, 255, 255))
        surf1.set_at((0, 1), (0,0,0))
        surf1 = pg.transform.smoothscale(surf1, (self.w, colorpicker_height))

        vibrant_col = pg.Color(0)
        vibrant_col.hsla = (self.value.hsla[0], 100, 50, 100)
        surf2 = pg.Surface((2, 1), pg.SRCALPHA, 32)
        surf2.fill((255, 255, 255))
        surf2.set_at((1, 0), vibrant_col)
        surf2 = pg.transform.smoothscale(surf2, (self.w, colorpicker_height))
        
        surf1.blit(surf2, (0, 0), special_flags=pg.BLEND_MULT)
        surf.blit(surf1, (0,0))

        h = self.h - colorpicker_height
        slidersurf = pg.Surface((self.w, h+1), pg.SRCALPHA, 32)
        self.rad = h//4
        
        for i in range(0, int(self.w), 3): 
            color = pg.Color(0)
            hue = int(360 * i / self.w)
            color.hsla = (hue, 100, 50, 100)
            pg.draw.rect(slidersurf, color, (i, 0, 5, h+1))
        self.p = 0

        pg.draw.rect(
            slidersurf,
            (255,255,255),
            pg.rect.Rect(self.huepos-2, 0, 4, h),
        )

        pg.draw.circle(
            surf,
            (255,255, 255),
            (self.satpos, self.lumpos),
            5
        )
        pg.draw.circle(
            surf,
            (0,0,0),
            (self.satpos, self.lumpos),
            5,
            2
        )

        self.app.screen.blit(slidersurf, (self.x,self.y+colorpicker_height))
        self.app.screen.blit(surf, (self.x,self.y))
    
    def get_color(self):
        color = pg.Color(0)
        color.hsla = (int(self.p * self.pwidth), 100, 50, 100)
        return color