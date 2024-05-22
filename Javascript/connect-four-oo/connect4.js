// Player class with a constructor to store the player's color
class Player {
  constructor(color) {
    this.color = color;
  }
}

// Game class with constructor to set initial game state and dimensions
class Game {
  constructor(height, width) {
    this.height = height;
    this.width = width;
    this.currPlayer = null;
    this.players = [null, null]; // Player 1 and Player 2
    this.board = [];
    this.gameStarted = false;
    this.initGame();
  }

  // Initialize the game, add event listener to the start button
  initGame() {
    const startButton = document.getElementById('start-button');
    startButton.addEventListener('click', () => this.startGame());

    // Additional initialization logic can be added here. Put at bottom so it starts new game on reset.
  }

  // Start the game, set player colors, initialize the board, and mark game as started
  startGame() {
    const player1Color = document.getElementById('player1Color').value;
    const player2Color = document.getElementById('player2Color').value;

    this.players[0] = new Player(player1Color);
    this.players[1] = new Player(player2Color);

    this.currPlayer = this.players[0];
    this.board = [];
    this.makeBoard();
    this.makeHtmlBoard();
    this.gameStarted = true;
  }

  // Create the game board array
  makeBoard() {
    for (let y = 0; y < this.height; y++) {
      this.board.push(Array.from({ length: this.width }));
    }
  }

  // Create the HTML game board, including clickable column tops
  makeHtmlBoard() {
    const boardElement = document.getElementById('board');
    boardElement.innerHTML = '';

    const top = document.createElement('tr');
    top.setAttribute('id', 'column-top');
    top.addEventListener('click', this.handleClick.bind(this));

    for (let x = 0; x < this.width; x++) {
      const headCell = document.createElement('td');
      headCell.setAttribute('id', x);
      top.append(headCell);
    }

    boardElement.append(top);

    for (let y = 0; y < this.height; y++) {
      const row = document.createElement('tr');

      for (let x = 0; x < this.width; x++) {
        const cell = document.createElement('td');
        cell.setAttribute('id', `${y}-${x}`);
        row.append(cell);
      }

      boardElement.append(row);
    }
  }

  // Find the top empty row in a given column
  findSpotForCol(x) {
    for (let y = this.height - 1; y >= 0; y--) {
      if (!this.board[y][x]) {
        return y;
      }
    }
    return null;
  }

  // Place a piece in the HTML table and update the board
  placeInTable(y, x) {
    const piece = document.createElement('div');
    piece.classList.add('piece');
    piece.style.backgroundColor = this.currPlayer.color;
  
    const spot = document.getElementById(`${y}-${x}`);
    spot.append(piece);
  }

  // Display an alert with the game result and mark game as ended
  endGame(msg) {
    alert(msg);
    this.gameStarted = false;
  }

  // Reset the game to the initial state
  resetGame() {
    this.currPlayer = this.players[0];
    this.board = [];
    this.makeBoard();
    const boardElement = document.getElementById('board');
    boardElement.innerHTML = '';
    this.makeHtmlBoard();
    this.gameStarted = true;
  }

  // Handle click events on the column tops to make a move
  handleClick(evt) {
    if (!this.gameStarted) {
      alert('Please start the game first!');
      return;
    }

    const x = +evt.target.id;
    const y = this.findSpotForCol(x);
    if (y === null) {
      return;
    }

    this.board[y][x] = this.currPlayer;
    this.placeInTable(y, x);

    if (this.checkForWin()) {
      return this.endGame(`Player ${this.currPlayer.color} won!`);
    }

    if (this.board.every(row => row.every(cell => cell))) {
      return this.endGame('Tie!');
    }

    this.currPlayer = this.currPlayer === this.players[0] ? this.players[1] : this.players[0];
  }

  // Check if the current player has won
  checkForWin() {
    function _win(cells) {
      return cells.every(
        ([y, x]) =>
          y >= 0 &&
          y < this.height &&
          x >= 0 &&
          x < this.width &&
          this.board[y][x] === this.currPlayer
      );
    }

    for (let y = 0; y < this.height; y++) {
      for (let x = 0; x < this.width; x++) {
        const horiz = [[y, x], [y, x + 1], [y, x + 2], [y, x + 3]];
        const vert = [[y, x], [y + 1, x], [y + 2, x], [y + 3, x]];
        const diagDR = [[y, x], [y + 1, x + 1], [y + 2, x + 2], [y + 3, x + 3]];
        const diagDL = [[y, x], [y + 1, x - 1], [y + 2, x - 2], [y + 3, x - 3]];

        if (
          _win.call(this, horiz) ||
          _win.call(this, vert) ||
          _win.call(this, diagDR) ||
          _win.call(this, diagDL)
        ) {
          return true;
        }
      }
    }

    return false;
  }
}

// Create a new game instance with dimensions 6x7
new Game(6, 7);