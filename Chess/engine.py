""" Handles storing information on game state, logs moves, determines valid moves """


# Class Defining Board State
class BoardState:
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
        self.move_dictionary = {'p': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                                'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.log = []
        self.white_to_move = True
        self.in_check = False
        self.white_king = (7, 4)
        self.black_king = (0, 4)
        self.pins = []
        self.checks = []
        self.check_mate = False
        self.stale_mate = False
        self.enpassant_move = ()
        self.current_castling_right = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.current_castling_right.wks, self.current_castling_right.bks,
                                               self.current_castling_right.wqs, self.current_castling_right.bqs)]

    # Updates board state based on move made
    def make_move(self, piecemove):
        self.board[piecemove.start_rank][piecemove.start_file] = ".."
        self.board[piecemove.end_rank][piecemove.end_file] = piecemove.piece_moved
        self.log.append(piecemove)
        self.white_to_move = not self.white_to_move
        if piecemove.piece_moved == "wK":
            self.white_king = (piecemove.end_rank, piecemove.end_file)
        elif piecemove.piece_moved == "bK":
            self.black_king = (piecemove.end_rank, piecemove.end_file)

        # Pawn promotion
        if piecemove.is_pawn_promotion:
            self.board[piecemove.end_rank][piecemove.end_file] = piecemove.piece_moved[0] + 'Q'

        # Enpassant
        if piecemove.is_en_passant:
            self.board[piecemove.start_rank][piecemove.end_file] = '..'

        if piecemove.piece_moved[1] == 'p' and abs(piecemove.start_rank - piecemove.end_rank) == 2:
            self.enpassant_move = ((piecemove.start_rank + piecemove.end_rank) // 2, piecemove.start_file)
        else:
            self.enpassant_move = ()

        # Castling Rights
        self.update_castle_rights(piecemove)
        self.castle_rights_log.append(CastleRights(self.current_castling_right.wks, self.current_castling_right.bks,
                                                   self.current_castling_right.wqs, self.current_castling_right.bqs))

        if piecemove.is_castle_move:
            if piecemove.end_file - piecemove.start_file == 2:  # Kingside castle
                self.board[piecemove.end_rank][piecemove.end_file - 1] = self.board[piecemove.end_rank][
                    piecemove.end_file + 1]
                self.board[piecemove.end_rank][piecemove.end_file + 1] = ".."
            else:
                self.board[piecemove.end_rank][piecemove.end_file + 1] = self.board[piecemove.end_rank][
                    piecemove.end_file - 2]
                self.board[piecemove.end_rank][piecemove.end_file - 2] = ".."

    # Undo a move by clicking u on the keyboard
    def undo_move(self):
        # Makes sure there is a move to undo
        if len(self.log) != 0:
            piecemove = self.log.pop()
            self.board[piecemove.start_rank][piecemove.start_file] = piecemove.piece_moved
            self.board[piecemove.end_rank][piecemove.end_file] = piecemove.piece_captured
            self.white_to_move = not self.white_to_move
            # Updates king location in case of undoing king moves
            if piecemove.piece_moved == "wK":
                self.white_king = (piecemove.start_rank, piecemove.start_file)
            elif piecemove.piece_moved == "bK":
                self.black_king = (piecemove.start_rank, piecemove.start_file)
            # Undo enpassant
            if piecemove.is_en_passant:
                self.board[piecemove.end_rank][piecemove.end_file] = ".."
                self.board[piecemove.start_rank][piecemove.end_file] = piecemove.piece_captured
                self.en_passant_possible = (piecemove.end_rank, piecemove.end_file)
            # Undo two square advance
            if piecemove.piece_moved[1] == 'p' and abs(piecemove.end_rank - piecemove.start_rank) == 2:
                self.en_passant_possible = ()
            # Undo castling rights
            self.castle_rights_log.pop()
            self.current_castling_right = self.castle_rights_log[-1]
            # Undo castle move
            if piecemove.is_castle_move:
                if piecemove.end_file - piecemove.start_file == 2:
                    self.board[piecemove.end_rank][piecemove.end_file + 1] = self.board[piecemove.end_rank][
                        piecemove.end_file - 1]
                    self.board[piecemove.end_rank][piecemove.end_file - 1] = ".."
                else:
                    self.board[piecemove.end_rank][piecemove.end_file - 2] = self.board[piecemove.end_rank][
                        piecemove.end_file + 1]
                    self.board[piecemove.end_rank][piecemove.end_file + 1] = ".."

            self.check_mate = False
            self.stale_mate = False

    # Update castling rights given move
    def update_castle_rights(self, piecemove):
        if piecemove.piece_moved == 'wK':  # If white king moved
            self.current_castling_right.wks = False
            self.current_castling_right.wqs = False
        elif piecemove.piece_moved == 'bK':
            self.current_castling_right.bks = False
            self.current_castling_right.bqs = False
        elif piecemove.piece_moved == 'wR':  # If white rook moved
            if piecemove.start_rank == 7:
                if piecemove.start_file == 0:
                    self.current_castling_right.wqs = False
                elif piecemove.start_file == 7:
                    self.current_castling_right.wks = False
        elif piecemove.piece_moved == 'bR':
            if piecemove.start_rank == 0:
                if piecemove.start_file == 0:
                    self.current_castling_right.bqs = False
                elif piecemove.start_file == 7:
                    self.current_castling_right.bks = False
        # If Rook is captured
        if piecemove.piece_captured == 'wR':
            if piecemove.end_rank == 7:
                if piecemove.end_file == 0:
                    self.current_castling_right.wqs = False
                elif piecemove.end_file == 7:
                    self.current_castling_right.wks = False
        elif piecemove.piece_captured == 'bR':
            if piecemove.end_rank == 0:
                if piecemove.end_file == 0:
                    self.current_castling_right.bqs = False
                elif piecemove.end_file == 7:
                    self.current_castling_right.bks = False

    # Get all the valid moves based on the board state, including checks and pins
    def get_valid_moves(self):
        temp_enpassant = self.enpassant_move  # Storing this because our method might change this, we want to conserve it
        temp_castle_rights = CastleRights(self.current_castling_right.wks, self.current_castling_right.bks,
                                          self.current_castling_right.wqs, self.current_castling_right.bqs)
        valid_moves = []
        self.in_check, self.pins, self.checks = self.pins_and_checks()
        if self.white_to_move:
            king_rank, king_file = self.white_king
        else:
            king_rank, king_file = self.black_king
        if self.in_check:
            # Moves if only one piece is putting the king in check
            if len(self.checks) == 1:
                moves = self.get_all_possible_moves()
                check = self.checks[0]
                check_rank, check_file, check_rank_dir, check_file_dir = check
                piece_putting_check = self.board[check_rank][check_file]
                possible_squares = []
                # If a knight is checking, then no blocking is possible, you can only capture the knight
                if piece_putting_check[1] == 'N':
                    possible_squares = [(check_rank, check_file)]
                # Any other piece is checking
                else:
                    for i in range(1, 8):
                        # Can block by moving any piece in the check direction up to the check piece
                        possible_square = (king_rank + check_rank_dir * i, king_file + check_file_dir * i)
                        possible_squares.append(possible_square)
                        if possible_square[0] == check_rank and possible_square[1] == check_file:
                            break
                # Remove from all possible moves, ones that are not valid given a check
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != 'K':
                        if not (moves[i].end_rank, moves[i].end_file) in possible_squares:
                            moves.remove(moves[i])
                valid_moves = moves
            # If multiple checks (double checks) then the king needs to move
            else:
                self.get_king_moves(king_rank, king_file, valid_moves)
        # No checks mean all moves that are possible are valid
        else:
            valid_moves = self.get_all_possible_moves()
            if self.white_to_move:
                self.get_castle_moves(self.white_king[0], self.white_king[1], valid_moves)
            else:
                self.get_castle_moves(self.black_king[0], self.black_king[1], valid_moves)

        if len(valid_moves) == 0:
            if self.in_check:
                self.check_mate = True
            else:
                self.stale_mate = True

        self.enpassant_move = temp_enpassant
        self.current_castling_right = temp_castle_rights
        return valid_moves

    # Get all possible moves based on piece
    def get_all_possible_moves(self):
        valid_moves = []
        for r in range(len(self.board)):
            for f in range(len(self.board[r])):
                turn = self.board[r][f][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[r][f][1]
                    self.move_dictionary[piece](r, f, valid_moves)
        return valid_moves

    # Get all possible pawn moves including if pinned
    def get_pawn_moves(self, r, f, valid_moves):
        # Check if a pawn is pinned, and if so get the direction of the pin
        pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == f:
                pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])  # Remove from total pins the one given by this pawn
                break
        if self.white_to_move:
            move_amount = -1
            start_row = 6
            enemy_color = 'b'
            king_rank, king_file = self.white_king
        else:
            move_amount = 1
            start_row = 1
            enemy_color = 'w'
            king_rank, king_file = self.black_king

        # One square, two square moves
        if self.board[r + move_amount][f] == "..":
            if not pinned or pin_direction == (move_amount, 0):
                valid_moves.append(PieceMove((r, f), (r + move_amount, f), self.board))
                if r == start_row and self.board[r + 2 * move_amount][f] == "..":
                    valid_moves.append(PieceMove((r, f), (r + 2 * move_amount, f), self.board))
        # Left capture
        if f - 1 >= 0:
            if not pinned or pin_direction == (move_amount, -1):
                if self.board[r + move_amount][f - 1][0] == enemy_color:
                    valid_moves.append(PieceMove((r, f), (r + move_amount, f - 1), self.board))
                if (r + move_amount, f - 1) == self.enpassant_move:
                    attacking_piece = blocking_piece = False
                    if king_rank == r:
                        if king_file < f:  # King is left of pawn
                            inside = range(king_file + 1, f - 1)
                            outside = range(f + 1, 8)
                        else:
                            inside = range(king_file - 1, f, -1)
                            outside = range(f - 2, -1, -1)
                        for i in inside:
                            if self.board[r][i] != "..":  # Some piece is blocking
                                blocking_piece = True
                        for i in outside:
                            square = self.board[r][i]
                            if square[0] == enemy_color and (square[1] == 'R' or square[1] == 'Q'):
                                attacking_piece = True
                            elif square != "..":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        valid_moves.append(PieceMove((r, f), (r + move_amount, f - 1), self.board, en_passant_possible=True))
        # Right capture
        if f + 1 <= 7:
            if not pinned or pin_direction == (move_amount, 1):
                if self.board[r + move_amount][f + 1][0] == enemy_color:
                    valid_moves.append(PieceMove((r, f), (r + move_amount, f + 1), self.board))
                if (r + move_amount, f + 1) == self.enpassant_move:
                    attacking_piece = blocking_piece = False
                    if king_rank == r:
                        if king_file > f:  # King is left of pawn
                            inside = range(king_file + 1, f)
                            outside = range(f + 2, 8)
                        else:
                            inside = range(king_file - 1, f + 1, -1)
                            outside = range(f - 1, -1, -1)
                        for i in inside:
                            if self.board[r][i] != "..":  # Some piece is blocking
                                blocking_piece = True
                        for i in outside:
                            square = self.board[r][i]
                            if square[0] == enemy_color and (square[1] == 'R' or square[1] == 'Q'):
                                attacking_piece = True
                            elif square != "..":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        valid_moves.append(PieceMove((r, f), (r + move_amount, f - 1), self.board, en_passant_possible=True))

        return valid_moves

    # Get all rook moves including if pinned
    def get_rook_moves(self, r, f, valid_moves):
        # Check if rook is pinned, and if so remove it from total pins
        pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == f:
                pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][f][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))  # Unit vector rook movement
        opponent_color = 'b' if self.white_to_move else 'w'
        # Deal with rook movement in each direction
        for direction in directions:
            for i in range(1, 8):
                end_rank = r + direction[0] * i
                end_file = f + direction[1] * i
                if 0 <= end_rank <= 7 and 0 <= end_file <= 7:
                    if not pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_rank][end_file]
                        if end_piece == "..":
                            valid_moves.append(PieceMove((r, f), (end_rank, end_file), self.board))
                        elif end_piece[0] == opponent_color:
                            valid_moves.append(PieceMove((r, f), (end_rank, end_file), self.board))
                            break
                        else:
                            break
                else:
                    break
        return valid_moves

    # Get all knight moves including if pinned
    def get_knight_moves(self, r, f, valid_moves):
        # Check if knight is pinned, if so remove it from total pins
        pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == f:
                pinned = True
                self.pins.remove(self.pins[i])
                break

        directions = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2))  # Vector for knight moves
        ally_color = 'w' if self.white_to_move else 'b'
        # Get all knight moves for each direction
        for direction in directions:
            end_rank = r + direction[0]
            end_file = f + direction[1]
            if 0 <= end_rank <= 7 and 0 <= end_file <= 7:
                if not pinned:
                    end_piece = self.board[end_rank][end_file]
                    if end_piece[0] != ally_color:
                        valid_moves.append(PieceMove((r, f), (end_rank, end_file), self.board))
        return valid_moves

    # Get all bishop moves including if pinned
    def get_bishop_moves(self, r, f, valid_moves):
        # Check if bishop is pinned, if so remove it from total pins
        pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == f:
                pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (1, -1), (1, 1), (-1, 1))  # Vectors for bishop directions
        opponent_color = 'b' if self.white_to_move else 'w'
        # Check bishop moves in each direction
        for direction in directions:
            for i in range(1, 8):
                end_rank = r + direction[0] * i
                end_file = f + direction[1] * i
                if 0 <= end_rank <= 7 and 0 <= end_file <= 7:
                    if not pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_rank][end_file]
                        if end_piece == "..":
                            valid_moves.append(PieceMove((r, f), (end_rank, end_file), self.board))
                        elif end_piece[0] == opponent_color:
                            valid_moves.append(PieceMove((r, f), (end_rank, end_file), self.board))
                            break
                        else:
                            break
                else:
                    break
        return valid_moves

    # Get all queen moves (is exactly rook and bishop combined)
    def get_queen_moves(self, r, f, valid_moves):
        self.get_rook_moves(r, f, valid_moves)
        self.get_bishop_moves(r, f, valid_moves)

    # Get all possible king moves
    def get_king_moves(self, r, f, valid_moves):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (1, 1), (-1, 1))
        ally_color = 'w' if self.white_to_move else 'b'
        for direction in directions:
            end_rank = r + direction[0]
            end_file = f + direction[1]
            if 0 <= end_rank <= 7 and 0 <= end_file <= 7:
                end_piece = self.board[end_rank][end_file]
                if end_piece[0] != ally_color:
                    # Move king temporarily to square being considered, if not in check then add that to possible moves
                    if ally_color == 'w':
                        self.white_king = (end_rank, end_file)
                    else:
                        self.black_king = (end_rank, end_file)
                    in_check, pins, checks = self.pins_and_checks()
                    if not in_check:
                        valid_moves.append(PieceMove((r, f), (end_rank, end_file), self.board))
                    if ally_color == 'w':
                        self.white_king = (r, f)
                    else:
                        self.black_king = (r, f)

        return valid_moves

    # Get moves for castling if possible
    def get_castle_moves(self, r, f, moves):
        if self.square_under_attack(r, f):
            return
        if (self.current_castling_right.wks and self.white_to_move) or (
                self.current_castling_right.bks and not self.white_to_move):
            self.get_king_side_castle_moves(r, f, moves)
        if (self.current_castling_right.wqs and self.white_to_move) or (
                self.current_castling_right.bqs and not self.white_to_move):
            self.get_queen_side_castle_moves(r, f, moves)

    # Add king side castle moves
    def get_king_side_castle_moves(self, r, f, moves):
        if self.board[r][f + 1] == ".." and self.board[r][f + 2] == "..":
            if not self.square_under_attack(r, f + 1) and not self.square_under_attack(r, f + 2):
                moves.append(PieceMove((r, f), (r, f + 2), self.board, is_castle=True))

    # Add queen side castle moves
    def get_queen_side_castle_moves(self, r, f, moves):
        if self.board[r][f - 1] == ".." and self.board[r][f - 2] == ".." and self.board[r][f - 3] == "..":
            if not self.square_under_attack(r, f - 1) and not self.square_under_attack(r, f - 2):
                moves.append(PieceMove((r, f), (r, f - 2), self.board, is_castle=True))

    # Checks for all pins and checks for a given board state
    def pins_and_checks(self):
        pins = []
        checks = []
        in_check = False
        if self.white_to_move:
            opponent_color = 'b'
            ally_color = 'w'
            start_rank = self.white_king[0]
            start_file = self.white_king[1]
        else:
            opponent_color = 'w'
            ally_color = 'b'
            start_rank = self.black_king[0]
            start_file = self.black_king[1]
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        # Check in all directions for pins and checks
        for i, direction in enumerate(directions):
            poss_pins = ()
            # Check all the way in each direction until an allied piece, enemy piece, or end of board
            for j in range(1, 8):
                end_rank = start_rank + direction[0] * j
                end_file = start_file + direction[1] * j
                if 0 <= end_rank <= 7 and 0 <= end_file <= 7:
                    end_piece = self.board[end_rank][end_file]
                    if (end_piece[0] == ally_color) and (end_piece[1] != 'K'):  # King cannot be a pinned piece
                        if poss_pins == ():
                            poss_pins = (end_rank, end_file, direction[0], direction[1])
                        else:  # If there's already a piece pinned in this direction, we don't add it
                            break
                    # Check if piece in specific direction can actually check the king
                    elif end_piece[0] == opponent_color:
                        piece_type = end_piece[1]
                        if (0 <= i <= 3 and piece_type == 'R') or \
                                (4 <= i <= 7 and piece_type == 'B') or \
                                (j == 1 and piece_type == 'p' and ((opponent_color == 'w' and 6 <= i <= 7) or (
                                        opponent_color == 'b' and 4 <= i <= 5))) or \
                                (piece_type == 'Q') or (j == 1 and piece_type == 'K'):
                            if poss_pins == ():
                                in_check = True
                                checks.append((end_rank, end_file, direction[0], direction[1]))
                                break
                            else:
                                pins.append(poss_pins)
                                break
                        else:
                            break
                else:
                    break
        # Check if knight is checking the king
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for move in knight_moves:
            end_rank = start_rank + move[0]
            end_file = start_file + move[1]
            if 0 <= end_rank <= 7 and 0 <= end_file <= 7:
                end_piece = self.board[end_rank][end_file]
                if end_piece[0] == opponent_color and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_rank, end_file, move[0], move[1]))
        return in_check, pins, checks

    # Checks if king is in check
    def is_in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king[0], self.white_king[1])
        else:
            return self.square_under_attack(self.black_king[0], self.black_king[1])

    # Checks if a given square is under attack
    def square_under_attack(self, r, f):
        self.white_to_move = not self.white_to_move
        opponent_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for piecemove in opponent_moves:
            if piecemove.end_rank == r and piecemove.end_file == f:
                return True
        return False


