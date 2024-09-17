import json
import time
from functools import reduce

'''Debug Functions'''

def bin64_to_str(bin64):
    return str(bin(bin64))[2:].zfill(64)

def str_to_bin64(s):
    total = 0
    for idx, val in enumerate(s):
        total += 2 ** idx if val == "1" else 0
    return total

def print_bb(bb):
    s = bin64_to_str(bb)
    for c, char in enumerate(s):
        print(char, end='')
        if (c + 1) % 8 == 0:
            print()

'''Bitwise Operations'''

BB_SQRS = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 
           131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 
           67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648, 4294967296, 
           8589934592, 17179869184, 34359738368, 68719476736, 137438953472, 274877906944, 
           549755813888, 1099511627776, 2199023255552, 4398046511104, 8796093022208, 
           17592186044416, 35184372088832, 70368744177664, 140737488355328, 281474976710656, 
           562949953421312, 1125899906842624, 2251799813685248, 4503599627370496, 9007199254740992, 
           18014398509481984, 36028797018963968, 72057594037927936, 144115188075855872, 
           288230376151711744, 576460752303423488, 1152921504606846976, 2305843009213693952, 
           4611686018427387904, 9223372036854775808]

BB_RANKS = [255, 65280, 16711680, 4278190080, 1095216660480, 280375465082880, 71776119061217280, 18374686479671623680]

BB_ALL = 2**64 - 1

BB_DIAG_MASKS = [18049651735527936, 70506452091904, 275415828992, 1075975168, 38021120, 8657588224, 
                 2216338399232, 567382630219776, 9024825867763712, 18049651735527424, 70506452221952, 
                 275449643008, 9733406720, 2216342585344, 567382630203392, 1134765260406784, 4512412933816832, 
                 9024825867633664, 18049651768822272, 70515108615168, 2491752130560, 567383701868544, 
                 1134765256220672, 2269530512441344, 2256206450263040, 4512412900526080, 9024834391117824, 
                 18051867805491712, 637888545440768, 1135039602493440, 2269529440784384, 4539058881568768, 
                 1128098963916800, 2256197927833600, 4514594912477184, 9592139778506752, 19184279556981248, 
                 2339762086609920, 4538784537380864, 9077569074761728, 562958610993152, 1125917221986304, 
                 2814792987328512, 5629586008178688, 11259172008099840, 22518341868716544, 9007336962655232, 
                 18014673925310464, 2216338399232, 4432676798464, 11064376819712, 22137335185408, 44272556441600, 
                 87995357200384, 35253226045952, 70506452091904, 567382630219776, 1134765260406784, 2832480465846272, 
                 5667157807464448, 11333774449049600, 22526811443298304, 9024825867763712, 18049651735527936]

BB_RF_MASKS = [282578800148862, 565157600297596, 1130315200595066, 2260630401190006, 4521260802379886, 9042521604759646, 
               18085043209519166, 36170086419038334, 282578800180736, 565157600328704, 1130315200625152, 2260630401218048, 
               4521260802403840, 9042521604775424, 18085043209518592, 36170086419037696, 282578808340736, 565157608292864, 
               1130315208328192, 2260630408398848, 4521260808540160, 9042521608822784, 18085043209388032, 36170086418907136, 
               282580897300736, 565159647117824, 1130317180306432, 2260632246683648, 4521262379438080, 9042522644946944, 
               18085043175964672, 36170086385483776, 283115671060736, 565681586307584, 1130822006735872, 2261102847592448, 
               4521664529305600, 9042787892731904, 18085034619584512, 36170077829103616, 420017753620736, 699298018886144, 
               1260057572672512, 2381576680245248, 4624614895390720, 9110691325681664, 18082844186263552, 36167887395782656, 
               35466950888980736, 34905104758997504, 34344362452452352, 33222877839362048, 30979908613181440, 26493970160820224, 
               17522093256097792, 35607136465616896, 9079539427579068672, 8935706818303361536, 8792156787827803136, 
               8505056726876686336, 7930856604974452736, 6782456361169985536, 4485655873561051136, 9115426935197958144]

def bsf(x):
    if x == 0:
        return None
    return x.bit_length() - 1

