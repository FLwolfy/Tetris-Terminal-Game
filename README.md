# Tetris Terminal Game

Welcome to Tetris Terminal Game, an terminal game version of the classic Tetris Game developed for INFOSCI-102 FINAL PROJ.

## Preview
Here is the preview PNG:
<div align="center">
  <img src="Preview.png" alt="Preview">
</div>

## About the Game

Tetris Terminal Game is a FINAL PROJ for DKU INFOSCI-102. This adds on some [_advanced features_](#advanced-features) based on the original game.

## How to Play

To play this game, follow these simple steps:

- To start the game, double click the `Tetris.exe` file, or enter the command:
```bash
python main.py
```
- To control the block, press keyboard `A` and `D` buttons to apply left or right move, press keyboard `Q` and `R` buttons to rotate counterclockwise or clockwise, and press keyboard `D` button to immediately drag down.
- Press keyboard `SPACE` button to pause the game, and press keyboard `ESC` button to quit the game.
- Do __NOT__ stretch the terminal window, or the game may bug.

## Advanced Features

#### 1. Different Levels of Difficulty:
This game now offers players three levels of difficulty (easy, normal, hard). Players can choose various speeds of falling blocks on the board.

#### 2. Special Blocks with Unique Abilities: 
This game has special blocks that can eliminate the corresponding column when the special blocks are eliminated.

#### 3. High Score System:
This game keeps track of your overall performance. The high score system now stores and displays the different highest record score of all gamemodes.

#### 4. Sound Effects and Music:
This game contains sound effects for block movements and background music to enhance the overall gameplay experience.

#### 5. Pause and Save Functionality:
This game has the ability to pause the ongoing game (press `SPACE`) and also save the current game state for next time gaming.

#### 6. Different Game Modes:
This game now offers different modes, including __Classic__, __Stretch__, and __Drawing__ modes:
- 6.1 __Classic mode__:\
   Mirrors the original game with special blocks involved.

- 6.2 __Stretch mode__:\
   Adds a dynamic gameplay to the gameboard by continuously changing the right border.

- 6.3 __Drawing mode__:\
   Introduces creative tasks, providing players with specific "shape" challenges to complete.
  
#### 7. Replay System: 
After each game ends, players can now replay their game, allowing them to analyze their performance, identify mistakes, and improve their Tetris skills in different modes.

## Requirements

#### 1. Environment:
Make sure you have Python installed (>=3.11.6 for .exe) on your system to run the game successfully.

#### 2. Package:
Make sure the following dependent libraries are installed:
- `KBHit`
- `simpleaudio`

## Notes

This is a course PROJ. Feel free to contribute to the project by submitting bug reports or suggesting improvements. Feedback and ideas are welcomed to make Tetris Terminal Game better.

Happy gaming! 🎮
