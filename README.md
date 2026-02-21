# Tic-Tac-Toe with AI

A Python tic-tac-toe game built incrementally over several weekends as a learning project. Each weekend introduces new Python concepts while adding features to the game.

## How to Play

```bash
python tictactoe.py
```

Requires **Python 3.10+**.

## Weekend Roadmap

### Weekend 1: Setup & Game Board
**Status:** Complete

**Python Concepts:** Lists, nested lists, printing, functions

- Display a 3x3 game board
- Number the positions (1-9) so players know where to play

### Weekend 2: Taking Turns
**Status:** Complete

**Python Concepts:** Input, variables, if/elif/else, while loops

- Two players take turns entering moves
- Place X's and O's on the board
- Input validation (must be 1-9, can't play in taken spots)

### Weekend 3: Winning & Ending
**Status:** Complete

**Python Concepts:** Functions, returning values, boolean logic

- Check for three in a row (horizontal, vertical, diagonal)
- Detect when the board is full (tie game)
- Announce the winner

### Weekend 4: Polish & Features
**Status:** Complete

**Python Concepts:** String formatting, clearing screen, game loop

- Visual improvements (colors or borders)
- Play-again option
- Score tracking across multiple games
- Player names

### Weekend 5-6: AI Player
**Status:** Complete

**Python Concepts:** Random module, time module, simple strategy, "what if" logic

- Single-player and two-player game modes
- Easy difficulty (random moves)
- Hard difficulty (strategic AI: win → block → center → corner → random)
- Computer "thinking" animation
- Difficulty display during gameplay

## Project Structure

```
tic-tac-toe/
  tictactoe.py        # Main game file
  test_tictactoe.py   # Unit tests
  README.md           # This file
  .gitignore          # Git ignore rules for Python
```

## What We're Learning

- **Python fundamentals** — variables, lists, loops, functions, input/output
- **Problem solving** — breaking a game into small, buildable pieces
- **Git & GitHub** — version control, branches, pull requests
- **AI-assisted coding** — using AI as a learning partner, not a replacement for thinking
