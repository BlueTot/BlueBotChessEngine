'''Imports'''
import chess.polyglot
import chess.svg
import time
import copy

'''Piece Square Tables & MVV/LVA Tables'''

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

# MVV LVA table
# attacker  K  Q  R  B  N  P  None
MVV_LVA = [[0, 0, 0, 0, 0, 0, 0], # victim K
           [50, 51, 52, 53, 54, 55, 0], # victim Q
           [40, 41, 42, 43, 44, 45, 0], # victim R
           [30, 31, 32, 33, 34, 35, 0], # victim B
           [20, 21, 22, 23, 24, 25, 0], # victim N
           [10, 11, 12, 13, 14, 15, 0], # victim P
           [0, 0, 0, 0, 0, 0, 0]] # victim None

PIECE_INDEXES = {chess.KING: 0, chess.QUEEN: 1, chess.ROOK: 2, chess.BISHOP: 3, chess.KNIGHT: 4, chess.PAWN: 5, None: 6}

'''Hash Tables'''

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

class HistoryMovesTable: # History moves table class

    def __init__(self):
        self.__table = {}
    
    def add_move(self, turn, move, depth):
        if (turn, move.from_square, move.to_square) not in self.__table:
            self.__table[(turn, move.from_square, move.to_square)] = 0
        self.__table[(turn, move.from_square, move.to_square)] += 2 ** depth
    
    def get_move_score(self, turn, move):
        if (turn, move.from_square, move.to_square) in self.__table:
            return self.__table[(turn, move.from_square, move.to_square)]
    
    def __repr__(self):
        return str(self.__table)
    
'''Blue Bot Chess Engine'''

