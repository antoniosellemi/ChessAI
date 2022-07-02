""" Handles user input and displaying game state at given time """

import pygame as game
from Chess import engine

IMAGES = {}
HEIGHT = WIDTH = 512
DIMENSION = 8
SQUARE_SIZE = WIDTH // DIMENSION
MAX_FPS = 15

""" 
Load in Images into Dictionary 
"""
def getimages():
    pieces = ["wp", "bp", "wR", "bR", "wN", "bN", "wB", "bB", "wQ", "bQ", "wK", "bK"]
    for piece in pieces:
        IMAGES[piece] = game.transform.scale(game.image.load("Images/" + piece + ".png"), (SQUARE_SIZE,SQUARE_SIZE))

"""
Handles User Input and Updating Graphics
"""
def rungame():
    getimages()
    game.init()
    screen = game.display.set_mode((WIDTH, HEIGHT))
    clock = game.time.Clock()
    screen.fill(game.Color("white"))
    bs = engine.BoardState()
    playing = True
    while playing:
        for event in game.event.get():
            if event.type == game.QUIT:
                playing = False
        clock.tick(MAX_FPS)
        game.display.flip()

if __name__ == '__main__':
    rungame()