""" Handles user input and displaying game state at given time """

import pygame as game
import chessAI

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
    possible_moves = bs.get_valid_moves()
    move_made = False
    animate = False
    game_over = False
    player_one = True
    player_two = True
    start = True
    random_ai = False
    greedy_ai = False
    best_ai = False
    while playing:
        is_human_turn = (bs.white_to_move and player_one) or (not bs.white_to_move and player_two)
        for event in game.event.get():
            if event.type == game.QUIT:
                playing = False
            # handle mouse clicks
            elif event.type == game.MOUSEBUTTONDOWN:
                if not game_over and is_human_turn:
                    square = game.mouse.get_pos()
                    file = square[0] // SQUARE_SIZE
                    rank = square[1] // SQUARE_SIZE
                    if selected == (rank, file):
                        selected = ()
                        player_mouse_clicks = []
                    else:
                        selected = (rank, file)
                        player_mouse_clicks.append(selected)
                    if len(player_mouse_clicks) == 2:
                        move = engine.PieceMove(player_mouse_clicks[0], player_mouse_clicks[1], bs.board)
                        for m in possible_moves:
                            if move == m:
                                bs.make_move(m)
                                move_made = True
                                animate = True
                                selected = ()
                                player_mouse_clicks = []
                        if not move_made:
                            player_mouse_clicks = [selected]
            elif event.type == game.KEYDOWN:
                if event.key == game.K_u:
                    bs.undo_move()
                    move_made = True
                    animate = False
                    game_over = False
                if event.key == game.K_n:
                    bs = engine.BoardState()
                    possible_moves = bs.get_valid_moves()
                    selected = ()
                    player_mouse_clicks = []
                    move_made = False
                    animate = False
                    game_over = False

        # AI Move
        if not game_over and not is_human_turn:
            if best_ai:
                ai_move = chessAI.find_best_move(bs, possible_moves)
                if ai_move is None:
                    ai_move = chessAI.find_random_moves(possible_moves)
                bs.make_move(ai_move)
            if greedy_ai:
                ai_move = chessAI.find_greedy_move(bs, possible_moves)
                bs.make_move(ai_move)
            if random_ai:
                ai_move = chessAI.find_random_moves(possible_moves)
                bs.make_move(ai_move)

            move_made = True
            animate = True

        if move_made:
            if animate:
                animate_moves(bs.log[-1], screen, bs.board, clock)
            possible_moves = bs.get_valid_moves()
            move_made = False
            animate = False

        draw_game(bs, screen, possible_moves, selected)
        draw_checkmate_and_stalemate(screen, bs)
        game_over = draw_checkmate_and_stalemate(screen, bs)

        # if start:
        #     while True:
        #         draw_starting_menu(screen)
        #         for event in game.event.get():
        #             if event.type == game.KEYDOWN:
        #                 if event.key == game.K_1:
        #                     draw_ai_choice(screen)
        #                     player_two = False
        #                     if event.key == game.K_e:
        #                         random_ai = True
        #                     elif event.key == game.K_m:
        #                         greedy_ai = True
        #                     elif event.key == game.K_h:
        #                         best_ai = True
        #                 elif event.key == game.K_2:
        #                     draw_ai_choice(screen)
        #                     player_one = False
        #                     if event.key == game.K_e:
        #                         random_ai = True
        #                     elif event.key == game.K_m:
        #                         greedy_ai = True
        #                     elif event.key == game.K_h:
        #                         best_ai = True
        #             start = False

        clock.tick(MAX_FPS)
        game.display.flip()


"""
Handles graphics of given board state
"""


def draw_game(bs, screen, valid_moves, selected):
    draw_board(screen)
    highlight_squares(screen, bs, valid_moves, selected)
    draw_pieces(screen, bs.board)


"""
Helpers
"""