class ChessEngine: # Chess engine class

    VERSION = "v0.77" # Version
    INF = 99999 # Infinity value
    R = 2 # Null move pruning reduction R
    PAWN_VAL = 10
    WINDOW = 1/4 * PAWN_VAL # Aspiration window value = 1/4 of a pawn
    ENDGAME_UPPER, ENDGAME_LOWER = 100, 270

    # Constructor
    def __init__(self):

        self.__times = []
        self.__debug = {"positions": 0, "tt move orders": 0, "tt hits": 0, "killer move orders": 0, 
                        "killer move stores": 0, "beta cutoff move num": {}, "qt hits": 0, "qt move orders": 0,
                        "history move orders": 0, "msnodes": 0, "lnodes": 0} # Debug dictionary
        self.__tt = TranspositionTable() # Initialise transposition table
        self.__qt = TranspositionTable() # Initialise quiescence search transposition table
        self.__kt = KillerMovesTable() # Initialise killer moves table
        self.__ht = HistoryMovesTable() # Initialise history moves table

    def __reset_tables(self):
        self.__init__()

    def __endgame_score(self, board : chess.Board):
        mm_material = 0
        for square in range(64):
            piece = board.piece_at(square)
            if piece is not None and piece.piece_type in (chess.QUEEN, chess.ROOK, chess.KNIGHT, chess.BISHOP):
                mm_material += MATERIAL[piece.piece_type]
        if mm_material < self.ENDGAME_UPPER:
            endgame = 1
        elif mm_material > self.ENDGAME_LOWER:
            endgame = 0
        else:
            endgame = (mm_material - self.ENDGAME_LOWER) / (self.ENDGAME_UPPER - self.ENDGAME_LOWER)
        return endgame

    def __evaluate(self, board : chess.Board): # Evaluation function
        score = 0

        # Initial checks
        if board.is_checkmate():
            return -self.INF
        if board.is_stalemate():
            return 0

        # Game Stage Calculation
        endgame = self.__endgame_score(board)
        
        # Material and Piece Square Tables
        for square in range(64):
            row, col = divmod(square, 8)
            piece = board.piece_at(square)

            if piece is not None:

                mult = 1 if piece.color else -1

                match piece.piece_type:
                    case chess.KING:
                        score += mult * (900 + (KING if piece.color else R_KING)[row][col]) * (1 - endgame) # King Middlegame
                        score += mult * (900 + (KING_END if piece.color else R_KING_END)[row][col]) * endgame # King Endgame
                    case chess.QUEEN:
                        score += mult * (88 + (QUEEN if piece.color else R_QUEEN)[row][col])
                    case chess.ROOK:
                        score += mult * (51 + (ROOK if piece.color else R_ROOK)[row][col])
                    case chess.BISHOP:
                        score += mult * (32 + (BISHOP if piece.color else R_BISHOP)[row][col])
                    case chess.KNIGHT:
                        score += mult * (30 + (KNIGHT if piece.color else R_KNIGHT)[row][col])
                    case chess.PAWN:
                        score += mult * (10 + (PAWN if piece.color else R_PAWN)[row][col]) * (1 - endgame) # Pawn Middlegame
                        score += mult * (10 + (PAWN_END if piece.color else R_PAWN_END)[row][col]) * endgame # Pawn Endgame

        return round(score * (1 if board.turn else -1), 2)

    def __capture_value(self, board : chess.Board, move : chess.Move): # Depth 1 Static Exchange Evaluation
        victim = piece.piece_type if (piece := board.piece_at(move.to_square)) is not None else chess.PAWN
        attacker = piece.piece_type if (piece := board.piece_at(move.from_square)) is not None else None
        if board.attackers(not board.turn, move.to_square): # is defended
            return MATERIAL[victim] - MATERIAL[attacker]
        return MATERIAL[victim] # hanging piece

    '''Move Ordering:
        1. PV Move
        2. Good or Equal Captures
        3. Killer Moves (2)
        4. Bad Captures
        5. Quiet Moves sorted by History Heuristic
    '''
    def __sort_moves(self, board : chess.Board, ply): # Sort normal moves

        legal_moves = list(board.legal_moves)
        if (best_move := self.__tt.get_best_move(chess.polyglot.zobrist_hash(board))) is not None: # If current position found
            if best_move in legal_moves: # If best move found
                self.__debug["tt move orders"] += 1
                legal_moves.remove(best_move)
                yield best_move
        moves = {}
        killer_moves = self.__kt.get_moves(ply)
        for move in legal_moves: # Evaluate all the moves using evaluation function
            if board.is_capture(move): # Captures
                value = self.__capture_value(board, move)
                moves[move ] = -value - (10000 if value >= 0 else 2500)
            elif killer_moves is not None and move in killer_moves: # Killer move ordering
                self.__debug["killer move orders"] += 1
                moves[move] = -5000
            else: # Non-captures
                if (score := self.__ht.get_move_score(board.turn, move)) is not None: # History move found
                    self.__debug["history move orders"] += 1
                    moves[move] = -score # History move ordering
                else: # Otherwise
                    board.push(move)
                    moves[move] = self.__evaluate(board) # Normal evaluation
                    board.pop()
        sorted_dict = sorted(moves.items(), key=lambda x: x[1])
        for i in sorted_dict:
            yield i[0] 

    def __sort_captures(self, board : chess.Board): # Sort captures

        legal_captures = list(board.generate_legal_captures())
        if (best_move := self.__qt.get_best_move(chess.polyglot.zobrist_hash(board))) is not None: # If current position found
            if best_move in legal_captures: # If best move found
                self.__debug["qt move orders"] += 1
                legal_captures.remove(best_move)
                yield best_move
        moves = {}
        for move in legal_captures: # Sort moves using MVV/LVA
            victim = piece.piece_type if (piece := board.piece_at(move.to_square)) is not None else None
            attacker = piece.piece_type if (piece := board.piece_at(move.from_square)) is not None else None
            moves[move] = -MVV_LVA[PIECE_INDEXES[victim]][PIECE_INDEXES[attacker]]
        sorted_dict = sorted(moves.items(), key=lambda x: x[1])
        for i in sorted_dict:
            yield i[0]

    def __quiescence(self, board : chess.Board, alpha, beta): # Quiescence search

        if (val := self.__qt.probe_hash(0, alpha, beta, chess.polyglot.zobrist_hash(board))) is not None: # Q-search transposition table lookup
            self.__debug["qt hits"] += 1
            return val
        
        flag = TranspositionTable.ALPHA_FLAG
        best_move_found = chess.Move.null()
        stand_pat = self.__evaluate(board)

        if stand_pat >= beta:
            return beta

        if alpha < stand_pat:
            alpha = stand_pat

        for move in self.__sort_captures(board):
            self.__debug["positions"] += 1
            board.push(move)
            score = -self.__quiescence(board, -beta, -alpha)
            board.pop()

            if score >= beta:
                self.__qt.record_hash(0, TranspositionTable.BETA_FLAG, beta, move, chess.polyglot.zobrist_hash(board))
                return beta

            if score > alpha:
                flag = TranspositionTable.EXACT_FLAG
                alpha = score
                best_move_found = move
        
        if best_move_found != chess.Move.null():
            self.__qt.record_hash(0, flag, alpha, best_move_found, chess.polyglot.zobrist_hash(board)) # Transposition table store

        return alpha


    def __negamax(self, board : chess.Board, alpha, beta, depth, ply): # Main negamax search function

        # call quiescence search at leaf node
        if depth == 0 or board.is_game_over() or board.can_claim_draw():
            self.__debug["lnodes"] += 1
            return self.__quiescence(board, alpha, beta) # call quiescence search
        
        # check extensions
        if board.is_check():
            depth += 1

        # null move pruning
        if depth > self.R and not board.is_check() and list(board.move_stack)[-1] != chess.Move.null(): # Check if null move can be played
            board.push(chess.Move.null()) # push null move
            score = -self.__negamax(board, -beta, -beta + 1, depth - self.R - 1, ply + self.R + 1) # search with reduction R
            board.pop()
            if score >= beta: # check if there is a beta cutoff
                return beta
        
        if (val := self.__tt.probe_hash(depth, alpha, beta, chess.polyglot.zobrist_hash(board))) is not None: # Transposition table lookup
            self.__debug["tt hits"] += 1
            return val
        
        flag = TranspositionTable.ALPHA_FLAG
        best_move = chess.Move.null()
        move_num = 0

        # search child nodes
        for move in self.__sort_moves(board, ply): # Sort moves

            self.__debug["positions"] += 1
            self.__debug["msnodes"] += 1
            board.push(move)

            score = -self.__negamax(board, -beta, -alpha, depth - 1, ply + 1) # Score move

            board.pop()

            if score >= beta: # Beta cutoff

                if move_num not in self.__debug["beta cutoff move num"]:
                    self.__debug["beta cutoff move num"][move_num] = 0
                self.__debug["beta cutoff move num"][move_num] += 1

                self.__debug["killer move stores"] += 1

                self.__tt.record_hash(depth, TranspositionTable.BETA_FLAG, beta, move, chess.polyglot.zobrist_hash(board))
                if not board.is_capture(move):
                    self.__kt.add_move(move, ply)  # Store killer move
                    self.__ht.add_move(board.turn, move, depth) # Store history move
                return beta
            
            if score > alpha: # New best move found
                flag = TranspositionTable.EXACT_FLAG
                alpha = score
                best_move = move
            move_num += 1
        
        if move_num not in self.__debug["beta cutoff move num"]:
            self.__debug["beta cutoff move num"][move_num] = 0
        self.__debug["beta cutoff move num"][move_num] += 1

        if best_move != chess.Move.null():
            self.__tt.record_hash(depth, flag, alpha, best_move, chess.polyglot.zobrist_hash(board)) # Transposition table store
            self.__ht.add_move(board.turn, best_move, depth) # Store history move

        return alpha

    def __root_search(self, board : chess.Board, depth, alpha, beta): # Root negamax search function

        # initialisation
        best_move_found = chess.Move.null()
        flag = TranspositionTable.ALPHA_FLAG
        ply = 0
        move_num = 0

        # search child nodes
        for move in self.__sort_moves(board, ply):

            self.__debug["positions"] += 1
            self.__debug["msnodes"] += 1
            board.push(move)

            # TOP-LEVEL CHECKS
            if board.is_checkmate():  # checks for M1
                board.pop()
                return move, -self.INF
            
            if board.can_claim_draw(): # Checks for draws
                score = 0
            else:
                score = -self.__negamax(board, -beta, -alpha, depth - 1, ply + 1) # score move

            is_repetition = board.is_repetition(2) # check for repetition
            board.pop()

            if self.__evaluate(board) > 0 and is_repetition: # Do not allow bot to repeat moves when winning
                continue

            if depth >= 4:
                print(board.san(move), score) # Print score of move

            if score >= beta: # Beta cutoff

                if move_num not in self.__debug["beta cutoff move num"]:
                    self.__debug["beta cutoff move num"][move_num] = 0
                self.__debug["beta cutoff move num"][move_num] += 1

                self.__debug["killer move stores"] += 1

                self.__tt.record_hash(depth, TranspositionTable.BETA_FLAG, beta, move, chess.polyglot.zobrist_hash(board))
                if not board.is_capture(move): # Not a capture
                    self.__kt.add_move(move, ply)  # Store killer move
                    self.__ht.add_move(board.turn, move, depth) # Store history move
                return move, beta
            
            if score > alpha: # New best move found
                flag = TranspositionTable.EXACT_FLAG
                alpha = score
                best_move_found = move
            
            move_num += 1

        if move_num not in self.__debug["beta cutoff move num"]:
            self.__debug["beta cutoff move num"][move_num] = 0
        self.__debug["beta cutoff move num"][move_num] += 1

        if best_move_found != chess.Move.null():
            self.__tt.record_hash(depth, flag, alpha, best_move_found, chess.polyglot.zobrist_hash(board)) # Transposition table store
            self.__ht.add_move(board.turn, best_move_found, depth) # Store history move

        return best_move_found, alpha # Return the score as well for aspiration window

    def __get_pv_line(self, board : chess.Board, depth): # Function to get principal variation for printing purposes
        pv = []
        curr = copy.deepcopy(board)
        while (best_move := self.__tt.get_best_move(chess.polyglot.zobrist_hash(curr))) is not None: # If there is a next best move
            curr.push(best_move) # Update board
            pv.append(best_move) # Add to PV list
            if len(pv) > depth:
                break
        return pv

    def get_best_move(self, board : chess.Board, max_depth): # Function to get best move after search

        self.__reset_tables()
    
        try:
            return chess.polyglot.MemoryMappedReader("../Titans.bin").weighted_choice(board).move # Opening book

        except IndexError:

            alpha = -self.INF
            beta = self.INF
            stime = time.perf_counter()
            print(f"Current Evaluation: {self.__evaluate(board)}")

            for depth in range(1, max_depth + 1): # Iterative deepening
                
                best_move_found, score = self.__root_search(board, depth, alpha, beta) # Search at given depth
                print(f"PV line: {' '.join(list(map(str, pv_line := self.__get_pv_line(board, depth))))}") # Print the principal variation
                print(f"Depth {depth} complete, best move found is {best_move_found}, nodes taken: {self.__debug['positions']}")

                # Aspiration window
                if score <= alpha or score >= beta: # If the score lies outside the alpha-beta range
                    alpha = -self.INF
                    beta = self.INF # Reset the bounds
                else:
                    alpha = score - self.WINDOW
                    beta = score + self.WINDOW # Otherwise make the alpha-beta window narrower

            self.__debug["time"] = round(time.perf_counter() - stime, 2)

            try:
                self.__debug["positions per second"] = round(self.__debug["positions"] / self.__debug["time"], 2)
            except ZeroDivisionError:
                self.__debug["positions per second"] = "inf"

            self.__debug["tt length"] = self.__tt.length
            
            try:
                self.__debug["beta cutoff move num"] = sum([k*v for k, v in self.__debug["beta cutoff move num"].items()]) / sum(list(self.__debug["beta cutoff move num"].values()))
                self.__debug["ebf"] = (self.__debug["msnodes"] + self.__debug["lnodes"]) / self.__debug["msnodes"]
            except ZeroDivisionError:
                pass

            print(f"{self.VERSION} DEBUG: {self.__debug}")
            self.__times.append(self.__debug["time"])
            print(f"{self.VERSION} Average Time: {sum(self.__times)/len(self.__times)}, Total Time: {sum(self.__times)}")

            return pv_line[0] if pv_line else best_move_found
