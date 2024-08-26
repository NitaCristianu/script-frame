import pygame
import sys
from classes.App import *
from config.consts import *

def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(INITIAL_VIEWPORT_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption(NAME)

    app = App(screen)

    initialRenders = 0

    while True:
        events = pygame.event.get()
        for event in events:
            # Default events
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                App.width = event.w
                App.height = event.h
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                app.screen = pg.Surface((event.w, event.h), pg.SRCALPHA, 32)
                app.resize = True
                app.update()
                app.draw()

        app.update()
        if initialRenders < 2:
            initialRenders += 1
            app.draw()



if __name__ == "__main__":
    main()
 