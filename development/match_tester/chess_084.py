# Imports
import concurrent.futures
from threading import Lock
import chess.polyglot
import chess.svg
import time
import copy

VERSION = "v0.82" # Version
INF = 99999 # Infinity value
R = 2 # Null move pruning reduction R
PAWN_VAL = 10
WINDOW = 1/4 * PAWN_VAL # Aspiration window value = 1/4 of a pawn


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
    
    @property
    def data(self):
        return self.__table
    
    def combine(self, tt):
        for k, v in tt.data.items():
            self.__table[k] = v

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
    
    @property
    def data(self):
        return self.__table
    
    def combine(self, kt):
        for k, v in kt.data.items():
            self.__table[k] = v

# Thread-safe shared state for alpha and beta
class SharedState:
    def __init__(self, alpha, beta):
        self.__alpha = alpha
        self.__beta = beta
        self.__lock = Lock()

    def update_alpha(self, new_alpha):
        with self.__lock:
            if new_alpha > self.__alpha:
                self.__alpha = new_alpha

    def update_beta(self, new_beta):
        with self.__lock:
            if new_beta < self.__beta:
                self.__beta = new_beta

    def get_alpha(self):
        with self.__lock:
            return self.__alpha

    def get_beta(self):
        with self.__lock:
            return self.__beta

shared_state = SharedState(-INF, INF)

