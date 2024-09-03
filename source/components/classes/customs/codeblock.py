from components.classes.node import *
from pygments import highlight
from classes.components.core.Text import getFont
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.token import Token
from collections import defaultdict

class codeblock(Node):
    def __init__(self, master, **args) -> None:
        
        props = {
            'color' : pg.Color((0, 0, 0, 0)),
            'code' : "",
            'font' : "Poppins",
            "lang" : "python",
            "style" : "monokai", # Choose a style (e.g., 'monokai', 'default', 'solarized-dark')
            "fontheight" : 25,
        } | args

        super().__init__(master,**props)

    def render(self) -> None:
        self.fontobj = getFont(font=self.font(), fontHeight = self.fontheight())
        x,y = 0, 0
        parent = self
        while (parent):
            x += parent.x()
            y += parent.y()
            parent = parent.parent
        
        style_name = self.style()
        formatter = HtmlFormatter(style = style_name)
        lexer = get_lexer_by_name(self.lang())
        
        code = self.code()

        style_dict = defaultdict(lambda : "#000000")
        for token, style in formatter.style:
            if style['color']:
                style_dict[token] = f"#{style['color']}"

        lines = code.splitlines()
        colored_lines = []
        
        for line in lines:
            tokens = lexer.get_tokens(line)
            colored_tokens = [(value, style_dict[token_type]) for token_type, value in tokens]
            colored_tokens.pop()
            colored_lines.append(colored_tokens)

        startx = x
        starty = y
        lineheight = self.fontheight() + 5
        
        w, h = 0, 0
        x, y = 0, 0
        surfs = []
        for line in colored_lines:
            x = 0  # Reset x for each new line
            for word, color in line:
                text_surface = self.fontobj.render(word, True, pg.Color(color))
                surfs.append((text_surface, (x,y)))
                x += text_surface.get_width()
                w = max(w, x)
            y += lineheight  # Move to the next line
            h = max(h, y)
        h+= lineheight

        x = startx
        y = starty
        
        surf = pg.Surface((w, h), pg.SRCALPHA)
        size = surf.get_size()
        for text_surf in surfs:
            surf.blit(*text_surf)

        self.w = Signal(lambda : size[0], self.master)
        self.h = Signal(lambda : size[1], self.master)
        self.master.surf.blit(surf, surf.get_rect(center = self.rect.center))

        return super().render()