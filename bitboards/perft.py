import chess
import bitboard_019

board = chess.Board()
board.set_board_fen("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8")

def perft(brd, depth):
    global nodes, log
    nodes = 0
    log = set()
    __perft(brd, depth)
    return log

def __perft(brd, depth):
    global nodes
    if depth == 0:
        return
    for move in brd.legal_moves:
        if depth == 1:
            nodes += 1
        brd.push(move)
        if depth == 1:
            log.add(tuple([i.uci() for i in list(brd.move_stack)]))
        __perft(brd, depth - 1)
        brd.pop()


correct_log = perft(board, 2)
print(len(correct_log))

b = bitboard_019.Board()
b.set_fen("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - -")
incorrect_log = b.perft(2)
print(len(incorrect_log))

with open("correct.txt", "w") as f:
    for pos in sorted(list(correct_log)):
        f.write(str(pos) + "\n")
with open("incorrect.txt", "w") as f:
    for pos in sorted(list(incorrect_log)):
        f.write(str(pos) + "\n")
