import chess
from time import perf_counter

board = chess.Board()
board.set_fen("rnbqkbnr/ppPpp1pp/8/8/8/8/PPP1PPpP/RNBQKBNR w KQkq - 0 5")
# stime = perf_counter()
# print(board.legal_moves)
# print(perf_counter() - stime)

# stime = perf_counter()
# board.push_san("e4")
# print(perf_counter() - stime)

# nodes = 0

def perft(brd, depth):
    global nodes
    nodes = 0
    __perft(brd, depth)
    return nodes

def __perft(brd, depth):
    global nodes
    if depth == 0:
        return
    for move in brd.legal_moves:
        if depth == 1:
            nodes += 1
        brd.push(move)
        __perft(brd, depth - 1)
        brd.pop()

# stime = perf_counter()
print(perft(board, 1))
print(perft(board, 2))
print(perft(board, 3))
print(perft(board, 4))

# 5.0178473

# 363 / 5 = 73 times faster ...