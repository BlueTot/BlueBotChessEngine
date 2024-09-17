import json
import os
import time

WP = """00000000
        11111111
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000"""

BP = """00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        11111111
        00000000"""

WN = """01000010
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000"""

BN = """00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        01000010"""

WB = """00100100
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000"""

BB = """00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        00100100"""

WR = """10000001
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000"""

BR = """00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        10000001"""

WQ = """00010000
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000"""

BQ = """00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        00010000"""

WK = """00001000
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000"""

BK = """00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        00000000
        00001000"""

PAWN = 2
KNIGHT = 3
BISHOP = 4
ROOK = 5
QUEEN = 6
KING = 7

WHITE = True
BLACK = False

files = ["a", "b", "c", "d", "e", "f", "g", "h"]


def str_to_bin64(s):
    total = 0
    for idx, val in enumerate(s):
        c = 63 - idx
        total += 2 ** c if val == "1" else 0
    return total


def ms_to_bin64(ms):
    return str_to_bin64("".join([line for line in ms.split()]))


def bin64_to_str(bin64):
    return str(bin(bin64))[2:].zfill(64)


def bsf(bin64):
    s = bin64_to_str(bin64)
    for idx in range(64):
        if s[idx] == "1":
            return idx
    return None


def bwn(bin64):
    return bin64 ^ (2 ** 64 - 1)


def bsr(bin64):
    s = bin64_to_str(bin64)
    for idx in range(63, -1, -1):
        if s[idx] == "1":
            return idx
    return None


def print_bb(bb):
    s = bin64_to_str(bb)
    for c, char in enumerate(s):
        print(char, end='')
        if (c + 1) % 8 == 0:
            print()


