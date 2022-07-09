import random
import engine

CHECKMATE = 999
STALEMATE = 0
piece_scores = {'p': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9, 'K': 0}
DEPTH = 3

# Returns random move
def find_random_moves(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves)-1)]

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
            score = find_best_move(bs, next_moves, depth - 1, False)
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
            score = find_best_move(bs, next_moves, depth - 1, True)
            if score < min_score:
                max_score = score
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
    if bs.check_mate:
        if bs.white_to_move:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif bs.stale_mate:
        return STALEMATE

    score = 0
    for rank in bs.board:
        for square in rank:
            if square[0] == 'w':
                score += piece_scores[square[1]]
            elif square[0] == 'b':
                score -= piece_scores[square[1]]

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
