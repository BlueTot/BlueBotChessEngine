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

PAWN_ATK_WHITE_SQRS = {0: 18014398509481984, 1: 45035996273704960, 2: 22517998136852480, 3: 11258999068426240, 4: 5629499534213120, 5: 2814749767106560, 6: 1407374883553280, 7: 562949953421312,
                       8: 70368744177664, 9: 175921860444160, 10: 87960930222080, 11: 43980465111040, 12: 21990232555520, 13: 10995116277760, 14: 5497558138880, 15: 2199023255552,
                       16: 274877906944, 17: 687194767360, 18: 343597383680, 19: 171798691840, 20: 85899345920, 21: 42949672960, 22: 21474836480, 23: 8589934592,
                       24: 1073741824, 25: 2684354560, 26: 1342177280, 27: 671088640, 28: 335544320, 29: 167772160, 30: 83886080, 31: 33554432,
                       32: 4194304, 33: 10485760, 34: 5242880, 35: 2621440, 36: 1310720, 37: 655360, 38: 327680, 39: 131072,
                       40: 16384, 41: 40960, 42: 20480, 43: 10240, 44: 5120, 45: 2560, 46: 1280, 47: 512,
                       48: 64, 49: 160, 50: 80, 51: 40, 52: 20, 53: 10, 54: 5, 55: 2,
                       56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0}

PAWN_ATK_BLACK_SQRS = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0,
                       8: 4611686018427387904, 9: 11529215046068469760, 10: 5764607523034234880, 11: 2882303761517117440, 12: 1441151880758558720, 13: 720575940379279360, 14: 360287970189639680, 15: 144115188075855872,
                       16: 18014398509481984, 17: 45035996273704960, 18: 22517998136852480, 19: 11258999068426240, 20: 5629499534213120, 21: 2814749767106560, 22: 1407374883553280, 23: 562949953421312,
                       24: 70368744177664, 25: 175921860444160, 26: 87960930222080, 27: 43980465111040, 28: 21990232555520, 29: 10995116277760, 30: 5497558138880, 31: 2199023255552,
                       32: 274877906944, 33: 687194767360, 34: 343597383680, 35: 171798691840, 36: 85899345920, 37: 42949672960, 38: 21474836480, 39: 8589934592,
                       40: 1073741824, 41: 2684354560, 42: 1342177280, 43: 671088640, 44: 335544320, 45: 167772160, 46: 83886080, 47: 33554432,
                       48: 4194304, 49: 10485760, 50: 5242880, 51: 2621440, 52: 1310720, 53: 655360, 54: 327680, 55: 131072,
                       56: 16384, 57: 40960, 58: 20480, 59: 10240, 60: 5120, 61: 2560, 62: 1280, 63: 512}

KNIGHT_SQRS = {0: 9077567998918656, 1: 4679521487814656, 2: 38368557762871296, 3: 19184278881435648, 4: 9592139440717824, 5: 4796069720358912, 6: 2257297371824128, 7: 1128098930098176,
               8: 2305878468463689728, 9: 1152939783987658752, 10: 9799982666336960512, 11: 4899991333168480256, 12: 2449995666584240128, 13: 1224997833292120064, 14: 576469569871282176, 15: 288234782788157440,
               16: 4620693356194824192, 17: 11533718717099671552, 18: 5802888705324613632, 19: 2901444352662306816, 20: 1450722176331153408, 21: 725361088165576704, 22: 362539804446949376, 23: 145241105196122112,
               24: 18049583422636032, 25: 45053588738670592, 26: 22667534005174272, 27: 11333767002587136, 28: 5666883501293568, 29: 2833441750646784, 30: 1416171111120896, 31: 567348067172352,
               32: 70506185244672, 33: 175990581010432, 34: 88545054707712, 35: 44272527353856, 36: 22136263676928, 37: 11068131838464, 38: 5531918402816, 39: 2216203387392,
               40: 275414786112, 41: 687463207072, 42: 345879119952, 43: 172939559976, 44: 86469779988, 45: 43234889994, 46: 21609056261, 47: 8657044482,
               48: 1075839008, 49: 2685403152, 50: 1351090312, 51: 675545156, 52: 337772578, 53: 168886289, 54: 84410376, 55: 33816580,
               56: 4202496, 57: 10489856, 58: 5277696, 59: 2638848, 60: 1319424, 61: 659712, 62: 329728, 63: 132096}

