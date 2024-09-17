import json
import os
import time
from functools import reduce

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


def sq_num(name):
    f, r = name
    return get_sq(f, r)


def open_json(file_name):
    with open(os.path.join(os.path.join(os.path.dirname(os.getcwd()), "movement_sqrs"), file_name)) as f:
        data = json.load(f)
    return dict(zip(map(int, data), data.values()))


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


def char_to_promotion(char):
    if char == "n":
        return KNIGHT
    elif char == "b":
        return BISHOP
    elif char == "r":
        return ROOK
    elif char == "q":
        return QUEEN


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


class Piece:
    def __init__(self, piece_type, colour):
        self.piece_type = piece_type
        self.colour = colour

    def __repr__(self):
        return piece_chars[self.piece_type] if self.colour else piece_chars[self.piece_type].lower()


class Move:
    def __init__(self, from_square, to_square, en_passant=False, promotion=0, castling=False):
        self.from_square = from_square
        self.to_square = to_square
        self.en_passant = en_passant
        self.promotion = promotion
        self.castling = castling

    def uci(self):
        return file(self.from_square) + rank(self.from_square) + file(self.to_square) + rank(self.to_square) + promotion_char(self.promotion)

    def __repr__(self):
        return self.uci()

    @staticmethod
    def from_uci(uci):
        return Move(get_sq(uci[0], uci[1]), get_sq(uci[2], uci[3]), promotion=char_to_promotion(uci[4]) if len(uci) > 4 else 0)


