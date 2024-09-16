import pygame as pg

INITIAL_WIDTH = 1200
INITIAL_HEIGHT = 700
COMPONENTS_DIRECTORY = r"C:\Users\andre\Documents\GitHub\script-frame-master\videodata"
AUDIO_DIRECTORY = COMPONENTS_DIRECTORY + "\\audio"
EDITOR_DIRECTORY = r"C:\Users\andre\Documents\GitHub\script-frame-master"
ENABLE_ERRORS = True
INITIAL_VIEWPORT_SIZE = (INITIAL_WIDTH, INITIAL_HEIGHT)

ADD_ELEMENT_EVENT = pg.USEREVENT + 1
SELECT_ELEMENT_EVENT = pg.USEREVENT + 2
APPLY_PROPS = pg.USEREVENT + 3
RENDER_VIDEO = pg.USEREVENT + 4

NAME = "ScriptFrame"

def setDirectory(location : str):
    global COMPONENTS_DIRECTORY
    COMPONENTS_DIRECTORY = location