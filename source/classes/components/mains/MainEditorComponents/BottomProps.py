from classes.components.core.Rect import Rect
from classes.components.core.Area import *
from classes.components.core.Text import *
from classes.components.core.Image import *
from classes.components.core.Textbox import *
from classes.components.mains.MainEditorComponents.Videoplayer import *
from config.projectData import *
from config.consts import *
from pygame import gfxdraw
from utils.colors import *
from utils.shapes import *
from utils.math import *
from math import ceil

x_start_offset = 2

def revertCut(element, element1, element2, refr):
    try:
        if element1 in elements and element2 in elements:
            elements.remove(element1)
            elements.remove(element2)
            elements.append(element)
            refr(ADD_ELEMENT_EVENT)
    except Exception as e:
        print(e)


class TimelineSeciton(Rect):
    def __init__(self, dimension: tuple[int, int, int, int], app: any, color: str | tuple[int, int, int, int] = "#ffffff", borderRadius=0, detectHover=False, onHoverModifiedColor=0) -> None:
        super().__init__(dimension, app, color, borderRadius, detectHover, onHoverModifiedColor)

        self.currentTime = 0.5
        self.zoomlevel = 1
        self.detectHover = True
        self.lineFont = getFont(fontHeight=10, weight='semibold')
        self.layersTop = 0
        self.layerSize = 70
        self.timeline_lenght = 5
        self.selectedInTimeline = "outside"
        self.elementsrect = []
        self.hoveredElement : "Element" = None
        self.elementFont = getFont(weight="bold", fontHeight=15)
        self.cutmode = False

        app.event.add_listener(APPLY_PROPS, lambda: (self.app.draw(), app.refresh(self.rect)))
        app.event.add_listener(SELECT_ELEMENT_EVENT, lambda: (self.app.draw(), app.refresh(self.rect)))

    def getTimelineStartTime(self):
        return min(-self.currentTime, -self.timeline_lenght+self.currentTime)

    def getTimelineEndTime(self):
        return max(-self.currentTime, -self.timeline_lenght+self.currentTime)

    def drawTimelineBgr(self):
        timelinecolor = "#928b8d"
        x_start = self.x + x_start_offset
        x_end = self.x + self.w - x_start_offset
        x_dist = x_end - x_start
        top = self.y 
        bottom = self.y + self.h
        distance = self.zoomlevel * self.second_length  # assuming distance is the equivalent of one second
        t = self.currentTime * distance
        offset = t % distance
        
        # Create a transparent surface for drawing
        surf = pg.Surface((x_dist, bottom - top), pg.SRCALPHA)
        
        scale = max(int(1/self.zoomlevel),1)
        currentX = int(t % max(int(distance / 5), 1))
        if self.zoomlevel > .4:
            while currentX < x_end:
                pg.gfxdraw.vline(
                    surf,
                    int(currentX),
                    2,
                    4,
                    hex_to_rgb(timelinecolor),
                )
                currentX += distance / 5            
        
        
        # Draw directly onto the main screen
        currentX = int(offset)
        currentT = ceil(self.currentTime)
        # currentT -= currentT%2
        i = currentT%scale
        while currentX < x_end:
            # Draw thicker lines
            i+=1
            if i%scale == 0:
                pg.gfxdraw.vline(
                    surf,
                    int(currentX + 0.5),
                    2,
                    7,
                    hex_to_rgb(timelinecolor),
                )
                pg.gfxdraw.vline(
                    surf,
                    int(currentX - 0.5),
                    2,
                    7,
                    hex_to_rgb(timelinecolor),
                )
                text_surf = self.lineFont.render(f"{-int(currentT)} s", True, hex_to_rgb("#c2cbcd"))
                text_rect = text_surf.get_rect(center=(currentX + 1, 20))
                surf.blit(text_surf, text_rect)
                pg.gfxdraw.vline(
                    surf,
                    int(currentX),
                    35,
                    bottom,
                    hex_to_rgb("#262626"),
                )
            currentX += distance          
            currentT -= 1

        self.app.screen.blit(surf, (x_start, top))

    def getElementSize(self, element):
        element_start = element.start
        element_end = element.end
        duration = element_end - element_start
        left = int(-(-element_start - self.currentTime - 1) * self.second_length * self.zoomlevel)
        top = int(element.layer * self.layerSize + 2)
        width = int(duration * self.second_length * self.zoomlevel)
        height = int(self.layerSize - 4)
        return left, top, width, height

    def drawElements(self):
        x_start = x_start_offset
        x_end = self.w - 2
        bottom = self.h + self.y - self.layersTop

        surf = pg.Surface((x_end - x_start, bottom ), pg.SRCALPHA)

        self.elementsrect.clear()

        for element in elements:
            
            left, top, width, height = self.getElementSize(element)
            
            self.elementsrect.append((left+self.x+x_start, top+self.layersTop, width, height))

            color = hex_to_rgb(element.color)
            lighter = modifyRGB(color, .1)
            inverted = modifyRGB(invertColor(color), .1)

            gfxdraw.box(
                surf,
                pg.Rect(left, top, width, height),
                lighter
            )
            gfxdraw.rectangle(
                surf,
                pg.Rect(left, top, width+1, height+1),
                lighter
            )
            gfxdraw.box(
                surf,
                pg.Rect(left, top+height/2, width, height/2),
                color
            )
            gfxdraw.rectangle(
                surf,
                pg.Rect(left, top+height/2, width+1, height/2+1),
                color
            )
            text_surf = self.elementFont.render(len(element.name) < 10 and element.name or element[:7]+"...", True, inverted)
            text_rect = text_surf.get_rect(center = (left, top + height * 0.25))
            surf.blit(text_surf, pg.Rect(left + 3, text_rect.y, text_rect.w, text_rect.h))
             
            if element.type == 'audio' and element.selected:
                data = element.data
                downscale_factor = 500
                leftchannel = []
                rightchannel = []
                for index in range(0, len(data), downscale_factor):
                    leftval = data[index][0]
                    leftval *= element.volumemul * 8
                    y0 = -clamp(-leftval, 0, height//4)
                    center = top + int(height*.75)
                    leftchannel.append((int(index / len(data) * width + left), center-y0))
                    if len(data[index]) > 1:
                        rightval = data[index][1]
                        rightval *= element.volumemul * 8
                        y1 = clamp(rightval, 0, height//4)
                        rightchannel.append((int(index / len(data) * width + left), center-y1))

                if len(rightchannel) > 1:
                    gfxdraw.filled_polygon(
                        surf,
                        rightchannel,
                        inverted
                    )

                gfxdraw.filled_polygon(
                    surf,
                    leftchannel,
                    inverted
                )
           
            if element.selected:
                gfxdraw.rectangle(
                    surf,
                    pg.Rect(left, top, width+1, height+1),
                    inverted
                )
                gfxdraw.rectangle(
                    surf,
                    pg.Rect(left-1, top-1, width+3, height+3),
                    inverted
                )
                

        videotime_x = self.getVideoTimeMarkPosition()
        gfxdraw.vline(
            surf,
            int(videotime_x),
            2,
            bottom,
            hex_to_rgb("#6de6b7")
        )
        self.app.screen.blit(surf, (self.x + x_start, self.layersTop)) 

    def drawContent(self):
        if not self.enabled: 
            return
        super().drawContent()
        self.drawTimelineBgr()
        self.drawElements()
    
    def update(self):
        if not self.enabled: return
        super().update()
        self.layersTop = 35 + self.y
        self.second_length = self.w / self.timeline_lenght

        if self.app.mbuttons[0] and not self.app.oldmbuttons[0]:
            self.selectedInTimeline = self.getSelected()
            if self.hoveredElement:
                if not self.app.holdingCtrl:
                    for element in elements:
                        element.selected = False
                self.hoveredElement.selected = True
                self.app.event.fire_event(SELECT_ELEMENT_EVENT)
        if self.selectedInTimeline == "timeline" and self.app.doubleclick:
            if self.app.holdingShift:
                self.app.videotime = round(self.getMouseTime() * 1000, 1)
            else:
                self.app.videotime = self.getMouseTime() * 1000
            self.app.draw()
            self.app.refresh(self.rect)

        if self.app.keyUp(pg.K_BACKSPACE):
            
            foundOne = False
            while True:
                found = False
                for element in elements:
                    if element.selected:
                        found = True
                        foundOne = True
                        elements.remove(element)
                        break
                if not found: break
            if foundOne:
                self.draw()
                self.app.refresh(self.rect)
                self.app.event.fire_event(ADD_ELEMENT_EVENT)

        if self.selectedInTimeline != "outside" and self.hovered and self.app.mbuttons[0]:
            delta = self.app.mpos[0] - self.app.oldmpos[0]
            distance = self.zoomlevel * self.second_length  # assuming distance is the equivalent of one second
            change = 0
            if distance != 0:
                change =  delta / distance
            selecting = self.selectedInTimeline

            if self.app.holdingCtrl:
                self.zoomlevel = clamp(self.zoomlevel + delta/800, 0.05, 90)
                self.draw()
                self.app.refresh(self.rect)
            else:
                if selecting == "timeline":   
                    self.currentTime += change
                elif selecting == "element" and self.hoveredElement:
                    hovered = self.hoveredElement
                    hovered.selected = True
                    mLayer = int(max(self.app.mpos[1] - self.layersTop, 0)/self.layerSize)
                    hovered.layer = mLayer
                    if self.app.holdingShift:
                        delta = hovered.start
                        hovered.start = round(change+hovered.start, 1)
                        delta = hovered.start - delta
                        hovered.end += delta
                    else:
                        hovered.start += change
                        hovered.end += change
                elif selecting == "videomark":
                    self.app.videorunning = False
                    if self.app.holdingShift:
                        self.app.videotime = round(self.app.videotime + change * 1000, 1)
                    else:
                        self.app.videotime += change * 1000
                if selecting == "timeline" or selecting == "outside":
                    found = False
                    for element in elements:
                        found = True
                        element.selected = False
                    if found : self.app.event.fire_event(SELECT_ELEMENT_EVENT)

                    self.draw()
                    self.app.refresh(self.rect)
                else:
                    self.app.draw()
                    self.app.refresh()

        if self.app.keyUp(pygame.K_c) and self.cutmode:
            # cut audio
            for element in (element for element in elements if element.type == 'audio' and element.selected):
                start = element.start
                end = element.end

                current = self.app.videotime / 1000
                if not(start <= current and end > current): continue
                
                elements12 = element.splitaudio(current)
                self.app.addAction(revertCut, [element, *elements12, self.app.event.fire_event])
                self.app.event.fire_event(ADD_ELEMENT_EVENT)
                
                self.drawContent()
                self.app.refresh(self.rect)
            

        if self.app.videorunning:
            self.drawContent()
            self.app.refresh(self.rect)

    def getTimeMarkPosition(self, time) -> float:
        return (time + self.currentTime + 1) * self.second_length * self.zoomlevel

    def getVideoTimeMarkPosition(self) -> float:
        return self.getTimeMarkPosition(self.app.videotime/1000)

    def getMouseTime(self) -> float:
        mx, my = self.app.mpos
        sl = self.second_length * self.zoomlevel
        currentTime = self.currentTime
        secondsaonscreen = int(self.w / sl)
        lastsecond = secondsaonscreen-currentTime-1
        firstsecond = -self.currentTime-1

        return lerpMap(self.x, self.x+self.w, firstsecond, lastsecond, mx)
    
    def getSelected(self) -> str:
        mx,my = self.app.mpos
        if not inRect(mx,my,self.x,self.y,self.w,self.h):
            self.hoveredElement = None
            return "outside"

        dist = abs(self.getVideoTimeMarkPosition() + self.x + x_start_offset - mx)
        if dist < 5:
            self.hoveredElement = None
            return "videomark"
        for i, element in enumerate(self.elementsrect):
            if inRect(mx,my, *element):
                self.hoveredElement = elements[i]
                return "element"
        self.hoveredElement = None


        return "timeline"

class ProjectSettings(Rect):
    def __init__(self, dimension: tuple[int, int, int, int], app: any, color: str | tuple[int, int, int, int] = "#ffffff", borderRadius=0, detectHover=False, onHoverModifiedColor=0.15) -> None:
        super().__init__(dimension, app, color, borderRadius, detectHover, onHoverModifiedColor)
        self.enabled = False

        self.bgr = self.add_child(Rect(
            (5, 5, '1x - 10', '1x - 10'),
            self.app,
            "#0a0a0a",
            borderRadius=4,
            onHoverModifiedColor=0


        ))

        self.versionLabel = self.add_child(Text(
            (0, 10, '1x', '40'),
            self.app,
            fontColor= (22, 22, 22),
            text = f'version: {str(self.app.projectVersion)}',
            fontHeight=15
            
        ))

        innerbuttonsColor = "#ec2416"
        self.projectnameLabel = self.add_child(Textbox(
            (".1x", '30', '.8x', '30'),
            self.app,
            autoHeight=False,
            color=innerbuttonsColor,
            starterInput=self.app.projectName,
            fontHeight = 20,
            borderRadius=4
        ))
        def changename(label : Textbox):
            self.app.projectName = label.value
            self.draw()
            self.app.refresh(self.rect)
        self.projectnameLabel.binds['changed'] = changename
    


class BottomPropsTab(Rect):
    
    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,    ) -> None:
        super().__init__(dimension, app)
        self.color = "#0a0a0a"
        self.onHoverModifiedColor = 0

        self.add_child([
            TimelineSeciton((0, 45, '1x', '1y-50'), self.app, color = "#050505", borderRadius=4),
            ProjectSettings((0, 45, '1x', '1y-50'), self.app, color = "#050505", borderRadius=4)
        ])
        self.onHoverModifiedColor = 0
    
        self.add_child(Text(
            dimension=(10, 10, 120, '25'),
            app = self.app,
            text="RENDER",
            weight="semibold",
            color="#021303",
            fontColor="#04f72c",
            autoHeight=False,
            padding=10,
            fontHeight=20,
            borderRadius=4,
            detectHover=True
        ))


        self.add_child(Image(
            dimension=(140, 10, '25', '25'),
            app = self.app,
            pngSource= "transform.png",
            color = "#262626",
            scale=(0.7, 0.7),
            centerImage=True,
            detectHover=True
        ))

        self.add_child(Image(
            dimension=(175, 10, '25', '25'),
            app = self.app,
            pngSource= "razor.png",
            color = "#262626",
            scale=(0.7, 0.7),
            centerImage=True,
            detectHover=True
        ))

        self.add_child(Image(
            dimension=(210, 10, '25', '25'),
            app = self.app,
            pngSource= "settings.png",
            color = "#262626",
            scale=(0.7, 0.7),
            centerImage=True,
            detectHover=True
        ))

    @property
    def renderButton(self):
        return self.children[2]

    @property
    def transformModeBtn(self):
        return self.children[3]
    
    @property
    def cutmodebtn(self):
        return self.children[4]

    @property
    def settingbtton(self):
        return self.children[5]

    def update(self):
        super().update()

        if self.renderButton.clicked:
            self.app.setWindowMode(2)
            self.app.draw()
            self.app.event.fire_event(RENDER_VIDEO)
        elif self.transformModeBtn.clicked:
            self.app.transformMode = not self.app.transformMode
            self.draw()
            self.app.refresh(self.rect)
        elif self.cutmodebtn.clicked:
            self.children[0].cutmode = not self.children[0].cutmode
            self.draw()
            self.app.refresh(self.rect)
        elif self.settingbtton.clicked:
            self.children[0].enabled = not self.children[0].enabled
            self.children[1].enabled = not self.children[1].enabled
            self.draw()
            self.app.refresh(self.rect)


    def drawContent(self):
        self.transformModeBtn.color = "#1e61f1" if self.app.transformMode else self.color
        self.cutmodebtn.color = "#9716ec" if self.children[0].cutmode else self.color
        self.settingbtton.color = "#ec2416" if self.children[1].enabled else self.color

        super().drawContent()