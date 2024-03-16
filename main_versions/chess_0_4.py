import chess.svg
import pygame
import cairosvg
import io
import math
import time


KING = [[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
        [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]]

QUEEN = [[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
         [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
         [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
         [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
         [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
         [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
         [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
         [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]

ROOK = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]]

BISHOP = [[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
          [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
          [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
          [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
          [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
          [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
          [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
          [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]

KNIGHT = [[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
          [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
          [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
          [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
          [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
          [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
          [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
          [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]

PAWN = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
        [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
        [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
        [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
        [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]


def evaluate(board, colour):
    print(board)
    Eval = 0
    for row in range(8):
        for col in range(8):
            square = row * 8 + col
            piece = board.piece_at(square)
            if piece is not None:
                mult = 1 if piece.color == colour else -1
                if colour:
                    row = 7 - row
                else:
                    col = 7 - col
                match piece.piece_type:
                    case chess.KING:
                        Eval += mult * (900 + KING[row][col])
                    case chess.QUEEN:
                        # print(chess.square_name(chess.square(col, row)), mult)
                        Eval += mult * (90 + QUEEN[row][col])
                    case chess.ROOK:
                        Eval += mult * (50 + ROOK[row][col])
                    case chess.BISHOP:
                        Eval += mult * (30 + BISHOP[row][col])
                    case chess.KNIGHT:
                        Eval += mult * (30 + KNIGHT[row][col])
                    case chess.PAWN:
                        Eval += mult * (10 + PAWN[row][col])

    return Eval


def child_of_pos(board):
    for move in list(board.legal_moves):
        new_board = board.copy()
        new_board.push(move)
        yield new_board


def get_player_index(player):
    return 0 if player else 1


def minimax(pos, depth, alpha, beta, maxingPlayer, colour):
    global positions

    positions += 1

    # if chess.Move(chess.F6, chess.G4) in pos.move_stack:
    #     print(pos, evaluate(pos, colour))

    if depth == 0 or pos.is_checkmate() or pos.is_stalemate():  # no more valid moves or reached set depth
        if pos.is_checkmate():
            # print(pos, -1 * math.inf if maxingPlayer else math.inf)
            if maxingPlayer:
                return -1 * math.inf
            else:
                return math.inf
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
        print(board.san(moves[i]), val)
        if val >= bestMove:
            bestMove = val
            bestMoveFound = moves[i]
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


def main():  # Main Loop
    board = chess.Board()

    pygame.init()
    pygame.display.set_caption("Chess")
    display = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    move_list = []
    player = chess.WHITE
    gameOver = False

    nb = chess.Board()
    nb.push_san("e4")
    nb.push_san("e5")
    nb.push_san("Qg4")
    nb.push_san("Nf6")
    nb.push_san("d3")
    nb.push_san("Nxg4")
    print(evaluate(nb, True), evaluate(nb, False))

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
            if board.turn == player:  # Player's turn
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
            else:  # Computer's turn
                move = minimax_root(3, board, True, board.turn)
                print(board.san(move))
                board.push(move)

        # Render board
        img = pygame.transform.scale(get_img(board, None if not move_list else move_list[0], player), (800, 800))
        display.blit(img, (0, 0))
        pygame.display.flip()

        if not gameOver:  # game is not over
            if board.is_checkmate():  # Checkmate
                print(title := f"{'White' if player else 'Black'} won the game by checkmate!")
                pygame.display.set_caption(f"Chess: {title}")
                gameOver = True

            if board.is_stalemate():  # Stalemate
                print(title := "Draw by stalemate")
                pygame.display.set_caption(f"Chess: {title}")
                gameOver = True


if __name__ in "__main__":  # Run the game
    main()
