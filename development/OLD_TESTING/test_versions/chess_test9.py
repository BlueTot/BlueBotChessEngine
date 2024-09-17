import chess.svg
import chess.polyglot
import pygame
import cairosvg
import io
import time
import copy

INF = 99999
NEG_INF = -99999
times = []


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


EVALS = {"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1": 0.0}

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


def check_endgame(board):
    queens, minors = 0, 0
    for square in range(64):
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.QUEEN:
            queens += 1
        if piece and piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
            minors += 1
    return queens == 0 or (queens == 2 and minors <= 1)


def piece_value(piece, mult, square):
    row = square // 8
    col = square % 8
    match piece.piece_type:
        case chess.KING:
            return mult * (900 + (KING if piece.color else R_KING)[row][col])
        case chess.QUEEN:
            return mult * (90 + (QUEEN if piece.color else R_QUEEN)[row][col])
        case chess.ROOK:
            return mult * (50 + (ROOK if piece.color else R_ROOK)[row][col])
        case chess.BISHOP:
            return mult * (30 + (BISHOP if piece.color else R_BISHOP)[row][col])
        case chess.KNIGHT:
            return mult * (30 + (KNIGHT if piece.color else R_KNIGHT)[row][col])
        case chess.PAWN:
            return mult * (10 + (PAWN if piece.color else R_PAWN)[row][col])


def evaluate(board, depth=3):
    global EVALS

    if board.is_checkmate():
        return NEG_INF + (3 - depth)
    if board.is_stalemate() or board.can_claim_draw() or board.is_insufficient_material():
        return 0

    prev_board = board.copy()
    prev_board.pop()

    Eval = EVALS[prev_board.fen()] if prev_board.fen() in EVALS else evaluate(prev_board)
    move = list(board.move_stack)[-1]
    piece = prev_board.piece_at(move.from_square)
    mult = 1 if piece.color else -1

    Eval -= piece_value(piece, mult, move.from_square)
    Eval += piece_value(piece, mult, move.to_square)
    if prev_board.is_capture(move):  # is capture
        capture_piece = prev_board.piece_at(move.to_square)
        Eval -= piece_value(capture_piece, mult, move.to_square)

    EVALS[board.fen()] = Eval
    return Eval


def sort_moves(board):
    moves = {}
    for move in list(board.legal_moves):
        board.push(move)
        moves[move] = evaluate(board)
        board.pop()
    sorted_dict = sorted(moves.items(), key=lambda x: x[1])
    return [i[0] for i in sorted_dict]


def quiescence(board, alpha, beta, depth):
    global positions, times

    stime = time.perf_counter_ns()
    pos_eval = evaluate(board, depth) * (1 if board.turn else -1)
    times.append(time.perf_counter_ns() - stime)

    if pos_eval >= beta:
        return beta

    if alpha < pos_eval:
        alpha = pos_eval

    if depth == 0:
        return alpha

    for move in list(board.generate_legal_captures()):
        positions += 1
        board.push(move)
        score = -quiescence(board, -beta, -alpha, depth - 1)
        board.pop()

        if score >= beta:
            return beta

        if alpha > score:
            alpha = score

    return alpha


def negamax(depth, board, alpha, beta):
    global positions

    if board.is_stalemate() or board.can_claim_draw():
        return 0

    if depth == 0:
        return quiescence(board, alpha, beta, depth + 3)

    for move in list(board.legal_moves):
        positions += 1
        board.push(move)
        score = -negamax(depth - 1, board, -beta, -alpha)
        board.pop()
        alpha = max(score, alpha)
        if alpha >= beta:
            break

    return alpha


def root_search(board, depth):
    global positions, times

    positions = 0
    startTime = time.perf_counter()

    if board.is_checkmate():
        return NEG_INF
    if board.is_stalemate() or board.can_claim_draw():
        return 0

    try:

        return chess.polyglot.MemoryMappedReader("../Titans.bin").weighted_choice(board).move

    except IndexError:

        alpha = NEG_INF
        beta = INF
        bestMoveFound = None

        for move in list(board.legal_moves):
            if "#" in board.san(move):  # checks for mate in one
                return move

        for move in list(sort_moves(board)):
            positions += 1
            board.push(move)
            score = -negamax(depth - 1, board, -beta, -alpha)
            is_repetition = board.is_repetition(2)
            board.pop()

            # code to prevent bot from repeating moves if it is winning
            if evaluate(board) > 0 and is_repetition:
                continue

            print(board.san(move), score)

            if score > alpha:
                alpha = score
                bestMoveFound = move

            if alpha >= beta:
                break

        print(f"moves checked: {positions}")
        print("time taken: ", time_taken := time.perf_counter() - startTime)
        print(f"moves per second: {positions / time_taken}")
        avg_time = sum(times)/len(times) / 1.0e9
        percent_time = avg_time / time_taken * 100
        print(f"average time: {avg_time}s")
        print(f"percent time: {percent_time}%")

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
    move = root_search(board, 3)
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

            if board.can_claim_draw():
                print(title := "Draw by threefold repetition")
                pygame.display.set_caption(f"Chess: {title}")
                gameOver = True

            if board.is_insufficient_material():
                print(title := "Draw by insufficient material")
                pygame.display.set_caption(f"Chess: {title}")
                gameOver = True

        # print(board.fen())


if __name__ in "__main__":  # Run the game
    main()