# Class for defining a move
class PieceMove:
    # Dictionaries for translation from computer indices to chess notation and vice versa
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"h": 7, "g": 6, "f": 5, "e": 4, "d": 3, "c": 2, "b": 1, "a": 0}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, en_passant_possible=False, is_castle=False):
        self.start_rank = start_sq[0]
        self.start_file = start_sq[1]
        self.end_rank = end_sq[0]
        self.end_file = end_sq[1]
        self.piece_moved = board[self.start_rank][self.start_file]
        self.piece_captured = board[self.end_rank][self.end_file]
        # Sort of like a hash map for pieces
        self.move_id = self.start_rank * 1000 + self.start_file * 100 + self.end_rank * 10 + self.end_file
        self.is_pawn_promotion = ((self.piece_moved == 'wp' and self.end_rank == 0) or (
                self.piece_moved == 'bp' and self.end_rank == 7))
        self.is_en_passant = en_passant_possible
        if self.is_en_passant:
            self.piece_captured = 'wp' if self.piece_moved == 'bp' else 'bp'
        self.is_capture = self.piece_captured != ".."
        self.is_castle_move = is_castle

    def __eq__(self, other):
        if isinstance(other, PieceMove):
            return self.move_id == other.move_id
        return False

    def __str__(self):
        if self.is_castle_move:
            return "O-O" if self.end_file == 6 else "O-O-O"
        end_square = self.get_rank_and_file(self.end_rank, self.end_file)
        # Dealing with pawn moves and captures
        if self.piece_moved[1] == 'p':
            if self.is_capture:
                return self.cols_to_files[self.start_file] + "x" + end_square
            else:
                return end_square
        # Dealing with all other moves and captures
        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += 'x'
        return move_string + end_square

    def get_chess_notation(self):
        return self.get_rank_and_file(self.start_rank, self.start_file) + self.get_rank_and_file(self.end_file,
                                                                                                 self.end_file)

    def get_rank_and_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