def bsr(x):
    if x == 0:
        return None
    return (x&-x).bit_length() - 1

def bb_from_sqrs(sqrs):
    bb = 0
    for sq in sqrs:
        bb |= BB_SQRS[sq]
    return bb

def add_piece(bb, sq): # Add piece
    bb |= BB_SQRS[sq]
    return bb

def remove_piece(bb, sq): # Remove piece
    bb ^= BB_SQRS[sq]
    return bb

def move_piece(bb, sqs): # Move piece
    s1, s2 = sqs
    bb = remove_piece(bb, s1)
    bb = add_piece(bb, s2)
    return bb

def squares_from(bb): # Get squares from bitboard
    while bb != 0:
        sq = bsf(bb)
        bb = remove_piece(bb, sq := bsf(bb))
        yield sq

'''Other Functions'''

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
    with open("resources/" + file_name) as f:
        data = json.load(f)
    return dict(zip(map(int, data), data.values()))

def open_jsonl(file_name):
    with open("resources/" + file_name) as f:
        data = json.load(f)
    return [dict(zip(map(int, d), d.values())) for d in data]

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

'''Constants'''

PAWN = 2
KNIGHT = 3
BISHOP = 4
ROOK = 5
QUEEN = 6
KING = 7

WHITE = True
BLACK = False

files = ["a", "b", "c", "d", "e", "f", "g", "h"]

PAWN_ATK_WHITE_SQRS = open_json("pawn_atk_white_sqrs.json")
PAWN_ATK_BLACK_SQRS = open_json("pawn_atk_black_sqrs.json")
KNIGHT_SQRS = open_json("knight_sqrs.json")
KING_SQRS = open_json("king_sqrs.json")
BISHOP_SQRS = open_json("bishop_sqrs.json")
ROOK_SQRS = open_json("rook_sqrs.json")

BB_DIAG_ATTACKS = open_jsonl("diag_attacks.json")
BB_RF_ATTACKS = open_jsonl("rf_attacks.json")

piece_chars = {PAWN: "P", KNIGHT: "N", BISHOP: "B", ROOK: "R", QUEEN: "Q", KING: "K"}

'''Classes'''

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

'''Main Board Class & Move Generator'''

