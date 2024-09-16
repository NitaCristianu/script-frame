from components.classes.node import *
from classes.components.core.Text import getFont
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from collections import defaultdict
from uuid import uuid4
from components.utils.easing import linear

class Word():
    def __init__(self, val: str, color: pg.Color, codeblock: 'codeblock', apperanceval = 255) -> None:
        self.value = Signal(val, codeblock.master)
        self.color = color
        self.apperance = Signal(apperanceval, codeblock.master)
        self.enabled = True

    def getsurf(self, fontobj: pg.font.Font) -> pg.Surface:
        self.color.a = 0  # Directly set the alpha to 0, making the color fully transparent
        text_surface = fontobj.render(self.value(), True, self.color)
        text_surface.set_alpha(self.apperance())

        return text_surface

    def remove(self, t):
        self.enabled = False
        self.apperance(0, t)


class codeblock(Node):
    def __init__(self, master, **args) -> None:

        props = {
            'color': pg.Color((0, 0, 0, 0)),
            'code': "",
            'font': "Poppins",
            "lang": "python",
            # Choose a style (e.g., 'monokai', 'default', 'solarized-dark')
            "style": "monokai",
            "fontheight": 25,
        } | args
        
        self.deletelinecount = 0
        self.addlinecount = 0
        self.removedline = False
        self.addedline = False
        self.addedline = False
        self.id = uuid4().hex

        super().__init__(master, **props)
        self.setlinedata(self.code())

    def reset(self):
        for line in self.linedata:
            for w in line:
                w.apperance.reset()
                w.value.reset()
        return super().reset()

    def setlinedata(self, val):
        self.linedata = self.getlinesdata(val)
        self.removedlines: dict[str, Signal] = {}

    def deleteWord(self, line: int, column: int, t=1):
        """
        deletes the word at [line][column] in t time
        """
        if not (0 <= line < len(self.linedata)):
            return False
        if not (0 <= column < len(self.linedata[line])):
            return False

        word: 'Word' = self.linedata[line][column]
        word.remove(t)

        return True

    def deleteLine(self, line: int, t=1):
        """
        deletes the line at [line] in t time
        """
        deletionid = self.id + "deletion" + str(self.master.reqtime)
        self.deletelinecount = 0
        if not (0 <= line < len(self.linedata)):
            return False

        self.removedlines[str(line)] = Signal(1, self.master)
        self.removedlines[str(line)](0, t)
        for word in self.linedata[line]:
            word.apperance(0, t)
        self.removedline = True
        def deleteline():
            code: str = self.code()
            codelines = code.splitlines()
            del codelines[line]
            newcode = "\n".join(codelines)
            self.setlinedata(newcode)

        self.master.callin(deleteline, t, deletionid)

    def editat(self, line, column, t = .3):
        """
        adds a word at [line][column] in t time
        """ 
        if not (0 <= line < len(self.linedata)):
            return False
        if not (0 <= column < len(self.linedata[line])):
            return False

        return self.linedata[line][column].value

    @property
    def style_dict(self):
        style_name = self.style()
        formatter = HtmlFormatter(style=style_name)
        style_dict = defaultdict(lambda: "#000000")

        for token, style in formatter.style:
            if style['color']:
                style_dict[token] = f"#{style['color']}"

        return style_dict

    @property
    def lexer(self):
        return get_lexer_by_name(self.lang())

    def getlinesdata(self, code: str) -> List[List['Word']]:
        style_name = self.style()
        formatter = HtmlFormatter(style = style_name)
        lexer = get_lexer_by_name(self.lang())

        style_dict = defaultdict(lambda : "#000000")
        for token, style in formatter.style:
            if style['color']:
                style_dict[token] = f"#{style['color']}"

        lines = code.splitlines()
        colored_lines = []
        
        for line in lines:
            tokens = lexer.get_tokens(line)
            colored_tokens = [Word(value, pg.Color(style_dict[token_type]), self, 255) for token_type, value in tokens]
            colored_tokens.pop()
            colored_lines.append(colored_tokens)
        return colored_lines


    def drawlines(self):
        lineheight = self.fontheight() + 5
        surfs = []
        oy = w = h = 0

        for line_index, line in enumerate(self.linedata):
            ox = 0  # Reset x for each new line
            lineremoved = str(line_index) in self.removedlines
            for word in line:
                word_surface = word.getsurf(self.fontobj)
                word_width = word_surface.get_width()
                apperance = word.apperance()
                
                surfs.append((word_surface, (ox, oy)))
                w = max(w, ox+word_width)
                if lineremoved:
                    ox += word_width
                else:
                    ox += apperance / 255 * word_width 

            if lineremoved:
                oy += self.removedlines[str(line_index)]() * lineheight
            else:
                oy += lineheight  # Move to the next line
            h = max(h, oy)

        h += lineheight

        return surfs, (w, h)

    def render(self) -> None:
        self.fontobj = getFont(font=self.font(), fontHeight=self.fontheight())

        surfs, size = self.drawlines()
        surf = pg.Surface(size, pg.SRCALPHA, 32)

        for text_surf in surfs:
            surf.blit(*text_surf)
        
        # print("------------------")
        # for line_index, line in enumerate(self.linedata):
        #     lineremoved = str(line_index) in self.removedlines
        #     print("line : ", lineremoved, end = " ")
        #     for word in line:
        #         print(word.apperance(), end=" ")
        #     print()

        self.w = Signal(lambda: size[0], self.master)
        self.h = Signal(lambda: size[1], self.master)
        self.master.surf.blit(surf, surf.get_rect(center=self.rect.center))

        return super().render()
