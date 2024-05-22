console.log("Let's get this party started!");

const apiKey = 'oLwF1ba5yG4IoBOzOza7BINXnYa66Hnt';

document.getElementById('searchForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the search term from the input field
    const searchTerm = document.getElementById('searchTerm').value;

    try {
        const response = await axios.get(`https://api.giphy.com/v1/gifs/search?api_key=${apiKey}&q=${searchTerm}&limit=1&offset=0&rating=g&lang=en&bundle=messaging_non_clips`);
        appendGif(response.data.data[0].images.original.url);
    } catch (error) {
        // Handle any errors
        console.error(error);
    }

});

document.getElementById('clearButton').addEventListener('click', function() {
    const gifsContainer = document.getElementById('gifContainer');
    gifsContainer.innerHTML = '';
    return false; // Prevent page reload
});

function appendGif(gifUrl) {
    // Create img element for the GIF
    const img = document.createElement('img');
    img.src = gifUrl;

    // Append the img element to the gifContainer
    const gifContainer = document.getElementById('gifContainer');
    gifContainer.appendChild(img);
}