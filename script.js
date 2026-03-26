const boardElement = document.querySelector("#board");
const statusMessageElement = document.querySelector("#statusMessage");
const resetButton = document.querySelector("#resetButton");
const cellElements = Array.from(document.querySelectorAll(".cell"));

const winningLines = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6],
];

let board = Array(9).fill("");
let currentPlayer = "X";
let gameFinished = false;

function updateStatus(message) {
  statusMessageElement.textContent = message;
}

function renderBoard() {
  cellElements.forEach((cell, index) => {
    const value = board[index];
    cell.textContent = value;
    cell.dataset.value = value;
    cell.classList.remove("winning");
    cell.disabled = gameFinished || value !== "";
  });
}

function findWinningLine() {
  return winningLines.find(([a, b, c]) => {
    return board[a] && board[a] === board[b] && board[a] === board[c];
  });
}

function markWinningLine(line) {
  line.forEach((index) => {
    cellElements[index].classList.add("winning");
  });
}

function handleMove(index) {
  if (gameFinished || board[index]) {
    return;
  }

  board[index] = currentPlayer;

  const winningLine = findWinningLine();
  if (winningLine) {
    gameFinished = true;
    renderBoard();
    markWinningLine(winningLine);
    updateStatus(`Player ${currentPlayer} wins`);
    return;
  }

  if (board.every((cell) => cell)) {
    gameFinished = true;
    renderBoard();
    updateStatus("Draw game");
    return;
  }

  currentPlayer = currentPlayer === "X" ? "O" : "X";
  renderBoard();
  updateStatus(`Player ${currentPlayer}'s turn`);
}

function resetGame() {
  board = Array(9).fill("");
  currentPlayer = "X";
  gameFinished = false;
  renderBoard();
  updateStatus("Player X starts");
}

boardElement.addEventListener("click", (event) => {
  const cell = event.target.closest(".cell");
  if (!cell) {
    return;
  }

  handleMove(Number(cell.dataset.cellIndex));
});

resetButton.addEventListener("click", resetGame);

renderBoard();