class Board:

    def __init__(self):

        with open("../movement_sqrs/base_board.json") as f:
            base_bb = json.load(f)

        self.__board_bb = [base_bb["white pawn"], base_bb["black pawn"], base_bb["white knight"], base_bb["black knight"], base_bb["white bishop"], base_bb["black bishop"],
                           base_bb["white rook"], base_bb["black rook"], base_bb["white queen"], base_bb["black queen"], base_bb["white king"], base_bb["black king"]]

        self.__turn = WHITE

        self.__move_stack = {}

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

    def __white_pieces(self):
        return reduce(lambda x, y : x | y, [self.__board_bb[i] for i in range(0, 12, 2)])

    def __black_pieces(self):
        return reduce(lambda x, y : x | y, [self.__board_bb[i] for i in range(1, 12, 2)])

    def __blockers(self):
        return self.__white_pieces() | self.__black_pieces()

    def __masked_blockers(self, mask):
        return self.__blockers() & mask

    def __enemy_squares(self):
        return self.__black_pieces() if self.__turn else self.__white_pieces()

    def __friendly_squares(self):
        return self.__white_pieces() if self.__turn else self.__black_pieces()

    def __enemy_squares_no_king(self):
        if self.__turn:
            return reduce(lambda x, y : x | y, [self.__board_bb[i] for i in range(1, 10, 2)]) # black
        else:
            return reduce(lambda x, y : x | y, [self.__board_bb[i] for i in range(0, 10, 2)]) # white

    def __intersection_sqrs(self, no_king, empty, protected, isPawn=False):
        if protected:
            return self.__friendly_squares()
        if empty:
            return self.__empty_squares()
        if no_king:
            return self.__empty_squares() | self.__enemy_squares_no_king()
        else:
            return (self.__empty_squares() | self.__enemy_squares()) if not isPawn else self.__enemy_squares()

    def __pawn_squares(self, ranks):
        bb = self.__board_bb[0 if self.__turn else 1]
        bb = bb >> 8 * ranks if self.__turn else bb << 8 * ranks
        return bb & self.__empty_squares()

    def __pawn_atk_squares(self, sq, no_king=False, empty=False, protected=False):
        if self.__turn:
            return PAWN_ATK_WHITE_SQRS[sq] & self.__intersection_sqrs(no_king, empty, protected, isPawn=True)
        else:
            return PAWN_ATK_BLACK_SQRS[sq] & self.__intersection_sqrs(no_king, empty, protected, isPawn=True)

    def __knight_squares(self, sq, no_king=False, empty=False, protected=False):
        return KNIGHT_SQRS[sq] & self.__intersection_sqrs(no_king, empty, protected)

    def __knight_atk_squares(self, sq):
        return KNIGHT_SQRS[sq] & self.__enemy_squares()

    def __king_squares(self, sq, no_king=False, empty=False, protected=False):
        return KING_SQRS[sq] & self.__intersection_sqrs(no_king, empty, protected)

    def __king_atk_squares(self, sq):
        return KING_SQRS[sq] & self.__enemy_squares()

    def __bishop_squares(self, sq, no_king=False, empty=False, protected=False):

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

        return self.__intersection_sqrs(no_king, empty, protected) & (nw_sqrs | ne_sqrs | sw_sqrs | se_sqrs)

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

    def __rook_squares(self, sq, no_king=False, empty=False, protected=False):

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

        return self.__intersection_sqrs(no_king, empty, protected) & (n_sqrs | e_sqrs | s_sqrs | w_sqrs)

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

    def __queen_squares(self, sq, no_king=False, empty=False, protected=False):
        return self.__bishop_squares(sq, no_king, empty, protected) | self.__rook_squares(sq, no_king, empty, protected)

    def __queen_atk_squares(self, sq):

        return self.__bishop_atk_squares(sq) | self.__rook_atk_squares(sq)

    @staticmethod
    def __squares_from(bb):
        for sq, bit in enumerate(bin64_to_str(bb)):
            if bit == "1":
                yield sq

    def __is_double_push(self, move):
        s1, s2 = move.from_square, move.to_square
        if self.piece_at(s2) is None:
            return False
        if self.piece_at(s2).piece_type == PAWN and abs(s2 - s1) == 16:
            return True
        return False

    def is_en_passant(self, move):
        s1, s2 = move.from_square, move.to_square
        if self.piece_at(s1) is None:
            return False
        if self.piece_at(s1).piece_type == PAWN and self.piece_at(s2) is None and abs(s2 - s1) not in (8, 16):
            return True
        return False

    def is_castling(self, move):
        s1, s2 = move.from_square, move.to_square
        if abs(s2 - s1) == 2 and self.piece_at(s1).piece_type == KING:
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
            sec_sq = sq - 8 if self.__turn else sq + 8
            if (self.__turn and rank(orig_sq) == "2") or (not self.__turn and rank(orig_sq) == "7"):
                if self.__empty_squares() & 2 ** (63 - sec_sq) != 0:
                    moves.append(Move(orig_sq, sq))

        # Captures
        for Psq in self.__squares_from(self.__board_bb[0 if self.__turn else 1]):
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
            left, right = self.piece_at(sq - 1), self.piece_at(sq + 1)
            centre = self.piece_at(sq)

            if self.__is_double_push(last_move):

                if left is not None and left.piece_type == PAWN and left.colour != centre.colour and rank(sq - 1) == rank(sq):
                    moves.append(Move(sq - 1, sq + 8 if self.__turn else sq - 8, en_passant=True))

                if right is not None and right.piece_type == PAWN and right.colour != centre.colour and rank(sq + 1) == rank(sq):
                    moves.append(Move(sq + 1, sq + 8 if self.__turn else sq - 8, en_passant=True))

        return moves

    def generate_knight_moves(self):
        moves = []

        for Nsq in self.__squares_from(self.__board_bb[2 if self.__turn else 3]):
            for sq in self.__squares_from(self.__knight_squares(Nsq)):
                moves.append(Move(Nsq, sq))

        return moves

    def generate_king_moves(self):
        moves = []

        self.__turn = not self.__turn

        legal_sqrs = bwn(self.generate_attacks_bb(no_king=True))
        non_protected_sqrs = bwn(self.generate_attacks_bb(protected=True))

        self.__turn = not self.__turn

        for Ksq in self.__squares_from(self.__board_bb[10 if self.__turn else 11]):
            for sq in self.__squares_from(self.__king_squares(Ksq) & (legal_sqrs & non_protected_sqrs)):
                moves.append(Move(Ksq, sq))

        return moves

    def generate_bishop_moves(self):
        moves = []

        for Bsq in self.__squares_from(self.__board_bb[4 if self.__turn else 5]):
            for sq in self.__squares_from(self.__bishop_squares(Bsq)):
                moves.append(Move(Bsq, sq))

        return moves

    def generate_rook_moves(self):
        moves = []

        for Rsq in self.__squares_from(self.__board_bb[6 if self.__turn else 7]):
            for sq in self.__squares_from(self.__rook_squares(Rsq)):
                moves.append(Move(Rsq, sq))

        return moves

    def generate_queen_moves(self):
        moves = []

        for Qsq in self.__squares_from(self.__board_bb[8 if self.__turn else 9]):
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
            moves.append(Move(sq_num("e1") if self.__turn else sq_num("e8"), sq_num("g1") if self.__turn else sq_num("g8"), castling=True))
        if self.__can_long_castle():
            moves.append(Move(sq_num("e1") if self.__turn else sq_num("e8"), sq_num("c1") if self.__turn else sq_num("c8"), castling=True))

        return moves

    def generate_capture_bb(self):
        funcs = [self.__pawn_atk_squares, self.__knight_atk_squares, self.__bishop_atk_squares, 
                 self.__rook_atk_squares, self.__queen_atk_squares, self.__king_atk_squares]
        bb = 0
        for i, idx in enumerate(range(0 if self.__turn else 1, 12, 2)):
            for sq in self.__squares_from(self.__board_bb[idx]):
                bb |= funcs[i](sq)
        return bb

    def generate_attacks_bb(self, no_king=False, empty=False, protected=False):
        funcs = [self.__pawn_atk_squares, self.__knight_squares, self.__bishop_squares, 
            self.__rook_squares, self.__queen_squares, self.__king_squares]
        bb = 0
        for i, idx in enumerate(range(0 if self.__turn else 1, 12, 2)):
            for sq in self.__squares_from(self.__board_bb[idx]):
                bb |= funcs[i](sq, no_king, empty, protected)
        return bb

    @property
    def pseudo_legal_moves(self):
        return self.generate_pawn_moves() + self.generate_knight_moves() + self.generate_bishop_moves() + \
               self.generate_rook_moves() + self.generate_queen_moves() + self.generate_castling_moves()

    @property
    def legal_moves(self):
        pseudo_legal_moves = self.pseudo_legal_moves
        legal_moves = []
        for move in pseudo_legal_moves:
            # print(move, self.__board_bb)
            self.push(move)
            if self.generate_capture_bb() & (self.__board_bb[10 if not self.__turn else 11]) == 0:
                legal_moves.append(move)
            self.pop()
            # print(self.__board_bb)
        return legal_moves + self.generate_king_moves()

    def piece_at(self, sq):
        pieces = {bin64_to_str(self.__board_bb[0]): Piece(PAWN, WHITE),
                  bin64_to_str(self.__board_bb[1]): Piece(PAWN, BLACK),
                  bin64_to_str(self.__board_bb[2]): Piece(KNIGHT, WHITE),
                  bin64_to_str(self.__board_bb[3]): Piece(KNIGHT, BLACK),
                  bin64_to_str(self.__board_bb[4]): Piece(BISHOP, WHITE),
                  bin64_to_str(self.__board_bb[5]): Piece(BISHOP, BLACK),
                  bin64_to_str(self.__board_bb[6]): Piece(ROOK, WHITE),
                  bin64_to_str(self.__board_bb[7]): Piece(ROOK, BLACK),
                  bin64_to_str(self.__board_bb[8]): Piece(QUEEN, WHITE),
                  bin64_to_str(self.__board_bb[9]): Piece(QUEEN, BLACK),
                  bin64_to_str(self.__board_bb[10]): Piece(KING, WHITE),
                  bin64_to_str(self.__board_bb[11]): Piece(KING, BLACK)}

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
                grid[-1].append(self.piece_at(sq))

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
        mapping = {(PAWN, WHITE): 0,
                   (PAWN, BLACK): 1,
                   (KNIGHT, WHITE): 2,
                   (KNIGHT, BLACK): 3,
                   (BISHOP, WHITE): 4,
                   (BISHOP, BLACK): 5,
                   (ROOK, WHITE): 6,
                   (ROOK, BLACK): 7,
                   (QUEEN, WHITE): 8,
                   (QUEEN, BLACK): 9,
                   (KING, WHITE): 10,
                   (KING, BLACK): 11}
        bbi = mapping[(pt, c)]
        self.__board_bb[bbi] = func(self.__board_bb[bbi], params)

    def push(self, move):

        s1, s2 = move.from_square, move.to_square
        p1, p2 = self.piece_at(s1), self.piece_at(s2)

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

        self.__move_stack[move] = [self.__board_bb[:], [self.__WRookA_moved, self.__WRookH_moved, self.__WKing_moved, self.__BRookA_moved, self.__BRookH_moved, self.__BKing_moved]]
        self.__turn = not self.__turn

    def pop(self):
        if self.__move_stack:  # move list is not empty
            self.__move_stack.pop(list(self.__move_stack.keys())[-1])
            try:  # has 2 or more moves on the move stack
                last = list(self.__move_stack.keys())[-1]
                self.__board_bb = self.__move_stack[last][0][:]
                self.__WRookA_moved, self.__WRookH_moved, self.__WKing_moved, self.__BRookA_moved, self.__BRookH_moved, self.__BKing_moved = self.__move_stack[last][1]
                self.__turn = not self.__turn
            except IndexError:  # has only 1 move on the move stack
                self.__init__()  # reset to default position

    def is_capture(self, move):
        p1, p2 = self.piece_at(move.from_square), self.piece_at(move.to_square)
        if move.en_passant:
            return True
        elif p2 is not None:
            return True
        return False

    def is_check(self, move):
        self.push(move)
        self.__turn = not self.__turn
        bb = self.generate_capture_bb()
        self.__turn = not self.__turn
        self.pop()
        if bb & (self.__board_bb[10 if not self.__turn else 11]) != 0:
            return True
        return False

    # def set_fen(self, fen):
    #     pp, turn, castling, epts, hmc, moves = fen.split(" ")
    #     for rn, rank in enumerate(pp.split("/")): # iterate through each rank
    #         fn = 0
    #         for char in rank:
    #             if char in "PNBRQKpnbrqk":
    #                 fn += 1
    #             else:
    #                 fn += int(char)
        
    def perft(self, depth):
        global nodes, captures, checks, en_passant, checkmates
        nodes = 0
        captures = 0
        checks = 0
        en_passant = 0
        checkmates = 0
        stime = time.perf_counter()
        self.__perft(depth)
        return {"nodes": nodes, "captures": captures, "checks": checks, "en passant": en_passant, 
                "checkmates": checkmates, "time": time.perf_counter() - stime}

    def __perft(self, depth):
        global nodes, captures, checks, en_passant, checkmates

        if depth == 0:
            return

        for move in (moves := self.legal_moves):
            # print(depth, move)
            if depth == 1:
                if self.is_capture(move):
                    captures += 1
                if self.is_check(move):
                    checks += 1
                if self.is_en_passant(move):
                    en_passant += 1
                nodes += 1
            self.push(move)
            # self.print_board()
            # print(self.__board_bb)
            self.__perft(depth - 1)
            self.pop()
            # print(self.__board_bb)
        
        if len(moves) == 0:
            checkmates += 1


