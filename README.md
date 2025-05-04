# Gobblet Jr. – Python Board Game Project

## Overview

This project implements **Gobblet Jr.**, a simplified 3x3 board game inspired by Tic-Tac-Toe but with a strategic twist! Built using Python, this game supports 2 players with each having 6 pieces (2 small, 2 medium, 2 large) of their respective color.

**Features:**
- Full game logic implemented as per the official [Gobblet Jr. rules](https://docs.racket-lang.org/games/gobblet.html)
- 3x3 interactive game board
- Stackable pieces with hiding mechanics
- Graphical user interface using `pygame`
- Linting and code improvements tracked with `pylint`

## Game Rules

- Each player has 6 pieces: 2 small, 2 medium, and 2 large.
- Players take turns placing or moving their pieces on the 3x3 board.
- A larger piece can **gobble** (cover) a smaller one.
- You **cannot move** a piece that is covered by another.
- The goal is to **align 3 visible top pieces** of your color in a row (horizontal, vertical, or diagonal).

For a visual explanation: [YouTube video](https://www.youtube.com/watch?v=nYvYEhBG9HM)

## Assumptions

- Only the top-most piece in a stack is visible and counts toward win conditions.
- Players can move their own previously placed pieces as long as they are not covered.
- Input is taken via mouse interaction through the `pygame` interface.
- Game automatically detects invalid moves (e.g., placing smaller piece on a larger one).
- Turn-based system strictly enforced.

## Installation & Usage

### Install the dependencies using:
``` bash
pip install pygame pylint 
```

### Running the program

```bash
cd OriginalGame
python3 gobblet.py
```

## Project Structure

```bash
GobbletJr/
│
├── OriginalGame/
│ └── gobblet.py # Main executable game file
│
├── InitialLint/
│ └── result.txt # Initial Pylint result before refactoring
│
├── AllLint/
│ ├── gobblet_1/
│ │ ├── gobblet_1.py
│ │ └── result_1.txt # First iteration result
│ │
│ ├── gobblet_2/
│ │ ├── gobblet_2.py
│ │ └── result_2.txt # Second iteration result
│ │
│ └── gobblet_final/
│ ├── gobbletfinal.py # Final version of the game
│ └── lintfinal.txt # Final Pylint result
│
└── README.md 


