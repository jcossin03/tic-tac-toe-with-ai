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

---

## Issue #5: Add Animated Board Transitions

**Labels:** enhancement, UI/UX

**Description:**
Add frame-by-frame animations when placing marks on the board. Instead of an instant redraw, the new mark "materializes" with a brief multi-frame animation (e.g., dot → character → colored character). Also add a winning-line flash animation when someone wins.

**Acceptance Criteria:**
- [ ] Marks appear with a short multi-frame animation
- [ ] Winning line flashes to celebrate the victory
- [ ] Animation timing is configurable via GameConfig
- [ ] Animations are short enough to not slow down gameplay

---

## Issue #6: Add Sound Effects

**Labels:** enhancement, UI/UX

**Description:**
Add terminal bell sounds for key game events: move placement, wins, ties, and invalid input. Use the standard terminal bell character (`\a`) which works universally without external dependencies.

**Acceptance Criteria:**
- [ ] Bell on move placement
- [ ] Double bell on win
- [ ] Bell on tie
- [ ] Sound can be toggled on/off via GameConfig
- [ ] No external dependencies required

---

## Issue #7: Add Game Replay System

**Labels:** enhancement, gameplay

**Description:**
After a game ends, offer the option to replay the game move-by-move. The replay shows each move being placed on the board step by step so players can review their strategy. Replays are saved as JSON and can be loaded later.

**Acceptance Criteria:**
- [ ] Save completed game replays to JSON files
- [ ] Offer replay option after each game
- [ ] Step-by-step replay with board visualization
- [ ] Option to load and watch saved replays from the main menu
- [ ] Unit tests cover replay save/load

---

## Issue #8: Add Streak Tracking and Achievements

**Labels:** enhancement, gameplay

**Description:**
Track win/loss streaks in GameStats and award achievement milestones (e.g., "First Win", "5-Game Streak", "Beat Impossible AI"). Display unlocked achievements in the lifetime stats dashboard.

**Acceptance Criteria:**
- [ ] Track current and best win streaks per difficulty
- [ ] Define achievement milestones with descriptions
- [ ] Unlock and persist achievements in stats.json
- [ ] Display achievements in lifetime stats
- [ ] Unit tests cover streak and achievement logic
