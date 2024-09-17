import chess.svg
from chessboard import display


def main():

    board = chess.Board()

    current_player = "White"

    gameboard = display.start()

    while True:
        display.check_for_quit()
        display.update(board.fen(), gameboard)
        current_player = "Black" if current_player == "White" else "White"
        nextmove = input(f"{current_player}'s  Next Move: ")



if __name__ in "__main__":
    main()
