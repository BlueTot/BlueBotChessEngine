# BlueBotChessEngine
A python chess bot that started out of a tutorial

Used to play on chess.com as: (chess v0.22)
- BlueBotChessTest2 : 1355 rating on 15 | 10 rapid
- BlueBotChessTest3 : 1833 rating on 10 min rapid

Latest version: v0.29

Main features:
- Depth 5 - 6 alpha-beta negamax search
- Quiescence search
- Simple material evaluation function
- Simple move ordering based on evaluation function
- Null move pruning
- Principal Variation move ordering
- Iterative deepening

Also...
- All chess bot releases use an opening book called Titans which can be found here: https://digilander.libero.it/taioscacchi/archivio/Titans.zip
- Latest version v0.29 is best run with PyPy instead of normal Python which can be found here: https://www.pypy.org/download.html