class Board:

    PIECES = [Piece(PAWN, WHITE), Piece(PAWN, BLACK), Piece(KNIGHT, WHITE), Piece(KNIGHT, BLACK), Piece(BISHOP, WHITE), Piece(BISHOP, BLACK),
              Piece(ROOK, WHITE), Piece(ROOK, BLACK), Piece(QUEEN, WHITE), Piece(QUEEN, BLACK), Piece(KING, WHITE), Piece(KING, BLACK)]
    
    WShortCastle_bb = bb_from_sqrs([sq_num("f1"), sq_num("g1")])
    WLongCastle_bb = bb_from_sqrs([sq_num("b1"), sq_num("c1"), sq_num("d1")])
    BShortCastle_bb = bb_from_sqrs([sq_num("f8"), sq_num("g8")])
    BLongCastle_bb = bb_from_sqrs([sq_num("b8"), sq_num("c8"), sq_num("d8")])

    def __init__(self): # Constructor

        # main states for FEN: board, turn, castling rights, en passant square
        self.__board_bb = [BB_RANKS[1], BB_RANKS[6],
                           BB_SQRS[sq_num("b1")] | BB_SQRS[sq_num("g1")], BB_SQRS[sq_num("b8")] | BB_SQRS[sq_num("g8")],
                           BB_SQRS[sq_num("c1")] | BB_SQRS[sq_num("f1")], BB_SQRS[sq_num("c8")] | BB_SQRS[sq_num("f8")],
                           BB_SQRS[sq_num("a1")] | BB_SQRS[sq_num("h1")], BB_SQRS[sq_num("a8")] | BB_SQRS[sq_num("h8")],
                           BB_SQRS[sq_num("d1")] , BB_SQRS[sq_num("d8")],
                           BB_SQRS[sq_num("e1")] , BB_SQRS[sq_num("e8")]]
        self.__turn = WHITE
        self.__castling_rights = [True, True, True, True]
        self.__en_passant_square = None

        # working states
        self.__white_pieces = reduce(lambda x, y : x | y, [self.__board_bb[i] for i in range(0, 12, 2)])
        self.__black_pieces = reduce(lambda x, y : x | y, [self.__board_bb[i] for i in range(1, 12, 2)])
        self.__white_pieces_no_king = reduce(lambda x, y : x | y, [self.__board_bb[i] for i in range(0, 10, 2)])
        self.__black_pieces_no_king = reduce(lambda x, y : x | y, [self.__board_bb[i] for i in range(1, 10, 2)])
        self.__isqrs = 0 # cache the intersection squares

        # stacks
        self.__move_stack = []
        self.__state_stack = [[self.__board_bb[:], self.__castling_rights, self.__en_passant_square, 
                               self.__white_pieces, self.__black_pieces, self.__white_pieces_no_king, self.__black_pieces_no_king]]

        # function lists
        self.__CAPTURE_FUNCS = [self.__pawn_atk_squares, self.__knight_atk_squares, self.__bishop_atk_squares, 
                                self.__rook_atk_squares, self.__queen_atk_squares, self.__king_atk_squares]
        self.__ATTACK_FUNCS = [self.__pawn_atk_squares, self.__knight_squares, self.__bishop_squares, 
                               self.__rook_squares, self.__queen_squares, self.__king_squares]

        self.nodes = 0

    def __empty_squares(self): # Empty squares
        return ~self.__blockers()

    def __blockers(self, no_enemy_king=False): # Blockers with options
        if no_enemy_king:
            return self.__white_pieces | self.__black_pieces_no_king if self.__turn else self.__white_pieces_no_king | self.__black_pieces
        return self.__white_pieces | self.__black_pieces

    def __masked_blockers(self, mask, no_enemy_king=False): # Masked blockers
        return self.__blockers(no_enemy_king) & mask

    def __enemy_squares(self): # Enemy pieces
        return self.__black_pieces if self.__turn else self.__white_pieces

    def __friendly_squares(self): # Friendly pieces
        return self.__white_pieces if self.__turn else self.__black_pieces

    def __intersection_sqrs(self, protected, isPawn=False): # Get intersection squares with options
        if protected:
            return self.__friendly_squares()
        return (self.__empty_squares() | self.__enemy_squares()) if not isPawn else self.__enemy_squares()

    def __pawn_squares(self, ranks): # Get pawn squares
        if ranks == 1:
            bb = self.__board_bb[0 if self.__turn else 1]
        else:
            bb = self.__board_bb[0 if self.__turn else 1] & BB_RANKS[1 if self.__turn else 6]
        bb = bb << 8 * ranks if self.__turn else bb >> 8 * ranks
        return bb & self.__empty_squares()

    def __pawn_atk_squares(self, sq, no_king=False, protected=False): # Get pawn attack squares
        if self.__turn:
            return PAWN_ATK_WHITE_SQRS[sq] & self.__intersection_sqrs(protected, isPawn=True if not no_king else False)
        else:
            return PAWN_ATK_BLACK_SQRS[sq] & self.__intersection_sqrs(protected, isPawn=True if not no_king else False)

    def __knight_squares(self, sq, no_king=False, protected=False): # Get knight squares
        return KNIGHT_SQRS[sq] &  self.__isqrs

    def __knight_atk_squares(self, sq): # Get knight attack squares
        return KNIGHT_SQRS[sq] & self.__enemy_squares()

    def __king_squares(self, sq, no_king=False, protected=False): # Get king squares
        return KING_SQRS[sq] & self.__intersection_sqrs(protected)

    def __king_atk_squares(self, sq): # Get king attack squares
        return KING_SQRS[sq] & self.__enemy_squares()

    def __bishop_squares(self, sq, no_king=False, protected=False): # Get bishop squares
        return self.__isqrs & BB_DIAG_ATTACKS[sq][BB_DIAG_MASKS[sq] & self.__blockers(no_enemy_king=no_king)]

    def __bishop_atk_squares(self, sq): # Get bishop attack squares

        bb = 0

        # North-west
        nw_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["NW"])
        blocker = bsf(nw_blockers)
        bb |= BB_SQRS[blocker] if blocker is not None else 0

        # North-east
        ne_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["NE"])
        blocker = bsf(ne_blockers)
        bb |= BB_SQRS[blocker] if blocker is not None else 0

        # South-west
        sw_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["SW"])
        blocker = bsr(sw_blockers)
        bb |= BB_SQRS[blocker] if blocker is not None else 0

        # South-east
        se_blockers = self.__masked_blockers(BISHOP_SQRS[sq]["SE"])
        blocker = bsr(se_blockers)
        bb |= BB_SQRS[blocker] if blocker is not None else 0

        return bb & self.__enemy_squares()

    def __rook_squares(self, sq, no_king=False, protected=False): # Get rook squares
        return self.__isqrs & BB_RF_ATTACKS[sq][BB_RF_MASKS[sq] & self.__blockers(no_enemy_king=no_king)]

    def __rook_atk_squares(self, sq): # Get rook attack squares

        bb = 0

        # North
        n_blockers = self.__masked_blockers(ROOK_SQRS[sq]["N"])
        blocker = bsf(n_blockers)
        bb |= BB_SQRS[blocker] if blocker is not None else 0

        # East
        e_blockers = self.__masked_blockers(ROOK_SQRS[sq]["E"])
        blocker = bsr(e_blockers)
        bb |= BB_SQRS[blocker] if blocker is not None else 0

        # South
        s_blockers = self.__masked_blockers(ROOK_SQRS[sq]["S"])
        blocker = bsr(s_blockers)
        bb |= BB_SQRS[blocker] if blocker is not None else 0

        # West
        w_blockers = self.__masked_blockers(ROOK_SQRS[sq]["W"])
        blocker = bsf(w_blockers)
        bb |= BB_SQRS[blocker] if blocker is not None else 0

        return bb & self.__enemy_squares()

    def __queen_squares(self, sq, no_king=False, protected=False): # Get queen squares
        return self.__bishop_squares(sq, no_king, protected) | self.__rook_squares(sq, no_king, protected)

    def __queen_atk_squares(self, sq): # Get queen attack squares
        return self.__bishop_atk_squares(sq) | self.__rook_atk_squares(sq)

    def __is_double_push(self, move): # Check if pawn move is a double push
        s1, s2 = move.from_square, move.to_square
        if self.piece_at(s2) is None:
            return False
        if self.piece_at(s2).piece_type == PAWN and abs(s2 - s1) == 16:
            return True
        return False

    def is_en_passant(self, move): # Check if move is en passant
        s1, s2 = move.from_square, move.to_square
        if self.piece_at(s1) is None:
            return False
        if self.piece_at(s1).piece_type == PAWN and self.piece_at(s2) is None and abs(s2 - s1) not in (8, 16):
            return True
        return False

    def is_castling(self, move): # Check if move is castling
        s1, s2 = move.from_square, move.to_square
        if abs(s2 - s1) == 2 and self.piece_at(s1).piece_type == KING:
            return True
        return False

    def generate_pawn_moves(self): # Generate pawn moves
        moves = []

        # Normal push
        for sq in squares_from(self.__pawn_squares(1)):
            orig_sq = sq - 8 if self.__turn else sq + 8
            if (self.__turn and rank(sq) == "8") or (not self.__turn and rank(sq) == "1"):  # promotion
                for piece in (KNIGHT, BISHOP, ROOK, QUEEN):
                    moves.append(Move(orig_sq, sq, promotion=piece))
            else:
                moves.append(Move(orig_sq, sq))

        # Double push
        for sq in squares_from(self.__pawn_squares(2)):
            orig_sq = sq - 16 if self.__turn else sq + 16
            sec_sq = sq - 8 if self.__turn else sq + 8
            if self.__empty_squares() & BB_SQRS[sec_sq] != 0:
                moves.append(Move(orig_sq, sq))

        # Captures
        for Psq in squares_from(self.__board_bb[0 if self.__turn else 1]):
            for sq in squares_from(self.__pawn_atk_squares(Psq)):
                if (self.__turn and rank(sq) == "8") or (not self.__turn and rank(sq) == "1"):  # promotion
                    for piece in (KNIGHT, BISHOP, ROOK, QUEEN):
                        moves.append(Move(Psq, sq, promotion=piece))
                else:
                    moves.append(Move(Psq, sq))

        # En Passant
        epsq = self.__en_passant_square
        if epsq is not None:
            pattack_sqrs = []
            if self.__turn: # white
                if file(epsq) != "a" : # left pawn
                    pattack_sqrs.append(epsq - 9)
                if file(epsq) != "h": # right pawn
                    pattack_sqrs.append(epsq - 7)
            else: # black
                if file(epsq) != "a": # left pawn
                    pattack_sqrs.append(epsq + 7)
                if file(epsq) != "h": # right pawn
                    pattack_sqrs.append(epsq + 9)
            for psq in pattack_sqrs:
                if (p := self.piece_at(psq)) is not None and p.piece_type == PAWN and p.colour == self.__turn:
                    moves.append(Move(psq, epsq, en_passant=True))

        return moves

    def generate_knight_moves(self): # Generate knight moves
        moves = []

        for Nsq in squares_from(self.__board_bb[2 if self.__turn else 3]):
            for sq in squares_from(self.__knight_squares(Nsq)):
                moves.append(Move(Nsq, sq))

        return moves

    def generate_king_moves(self): # Generate king moves
        moves = []

        self.__turn = not self.__turn

        non_legal_sqrs = self.generate_attacks_bb(no_king=True)
        protected_sqrs = self.generate_attacks_bb(no_king=True, protected=True)

        self.__turn = not self.__turn

        for Ksq in squares_from(self.__board_bb[10 if self.__turn else 11]):
            for sq in squares_from(self.__king_squares(Ksq) & ~(non_legal_sqrs | protected_sqrs)):
                moves.append(Move(Ksq, sq))

        return moves
    
    def enemy_attacked_squares(self): # Get enemy attacked squares, removing king from board
        self.__turn = not self.__turn
        sqrs = self.generate_attacks_bb(no_king=True)
        self.__turn = not self.__turn
        return sqrs

    def generate_bishop_moves(self): # Generate bishop moves
        moves = []

        for Bsq in squares_from(self.__board_bb[4 if self.__turn else 5]):
            for sq in squares_from(self.__bishop_squares(Bsq)):
                moves.append(Move(Bsq, sq))

        return moves

    def generate_rook_moves(self): # Generate rook moves
        moves = []

        for Rsq in squares_from(self.__board_bb[6 if self.__turn else 7]):
            for sq in squares_from(self.__rook_squares(Rsq)):
                moves.append(Move(Rsq, sq))

        return moves

    def generate_queen_moves(self): # Generate queen moves
        moves = []

        for Qsq in squares_from(self.__board_bb[8 if self.__turn else 9]):
            for sq in squares_from(self.__queen_squares(Qsq)):
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

    # Generate captures bitboard
    def generate_capture_bb(self):
        bb = 0
        for i, idx in enumerate(range(0 if self.__turn else 1, 12, 2)):
            for sq in squares_from(self.__board_bb[idx]):
                bb |= self.__CAPTURE_FUNCS[i](sq)
        return bb

    # Generate attacks bitboard
    def generate_attacks_bb(self, no_king=False, protected=False):
        bb = 0
        self.__isqrs = self.__intersection_sqrs(protected) # set isqrs to protected mode
        for i, idx in enumerate(range(0 if self.__turn else 1, 12, 2)):
            for sq in squares_from(self.__board_bb[idx]):
                bb |= self.__ATTACK_FUNCS[i](sq, no_king, protected)
        return bb

    @property
    def pseudo_legal_moves(self): # Pseudo-legal moves
        self.__isqrs = self.__intersection_sqrs(protected=False) # set isqrs to normal mode
        return self.generate_pawn_moves() + self.generate_knight_moves() + self.generate_bishop_moves() + \
               self.generate_rook_moves() + self.generate_queen_moves() + self.generate_castling_moves()

    @property
    def legal_moves(self): # Legal moves
        pseudo_legal_moves = self.pseudo_legal_moves
        legal_moves = []
        for move in pseudo_legal_moves:
            self.push(move)
            if self.generate_capture_bb() & (self.__board_bb[10 if not self.__turn else 11]) == 0:
                legal_moves.append(move)
            self.pop()
        return legal_moves + self.generate_king_moves()

    def piece_at(self, sq): # Get piece at square
        sq_bb = bb_from_sqrs([sq])
        for i in range(12):
            if self.__board_bb[i] & sq_bb != 0:
                return self.PIECES[i]

    def __get_board(self): # Get board

        grid = []
        for row in range(8):
            grid.append([])
            for col in range(8):
                sq = row * 8 + col
                grid[-1].append(self.piece_at(sq))

        return grid

    def print_board(self): # Print the board
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

    def __update_bb(self, piece, func, params): # Update bitboard with function
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

        # update supporting bitboards
        if piece.colour:
            self.__white_pieces = func(self.__white_pieces, params)
            if pt != KING:
                self.__white_pieces_no_king = func(self.__white_pieces_no_king, params)
        else:
            self.__black_pieces = func(self.__black_pieces, params)
            if pt != KING:
                self.__black_pieces_no_king = func(self.__black_pieces_no_king, params)

    def push(self, move): # Push move

        s1, s2 = move.from_square, move.to_square
        p1, p2 = self.piece_at(s1), self.piece_at(s2)

        # Make the move
        if move.castling:
            if file(s2) == "g":  # short castle
                self.__update_bb(Piece(ROOK, self.__turn), move_piece, (s1 + 3, s2 - 1))
            elif file(s2) == "c":  # long castle
                self.__update_bb(Piece(ROOK, self.__turn), move_piece, (s1 - 4, s2 + 1))

        if move.promotion:  # move a piece and promote
            self.__update_bb(p1, remove_piece, s1)
            self.__update_bb(Piece(move.promotion, p1.colour), add_piece, s2)
        else:
            self.__update_bb(p1, move_piece, (s1, s2))  # move a piece normally
        if p2 is not None:  # normal capture
            self.__update_bb(p2, remove_piece, s2)
        if move.en_passant:  # en passant move only
            self.__update_bb(Piece(PAWN, not self.__turn), remove_piece, s2 - 8 if self.__turn else s2 + 8)

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
        else:
            self.__en_passant_square = None

        self.__move_stack.append(move)
        self.__state_stack.append([tuple(self.__board_bb), tuple(self.__castling_rights), self.__en_passant_square, 
                                   self.__white_pieces, self.__black_pieces, self.__white_pieces_no_king, self.__black_pieces_no_king]) 
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
            self.__white_pieces = last_state[3]
            self.__black_pieces = last_state[4]
            self.__white_pieces_no_king = last_state[5]
            self.__black_pieces_no_king = last_state[6]
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
    
    def is_checkmate(self): # Is Checkmate
        return len(self.legal_moves) == 0 and self.in_check()

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
                    self.__board_bb[i] = add_piece(self.__board_bb[i], rn * 8 + fn)
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

        # Working States
        self.__white_pieces = reduce(lambda x, y : x | y, [self.__board_bb[i] for i in range(0, 12, 2)])
        self.__black_pieces = reduce(lambda x, y : x | y, [self.__board_bb[i] for i in range(1, 12, 2)])
        self.__white_pieces_no_king = reduce(lambda x, y : x | y, [self.__board_bb[i] for i in range(0, 10, 2)])
        self.__black_pieces_no_king = reduce(lambda x, y : x | y, [self.__board_bb[i] for i in range(1, 10, 2)])

        # Set Base Fen
        self.__state_stack = [[self.__board_bb[:], self.__castling_rights, self.__en_passant_square, 
                               self.__white_pieces, self.__black_pieces, self.__white_pieces_no_king, self.__black_pieces_no_king]]
        
        print("FEN SET")
        
    def perft(self, depth): # Root Perft
        global nodes, captures, checks, en_passant, checkmates, log
        nodes = 0
        captures = 0
        checks = 0
        en_passant = 0
        checkmates = 0
        stime = time.perf_counter()
        # log = set()
        self.__perft(depth)
        # return log
        return {"nodes": nodes, "captures": captures, "checks": checks, "en passant": en_passant, "time": time.perf_counter() - stime}

    def __perft(self, depth): # Perft Test
        global nodes, captures, checks, en_passant, checkmates

        if depth == 0:
            return

        for move in self.legal_moves:
            if depth == 1:
                if self.is_capture(move):
                    captures += 1
                if self.is_check(move):
                    checks += 1
                if self.is_en_passant(move):
                    en_passant += 1
                nodes += 1
                
            self.push(move)
            # if depth == 1:
            #     log.add(tuple([i.uci() for i in list(self.__move_stack)]))
            self.__perft(depth - 1)
            self.pop()