if __name__ in "__main__":

    board = Board()

    # while True:
    #
    #     stime = time.perf_counter_ns()
    #
    #     board.print_board()
    #     print(board.legal_moves)
    #
    #     print(f"time taken: {(time.perf_counter_ns() - stime) / 1e9}s")
    #
    #     next_move = input("next move [(q)uit the game, (p)op last move]: ")
    #     if next_move == "q":
    #         break
    #     if next_move == "p":
    #         board.pop()
    #         continue
    #     try:
    #         move_obj = Move.from_uci(next_move)
    #         if board.is_en_passant(move_obj):
    #             move_obj.en_passant = True
    #         elif board.is_castling(move_obj):
    #             move_obj.castling = True
    #         if move_obj.uci() in [move.uci() for move in board.legal_moves]:
    #             board.push(move_obj)
    #         else:
    #             print("illegal move, try again!")
    #     except Exception as err:
    #         print(err)

    print(board.perft(1))
    print(board.perft(2))
    print(board.perft(3))
    print(board.perft(4))
    # print(board.perft(5))

    print("done")

'''

prev:

{'nodes': 20, 'captures': 0, 'checks': 0, 'en passant': 0, 'time': 0.014631700003519654}
{'nodes': 400, 'captures': 0, 'checks': 0, 'en passant': 0, 'time': 0.2107947999611497}
{'nodes': 8902, 'captures': 34, 'checks': 12, 'en passant': 0, 'time': 3.15568790002726}
{'nodes': 197281, 'captures': 1576, 'checks': 469, 'en passant': 0, 'time': 62.353513499954715}
{'nodes': 4865621, 'captures': 82719, 'checks': 27351, 'en passant': 258, 'time': 1796.025495500071}

most updated:

{'nodes': 20, 'captures': 0, 'checks': 0, 'en passant': 0, 'checkmates': 0, 'time': 0.0344046}
{'nodes': 400, 'captures': 0, 'checks': 0, 'en passant': 0, 'checkmates': 0, 'time': 0.23974059999999997}
{'nodes': 8902, 'captures': 34, 'checks': 12, 'en passant': 0, 'checkmates': 0, 'time': 1.9510216999999999}
{'nodes': 197281, 'captures': 1576, 'checks': 469, 'en passant': 0, 'checkmates': 0, 'time': 23.550980300000003}
{'nodes': 4865621, 'captures': 82719, 'checks': 27351, 'en passant': 258, 'checkmates': 8, 'time': 556.6171326}
done

35888059530608640
71776119061217280
53832089295912960
71776119061217280
62804104178565120
71776119061217280
67290111619891200
71776119061217280
69533115340554240
71776119061217280
70654617200885760
71776119061217280
71215368131051520
71776119061217280
71495743596134400
71776119061217280
35747871798067200
71776119061217280
53761995429642240
71776119061217280
62769057245429760
71776119061217280
67272588153323520
71776119061217280
69524353607270400
71776119061217280
70650236334243840
71776119061217280
71213177697730560
71776119061217280
71494648379473920
71776119061217280
71776119061217280
71776119061217280
71776119061217280
71776119061217280
71776119061217280
71776119061217280
71776119061217280
71776119061217280
{'nodes': 20, 'captures': 0, 'checks': 0, 'en passant': 0, 'checkmates': 0, 'time': 0.0482498}
done

'''