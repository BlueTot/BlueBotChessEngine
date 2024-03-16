import chess.polyglot
import chess.svg
import time
import copy

INF = 99999

times = []


class TTEntry:

    EXACT = "exact"
    LOWER_BOUND = "lower bound"
    UPPER_BOUND = "upper bound"

    def __init__(self, flag, depth, value, current_best_move):
        self.flag = flag
        self.depth = depth
        self.value = value
        self.current_best_move = current_best_move

    def __repr__(self):
        return f"{self.flag} {self.depth} {self.value} {self.current_best_move}"


class TranspositionTable:
    def __init__(self):
        self.__tt = {}

    def lookup(self, board):
        if (board_hash := chess.polyglot.zobrist_hash(board)) in self.__tt:
            return self.__tt[board_hash]

    def store(self, board, entry):
        self.__tt[chess.polyglot.zobrist_hash(board)] = entry

    def PV_table(self):
        pv_table = {}
        for entry in self.__tt.values():
            if entry.flag == TTEntry.EXACT:
                if entry.depth not in pv_table:
                    pv_table[entry.depth] = []
                pv_table[entry.depth].append(entry)
        return pv_table


class KillerMovesTable:
    def __init__(self):
        self.__table = {}

    def add_move(self, move, depth):
        if depth not in self.__table:
            self.__table[depth] = []
        if move not in self.__table[depth]:
            if len(self.__table[depth]) == 2:
                self.__table[depth] = [move] + [self.__table[depth][0]]
            else:
                self.__table[depth] = [move] + self.__table[depth]

    def in_table(self, move, depth):
        if depth in self.__table:
            return move in self.__table[depth]
        return False

    def get_moves(self, depth):
        if depth in self.__table:
            return self.__table[depth]

    def __repr__(self):
        return str(self.__table)


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


def sort_moves(board, lst, depth, tt_move):
    global kt, debug
    moves = {}
    for move in lst:
        board.push(move)
        if depth is not None and kt.in_table(move, depth):  # Killer Moves
            debug["killer move hits"] += 1
            moves[move] = evaluate(board) - 9000
        elif move == tt_move:  # Transposition Table Moves
            debug["tt move orders"] += 1
            moves[move] = evaluate(board) - 10000
        else:  # Normal Moves
            moves[move] = evaluate(board)
        board.pop()
    sorted_dict = sorted(moves.items(), key=lambda x: x[1])
    return [i[0] for i in sorted_dict]


def quiescence(board, alpha, beta):
    global debug

    debug["positions"] += 1
    debug["q-search positions"] += 1

    stand_pat = evaluate(board)

    if stand_pat >= beta:
        return beta

    if alpha < stand_pat:
        alpha = stand_pat

    for move in sort_moves(board, list(board.generate_legal_captures()), None, None):

        board.push(move)
        score = -quiescence(board, -beta, -alpha)
        board.pop()

        if score >= beta:
            return beta

        if score > alpha:
            alpha = score

    return alpha


def negamax(board, alpha, beta, depth):
    global debug, tt, kt

    debug["positions"] += 1
    debug["negamax positions"] += 1

    # Transposition table lookup
    alpha_orig = alpha
    tt_entry = tt.lookup(board)
    curr_best_move = None
    if tt_entry is not None and tt_entry.depth >= depth:
        debug["tt hits"] += 1
        if tt_entry.flag == TTEntry.EXACT:  # exact PV node entry, return immediately
            return tt_entry.value
        elif tt_entry.flag == TTEntry.LOWER_BOUND:
            alpha = max(alpha, tt_entry.value)
            curr_best_move = tt_entry.current_best_move
        elif tt_entry.flag == TTEntry.UPPER_BOUND:
            beta = min(beta, tt_entry.value)
            curr_best_move = tt_entry.current_best_move
        if alpha >= beta:
            return tt_entry.value

    # call q-search if at leaf node
    if depth == 0 or board.is_game_over() or board.can_claim_draw():
        if board.is_check():  # inc. depth if last move is check
            depth += 1
        else:
            debug["leaf nodes"] += 1
            return quiescence(board, alpha, beta)

    # null move pruning
    if depth >= 3 and not board.is_check():
        board.push(chess.Move.null())
        score = -negamax(board, -beta, -beta + 1, depth - 2)
        board.pop()
        if score >= beta:
            return beta

    best_move = None

    # Move ordering
    moves = sort_moves(board, list(board.legal_moves), depth, curr_best_move)

    # search child nodes
    for move in moves:
        if board.is_legal(move):
            board.push(move)
            score = -negamax(board, -beta, -alpha, depth - 1)
            board.pop()
            if score > alpha:
                alpha = score
                best_move = move
                if score >= beta:  # Beta cut off
                    debug["tt stores"] += 1
                    tt.store(board, TTEntry(TTEntry.LOWER_BOUND, depth, alpha, best_move))  # Store TT Entry for beta cut off
                    if chess.Move.null() not in board.move_stack:
                        kt.add_move(move, depth)  # Store killer move
                    return beta

    # Transposition Table Store
    if alpha <= alpha_orig:
        tt.store(board, TTEntry(TTEntry.UPPER_BOUND, depth, alpha, best_move))
    elif alpha >= beta:
        tt.store(board, TTEntry(TTEntry.LOWER_BOUND, depth, alpha, best_move))
    else:
        tt.store(board, TTEntry(TTEntry.EXACT, depth, alpha, best_move))
    debug["tt stores"] += 1

    return alpha


