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

    PIECES = [Piece(PAWN, WHITE), Piece(PAWN, BLACK), Piece(KNIGHT, WHITE), Piece(KNIGHT, BLACK), Piece(BISHOP, WHITE), Piece(BISHOP, BLACK),
              Piece(ROOK, WHITE), Piece(ROOK, BLACK), Piece(QUEEN, WHITE), Piece(QUEEN, BLACK), Piece(KING, WHITE), Piece(KING, BLACK)]
    
    WShortCastle_bb = bb_from_sqrs([sq_num("f1"), sq_num("g1")])
    WLongCastle_bb = bb_from_sqrs([sq_num("b1"), sq_num("c1"), sq_num("d1")])
    BShortCastle_bb = bb_from_sqrs([sq_num("f8"), sq_num("g8")])
    BLongCastle_bb = bb_from_sqrs([sq_num("b8"), sq_num("c8"), sq_num("d8")])

    def __init__(self):

        with open("../movement_sqrs/base_board.json") as f:
            base_bb = json.load(f)

        self.__board_bb = [base_bb["white pawn"], base_bb["black pawn"], base_bb["white knight"], base_bb["black knight"], base_bb["white bishop"], base_bb["black bishop"],
                           base_bb["white rook"], base_bb["black rook"], base_bb["white queen"], base_bb["black queen"], base_bb["white king"], base_bb["black king"]]
        self.__turn = WHITE
        self.__castling_rights = [True, True, True, True]
        self.__en_passant_square = None

        self.__move_stack = []
        self.__state_stack = [[self.__board_bb[:], self.__castling_rights, self.__en_passant_square]]

        

        self.__CAPTURE_FUNCS = [self.__pawn_atk_squares, self.__knight_atk_squares, self.__bishop_atk_squares, 
                                self.__rook_atk_squares, self.__queen_atk_squares, self.__king_atk_squares]
        self.__ATTACK_FUNCS = [self.__pawn_atk_squares, self.__knight_squares, self.__bishop_squares, 
                               self.__rook_squares, self.__queen_squares, self.__king_squares]

        self.nodes = 0

    def __empty_squares(self):
        return bwn(self.__blockers())
    
    def __enemy_king_squares(self):
        return self.__board_bb[10 if not self.__turn else 11]

    def __white_pieces(self):
        return reduce(lambda x, y : x | y, [self.__board_bb[i] for i in range(0, 12, 2)])

    def __black_pieces(self):
        return reduce(lambda x, y : x | y, [self.__board_bb[i] for i in range(1, 12, 2)])

    def __blockers(self, no_enemy_king=False):
        if no_enemy_king:
            return self.__white_pieces() | self.__enemy_squares_no_king() if self.__turn else self.__enemy_squares_no_king() | self.__black_pieces()
        return self.__white_pieces() | self.__black_pieces()

    def __masked_blockers(self, mask, no_enemy_king=False):
        return self.__blockers(no_enemy_king) & mask

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
            return self.__empty_squares() | self.__enemy_squares_no_king() | self.__enemy_king_squares()
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
        nw_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["NW"], no_enemy_king=no_king)
        blocker = bsr(nw_blockers)
        nw_sqrs = BISHOP_SQRS[sq]["NW"] & bwn(BISHOP_SQRS[blocker]["NW"] if blocker is not None else 0)

        # North-east
        ne_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["NE"], no_enemy_king=no_king)
        blocker = bsr(ne_blockers)
        ne_sqrs = BISHOP_SQRS[sq]["NE"] & bwn(BISHOP_SQRS[blocker]["NE"] if blocker is not None else 0)

        # South-west
        sw_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["SW"], no_enemy_king=no_king)
        blocker = bsf(sw_blockers)
        sw_sqrs = BISHOP_SQRS[sq]["SW"] & bwn(BISHOP_SQRS[blocker]["SW"] if blocker is not None else 0)

        # South-east
        se_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["SE"], no_enemy_king=no_king)
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
        n_blockers = self.__masked_blockers(ROOK_SQRS[sq]["N"], no_enemy_king=no_king)
        blocker = bsr(n_blockers)
        n_sqrs = ROOK_SQRS[sq]["N"] & bwn(ROOK_SQRS[blocker]["N"] if blocker is not None else 0)

        # East
        e_blockers = self.__masked_blockers(ROOK_SQRS[sq]["E"], no_enemy_king=no_king)
        blocker = bsf(e_blockers)
        e_sqrs = ROOK_SQRS[sq]["E"] & bwn(ROOK_SQRS[blocker]["E"] if blocker is not None else 0)

        # South
        s_blockers = self.__masked_blockers(ROOK_SQRS[sq]["S"], no_enemy_king=no_king)
        blocker = bsf(s_blockers)
        s_sqrs = ROOK_SQRS[sq]["S"] & bwn(ROOK_SQRS[blocker]["S"] if blocker is not None else 0)

        # West
        w_blockers = self.__masked_blockers(ROOK_SQRS[sq]["W"], no_enemy_king=no_king)
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
        pattack_sqrs = set()
        for Psq in self.__squares_from(self.__board_bb[0 if self.__turn else 1]):
            for sq in self.__squares_from(self.__pawn_atk_squares(Psq)):
                pattack_sqrs.add(sq)
                if (self.__turn and rank(sq) == "8") or (not self.__turn and rank(sq) == "1"):  # promotion
                    for piece in (KNIGHT, BISHOP, ROOK, QUEEN):
                        moves.append(Move(Psq, sq, promotion=piece))
                else:
                    moves.append(Move(Psq, sq))

        # En Passant
        epsq = self.__en_passant_square
        if epsq is not None and epsq in pattack_sqrs: # Valid en passant move
            left, right = self.piece_at(epsq - 1), self.piece_at(epsq + 1)
            centre = self.piece_at(epsq)

            if left is not None and left.piece_type == PAWN and left.colour != centre.colour and rank(epsq - 1) == rank(epsq):
                moves.append(Move(epsq - 1, epsq + 8 if self.__turn else epsq - 8, en_passant=True))

            if right is not None and right.piece_type == PAWN and right.colour != centre.colour and rank(epsq + 1) == rank(epsq):
                moves.append(Move(epsq + 1, epsq + 8 if self.__turn else epsq - 8, en_passant=True))

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
    
    def enemy_attacked_squares(self):
        self.__turn = not self.__turn
        sqrs = self.generate_attacks_bb(no_king=True)
        self.__turn = not self.__turn
        return sqrs

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
    
    '''Castling Conditions: 
        - Empty squares between king and rook
        - Has castling rights
        - Cannot castle through check
        - Rook has to be on the home square
    '''
    def __generate_castling_rights(self):
        rights = [False, False] # Short, Long
        if self.__turn: # white
            if self.WShortCastle_bb & self.__empty_squares() == self.WShortCastle_bb and \
            self.__castling_rights[0] and \
            self.enemy_attacked_squares() & bb_from_sqrs([sq_num("f1"), sq_num("g1")]) == 0 and \
                self.piece_at(sq_num("h1")).piece_type == ROOK:
                rights[0] = True
            if self.WLongCastle_bb & self.__empty_squares() == self.WLongCastle_bb and \
            self.__castling_rights[1] and \
            self.enemy_attacked_squares() & bb_from_sqrs([sq_num("d1"), sq_num("c1")]) == 0 and \
                self.piece_at(sq_num("a1")).piece_type == ROOK:
                rights[1] = True
        else: # black
            if self.BShortCastle_bb & self.__empty_squares() == self.BShortCastle_bb and \
            self.__castling_rights[2] and \
            self.enemy_attacked_squares() & bb_from_sqrs([sq_num("f8"), sq_num("g8")]) == 0 and \
                self.piece_at(sq_num("h8")).piece_type == ROOK:
                rights[0] = True
            if self.BLongCastle_bb & self.__empty_squares() == self.BLongCastle_bb and \
            self.__castling_rights[3] and \
            self.enemy_attacked_squares() & bb_from_sqrs([sq_num("d8"), sq_num("c8")]) == 0 and \
                self.piece_at(sq_num("a8")).piece_type == ROOK:
                rights[1] = True
        return rights

    # Generate castling moves
    def generate_castling_moves(self):
        if self.in_check():
            return []
        moves = []
        castling_rights = self.__generate_castling_rights()
        if castling_rights[0]:
            moves.append(Move(sq_num("e1") if self.__turn else sq_num("e8"), sq_num("g1") if self.__turn else sq_num("g8"), castling=True))
        if castling_rights[1]:
            moves.append(Move(sq_num("e1") if self.__turn else sq_num("e8"), sq_num("c1") if self.__turn else sq_num("c8"), castling=True))
        return moves

    def generate_capture_bb(self):
        bb = 0
        for i, idx in enumerate(range(0 if self.__turn else 1, 12, 2)):
            for sq in self.__squares_from(self.__board_bb[idx]):
                bb |= self.__CAPTURE_FUNCS[i](sq)
        return bb

    def generate_attacks_bb(self, no_king=False, empty=False, protected=False):
        bb = 0
        for i, idx in enumerate(range(0 if self.__turn else 1, 12, 2)):
            for sq in self.__squares_from(self.__board_bb[idx]):
                bb |= self.__ATTACK_FUNCS[i](sq, no_king, empty, protected)
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
            self.push(move)
            if self.generate_capture_bb() & (self.__board_bb[10 if not self.__turn else 11]) == 0:
                legal_moves.append(move)
            self.pop()
        return legal_moves + self.generate_king_moves()

    def piece_at(self, sq):
        sq_bb = bb_from_sqrs([sq])
        for i in range(12):
            if self.__board_bb[i] & sq_bb != 0:
                return self.PIECES[i]

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

        # if move.uci() == "a2a4":
        #     pass

        s1, s2 = move.from_square, move.to_square
        p1, p2 = self.piece_at(s1), self.piece_at(s2)

        # Make the move
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

        # Log castling rights
        if p1.piece_type == KING:
            if p1.colour:
                self.__castling_rights[0] = False
                self.__castling_rights[1] = False
            else:
                self.__castling_rights[2] = False
                self.__castling_rights[3] = False
                    
        elif p1.piece_type == ROOK:
            if p1.colour:
                if file(s1) == "a":
                    self.__castling_rights[1] = False
                elif file(s1) == "h":
                    self.__castling_rights[0] = False
            else:
                if file(s1) == "a":
                    self.__castling_rights[3] = False
                elif file(s1) == "h":
                    self.__castling_rights[2] = False
        
        # Log en passant square
        if p1 is not None and p1.piece_type == PAWN and self.__is_double_push(move):
            self.__en_passant_square = s1 + (8 if self.__turn else -8)
        # if move.uci() == "a2a4":
        #     print(self.__en_passant_square)
        self.__move_stack.append(move)
        # if move.uci() == "a2a4":
        #     print(self.__en_passant_square)
        self.__state_stack.append([tuple(self.__board_bb), tuple(self.__castling_rights), self.__en_passant_square]) 
        # if move.uci() == "a2a4":
        #     print(self.__state_stack)
        self.__turn = not self.__turn # Update board turn

    # Remove move from move stack
    def pop(self):
        if self.__move_stack:  # move list is not empty
            self.__move_stack.pop()
            self.__state_stack.pop()
            last_state = self.__state_stack[-1]
            self.__board_bb = list(last_state[0])
            self.__castling_rights = list(last_state[1])
            self.__en_passant_square = last_state[2]
            self.__turn = not self.__turn

    def is_capture(self, move): # Is capture
        p2 = self.piece_at(move.to_square)
        if move.en_passant:
            return True
        elif p2 is not None:
            return True
        return False

    def is_check(self, move): # Is Check
        self.push(move)
        is_in_check = self.in_check()
        self.pop()
        return is_in_check
    
    def in_check(self): # In Check
        return self.enemy_attacked_squares() & (self.__board_bb[10 if self.__turn else 11]) != 0

    def set_fen(self, fen): # Set Fen

        self.__board_bb = [0 for _ in range(12)]
        args = fen.split(" ")
        pp, turn, castling, epts = args[0:4]
        mapping = {"P": 0, "p": 1, "N": 2, "n": 3, "B": 4, "b": 5, "R" : 6, "r" : 7, "Q" : 8, "q" : 9, "K" : 10, "k" : 11}

        # Setting up the Pieces
        for rn, rank in enumerate(pp.split("/")[::-1]): # iterate through each rank
            fn = 0
            for char in rank: # iterate through each character
                if char in "PNBRQKpnbrqk":
                    i = mapping[char]
                    self.__board_bb[i] = self.__add_piece(self.__board_bb[i], rn * 8 + fn)
                    fn += 1
                else:
                    fn += int(char)
        
        # Player's Turn
        self.__turn = turn == "w"

        # Castling Rights
        self.__castling_rights = ["K" in castling, "Q" in castling, "k" in castling, "q" in castling]

        # En Passant Square
        if epts != "-":
            self.__en_passant_square = sq_num(epts)

        # Set Base Fen
        self.__state_stack = [[self.__board_bb[:], self.__castling_rights, self.__en_passant_square]]
        
        print("FEN SET")
        
    def perft(self, depth):
        global nodes, captures, checks, en_passant, checkmates, log
        nodes = 0
        captures = 0
        checks = 0
        en_passant = 0
        checkmates = 0
        stime = time.perf_counter()
        log = set()
        self.__perft(depth)
        # return log
        return {"nodes": nodes, "captures": captures, "checks": checks, "en passant": en_passant, 
                "checkmates": checkmates, "time": time.perf_counter() - stime}

    def __perft(self, depth):
        global nodes, captures, checks, en_passant, checkmates

        if depth == 0:
            return

        for move in (moves := self.legal_moves):
            # print(depth, self.__state_stack)
            if depth == 1:
                if self.is_capture(move):
                    captures += 1
                if self.is_check(move):
                    checks += 1
                if self.is_en_passant(move):
                    en_passant += 1
                nodes += 1
                
            self.push(move)
            if depth == 1:
                log.add(tuple([i.uci() for i in list(self.__move_stack)]))
            self.__perft(depth - 1)
            self.pop()
        
        if len(moves) == 0:
            checkmates += 1


