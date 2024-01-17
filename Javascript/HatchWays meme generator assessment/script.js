// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function() {
    // Get references to the form and meme container elements
    const memeForm = document.getElementById('memeForm');
    const memeContainer = document.getElementById('memeContainer');

    // Event listener for the form submission
    memeForm.addEventListener('submit', function(event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        // Get the values from the form inputs
        const topText = document.getElementById('topText').value;
        const bottomText = document.getElementById('bottomText').value;
        const imageUrl = document.getElementById('imageUrl').value;

                // Check if the URL is valid before creating the meme
                if (isValidUrl(imageUrl)) {
                    createMeme(imageUrl, topText, bottomText);
                    memeForm.reset();
                } else {
                    alert('Invalid URL. Please enter a valid URL.');
                }

        // Call the function to create and display a new meme
        createMeme(imageUrl, topText, bottomText);

        // Reset the form fields after meme creation
        memeForm.reset();
    });

    // Event listener for the meme container to handle meme deletion
    memeContainer.addEventListener('click', function(event) {
        // Check if the clicked element has the 'delete-button' class
        if (event.target.classList.contains('delete-button')) {
            // Remove the parent element (meme) when the delete button is clicked
            event.target.parentElement.remove();
        }
    });

    // Function to create a new meme element with image, top text, bottom text, and delete button
    function createMeme(imageUrl, topText, bottomText) {
        // Create a new div element for the meme
        const meme = document.createElement('div');
        meme.classList.add('meme');

        // Create a div to contain the image and text elements
        const imageContainer = document.createElement('div');
        imageContainer.classList.add('imageContainer');

        // Create an image element and set its source
        const img = document.createElement('img');
        img.src = imageUrl;
        imageContainer.appendChild(img);

        // Create div elements for top and bottom text, set their text content
        const topTextDiv = document.createElement('div');
        topTextDiv.classList.add('topText');
        topTextDiv.innerText = topText;
        imageContainer.appendChild(topTextDiv);

        const bottomTextDiv = document.createElement('div');
        bottomTextDiv.classList.add('bottomText');
        bottomTextDiv.innerText = bottomText;
        imageContainer.appendChild(bottomTextDiv);

        // Append the image container to the meme
        meme.appendChild(imageContainer);

        // Create a delete button and append it to the meme
        const deleteButton = document.createElement('button');
        deleteButton.classList.add('delete-button');
        deleteButton.innerText = 'Delete';
        meme.appendChild(deleteButton);

        // Append the meme to the meme container
        memeContainer.appendChild(meme);
    }
});
