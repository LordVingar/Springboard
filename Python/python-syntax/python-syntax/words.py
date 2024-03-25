def print_upper_words(words, must_start_with=None):
    """Prints each word from a list on a separate line in all uppercase.

    If `must_start_with` is provided, only words starting with those letters are printed.
    """
    for word in words:
        if must_start_with is None or any(word.lower().startswith(letter) for letter in must_start_with):
            print(word.upper())

# Test the function
print_upper_words(["hello", "hey", "goodbye", "yo", "yes"])  # Should print HELLO, HEY, YO, YES
print_upper_words(["hello", "hey", "goodbye", "yo", "yes"], must_start_with={"h", "y"})  # Should print HELLO, HEY, YO, YES
print_upper_words(["hello", "apple", "Elephant", "Egg"], {"e", "a"})  # Should print Elephant, Egg, apple