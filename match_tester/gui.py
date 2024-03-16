import chess.svg
import pygame
import cairosvg
import io
import chess_020, chess_021, chess_022, chess_023, chess_025, chess_027, chess_028


class Player:
    name = "player"
    tag = 1


class Chess020:
    depth = 4
    name = f"Chess v0.20 (depth {depth})"
    tag = (chess_020.root, depth)


class Chess021:
    depth = 4
    name = f"Chess v0.21 (depth {depth})"
    tag = (chess_021.root, depth)


class Chess022:
    depth = 4
    name = f"Chess v0.22 (depth {depth})"
    tag = (chess_022.get_best_move, depth)


class Chess023:
    depth = 4
    name = f"Chess v0.23 (depth {depth})"
    tag = (chess_023.get_best_move, depth)


class Chess025:
    depth = 4
    name = f"Chess v0.25 (depth {depth})"
    tag = (chess_025.get_best_move, depth)


class Chess027:
    depth = 4
    name = f"Chess v0.27 (depth {depth})"
    tag = (chess_027.get_best_move, depth)


class Chess028:
    depth = 4
    name = f"Chess v0.28 (depth {depth})"
    tag = (chess_028.get_best_move, depth)


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
            print(san := self.__board.san(move))
            self.__moves.append(san)
        except AssertionError:
            pass
        self.__board.push(move)
        print(self.__board.fen())
        print(self.__board.legal_moves)

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
    bot_perspective = False
    game = ChessGame(player1=Chess022() if bot else Player(),
                     player2=Player() if bot else Chess022(),
                     perspective=chess.WHITE if (bot if bot_perspective else not bot) else chess.BLACK)
                         # game = ChessGame(player1=Chess027(), player2=Chess022(), perspective=chess.WHITE,
    #                  fen="r4rk1/pp2ppbp/3p1np1/2q5/1n2PPb1/2NB1N2/PPP3PP/R1B1QR1K")
    # game = ChessGame(player1=Chess022(), player2=Chess022(), perspective=chess.WHITE,
    #                  fen="r1b1kbnr/pp1n1ppp/2p1p3/3p4/3PP3/3BBP2/PqPN2PP/R2QK1NR")
    game.play()

'''
chess 0.23 : 1.5
chess 0.22 : 3.5
'''

'''
chess 0.24: 7.0
chess 0.22: 6.0
'''

'''
chess 0.25 : 1.0
chess 0.22 : 0.0

first game: ['c4', 'Nf6', 'Nc3', 'e6', 'Nf3', 'Bb4', 'g3', 'O-O', 'Bg2', 'd5', 'a3', 'Bxc3', 'dxc3', 'Nbd7', 'cxd5', 'exd5', 'O-O', 'b6', 'Bf4', 'Bb7', 'e3', 'Nc5', 'c4', 'Ne6', 'cxd5', 'Nxf4', 'gxf4', 'Qxd5', 'Re1', 'Rfe8', 'Qc2', 'Qd6', 'Rad1', 'Qc5', 'Qxc5', 'bxc5', 'Rc1', 'Nd7', 'b4', 'cxb4', 'Rxc7', 'Bxf3', 'Bxf3', 'Rad8', 'axb4', 'a6', 'Bc6', 'Re7', 'Ra1', 'Kf8', 'Rd1', 'Ke8', 'Ra7', 'h5', 'e4', 'h4', 'f5', 'h3', 'Rd6', 'f6', 'Rd3', 'g5', 'Rxh3', 'Rg7', 'Rh8+', 'Ke7', 'Rxd8', 'Kxd8', 'Rxa6', 'Ne5', 'Bd5', 'Nd3', 'b5', 'Ke7', 'Re6+', 'Kf7', 'Rc6+', 'Ke7', 'b6', 'Nb4', 'Re6+', 'Kd8', 'Rxf6', 'Nxd5', 'exd5', 'Kc8', 'Rf8+', 'Kb7', 'd6', 'Kxb6', 'f6', 'Rd7', 'f7', 'Rb7', 'Rg8', 'Rxf7', 'Rxg5', 'Kc6', 'Rg6', 'Rd7', 'Rf6', 'Rxd6', 'Rf7', 'Rd7', 'Rxd7', 'Kxd7', 'h4', 'Kc8', 'h5', 'Kb7', 'h6', 'Kb8', 'h7', 'Ka8', 'h8=Q+', 'Kb7', 'Qe5', 'Ka8', 'Qd6', 'Kb7', 'Qf4', 'Ka8', 'Qe5', 'Kb7', 'Qd6', 'Ka8', 'Qc6+', 'Kb8', 'Qa6', 'Kc7', 'Qb5', 'Kc8', 'Qb6', 'Kd7', 'Qc5', 'Ke8', 'Qf5', 'Kd8', 'Qc5', 'Ke8', 'Qd6', 'Kf7', 'Qc5']


'''

'''fen="r4rk1/2p1qppp/p1p2n2/1p6/4PQ2/2N5/PPP2PPP/R2R2K1"'''