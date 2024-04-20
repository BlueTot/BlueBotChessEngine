import chess
import chess_022, chess_029, chess_034, chess_035, chess_036, chess_037, chess_038, chess_039, chess_040, chess_041, chess_042, chess_043, chess_044, chess_045, chess_046, chess_047, chess_048


class Player:
    name = "player"
    tag = 1

class Chess022:
    depth = 6
    name = f"Chess v0.22 (depth {depth})"
    tag = (chess_022.get_best_move, depth)

class Chess029:
    depth = 6
    name = f"Chess v0.29 (depth {depth})"
    tag = (chess_029.get_best_move, depth)

class Chess034:
    depth = 6
    name = f"Chess v0.34 (depth {depth})"
    tag = (chess_034.get_best_move, depth)

class Chess035:
    depth = 6
    name = f"Chess v0.35 (depth {depth})"
    tag = (chess_035.get_best_move, depth)

class Chess036:
    depth = 6
    name = f"Chess v0.36 (depth {depth})"
    tag = (chess_036.get_best_move, depth)

class Chess037:
    depth = 6
    name = f"Chess v0.37 (depth {depth})"
    tag = (chess_037.get_best_move, depth)

class Chess038:
    depth = 6
    name = f"Chess v0.38 (depth {depth})"
    tag = (chess_038.get_best_move, depth)

class Chess039:
    depth = 6
    name = f"Chess v0.39 (depth {depth})"
    tag = (chess_039.get_best_move, depth)

class Chess040:
    depth = 7
    name = f"Chess v0.40 (depth {depth})"
    tag = (chess_040.get_best_move, depth)

class Chess041:
    depth = 6
    name = f"Chess v0.41 (depth {depth})"
    tag = (chess_041.get_best_move, depth)

class Chess042:
    depth = 6
    name = f"Chess v0.42 (depth {depth})"
    tag = (chess_042.get_best_move, depth)

class Chess043:
    depth = 6
    name = f"Chess v0.43 (depth {depth})"
    tag = (chess_043.get_best_move, depth)

class Chess044:
    depth = 6
    name = f"Chess v0.44 (depth {depth})"
    tag = (chess_044.get_best_move, depth)

class Chess045:
    depth = 6
    name = f"Chess v0.45 (depth {depth})"
    tag = (chess_045.get_best_move, depth)

class Chess046:
    depth = 6
    name = f"Chess v0.46 (depth {depth})"
    tag = (chess_046.get_best_move, depth)

class Chess047:
    depth = 6
    name = f"Chess v0.47 (depth {depth})"
    tag = (chess_047.get_best_move, depth)

class Chess048:
    depth = 6
    name = f"Chess v0.48 (depth {depth})"
    tag = (chess_048.get_best_move, depth)

class ChessGame:
    def __init__(self, player1, player2, fen=None, turn=chess.WHITE):

        self.__board = chess.Board()
        if fen is not None:
            self.__board.set_board_fen(fen)
        self.__board.turn = turn

        self.__player1 = player1.tag
        self.__player2 = player2.tag
        self.__gameOver = False
        self.__moves = []

        print(f"\033[32;1;1mChess: {player1.name} vs {player2.name}\033[0m")
    
    def insert_move(self, san):
        self.__moves.append(san)
        self.__board.push_san(san)

    def __player_make_move(self):
        san = input("PLAYER make a move: ")
        try:
            self.__moves.append(san)
            self.__board.push_san(san)
        except Exception:
            print("Illegal move")

    def __computer_make_move(self):
        turn = self.__player1 if self.__board.turn else self.__player2
        move = turn[0](self.__board, turn[1])
        if move == chess.Move.null():
            move = list(self.__board.legal_moves)[-1]
        try:
            san = self.__board.san(move)
            print(f"\033[32;1;1m{san}\033[0m")
            self.__moves.append(san)
        except AssertionError:
            pass
        self.__board.push(move)
        print(f"FEN: {self.__board.fen()}")

    def play(self):

        while not self.__gameOver: # If game is still ongoing

            print(self.__board) # Print the board

            # Make next move
            if self.__board.turn:
                self.__computer_make_move() if type(self.__player1) == tuple else self.__player_make_move()
            else:
                self.__computer_make_move() if type(self.__player2) == tuple else self.__player_make_move()

            if self.__board.is_checkmate():  # Checkmate
                print(f"{'White' if not self.__board.turn else 'Black'} won the game by checkmate!")
                self.__gameOver = True
                print(self.__moves)

            if self.__board.is_stalemate():  # Stalemate
                print("Draw by stalemate")
                self.__gameOver = True
                print(self.__moves)

            if self.__board.can_claim_draw():
                print("Draw by threefold repetition")
                self.__gameOver = True
                print(self.__moves)

            if self.__board.is_insufficient_material():
                print("Draw by insufficient material")
                self.__gameOver = True
                print(self.__moves)

