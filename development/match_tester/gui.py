import chess.svg
import pygame
import cairosvg
import io
import chess_022, chess_029, chess_030, chess_031


class Player:
    name = "player"
    tag = 1


class Chess022:
    depth = 6
    name = f"Chess v0.22 (depth {depth})"
    tag = (chess_022.get_best_move, depth)


class Chess029:
    depth = 6
    name = f"Chess v0.29 (depth {depth})"
    tag = (chess_029.get_best_move, depth)

class Chess030:
    depth = 5
    name = f"Chess v0.30 (depth {depth})"
    tag = (chess_030.get_best_move, depth)

class Chess031:
    depth = 5
    name = f"Chess v0.31 (depth {depth})"
    tag = (chess_031.get_best_move, depth)


class ChessGame:
    def __init__(self, player1, player2, perspective, fen=None, turn=chess.WHITE):

        self.__board = chess.Board()
        if fen is not None:
            self.__board.set_board_fen(fen)
        self.__board.turn = turn

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
                promotion_squares = [i for i in range(8)] if self.__board.turn == chess.BLACK else [i for i in
                                                                                                    range(56, 64)]
                if self.__move_list[1] in promotion_squares and self.__board.piece_at(
                        self.__move_list[0]).piece_type == chess.PAWN:  # Promotion
                    move = chess.Move(from_square=self.__move_list[0], to_square=self.__move_list[1],
                                      promotion=chess.QUEEN)
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
        try:
            san = self.__board.san(move)
            print(f"\033[32;1;1m{san}\33[0m")
            self.__moves.append(san)
        except AssertionError:
            pass
        self.__board.push(move)
        print(f"FEN: {self.__board.fen()}")

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
    bot = True
    bot_perspective = True
    version = Chess029
    game = ChessGame(player1=version() if bot else Player(),
                     player2=Player() if bot else version(),
                     perspective=chess.WHITE if (bot if bot_perspective else not bot) else chess.BLACK)
    # game = ChessGame(player1=Chess022(), player2=Player(), perspective=chess.WHITE,
    #                  fen="r1b1k2r/ppppnppp/2n3q1/1Bb3B1/3pP3/2P2N2/PP3PPP/RN1Q1RK1")
    game.play()

'''original fen test: r1bqkbnr/pppp1ppp/8/4p3/2BnP3/5N2/PPPP1PPP/RNBQK2R
   second fen test: 1q1r1rk1/pb2bppp/1pn1pn2/8/3P4/P1N1BN2/1P2QPPP/1B1R1RK1
   third fen test: r3kb1r/pppb1ppp/2n1p3/qB6/3P4/1QP1PN2/P4PPP/R1B1K2R
   fourth fen test: r1b1k2r/ppppnppp/2n3q1/1Bb3B1/3pP3/2P2N2/PP3PPP/RN1Q1RK1'''