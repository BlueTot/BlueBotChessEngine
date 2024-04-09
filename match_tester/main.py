import chess
import chess_022, chess_029, chess_030, chess_031, chess_032, chess_033, chess_034


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

class Chess030:
    depth = 6
    name = f"Chess v0.30 (depth {depth})"
    tag = (chess_030.get_best_move, depth)

class Chess031:
    depth = 6
    name = f"Chess v0.31 (depth {depth})"
    tag = (chess_031.get_best_move, depth)

class Chess032:
    depth = 6
    name = f"Chess v0.32 (depth {depth})"
    tag = (chess_032.get_best_move, depth)

class Chess033:
    depth = 6
    name = f"Chess v0.33 (depth {depth})"
    tag = (chess_033.get_best_move, depth)

class Chess034:
    depth = 6
    name = f"Chess v0.34 (depth {depth})"
    tag = (chess_034.get_best_move, depth)


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
        san = input("BLACK make a move: ")
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
    bot = True
    bot_perspective = True
    version = Chess034
    game = ChessGame(player1=version() if bot else Player(),
                     player2=Player() if bot else version())
    game.play()

'''original fen test: r1bqkbnr/pppp1ppp/8/4p3/2BnP3/5N2/PPPP1PPP/RNBQK2R
   second fen test: 1q1r1rk1/pb2bppp/1pn1pn2/8/3P4/P1N1BN2/1P2QPPP/1B1R1RK1
   third fen test: r3kb1r/pppb1ppp/2n1p3/qB6/3P4/1QP1PN2/P4PPP/R1B1K2R
   fourth fen test: r1b1k2r/ppppnppp/2n3q1/1Bb3B1/3pP3/2P2N2/PP3PPP/RN1Q1RK1
   problematic fen: 3r4/1r1PR3/3R2kp/pp3p2/7P/P7/BpP2P2/6K1 (black to move = Kh5)
   endgame draw fen test: 7r/8/2p2k2/5pp1/3P1n2/P1P2N2/1P2KPPP/1R6 (original move white = Kf1 draws the game)
   endgame draw fen test 2: r7/8/2p2k2/5pp1/3P4/P1Pn1N2/1P3PPP/1R3K2
   problematic fen 2: r1b1k2r/1ppp1p1p/3b4/8/2P3B1/P3P3/P2N1PPP/qQKR3R'''