import pygame
import sys
from classes.App import *
from config.consts import *

def main():
    pygame.init()
    screen = pygame.display.set_mode(INITIAL_VIEWPORT_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption(NAME)

    app = App(screen)

    while True:
        for event in pygame.event.get():
            # Default events
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                App.width = event.w
                App.height = event.h
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            app.processEvent(event)
            
        app.update()
        app.draw()

if __name__ == "__main__":
    main()