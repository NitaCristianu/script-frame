from classes.components.core.Rect import Rect
from config.projectData import *
from config.consts import *
from utils.math import *
from pygame import gfxdraw
from config.errorobj import Main as ErrorScene
from classes.components.core.Area import *


def renderFrame(videosize, t):
    frame: pg.Surface = pg.Surface(videosize, pg.SRCALPHA, 32)

    elements.sort(key= lambda el: -el.layer)
    for element in (element for element in elements if element.type == "video"):
        # if element appears on the video
        if t < element.start*1000 or t > element.end*1000: continue

        element.instance.render_start(t/1000 - element.start)
        result: pg.Surface = element.instance.render_end()

        # set element lenght
        if hasattr(element.instance, 'lenght'):
            element.end = element.start + element.instance.lenght

        pos = (element.x, element.y)
        
        # attach surface to video
        frame.blit(
            result,
            pos
        )
    
    return frame


class VideoPlayer(Rect):
    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,
    ) -> None:
        super().__init__(dimension, app)
        self.color = "#050505"
        self.videoscale = 0.25
        self.videosize = (1920, 1080)
        self.oldvideosize = self.videosize
        self.lastRender = app.currentTime 
        self.elementData= []
        self.onHoverModifiedColor = 0
        
        def renderSelected():
            if app.transformMode:
                self.draw()
                app.refresh()
        
        app.event.add_listener(APPLY_PROPS, lambda: (self.draw(), app.refresh(self.rect)))
        app.event.add_listener(SELECT_ELEMENT_EVENT, renderSelected)
        
    def getVideoRect(self):
        """"
        returns the video rect which is clipped
        inside the self.rect
        """
        scale_width = self.w / self.videosize[0]
        scale_height = self.h / self.videosize[1]
        scale = min(scale_width, scale_height)
        scaledSize = (self.videosize[0] * scale, self.videosize[1] * scale)
        center = (int(self.x + self.w//2), int(self.y + self.h//2))
        topleft = (int(center[0] - scaledSize[0]//2), int(center[1] - scaledSize[1]//2))
        return topleft, scaledSize

    def toVideoPosition(self, x, y):
        """
        returns the position of x y
        relative to the video
        """
        topleft, scaledSize = self.getVideoRect()
        mx = lerpMap(topleft[0], topleft[0]+scaledSize[0],0,self.videosize[0],x)
        my = lerpMap(topleft[1], topleft[1]+scaledSize[1],0,self.videosize[1],y)
        return mx, my

    def roundElementCenter(self, pos_x, pos_y, unit_x, unit_y, object_w, object_h):
        """"
        centers the element based on position sectioned on a grid
        the units are specified in arguments
        """
        cx = round(pos_x / unit_x) * unit_x
        cy = round(pos_y / unit_y) * unit_y
        return (int(cx - object_w/2), int(cy - object_h/2))

    def drawBox(self, frame, x, y, w, h):
        gfxdraw.box(frame, pg.Rect(x-10,y-10,w+20,h+20), (250,210,50, 150))
    
    def drawGridLines(self, frame, x, y, w, h):
        pg.draw.line(frame, (255,255,255, 100), (0, y+h/2), (self.videosize[0], y+h/2), 10)
        pg.draw.line(frame, (255,255,255, 100), (x+w/2, 0), (x+w/2, self.videosize[1]), 10)

    def refresh(self):
        self.draw()
        self.app.refresh(self.rect)

    def update(self):
        super().update()

        if self.app.keyUp(pg.K_SPACE):
            self.app.videorunning = not self.app.videorunning
        if self.app.videorunning:
            self.app.videotime += self.app.deltatime * self.app.playbackspeed
            self.drawContent()
            self.app.refresh(self.rect)
        if self.videosize != self.oldvideosize or self.app.resize:
            self.drawContent()
            self.app.refresh(self.rect)
        if self.app.transformMode and self.isHoveredCurrently:
            # handle transformation

            # get mouse positions relative to video
            mx, my = self.toVideoPosition(*self.app.mpos)
            omx, omy = self.toVideoPosition(*self.app.oldmpos)
            
            # get unit lenght by dividing the total 
            # video size in multiple segments
            unit_x = (self.videosize[0])/10
            unit_y = (self.videosize[1])/10

            # looping through every element to check for transformations
            for elementdata in self.elementData:
                # does element exist
                element =  next((element for element in elements if element.id == elementdata[0]), None)
                if not element or not element.selected: continue

                # object rect's data
                object_position = elementdata[1]
                object_surface = elementdata[2]
                object_w, object_h = object_surface.get_size()


                if self.app.mup:
                    # element dragging logic
                    if element.dragging:
                        element.dragging = False
                    else:
                        element.dragging = inRect(mx, my, *object_position, object_w, object_h)
                    
                    self.refresh()

                # move object if being dragged
                
                if element.dragging:
                    if self.app.holdingCtrl:
                        element.x = 0
                        element.y = 0
                    elif not self.app.holdingShift:
                        # move based on grid
                        new_x, new_y = self.roundElementCenter(mx, my, unit_x, unit_y, object_w, object_h)
                        element.x = new_x
                        element.y = new_y
                    else:
                        # move freely
                        element.x += mx - omx
                        element.y += my - omy


                    self.refresh()

        self.playAudio()
        # register video size change
        self.oldvideosize = self.videosize       

    def playSound(self, sound: pg.mixer.Sound, soundTime: float):
        time = self.app.videotime
        oldtime = time - self.app.deltatime * self.app.playbackspeed

        if time >= soundTime and oldtime < soundTime and self.app.videorunning: 
            sound.play()
        elif not self.app.videorunning:
            sound.stop()


    def playAudio(self):

        for element in elements:
            if element.type == "audio":
                sound = element.pygamesound
                sound.set_volume(element.volumemul)
                self.playSound(sound, element.start * 1000)
            elif element.type == "video":
                sounds = element.instance.sounds
                for sound, time in sounds:
                    self.playSound(sound, time * 1000 + element.start * 1000)

            

    def drawContent(self):
        # the conditions for rendering
        if not self.enabled: return
        if self.videosize == (0,0): return
        if self.app.currentTime - self.lastRender < 30: return
        super().drawContent()

        # frame and time variables
        frame = pg.Surface(self.videosize, pg.SRCALPHA, 32)
        t = self.app.videotime

        # clear the element list used in update
        self.elementData.clear()
        
        # sort elements based on layers
        elements.sort(key= lambda el: -el.layer)
        for element in elements:
            # if element appears on the video
            if t < element.start*1000 or t > element.end*1000 or not element.type == "video" : continue

            try:
                element.instance.render_start(t/1000 - element.start)
            except Exception as e:
                element.instance = ErrorScene()
                element.instance.errormessage = str(e)
                element.instance.render_start(t/1000 - element.start)
                print(e)

            result: pg.Surface = element.instance.render_end()

            # set element lenght
            if hasattr(element.instance, 'lenght'):
                element.end = element.start + element.instance.lenght

            pos = (element.x, element.y)

            self.elementData.append((
                element.id,
                pos,
                result
            ))

            # draw transform lines
            if element.selected and self.app.transformMode and element.dragging:
                w,h = result.get_size()
                x,y = (int(element.x), int(element.y))
                if not self.app.holdingShift:
                    self.drawGridLines(frame, x, y, w, h)
                self.drawBox(frame, x,y,w,h)
            
            # attach surface to video
            frame.blit(
                result,
                pos
            )


        # rescale the video so it fits the screen
        topleft, scaledSize = self.getVideoRect()
        scaled = pg.transform.scale(frame, scaledSize)
        
        # render and save last render
        self.app.screen.blit(scaled, topleft)
        self.lastRender = self.app.currentTime
            