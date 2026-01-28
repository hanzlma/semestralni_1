# Prsi card game with CLI interface

## How to run
Using a terminal in this directory
### Program

```
python -m main
```

### Tests

```
pytest
```

## Code structure

### main.py
Runs the game
### game_runner.py
Contains the runner class which manages the game as a whole
### player.py
Contains the player classes, both for the human and the computer player
### cards.py
Contains card pack and card hand classes
### tests
Module containing test files.

## How it works
1. On start, the player chooses a difficulty.
2. Afterwards, the cards are generated and given to human and computer players according to prsi rules.
3. When player chooses to play a certain card, check_card_playble [game_runner.py] checks if it can be played or not.
4. If it can be played, it is moved from the players card to the top of the played card pack.
5. The computer players turn implements a minimax algorithm which decides what is the best decision to do.