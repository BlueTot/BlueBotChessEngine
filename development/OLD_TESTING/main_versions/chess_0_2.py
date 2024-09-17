import chess.svg
import pygame
import cairosvg
import io
import random


def get_img(board, selected_square, player):
    if selected_square is not None:
        svg = chess.svg.board(board=board, flipped=True if player == "Black" else False, fill=dict.fromkeys(board.attacks(selected_square), "#cc0000cc"))
    else:
        svg = chess.svg.board(board=board, flipped=True if player == "Black" else False)

    png_io = io.BytesIO()
    cairosvg.svg2png(bytestring=bytes(svg, "utf8"), write_to=png_io)
    png_io.seek(0)

    surface = pygame.image.load(png_io, "png")
    return surface


def get_square(x, y, flipped):
    file = (x - 30) // (740 // 8)
    rank = 8 - (y - 30) // (740 // 8) - 1
    if flipped:
        file = 7 - file
        rank = 7 - rank
    return file + rank * 8


def main():
    board = chess.Board()

    pygame.init()
    pygame.display.set_caption("Chess")
    display = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    move_list = []
    player = "White"
    turn = "White"
    movePlayed = False
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
                        move_list.append(get_square(x, y, player == "Black"))

        if not gameOver:
            if turn == player:
                if len(move_list) == 2:
                    try:
                        promotion_squares = [i for i in range(8)] if player == "White" else [i for i in range(56, 64)]
                        if move_list[1] in promotion_squares and board.piece_at(move_list[0]).piece_type == chess.PAWN:
                            move = chess.Move(from_square=move_list[0], to_square=move_list[1], promotion=chess.QUEEN)
                        else:
                            move = chess.Move(from_square=move_list[0], to_square=move_list[1])
                        if move in board.legal_moves:
                            print(san := board.san(move))
                            board.push_san(san)
                            movePlayed = True
                        else:
                            raise chess.IllegalMoveError

                    except chess.IllegalMoveError:
                        print("Illegal move, try again!")
                    except AttributeError:
                        print("Illegal move, try again!")
                    finally:
                        move_list = []
            else:
                legal_moves = list(board.legal_moves)
                move = random.choice(legal_moves)
                board.push(move)
                movePlayed = True

        img = pygame.transform.scale(get_img(board, None if not move_list else move_list[0], player), (800, 800))
        display.blit(img, (0, 0))
        pygame.display.flip()

        if board.is_checkmate() and not gameOver:
            print(title := f"{player} won the game by checkmate!")
            pygame.display.set_caption(f"Chess: {title}")
            gameOver = True

        if board.is_stalemate() and not gameOver:
            print(title := "Draw")
            pygame.display.set_caption(f"Chess: {title}")
            gameOver = True

        if movePlayed and not gameOver:
            turn = "White" if turn == "Black" else "Black"
            movePlayed = False


if __name__ in "__main__":
    main()