if __name__ in "__main__":

    board = Board()
    # board.set_fen("r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10")
    board.print_board()
    # print(board.legal_moves)

    print(board.perft(1))
    print(board.perft(2))
    print(board.perft(3))
    print(board.perft(4))
    print(board.perft(5))

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

v31
{'nodes': 20, 'captures': 0, 'checks': 0, 'en passant': 0, 'time': 0.0061465}
{'nodes': 400, 'captures': 0, 'checks': 0, 'en passant': 0, 'time': 0.13669219999999999}
{'nodes': 8902, 'captures': 34, 'checks': 12, 'en passant': 0, 'time': 0.6387716}
{'nodes': 197281, 'captures': 1576, 'checks': 469, 'en passant': 0, 'time': 3.3308638999999998}
{'nodes': 4865609, 'captures': 82719, 'checks': 27351, 'en passant': 258, 'time': 59.9858959}
done

v30
{'nodes': 20, 'captures': 0, 'checks': 0, 'en passant': 0, 'time': 0.0084517}
{'nodes': 400, 'captures': 0, 'checks': 0, 'en passant': 0, 'time': 0.14967260000000002}
{'nodes': 8902, 'captures': 34, 'checks': 12, 'en passant': 0, 'time': 0.7153956}
{'nodes': 197281, 'captures': 1576, 'checks': 469, 'en passant': 0, 'time': 3.4523732}
{'nodes': 4865609, 'captures': 82719, 'checks': 27351, 'en passant': 258, 'time': 66.13311870000001}
done

