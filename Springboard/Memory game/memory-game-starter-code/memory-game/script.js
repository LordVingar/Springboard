// Array of colors for the cards
const COLORS = [
  "red",
  "blue",
  "green",
  "orange",
  "purple",
  "red",
  "blue",
  "green",
  "orange",
  "purple"
];

// Reference to the game container in the HTML
const gameContainer = document.getElementById("game");

let previousTile = undefined;

let timer = undefined;

// Function to shuffle an array using the Fisher-Yates algorithm
function shuffle(array) {
  let counter = array.length;

  while (counter > 0) {
    let index = Math.floor(Math.random() * counter);
    counter--;
    let temp = array[counter];
    array[counter] = array[index];
    array[index] = temp;
  }

  return array;
}


const isPaired = element => element.getAttribute('data-paired') === 'true';
const pair = element => element.setAttribute('data-paired', true);
const unpair = element => element.setAttribute('data-paired', false);
const matching = (first, second) => first.style.backgroundColor === second.style.backgroundColor
const isTileShowing = (element) => element.getAttribute('data-facing-up') === 'true'
const showTile = (element) => element.setAttribute('data-facing-up', true)
const hideTile = (element) => {
  if (isPaired(element) === false)
    element.setAttribute('data-facing-up', false)
}

const isGameWon = () => [...gameContainer.children].every(isPaired);

// Function to create divs with colors for each card and attach click event listener
function createDivsForColors(colorArray) {
  for (let color of colorArray) {
    const newDiv = document.createElement("div");
    hideTile(newDiv);
    unpair(newDiv)
    newDiv.style.backgroundColor = color;
    newDiv.addEventListener("click", handleCardClick);
    gameContainer.append(newDiv);
  }
}

// Function to handle card clicks
function handleCardClick(event) {
  const selected = event.target;

  // if tile is solved already take no action
  if (isPaired(selected) === true) return;

  // if tile is showing already take no action
  if (isTileShowing(selected) === true) return;

  // timer engaged
  if (timer !== undefined) return;

  // show tile
  showTile(selected);

  // if no other is showing
  if (previousTile === undefined) {
    previousTile = selected;
    return;
  }

  if (matching(previousTile, selected) === true) {
    pair(previousTile);
    pair(selected);
    previousTile = undefined;
    if (isGameWon() === true) {
      alert("Congratulations! You've matched all the pairs.");
      resetGame();
    }
    return;
  }
  timer = setTimeout(() => {
    hideTile(previousTile);
    previousTile = undefined
    hideTile(selected);
    clearTimeout(timer);
    timer = undefined;
  }, 1000);
}

// Function to reset the game
function resetGame() {
  matchedPairs = 0;
  gameContainer.innerHTML = "";
  // Reshuffle the colors and recreate the cards
  shuffledColors = shuffle(COLORS);
  gameContainer.innerHTML = "";
  createDivsForColors(shuffledColors);
}

resetGame()