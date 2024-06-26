import json
import os
import time
from numba import njit
from numba.experimental import jitclass
import numba.types
# import numba.typed.dictobject
from numba.typed import Dict

PAWN = 2
KNIGHT = 3
BISHOP = 4
ROOK = 5
QUEEN = 6
KING = 7

WHITE = True
BLACK = False

files = ["a", "b", "c", "d", "e", "f", "g", "h"]


@njit
def str_to_bin64(s):
    total = 0
    for idx, val in enumerate(s):
        c = 63 - idx
        total += 2 ** c if val == "1" else 0
    return total


@njit
def bin64_to_str(bin64):
    return str(bin(bin64))[2:].zfill(64)


@njit
def bsf(bin64):
    s = bin64_to_str(bin64)
    for idx in range(64):
        if s[idx] == "1":
            return idx
    return None


@njit
def bwn(bin64):
    return bin64 ^ (2 ** 64 - 1)


@njit
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


@njit
def rank(sq):
    return str(sq // 8 + 1)


@njit
def file(sq):
    return files[sq % 8]


@njit
def get_sq(f, r):
    return files.index(f) + (int(r) - 1) * 8


@njit
def sq_num(name):
    f, r = name
    return get_sq(f, r)


def open_json(file_name):
    with open(os.path.join(os.path.join(os.path.dirname(os.getcwd()), "movement_sqrs"), file_name)) as f:
        data = json.load(f)
    return dict(zip(map(int, data), data.values()))


@njit
def promotion_char(promotion):
    if promotion == KNIGHT:
        return "n"
    elif promotion == BISHOP:
        return "b"
    elif promotion == ROOK:
        return "r"
    elif promotion == QUEEN:
        return "q"
    else:
        return ""


@njit
def char_to_promotion(char):
    if char == "n":
        return KNIGHT
    elif char == "b":
        return BISHOP
    elif char == "r":
        return ROOK
    elif char == "q":
        return QUEEN


@njit
def bb_from_sqrs(sqrs):
    bb = 0
    for sq in sqrs:
        bb += 2 ** (63 - sq)
    return bb


PAWN_ATK_WHITE_SQRS = open_json("pawn_atk_white_sqrs.json")
PAWN_ATK_BLACK_SQRS = open_json("pawn_atk_black_sqrs.json")
KNIGHT_SQRS = open_json("knight_sqrs.json")
KING_SQRS = open_json("king_sqrs.json")
BISHOP_SQRS = open_json("bishop_sqrs.json")
ROOK_SQRS = open_json("rook_sqrs.json")

piece_chars = {PAWN: "P", KNIGHT: "N", BISHOP: "B", ROOK: "R", QUEEN: "Q", KING: "K"}


@jitclass({"piece_type": numba.types.int64, "colour": numba.types.boolean})
class Piece:
    def __init__(self, piece_type, colour):
        self.piece_type = piece_type
        self.colour = colour

    def __repr__(self):
        return piece_chars[self.piece_type] if self.colour else piece_chars[self.piece_type].lower()


@jitclass({"from_square": numba.types.int64, "to_square": numba.types.int64, "en_passant": numba.types.boolean, "promotion": numba.types.int64, "castling": numba.types.boolean})
class Move:
    def __init__(self, from_square, to_square, en_passant=False, promotion=0, castling=False):
        self.from_square = from_square
        self.to_square = to_square
        self.en_passant = en_passant
        self.promotion = promotion
        self.castling = castling

    def uci(self):
        return file(self.from_square) + rank(self.from_square) + file(self.to_square) + rank(
            self.to_square) + promotion_char(self.promotion)

    def __repr__(self):
        return self.uci()

    @staticmethod
    def from_uci(uci):
        return Move(get_sq(uci[0], uci[1]), get_sq(uci[2], uci[3]),
                    promotion=char_to_promotion(uci[4]) if len(uci) > 4 else 0)


@jitclass({"__WP_BB": numba.types.int64, "__BP_BB": numba.types.int64, "__WN_BB": numba.types.int64, "__BN_BB": numba.types.int64, "__WB_BB": numba.types.int64, "__BB_BB": numba.types.int64,
           "__WR_BB": numba.types.int64, "__BR_BB": numba.types.int64, "__WQ_BB": numba.types.int64, "__BQ_BB": numba.types.int64, "__WK_BB": numba.types.int64, "__BK_BB": numba.types.int64,
           "__turn": numba.types.boolean, "__move_stack": numba.types.List(numba.)
           "__WShortCastle_bb": numba.types.int64, "__WLongCastle_bb": numba.types.int64, "__BShortCastle_bb": numba.types.int64, "__BLongCastle_bb": numba.types.int64})
class Board:
    def __init__(self, base_bb):

        self.__WP_BB = base_bb[0]
        self.__BP_BB = base_bb[1]

        self.__WN_BB = base_bb[2]
        self.__BN_BB = base_bb[3]

        self.__WB_BB = base_bb[4]
        self.__BB_BB = base_bb[5]

        self.__WR_BB = base_bb[6]
        self.__BR_BB = base_bb[7]

        self.__WQ_BB = base_bb[8]
        self.__BQ_BB = base_bb[9]

        self.__WK_BB = base_bb[10]
        self.__BK_BB = base_bb[11]

        self.__turn = WHITE

        self.__move_stack = []

        self.__WRookA_moved = False
        self.__WRookH_moved = False
        self.__BRookA_moved = False
        self.__BRookH_moved = False
        self.__WKing_moved = False
        self.__BKing_moved = False

        self.__WShortCastle_bb = bb_from_sqrs([sq_num("f1"), sq_num("g1")])
        self.__WLongCastle_bb = bb_from_sqrs([sq_num("b1"), sq_num("c1"), sq_num("d1")])
        self.__BShortCastle_bb = bb_from_sqrs([sq_num("f8"), sq_num("g8")])
        self.__BLongCastle_bb = bb_from_sqrs([sq_num("b8"), sq_num("c8"), sq_num("d8")])

        self.nodes = 0

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

    def __knight_atk_squares(self, sq):
        return KNIGHT_SQRS[sq] & self.__enemy_squares()

    def __king_squares(self, sq):
        return KING_SQRS[sq] & (self.__empty_squares() | self.__enemy_squares())

    def __king_atk_squares(self, sq):
        return KING_SQRS[sq] & self.__enemy_squares()

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

    def __bishop_atk_squares(self, sq):

        bb = 0

        # North-west
        nw_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["NW"])
        blocker = bsr(nw_blockers)
        bb += 2 ** (63 - blocker) if blocker is not None else 0

        # North-east
        ne_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["NE"])
        blocker = bsr(ne_blockers)
        bb += 2 ** (63 - blocker) if blocker is not None else 0

        # South-west
        sw_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["SW"])
        blocker = bsf(sw_blockers)
        bb += 2 ** (63 - blocker) if blocker is not None else 0

        # South-east
        se_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["SE"])
        blocker = bsf(se_blockers)
        bb += 2 ** (63 - blocker) if blocker is not None else 0

        return bb & self.__enemy_squares()

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

    def __rook_atk_squares(self, sq):

        bb = 0

        # North
        n_blockers = self.__masked_blockers(ROOK_SQRS[sq]["N"])
        blocker = bsr(n_blockers)
        bb += 2 ** (63 - blocker) if blocker is not None else 0

        # East
        e_blockers = self.__masked_blockers(ROOK_SQRS[sq]["E"])
        blocker = bsf(e_blockers)
        bb += 2 ** (63 - blocker) if blocker is not None else 0

        # South
        s_blockers = self.__masked_blockers(ROOK_SQRS[sq]["S"])
        blocker = bsf(s_blockers)
        bb += 2 ** (63 - blocker) if blocker is not None else 0

        # West
        w_blockers = self.__masked_blockers(ROOK_SQRS[sq]["W"])
        blocker = bsr(w_blockers)
        bb += 2 ** (63 - blocker) if blocker is not None else 0

        return bb & self.__enemy_squares()

    def __queen_squares(self, sq):
        return self.__bishop_squares(sq) | self.__rook_squares(sq)

    def __queen_atk_squares(self, sq):

        return self.__bishop_atk_squares(sq) | self.__rook_atk_squares(sq)

    @staticmethod
    def __squares_from(bb):
        for sq, bit in enumerate(bin64_to_str(bb)):
            if bit == "1":
                yield sq

    def __is_double_push(self, move):
        s1, s2 = move.from_square, move.to_square
        if self.__piece_at(s2) is None:
            return False
        if self.__piece_at(s2).piece_type == PAWN and abs(s2 - s1) == 16:
            return True
        return False

    def is_en_passant(self, move):
        s1, s2 = move.from_square, move.to_square
        if self.__piece_at(s1) is None:
            return False
        if self.__piece_at(s1).piece_type == PAWN and self.__piece_at(s2) is None and abs(s2 - s1) not in (8, 16):
            return True
        return False

    def is_castling(self, move):
        s1, s2 = move.from_square, move.to_square
        if abs(s2 - s1) == 2 and self.__piece_at(s1).piece_type == KING:
            return True
        return False

    def generate_pawn_moves(self):
        moves = []

        # Normal push
        for sq in self.__squares_from(self.__pawn_squares(1)):
            orig_sq = sq - 8 if self.__turn else sq + 8
            if (self.__turn and rank(sq) == "8") or (not self.__turn and rank(sq) == "1"):  # promotion
                for piece in (KNIGHT, BISHOP, ROOK, QUEEN):
                    moves.append(Move(orig_sq, sq, promotion=piece))
            else:
                moves.append(Move(orig_sq, sq))

        # Double push
        for sq in self.__squares_from(self.__pawn_squares(2)):
            orig_sq = sq - 16 if self.__turn else sq + 16
            if (self.__turn and rank(orig_sq) == "2") or (not self.__turn and rank(orig_sq) == "7"):
                moves.append(Move(orig_sq, sq))

        # Captures
        for Psq in self.__squares_from(self.__WP_BB if self.__turn else self.__BP_BB):
            for sq in self.__squares_from(self.__pawn_atk_squares(Psq)):
                if (self.__turn and rank(sq) == "8") or (not self.__turn and rank(sq) == "1"):  # promotion
                    for piece in (KNIGHT, BISHOP, ROOK, QUEEN):
                        moves.append(Move(Psq, sq, promotion=piece))
                else:
                    moves.append(Move(Psq, sq))

        # En Passant
        if len(self.__move_stack) > 0:

            last_move = list(self.__move_stack.keys())[-1]
            sq = last_move.to_square
            left, right = self.__piece_at(sq - 1), self.__piece_at(sq + 1)

            if self.__is_double_push(last_move):

                if left is not None and left.piece_type == PAWN and left.colour == self.__turn:

                    if (self.__turn and rank(sq) == "8") or (not self.__turn and rank(sq) == "1"):  # promotion
                        for piece in (KNIGHT, BISHOP, ROOK, QUEEN):
                            moves.append(
                                Move(sq - 1, sq + 8 if self.__turn else sq - 8, promotion=piece, en_passant=True))
                    else:
                        moves.append(Move(sq - 1, sq + 8 if self.__turn else sq - 8, en_passant=True))

                elif right is not None and right.piece_type == PAWN and right.colour == self.__turn:

                    if (self.__turn and rank(sq) == "8") or (not self.__turn and rank(sq) == "1"):  # promotion
                        for piece in (KNIGHT, BISHOP, ROOK, QUEEN):
                            moves.append(
                                Move(sq - 1, sq + 8 if self.__turn else sq - 8, promotion=piece, en_passant=True))
                    else:
                        moves.append(Move(sq + 1, sq + 8 if self.__turn else sq - 8, en_passant=True))

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

    def __can_short_castle(self):
        if self.__turn:
            if self.__WShortCastle_bb & self.__empty_squares() == self.__WShortCastle_bb and not self.__WRookH_moved and not self.__WKing_moved:
                return True
        else:
            if self.__BShortCastle_bb & self.__empty_squares() == self.__BShortCastle_bb and not self.__WRookH_moved and not self.__BKing_moved:
                return True
        return False

    def __can_long_castle(self):
        if self.__turn:
            if self.__WLongCastle_bb & self.__empty_squares() == self.__WLongCastle_bb and not self.__WRookA_moved and not self.__WKing_moved:
                return True
        else:
            if self.__BLongCastle_bb & self.__empty_squares() == self.__BLongCastle_bb and not self.__BRookA_moved and not self.__BKing_moved:
                return True
        return False

    def generate_castling_moves(self):
        moves = []
        if self.__can_short_castle():
            moves.append(
                Move(sq_num("e1") if self.__turn else sq_num("e8"), sq_num("g1") if self.__turn else sq_num("g8"),
                     castling=True))
        if self.__can_long_castle():
            moves.append(
                Move(sq_num("e1") if self.__turn else sq_num("e8"), sq_num("c1") if self.__turn else sq_num("c8"),
                     castling=True))

        return moves

    def generate_capture_bb(self):
        bb = 0
        for sq in self.__squares_from(self.__WP_BB if self.__turn else self.__BP_BB):
            bb |= self.__pawn_atk_squares(sq)
        for sq in self.__squares_from(self.__WN_BB if self.__turn else self.__BN_BB):
            bb |= self.__knight_atk_squares(sq)
        for sq in self.__squares_from(self.__WB_BB if self.__turn else self.__BB_BB):
            bb |= self.__bishop_atk_squares(sq)
        for sq in self.__squares_from(self.__WR_BB if self.__turn else self.__BR_BB):
            bb |= self.__rook_atk_squares(sq)
        for sq in self.__squares_from(self.__WQ_BB if self.__turn else self.__BQ_BB):
            bb |= self.__queen_atk_squares(sq)
        for sq in self.__squares_from(self.__WK_BB if self.__turn else self.__BK_BB):
            bb |= self.__king_atk_squares(sq)
        return bb

    @property
    def pseudo_legal_moves(self):
        return self.generate_pawn_moves() + self.generate_knight_moves() + self.generate_bishop_moves() + \
               self.generate_rook_moves() + self.generate_queen_moves() + self.generate_king_moves() + self.generate_castling_moves()

    @property
    # @njit
    def legal_moves(self):
        pseudo_legal_moves = self.pseudo_legal_moves
        legal_moves = []
        for move in pseudo_legal_moves:
            self.push(move)
            if self.generate_capture_bb() & (self.__WK_BB if not self.__turn else self.__BK_BB) == 0:
                legal_moves.append(move)
            self.pop()
        return legal_moves

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
    def __add_piece(bb, sq):
        bb += 2 ** (63 - sq)
        return bb

    @staticmethod
    def __remove_piece(bb, sq):
        bb -= 2 ** (63 - sq)
        return bb

    def __move_piece(self, bb, sqs):
        s1, s2 = sqs
        bb = self.__remove_piece(bb, s1)
        bb = self.__add_piece(bb, s2)
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

        if move.castling:
            if file(s2) == "g":  # short castle
                self.__update_bb(Piece(ROOK, self.__turn), self.__move_piece, (s1 + 3, s2 - 1))
            elif file(s2) == "c":  # long castle
                self.__update_bb(Piece(ROOK, self.__turn), self.__move_piece, (s1 - 4, s2 + 1))

        if move.promotion:  # move a piece and promote
            self.__update_bb(p1, self.__remove_piece, s1)
            self.__update_bb(Piece(move.promotion, p1.colour), self.__add_piece, s2)
        else:
            self.__update_bb(p1, self.__move_piece, (s1, s2))  # move a piece normally
        if p2 is not None:  # normal capture
            self.__update_bb(p2, self.__remove_piece, s2)
        if move.en_passant:  # en passant move only
            self.__update_bb(Piece(PAWN, not self.__turn), self.__remove_piece, s2 - 8 if self.__turn else s2 + 8)

        # Updating whether king or rook have moved
        if p1.piece_type == KING:
            if p1.colour:
                if not self.__WKing_moved:
                    self.__WKing_moved = True
            else:
                if not self.__BKing_moved:
                    self.__BKing_moved = True
        elif p1.piece_type == ROOK:
            if p1.colour:
                if file(s1) == "a" and not self.__WRookA_moved:
                    self.__WRookA_moved = True
                elif file(s1) == "h" and not self.__WRookH_moved:
                    self.__WRookH_moved = True
            else:
                if file(s1) == "a" and not self.__BRookA_moved:
                    self.__BRookA_moved = True
                elif file(s1) == "h" and not self.__BRookH_moved:
                    self.__BRookH_moved = True

        self.__move_stack[move] = [[self.__WP_BB, self.__BP_BB, self.__WN_BB, self.__BN_BB, self.__WB_BB, self.__BB_BB,
                                    self.__WR_BB, self.__BR_BB, self.__WQ_BB, self.__BQ_BB, self.__WK_BB, self.__BK_BB],
                                   [self.__WRookA_moved, self.__WRookH_moved, self.__WKing_moved, self.__BRookA_moved,
                                    self.__BRookH_moved, self.__BKing_moved]]
        self.__turn = not self.__turn

    def pop(self):
        if self.__move_stack:  # move list is not empty
            self.__move_stack.pop(list(self.__move_stack.keys())[-1])
            try:  # has 2 or more moves on the move stack
                last = list(self.__move_stack.keys())[-1]
                self.__WP_BB, self.__BP_BB, self.__WN_BB, self.__BN_BB, self.__WB_BB, self.__BB_BB, \
                self.__WR_BB, self.__BR_BB, self.__WQ_BB, self.__BQ_BB, self.__WK_BB, self.__BK_BB = \
                self.__move_stack[last][0]
                self.__WRookA_moved, self.__WRookH_moved, self.__WKing_moved, self.__BRookA_moved, self.__BRookH_moved, self.__BKing_moved = \
                self.__move_stack[last][1]
                self.__turn = not self.__turn
            except IndexError:  # has only 1 move on the move stack
                self.__init__(base_bb)  # reset to default position

    def perft(self, depth):
        global nodes
        nodes = 0
        stime = time.perf_counter()
        self.__perft(depth)
        return {"nodes": nodes, "time": time.perf_counter() - stime}

    def __perft(self, depth):
        global nodes

        if depth == 0:
            nodes += 1
            return

        for move in self.legal_moves:
            self.push(move)
            self.__perft(depth - 1)
            self.pop()


with open("../movement_sqrs/base_board.json") as f:
    base_bb = json.load(f)
base_bb = [item for item in base_bb.keys()]

board = Board(base_bb)

while True:

    stime = time.perf_counter_ns()

    board.print_board()
    print(board.legal_moves)

    print(f"time taken: {(time.perf_counter_ns() - stime) / 1e9}s")

    next_move = input("next move [(q)uit the game, (p)op last move]: ")
    if next_move == "q":
        break
    if next_move == "p":
        board.pop()
        continue
    try:
        move_obj = Move.from_uci(next_move)
        if board.is_en_passant(move_obj):
            move_obj.en_passant = True
        elif board.is_castling(move_obj):
            move_obj.castling = True
        if move_obj.uci() in [move.uci() for move in board.legal_moves]:
            board.push(move_obj)
        else:
            print("illegal move, try again!")
    except Exception as err:
        print(err)

# print(board.perft(1))
# print(board.perft(2))
# print(board.perft(3))
# print(board.perft(4))

print("done")