v28
{'nodes': 20, 'captures': 0, 'checks': 0, 'en passant': 0, 'time': 0.008700999999999999}
{'nodes': 400, 'captures': 0, 'checks': 0, 'en passant': 0, 'time': 0.12397369999999999}
{'nodes': 8902, 'captures': 34, 'checks': 12, 'en passant': 0, 'time': 0.9454498}
{'nodes': 197281, 'captures': 1576, 'checks': 469, 'en passant': 0, 'time': 3.6886577}
{'nodes': 4865609, 'captures': 82719, 'checks': 27351, 'en passant': 258, 'time': 78.8998938}
done

POSITION 2

v30
{'nodes': 48, 'captures': 8, 'checks': 0, 'en passant': 0, 'time': 0.0141156}
{'nodes': 2039, 'captures': 351, 'checks': 3, 'en passant': 1, 'time': 0.4508072}
{'nodes': 97862, 'captures': 17102, 'checks': 993, 'en passant': 45, 'time': 3.0486984}
{'nodes': 4085603, 'captures': 757163, 'checks': 25523, 'en passant': 1929, 'time': 62.2310165}
done

v25
{'nodes': 48, 'captures': 8, 'checks': 0, 'en passant': 0, 'time': 0.0168245}
{'nodes': 2039, 'captures': 351, 'checks': 3, 'en passant': 1, 'time': 0.5135089}
{'nodes': 97862, 'captures': 17102, 'checks': 993, 'en passant': 45, 'time': 4.0875164}
{'nodes': 4085603, 'captures': 757163, 'checks': 25523, 'en passant': 1929, 'time': 77.2409586}
done