KING_SQRS = {0: 4665729213955833856, 1: 11592265440851656704, 2: 5796132720425828352, 3: 2898066360212914176, 4: 1449033180106457088, 5: 724516590053228544, 6: 362258295026614272, 7: 144959613005987840,
             8: 13853283560024178688, 9: 16186183351374184448, 10: 8093091675687092224, 11: 4046545837843546112, 12: 2023272918921773056, 13: 1011636459460886528, 14: 505818229730443264, 15: 216739030602088448,
             16: 54114388906344448, 17: 63227278716305408, 18: 31613639358152704, 19: 15806819679076352, 20: 7903409839538176, 21: 3951704919769088, 22: 1975852459884544, 23: 846636838289408,
             24: 211384331665408, 25: 246981557485568, 26: 123490778742784, 27: 61745389371392, 28: 30872694685696, 29: 15436347342848, 30: 7718173671424, 31: 3307175149568,
             32: 825720045568, 33: 964771708928, 34: 482385854464, 35: 241192927232, 36: 120596463616, 37: 60298231808, 38: 30149115904, 39: 12918652928,
             40: 3225468928, 41: 3768639488, 42: 1884319744, 43: 942159872, 44: 471079936, 45: 235539968, 46: 117769984, 47: 50463488,
             48: 12599488, 49: 14721248, 50: 7360624, 51: 3680312, 52: 1840156, 53: 920078, 54: 460039, 55: 197123,
             56: 49216, 57: 57504, 58: 28752, 59: 14376, 60: 7188, 61: 3594, 62: 1797, 63: 770}


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
        self.WP_BB = ms_to_bin64(WP)
        self.BP_BB = ms_to_bin64(BP)

        self.WN_BB = ms_to_bin64(WN)
        self.BN_BB = ms_to_bin64(BN)

        self.WB_BB = ms_to_bin64(WB)
        self.BB_BB = ms_to_bin64(BB)

        self.WR_BB = ms_to_bin64(WR)
        self.BR_BB = ms_to_bin64(BR)

        self.WQ_BB = ms_to_bin64(WQ)
        self.BQ_BB = ms_to_bin64(BQ)

        self.WK_BB = ms_to_bin64(WK)
        self.BK_BB = ms_to_bin64(BK)

        self.turn = True

    def empty_squares(self):
        return self.blockers() ^ (2 ** 64 - 1)

    def blockers(self):
        whites = self.WP_BB | self.WN_BB | self.WB_BB | self.WR_BB | self.WQ_BB | self.WK_BB
        blacks = self.BP_BB | self.BN_BB | self.BB_BB | self.BR_BB | self.BQ_BB | self.BK_BB
        return whites | blacks

    def enemy_squares(self):
        if self.turn:
            return self.BP_BB | self.BN_BB | self.BB_BB | self.BR_BB | self.BQ_BB | self.BK_BB
        else:
            return self.WP_BB | self.WN_BB | self.WB_BB | self.WR_BB | self.WQ_BB | self.WK_BB

    def pawn_end_squares(self, ranks):
        bb = self.WP_BB if self.turn else self.BP_BB
        bb = bb >> 8*ranks if self.turn else bb << 8*ranks
        return bb & self.empty_squares()

    def pawn_atk_end_squares(self, sq):
        if self.turn:
            return PAWN_ATK_WHITE_SQRS[sq] & self.enemy_squares()
        else:
            return PAWN_ATK_BLACK_SQRS[sq] & self.enemy_squares()

    def knight_end_squares(self, sq):
        return KNIGHT_SQRS[sq] & (self.empty_squares() | self.enemy_squares())

    def king_end_squares(self, sq):
        return KING_SQRS[sq] & (self.empty_squares() | self.enemy_squares())

    @staticmethod
    def squares_from(bb):
        for sq, bit in enumerate(bin64_to_str(bb)):
            if bit == "1":
                yield sq

    def generate_pawn_moves(self):
        moves = []

        # Normal push
        for sq in self.squares_from(self.pawn_end_squares(1)):
            orig_sq = sq - 8 if self.turn else sq + 8
            moves.append(Move(orig_sq, sq))

        # Double push
        for sq in self.squares_from(self.pawn_end_squares(2)):
            orig_sq = sq - 16 if self.turn else sq + 16
            if self.turn and rank(orig_sq) == "2" or not self.turn and rank(orig_sq) == "7":
                moves.append(Move(orig_sq, sq))

        # Captures
        for Psq in self.squares_from(self.WP_BB if self.turn else self.BP_BB):
            for sq in self.squares_from(self.pawn_atk_end_squares(Psq)):
                moves.append(Move(Psq, sq))

        return moves

    def generate_knight_moves(self):
        moves = []

        for Nsq in self.squares_from(self.WN_BB if self.turn else self.BN_BB):
            for sq in self.squares_from(self.knight_end_squares(Nsq)):
                moves.append(Move(Nsq, sq))

        return moves

    def generate_king_moves(self):
        moves = []

        for Ksq in self.squares_from(self.WK_BB if self.turn else self.BK_BB):
            for sq in self.squares_from(self.king_end_squares(Ksq)):
                moves.append(Move(Ksq, sq))

        return moves


board = Board()
print(board.generate_pawn_moves())
print(board.generate_knight_moves())
print(board.generate_king_moves())
