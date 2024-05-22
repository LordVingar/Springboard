"""Word Finder: finds random words from a dictionary."""
import random

class WordFinder:
    ...
    def __init__(self, path):
        """Initialize a WordFinder instance with a path to a file."""
        self.path = path
        self.words = self.read_words()
        print(f"{len(self.words)} words read")

    def read_words(self):
        """Read words from the file and return a list of words."""
        with open(self.path, 'r') as file:
            return [line.strip() for line in file]

    def random(self):
        """Return a random word from the list of words."""
        return random.choice(self.words)

class SpecialWordFinder(WordFinder):
    def read_words(self):
        """Read words from the file, ignoring blank lines and comments."""
        with open(self.path, 'r') as file:
            return [line.strip() for line in file if line.strip() and not line.startswith('#')]