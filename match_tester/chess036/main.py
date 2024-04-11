import chess
import chess_036


class Player:
    name = "player"
    tag = 1

class Chess036:
    depth = 6
    name = f"Chess v0.36 (depth {depth})"
    tag = (chess_036.get_best_move, depth)

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
    version = Chess036
    game = ChessGame(player1=version() if bot else Player(),
                     player2=Player() if bot else version())
    game.play()
