import chess
import time

board = chess.Board()


def perft(brd, depth):
    global nodes
    nodes = 0
    stime = time.perf_counter()
    __perft(brd, depth)
    print(nodes, time.perf_counter() - stime)


def __perft(brd, depth):
    global nodes
    if depth == 0:
        # nodes += 1
        return
    for move in brd.legal_moves:
        if depth == 1:
            nodes += 1
        brd.push(move)
        __perft(brd, depth - 1)
        brd.pop()


perft(board, 1)
perft(board, 2)
perft(board, 3)
perft(board, 4)
perft(board, 5)
