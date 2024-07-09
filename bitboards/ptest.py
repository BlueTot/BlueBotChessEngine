import chess
from time import perf_counter

board = chess.Board()
stime = perf_counter()
print(board.legal_moves)
print(perf_counter() - stime)

# stime = perf_counter()
# board.push_san("e4")
# print(perf_counter() - stime)

# nodes = 0

# def __perft(brd, depth):
#     global nodes
#     if depth == 0:
#         return
#     for move in brd.legal_moves:
#         if depth == 1:
#             nodes += 1
#         brd.push(move)
#         __perft(brd, depth - 1)
#         brd.pop()

# stime = perf_counter()
# __perft(board, 5)
# print(nodes, perf_counter() - stime)

# 5.0178473

# 363 / 5 = 73 times faster ...