from classes.components.core.Rect import Rect
from classes.components.core.Area import *
from classes.components.core.Text import *
from classes.components.core.Image import *
from classes.components.core.Textbox import *
from classes.components.mains.MainEditorComponents.Videoplayer import *
from config.projectData import *
from config.consts import *
from pygame import gfxdraw
from pathlib import Path
from utils.colors import *
from utils.shapes import *
from utils.math import *
import json
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
        self.second_length = 100
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
            top += 2
            height -= 4

            self.elementsrect.append((left+self.x+x_start, top+self.layersTop, width, height))

            color = hex_to_rgb(element.color)
            lighter = modifyRGB(color, .1)
            inverted = modifyRGB(invertColor(color), .1)

            pg.draw.rect(surf, lighter, pg.Rect(left, top, width, height), 0, 4)
            pg.draw.rect(surf, color, pg.Rect(left, top+height//2, width, height//2), 0, -1, -1, -1, 4, 4)

            dotsize = self.elementFont.size("...")
            if isinstance(element.name, str) and element.name != "":
                letters = len(element.name)
                
                # Measure the size of the full string once
                text_size = self.elementFont.size(element.name)
                
                # If the full string fits, no need to truncate
                if text_size[0] <= width:
                    text_surf = self.elementFont.render(element.name, True, inverted)
                else:
                    # Calculate average width per character
                    avg_char_width = text_size[0] / letters
                    
                    # Estimate how many letters can fit within the width
                    max_letters = int((width - dotsize[0]) / avg_char_width)
                    
                    # Render text with truncation
                    text_surf = self.elementFont.render(element.name[:max_letters] + "...", True, inverted)
                
                text_rect = text_surf.get_rect(center=(left, top + height * 0.25))
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
                pg.draw.rect(surf, inverted, pg.Rect(left, top, width, height), 1, 4)
               
                

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
            for el in elements:
                if el.type != "video": continue
                el.setInstance()
            if self.app.holdingShift:
                self.app.videotime = round(self.getMouseTime() * 1000, 1)
            else:
                self.app.videotime = self.getMouseTime() * 1000
            self.app.draw()
            self.app.refresh(self.rect)

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
                    self.app.event.fire_event(SELECT_ELEMENT_EVENT)
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
            (5, 5, '1x - 5', '1y - 10'),
            self.app,
            "#0a0a0a",
            borderRadius=4,
            onHoverModifiedColor=0


        ))

        self.versionLabel = self.add_child(Text(
            (0, 10, '1x', '40'),
            self.app,
            fontColor= (42, 42, 42),
            text = f'version: {str(self.app.projectVersion)}',
            fontHeight=15
            
        ))
        self.directoryLabel = self.add_child(Text(
            (0, 30, '1x', '40'),
            self.app,
            fontColor= (42, 42, 42),
            text = f'{COMPONENTS_DIRECTORY}',
            fontHeight=10
            
        ))

        innerbuttonsColor = "#1d1d1d"
        self.projectnameLabel = self.add_child(Text(
            (".1x", '60', '.8x', '30'),
            self.app,
            autoHeight=False,
            color=innerbuttonsColor,
            text=self.app.projectName,
            fontHeight = 20,
            borderRadius=4,
            onHoverModifiedColor=0
        ))

        self.saveButton = self.add_child(Text(
            (".25x", '100', '.5x', '30'),
            self.app,
            autoHeight=False,
            color="#03140d",
            fontColor="#2ef782",
            text="SAVE",
            fontHeight = 20,
            borderRadius=4,
            detectHover=True,
            onHoverModifiedColor=0.06,
            weight="bold"
        ))
        
        self.renderButon = self.add_child(Text(
            (".25x", '140', '.5x', '30'),
            self.app,
            autoHeight=False,
            fontHeight = 20,
            color="#060e24",
            fontColor="#1342c5",
            text="RENDER",
            borderRadius=4,
            detectHover=True,
            onHoverModifiedColor=0.06,
            weight="bold"
        ))

        self.exitButton = self.add_child(Text(
            (".25x", '180', '.5x', '30'),
            self.app,
            autoHeight=False,
            fontHeight = 20,
            color="#240606",
            fontColor="#f73232",
            text="EXIT",
            borderRadius=4,
            detectHover=True,
            onHoverModifiedColor=0.06,
            weight="bold"
        ))

        self.saveButton.binds['onclick'] = lambda x: self.saveproject()
        self.renderButon.binds['onclick'] = lambda x: (self.app.setWindowMode(2), self.app.draw(), self.app.event.fire_event(RENDER_VIDEO))
        self.exitButton.binds['onclick'] = lambda x: (self.saveproject(), self.app.setWindowMode(3))
    
    def draw(self):
        self.versionLabel.text = "version: " + str(self.app.projectVersion)
        super().draw()

    def saveproject(self):
        data = {}

        data['name'] = self.app.projectName
        data['version'] = self.app.projectVersion
        data['directory'] = COMPONENTS_DIRECTORY
        data['elements'] = []

        for element in elements:
            attr = ['name', 'source', 'start', 
                    'layer', 'x', 'y',
                    'id', 'type', 'volumemul', 'calcInstance']

            elementobj = {}
            elementobj['props'] = []
            if element.type == 'video':
                elementobj['props'] = element.instance.props

            for x in attr:
                elementobj[x] = getattr(element, x)
        
            data['elements'].append(elementobj)

        directory = Path("versions")
        foldername = self.app.projectName
        targetfolder = directory / foldername

        if not targetfolder.exists():
            targetfolder.mkdir(parents = True)

        jsonfilename = f"v{data['version']}.json"
        filepath = targetfolder / jsonfilename

        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)

        self.app.projectVersion += 1
        self.draw()
        self.app.refresh(self.rect)

        


