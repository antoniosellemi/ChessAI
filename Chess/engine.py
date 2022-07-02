""" Handles storing information on game state, logs moves, determines valid moves """


class BoardState():
    def __init__(self):
        # bR = black rook, rest follow same formatting, ".." signifies empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["..", "..", "..", "..", "..", "..", "..", ".."],
            ["..", "..", "..", "..", "..", "..", "..", ".."],
            ["..", "..", "..", "..", "..", "..", "..", ".."],
            ["..", "..", "..", "..", "..", "..", "..", ".."],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.log = []
        self.white_to_move = True

    def make_move(self, piecemove):
        self.board[piecemove.start_rank][piecemove.start_file] = ".."
        self.board[piecemove.end_rank][piecemove.end_file] = piecemove.piece_moved
        self.log.append(piecemove)
        self.white_to_move = not self.white_to_move

class PieceMove():
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"h": 7, "g": 6, "f": 5, "e": 4, "d": 3, "c": 2, "b": 1, "a": 0}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_rank = start_sq[0]
        self.start_file = start_sq[1]
        self.end_rank = end_sq[0]
        self.end_file = end_sq[1]
        self.piece_moved = board[self.start_rank][self.start_file]
        self.piece_captured = board[self.end_rank][self.end_file]

    def get_chess_notation_square(self):
        return self.get_rank_and_file(self.start_rank, self.start_file) + self.get_rank_and_file(self.end_file, self.end_file)

    def get_rank_and_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]