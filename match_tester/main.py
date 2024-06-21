import chess
import chess_022, chess_029, chess_034, chess_035, chess_036, chess_037, chess_038, chess_039, chess_040, chess_041, chess_042, chess_043, chess_044, chess_045, chess_046, chess_047, chess_048, chess_049, chess_050, chess_051, chess_052, chess_053, chess_054, chess_055, chess_056, chess_057, chess_058, chess_059, chess_060, chess_061


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
    depth = 8
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
    depth = 6
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

class Chess049:
    depth = 6
    name = f"Chess v0.49 (depth {depth})"
    tag = (chess_049.get_best_move, depth)

class Chess050:
    depth = 6
    name = f"Chess v0.50 (depth {depth})"
    tag = (chess_050.get_best_move, depth)

class Chess051:
    depth = 6
    name = f"Chess v0.51 (depth {depth})"
    tag = (chess_051.get_best_move, depth)

class Chess052:
    depth = 6
    name = f"Chess v0.52 (depth {depth})"
    tag = (chess_052.get_best_move, depth)

class Chess053:
    depth = 6
    name = f"Chess v0.53 (depth {depth})"
    tag = (chess_053.get_best_move, depth)

class Chess054:
    depth = 6
    name = f"Chess v0.54 (depth {depth})"
    tag = (chess_054.get_best_move, depth)

class Chess055:
    depth = 6
    name = f"Chess v0.55 (depth {depth})"
    tag = (chess_055.get_best_move, depth)

class Chess056:
    depth = 7
    name = f"Chess v0.56 (depth {depth})"
    tag = (chess_056.get_best_move, depth)

class Chess057:
    depth = 7
    name = f"Chess v0.57 (depth {depth})"
    tag = (chess_057.get_best_move, depth)

class Chess058:
    depth = 6
    name = f"Chess v0.58 (depth {depth})"
    tag = (chess_058.get_best_move, depth)

class Chess059:
    depth = 8
    name = f"Chess v0.59 (depth {depth})"
    tag = (chess_059.get_best_move, depth)

class Chess060:
    depth = 8
    name = f"Chess v0.60 (depth {depth})"
    tag = (chess_060.get_best_move, depth)

class Chess061:
    depth = 8
    name = f"Chess v0.61 (depth {depth})"
    tag = (chess_061.get_best_move, depth)

class ChessGame:
    def __init__(self, player1, player2, fen=None, castling_fen=None, turn=chess.WHITE):

        self.__board = chess.Board()
        if fen is not None:
            self.__board.set_board_fen(fen)
        if castling_fen is not None:
            self.__board.set_castling_fen(castling_fen)
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
    version = Chess060
    game = ChessGame(player1=version() if bot else Player(),
                     player2=Player() if bot else version(),
                     fen="2R5/p2r2pk/1b3p2/2N2P1p/1p4nB/1P6/1P6/R2r1NK1")
    game.play()

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
   Qb8 blunder fen (black to play): r2r2k1/pb2np1p/1p1q2p1/2pPb3/8/1Q1PN1P1/PP1B1PBP/R3R1K1
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
   endgame fen 2: 8/8/8/2P1k3/1P4P1/P2Bp1KP/2R2r2/5n2
   Mistake fen: r1k2b1r/pp1n1ppp/2p2n2/1Nqp4/8/P4PB1/1P2QPPP/1K2RB1R
   Bf8 fen: r1k4r/pp1n1ppp/2p2n2/2bp4/3q4/P1N2PB1/1PQ2PPP/1K2RB1R
   Bc5 fen: r1k2b1r/ppBn1ppp/2p2n2/3p4/3q4/P1N2P2/1PQ2PPP/1K2RB1R
   Qc3 fen: r1b1kb1r/3n1ppp/pqn1p3/2ppP3/3P1P2/4BN2/1PPQN1PP/R3KB1R w Kkq - 2 14
   Kh7 fen: r2r2k1/pp2np2/3pb2p/1P2q3/1QPRp1pN/P3P1P1/4BPP1/2R3K1
   Qxg6 blunder fen: 1k1r3r/pp4b1/2np2p1/2q5/4Q3/7P/PPPN2B1/R1B1K2R
   f6 mistake fen: r1b1kbnr/pp1n1ppp/1q2p3/3pP3/3P4/2PB1N2/5PPP/RNBQK2R
   f4 blunder fen: rr4k1/5pp1/3pqn1p/2p1p3/p1P1P3/2QPBP1P/PP3P2/1R2R1K1
   Qd2 mistake fen: r3k2r/pb1n4/2pPpq2/1p1n1p2/2pP2p1/P1N3B1/1PQ1BPP1/R4RK1 w kq - 0 20
   a4 fen: 2rqkb1r/3n1ppp/bp2pn2/1Npp4/3P1B2/4PNP1/PPP2PBP/R2Q1RK1 w k - 1 12
   hxg5 blunder fen: r2q1rk1/1p2bpp1/p2pbn1p/4p1P1/4P2P/1PN1BP2/PP1QB3/2KR3R b - - 0 15
   Rdf8 blunder fen: r4rk1/p1p1qp1p/2p5/3p4/8/2P2P2/PP1Q1P1R/2KR4 b - - 0 19
   Qd6 blunder fen: r2q1rk1/bbp2pp1/p1n2n1p/1p2p3/4P1PB/1BP2N1P/PP2QP2/R3KN1R b KQ - 1 14
   Bc6 best move fen: 1r1qkbr1/1B3p2/p3p2p/1p6/2pB4/P7/1PP2PPP/R2QR1K1 w - - 1 19
   Qb5 best move fen: 1r3rk1/pp2nppp/2n1p3/q2pPb2/2P5/1Q2BN2/PP2BPPP/R4RK1 w - - 1 15
   Rg5 blunder fen: RN6/4kp2/4p1p1/2b1P2p/2r2n2/3b1NRP/5PP1/6K1 w - - 9 54
   Re1 mistake fen: 2r1kb2/5p2/4p1p1/4P2p/3N3R/2nb1N2/5PPP/R5K1 w - - 6 45
   gxh3 blunder fen: 8/4kp2/N3p1p1/R1b1P1Rp/2r5/5b1n/5PP1/6K1 w - - 0 57
   N2f3 mistake fen: 2r1k3/5p2/4p1p1/4P2p/1b1N3R/2nb4/3N1PPP/2R3K1 w - - 2 43
   Be6 blunder fen: 8/8/P4k2/3B1Ppp/2Pb1p2/5P2/P3R1KP/2r5 w - - 1 58
   Rxd1 blunder fen: 2R5/p2r2pk/1b3p2/2N2P1p/1p4nB/1P6/1P6/R2r1NK1'''