if __name__ in "__main__":  # Run the game
    bot = (input("COLOUR: ") == "white")
    bot_perspective = True
    version = Chess048
    game = ChessGame(player1=version() if bot else Player(),
                     player2=Player() if bot else version())
    game.play()

'''
Tournament between v0.40 and v0.34 [0.5-3.5]

Game 1: v0.40 (WHITE) vs 0.34 (BLACK) : 1/2-1/2
['e4', 'c5', 'Nf3', 'e6', 'd4', 'cxd4', 'Nxd4', 'Nc6', 'Nc3', 'd6', 'Be3', 'Nf6', 'f4', 'e5', 'Nf3', 'Ng4', 'Qd2', 'Nxe3', 'Qxe3', 'exf4', 'Qxf4', 'Be7', 'O-O-O', 'O-O', 'Nb5', 'Be6', 'Nxd6', 'Qb8', 'a3', 'Rd8', 'e5', 'Nxe5', 'Nxe5', 'Bxd6', 'Re1', 'Ba2', 'Qf5', 'Re8', 'Bc4', 'Bxc4', 'Nxc4', 'Rxe1+', 'Rxe1', 'Bxh2', 'Kb1', 'Qc7', 'Qb5', 'h6', 'Re8+', 'Rxe8', 'Qxe8+', 'Kh7', 'Qe4+', 'Kg8', 'Qe8+', 'Kh7', 'Qe4+', 'Kh8', 'Qe8+']
v0.40 Average Time: 2.668333333333334, Total Time: 48.03000000000001
v0.34 Average Time: 6.722941176470589, Total Time: 114.29

Game 2: v0.34 (WHITE) vs v0.40 (BLACK) : 1-0
['d4', 'd5', 'c4', 'c6', 'Nc3', 'Nf6', 'e3', 'e6', 'Nf3', 'Nbd7', 'Bd3', 'dxc4', 'Bxc4', 'b5', 'Bd3', 'a6', 'e4', 'c5', 'e5', 'cxd4', 'Nxb5', 'axb5', 'exf6', 'Qb6', 'fxg7', 'Bxg7', 'O-O', 'Bb7', 'Qe2', 'b4', 'Be4', 'b3', 'Bxb7', 'Rxa2', 'Bf4', 'Qxb7', 'Rad1', 'O-O', 'Nxd4', 'e5', 'Nf5', 'Bf6', 'Bh6', 'Ra4', 'Qd3', 'Rg4', 'f3', 'Rb4', 'Qxd7', 'Qxd7', 'Rxd7', 'Rd8', 'Ne7+', 'Bxe7', 'Rxe7', 'Rb6', 'Bg5', 'Rd5', 'f4', 'h6', 'Bh4', 'Rb4', 'Bg3', 'e4', 'Be1', 'Rc4', 'Rb7', 'e3', 'Rb8+', 'Kh7', 'Rxb3', 'e2', 'Rf2', 'Re4', 'Rff3', 'Rd1', 'Kf2', 'Re7', 'Rfe3', 'Rxe3', 'Rxe3', 'Rd4', 'g3', 'Rd6', 'Rxe2', 'Rd8', 'Bc3', 'Rd7', 'Re8', 'Rd6', 'Re7', 'Kg8', 'Re8+', 'Kh7', 'Rf8', 'Kg6', 'Rg8+', 'Kf5', 'Rg7', 'Ke6', 'Rh7', 'Rd1', 'Rxh6+', 'Ke7', 'Kg2', 'Rc1', 'Rh7', 'Rc2+', 'Kg1', 'Rc1+', 'Kf2', 'Rc2+', 'Kf1', 'Rc1+', 'Ke2', 'Kf8', 'Rh8+', 'Ke7', 'Kf2', 'Rc2+', 'Kg1', 'Rc1+', 'Kg2', 'Rc2+', 'Kh1', 'Rc1+', 'Be1', 'Rxe1+', 'Kg2', 'Re2+', 'Kg1', 'Rxb2', 'f5', 'Rb1+', 'Kg2', 'Rb2+', 'Kh1', 'Rf2', 'g4', 'Rf4', 'Rg8', 'Re4', 'g5', 'Re1+', 'Kg2', 'Re2+', 'Kg1', 'Re1+', 'Kf2', 'Re5', 'f6+', 'Kd7', 'Rg7', 'Ke8', 'Kg1', 'Kf8', 'Kf1', 'Re6', 'Rh7', 'Kg8', 'Rg7+', 'Kf8', 'Kf2', 'Rd6', 'Kg1', 'Rd1+', 'Kg2', 'Rd2+', 'Kg1', 'Rd1+', 'Kf2', 'Rh1', 'Rh7', 'Kg8', 'Rg7+', 'Kf8', 'Kg2', 'Rd1', 'h3', 'Rd3', 'Kh2', 'Rd2+', 'Kh1', 'Rf2', 'Kg1', 'Rd2', 'h4', 'Rd4', 'h5', 'Rg4+', 'Kf1', 'Rf4+', 'Kg2', 'Rg4+', 'Kh3', 'Re4', 'h6', 'Re6', 'h7', 'Re3+', 'Kg2', 'Ke8', 'h8=Q+', 'Kd7', 'Rxf7+', 'Kc6', 'Qc8+', 'Kd5', 'Rd7+', 'Ke5', 'f7', 'Rb3', 'Qc5+', 'Ke4', 'Rd4+', 'Ke3', 'Qe5#']
v0.34 Average Time: 2.4867368421052634, Total Time: 236.24
v0.40 Average Time: 0.9980851063829779, Total Time: 93.8199999999999

Game 3: v0.40 (WHITE) vs v0.34 (BLACK) : 0-1
['e4', 'e6', 'd4', 'd5', 'Nd2', 'c5', 'exd5', 'Qxd5', 'Ngf3', 'cxd4', 'Bc4', 'Qd8', 'O-O', 'a6', 'Nb3', 'Qc7', 'Bd3', 'Ne7', 'Nfxd4', 'e5', 'Ne2', 'Nbc6', 'Nc3', 'Nb4', 'Be3', 'Nf5', 'Be4', 'Nxe3', 'fxe3', 'Be6', 'a3', 'Nc6', 'Qd3', 'Bd6', 'Bxc6+', 'Qxc6', 'Na5', 'Qb6', 'Nxb7', 'Bc7', 'Qe4', 'Rb8', 'Qa4+', 'Ke7', 'Qh4+', 'Ke8', 'Qa4+', 'Ke7', 'Qe4', 'Qxb7', 'b4', 'Kf8', 'Qxb7', 'Rxb7', 'Ne4', 'Bb6', 'Rae1', 'Rc7', 'Rf2', 'Kg8', 'Rd2', 'Rc4', 'Rd6', 'Bc7', 'Rxa6', 'h6', 'Nc5', 'Rxc2', 'Nxe6', 'fxe6', 'Rxe6', 'Kf7', 'Ra6', 'Rb8', 'e4', 'Bb6+', 'Kh1', 'Kg8', 'b5', 'Bf2', 'Rf1', 'Re2', 'b6', 'Bxb6', 'g3', 'Bd4', 'h4', 'Rbb2', 'Ra8+', 'Kh7', 'Rf2', 'Rxf2', 'Rh8+', 'Kxh8', 'Kg1', 'Rb1#']
v0.34 Average Time: 8.04625, Total Time: 321.85
v0.40 Average Time: 3.7476923076923083, Total Time: 146.16000000000003

Game 4: v0.34 (WHITE) vs v0.40 (BLACK): 1-0
['Nf3', 'c5', 'g3', 'g6', 'Bg2', 'Bg7', 'O-O', 'Nc6', 'd3', 'e6', 'e4', 'Nge7', 'Nbd2', 'O-O', 'c3', 'd6', 'Qb3', 'b6', 'Nc4', 'd5', 'Ne3', 'Bb7', 'Bd2', 'Qd6', 'Rfe1', 'Ne5', 'Nxe5', 'Bxe5', 'exd5', 'exd5', 'c4', 'Rfd8', 'cxd5', 'Qb8', 'Bc3', 'Bxc3', 'bxc3', 'Qd6', 'c4', 'Nf5', 'Nxf5', 'gxf5', 'Rad1', 'Re8', 'Rxe8+', 'Rxe8', 'Qa4', 'Ra8', 'Re1', 'Qd8', 'Rd1', 'Qd6', 'h3', 'a6', 'Qb3', 'h6', 'a4', 'a5', 'Rb1', 'Ra6', 'Re1', 'Ra8', 'Rd1', 'Ra7', 'Rb1', 'Ra6', 'Rb2', 'Qf6', 'Qc2', 'Ra8', 'Qb3', 'Ra6', 'Qb5', 'Qd6', 'Re2', 'Ra8', 'Rb2', 'Ra6', 'Qe8+', 'Kg7', 'Re2', 'Ra8', 'Qe7', 'Qxe7', 'Rxe7', 'Rb8', 'Rd7', 'Bc8', 'Rd8', 'Kf6', 'd6', 'Rb7', 'Rxc8', 'Rd7', 'Rc6', 'Rb7', 'Rxc5', 'bxc5', 'Bxb7', 'Ke6', 'Bd5+', 'Kxd6', 'Bxf7', 'Ke5', 'Bg6', 'Kf6', 'Be8', 'Ke7', 'Bc6', 'Kf7', 'Bd5+', 'Kg7', 'Be6', 'Kf6', 'Bd5', 'Kg7', 'Bc6', 'Kf7', 'Bd7', 'Kf6', 'h4', 'Kg6', 'h5+', 'Kg5', 'Be8', 'Kf6', 'Bc6', 'Ke6', 'Bg2', 'Kf7', 'Bh3', 'Ke6', 'Kh2', 'Ke5', 'Bg2', 'Ke6', 'Kh1', 'Kf6', 'Kg1', 'Kg5', 'Bf3', 'Kf6', 'Bb7', 'Kg5', 'Bc8', 'Kg4', 'Be6', 'Kg5', 'Bf7', 'Kf6', 'Bd5', 'Kg7', 'Be6', 'Kf6', 'Bd7', 'Kg5', 'Be6', 'Kf6', 'Bc8', 'Kg5', 'Bd7', 'Kg4', 'Be8', 'Kf3', 'Bg6', 'Kg4', 'Bf7', 'Kg5', 'Kh2', 'Kf6', 'Bg6', 'Ke6', 'Kg2', 'Kf6', 'Kh1', 'Ke6', 'Kh2', 'Kf6', 'Kg2', 'Ke6', 'Kh1', 'Kf6', 'Kg1', 'Ke6', 'Bh7', 'Kf6', 'Kh2', 'Ke6', 'Kg2', 'Ke5', 'Bg6', 'Kf6', 'Kf3', 'Kg5', 'Ke2', 'Kf6', 'Kf1', 'Ke6', 'Kg1', 'Kf6', 'Be8', 'Kg5', 'f4+', 'Kg4', 'Kh2', 'Kf3', 'Bg6', 'Kg4', 'Bf7', 'Kf3', 'Be6', 'Kg4', 'Bd7', 'Kxh5', 'd4', 'Kg6', 'dxc5', 'Kh5', 'c6', 'Kg6', 'c7', 'Kh5', 'c8=Q', 'Kg4', 'Bc6', 'h5', 'Qg8#']
v0.34 Average Time: 2.6707476635514023, Total Time: 285.77000000000004
v0.40 Average Time: 0.9517142857142866, Total Time: 99.93000000000009

'''

