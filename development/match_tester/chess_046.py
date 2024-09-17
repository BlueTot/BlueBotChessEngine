# Imports
import chess.polyglot
import chess.svg
import time
import copy

VERSION = "v0.46" # Version
INF = 99999 # Infinity value
R = 2 # Null move pruning reduction R
PAWN_VAL = 10
WINDOW = 1/4 * PAWN_VAL # Aspiration window value = 1/4 of a pawn
ENDGAME_UPPER, ENDGAME_LOWER = 100, 270

times = []


def reverse(lst): # Function to reverse piece square tables for black side
    lst2 = copy.deepcopy(lst)
    for i in range(len(lst2)):
        lst2[i].reverse()
    lst2.reverse()
    return lst2

# Piece square tables for evaluation function

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

KING_END = [[-5.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0],
            [-3.0, -3.0, 0.0, 0.0, 0.0, 0.0, -3.0, -3.0],
            [-3.0, -1.0, 2.0, 4.0, 4.0, 2.0, -1.0, -3.0],
            [-3.0, -1.0, 3.0, 4.0, 4.0, 3.0, -1.0, -3.0],
            [-3.0, -1.0, 3.0, 4.0, 4.0, 3.0, -1.0, -3.0],
            [-3.0, -1.0, 2.0, 4.0, 4.0, 2.0, -1.0, -3.0],
            [-3.0, -3.0, 0.0, 0.0, 0.0, 0.0, -3.0, -3.0],
            [-5.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0]]
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
          [-1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, -1.0],
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

PAWN_END = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0],
        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0],
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
PAWN_END.reverse()
R_PAWN_END = reverse(PAWN_END)

MATERIAL = {chess.KING: 900, chess.QUEEN: 88, chess.ROOK: 51, chess.BISHOP: 32, chess.KNIGHT: 30, chess.PAWN: 10}

class TranspositionTable: # Transposition Table class

    EXACT_FLAG = 0
    ALPHA_FLAG = 1
    BETA_FLAG = 2

    def __init__(self):
        self.__table = {} # Depth, flag, value, best move

    def probe_hash(self, depth, alpha, beta, zhash): # Lookup
        if zhash in self.__table:
            entry_depth, entry_flag, entry_value, _ = self.__table[zhash]
            if entry_depth >= depth:
                if entry_flag == self.EXACT_FLAG:
                    return entry_value
                elif entry_flag == self.ALPHA_FLAG and entry_value <= alpha:
                    return alpha
                elif entry_flag == self.BETA_FLAG and entry_value >= beta:
                    return beta

    def record_hash(self, depth, flag, val, best, zhash): # Store
        self.__table[zhash] = (depth, flag, val, best)
    
    def get_best_move(self, zhash): # Lookup best move for move ordering
        if zhash in self.__table:
            return self.__table[zhash][3]
    
    @property
    def length(self):
        return len(self.__table)

class KillerMovesTable: # Killer moves table class

    NUM_OF_KILLERS = 2 # 2 killer moves is most optimal

    def __init__(self):
        self.__table = {}

    def add_move(self, move, ply): # Add killer move
        if ply not in self.__table:
            self.__table[ply] = []
        if move not in self.__table[ply]:
            if len(self.__table[ply]) == self.NUM_OF_KILLERS:
                self.__table[ply] = [move] + [self.__table[ply][:self.NUM_OF_KILLERS-1]]
            else:
                self.__table[ply] = [move] + self.__table[ply]

    def in_table(self, move, ply): # Check if ply is in table
        if ply in self.__table:
            return move in self.__table[ply]
        return False

    def get_moves(self, ply): # Get killer moves for given ply
        if ply in self.__table:
            return self.__table[ply]

    def __repr__(self):
        return str(self.__table)

def endgame_score(board):
    mm_material = 0
    for square in range(64):
        piece = board.piece_at(square)
        if piece is not None and piece.piece_type in (chess.QUEEN, chess.ROOK, chess.KNIGHT, chess.BISHOP):
            mm_material += MATERIAL[piece.piece_type]
    if mm_material < ENDGAME_UPPER:
        endgame = 1
    elif mm_material > ENDGAME_LOWER:
        endgame = 0
    else:
        endgame = (mm_material - ENDGAME_LOWER) / (ENDGAME_UPPER - ENDGAME_LOWER)
    return endgame

