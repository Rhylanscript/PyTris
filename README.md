# PyTris

PyTris is a Python-based Tetris clone built with `pygame`. It features smooth block movement, line clearing, score tracking, high score persistence, and simple keyboard controls.

## Features

- Classic Tetris-style gameplay
- Seven standard tetromino shapes
- Next-piece preview
- Score and high score tracking
- Persistent high score saved to `%LOCALAPPDATA%\pytris\highscore.txt`
- Pause, block swap, and fast drop controls
- Sound effects and background music

## Requirements

- Python 3.8+
- `pygame`

## Installation

1. Install Python if needed.
2. Install the required dependency(s):

```powershell
pip install requirements.txt
```

## Running the Game

From the project root:

```powershell
python __main__.py
```

Building into an exe:
- Run `build.bat` and executable will be generated in dist/PyTris.exe

## Controls

- `left arrow` or `A`: Move block left
- `right arrow` or `D`: Move block right
- `down arrow` or `S`: Move block down
- `up arrow` or `W`: Rotate block
- `Space`: Hard drop / restart after game over
- `C`: Swap current block with the hold block
- `R`: Reset the game
- `P`: Pause / unpause
- `Esc`: Exit

## Notes

- The game uses `pygame` for rendering, audio, and event handling.
- High score data is managed by `src/core/backend.py` and stored in the local app data folder.
- The game currently plays background music and uses sound effect assets from `assets/sounds/`.