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


def get_images():
    pieces = ["wp", "bp", "wR", "bR", "wN", "bN", "wB", "bB", "wQ", "bQ", "wK", "bK"]
    for piece in pieces:
        IMAGES[piece] = game.transform.scale(game.image.load("Images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


"""
Handles User Input and Updating Graphics
"""


def run_game():
    get_images()
    game.init()
    screen = game.display.set_mode((WIDTH, HEIGHT))
    clock = game.time.Clock()
    screen.fill(game.Color("white"))
    bs = engine.BoardState()
    playing = True
    player_mouse_clicks = []
    selected = ()
    while playing:
        for event in game.event.get():
            if event.type == game.QUIT:
                playing = False
            elif event.type == game.MOUSEBUTTONDOWN:
                square = game.mouse.get_pos()
                file = square[0]//SQUARE_SIZE
                rank = square[1]//SQUARE_SIZE
                if selected == (rank, file):
                    selected = ()
                    player_mouse_clicks = []
                else:
                    selected = (rank, file)
                    player_mouse_clicks.append(selected)
                if len(player_mouse_clicks) == 2:
                    move = engine.PieceMove(player_mouse_clicks[0], player_mouse_clicks[1], bs.board)
                    bs.make_move(move)
                    selected = ()
                    player_mouse_clicks = []
        draw_game(bs, screen)
        clock.tick(MAX_FPS)
        game.display.flip()


"""
Handles graphics of given board state
"""


def draw_game(bs, screen):
    draw_board(screen)
    draw_pieces(screen, bs.board)


"""
Helpers
"""


def draw_board(screen):
    colors = [game.Color("light yellow"), game.Color("dark green")]
    for r in range(DIMENSION):
        for f in range(DIMENSION):
            color = colors[(r + f) % 2]  # Dark squares will have a remainder 1
            game.draw.rect(screen, color, game.Rect(f*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for f in range(DIMENSION):
            piece = board[r][f]
            if piece != "..":
                screen.blit(IMAGES[piece], game.Rect(f * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


run_game()