def root_search(board, depth):
    global debug

    alpha = -INF
    beta = INF
    bestMoveFound = chess.Move.null()
    alpha_orig = alpha

    debug["positions"] += 1
    debug["negamax positions"] += 1

    tt_entry = tt.lookup(board)
    curr_best_move = None
    if tt_entry is not None and tt_entry.depth >= depth:
        debug["tt hits"] += 1
        if tt_entry.flag == TTEntry.EXACT:  # exact PV node entry, return immediately
            return tt_entry.current_best_move
        elif tt_entry.flag == TTEntry.LOWER_BOUND:
            alpha = max(alpha, tt_entry.value)
            curr_best_move = tt_entry.current_best_move
        elif tt_entry.flag == TTEntry.UPPER_BOUND:
            beta = min(beta, tt_entry.value)
            curr_best_move = tt_entry.current_best_move
        if alpha >= beta:
            return tt_entry.current_best_move

    # Move ordering
    moves = sort_moves(board, list(board.legal_moves), depth, curr_best_move)

    for move in moves:
        board.push(move)
        if board.is_checkmate():  # checks for M1
            board.pop()
            return move
        score = -negamax(board, -beta, -alpha, depth - 1)
        is_repetition = board.is_repetition(2)
        board.pop()

        if evaluate(board) > 0 and is_repetition:
            continue
        if depth >= 4:
            print(board.san(move), score)
        if score >= beta:
            break
        if score > alpha:
            alpha = score
            bestMoveFound = move

    # Transposition Table Store
    if alpha <= alpha_orig:
        tt.store(board, TTEntry(TTEntry.UPPER_BOUND, depth, alpha, bestMoveFound))
    elif alpha >= beta:
        tt.store(board, TTEntry(TTEntry.LOWER_BOUND, depth, alpha, bestMoveFound))
    else:
        tt.store(board, TTEntry(TTEntry.EXACT, depth, alpha, bestMoveFound))
    debug["tt stores"] += 1

    return bestMoveFound


def get_best_move(board, max_depth):
    global debug, tt, kt

    tt = TranspositionTable()
    kt = KillerMovesTable()

    try:
        return chess.polyglot.MemoryMappedReader("../Titans.bin").weighted_choice(board).move

    except IndexError:
        
        debug = {"positions": 0, "negamax positions": 0, "q-search positions": 0, "leaf nodes": 0, "tt stores": 0, "tt hits": 0, "tt move orders": 0, "killer move hits": 0}
        stime = time.perf_counter()

        for depth in range(max_depth, max_depth+1):
            best_move_found = root_search(board, depth)
            print(f"depth {depth} complete with best move found being {best_move_found}")

        debug["time"] = round(time.perf_counter() - stime, 2)
        try:
            debug["positions per second"] = round(debug["positions"] / debug["time"], 2)
        except ZeroDivisionError:
            debug["positions per second"] = "inf"
        try:
            debug["hit rate"] = f'{debug["tt hits"] / debug["tt stores"] * 100:.4f}%'
        except ZeroDivisionError:
            debug["hit rate"] = "inf"
        print(debug)
        print(tt.PV_table())
        print(kt)
        times.append(debug["time"])
        print(f"chess v0.27 average time: {sum(times)/len(times)}")

        return best_move_found
