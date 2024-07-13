import json


def bin64_to_str(bin64):
    s = []
    while bin64 > 0:
        s.append(bin64 % 2)
        bin64 //= 2
    s.reverse()
    return "".join(list(map(str, s))).zfill(64)


def print_bb(BB):
    s = bin64_to_str(BB)
    for c, char in enumerate(s):
        print(char, end='')
        if (c + 1) % 8 == 0:
            print()


'''KNIGHT'''
# d = {}
# for sq in range(64):
#     bb = 0
#     file, rank = sq % 8, sq // 8
#     for df, dr in [(2, 1), (2, -1), (1, 2), (1, -2), (-2, 1), (-2, -1), (-1, 2), (-1, -2)]:
#         nf, nr = file + df, rank + dr
#         new_sq = nf + nr * 8
#         if 0 <= nf <= 7 and 0 <= nr <= 7:
#             bb += 2 ** new_sq
#     d[sq] = bb

'''PAWN ATTACKS (WHITE)'''
# d = {}
# for sq in range(64):
#     bb = 0
#     file, rank = sq % 8, sq // 8
#     for df, dr in [(-1, 1), (1, 1)]:
#         nf, nr = file + df, rank + dr
#         new_sq = nf + nr * 8
#         if 0 <= nf <= 7 and 0 <= nr <= 7:
#             bb += 2 ** new_sq
#     d[sq] = bb

# print(d)

'''PAWN ATTACKS (BLACK)'''
# d = {}
# for sq in range(64):
#     bb = 0
#     file, rank = sq % 8, sq // 8
#     for df, dr in [(-1, -1), (1, -1)]:
#         nf, nr = file + df, rank + dr
#         new_sq = nf + nr * 8
#         if 0 <= nf <= 7 and 0 <= nr <= 7:
#             bb += 2 ** new_sq
#     d[sq] = bb

'''KING'''
# d = {}
# for sq in range(64):
#     bb = 0
#     file, rank = sq % 8, sq // 8
#     for df, dr in [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (-1, -1), (1, 1), (1, -1)]:
#         nf, nr = file + df, rank + dr
#         new_sq = nf + nr * 8
#         if 0 <= nf <= 7 and 0 <= nr <= 7:
#             bb += 2 ** new_sq
#     d[sq] = bb

'''BISHOP'''
# d = {}
# for sq in range(64):
#     inner_d = {}
#     file, rank = sq % 8, sq // 8
#     for k, v in {"NW": (-1, -1), "SW": (-1, 1), "NE": (1, -1), "SE": (1, 1)}.items():
#         df, dr = v
#         bb = 0
#         nf, nr = file, rank
#         while True:
#             nf += df
#             nr += dr
#             new_sq = nf + nr * 8
#             if not (0 <= nf <= 7 and 0 <= nr <= 7):
#                 break
#             bb += 2 ** new_sq
#         inner_d[k] = bb
#         # print(sq, k)
#         # print_bb(bb)
#         # print()
#     d[sq] = inner_d

'''ROOK'''
# d = {}
# for sq in range(64):
#     inner_d = {}
#     file, rank = sq % 8, sq // 8
#     for k, v in {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}.items():
#         df, dr = v
#         bb = 0
#         nf, nr = file, rank
#         while True:
#             nf += df
#             nr += dr
#             new_sq = nf + nr * 8
#             if not (0 <= nf <= 7 and 0 <= nr <= 7):
#                 break
#             bb += 2 ** new_sq
#         inner_d[k] = bb
#         # print(sq, k)
#         # print_bb(bb)
#         # print()
#     d[sq] = inner_d

# d = {}

# print(d)

# data_string = json.dumps(d, indent=4)
# with open("resources/rook_sqrs.json", "w") as f:
#     f.write(data_string)
