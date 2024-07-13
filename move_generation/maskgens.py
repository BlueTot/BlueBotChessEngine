from itertools import chain, combinations
import json

'''BITWISE FUNCTIONS AND TABLES'''

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

def bsf(x):
    if x == 0:
        return None
    return x.bit_length() - 1

def bsr(x):
    if x == 0:
        return None
    return (x&-x).bit_length() - 1

def remove_piece(bb, sq): # Remove piece
    bb ^= BB_SQRS[sq]
    return bb

def squares_from(bb): # Get squares from bitboard
    while bb != 0:
        sq = bsf(bb)
        bb = remove_piece(bb, sq := bsf(bb))
        yield sq

def bb_from_sqrs(sqrs):
    bb = 0
    for sq in sqrs:
        bb |= BB_SQRS[sq]
    return bb

'''POWER SET AND MASKS'''

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

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

'''ACTUAL CALCULATIONS'''

def open_json(file_name):
    with open("resources/" + file_name) as f:
        data = json.load(f)
    return dict(zip(map(int, data), data.values()))

BISHOP_SQRS = open_json("bishop_sqrs.json")
ROOK_SQRS = open_json("rook_sqrs.json")

def diagonals(sq, blockers): # Get bishop squares

    # North-west
    nw_blockers = BISHOP_SQRS[sq]["NW"] & blockers
    blocker = bsf(nw_blockers)
    nw_sqrs = BISHOP_SQRS[sq]["NW"] & ~(BISHOP_SQRS[blocker]["NW"] if blocker is not None else 0)

    # North-east
    ne_blockers = BISHOP_SQRS[sq]["NE"] & blockers
    blocker = bsf(ne_blockers)
    ne_sqrs = BISHOP_SQRS[sq]["NE"] & ~(BISHOP_SQRS[blocker]["NE"] if blocker is not None else 0)

    # South-west
    sw_blockers = BISHOP_SQRS[sq]["SW"] & blockers
    blocker = bsr(sw_blockers)
    sw_sqrs = BISHOP_SQRS[sq]["SW"] & ~(BISHOP_SQRS[blocker]["SW"] if blocker is not None else 0)

    # South-east
    se_blockers = BISHOP_SQRS[sq]["SE"] & blockers
    blocker = bsr(se_blockers)
    se_sqrs = BISHOP_SQRS[sq]["SE"] & ~(BISHOP_SQRS[blocker]["SE"] if blocker is not None else 0)

    return (nw_sqrs | ne_sqrs | sw_sqrs | se_sqrs)

def ranks_and_files(sq, blockers): # Get rook squares

    # North
    n_blockers = ROOK_SQRS[sq]["N"] & blockers
    blocker = bsf(n_blockers)
    n_sqrs = ROOK_SQRS[sq]["N"] & ~(ROOK_SQRS[blocker]["N"] if blocker is not None else 0)

    # East
    e_blockers = ROOK_SQRS[sq]["E"] & blockers
    blocker = bsr(e_blockers)
    e_sqrs = ROOK_SQRS[sq]["E"] & ~(ROOK_SQRS[blocker]["E"] if blocker is not None else 0)

    # South
    s_blockers = ROOK_SQRS[sq]["S"] & blockers
    blocker = bsr(s_blockers)
    s_sqrs = ROOK_SQRS[sq]["S"] & ~(ROOK_SQRS[blocker]["S"] if blocker is not None else 0)

    # West
    w_blockers = ROOK_SQRS[sq]["W"] & blockers
    blocker = bsf(w_blockers)
    w_sqrs = ROOK_SQRS[sq]["W"] & ~(ROOK_SQRS[blocker]["W"] if blocker is not None else 0)

    return (n_sqrs | e_sqrs | s_sqrs | w_sqrs)

'''MAIN CODE'''

# BB_DIAG_ATTACKS = [{} for _ in range(64)]
# for i, mask in enumerate(BB_DIAG_MASKS):
#     print(i)
#     for subset in powerset(squares_from(mask)):
#         blockers = bb_from_sqrs(subset)
#         BB_DIAG_ATTACKS[i][blockers] = diagonals(i, blockers)
# print("done")
# data_string = json.dumps(BB_DIAG_ATTACKS, indent=4)
# with open("resources/diag_attacks.json", "w") as f:
#     f.write(data_string)

# def bb_diag_attacks():
#     return BB_DIAG_ATTACKS

BB_RF_ATTACKS = [{} for _ in range(64)]
for i, mask in enumerate(BB_RF_MASKS):
    print(i)
    for subset in powerset(squares_from(mask)):
        blockers = bb_from_sqrs(subset)
        BB_RF_ATTACKS[i][blockers] = ranks_and_files(i, blockers)
print("done")
data_string = json.dumps(BB_RF_ATTACKS, indent=4)
with open("resources/rf_attacks.json", "w") as f:
    f.write(data_string)

def bb_diag_attacks():
    return BB_RF_ATTACKS
        