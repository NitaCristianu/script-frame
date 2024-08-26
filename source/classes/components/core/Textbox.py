from classes.components.core.Text import *
from utils.keyconsts import *
from pygame import gfxdraw

selected_id = None  # Global variable to store the selected textbox id

class Textbox(Text):
    
    holding = False
    lastPressedTime = ""
    delay = 0
    changed = False
    placeholder = ""

    def __init__(self, dimension: tuple[int, int, int, int], app: any, color: str = "#00000000", borderRadius=0, font="Poppins", italic=False, weight='normal', fontHeight=25, text="", align="center", fontColor="#ececec", padding=0, autoHeight=True, detectHover=True, onHoverModifiedColor=0, placeholder = "", starterInput = "") -> None:
        super().__init__(dimension, app, color, borderRadius, font, italic, weight, fontHeight, text, align, fontColor, padding, autoHeight, detectHover, onHoverModifiedColor)
        self.holding = self.changed = False
        self.lastDeleted = self.delay = 0
        self.placeholder = placeholder
        self.value = starterInput
        self.lastPressedTime = self.text = ""
        self.binds['changed'] = None

    def applyKey(self, key: str):
        capslock = pg.key.get_mods() & pg.KMOD_CAPS
        holdShift = self.app.holdingShift
        isUpper = holdShift != capslock
        
        if len(key) == 1:
            self.value = self.value + (isUpper and key.upper() or key)
        elif key == "BACKSPACE":
            self.value = self.value[:-1]
        elif key == "SPACE":
            self.value = self.value + " "

        self.lastDeleted = self.app.currentTime
        self.lastPressedTime = key
        return True

    @property
    def selected(self):
        global selected_id  
        return selected_id == self.id
        
    def read(self):
        return self.value or ""
    
    def setInput(self, value: str):
        self.value = value
        return True

    def drawContent(self):
        if not self.enabled: return False
        
        x,y,w,h = max(self.x, 0), max(self.y, 0), max(self.w, 0), max(self.h, 0)
        surface = pg.Surface((w, h), pg.SRCALPHA)

        AAfilledRoundedRect(
            surface,
            pg.Rect(0,0,w,h),
            hex_to_rgb(self.color),
            self.borderRadius
        )
        


        self.app.screen.blit(surface, (x, y))
        text = len(self.value) > 0 and self.value or self.placeholder
        color = len(self.value) > 0 and self.fontColor or modifyRGB(hex_to_rgb(self.fontColor), -.4)
        text_surface = self.font.render(text, True, color)
        h = self.autoHeight and self.fontHeight or self.h
        
        if self.align == 'center':
            text_rect = text_surface.get_rect(
                center=((self.x + self.w//2, self.y + h//2))
            )
        else:
            text_rect = text_surface.get_rect(
                topleft=(self.x + self.padding, self.y +
                         h/2 - self.fontHeight/1.5)
            )
        self.app.screen.blit(text_surface, text_rect)

    def update(self):
        self.changed = False

        super().update()
        global selected_id  

        if not self.isEnabled:
            if selected_id == self.id:
                selected_id = None
            return

        # Selection logic
        if self.app.mup:
            if self.hovered:
                selected_id = self.id
            elif selected_id == self.id:
                selected_id = None

        if self.selected:
            for key, value in keyconsts.items():
                if self.app.keyboard[value] and self.lastDeleted < self.app.currentTime - self.delay and len(self.lastPressedTime) > 0:  # Holding key
                    self.changed = self.applyKey(key)
                    self.delay = max(50, self.delay - 250)
                if self.app.keyUp(value):  # First pressed
                    self.changed = self.applyKey(key)
                    self.delay = 500

            if len(self.lastPressedTime) and self.app.currentTime - self.lastDeleted > 500:
                self.lastPressedTime = ""
            
            if self.changed:
                self.text = len(self.value) > 0 and self.value or self.placeholder
                self.binds['changed'](self)
                self.app.draw()
                self.app.refresh(self.rect)
