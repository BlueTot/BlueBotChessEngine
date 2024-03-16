import chess.svg
import cairosvg
import pygame
import io

import bitboards.bitboard_09 as mvg


class Modes:
    PLAYER_VS_COMPUTER = 0
    COMPUTER_ONLY = 1
    PLAYER_ONLY = 2


def get_img(overlay, board, selected_square, player):  # Get board pygame image to render
    if selected_square is not None:
        svg = chess.svg.board(board=overlay, flipped=True if player == chess.BLACK else False,
                              fill=dict.fromkeys(get_move_squares(board, selected_square), "#cc0000cc"))
    else:
        svg = chess.svg.board(board=overlay, flipped=True if player == chess.BLACK else False)

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
    for move in board.legal_moves:
        move = move.uci()
        start, dest = move[:2], move[2:4]
        if chess.square_name(square) == start:
            moves.append(chess.parse_square(dest))
    return moves


def player_make_move(board, overlay, player, move_list):
    if len(move_list) == 2:  # Player clicked twice
        try:
            promotion_squares = [i for i in range(8)] if overlay.turn == chess.BLACK else [i for i in range(56, 64)]
            if move_list[1] in promotion_squares and board.piece_at(move_list[0]).piece_type == mvg.PAWN:  # Promotion
                board_move = mvg.Move(from_square=move_list[0], to_square=move_list[1], promotion=mvg.QUEEN)
                overlay_move = chess.Move(from_square=move_list[0], to_square=move_list[1], promotion=chess.QUEEN)
            else:  # Non-Promotion
                board_move = mvg.Move(from_square=move_list[0], to_square=move_list[1])
                overlay_move = chess.Move(from_square=move_list[0], to_square=move_list[1])
            print(board.legal_moves)
            if board.is_en_passant(board_move):
                board_move.en_passant = True
            elif board.is_castling(board_move):
                board_move.castling = True
            if board_move.uci() in [move.uci() for move in board.legal_moves]:  # Move is legal
                board.push(board_move)
                overlay.push(overlay_move)
                print(board_move)
            else:  # Illegal move
                print(board_move.uci())
                raise chess.IllegalMoveError
        except chess.IllegalMoveError:
            pass
        except AttributeError:
            pass
        finally:
            move_list = []
    return board, overlay, player, move_list


def main():  # Main Loop
    overlay = chess.Board()
    board = mvg.Board()

    pygame.init()
    pygame.display.set_caption("Chess")
    display = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    move_list = []
    player = chess.WHITE
    mode = Modes.PLAYER_ONLY
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
                board, overlay, player, move_list = player_make_move(board, overlay, player, move_list)

        # Render board
        img = pygame.transform.scale(get_img(overlay, board, None if not move_list else move_list[0], player), (800, 800))
        display.blit(img, (0, 0))
        pygame.display.flip()

        if not gameOver:  # game is not over
            if overlay.is_checkmate():  # Checkmate
                print(title := f"{'White' if not overlay.turn else 'Black'} won the game by checkmate!")
                pygame.display.set_caption(f"Chess: {title}")
                gameOver = True

            if overlay.is_stalemate():  # Stalemate
                print(title := "Draw by stalemate")
                pygame.display.set_caption(f"Chess: {title}")
                gameOver = True

            if overlay.can_claim_draw():
                print(title := "Draw by threefold repetition")
                pygame.display.set_caption(f"Chess: {title}")
                gameOver = True

            if overlay.is_insufficient_material():
                print(title := "Draw by insufficient material")
                pygame.display.set_caption(f"Chess: {title}")
                gameOver = True


if __name__ in "__main__":  # Run the game
    main()
