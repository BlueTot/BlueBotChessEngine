# DEPRECATED

This repository is no longer maintained.
Please use [BlueTot/bluebot2](https://github.com/BlueTot/bluebot2) instead.
This repo is kept for historical/reference purposes only.

# Bluebot Chess Engine

A ~2000 rated classical minimax chess engine written in python that started out of a tutorial. It used to play on chess.com as `BlueBotChessTest4` with a peak rating of 2096 in 10+0 rapid, and it won against Komodo 17 (2100) on chess.com and Fairy Stockfish 6 (~2100) on lichess in 10+0 rapid.

## Installation / Downloading

First, clone the repository

```bash
git clone https://github.com/BlueTot/bluetot-chess-engine
```

Install PyPy if you don't have it already (these instructions are for linux, search online for how to install on other OS's)

```bash
wget https://downloads.python.org/pypy/pypy3.10-v7.3.15-linux64.tar.bz2
tar -xvf pypy3.10-v7.3.15-linux64.tar.bz2
sudo mv pypy3.10-v7.3.15-linux64 /opt/pypy3.10
sudo ln -s /opt/pypy3.10/bin/pypy3 /usr/local/bin/pypy3
```

Install Pip for PyPy and install the `chess` library

```bash
pypy3 -m ensurepip
pypy3 -m pip install --upgrade pip
pypy3 -m pip install python-chess
```

Lastly, run the engine, and have fun!

```bash
cd bluebot-chess-engine
pypy3 main.py
```

## Features

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

Feel free to use this engine however you want! If you get banned for cheating using this program on a public website (chess.com, lichess) it is your fault!
