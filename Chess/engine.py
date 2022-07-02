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

    def undo_move(self):
        if len(self.log) != 0:
            piecemove = self.log.pop()
            self.board[piecemove.start_rank][piecemove.start_file] = piecemove.piece_moved
            self.board[piecemove.end_rank][piecemove.end_file] = piecemove.piece_captured
            self.white_to_move = not self.white_to_move

    def get_valid_moves(self):
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        valid_moves = []
        for r in range(len(self.board)):
            for f in range(len(self.board[r])):
                turn = self.board[r][f][0]
                if (turn == "w" and self.white_to_move) and (turn == "b" and not self.white_to_move):
                    piece = self.board[r][f][1]
                    if piece == "p":
                        self.get_pawn_moves()
                    elif piece == "R":
                        self.get_rook_moves()
                    elif piece == "N":
                        self.get_knight_moves()
                    elif piece == "B":
                        self.get_bishop_moves()
                    elif piece == "Q":
                        self.get_queen_moves()
                    elif piece == "K":
                        self.get_king_moves()
        return valid_moves

    def get_pawn_moves(self):
        pass



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
        self.move_id = self.start_rank * 1000 + self.start_file * 100 + self.end_rank * 10 + self.end_file

    def __eq__(self, other):
        if isinstance(other, PieceMove):
            return self.move_id == other.move_id
        return False


    def get_chess_notation_square(self):
        return self.get_rank_and_file(self.start_rank, self.start_file) + self.get_rank_and_file(self.end_file, self.end_file)

    def get_rank_and_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]