POSITION 3

v30
{'nodes': 14, 'captures': 1, 'checks': 2, 'en passant': 0, 'time': 0.0029706}
{'nodes': 191, 'captures': 14, 'checks': 10, 'en passant': 0, 'time': 0.034503900000000004}
{'nodes': 2812, 'captures': 209, 'checks': 267, 'en passant': 2, 'time': 0.2870311}
{'nodes': 43238, 'captures': 3348, 'checks': 1680, 'en passant': 123, 'time': 0.9161764000000001}
{'nodes': 674624, 'captures': 52051, 'checks': 52950, 'en passant': 1165, 'time': 6.7340271000000005}
done

v27
{'nodes': 14, 'captures': 1, 'checks': 2, 'en passant': 0, 'time': 0.0038778}
{'nodes': 191, 'captures': 14, 'checks': 10, 'en passant': 0, 'time': 0.033395100000000004}
{'nodes': 2812, 'captures': 209, 'checks': 267, 'en passant': 2, 'time': 0.29157109999999997}
{'nodes': 43238, 'captures': 3348, 'checks': 1680, 'en passant': 123, 'time': 0.8426283}
{'nodes': 674624, 'captures': 52051, 'checks': 52950, 'en passant': 1165, 'time': 4.358478}
done

POSITION 4

