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

// Counter for matched pairs
let matchedPairs = 0;

// Initialize firstCard
let firstCard = null;

// Variable to track if cards are being matched
let matching = false;

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

// Shuffle the COLORS array
let shuffledColors = shuffle(COLORS);

// Function to create divs with colors for each card and attach click event listener
function createDivsForColors(colorArray) {
  for (let color of colorArray) {
    const newDiv = document.createElement("div");
    newDiv.classList.add(color);
    newDiv.addEventListener("click", handleCardClick);
    gameContainer.append(newDiv);
  }
}

// Function to handle card clicks
function handleCardClick(event) {
  const selectedCard = event.target;

  // Ignore clicks on already matched cards or on the same card twice
  if (
    selectedCard.classList.contains("flipped") ||
    selectedCard === firstCard ||
    matching
  ) {
    return;
  }

  selectedCard.style.backgroundColor = selectedCard.classList[0];

  if (!firstCard) {
    // This is the first card clicked
    firstCard = selectedCard;
  } else {
    // This is the second card clicked
    if (selectedCard.classList[0] === firstCard.classList[0]) {
      // It's a match!
      matching = true;
      matchedPairs++;

      // Mark both cards as matched
      selectedCard.classList.add("flipped");
      firstCard.classList.add("flipped");

      // Check if all pairs are matched
      if (matchedPairs === COLORS.length / 2) {
        alert("Congratulations! You've matched all the pairs.");
        resetGame();
      }

      // Reset the firstCard variable for the next turn
      firstCard = null;
      matching = false;
    } else {
      // It's not a match, reset the cards after a short delay
      setTimeout(() => {
        selectedCard.style.backgroundColor = "";
        firstCard.style.backgroundColor = "";
        matching = false;
        firstCard = null;
      }, 1000);
    }
  }
}

// Function to reset the game
function resetGame() {
  matchedPairs = 0;
  // Remove the "flipped" class from all cards
  document.querySelectorAll(".flipped").forEach(card => card.classList.remove("flipped"));
  // Reshuffle the colors and recreate the cards
  shuffledColors = shuffle(COLORS);
  gameContainer.innerHTML = "";
  createDivsForColors(shuffledColors);
}

// Initial setup: create divs for colors and set up click event listeners
createDivsForColors(shuffledColors);