import chess.polyglot
import chess.svg
import time
import copy

INF = 99999
R = 2

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


def sort_moves(board): # Sort normal moves
    global best_moves, debug
    moves = {}
    for move in board.legal_moves: # Evaluate all the moves using evaluation function
        board.push(move)
        moves[move] = evaluate(board)
        board.pop()
    sorted_dict = sorted(moves.items(), key=lambda x: x[1])
    sorted_moves = [i[0] for i in sorted_dict] # Sort moves
    if (zobrist_hash := chess.polyglot.zobrist_hash(board)) in best_moves: # If current position found
        if (best_move := best_moves[zobrist_hash]) in sorted_moves: # If best move found
            debug["best move hits"] += 1
            sorted_moves.remove(best_move)
            sorted_moves.insert(0, best_move) # Move best move to the start of the list
    return sorted_moves


def sort_captures(board): # Sort captures
    moves = {}
    for move in list(board.generate_legal_captures()):
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

    for move in sort_captures(board):
        debug["positions"] += 1
        board.push(move)
        score = -quiescence(board, -beta, -alpha)
        board.pop()

        if score >= beta:
            return beta

        if score > alpha:
            alpha = score

    return alpha


def negamax(board, alpha, beta, depth): # Main negamax search function
    global debug, best_moves

    # call q-search if at leaf node
    if depth == 0 or board.is_game_over() or board.can_claim_draw():
        if board.is_check():  # inc. depth if last move is check
            depth += 1
        else:
            return quiescence(board, alpha, beta)

    # null move pruning
    if depth > R and not board.is_check() and list(board.move_stack)[-1] != chess.Move.null():
        board.push(chess.Move.null())
        score = -negamax(board, -beta, -beta + 1, depth - R - 1)
        board.pop()
        if score >= beta:
            return beta
    
    best_move = chess.Move.null()

    # search child nodes
    for move in sort_moves(board):
        debug["positions"] += 1
        board.push(move)
        score = -negamax(board, -beta, -alpha, depth - 1)
        board.pop()
        if score >= beta:
            best_moves[chess.polyglot.zobrist_hash(board)] = move # Beta cutoff move is the best move
            return beta
        if score > alpha:
            alpha = score
            best_move = move
    
    if best_move != chess.Move.null():
        best_moves[chess.polyglot.zobrist_hash(board)] = best_move # Current best move is the best move

    return alpha

def root_search(board, depth): # Root negamax search function
    global best_moves

    alpha = -INF
    beta = INF
    best_move_found = chess.Move.null()

    for move in sort_moves(board):
        debug["positions"] += 1
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
            best_moves[chess.polyglot.zobrist_hash(board)] = move # Beta cutoff move is the best move
            return move
        if score > alpha:
            alpha = score
            best_move_found = move
    
    best_moves[chess.polyglot.zobrist_hash(board)] = best_move_found # Store best move

    return best_move_found

def get_pv_line(board): # Function to get principal variation for printing purposes
    global best_moves
    pv = []
    curr = copy.deepcopy(board)
    while (zobrist_hash := chess.polyglot.zobrist_hash(curr)) in best_moves:
        best_move = best_moves[zobrist_hash]
        curr.push(best_move)
        pv.append(best_move)
    return pv

def get_best_move(board, max_depth): # Function to get best move after search
    global debug, best_moves

    best_moves = {}

    try:
        return chess.polyglot.MemoryMappedReader("../Titans.bin").weighted_choice(board).move

    except IndexError:

        debug = {"positions": 0, "best move hits": 0} # Debug dictionary
        stime = time.perf_counter()

        for depth in range(1, max_depth + 1): # Iterative deepening
            
            best_move_found = root_search(board, depth) # Search at given depth
            print(f"PV line: {' '.join(list(map(str, get_pv_line(board))))}") # Print the principal variation
            print(f"Depth {depth} complete, best move found is {best_move_found}")
            print(debug)

        debug["time"] = round(time.perf_counter() - stime, 2)
        try:
            debug["positions per second"] = round(debug["positions"] / debug["time"], 2)
        except ZeroDivisionError:
            debug["positions per second"] = "inf"
        debug["best moves table length"] = len(best_moves)
        print(f"v0.29 DEBUG: {debug}")
        times.append(debug["time"])
        print(f"v0.29 Average Time: {sum(times)/len(times)}, Total Time: {sum(times)}")

        return best_move_found