v30
{'nodes': 6, 'captures': 0, 'checks': 0, 'en passant': 0, 'time': 0.0059723}
{'nodes': 264, 'captures': 87, 'checks': 10, 'en passant': 0, 'time': 0.107778}
{'nodes': 9467, 'captures': 1021, 'checks': 38, 'en passant': 4, 'time': 0.9841846}
{'nodes': 422333, 'captures': 131393, 'checks': 15492, 'en passant': 0, 'time': 8.1295055}
done

v29
{'nodes': 6, 'captures': 0, 'checks': 0, 'en passant': 0, 'time': 0.0061558}
{'nodes': 264, 'captures': 87, 'checks': 10, 'en passant': 0, 'time': 0.1263024}
{'nodes': 9467, 'captures': 1021, 'checks': 38, 'en passant': 4, 'time': 1.2168419}
{'nodes': 422333, 'captures': 131393, 'checks': 15492, 'en passant': 0, 'time': 10.934938899999999}
done

POSITION 5

v30
{'nodes': 44, 'captures': 6, 'checks': 0, 'en passant': 0, 'time': 0.0114798}
{'nodes': 1486, 'captures': 222, 'checks': 117, 'en passant': 0, 'time': 0.26639569999999996}
{'nodes': 62379, 'captures': 8517, 'checks': 1201, 'en passant': 0, 'time': 2.3496254}
{'nodes': 2103487, 'captures': 296153, 'checks': 158486, 'en passant': 0, 'time': 31.6454454}
done

