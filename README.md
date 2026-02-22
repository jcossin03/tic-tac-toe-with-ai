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

### Weekend 7: Refactor & AI Upgrades
**Status:** Complete

**Python Concepts:** Classes, modules, minimax algorithm, recursion, unit testing

- Refactored game logic into `Board` and `AI` classes in `game_logic.py`
- Separated core logic from terminal I/O for testability
- Added minimax algorithm for unbeatable "Impossible" difficulty
- Added "Medium" difficulty (50/50 strategic vs random)
- AI now explains its moves after each turn
- Winning line highlighted with green background
- 43 unit tests covering board, win detection, ties, and all AI levels

### Weekend 8: New Game Modes & Stats
**Status:** Complete

**Python Concepts:** JSON file I/O, persistent storage, multiple AI instances

- First-move selection — choose whether X or O goes first
- AI vs AI watch mode — pick difficulties for both sides and watch them play
- Post-game move history — see every move in order after the game ends
- Persistent statistics — wins/losses/ties saved to `stats.json` across sessions
- Lifetime stats dashboard shown at startup and exit

### Weekend 9: Tournament, Timed Mode & Config
**Status:** Complete

**Python Concepts:** Threading, configuration patterns, state machines

- Tournament mode — best-of-3/5/7 series with visual bracket progress
- Timed mode — configurable per-move countdown (5/10/15 seconds) with auto-move on timeout
- Difficulty auto-adjustment — suggests harder/easier difficulty based on win rate
- Configuration system — `GameConfig` class centralizes all hardcoded values
- 21 new unit tests (70 total, all passing)

### Weekend 10: Animations, Replays & Achievements
**Status:** Complete

**Python Concepts:** Frame-based animation, JSON serialization, achievement patterns

- Animated board transitions — marks appear with a multi-frame animation (. → + → * → X/O)
- Winning line flash — the winning three cells flash on/off to celebrate
- Sound effects — terminal bell on moves, wins, and ties (toggleable via config)
- Game replay system — save games as JSON, browse and rewatch step-by-step from the menu
- Win streak tracking — current and best streak displayed in lifetime stats
- Achievement system — 8 milestones (First Win, Beat Impossible, streaks, Explorer, etc.)
- 14 new unit tests (84 total, all passing)

## Future Improvements

A backlog of ideas for future weekends, organized by category.

### Gameplay Enhancements

- [x] **Unbeatable AI (Minimax)** — Implement the minimax algorithm as a third "Impossible" difficulty that never loses
- [x] **Medium difficulty** — Bridge the gap between Easy and Hard (e.g., 50% chance of making the optimal move)
- [ ] **4x4 or 5x5 board** — Let players choose board size for more strategic variety
- [x] **First-move selection** — Let the player choose who goes first instead of X always starting

### AI & Intelligence

- [x] **AI move explanation** — After each AI move, optionally show *why* it chose that move ("Blocking your win!", "Taking the center")
- [x] **Difficulty auto-adjustment** — Track win/loss ratio and suggest or auto-adjust difficulty when a player is dominating or struggling

### UI/UX Improvements

- [x] **Highlight winning line** — When someone wins, highlight the three winning cells in a different color
- [x] **Move history display** — Show a post-game summary of all moves in order for strategy review
- [x] **Persistent game statistics** — Save stats (wins, losses, ties per difficulty) to a JSON file so they survive between sessions
- [x] **Animated board transitions** — Add frame-by-frame animations when placing marks instead of instant redraws
- [x] **Sound effects** — Terminal bell or `playsound` library for move placement, wins, and ties

### Architecture & Code Quality

- [x] **Unit tests** — Create `test_tictactoe.py` with tests for win detection, AI moves, board state, and input validation
- [x] **Refactor into classes** — Extract `Game`, `Board`, `Player`, and `AI` classes from the procedural code
- [x] **Configuration file** — Move hardcoded values (board size, thinking delay, colors) into a config dict or file

### New Game Modes

- [x] **Tournament mode** — Best-of-3 or best-of-5 series with bracket-style progression
- [x] **Timed mode** — Each player gets a time limit per move (e.g., 10 seconds)
- [x] **AI vs AI mode** — Watch two AI players at different difficulties play each other

### Platform & Distribution

- [ ] **Web version** — Port to a browser-based game using Flask or a rich TUI library like Textual
- [ ] **Network multiplayer** — Two-player games over a local network using sockets

### Recommended Starting Points

| Priority | Feature | Why |
|----------|---------|-----|
| 1 | Minimax AI (Impossible mode) | Classic CS algorithm, natural next step for the AI |
| 2 | Unit tests | Already listed in project structure, improves confidence |
| 3 | Highlight winning line | Small change, big UX payoff |
| 4 | AI move explanation | Fits the educational tone of the project |
| 5 | Persistent stats (JSON) | Makes repeated play more rewarding |

## Project Structure

```
tic-tac-toe/
  tictactoe.py        # Main game file (terminal UI)
  game_logic.py       # Core game engine (Board, AI, Tournament, GameReplay, GameStats)
  test_tictactoe.py   # 84 unit tests
  ISSUES.md           # Feature issue tracker
  README.md           # This file
  .gitignore          # Git ignore rules for Python
  replays/            # Saved game replays (gitignored)
  stats.json          # Persistent stats (gitignored)
```

## What We're Learning

- **Python fundamentals** — variables, lists, loops, functions, input/output
- **Problem solving** — breaking a game into small, buildable pieces
- **Git & GitHub** — version control, branches, pull requests
- **AI-assisted coding** — using AI as a learning partner, not a replacement for thinking
