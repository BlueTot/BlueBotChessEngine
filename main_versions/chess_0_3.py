import chess.svg
import pygame
import cairosvg
import io
import random


def get_img(board, selected_square, player):  # Get board pygame image to render
    if selected_square is not None:
        svg = chess.svg.board(board=board, flipped=True if player == chess.BLACK else False, fill=dict.fromkeys(get_move_squares(board, selected_square), "#cc0000cc"))
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
                        promotion_squares = [i for i in range(8)] if player == chess.BLACK else [i for i in range(56, 64)]
                        if move_list[1] in promotion_squares and board.piece_at(move_list[0]).piece_type == chess.PAWN:  # Promotion
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
                legal_moves = list(board.legal_moves)
                move = random.choice(legal_moves)
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
