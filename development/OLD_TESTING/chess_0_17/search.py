import chess.polyglot
import chess.svg
import math
import time
import copy
from chess.polyglot import zobrist_hash


def reverse(lst):
    lst2 = copy.deepcopy(lst)
    for i in range(len(lst2)):
        lst2[i].reverse()
    lst2.reverse()
    return lst2


LOWERBOUND = 3
UPPERBOUND = 4
EXACT = 5

KING = [[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
        [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]]
KING.reverse()
R_KING = reverse(KING)

QUEEN = [[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
         [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
         [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
         [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
         [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
         [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
         [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
         [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]
QUEEN.reverse()
R_QUEEN = reverse(QUEEN)

ROOK = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]]
ROOK.reverse()
R_ROOK = reverse(ROOK)

BISHOP = [[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
          [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
          [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
          [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
          [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
          [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
          [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
          [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]
BISHOP.reverse()
R_BISHOP = reverse(BISHOP)

KNIGHT = [[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
          [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
          [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
          [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
          [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
          [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
          [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
          [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]
KNIGHT.reverse()
R_KNIGHT = reverse(KNIGHT)

PAWN = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
        [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
        [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
        [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
        [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
PAWN.reverse()
R_PAWN = reverse(PAWN)


class TTEntry:
    def __init__(self, value, flag, depth):
        self.value = value
        self.flag = flag
        self.depth = depth


class TranspositionTable:

    def __init__(self):
        self.__table = {}

    def in_tt(self, fen):
        return fen in self.__table.keys()

    def search(self, fen):
        return self.__table[fen]

    def add(self, fen, ttEntry):
        self.__table[fen] = ttEntry

    def len(self):
        return len(self.__table)


tt = TranspositionTable()


def evaluate(board):
    Eval = 0

    if board.is_checkmate():
        return -1 * math.inf
    if board.is_stalemate() or board.is_repetition(3):
        return 0

    for row in range(8):
        for col in range(8):

            square = row * 8 + col
            piece = board.piece_at(square)

            if piece is not None:

                mult = 1 if piece.color else -1

                match piece.piece_type:
                    case chess.KING:
                        Eval += mult * (900 + (KING if piece.color else R_KING)[row][col])
                    case chess.QUEEN:
                        Eval += mult * (88 + (QUEEN if piece.color else R_QUEEN)[row][col])
                    case chess.ROOK:
                        Eval += mult * (51 + (ROOK if piece.color else R_ROOK)[row][col])
                    case chess.BISHOP:
                        Eval += mult * (32 + (BISHOP if piece.color else R_BISHOP)[row][col])
                    case chess.KNIGHT:
                        Eval += mult * (30 + (KNIGHT if piece.color else R_KNIGHT)[row][col])
                    case chess.PAWN:
                        Eval += mult * (10 + (PAWN if piece.color else R_PAWN)[row][col])

    return Eval if board.turn else -1 * Eval


def sort_moves(board, lst):
    moves = {}
    for move in lst:
        board.push(move)
        moves[move] = evaluate(board)
        board.pop()
    sorted_dict = sorted(moves.items(), key=lambda x: x[1])
    return [i[0] for i in sorted_dict]


def quiescence(board, alpha, beta, depth):
    global positions

    alphaOrig = alpha
    
    # Transposition Table Lookup
    if tt.in_tt(key := zobrist_hash(board)):
        ttEntry = tt.search(key)
        if ttEntry.depth >= depth:
            if ttEntry.flag == EXACT:
                return ttEntry.value
            elif ttEntry.flag == LOWERBOUND:
                alpha = max(alpha, ttEntry.value)
            elif ttEntry.flag == UPPERBOUND:
                beta = min(beta, ttEntry.value)
            if alpha >= beta:
                return ttEntry.value
            print(1)
    else:
        ttEntry = TTEntry(value=None, flag=None, depth=None)

    stand_pat = evaluate(board)

    if stand_pat >= beta:
        return beta

    if alpha < stand_pat:
        alpha = stand_pat

    if depth == 0:
        return alpha

    for move in sort_moves(board, list(board.generate_legal_captures())):
        positions += 1
        board.push(move)
        score = -quiescence(board, -beta, -alpha, depth-1)
        board.pop()

        if score >= beta:
            return beta

        if alpha > score:
            alpha = score

    # Transposition Table Store
    ttEntry.value = alpha
    if alpha <= alphaOrig:
        ttEntry.flag = UPPERBOUND
    elif alpha >= beta:
        ttEntry.flag = LOWERBOUND
    else:
        ttEntry.flag = EXACT
    ttEntry.depth = depth
    tt.add(fen=zobrist_hash(board), ttEntry=ttEntry)
    
    return alpha


def negamax(depth, board, alpha, beta):
    global positions

    alphaOrig = alpha

    # Transposition Table Lookup
    if tt.in_tt(key := zobrist_hash(board)):
        ttEntry = tt.search(key)
        if ttEntry.depth >= depth:
            if ttEntry.flag == EXACT:
                return ttEntry.value
            elif ttEntry.flag == LOWERBOUND:
                alpha = max(alpha, ttEntry.value)
            elif ttEntry.flag == UPPERBOUND:
                beta = min(beta, ttEntry.value)
            if alpha >= beta:
                return ttEntry.value
            print(1)
    else:
        ttEntry = TTEntry(value=None, flag=None, depth=None)

    if depth == 0 or board.is_game_over() or board.can_claim_draw():
        return quiescence(board, alpha, beta, 3)

    for move in sort_moves(board, list(board.legal_moves)):
        positions += 1
        board.push(move)
        score = -negamax(depth - 1, board, -beta, -alpha)
        board.pop()
        alpha = max(alpha, score)
        if alpha >= beta:
            break

    # Transposition Table Store
    ttEntry.value = alpha
    if alpha <= alphaOrig:
        ttEntry.flag = UPPERBOUND
    elif alpha >= beta:
        ttEntry.flag = LOWERBOUND
    else:
        ttEntry.flag = EXACT
    ttEntry.depth = depth
    tt.add(fen=zobrist_hash(board), ttEntry=ttEntry)

    return alpha


def root(board, depth):
    global positions, tt

    print(tt.len())

    try:
        return chess.polyglot.MemoryMappedReader("../Titans.bin").weighted_choice(board).move

    except IndexError:

        stime = time.perf_counter()

        alpha = -1 * math.inf
        # alphaOrig = alpha
        beta = math.inf
        bestMoveFound = None
        positions = 0

        # # Transposition Table Lookup
        # if tt.in_tt(key := zobrist_hash(board)):
        #     ttEntry = tt.search(key)
        #     if ttEntry.depth >= depth:
        #         if ttEntry.flag == EXACT:
        #             return ttEntry.value
        #         elif ttEntry.flag == LOWERBOUND:
        #             alpha = max(alpha, ttEntry.value)
        #         elif ttEntry.flag == UPPERBOUND:
        #             beta = min(beta, ttEntry.value)
        #         if alpha >= beta:
        #             return ttEntry.value
        #         print(1)
        # else:
        #     ttEntry = TTEntry(value=None, flag=None, depth=None)

        for move in list(board.legal_moves):
            if "#" in board.san(move):  # checks for mate in one
                return move

        for move in sort_moves(board, list(board.legal_moves)):
            positions += 1
            board.push(move)
            score = -negamax(depth - 1, board, -beta, -alpha)
            is_repetition = board.is_repetition(2)
            board.pop()

            if evaluate(board) > 0 and is_repetition:
                continue

            print(board.san(move), score)
            if score > alpha:
                alpha = score
                bestMoveFound = move

            if alpha >= beta:
                break

        # # Transposition Table Store
        # ttEntry.value = alpha
        # if alpha <= alphaOrig:
        #     ttEntry.flag = UPPERBOUND
        # elif alpha >= beta:
        #     ttEntry.flag = LOWERBOUND
        # else:
        #     ttEntry.flag = EXACT
        # ttEntry.depth = depth
        # tt.add(fen=zobrist_hash(board), ttEntry=ttEntry)

        print(f"nodes: {positions}")
        print("time taken: ", time_taken := time.perf_counter() - stime)
        print(f"nodes per second: {positions / time_taken}")

        return bestMoveFound
