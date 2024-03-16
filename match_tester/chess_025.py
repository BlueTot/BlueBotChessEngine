import chess.polyglot
import chess.svg
import time
import copy

INF = 99999

times = []


def reverse(lst):
    lst2 = copy.deepcopy(lst)
    for i in range(len(lst2)):
        lst2[i].reverse()
    lst2.reverse()
    return lst2


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

KING_END = [[-50, -30, -30, -30, -30, -30, -30, -50],
            [-30, -30, 0, 0, 0, 0, -30, -30],
            [-30, -10, 20, 40, 40, 20, -10, -30],
            [-30, -10, 30, 40, 40, 30, -10, -30],
            [-30, -10, 30, 40, 40, 30, -10, -30],
            [-30, -10, 20, 40, 40, 20, -10, -30],
            [-30, -30, 0, 0, 0, 0, -30, -30],
            [-50, -30, -30, -30, -30, -30, -30, -50]]
R_KING_END = reverse(KING_END)

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
          [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, -1.0],
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


def evaluate(board):
    Eval = 0

    if board.is_checkmate():
        return -INF
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


def quiescence(board, alpha, beta):
    global debug

    stand_pat = evaluate(board)

    if stand_pat >= beta:
        return beta

    if alpha < stand_pat:
        alpha = stand_pat

    for move in sort_moves(board, list(board.generate_legal_captures())):
        debug["q-search nodes"] += 1
        board.push(move)
        score = -quiescence(board, -beta, -alpha)
        board.pop()

        if score >= beta:
            return beta

        if score > alpha:
            alpha = score

    return alpha


def negamax(board, alpha, beta, depth):
    global debug, tt, tt_stores

    alphaOrig = alpha

    # Transposition Table Lookup
    if tt.in_tt(zobrist_hash := chess.polyglot.zobrist_hash(board)):
        ttEntry = tt.search(zobrist_hash)
        if ttEntry.depth >= depth:
            debug["tt hits"] += 1
            if ttEntry.flag == TranspositionTable.EXACT:
                return ttEntry.value
            elif ttEntry.flag == TranspositionTable.LOWERBOUND:
                alpha = max(alpha, ttEntry.value)
            elif ttEntry.flag == TranspositionTable.UPPERBOUND:
                beta = min(beta, ttEntry.value)
            if alpha >= beta:
                return ttEntry.value

    # call q-search if at leaf node
    if depth == 0 or board.is_game_over() or board.can_claim_draw():
        if board.is_check():  # inc. depth if last move is check
            depth += 1
        else:
            return quiescence(board, alpha, beta)

    # null move pruning
    if depth >= 3 and not board.is_check():
        board.push(chess.Move.null())
        score = -negamax(board, -beta, -beta + 1, depth - 2)
        board.pop()
        if score >= beta:
            return beta

    # search child nodes
    for move in sort_moves(board, list(board.legal_moves)):
        debug["negamax nodes"] += 1
        board.push(move)
        score = -negamax(board, -beta, -alpha, depth - 1)
        board.pop()
        alpha = max(alpha, score)
        if alpha >= beta:
            break

    # Transposition Table Store
    ttEntry = TTEntry(value=alpha, flag=None, depth=depth)
    if alpha <= alphaOrig:
        ttEntry.flag = TranspositionTable.UPPERBOUND
    elif alpha >= beta:
        ttEntry.flag = TranspositionTable.LOWERBOUND
    else:
        ttEntry.flag = TranspositionTable.EXACT
    tt.add(zobrist_hash=chess.polyglot.zobrist_hash(board), ttEntry=ttEntry)
    tt_stores += 1

    return alpha


def root_search(board, end_depth):
    try:
        return chess.polyglot.MemoryMappedReader("../Titans.bin").weighted_choice(board).move
    except IndexError:

        best_move_found = chess.Move.null()

        for depth in range(1, end_depth + 1):

            alpha = -INF
            beta = INF

            if depth == 1:
                moves = sort_moves(board, list(board.legal_moves))
            else:
                moves = sort_moves(board, list(board.legal_moves))
                moves.remove(best_move_found)
                moves = [best_move_found] + moves

            for move in moves:
                debug["root nodes"] += 1
                board.push(move)
                if board.is_checkmate():  # checks for M1
                    board.pop()
                    return move
                score = -negamax(board, -beta, -alpha, depth - 1)
                is_repetition = board.is_repetition(2)
                board.pop()

                if evaluate(board) > 0 and is_repetition:
                    continue

                if depth == end_depth:
                    print(board.san(move), score)
                if score > alpha:
                    alpha = score
                    best_move_found = move

                if alpha >= beta:
                    break

            print(f"depth {depth} complete, best move is {best_move_found}")
            print(debug)

        return best_move_found


def get_best_move(board, depth):
    global debug, tt, tt_stores

    debug = {"root nodes": 0, "negamax nodes": 0, "q-search nodes": 0, "tt hits": 0}
    stime = time.perf_counter()

    best_move = root_search(board, depth)

    debug["time"] = round(time.perf_counter() - stime, 2)
    try:
        debug["positions per second"] = round((debug["root nodes"] + debug["negamax nodes"] + debug["q-search nodes"]) / debug["time"], 2)
    except ZeroDivisionError:
        debug["positions per second"] = "inf"
    debug["tt entries"] = tt.len()
    debug["tt stores"] = tt_stores

    print(debug)
    times.append(debug["time"])
    print(f"chess v0.25 average time: {sum(times)/len(times)}")

    return best_move




class TTEntry:
    def __init__(self, value, flag, depth):
        self.value = value
        self.flag = flag
        self.depth = depth


class TranspositionTable:
    LOWERBOUND = 3
    UPPERBOUND = 4
    EXACT = 5

    def __init__(self):
        self.__table = {}

    def in_tt(self, zobrist_hash):
        return zobrist_hash in self.__table.keys()

    def search(self, zobrist_hash):
        return self.__table[zobrist_hash]

    def add(self, zobrist_hash, ttEntry):
        self.__table[zobrist_hash] = ttEntry

    def len(self):
        return len(self.__table)


tt = TranspositionTable()
tt_stores = 0
