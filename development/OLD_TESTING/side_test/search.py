from evaluation import evaluate
import time


def negamax(board, depth):
    global positions

    positions += 1

    if depth == 0:
        return evaluate(board)

    score = -99999
    for move in list(board.legal_moves):
        board.push(move)
        Eval = -negamax(board, depth - 1)
        board.pop()
        score = max(score, Eval)

    return score


def root(board, depth):
    global positions

    score = -99999
    bestMoveFound = None
    positions = 0
    stime = time.perf_counter()

    positions += 1

    for move in list(board.legal_moves):
        board.push(move)
        Eval = -negamax(board, depth - 1)
        board.pop()
        if Eval > score:
            score = Eval
            bestMoveFound = move
        print(board.san(move), score)

    print(f"nodes: {positions}")
    print("time elapsed: ", t := time.perf_counter() - stime)
    print(f"nodes per second: {positions / t}")

    return bestMoveFound