class BottomPropsTab(Rect):
    
    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,    ) -> None:
        super().__init__(dimension, app)
        self.color = "#050505"
        self.onHoverModifiedColor = 0

        self.add_child(Rect(
            (4, 2, '1x - 4', '43'),
            self.app,
            color = "#0a0a0a",
            onHoverModifiedColor=0,
            borderRadius=4
        ))

        self.add_child([
            TimelineSeciton((0, 45, '1x', '1y-50'), self.app, color = "#050505", borderRadius=4),
            ProjectSettings((0, 45, '1x', '1y-50'), self.app, color = "#050505", borderRadius=4)
        ])
        self.onHoverModifiedColor = 0
    
        self.add_child(Image(
            dimension=(10, 10, '25', '25'),
            app = self.app,
            pngSource= "transform.png",
            color = "#262626",
            scale=(0.7, 0.7),
            centerImage=True,
            detectHover=True
        ))

        self.add_child(Image(
            dimension=(45, 10, '25', '25'),
            app = self.app,
            pngSource= "razor.png",
            color = "#262626",
            scale=(0.7, 0.7),
            centerImage=True,
            detectHover=True
        ))

        self.add_child(Image(
            dimension=(80, 10, '25', '25'),
            app = self.app,
            pngSource= "settings.png",
            color = "#262626",
            scale=(0.7, 0.7),
            centerImage=True,
            detectHover=True
        ))

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

        # if self.renderButton.clicked:
        #     self.app.setWindowMode(2)
        #     self.app.draw()
        #     self.app.event.fire_event(RENDER_VIDEO)
        if self.transformModeBtn.clicked:
            self.app.transformMode = not self.app.transformMode
            self.draw()
            self.app.refresh(self.rect)
        elif self.cutmodebtn.clicked:
            self.children[1].cutmode = not self.children[1].cutmode
            self.draw()
            self.app.refresh(self.rect)
        elif self.settingbtton.clicked:
            self.children[1].enabled = not self.children[1].enabled
            self.children[2].enabled = not self.children[2].enabled
            self.draw()
            self.app.refresh(self.rect)


    def drawContent(self):
        self.transformModeBtn.color = "#1e61f1" if self.app.transformMode else self.color
        self.cutmodebtn.color = "#9716ec" if self.children[1].cutmode else self.color
        self.settingbtton.color = "#ec2416" if self.children[2].enabled else self.color

        super().drawContent()