'''original fen test: r1bqkbnr/pppp1ppp/8/4p3/2BnP3/5N2/PPPP1PPP/RNBQK2R
   second fen test: 1q1r1rk1/pb2bppp/1pn1pn2/8/3P4/P1N1BN2/1P2QPPP/1B1R1RK1
   third fen test: r3kb1r/pppb1ppp/2n1p3/qB6/3P4/1QP1PN2/P4PPP/R1B1K2R
   fourth fen test: r1b1k2r/ppppnppp/2n3q1/1Bb3B1/3pP3/2P2N2/PP3PPP/RN1Q1RK1
   problematic fen: 3r4/1r1PR3/3R2kp/pp3p2/7P/P7/BpP2P2/6K1 (black to move = Kh5)
   endgame draw fen test: 7r/8/2p2k2/5pp1/3P1n2/P1P2N2/1P2KPPP/1R6 (original move white = Kf1 draws the game)
   endgame draw fen test 2: r7/8/2p2k2/5pp1/3P4/P1Pn1N2/1P3PPP/1R3K2
   problematic fen 2: r1b1k2r/1ppp1p1p/3b4/8/2P3B1/P3P3/P2N1PPP/qQKR3R
   endgame 2 fen: 8/5p2/1p1k1n2/3P2pp/Rpr5/P6P/5PPK/3B4 (Bb3 is best move)
   checkmate prevention fen (black to move): 8/2R2pk1/1r3p1p/4p3/3pP1Q1/3q3P/5PP1/6K1
   mate in 10 fen (white to move): 5k2/2R2p2/1r3p1p/4p3/3pP1Q1/3q3P/5PP1/6K1
   KQ endgame fen: 4k3/4P3/4K3/8/8/8/8/8
   complex position fen: 2r3k1/1pr1q1p1/7p/p2n1p2/PnBP4/4B2P/1P2QPP1/R1R3K1
   complex position 2 fen: r1b1kb1r/2p1np1p/p1p2qp1/1B6/3P4/2N5/PP2QPPP/R1B1K2R 
   blunder position fen: 2bq2k1/6bp/r2p2p1/1pQP4/p3P3/3P4/PP3KBP/1R2R3
   blunder 2 position fen: r3k2r/1p3ppp/pq1bb3/N3p3/8/P1NQP3/1PP3PP/R4RK1
   london system fen: r1q1k2r/pp2bppp/2n1pn2/2pp1b2/3P1B2/1QP1PN2/PP1NBPPP/R3K2R
   blunder 3 position fen (black to play): r2r2k1/pb2np1p/1p1q2p1/2pPb3/8/1Q1PN1P1/PP1B1PBP/R3R1K1
   blunder 4 position fen (white to play): r1bqr1k1/1pp3b1/3p2pp/2nP1p2/2P1P3/p1N1BP2/PP2BQPP/R3R1K1
   john vs bluebot blunder fen 1 (black to play): r3kb1r/pp3ppp/1qn1pn2/3p4/3P1B1N/2PpP3/PP1N1PPP/R1Q1K2R
   positional fen 1: r3kb1r/pp3ppp/1qn1pn2/3p1b2/2pP1B1N/2P1P3/PP3PPP/RNQ1KB1R 
   positional fen 2: r3kb1r/pp3ppp/1qn1pn2/3p4/3P1B1N/2PpP3/PP3PPP/RNQ1K2R
   endgame fen: 6k1/p4ppp/pr3b2/3p4/2rN4/2P1P1P1/PP1R1PP1/3R1K2
   king safety fen: r1bq1rk1/1p1nppbp/2p3p1/2p5/3PP3/p1N1BN1P/PPPQ1PP1/2KR3R
   king safety 2: r1b2rk1/1p1nppbp/2p3p1/q1P5/4P3/2N1BN1P/PKPQ1PP1/3R3R
   king safety 3: r1bq1rk1/1p1nppbp/2p3p1/2p5/p3P3/2NPBN1P/PPPQ1PP1/2KR3R
   knight sacrifice blunder: rn1q1b1r/1bp2kpp/pp2p3/8/3P4/2B5/PP2PPPP/R2QKB1R
   knight sacrifice blunder 2: rn1qkb1r/1bp2ppp/pp2p3/4N3/3P4/2B5/PP2PPPP/R2QKB1R
   endgame fen 2: 8/8/8/2P1k3/1P4P1/P2Bp1KP/2R2r2/5n2'''
