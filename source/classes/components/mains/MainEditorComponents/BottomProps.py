from classes.components.core.Rect import Rect
from classes.components.core.Area import *
from classes.components.core.Text import *
from config.projectData import *
from pygame import gfxdraw
from utils.colors import *
from utils.shapes import *
from utils.math import *
from math import ceil

x_start_offset = 2

class Timeline(Rect):
    def __init__(self, dimension: tuple[int, int, int, int], app: any, color: str | tuple[int, int, int, int] = "#ffffff", borderRadius=0, detectHover=False, onHoverModifiedColor=0) -> None:
        super().__init__(dimension, app, color, borderRadius, detectHover, onHoverModifiedColor)

        self.currentTime = 0.5
        self.zoomlevel = 1
        self.detectHover = True
        self.lineFont = getFont(fontHeight=10, weight='semibold')
        self.layersTop = 0
        self.layerSize = 50
        self.seconds = 5
        self.selectedInTimeline = "outside"
        self.elementsrect = []
        self.hoveredElement : "Element" = None

    def drawTimeline(self):
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
        
        currentX = int(t % int(distance / 5))
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
        while currentX < x_end:
            # Draw thicker lines
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

    def drawElements(self):
        x_start = x_start_offset
        x_end = self.w - 2
        bottom = self.h + self.y - self.layersTop

        surf = pg.Surface((x_end - x_start, bottom ), pg.SRCALPHA)

        self.elementsrect.clear()
        for element in elements:
            element_start = element.start
            element_end = element.end
            duration = element_end - element_start # in seconds
            top = element.layer * self.layerSize + 2
            left = -(-element_start - self.currentTime - 1) * self.second_length * self.zoomlevel
            width = duration * self.second_length * self.zoomlevel
            height = self.layerSize - 4
            
            left = int(left)
            top = int(top)
            width = int(width)
            height = int(height)
            self.elementsrect.append((left+self.x+x_start, top+self.layersTop, width, height))

            color = hex_to_rgb(element.color)
            gfxdraw.filled_polygon(
                surf,
                [(left, top), (left+width, top), (left+width, top+height), (left, top+height)],
                color
            )
            if element.selected:
                gfxdraw.aapolygon(
                    surf,
                    [(left, top), (left+width, top), (left+width, top+height), (left, top+height)],
                    modifyRGB(invertColor(color), .1)
                    # 0,
                    # 15
                )
                gfxdraw.aapolygon(
                    surf,
                    [(left-1, top-1), (left+width+1, top-1), (left+width+1, top+height+1), (left-1, top+height+1)],
                    modifyRGB(invertColor(color), .3)
                    # 0,
                    # 15
                )

        videotime_x = self.getVideoTimeMarkPosition()
        gfxdraw.vline(
            surf,
            int(videotime_x),
            top,
            bottom,
            hex_to_rgb("#6de6b7")
        )
        self.app.screen.blit(surf, (self.x + x_start, self.layersTop))

    def drawContent(self):
        if not self.enabled: 
            return
        super().drawContent()
        self.drawTimeline()
        self.drawElements()

    def update(self):
        if not self.enabled: return
        super().update()
        self.layersTop = 35 + self.y
        self.second_length = self.w / self.seconds

        if self.app.mbuttons[0] and not self.app.oldmbuttons[0]:
            self.selectedInTimeline = self.getSelected()
        if self.selectedInTimeline == "timeline" and self.app.doubleclick:
            if self.app.holdingShift:
                self.app.videotime = round(self.getMouseTime() * 1000, 1)
            else:
                self.app.videotime = self.getMouseTime() * 1000
            self.app.draw()
            self.app.refresh(self.rect)


        if self.selectedInTimeline != "outside" and self.hovered and self.app.mbuttons[0]:
            delta = self.app.mpos[0] - self.app.oldmpos[0]
            distance = self.zoomlevel * self.second_length  # assuming distance is the equivalent of one second
            change =  delta / distance
            selecting = self.selectedInTimeline
            if selecting == "timeline":   
                self.currentTime += change
            elif selecting == "element" and self.hoveredElement:
                hovered = self.hoveredElement
                hovered.selected = True
                if self.app.holdingShift:
                    delta = hovered.start
                    hovered.start = round(change+hovered.start, 1)
                    delta = hovered.start - delta
                    hovered.end += delta
                else:
                    hovered.start += change
                    hovered.end += change


            elif selecting == "videomark":
                if self.app.holdingShift:
                   self.app.videotime = round(self.app.videotime + change * 1000, 1)
                else:
                   self.app.videotime += change * 1000

            if selecting == "timeline" or selecting == "outside":
                for element in elements:
                    element.selected = False
                self.draw()
                self.app.refresh(self.rect)
            else:
                self.app.draw()
                self.app.refresh()

        if self.app.videorunning:
            self.drawContent()
            self.app.refresh(self.rect)

    def getVideoTimeMarkPosition(self) -> float:
        return (self.app.videotime/1000 + self.currentTime + 1) * self.second_length * self.zoomlevel

    def getMouseTime(self) -> float:
        mx, my = self.app.mpos
        return mx / (self.second_length * self.zoomlevel ) - 3.5 - self.currentTime
    


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

class BottomPropsTab(Rect):
    def __init__(
        self,
        dimension: tuple[int, int, int, int],
        app: any,    ) -> None:
        super().__init__(dimension, app)
        self.color = "#1e1e24"

        self.add_child([
            Timeline((0, 45, '1x', '1y-50'), self.app, color = "#0e0e0e", borderRadius=4)
        ])
        self.onHoverModifiedColor = 0
    

    def update(self):
        super().update()

    def drawContent(self):
        super().drawContent()