class ChessEngine:

    WORKERS = [1, 1, 2, 3, 4, 5, 6]

    def __init__(self):

        self.__times = []
        
    def evaluate(self, board): # Evaluation function
        Eval = 0

        if board.is_checkmate():
            return -INF
        if board.is_stalemate():
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


    def sort_moves(self, board, ply, tt, kt, debug): # Sort normal moves
        moves = {}
        killer_moves = kt.get_moves(ply)
        for move in board.legal_moves: # Evaluate all the moves using evaluation function
            if board.is_capture(move): # Captures
                board.push(move)
                moves[move] = self.evaluate(board) - 10000
                board.pop()
            elif killer_moves is not None and move in killer_moves: # Killer move ordering
                debug["killer move orders"] += 1
                moves[move] = -5000
            else: # Non-captures
                board.push(move)
                moves[move] = self.evaluate(board)
                board.pop()
        sorted_dict = sorted(moves.items(), key=lambda x: x[1])
        sorted_moves = [i[0] for i in sorted_dict] # Sort moves
        if (best_move := tt.get_best_move(chess.polyglot.zobrist_hash(board))) is not None: # If current position found
            if best_move in sorted_moves: # If best move found
                debug["tt move orders"] += 1
                sorted_moves.remove(best_move)
                sorted_moves.insert(0, best_move) # Move best move to the start of the list
        return sorted_moves


    def sort_captures(self, board): # Sort captures
        moves = {}
        for move in list(board.generate_legal_captures()):
            board.push(move)
            moves[move] = self.evaluate(board)
            board.pop()
        sorted_dict = sorted(moves.items(), key=lambda x: x[1])
        return [i[0] for i in sorted_dict]


    def quiescence(self, board, alpha, beta, debug): # Quiescence search

        stand_pat = self.evaluate(board)

        if stand_pat >= beta:
            return beta

        if alpha < stand_pat:
            alpha = stand_pat

        for move in self.sort_captures(board):
            debug["positions"] += 1
            board.push(move)
            score = -self.quiescence(board, -beta, -alpha, debug)
            board.pop()

            if score >= beta:
                return beta

            if score > alpha:
                alpha = score

        return alpha


    def negamax(self, board, alpha, beta, depth, ply, tt, kt, debug): # Main negamax search function
        global shared_state

        # call quiescence search at leaf node
        if depth == 0 or board.is_game_over() or board.can_claim_draw():
            if board.is_check():  # increment depth if last move is check
                depth += 1
            else:
                return self.quiescence(board, alpha, beta, debug) # call quiescence search

        # null move pruning
        if depth > R and not board.is_check() and list(board.move_stack)[-1] != chess.Move.null(): # Check if null move can be played
            board.push(chess.Move.null()) # push null move
            score = -self.negamax(board, -beta, -beta + 1, depth - R - 1, ply + R + 1, tt, kt, debug) # search with reduction R
            board.pop()
            if score >= beta: # check if there is a beta cutoff
                return beta
        
        if (val := tt.probe_hash(depth, alpha, beta, chess.polyglot.zobrist_hash(board))) is not None: # Transposition table lookup
            debug["tt hits"] += 1
            return val
        
        flag = TranspositionTable.ALPHA_FLAG
        best_move = chess.Move.null()

        # search child nodes
        for move in self.sort_moves(board, ply, tt, kt, debug): # Sort moves

            debug["positions"] += 1
            board.push(move)

            score = -self.negamax(board, -beta, -alpha, depth - 1, ply + 1, tt, kt, debug)

            board.pop()

            if score >= beta: # Beta cutoff
                debug["killer move stores"] += 1
                tt.record_hash(depth, TranspositionTable.BETA_FLAG, beta, move, chess.polyglot.zobrist_hash(board))
                if not board.is_capture(move):
                    kt.add_move(move, ply)  # Store killer move
                return beta
            if score > alpha: # New best move found
                flag = TranspositionTable.EXACT_FLAG
                alpha = score
                best_move = move
        
        if best_move != chess.Move.null():
            tt.record_hash(depth, flag, alpha, best_move, chess.polyglot.zobrist_hash(board)) # Transposition table store
    
        return alpha

    def worker(self, move, board_fen, depth, ply, unified_tt, unified_kt):
        global shared_state

        board = chess.Board(board_fen)

        tt = copy.deepcopy(unified_tt)
        kt = copy.deepcopy(unified_kt)
        debug = {"positions": 0, "tt move orders": 0, "tt hits": 0, "killer move orders": 0, "killer move stores": 0} # Debug dictionary

        print(move, shared_state.get_alpha(), shared_state.get_beta())

        board.push(move)

        if board.is_checkmate():  # checks for M1
            board.pop()
            return move, -INF
            
        if board.can_claim_draw(): # Checks for draws
            score = 0
        else:
            score = -self.negamax(board, -shared_state.get_beta(), -shared_state.get_alpha(), depth - 1, ply + 1, tt, kt, debug)

        is_repetition = board.is_repetition(2)
        shared_state.update_alpha(score)

        return move, score, is_repetition, tt, kt, debug

    def root_search(self, board : chess.Board, depth, workers): # Root negamax search function
        global shared_state

        best_move_found = chess.Move.null()
        flag = TranspositionTable.ALPHA_FLAG
        ply = 0

        sorted_moves = self.sort_moves(board, ply, self.__tt, self.__kt, self.__debug)
        board_fen = board.fen()

        print(depth, shared_state.get_alpha(), shared_state.get_beta())

        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:

            futures = [executor.submit(self.worker, move, board_fen, depth, ply, self.__tt, self.__kt) for move in sorted_moves]

            for future in concurrent.futures.as_completed(futures):

                self.__debug["positions"] += 1

                move, score, is_repetition, tt, kt, debug = future.result()

                self.__tt.combine(tt) # Combine transposition table
                self.__kt.combine(kt) # Combine killer moves table

                # Combine debug dictionary
                for k, v in debug.items():
                    self.__debug[k] += v

                if self.evaluate(board) > 0 and is_repetition: # Do not allow bot to repeat moves when winning
                    continue

                if depth >= 4:
                    print(board.san(move), score) # Print score of move
                    #print(debug["positions"], shared_state.get_alpha(), shared_state.get_beta())
                
                if score >= shared_state.get_beta(): # Beta cutoff
                    self.__debug["killer move stores"] += 1
                    self.__tt.record_hash(depth, TranspositionTable.BETA_FLAG, shared_state.get_beta(), move, chess.polyglot.zobrist_hash(board))
                    if not board.is_capture(move):
                        self.__kt.add_move(move, ply)  # Store killer move
                    return move, shared_state.get_beta()
                
                if score > shared_state.get_alpha(): # Raise alpha
                    flag = TranspositionTable.EXACT_FLAG
                    shared_state.update_alpha(score)
                    best_move_found = move
        
        if best_move_found != chess.Move.null():
            self.__tt.record_hash(depth, flag, shared_state.get_alpha(), best_move_found, chess.polyglot.zobrist_hash(board)) # Transposition table store

        return best_move_found, shared_state.get_alpha() # Return the score as well for aspiration window

    def get_pv_line(self, board, depth): # Function to get principal variation for printing purposes
        pv = []
        curr = copy.deepcopy(board)
        while (best_move := self.__tt.get_best_move(chess.polyglot.zobrist_hash(curr))) is not None: # If there is a next best move
            curr.push(best_move) # Update board
            pv.append(best_move) # Add to PV list
            if len(pv) > depth:
                break
        return pv

    def get_best_move(self, board, max_depth): # Function to get best move after search
        global shared_state
        
        try:
            return chess.polyglot.MemoryMappedReader("../Titans.bin").weighted_choice(board).move # Opening book

        except IndexError:

            self.__tt = TranspositionTable() # Initialise transposition table
            self.__kt = KillerMovesTable() # Initialise killer moves table
            self.__debug = {"positions": 0, "tt move orders": 0, "tt hits": 0, "killer move orders": 0, "killer move stores": 0} # Debug dictionary

            alpha = -INF
            beta = INF
            stime = time.perf_counter()
            print(f"Current Evaluation: {self.evaluate(board)}")

            for depth in range(1, max_depth + 1): # Iterative deepening

                shared_state = SharedState(alpha, beta)
                
                best_move_found, score = self.root_search(board, depth, workers=self.WORKERS[depth]) # Search at given depth
                print(f"PV line: {' '.join(list(map(str, pv_line := self.get_pv_line(board, depth))))}") # Print the principal variation
                print(f"Depth {depth} complete, best move found is {best_move_found}, nodes taken: {self.__debug['positions']}")

                # Aspiration window
                if score <= alpha or score >= beta: # If the score lies outside the alpha-beta range
                    print("RESETTED", score, alpha, beta, shared_state.get_alpha(), shared_state.get_beta())
                    alpha = -INF
                    beta = INF # Reset the bounds
                else:
                    alpha = score - WINDOW
                    beta = score + WINDOW # Otherwise make the alpha-beta window narrower

            self.__debug["time"] = round(time.perf_counter() - stime, 2)
            try:
                self.__debug["positions per second"] = round(self.__debug["positions"] / self.__debug["time"], 2)
            except ZeroDivisionError:
                self.__debug["positions per second"] = "inf"
            self.__debug["tt length"] = self.__tt.length

            print(f"{VERSION} DEBUG: {self.__debug}")
            self.__times.append(self.__debug["time"])
            print(f"{VERSION} Average Time: {sum(self.__times)/len(self.__times)}, Total Time: {sum(self.__times)}")

            return pv_line[0] if pv_line else best_move_found