def rank(sq):
    return str(sq // 8 + 1)


def file(sq):
    return files[sq % 8]


def get_sq(f, r):
    return files.index(f) + (int(r) - 1) * 8


def open_json(file_name):
    with open(os.path.join(os.path.join(os.path.dirname(os.getcwd()), "movement_sqrs"), file_name)) as f:
        data = json.load(f)
    return dict(zip(map(int, data), data.values()))


PAWN_ATK_WHITE_SQRS = open_json("pawn_atk_white_sqrs.json")
PAWN_ATK_BLACK_SQRS = open_json("pawn_atk_black_sqrs.json")
KNIGHT_SQRS = open_json("knight_sqrs.json")
KING_SQRS = open_json("king_sqrs.json")
BISHOP_SQRS = open_json("bishop_sqrs.json")
ROOK_SQRS = open_json("rook_sqrs.json")

piece_chars = {PAWN: "P", KNIGHT: "N", BISHOP: "B", ROOK: "R", QUEEN: "Q", KING: "K"}


class Piece:
    def __init__(self, piece_type, colour):
        self.piece_type = piece_type
        self.colour = colour

    def __repr__(self):
        return piece_chars[self.piece_type] if self.colour else piece_chars[self.piece_type].lower()


class Move:
    def __init__(self, from_square, to_square, promotion=False):
        self.from_square = from_square
        self.to_square = to_square
        self.promotion = promotion

    def uci(self):
        return file(self.from_square) + rank(self.from_square) + file(self.to_square) + rank(self.to_square)

    def __repr__(self):
        return self.uci()

    @staticmethod
    def from_uci(uci):
        return Move(get_sq(uci[0], uci[1]), get_sq(uci[2], uci[3]))


class Board:

    def __init__(self):
        self.__WP_BB = ms_to_bin64(WP)
        self.__BP_BB = ms_to_bin64(BP)

        self.__WN_BB = ms_to_bin64(WN)
        self.__BN_BB = ms_to_bin64(BN)

        self.__WB_BB = ms_to_bin64(WB)
        self.__BB_BB = ms_to_bin64(BB)

        self.__WR_BB = ms_to_bin64(WR)
        self.__BR_BB = ms_to_bin64(BR)

        self.__WQ_BB = ms_to_bin64(WQ)
        self.__BQ_BB = ms_to_bin64(BQ)

        self.__WK_BB = ms_to_bin64(WK)
        self.__BK_BB = ms_to_bin64(BK)

        self.__turn = WHITE

        self.__move_stack = {}

    def __empty_squares(self):
        return bwn(self.__blockers())

    def __blockers(self):
        whites = self.__WP_BB | self.__WN_BB | self.__WB_BB | self.__WR_BB | self.__WQ_BB | self.__WK_BB
        blacks = self.__BP_BB | self.__BN_BB | self.__BB_BB | self.__BR_BB | self.__BQ_BB | self.__BK_BB
        return whites | blacks

    def __masked_blockers(self, mask):
        return self.__blockers() & mask

    def __enemy_squares(self):
        if self.__turn:
            return self.__BP_BB | self.__BN_BB | self.__BB_BB | self.__BR_BB | self.__BQ_BB | self.__BK_BB
        else:
            return self.__WP_BB | self.__WN_BB | self.__WB_BB | self.__WR_BB | self.__WQ_BB | self.__WK_BB

    def __pawn_squares(self, ranks):
        bb = self.__WP_BB if self.__turn else self.__BP_BB
        bb = bb >> 8 * ranks if self.__turn else bb << 8 * ranks
        return bb & self.__empty_squares()

    def __pawn_atk_squares(self, sq):
        if self.__turn:
            return PAWN_ATK_WHITE_SQRS[sq] & self.__enemy_squares()
        else:
            return PAWN_ATK_BLACK_SQRS[sq] & self.__enemy_squares()

    def __knight_squares(self, sq):
        return KNIGHT_SQRS[sq] & (self.__empty_squares() | self.__enemy_squares())

    def __king_squares(self, sq):
        return KING_SQRS[sq] & (self.__empty_squares() | self.__enemy_squares())

    def __bishop_squares(self, sq):

        # North-west
        nw_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["NW"])
        blocker = bsr(nw_blockers)
        nw_sqrs = BISHOP_SQRS[sq]["NW"] & bwn(BISHOP_SQRS[blocker]["NW"] if blocker is not None else 0)

        # North-east
        ne_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["NE"])
        blocker = bsr(ne_blockers)
        ne_sqrs = BISHOP_SQRS[sq]["NE"] & bwn(BISHOP_SQRS[blocker]["NE"] if blocker is not None else 0)

        # South-west
        sw_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["SW"])
        blocker = bsf(sw_blockers)
        sw_sqrs = BISHOP_SQRS[sq]["SW"] & bwn(BISHOP_SQRS[blocker]["SW"] if blocker is not None else 0)

        # South-east
        se_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["SE"])
        blocker = bsf(se_blockers)
        se_sqrs = BISHOP_SQRS[sq]["SE"] & bwn(BISHOP_SQRS[blocker]["SE"] if blocker is not None else 0)

        return (self.__enemy_squares() | self.__empty_squares()) & (nw_sqrs | ne_sqrs | sw_sqrs | se_sqrs)

    def __rook_squares(self, sq):

        # North
        n_blockers = self.__masked_blockers(ROOK_SQRS[sq]["N"])
        blocker = bsr(n_blockers)
        n_sqrs = ROOK_SQRS[sq]["N"] & bwn(ROOK_SQRS[blocker]["N"] if blocker is not None else 0)

        # East
        e_blockers = self.__masked_blockers(ROOK_SQRS[sq]["E"])
        blocker = bsf(e_blockers)
        e_sqrs = ROOK_SQRS[sq]["E"] & bwn(ROOK_SQRS[blocker]["E"] if blocker is not None else 0)

        # South
        s_blockers = self.__masked_blockers(ROOK_SQRS[sq]["S"])
        blocker = bsf(s_blockers)
        s_sqrs = ROOK_SQRS[sq]["S"] & bwn(ROOK_SQRS[blocker]["S"] if blocker is not None else 0)

        # West
        w_blockers = self.__masked_blockers(ROOK_SQRS[sq]["W"])
        blocker = bsr(w_blockers)
        w_sqrs = ROOK_SQRS[sq]["W"] & bwn(ROOK_SQRS[blocker]["W"] if blocker is not None else 0)

        return (self.__enemy_squares() | self.__empty_squares()) & (n_sqrs | e_sqrs | s_sqrs | w_sqrs)

    def __queen_squares(self, sq):
        return self.__bishop_squares(sq) | self.__rook_squares(sq)

    @staticmethod
    def __squares_from(bb):
        for sq, bit in enumerate(bin64_to_str(bb)):
            if bit == "1":
                yield sq

    def generate_pawn_moves(self):
        moves = []

        # Normal push
        for sq in self.__squares_from(self.__pawn_squares(1)):
            orig_sq = sq - 8 if self.__turn else sq + 8
            moves.append(Move(orig_sq, sq))

        # Double push
        for sq in self.__squares_from(self.__pawn_squares(2)):
            orig_sq = sq - 16 if self.__turn else sq + 16
            if self.__turn and rank(orig_sq) == "2" or not self.__turn and rank(orig_sq) == "7":
                moves.append(Move(orig_sq, sq))

        # Captures
        for Psq in self.__squares_from(self.__WP_BB if self.__turn else self.__BP_BB):
            for sq in self.__squares_from(self.__pawn_atk_squares(Psq)):
                moves.append(Move(Psq, sq))

        return moves

    def generate_knight_moves(self):
        moves = []

        for Nsq in self.__squares_from(self.__WN_BB if self.__turn else self.__BN_BB):
            for sq in self.__squares_from(self.__knight_squares(Nsq)):
                moves.append(Move(Nsq, sq))

        return moves

    def generate_king_moves(self):
        moves = []

        for Ksq in self.__squares_from(self.__WK_BB if self.__turn else self.__BK_BB):
            for sq in self.__squares_from(self.__king_squares(Ksq)):
                moves.append(Move(Ksq, sq))

        return moves

    def generate_bishop_moves(self):
        moves = []

        for Bsq in self.__squares_from(self.__WB_BB if self.__turn else self.__BB_BB):
            for sq in self.__squares_from(self.__bishop_squares(Bsq)):
                moves.append(Move(Bsq, sq))

        return moves

    def generate_rook_moves(self):
        moves = []

        for Rsq in self.__squares_from(self.__WR_BB if self.__turn else self.__BR_BB):
            for sq in self.__squares_from(self.__rook_squares(Rsq)):
                moves.append(Move(Rsq, sq))

        return moves

    def generate_queen_moves(self):
        moves = []

        for Qsq in self.__squares_from(self.__WQ_BB if self.__turn else self.__BQ_BB):
            for sq in self.__squares_from(self.__queen_squares(Qsq)):
                moves.append(Move(Qsq, sq))

        return moves

    def generate_legal_moves(self):
        return self.generate_pawn_moves() + self.generate_knight_moves() + self.generate_bishop_moves() + \
               self.generate_rook_moves() + self.generate_queen_moves() + self.generate_king_moves()

    def __piece_at(self, sq):
        pieces = {bin64_to_str(self.__WP_BB): Piece(PAWN, WHITE),
                  bin64_to_str(self.__BP_BB): Piece(PAWN, BLACK),
                  bin64_to_str(self.__WN_BB): Piece(KNIGHT, WHITE),
                  bin64_to_str(self.__BN_BB): Piece(KNIGHT, BLACK),
                  bin64_to_str(self.__WB_BB): Piece(BISHOP, WHITE),
                  bin64_to_str(self.__BB_BB): Piece(BISHOP, BLACK),
                  bin64_to_str(self.__WR_BB): Piece(ROOK, WHITE),
                  bin64_to_str(self.__BR_BB): Piece(ROOK, BLACK),
                  bin64_to_str(self.__WQ_BB): Piece(QUEEN, WHITE),
                  bin64_to_str(self.__BQ_BB): Piece(QUEEN, BLACK),
                  bin64_to_str(self.__WK_BB): Piece(KING, WHITE),
                  bin64_to_str(self.__BK_BB): Piece(KING, BLACK)}

        for bb, piece in pieces.items():
            if bb[sq] == "1":
                return piece
        else:
            return None

    def __get_board(self):

        grid = []
        for row in range(8):
            grid.append([])
            for col in range(8):
                sq = row * 8 + col
                grid[-1].append(self.__piece_at(sq))

        return grid

    def print_board(self):
        grid = self.__get_board()
        grid.reverse()
        print()
        print("  a b c d e f g h")
        for c, row in enumerate(grid):
            print(8 - c, end=' ')
            for char in row:
                print(char if char is not None else " ", end=' ')
            print()
        print()

    @staticmethod
    def __move_piece(bb, sqs):
        s1, s2 = sqs
        bb -= 2 ** (63 - s1)
        bb += 2 ** (63 - s2)
        return bb

    @staticmethod
    def __remove_piece(bb, sq):
        bb -= 2 ** (63 - sq)
        return bb

    def __update_bb(self, piece, func, params):
        global PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, WHITE, BLACK
        pt, c = piece.piece_type, piece.colour
        if pt == PAWN and c == WHITE:
            self.__WP_BB = func(self.__WP_BB, params)
        elif pt == PAWN and c == BLACK:
            self.__BP_BB = func(self.__BP_BB, params)
        elif pt == KNIGHT and c == WHITE:
            self.__WN_BB = func(self.__WN_BB, params)
        elif pt == KNIGHT and c == BLACK:
            self.__BN_BB = func(self.__BN_BB, params)
        elif pt == BISHOP and c == WHITE:
            self.__WB_BB = func(self.__WB_BB, params)
        elif pt == BISHOP and c == BLACK:
            self.__BB_BB = func(self.__BB_BB, params)
        elif pt == ROOK and c == WHITE:
            self.__WR_BB = func(self.__WR_BB, params)
        elif pt == ROOK and c == BLACK:
            self.__BR_BB = func(self.__BR_BB, params)
        elif pt == QUEEN and c == WHITE:
            self.__WQ_BB = func(self.__WQ_BB, params)
        elif pt == QUEEN and c == BLACK:
            self.__BQ_BB = func(self.__BQ_BB, params)
        elif pt == KING and c == WHITE:
            self.__WK_BB = func(self.__WK_BB, params)
        elif pt == KING and c == BLACK:
            self.__BK_BB = func(self.__BK_BB, params)

    def push(self, move):

        s1, s2 = move.from_square, move.to_square
        p1, p2 = self.__piece_at(s1), self.__piece_at(s2)

        self.__update_bb(p1, self.__move_piece, (s1, s2))
        if p2 is not None:
            self.__update_bb(p2, self.__remove_piece, s2)

        self.__move_stack[move] = [self.__WP_BB, self.__BP_BB, self.__WN_BB, self.__BN_BB, self.__WB_BB, self.__BB_BB,
                                   self.__WR_BB, self.__BR_BB, self.__WQ_BB, self.__BQ_BB, self.__WK_BB, self.__BK_BB]
        self.__turn = not self.__turn

    def pop(self):
        if self.__move_stack:
            self.__move_stack.pop(list(self.__move_stack.keys())[-1])
            try:
                last = list(self.__move_stack.keys())[-1]
                self.__WP_BB, self.__BP_BB, self.__WN_BB, self.__BN_BB, self.__WB_BB, self.__BB_BB, \
                self.__WR_BB, self.__BR_BB, self.__WQ_BB, self.__BQ_BB, self.__WK_BB, self.__BK_BB = self.__move_stack[last]
                self.__turn = not self.__turn
            except IndexError:
                self.__init__()


board = Board()

while True:

    stime = time.perf_counter_ns()

    board.print_board()
    print(board.generate_legal_moves())

    print(f"time taken: {(time.perf_counter_ns() - stime) / 1e9}s")

    next_move = input("next move [(q)uit the game, (p)op last move]: ")
    if next_move == "q":
        break
    if next_move == "p":
        board.pop()
        continue
    move_obj = Move.from_uci(next_move)
    if move_obj.uci() in [move.uci() for move in board.generate_legal_moves()]:
        board.push(move_obj)
    else:
        print("illegal move, try again!")

print("done")
