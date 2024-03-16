import chess.svg
import pygame
import cairosvg
import io
import math
import time
import copy
import random


class Modes:
    PLAYER_VS_COMPUTER = 0
    COMPUTER_ONLY = 1
    PLAYER_ONLY = 2


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
          [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
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


class Moves:
    e4 = chess.Move.from_uci("e2e4")
    e5 = chess.Move.from_uci("e7e5")
    e6 = chess.Move.from_uci("e7e6")
    d3 = chess.Move.from_uci("d2d3")
    d4 = chess.Move.from_uci("d2d4")
    d5 = chess.Move.from_uci("d7d5")
    d6 = chess.Move.from_uci("d7d6")
    c4 = chess.Move.from_uci("c2c4")
    c5 = chess.Move.from_uci("c7c5")

    Nc3 = chess.Move.from_uci("b1c3")
    Nf3 = chess.Move.from_uci("g1f3")
    Nc6 = chess.Move.from_uci("b8c6")
    Nf6 = chess.Move.from_uci("g8f6")
    O_O = chess.Move.from_uci("e1g1")

    exd5 = chess.Move.from_uci("e4d5")

    Bc4 = chess.Move.from_uci("f1c4")
    Bc5 = chess.Move.from_uci("f8c5")
    Bb5 = chess.Move.from_uci("f1b5")
    Bf4 = chess.Move.from_uci("c1f4")


WHITE_OPENINGS = {
    (): (Moves.e4, Moves.d4),
    (Moves.e4, Moves.e5): Moves.Nf3,
    (Moves.e4, Moves.e5, Moves.Nf3, Moves.Nc6): (Moves.Bc4, Moves.Bb5),
    (Moves.e4, Moves.e5, Moves.Nf3, Moves.Nc6, Moves.Bc4, Moves.Bc5): Moves.d3,
    (Moves.e4, Moves.e5, Moves.Nf3, Moves.Nc6, Moves.Bc4, Moves.Nf6): Moves.d3,
    (Moves.e4, Moves.e5, Moves.Nf3, Moves.Nc6, Moves.Bb5, Moves.Nf6): Moves.O_O,
    (Moves.e4, Moves.c5): (Moves.Nf3, Moves.Nc3),
    (Moves.d4, Moves.d5): (Moves.Nf3, Moves.Bf4, Moves.c4),
    (Moves.d4, Moves.Nf6): (Moves.Nf3, Moves.Bf4, Moves.c4),
    (Moves.d4, Moves.d5, Moves.Nf3, Moves.Nf6): Moves.Bf4,
    (Moves.e4, Moves.d5): Moves.exd5,
}

BLACK_OPENINGS = {
    Moves.e4: (Moves.e5, Moves.d5, Moves.c5),  # response to e4 (king's pawn opening)
    (Moves.e4, Moves.e5, Moves.Nf3): Moves.Nc6,  # response to e4 e5 Nf3
    (Moves.e4, Moves.e5, Moves.Nf3, Moves.Nc6, Moves.Bc4): Moves.Bc5,  # response to e4 e5 Nf3 Nc6 Bc4 (italian game)
    (Moves.e4, Moves.e5, Moves.Nf3, Moves.Nc6, Moves.Bb5): Moves.Nf6,  # response to e4 e5 Nf3 Nc6 Bb5 (ruy lopez)
    (Moves.e4, Moves.d5, Moves.exd5): Moves.Nf6,  # response to e4 d5 exd5 (scandinavian defence)
    (Moves.c5, Moves.Nf3): Moves.Nc6,  # response to c5 Nf3 (open sicilian)
    (Moves.c5, Moves.Nc3): Moves.d6,  # response to c5 Nc3 (closed sicilian)
    Moves.d4: Moves.d5,  # response to d4 (queen's pawn opening)
    (Moves.d4, Moves.d5, Moves.Nf3): Moves.Nf6,  # response to d4 d5 Nf3
    (Moves.d4, Moves.d5, Moves.Nf3, Moves.Nf6, Moves.Bf4): (Moves.e6, Moves.c5),
    # response to d4 d5 Nf3 Nf6 Bf4 (london system with d5 Nf6)
    (Moves.d4, Moves.d5, Moves.Bf4): (Moves.c5, Moves.Nf6),  # response to d4 d5 Bf4 (london system with d4 Bf4)
    (Moves.d4, Moves.d5, Moves.c4): Moves.e6,  # response to d4 d5 c4 (queen's gambit)
}


def evaluate(board, colour):
    Eval = 0

    for row in range(8):
        for col in range(8):

            square = row * 8 + col
            piece = board.piece_at(square)

            if piece is not None:

                mult = 1 if piece.color == colour else -1

                match piece.piece_type:
                    case chess.KING:
                        Eval += mult * (900 + (KING if piece.color else R_KING)[row][col])
                    case chess.QUEEN:
                        Eval += mult * (90 + (QUEEN if piece.color else R_QUEEN)[row][col])
                    case chess.ROOK:
                        Eval += mult * (50 + (ROOK if piece.color else R_ROOK)[row][col])
                    case chess.BISHOP:
                        Eval += mult * (30 + (BISHOP if piece.color else R_BISHOP)[row][col])
                    case chess.KNIGHT:
                        Eval += mult * (30 + (KNIGHT if piece.color else R_KNIGHT)[row][col])
                    case chess.PAWN:
                        Eval += mult * (10 + (PAWN if piece.color else R_PAWN)[row][col])

    return Eval


def child_of_pos(board):
    for move in list(board.legal_moves):
        new_board = board.copy()
        new_board.push(move)
        yield new_board


def get_player_index(player):
    return 0 if player else 1


def get_board_moves(board):
    lst = []
    for move in list(board.move_stack):
        lst.append(move)
    t = tuple(lst)
    if len(t) == 1:
        return t[0]
    return t


def minimax(pos, depth, alpha, beta, maxingPlayer, colour):
    global positions

    positions += 1

    if depth == 0 or pos.is_checkmate() or pos.is_stalemate():  # no more valid moves or reached set depth
        if pos.is_checkmate():
            # print(pos, maxingPlayer, -1 * math.inf if maxingPlayer else math.inf)
            if maxingPlayer:
                return -1 * math.inf
            else:
                return math.inf
        if pos.is_stalemate():
            return 0
        if pos.can_claim_threefold_repetition():
            return 0
        return evaluate(pos, colour)

    bestMove = [-1, 1][get_player_index(maxingPlayer)] * math.inf
    max_min = [max, min]
    for child in child_of_pos(pos):
        val = minimax(child, depth - 1, alpha, beta, not maxingPlayer, colour)
        bestMove = max_min[get_player_index(maxingPlayer)](bestMove, val)
        if maxingPlayer:
            alpha = max_min[get_player_index(maxingPlayer)](alpha, val)
        else:
            beta = max_min[get_player_index(maxingPlayer)](beta, val)
        if beta <= alpha:
            break
    return bestMove


def minimax_root(depth, board, maxingPlayer, colour):
    global positions

    moves = list(board.legal_moves)
    bestMove = -1 * math.inf
    bestMoveFound = None

    positions = 0
    start = time.perf_counter()

    i = 0
    for child in child_of_pos(board):
        val = minimax(child, depth - 1, -1 * math.inf, math.inf, not maxingPlayer, colour)

        if val >= bestMove:  # check if there is a better move
            bestMove = val
            bestMoveFound = moves[i]

        # print(board.san(moves[i]), val)

        if "#" in board.san(moves[i]):  # checks for mate in one
            bestMoveFound = moves[i]
            break

        # opening book
        if colour:
            if get_board_moves(board) in WHITE_OPENINGS.keys():
                if type(WHITE_OPENINGS[get_board_moves(board)]) == tuple:
                    bestMoveFound = random.choice(WHITE_OPENINGS[get_board_moves(board)])
                else:
                    bestMoveFound = WHITE_OPENINGS[get_board_moves(board)]
                break
        else:
            if get_board_moves(board) in BLACK_OPENINGS.keys():
                if type(BLACK_OPENINGS[get_board_moves(board)]) == tuple:
                    bestMoveFound = random.choice(BLACK_OPENINGS[get_board_moves(board)])
                else:
                    bestMoveFound = BLACK_OPENINGS[get_board_moves(board)]
                break

        i += 1

    print(f"positions / sec : {positions / (time.perf_counter() - start)}")

    return bestMoveFound


def get_img(board, selected_square, player):  # Get board pygame image to render
    if selected_square is not None:
        svg = chess.svg.board(board=board, flipped=True if player == chess.BLACK else False,
                              fill=dict.fromkeys(get_move_squares(board, selected_square), "#cc0000cc"))
    else:
        svg = chess.svg.board(board=board, flipped=True if player == chess.BLACK else False)

    png_io = io.BytesIO()
    cairosvg.svg2png(bytestring=bytes(svg, "utf8"), write_to=png_io)
    png_io.seek(0)

    surface = pygame.image.load(png_io, "png")
    return surface


def get_square(x, y, flipped):  # Get square number (0 - 63) from mouse coordinates
    file = (x - 30) // (740 // 8)
    rank = 8 - (y - 30) // (740 // 8) - 1
    if flipped:
        file = 7 - file
        rank = 7 - rank
    return file + rank * 8


def get_move_squares(board, square):  # Get legal moves for each piece on the board
    moves = []
    for move in list(board.legal_moves):
        move = str(move)
        start, dest = move[:2], move[2:4]
        if chess.square_name(square) == start:
            moves.append(chess.parse_square(dest))
    return moves


def player_make_move(board, player, move_list):
    if len(move_list) == 2:  # Player clicked twice
        try:
            promotion_squares = [i for i in range(8)] if player == chess.BLACK else [i for i in
                                                                                     range(56, 64)]
            if move_list[1] in promotion_squares and board.piece_at(
                    move_list[0]).piece_type == chess.PAWN:  # Promotion
                move = chess.Move(from_square=move_list[0], to_square=move_list[1],
                                  promotion=chess.QUEEN)
            else:  # Non-Promotion
                move = chess.Move(from_square=move_list[0], to_square=move_list[1])
            if move in board.legal_moves:  # Move is legal
                print(san := board.san(move))
                board.push_san(san)
            else:  # Illegal move
                raise chess.IllegalMoveError
        except chess.IllegalMoveError:
            pass
        except AttributeError:
            pass
        finally:
            move_list = []
    return board, player, move_list


def computer_make_move(board):
    move = minimax_root(3, board, True, board.turn)
    print(board.san(move))
    board.push(move)
    return board


def main():  # Main Loop
    board = chess.Board()

    pygame.init()
    pygame.display.set_caption("Chess")
    display = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    move_list = []
    player = chess.WHITE
    mode = Modes.PLAYER_VS_COMPUTER
    gameOver = False

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed(3)[0]:
                    if 30 <= x <= 800 - 30 and 30 <= y <= 800 - 30:
                        move_list.append(get_square(x, y, player == chess.BLACK))

        if not gameOver:  # If game is still ongoing
            if mode == Modes.PLAYER_ONLY:  # Player vs Player
                board, player, move_list = player_make_move(board, player, move_list)
            elif mode == Modes.PLAYER_VS_COMPUTER:
                if board.turn == player:  # Player's turn
                    board, player, move_list = player_make_move(board, player, move_list)
                else:  # Computer's turn
                    board = computer_make_move(board)
            else:  # Computer vs computer
                board = computer_make_move(board)

        # Render board
        img = pygame.transform.scale(get_img(board, None if not move_list else move_list[0], player), (800, 800))
        display.blit(img, (0, 0))
        pygame.display.flip()

        if not gameOver:  # game is not over
            if board.is_checkmate():  # Checkmate
                print(title := f"{'White' if not board.turn else 'Black'} won the game by checkmate!")
                pygame.display.set_caption(f"Chess: {title}")
                gameOver = True

            if board.is_stalemate():  # Stalemate
                print(title := "Draw by stalemate")
                pygame.display.set_caption(f"Chess: {title}")
                gameOver = True

            if board.can_claim_threefold_repetition():
                print(title := "Draw by threefold repetition")
                pygame.display.set_caption(f"Chess: {title}")
                gameOver = True


if __name__ in "__main__":  # Run the game
    main()
