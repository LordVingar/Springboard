// When dome is ready console.log "Lets get ready to party with jQuery"
$(document).ready(function() {
    console.log('Lets get ready to party with jQuery!');

// Give all images inside of an article tag the class of image-center
$('article img').addClass('image-center');

// Remove the last paragraph in the article.
$('article p:last-child').remove();

// Select the title element using jQuery
let $title = $('h1');

// Generate a random font size between 0 and 100 pixels
let randomFontSize = Math.floor(Math.random() * 101); // Generates a random number from 0 to 100

// Set the font size of the title element to the random value
$title.css('font-size', randomFontSize + 'px');

//Adding something to the article
$('ul').append('<li>I hope we\'re having lots of fun with jQuery</li>');

//removing the list

    // Select the aside element and empty its contents
    $('aside').empty();
    
    // Create a new paragraph element with the apology text
    const apologyParagraph = $('<p>').text('We apologize for the existence of the list.');
    
    // Append the paragraph to the aside element
    $('aside').append(apologyParagraph);

// Function to update the background color
function updateBackgroundColor() {
        const red = parseInt($('#red').val());
        const blue = parseInt($('#blue').val());
        const green = parseInt($('#green').val());
        
        // Set the background color based on the input values
        $('body').css('background-color', `rgb(${red}, ${green}, ${blue})`);
    }

    // Call the function initially
    updateBackgroundColor();

    // Listen for changes in the input values
    $('#red, #blue, #green').on('input', function() {
        updateBackgroundColor();
    });

// Attach click event listener to all images
$('img').on('click', function() {
    // Remove the clicked image from the DOM
    $(this).remove();
});
});