if __name__ in "__main__":

    board = Board()
    board.set_fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -")
    board.print_board()

    # print(board.perft(1))
    print(board.perft(2))
    # print(board.perft(3))
    # print(board.perft(4))
    # print(board.perft(5))

    # while True:
    
    #     stime = time.perf_counter_ns()
    
    #     board.print_board()
    #     print(board.generate_king_moves())
    #     # print(board.legal_moves)
    #     # print(board.in_check())
    #     # print(board.enemy_attacked_squares())
    
    #     print(f"time taken: {(time.perf_counter_ns() - stime) / 1e9}s")
    
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

    print("done")

'''

STARTING POSITION

v15
{'nodes': 20, 'captures': 0, 'checks': 0, 'en passant': 0, 'checkmates': 0, 'time': 0.041633300000000005}
{'nodes': 400, 'captures': 0, 'checks': 0, 'en passant': 0, 'checkmates': 0, 'time': 0.32299639999999996}
{'nodes': 8902, 'captures': 34, 'checks': 12, 'en passant': 0, 'checkmates': 0, 'time': 2.6004207}
{'nodes': 197281, 'captures': 1576, 'checks': 469, 'en passant': 0, 'checkmates': 0, 'time': 24.7565528}
{'nodes': 4865351, 'captures': 82461, 'checks': 27351, 'en passant': 0, 'checkmates': 8, 'time': 592.9917908}
done

v11

{'nodes': 20, 'captures': 0, 'checks': 0, 'en passant': 0, 'checkmates': 0, 'time': 0.0344046}
{'nodes': 400, 'captures': 0, 'checks': 0, 'en passant': 0, 'checkmates': 0, 'time': 0.23974059999999997}
{'nodes': 8902, 'captures': 34, 'checks': 12, 'en passant': 0, 'checkmates': 0, 'time': 1.9510216999999999}
{'nodes': 197281, 'captures': 1576, 'checks': 469, 'en passant': 0, 'checkmates': 0, 'time': 23.550980300000003}
{'nodes': 4865621, 'captures': 82719, 'checks': 27351, 'en passant': 258, 'checkmates': 8, 'time': 556.6171326}
done

PERFT 5 is INCORRECT...

POSITION 2

v15
{'nodes': 48, 'captures': 8, 'checks': 0, 'en passant': 0, 'checkmates': 0, 'time': 0.0849355}
{'nodes': 2038, 'captures': 350, 'checks': 3, 'en passant': 0, 'checkmates': 0, 'time': 1.1561373}
{'nodes': 97766, 'captures': 17047, 'checks': 993, 'en passant': 0, 'checkmates': 0, 'time': 18.6018411}
done

POSITION 5

v15
{'nodes': 44, 'captures': 6, 'checks': 0, 'en passant': 0, 'checkmates': 0, 'time': 0.0785979}
{'nodes': 1486, 'captures': 222, 'checks': 117, 'en passant': 0, 'checkmates': 0, 'time': 0.7398969000000001}
{'nodes': 62379, 'captures': 8517, 'checks': 1201, 'en passant': 0, 'checkmates': 0, 'time': 8.904277800000001}
{'nodes': 2103487, 'captures': 296153, 'checks': 158486, 'en passant': 0, 'checkmates': 44, 'time': 268.09974950000003}
done

WHICH IS CORRECT !!!

'''