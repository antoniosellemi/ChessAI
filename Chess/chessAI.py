import random
import engine

CHECKMATE = 999
STALEMATE = 0
piece_scores = {'p': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9, 'K': 0}
knight_scores = [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]]
bishop_scores = [[4, 3, 2, 1, 1, 2, 3, 4],
                 [3, 4, 3, 2, 2, 3, 4, 3],
                 [2, 3, 4, 3, 3, 4, 3, 2],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 4, 4, 4, 3, 2, 1],
                 [2, 3, 4, 3, 3, 4, 3, 2],
                 [3, 4, 3, 2, 2, 3, 4, 3],
                 [4, 3, 2, 1, 1, 2, 3, 4]]
queen_scores = [[1, 1, 1, 3, 1, 1, 1, 1],
                [1, 2, 3, 3, 3, 1, 1, 1],
                [1, 4, 3, 3, 3, 4, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 4, 3, 3, 3, 4, 2, 1],
                [1, 1, 2, 3, 3, 1, 1, 1],
                [1, 1, 1, 3, 1, 1, 1, 1]]
rook_scores = [[4, 3, 4, 4, 4, 4, 3, 4],
               [4, 4, 4, 4, 4, 4, 4, 4],
               [1, 1, 2, 3, 3, 2, 1, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 1, 2, 2, 2, 2, 1, 1],
               [4, 4, 4, 4, 4, 4, 4, 4],
               [4, 3, 4, 4, 4, 4, 3, 4]]
white_pawn_scores = [[9, 9, 9, 9, 9, 9, 9, 9],
                     [8, 8, 8, 8, 8, 8, 8, 8],
                     [5, 6, 6, 7, 7, 6, 6, 5],
                     [2, 3, 3, 5, 5, 3, 3, 2],
                     [1, 2, 3, 4, 4, 3, 2, 1],
                     [1, 1, 2, 3, 3, 2, 1, 1],
                     [1, 1, 1, 0, 0, 1, 1, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0]]

black_pawn_scores = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 1, 0, 0, 1, 1, 1],
                     [1, 1, 2, 3, 3, 2, 1, 1],
                     [1, 2, 3, 4, 4, 3, 2, 1],
                     [2, 3, 3, 5, 5, 3, 3, 2],
                     [5, 6, 6, 7, 7, 6, 6, 5],
                     [8, 8, 8, 8, 8, 8, 8, 8],
                     [9, 9, 9, 9, 9, 9, 9, 9]]
king_scores = [[1, 5, 2, 0, 5, 0, 7, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [1, 5, 2, 0, 5, 0, 7, 0]]

piece_position_scores = {"wp": white_pawn_scores, "bp": black_pawn_scores, "R": rook_scores, "N": knight_scores,
                         "B": bishop_scores, "Q": queen_scores, "K": king_scores}
DEPTH = 4


# Returns random move
def find_random_moves(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


# Find best move based on material alone, greedy algorithm
def find_greedy_move(bs, valid_moves):
    turn = 1 if bs.white_to_move else -1
    opponent_min_max_score = CHECKMATE
    best_player_move = None
    random.shuffle(valid_moves)
    for player_move in valid_moves:
        bs.make_move(player_move)
        opponent_moves = bs.get_valid_moves()
        if bs.stale_mate:
            opponent_max_score = STALEMATE
        elif bs.check_mate:
            opponent_max_score = -CHECKMATE
        else:
            opponent_max_score = -CHECKMATE
            for op_move in opponent_moves:
                bs.make_move(op_move)
                bs.get_valid_moves()
                if bs.check_mate:
                    score = CHECKMATE
                elif bs.stale_mate:
                    score = STALEMATE
                else:
                    score = -turn * material_score(bs.board)
                if score > opponent_max_score:
                    opponent_max_score = score
                bs.undo_move()
        if opponent_max_score < opponent_min_max_score:
            opponent_min_max_score = opponent_max_score
            best_player_move = player_move
        bs.undo_move()

    return best_player_move


# Helper for find best move first recursive call
def find_best_move(bs, valid_moves):
    global next_move
    random.shuffle(valid_moves)
    next_move = None
    find_move_nega_max_alpha_beta(bs, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if bs.white_to_move else -1)
    return next_move


# Implements min max algorithm
def find_best_move_min_max(bs, valid_moves, depth, white_to_move):
    global next_move
    if depth == 0:
        return material_score(bs.board)
    if white_to_move:
        max_score = -CHECKMATE
        for move in valid_moves:
            bs.make_move(move)
            next_moves = bs.get_valid_moves()
            score = find_move_nega_max(bs, next_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            bs.undo_move()
        return max_score
    else:
        min_score = CHECKMATE
        for move in valid_moves:
            bs.make_move(move)
            next_moves = bs.get_valid_moves()
            score = find_move_nega_max(bs, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            bs.undo_move()
        return min_score


def find_move_nega_max(bs, valid_moves, depth, turn):
    global next_move
    if depth == 0:
        return turn * score_board(bs)
    max_score = -CHECKMATE
    for move in valid_moves:
        bs.make_move(move)
        next_moves = bs.get_valid_moves()
        score = -find_move_nega_max(bs, next_moves, depth - 1, -turn)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        bs.undo_move()
    return max_score


def find_move_nega_max_alpha_beta(bs, valid_moves, depth, alpha, beta, turn):
    global next_move
    if depth == 0:
        return turn * score_board(bs)

    max_score = -CHECKMATE
    for move in valid_moves:
        bs.make_move(move)
        next_moves = bs.get_valid_moves()
        score = -find_move_nega_max_alpha_beta(bs, next_moves, depth - 1, -beta, -alpha, -turn)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        bs.undo_move()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


# Helpers

# More intuitive scoring method, positive is good for white
def score_board(bs):
    global piece_position_score
    if bs.check_mate:
        if bs.white_to_move:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif bs.stale_mate:
        return STALEMATE

    score = 0
    for rank in range(len(bs.board)):
        for file in range(len(bs.board[rank])):
            square = bs.board[rank][file]
            if square != "..":
                if square[1] == "p":
                    piece_position_score = piece_position_scores[square][rank][file]
                else:
                    piece_position_score = piece_position_scores[square[1]][rank][file]
            if square[0] == 'w':
                score += piece_scores[square[1]] + piece_position_score * .1
            elif square[0] == 'b':
                score -= piece_scores[square[1]] + piece_position_score * .1

    return score


# Score board based on material on board
def material_score(board):
    score = 0
    for rank in board:
        for square in rank:
            if square[0] == 'w':
                score += piece_scores[square[1]]
            elif square[0] == 'b':
                score -= piece_scores[square[1]]

    return score
