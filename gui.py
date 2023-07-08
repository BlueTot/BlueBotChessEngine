import chess.svg
import pygame
import cairosvg
import io
# import chess_011
import chess_018


class Player:
    name = "player"
    tag = 1


# class Chess011:
#     depth = 3
#     name = f"Chess v0.11 (depth {depth})"
#     tag = (chess_011.root, depth)


class Chess018:
    depth = 4
    name = f"Chess v0.18 (depth {depth})"
    tag = (chess_018.root, depth)


class ChessGame:
    def __init__(self, player1, player2, perspective):
        self.__board = chess.Board()

        pygame.init()
        pygame.display.set_caption(f"Chess: {player1.name} vs {player2.name}")
        self.__display = pygame.display.set_mode((800, 800))
        self.__clock = pygame.time.Clock()
        self.__move_list = []
        self.__player1 = player1.tag
        self.__player2 = player2.tag
        self.__perspective = perspective
        self.__gameOver = False
        self.__moves = []

    def __get_img(self, selected_square):  # Get board pygame image to render
        if selected_square is not None:
            svg = chess.svg.board(board=self.__board, flipped=True if self.__perspective == chess.BLACK else False,
                                  fill=dict.fromkeys(self.__get_move_squares(selected_square), "#cc0000cc"))
        else:
            svg = chess.svg.board(board=self.__board, flipped=True if self.__perspective == chess.BLACK else False)

        png_io = io.BytesIO()
        cairosvg.svg2png(bytestring=bytes(svg, "utf8"), write_to=png_io)
        png_io.seek(0)

        surface = pygame.image.load(png_io, "png")
        return surface

    @staticmethod
    def __get_square(x, y, flipped):  # Get square number (0 - 63) from mouse coordinates
        file = (x - 30) // (740 // 8)
        rank = 8 - (y - 30) // (740 // 8) - 1
        if flipped:
            file = 7 - file
            rank = 7 - rank
        return file + rank * 8

    def __get_move_squares(self, square):  # Get legal moves for each piece on the board
        moves = []
        for move in list(self.__board.legal_moves):
            move = str(move)
            start, dest = move[:2], move[2:4]
            if chess.square_name(square) == start:
                moves.append(chess.parse_square(dest))
        return moves

    def __player_make_move(self):
        if len(self.__move_list) == 2:  # Player clicked twice
            try:
                promotion_squares = [i for i in range(8)] if self.__board.turn == chess.BLACK else [i for i in range(56, 64)]
                if self.__move_list[1] in promotion_squares and self.__board.piece_at(
                        self.__move_list[0]).piece_type == chess.PAWN:  # Promotion
                    move = chess.Move(from_square=self.__move_list[0], to_square=self.__move_list[1], promotion=chess.QUEEN)
                else:  # Non-Promotion
                    move = chess.Move(from_square=self.__move_list[0], to_square=self.__move_list[1])
                if move in self.__board.legal_moves:  # Move is legal
                    print(san := self.__board.san(move))
                    self.__moves.append(san)
                    self.__board.push_san(san)
                else:  # Illegal move
                    raise chess.IllegalMoveError
            except chess.IllegalMoveError:
                pass
            except AttributeError:
                pass
            finally:
                self.__move_list = []

    def __computer_make_move(self):
        turn = self.__player1 if self.__board.turn else self.__player2
        move = turn[0](self.__board, turn[1])
        if move == chess.Move.null():
            move = list(self.__board.legal_moves)[-1]
        print(move)
        try:
            print(san := self.__board.san(move))
            self.__moves.append(san)
        except AssertionError:
            pass
        self.__board.push(move)

    def play(self):
        while True:
            self.__clock.tick(60)
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
                            self.__move_list.append(self.__get_square(x, y, self.__perspective == chess.BLACK))

            if not self.__gameOver:  # If game is still ongoing
                if self.__board.turn:
                    self.__computer_make_move() if type(self.__player1) == tuple else self.__player_make_move()
                else:
                    self.__computer_make_move() if type(self.__player2) == tuple else self.__player_make_move()

            # Render board
            img = pygame.transform.scale(
                self.__get_img(None if not self.__move_list else self.__move_list[0]), (800, 800))
            self.__display.blit(img, (0, 0))
            pygame.display.flip()

            if not self.__gameOver:  # game is not over
                if self.__board.is_checkmate():  # Checkmate
                    print(title := f"{'White' if not self.__board.turn else 'Black'} won the game by checkmate!")
                    pygame.display.set_caption(f"Chess: {title}")
                    self.__gameOver = True
                    print(self.__moves)

                if self.__board.is_stalemate():  # Stalemate
                    print(title := "Draw by stalemate")
                    pygame.display.set_caption(f"Chess: {title}")
                    self.__gameOver = True
                    print(self.__moves)

                if self.__board.can_claim_draw():
                    print(title := "Draw by threefold repetition")
                    pygame.display.set_caption(f"Chess: {title}")
                    self.__gameOver = True
                    print(self.__moves)

                if self.__board.is_insufficient_material():
                    print(title := "Draw by insufficient material")
                    pygame.display.set_caption(f"Chess: {title}")
                    self.__gameOver = True
                    print(self.__moves)


if __name__ in "__main__":  # Run the game
    game = ChessGame(player1=Chess018(), player2=Player(), perspective=chess.BLACK)
    game.play()
