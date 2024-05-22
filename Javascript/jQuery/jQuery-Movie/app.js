$(document).ready(function() {
    const movieList = [];
  
    function renderMovies() {
      $('#movieList').empty();
      movieList.forEach(movie => {
        const movieItem = $('<div>').addClass('movie-item');
        const title = $('<span>').text(`Title: ${movie.title}`);
        const rating = $('<span>').text(`Rating: ${movie.rating}`);
        const removeButton = $('<button>').text('Remove').click(() => removeMovie(movie));
        movieItem.append(title, rating, removeButton);
        $('#movieList').append(movieItem);
      });
    }
  
    function addMovie(title, rating) {
      movieList.push({ title, rating });
      renderMovies();
    }
  
    function removeMovie(movie) {
      const index = movieList.indexOf(movie);
      if (index !== -1) {
        movieList.splice(index, 1);
        renderMovies();
      }
    }
  
    $('#movieForm').submit(function(event) {
      event.preventDefault();
      const title = $('#titleInput').val();
      const rating = $('#ratingInput').val();
      addMovie(title, rating);
      this.reset();
    });
  
    $('#sortByTitleAsc').click(function() {
      movieList.sort((a, b) => a.title.localeCompare(b.title));
      renderMovies();
    });
  
    $('#sortByTitleDesc').click(function() {
      movieList.sort((a, b) => b.title.localeCompare(a.title));
      renderMovies();
    });
  
    $('#sortByRatingAsc').click(function() {
      movieList.sort((a, b) => a.rating - b.rating);
      renderMovies();
    });
  
    $('#sortByRatingDesc').click(function() {
      movieList.sort((a, b) => b.rating - a.rating);
      renderMovies();
    });
  });