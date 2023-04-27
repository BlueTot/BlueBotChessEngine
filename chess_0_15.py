import chess.polyglot
import chess.svg
import pygame
import cairosvg
import io
import math
import time
import copy


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


def evaluate(board):
    Eval = 0

    if board.is_checkmate():
        return -1 * math.inf
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
                        Eval += mult * (90 + (QUEEN if piece.color else R_QUEEN)[row][col])
                    case chess.ROOK:
                        Eval += mult * (50 + (ROOK if piece.color else R_ROOK)[row][col])
                    case chess.BISHOP:
                        Eval += mult * (30 + (BISHOP if piece.color else R_BISHOP)[row][col])
                    case chess.KNIGHT:
                        Eval += mult * (30 + (KNIGHT if piece.color else R_KNIGHT)[row][col])
                    case chess.PAWN:
                        Eval += mult * (10 + (PAWN if piece.color else R_PAWN)[row][col])

    return Eval if board.turn else -1 * Eval


def sort_moves(board, lst):
    moves = {}
    for move in lst:
        board.push(move)
        moves[move] = evaluate(board)
        board.pop()
    sorted_dict = sorted(moves.items(), key=lambda x: x[1])
    return [i[0] for i in sorted_dict]


def quiescence(board, alpha, beta, depth):
    global positions

    stand_pat = evaluate(board)

    if stand_pat >= beta:
        return beta

    if alpha < stand_pat:
        alpha = stand_pat

    if depth == 0:
        return alpha

    for move in sort_moves(board, list(board.generate_legal_captures())):
        positions += 1
        board.push(move)
        score = -quiescence(board, -beta, -alpha, depth-1)
        board.pop()

        if score >= beta:
            return beta

        if alpha > score:
            alpha = score

    return alpha


def negamax(depth, board, alpha, beta):
    global positions

    if depth == 0 or board.is_game_over() or board.can_claim_draw():
        return quiescence(board, alpha, beta, 3)

    for move in sort_moves(board, list(board.legal_moves)):
        positions += 1
        board.push(move)
        score = -negamax(depth - 1, board, -beta, -alpha)
        board.pop()
        alpha = max(alpha, score)
        if alpha >= beta:
            break

    return alpha


def root(board, depth):
    global positions

    try:
        return chess.polyglot.MemoryMappedReader("../Titans.bin").weighted_choice(board).move

    except IndexError:

        stime = time.perf_counter()

        alpha = -1 * math.inf
        beta = math.inf
        bestMoveFound = None
        positions = 0

        for move in list(board.legal_moves):
            if "#" in board.san(move):  # checks for mate in one
                return move

        for move in sort_moves(board, list(board.legal_moves)):
            positions += 1
            board.push(move)
            score = -negamax(depth - 1, board, -beta, -alpha)
            is_repetition = board.is_repetition(2)
            board.pop()

            if evaluate(board) > 0 and is_repetition:
                continue

            print(board.san(move), score)
            if score > alpha:
                alpha = score
                bestMoveFound = move

            if alpha >= beta:
                break

        print(f"nodes: {positions}")
        print("time taken: ", time_taken := time.perf_counter() - stime)
        print(f"nodes per second: {positions / time_taken}")

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
                move = chess.Move(from_square=move_list[0], to_square=move_list[1], promotion=chess.QUEEN)
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
    move = root(board, 4)
    if move is None:
        move = list(board.legal_moves)[-1]
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
    player = chess.BLACK
    mode = Modes.COMPUTER_ONLY
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
            if mode == Modes.PLAYER_ONLY:
                board, player, move_list = player_make_move(board, player, move_list)
            elif mode == Modes.PLAYER_VS_COMPUTER:
                if board.turn == player:
                    board, player, move_list = player_make_move(board, player, move_list)
                else:  # Computer's turn
                    board = computer_make_move(board)
            elif mode == Modes.COMPUTER_ONLY:  # Computer vs computer
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

            if board.can_claim_draw():
                print(title := "Draw by threefold repetition")
                pygame.display.set_caption(f"Chess: {title}")
                gameOver = True

            if board.is_insufficient_material():
                print(title := "Draw by insufficient material")
                pygame.display.set_caption(f"Chess: {title}")
                gameOver = True


if __name__ in "__main__":  # Run the game
    main()
