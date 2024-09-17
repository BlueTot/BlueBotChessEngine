import chess
import chess_036t, chess_078t, chess_079, chess_080, chess_081

class Chess036:
    depth = 6
    name = f"Chess v0.36 (depth {depth})"
    tag = (chess_036t.get_best_move, depth)

class Chess078:
    depth = 6
    name = f"Chess v0.78 (depth {depth})"
    tag = (chess_078t.ChessEngine, depth, "")

class Chess079:
    depth = 7
    name = f"Chess v0.79 (depth {depth})"
    tag = (chess_079.get_best_move, depth)

class Chess080:
    depth = 6
    name = f"Chess v0.80 (depth {depth})"
    tag = (chess_080.get_best_move, depth)

class Chess081:
    depth = 6
    name = f"Chess v0.81 (depth {depth})"
    tag = (chess_081.get_best_move, depth)

CCR_TEST_SUITE = """rn1qkb1r/pp2pppp/5n2/3p1b2/3P4/2N1P3/PP3PPP/R1BQKBNR w KQkq - 0 1 id "CCR01"; bm Qb3;
rn1qkb1r/pp2pppp/5n2/3p1b2/3P4/1QN1P3/PP3PPP/R1B1KBNR b KQkq - 1 1 id "CCR02";bm Bc8;
r1bqk2r/ppp2ppp/2n5/4P3/2Bp2n1/5N1P/PP1N1PP1/R2Q1RK1 b kq - 1 10 id "CCR03"; bm Nh6; am Ne5;
r1bqrnk1/pp2bp1p/2p2np1/3p2B1/3P4/2NBPN2/PPQ2PPP/1R3RK1 w - - 1 12 id "CCR04"; bm b4;
rnbqkb1r/ppp1pppp/5n2/8/3PP3/2N5/PP3PPP/R1BQKBNR b KQkq - 3 5 id "CCR05"; bm e5; 
rnbq1rk1/pppp1ppp/4pn2/8/1bPP4/P1N5/1PQ1PPPP/R1B1KBNR b KQ - 1 5 id "CCR06"; bm Bcx3+;
r4rk1/3nppbp/bq1p1np1/2pP4/8/2N2NPP/PP2PPB1/R1BQR1K1 b - - 1 12 id "CCR07"; bm Rfb8;
rn1qkb1r/pb1p1ppp/1p2pn2/2p5/2PP4/5NP1/PP2PPBP/RNBQK2R w KQkq c6 1 6 id "CCR08"; bm d5;
r1bq1rk1/1pp2pbp/p1np1np1/3Pp3/2P1P3/2N1BP2/PP4PP/R1NQKB1R b KQ - 1 9 id "CCR09"; bm Nd4;
rnbqr1k1/1p3pbp/p2p1np1/2pP4/4P3/2N5/PP1NBPPP/R1BQ1RK1 w - - 1 11 id "CCR10"; bm a4;
rnbqkb1r/pppp1ppp/5n2/4p3/4PP2/2N5/PPPP2PP/R1BQKBNR b KQkq f3 1 3 id "CCR11"; bm d5;
r1bqk1nr/pppnbppp/3p4/8/2BNP3/8/PPP2PPP/RNBQK2R w KQkq - 2 6 id "CCR12"; bm Bxf7+;
rnbq1b1r/ppp2kpp/3p1n2/8/3PP3/8/PPP2PPP/RNBQKB1R b KQ d3 1 5 id "CCR13"; am Ne4; 
rnbqkb1r/pppp1ppp/3n4/8/2BQ4/5N2/PPP2PPP/RNB2RK1 b kq - 1 6 id "CCR14"; am Nxc4;
r2q1rk1/2p1bppp/p2p1n2/1p2P3/4P1b1/1nP1BN2/PP3PPP/RN1QR1K1 w - - 1 12 id "CCR15"; bm exf6;
r1bqkb1r/2pp1ppp/p1n5/1p2p3/3Pn3/1B3N2/PPP2PPP/RNBQ1RK1 b kq - 2 7 id "CCR16"; bm d5;
r2qkbnr/2p2pp1/p1pp4/4p2p/4P1b1/5N1P/PPPP1PP1/RNBQ1RK1 w kq - 1 8 id "CCR17"; am hxg4;
r1bqkb1r/pp3ppp/2np1n2/4p1B1/3NP3/2N5/PPP2PPP/R2QKB1R w KQkq e6 1 7 id "CCR18"; bm Bxf6+;
rn1qk2r/1b2bppp/p2ppn2/1p6/3NP3/1BN5/PPP2PPP/R1BQR1K1 w kq - 5 10 id "CCR19"; am Bxe6;
r1b1kb1r/1pqpnppp/p1n1p3/8/3NP3/2N1B3/PPP1BPPP/R2QK2R w KQkq - 3 8 id "CCR20"; am Ndb5;
r1bqnr2/pp1ppkbp/4N1p1/n3P3/8/2N1B3/PPP2PPP/R2QK2R b KQ - 2 11 id "CCR21"; am Kxe6;
r3kb1r/pp1n1ppp/1q2p3/n2p4/3P1Bb1/2PB1N2/PPQ2PPP/RN2K2R w KQkq - 3 11 id "CCR22"; bm a4;
r1bq1rk1/pppnnppp/4p3/3pP3/1b1P4/2NB3N/PPP2PPP/R1BQK2R w KQ - 3 7 id "CCR23"; bm Bxh7+;
r2qkbnr/ppp1pp1p/3p2p1/3Pn3/4P1b1/2N2N2/PPP2PPP/R1BQKB1R w KQkq - 2 6 id "CCR24"; bm Nxe5;
rn2kb1r/pp2pppp/1qP2n2/8/6b1/1Q6/PP1PPPBP/RNB1K1NR b KQkq - 1 6 id "CCR25"; am Qxb3;""".splitlines()

# Test Suite
class TestSuite:

    def __init__(self, chess_engine, fens):
        if len(chess_engine.tag) == 3:
            engine = chess_engine.tag[0]()
            self.__computer = (engine.get_best_move, chess_engine.tag[1])
        else:
            self.__computer = chess_engine.tag
        self.__fens = fens

        open('testlog.txt', 'w').close()
        with open("testlog.txt", "a") as f:
            f.write(f"Test Suite with {chess_engine.name}\n")
        open('testlogdata.txt', 'w').close()
    
    def test_fen(self, fen):
        
        # initialise the board
        self.__board = chess.Board()
        fen_splitted = fen.split(" ")
        self.__board.set_board_fen(fen_splitted[0])
        self.__board.turn = {"w": chess.WHITE, "b": chess.BLACK}[fen_splitted[1]]
        self.__board.set_castling_fen(fen_splitted[2])

        # run chess engine on given position
        data = self.__computer[0](self.__board, self.__computer[1])
        if isinstance(data, chess.Move):
            print(s := f"{fen}: {data}, book")
        else:
            best_move, nodes, time = data
            print(s := f"{fen}: {best_move}, {nodes}, {time}, {nodes/time}")
            with open("testlogdata.txt", "a") as f:
                f.write(f"{nodes}\n")
        with open("testlog.txt", "a") as f:
            f.write(s + "\n")
    
    def run(self):

        for fen in self.__fens:
            self.test_fen(fen)

if __name__ in "__main__":

    test_suite = TestSuite(Chess078, CCR_TEST_SUITE)
    test_suite.run()