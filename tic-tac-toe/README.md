# Tic-Tac-Toe

A small browser-based Tic-Tac-Toe game built with plain HTML, CSS, and JavaScript. The project runs without a build step and is designed for two players sharing the same screen.

## Project Structure

- `index.html`: Defines the game layout, status panel, 3x3 board, and reset button.
- `styles.css`: Handles the full visual design, responsive layout, and cell state styling.
- `script.js`: Manages game state, turn handling, win detection, draw detection, and reset behavior.

## How It Works

### Markup

The HTML file provides:

- A heading and subtitle for the game shell
- A status area that announces the current game state
- Nine button-based cells inside a board container
- A reset button for starting a new round

Each board cell uses a `data-cell-index` attribute so the JavaScript can map clicks to positions in the game state array.

### Styling

The CSS creates a dark glassmorphism-style interface with:

- A centered game container
- A responsive 3-column board layout
- Visual distinction between `X` and `O`
- Hover and focus states for interactive cells
- Highlighting for the winning line
- Mobile-friendly spacing and sizing adjustments

### Game Logic

The JavaScript uses a simple in-memory state model:

- `board`: an array of 9 strings representing the grid
- `currentPlayer`: tracks whether `X` or `O` moves next
- `gameFinished`: prevents further moves after a win or draw

Core behavior:

1. Clicking a cell places the current player's mark if the move is valid.
2. The script checks all possible winning combinations.
3. If a winner is found, the matching cells are highlighted and the game stops.
4. If all cells are filled without a winner, the game is declared a draw.
5. Otherwise, the turn switches to the other player.
6. Clicking `New game` resets the board and restores the initial status.

## Running the Project

Because this is a static frontend project, you can open `index.html` directly in a browser.

If you prefer serving it locally:

```bash
python3 -m http.server
```

Then open `http://localhost:8000` in your browser.

## Current Feature Set

- Two-player local gameplay
- Turn-based status messaging
- Win detection across rows, columns, and diagonals
- Draw detection
- Winning-cell highlight
- Reset button for replay
- Responsive layout for smaller screens

## Notes

- There is no AI opponent.
- There is no score tracking across rounds.
- Game state is not persisted after refresh.

## Summary

This repository is a compact example of a complete interactive web app without frameworks. The codebase is easy to follow and separated cleanly by structure (`index.html`), presentation (`styles.css`), and behavior (`script.js`).
