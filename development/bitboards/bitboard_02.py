import json
import os
import time


def str_to_bin64(s):
    total = 0
    for idx, val in enumerate(s):
        c = 63 - idx
        total += 2 ** c if val == "1" else 0
    return total


def ms_to_bin64(ms):
    return str_to_bin64("".join([line for line in ms.split()]))


def bin64_to_str(bin64):
    s = []
    while bin64 > 0:
        s.append(bin64 % 2)
        bin64 //= 2
    s.reverse()
    return "".join(list(map(str, s))).zfill(64)


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
    return ["a", "b", "c", "d", "e", "f", "g", "h"][sq % 8]


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


# data = {"pawn atk white": PAWN_ATK_WHITE_SQRS,
#         "pawn atk black": PAWN_ATK_BLACK_SQRS,
#         "knight": KNIGHT_SQRS,
#         "king": KING_SQRS}
#
# data_string = json.dumps(data, indent=4)
#
# with open("movement_sqrs.json", "w") as f:
#     f.write(data_string)

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


class Move:
    def __init__(self, from_square, to_square, promotion=False):
        self.from_square = from_square
        self.to_square = to_square
        self.promotion = promotion

    def uci(self):
        return file(self.from_square) + rank(self.from_square) + file(self.to_square) + rank(self.to_square)

    def __repr__(self):
        return self.uci()


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

        self.__turn = True

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


stime = time.perf_counter_ns()

board = Board()
print(board.generate_pawn_moves())
print(board.generate_knight_moves())
print(board.generate_king_moves())
print(board.generate_bishop_moves())
print(board.generate_rook_moves())
print(board.generate_queen_moves())

print(f"time taken: {(time.perf_counter_ns() - stime) / 1e9}s")