v27
{'nodes': 44, 'captures': 6, 'checks': 0, 'en passant': 0, 'time': 0.015218500000000001}
{'nodes': 1486, 'captures': 222, 'checks': 117, 'en passant': 0, 'time': 0.32559879999999997}
{'nodes': 62379, 'captures': 8517, 'checks': 1201, 'en passant': 0, 'time': 2.1024192000000004}
{'nodes': 2103487, 'captures': 296153, 'checks': 158486, 'en passant': 0, 'time': 37.5346426}
done

POSITION 6

v30
{'nodes': 46, 'captures': 4, 'checks': 1, 'en passant': 0, 'time': 0.011433200000000001}
{'nodes': 2079, 'captures': 203, 'checks': 40, 'en passant': 0, 'time': 0.3005892}
{'nodes': 89890, 'captures': 9470, 'checks': 1783, 'en passant': 0, 'time': 2.6787666000000003}
{'nodes': 3894594, 'captures': 440388, 'checks': 68985, 'en passant': 0, 'time': 33.527477}
done

v29
{'nodes': 46, 'captures': 4, 'checks': 1, 'en passant': 0, 'time': 0.0163923}
{'nodes': 2079, 'captures': 203, 'checks': 40, 'en passant': 0, 'time': 0.3968527}
{'nodes': 89890, 'captures': 9470, 'checks': 1783, 'en passant': 0, 'time': 3.6832088}
{'nodes': 3894594, 'captures': 440388, 'checks': 68985, 'en passant': 0, 'time': 45.2799747}
done

'''