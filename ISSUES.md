# GitHub Issues Tracker

This file tracks planned feature issues for the tic-tac-toe project.
Create these as GitHub issues to follow proper CI/CD workflows.

---

## Issue #1: Add Tournament Mode (Best-of-N Series)

**Labels:** enhancement, gameplay

**Description:**
Add a tournament mode where players compete in a best-of-N series (best-of-3, best-of-5, or best-of-7). The game should track series progress, display a tournament bracket/scoreboard between games, and announce the series winner at the end.

**Acceptance Criteria:**
- [ ] Players can select tournament mode from the game mode menu
- [ ] Players choose series length (best-of-3, 5, or 7)
- [ ] Series progress is displayed between rounds
- [ ] Series winner is announced when a player clinches the majority
- [ ] Results are recorded in persistent stats
- [ ] Unit tests cover tournament logic

---

## Issue #2: Add Timed Mode (Move Time Limits)

**Labels:** enhancement, gameplay

**Description:**
Add a timed mode where each player has a configurable time limit per move (e.g., 5, 10, or 15 seconds). If a player runs out of time, a random valid move is made for them. A countdown timer should be visible during the player's turn.

**Acceptance Criteria:**
- [ ] Players can enable timed mode from settings
- [ ] Configurable time limits (5s, 10s, 15s)
- [ ] Visual countdown during player's turn
- [ ] Auto-move (random) when time expires
- [ ] Works in single-player and two-player modes
- [ ] Unit tests cover timer logic

---

## Issue #3: Add Difficulty Auto-Adjustment Suggestions

**Labels:** enhancement, AI

**Description:**
Track the player's win/loss ratio per difficulty level and suggest adjusting the difficulty when the player is consistently winning (>70% win rate over last 5+ games) or losing (<20% win rate). Show the suggestion at the end of a game, not intrusively.

**Acceptance Criteria:**
- [ ] Track win rate per difficulty in GameStats
- [ ] Suggest harder difficulty when player dominates (>70% wins)
- [ ] Suggest easier difficulty when player struggles (<20% wins)
- [ ] Suggestions are non-intrusive (post-game)
- [ ] Minimum 5 games before suggesting
- [ ] Unit tests cover suggestion logic

---

## Issue #4: Add Configuration System

**Labels:** enhancement, architecture

**Description:**
Extract hardcoded values (thinking delay, color codes, board display characters, time limits) into a centralized configuration dictionary in `game_logic.py`. This makes the game easier to customize and sets up for future config file support.

**Acceptance Criteria:**
- [ ] Create a `GameConfig` class with all configurable values
- [ ] Replace hardcoded values in tictactoe.py with config references
- [ ] Default config works identically to current behavior
- [ ] Unit tests verify config defaults