def draw_board(screen):
    global colors
    colors = [game.Color("light yellow"), game.Color("light gray")]
    for r in range(DIMENSION):
        for f in range(DIMENSION):
            color = colors[(r + f) % 2]  # Dark squares will have a remainder 1
            game.draw.rect(screen, color, game.Rect(f * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for f in range(DIMENSION):
            piece = board[r][f]
            if piece != "..":
                screen.blit(IMAGES[piece], game.Rect(f * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_text(screen, text):
    font = game.font.SysFont("Times New Roman", 32, True, False)
    text_object = font.render(text, False, game.Color("Gray"))
    text_location = game.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                        HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, game.Color("Black"))
    screen.blit(text_object, text_location.move(2, 2))


def draw_checkmate_and_stalemate(screen, bs):
    if bs.check_mate:
        if bs.white_to_move:
            draw_text(screen, "Black Wins: Checkmate")
        else:
            draw_text(screen, "White Wins: Checkmate")
        return True
    elif bs.stale_mate:
        draw_text(screen, "Stalemate")
        return True
    return False


def draw_starting_menu(screen):
    font = game.font.SysFont("Times New Roman", 40, True, False)
    text_object1 = font.render("Press 1 For Playing as White", False, game.Color("Black"))
    text_location1 = game.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object1.get_width() / 1.95,
                                                         text_object1.get_height()*7)
    screen.blit(text_object1, text_location1)
    text_object2 = font.render("Press 2 For Playing as Black", False, game.Color("Black"))
    text_location2 = game.Rect(SQUARE_SIZE, SQUARE_SIZE, WIDTH, HEIGHT).move(WIDTH / 2 - text_object1.get_width()/1.57,
                                                                             text_object1.get_height()*4)
    screen.blit(text_object2, text_location2)

    text_object3 = font.render("Press 3 For Two Player Game", False, game.Color("Black"))
    text_location3 = game.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object1.get_width() / 1.9,
                                                         text_object1.get_height()*4)
    screen.blit(text_object3, text_location3)

def draw_ai_choice(screen):
    font = game.font.SysFont("Times New Roman", 40, True, False)
    text_object1 = font.render("Press E For Easy Difficulty", False, game.Color("Black"))
    text_location1 = game.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object1.get_width() / 1.95,
                                                         text_object1.get_height() * 7)
    screen.blit(text_object1, text_location1)
    text_object2 = font.render("Press M For Medium Difficulty", False, game.Color("Black"))
    text_location2 = game.Rect(SQUARE_SIZE, SQUARE_SIZE, WIDTH, HEIGHT).move(
        WIDTH / 2 - text_object1.get_width() / 1.57,
        text_object1.get_height() * 4)
    screen.blit(text_object2, text_location2)

    text_object3 = font.render("Press H for Hard Difficulty", False, game.Color("Black"))
    text_location3 = game.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object1.get_width() / 1.9,
                                                         text_object1.get_height() * 4)
    screen.blit(text_object3, text_location3)

"""
Highlights Squares
"""


def highlight_squares(screen, bs, valid_moves, selected):
    if selected != ():
        r, f = selected
        if bs.board[r][f][0] == ('w' if bs.white_to_move else 'b'):
            s = game.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(game.Color('purple'))
            screen.blit(s, (f * SQUARE_SIZE, r * SQUARE_SIZE))
            s.fill(game.Color('yellow'))
            for piecemove in valid_moves:
                if piecemove.start_rank == r and piecemove.start_file == f:
                    screen.blit(s, (SQUARE_SIZE * piecemove.end_file, SQUARE_SIZE * piecemove.end_rank))


"""
Animating moves
"""


def animate_moves(piecemove, screen, board, clock):
    global colors
    coordinates = []
    diff_rank = piecemove.end_rank - piecemove.start_rank
    diff_file = piecemove.end_file - piecemove.start_file
    frames_per_square = 5
    frame_count = (abs(diff_rank) + abs(diff_file)) * frames_per_square
    for frame in range(frame_count + 1):
        r, f = piecemove.start_rank + diff_rank * frame / frame_count, piecemove.start_file + diff_file * frame / frame_count
        draw_board(screen)
        draw_pieces(screen, board)
        color = colors[(piecemove.end_rank + piecemove.end_file) % 2]
        end_square = game.Rect(piecemove.end_file * SQUARE_SIZE, piecemove.end_rank * SQUARE_SIZE, SQUARE_SIZE,
                               SQUARE_SIZE)
        game.draw.rect(screen, color, end_square)
        if piecemove.piece_captured != "..":
            screen.blit(IMAGES[piecemove.piece_captured], end_square)
        screen.blit(IMAGES[piecemove.piece_moved],
                    game.Rect(f * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        game.display.flip()
        clock.tick(60)


# Run Game
run_game()
