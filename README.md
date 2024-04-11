# BlueBotChessEngine
A python chess bot that started out of a tutorial

Used to play on chess.com as: (chess v0.22)
- BlueBotChessTest2 : 1355 rating on 15 | 10 rapid
- BlueBotChessTest3 : 1833 rating on 10 min rapid

Latest version won against:
- Komodo 17 (2100) on chess.com
- Fairy Stockfish 6 (~2100) on lichess in 10 min rapid

Latest version: v0.36

Main features:
- Depth 6 alpha-beta negamax search
- Quiescence search
- Simple material evaluation function
- Simple move ordering based on evaluation function
- Null move pruning
- Transposition table with principal variation move ordering
- Iterative deepening
- Killer heuristic move ordering
- Aspiration windows

Also...
- All chess bot releases use an opening book called Titans which can be found here: https://digilander.libero.it/taioscacchi/archivio/Titans.zip
- Latest version v0.36 is best run with PyPy instead of normal Python which can be found here: https://www.pypy.org/download.html