def evaluate(board : chess.Board): # Evaluation function
    score = 0

    # Initial checks
    if board.is_checkmate():
        return -INF
    if board.is_stalemate():
        return 0

    # King Location Calculation
    white_king, black_king = board.king(chess.WHITE), board.king(chess.BLACK)

    # Game Stage Calculation
    endgame = endgame_score(board)
    
    # Material and Piece Square Tables
    wp, bp, wpbb, bpbb = [], [], 0, 0
    for square in range(64):
        row, col = divmod(square, 8)
        piece = board.piece_at(square)

        if piece is not None:

            mult = 1 if piece.color else -1
            if piece.color:
                dist_to_king = abs(row - black_king // 8) + abs(col - black_king % 8)
            else:
                dist_to_king = abs(row - white_king // 8) + abs(col - white_king % 8)
            dist_to_king_bonus = (16 - dist_to_king) / 32 # Pieces gain +0.05 score if they are close to the enemy king

            match piece.piece_type:
                case chess.KING:
                    score += mult * (900 + (KING if piece.color else R_KING)[row][col]) * (1 - endgame) # King Middlegame
                    score += mult * (900 + (KING_END if piece.color else R_KING_END)[row][col]) * endgame # King Endgame
                case chess.QUEEN:
                    score += mult * (88 + (QUEEN if piece.color else R_QUEEN)[row][col] + dist_to_king_bonus)
                case chess.ROOK:
                    score += mult * (51 + (ROOK if piece.color else R_ROOK)[row][col] + dist_to_king_bonus)
                case chess.BISHOP:
                    score += mult * (32 + (BISHOP if piece.color else R_BISHOP)[row][col] + dist_to_king_bonus)
                case chess.KNIGHT:
                    score += mult * (30 + (KNIGHT if piece.color else R_KNIGHT)[row][col] + dist_to_king_bonus)
                case chess.PAWN:
                    score += mult * (10 + (PAWN if piece.color else R_PAWN)[row][col]) * (1 - endgame) # Pawn Middlegame
                    score += mult * (10 + (PAWN_END if piece.color else R_PAWN_END)[row][col]) * endgame # Pawn Endgame
                    if piece.color:
                        wp.append(square)
                        wpbb += 2**square
                    else:
                        bp.append(square)
                        bpbb += 2**square
    
    # # Pawn Structure
    # doubled, blocked, isolated = 0, 0, 0
    # for square in wp: # white pawns
    #     if (wpbb - 2**square) & chess.BB_FILES[square % 8] != 0: # doubled pawns
    #         doubled += 1
    #     if square % 8 == 0 and wpbb & chess.BB_FILES[(square % 8) + 1] == 0: # A file isolated pawn
    #         isolated += 1
    #     elif square % 8 == 7 and wpbb & chess.BB_FILES[(square % 8) - 1] == 0: # H file isolated pawn
    #         isolated += 1
    #     elif 1 <= square % 8 <= 6 and wpbb & chess.BB_FILES[(square % 8) + 1] == 0 and wpbb & chess.BB_FILES[(square % 8) - 1] == 0: # Remaining files
    #         isolated += 1
    #     if board.piece_at(square + 8) is not None and board.piece_at(square + 8).color == chess.BLACK:
    #         blocked += 1
    # for square in bp: # white pawns
    #     if (bpbb - 2**square) & chess.BB_FILES[square % 8] != 0: # doubled pawns
    #         doubled -= 1
    #     if square % 8 == 0 and bpbb & chess.BB_FILES[(square % 8) + 1] == 0: # A file isolated pawn
    #         isolated -= 1
    #     elif square % 8 == 7 and bpbb & chess.BB_FILES[(square % 8) - 1] == 0: # H file isolated pawn
    #         isolated -= 1
    #     elif 1 <= square % 8 <= 6 and bpbb & chess.BB_FILES[(square % 8) + 1] == 0 and bpbb & chess.BB_FILES[(square % 8) - 1] == 0: # Remaining files
    #         isolated -= 1
    #     if board.piece_at(square - 8) is not None and board.piece_at(square - 8).color == chess.WHITE:
    #         blocked -= 1
    # score -= 2 * (1 + endgame) * (doubled + blocked + isolated) # -0.2 per static weakness, increasing in the endgame

    # # King Safety (pawns in front of king)
    # king_safety = 0
    # if white_king != chess.E1: # Castled
    #     if white_king == chess.A1:
    #         critical_squares = (white_king + 8, white_king + 8 + 1)
    #     elif white_king == chess.H1:
    #         critical_squares = (white_king + 8, white_king + 8 - 1)
    #     else:
    #         critical_squares = (white_king + 8 - 1, white_king + 8, white_king + 8 + 1)
    #     for pawn_sq in critical_squares: # Critical pawns in front of king
    #         pawn_file =  pawn_sq % 8
    #         for curr_rank in range(1, 8):
    #             sq = curr_rank * 8 + pawn_file
    #             if board.piece_at(sq) is not None and board.piece_at(sq).piece_type == chess.PAWN and board.piece_at(sq).color == chess.WHITE: # Pawn found
    #                 king_safety += curr_rank - 1 if curr_rank > 2 else 0
    #                 break
    #         else: # No pawn on that file
    #             king_safety += 3
    # if black_king != chess.E8: # Castled
    #     if black_king == chess.A8:
    #         critical_squares = (black_king - 8, black_king - 8 + 1)
    #     elif black_king == chess.H8:
    #         critical_squares = (black_king - 8, black_king - 8 - 1)
    #     else:
    #         critical_squares = (black_king - 8 - 1, black_king - 8, black_king - 8 + 1)
    #     for pawn_sq in critical_squares: # Critical pawns in front of king
    #         pawn_file =  pawn_sq % 8
    #         for curr_rank in range(6, 0, -1):
    #             sq = curr_rank * 8 + pawn_file
    #             if board.piece_at(sq) is not None and board.piece_at(sq).piece_type == chess.PAWN and board.piece_at(sq).color == chess.BLACK: # Pawn found
    #                 king_safety -= 5 - curr_rank if curr_rank < 5 else 0
    #                 break
    #         else: # No pawn on that file
    #             king_safety -= 3
    # score -= 6 * (1 - endgame) * king_safety # -0.6 per point of king safety evaluation, decreasing in the endgame

    return round(score * (1 if board.turn else -1), 2)


def sort_moves(board, ply): # Sort normal moves
    global debug, tt, kt
    moves = {}
    killer_moves = kt.get_moves(ply)
    for move in board.legal_moves: # Evaluate all the moves using evaluation function
        if board.is_capture(move): # Captures
            board.push(move)
            moves[move] = evaluate(board) - 10000
            board.pop()
        elif killer_moves is not None and move in killer_moves: # Killer move ordering
            debug["killer move orders"] += 1
            moves[move] = -5000
        else: # Non-captures
            board.push(move)
            moves[move] = evaluate(board)
            board.pop()
    sorted_dict = sorted(moves.items(), key=lambda x: x[1])
    sorted_moves = [i[0] for i in sorted_dict] # Sort moves
    if (best_move := tt.get_best_move(chess.polyglot.zobrist_hash(board))) is not None: # If current position found
        if best_move in sorted_moves: # If best move found
            debug["tt move orders"] += 1
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


def quiescence(board, alpha, beta): # Quiescence search
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


def negamax(board, alpha, beta, depth, ply): # Main negamax search function
    global debug, tt, kt

    # call quiescence search at leaf node
    if depth == 0 or board.is_game_over() or board.can_claim_draw():
        if board.is_check():  # increment depth if last move is check
            depth += 1
        else:
            return quiescence(board, alpha, beta) # call quiescence search

    # null move pruning
    if depth > R and not board.is_check() and list(board.move_stack)[-1] != chess.Move.null(): # Check if null move can be played
        board.push(chess.Move.null()) # push null move
        score = -negamax(board, -beta, -beta + 1, depth - R - 1, ply + R + 1) # search with reduction R
        board.pop()
        if score >= beta: # check if there is a beta cutoff
            return beta
    
    if (val := tt.probe_hash(depth, alpha, beta, chess.polyglot.zobrist_hash(board))) is not None: # Transposition table lookup
        debug["tt hits"] += 1
        return val
    
    flag = TranspositionTable.ALPHA_FLAG
    best_move = chess.Move.null()

    # search child nodes
    for move_num, move in enumerate(moves := sort_moves(board, ply)): # Sort moves
        debug["positions"] += 1
        board.push(move)
        score = -negamax(board, -beta, -alpha, depth - 1, ply + 1)
        board.pop()
        if score >= beta: # Beta cutoff
            debug["beta cutoff move num"][0] += move_num
            debug["beta cutoff move num"][1] += 1
            debug["killer move stores"] += 1
            tt.record_hash(depth, TranspositionTable.BETA_FLAG, beta, move, chess.polyglot.zobrist_hash(board))
            if not board.is_capture(move):
                kt.add_move(move, ply)  # Store killer move
            return beta
        if score > alpha: # New best move found
            flag = TranspositionTable.EXACT_FLAG
            alpha = score
            best_move = move
    
    debug["beta cutoff move num"][0] += len(moves)
    debug["beta cutoff move num"][1] += 1
    if best_move != chess.Move.null():
        tt.record_hash(depth, flag, alpha, best_move, chess.polyglot.zobrist_hash(board)) # Transposition table store

    return alpha

def root_search(board, depth, alpha, beta): # Root negamax search function

    best_move_found = chess.Move.null()
    flag = TranspositionTable.ALPHA_FLAG
    ply = 0

    for move_num, move in enumerate(moves := sort_moves(board, ply)): # Iterate through sorted moves

        debug["positions"] += 1
        board.push(move)

        if board.is_checkmate():  # checks for M1
            board.pop()
            return move, -INF
        
        if board.can_claim_draw(): # Checks for draws
            score = 0
        else:
            score = -negamax(board, -beta, -alpha, depth - 1, ply + 1)

        is_repetition = board.is_repetition(2)
        board.pop()

        if evaluate(board) > 0 and is_repetition: # Do not allow bot to repeat moves when winning
            continue
        if depth >= 4:
            print(board.san(move), score) # Print score of move
        if score >= beta: # Beta cutoff
            debug["beta cutoff move num"][0] += move_num
            debug["beta cutoff move num"][1] += 1
            debug["killer move stores"] += 1
            tt.record_hash(depth, TranspositionTable.BETA_FLAG, beta, move, chess.polyglot.zobrist_hash(board))
            if not board.is_capture(move):
                kt.add_move(move, ply)  # Store killer move
            return move, beta
        if score > alpha: # New best move found
            flag = TranspositionTable.EXACT_FLAG
            alpha = score
            best_move_found = move
    
    debug["beta cutoff move num"][0] += len(moves)
    debug["beta cutoff move num"][1] += 1
    if best_move_found != chess.Move.null():
        tt.record_hash(depth, flag, alpha, best_move_found, chess.polyglot.zobrist_hash(board)) # Transposition table store

    return best_move_found, alpha # Return the score as well for aspiration window

def get_pv_line(board, depth): # Function to get principal variation for printing purposes
    global tt
    pv = []
    curr = copy.deepcopy(board)
    while (best_move := tt.get_best_move(chess.polyglot.zobrist_hash(curr))) is not None: # If there is a next best move
        curr.push(best_move) # Update board
        pv.append(best_move) # Add to PV list
        if len(pv) > depth:
            break
    return pv

def get_best_move(board, max_depth): # Function to get best move after search
    global debug, tt, kt

    tt = TranspositionTable() # Initialise transposition table
    kt = KillerMovesTable() # Initialise killer moves table
 
    try:
        return chess.polyglot.MemoryMappedReader("../Titans.bin").weighted_choice(board).move # Opening book

    except IndexError:

        max_depth += (dinc := int(4 * endgame_score(board)))
        if dinc > 0:
            print(f"Max depth incremented by +{dinc}")

        alpha = -INF
        beta = INF
        debug = {"positions": 0, "tt move orders": 0, "tt hits": 0, "killer move orders": 0, "killer move stores": 0, "beta cutoff move num": [0, 0]} # Debug dictionary
        stime = time.perf_counter()
        print(f"Current Evaluation: {evaluate(board)}")

        for depth in range(1, max_depth + 1): # Iterative deepening
            
            best_move_found, score = root_search(board, depth, alpha, beta) # Search at given depth
            print(f"PV line: {' '.join(list(map(str, pv_line := get_pv_line(board, depth))))}") # Print the principal variation
            print(f"Depth {depth} complete, best move found is {best_move_found}, nodes taken: {debug['positions']}")

            # Aspiration window
            if score <= alpha or score >= beta: # If the score lies outside the alpha-beta range
                alpha = -INF
                beta = INF # Reset the bounds
            else:
                alpha = score - WINDOW
                beta = score + WINDOW # Otherwise make the alpha-beta window narrower

        debug["time"] = round(time.perf_counter() - stime, 2)
        try:
            debug["positions per second"] = round(debug["positions"] / debug["time"], 2)
        except ZeroDivisionError:
            debug["positions per second"] = "inf"
        debug["tt length"] = tt.length
        try:
            debug["beta cutoff move num"] = debug["beta cutoff move num"][0] / debug["beta cutoff move num"][1]
        except ZeroDivisionError:
            debug["beta cutoff move num"] = "inf"
        print(f"{VERSION} DEBUG: {debug}")
        times.append(debug["time"])
        print(f"{VERSION} Average Time: {sum(times)/len(times)}, Total Time: {sum(times)}")

        return pv_line[0] if pv_line else best_move_found

