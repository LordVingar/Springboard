const input = document.querySelector('#fruit');
const suggestions = document.querySelector('.suggestions ul');

const fruit = ['Apple', 'Apricot', 'Avocado 🥑', 'Banana', 'Bilberry', 'Blackberry', 'Blackcurrant', 'Blueberry', 'Boysenberry', 'Currant', 'Cherry', 'Coconut', 'Cranberry', 'Cucumber', 'Custard apple', 'Damson', 'Date', 'Dragonfruit', 'Durian', 'Elderberry', 'Feijoa', 'Fig', 'Gooseberry', 'Grape', 'Raisin', 'Grapefruit', 'Guava', 'Honeyberry', 'Huckleberry', 'Jabuticaba', 'Jackfruit', 'Jambul', 'Juniper berry', 'Kiwifruit', 'Kumquat', 'Lemon', 'Lime', 'Loquat', 'Longan', 'Lychee', 'Mango', 'Mangosteen', 'Marionberry', 'Melon', 'Cantaloupe', 'Honeydew', 'Watermelon', 'Miracle fruit', 'Mulberry', 'Nectarine', 'Nance', 'Olive', 'Orange', 'Clementine', 'Mandarine', 'Tangerine', 'Papaya', 'Passionfruit', 'Peach', 'Pear', 'Persimmon', 'Plantain', 'Plum', 'Pineapple', 'Pomegranate', 'Pomelo', 'Quince', 'Raspberry', 'Salmonberry', 'Rambutan', 'Redcurrant', 'Salak', 'Satsuma', 'Soursop', 'Star fruit', 'Strawberry', 'Tamarillo', 'Tamarind', 'Yuzu'];

function search(str) {
  return fruit.filter(fruitName => fruitName.toLowerCase().includes(str.toLowerCase()));
}

function searchHandler(e) {
	console.log('searchHandler called!');
  const inputVal = e.target.value.trim();
  const results = search(inputVal);
  console.log('results', results);
  showSuggestions(results, inputVal);
}

function showSuggestions(results, inputVal) {
	console.log('showSuggestions called')
  suggestions.innerHTML = '';

  if (results.length > 0) {
    results.forEach(result => {
      const listItem = document.createElement('li');
      listItem.textContent = result;
	  console.log('Created listItem:', listItem);
      suggestions.appendChild(listItem);
    });
    suggestions.classList.add('has-suggestions');
  } else {
    suggestions.classList.remove('has-suggestions');
  }
}

function useSuggestion(e) {
  if (e.target.tagName === 'LI') {
    const selectedSuggestion = e.target.textContent;
    
    // Check if the selected suggestion contains the current input value
    if (selectedSuggestion.toLowerCase().includes(input.value.toLowerCase())) {
      input.value = selectedSuggestion;
    }

    // Remove the suggestions dropdown
    suggestions.classList.remove('has-suggestions');
	        // Clear the suggestions
			suggestions.innerHTML = '';
  }
}

input.addEventListener('input', searchHandler);
suggestions.addEventListener('click', useSuggestion);
console.log('Script is loaded!');