import unittest
from wordfinder import SpecialWordFinder

class TestSpecialWordFinder(unittest.TestCase):
    def setUp(self):
        # Create a test file with some words, blank lines, and comments
        self.test_file = 'test_words.txt'
        with open(self.test_file, 'w') as file:
            file.write("apple\n")
            file.write("\n")  # Blank line
            file.write("# Comment\n")
            file.write("banana\n")
            file.write("cherry\n")

    def tearDown(self):
        # Remove the test file after the test
        import os
        os.remove(self.test_file)

    def test_read_words(self):
        # Initialize SpecialWordFinder with the test file
        word_finder = SpecialWordFinder(self.test_file)
        # Ensure that the words list does not contain blank lines or comments
        self.assertEqual(word_finder.words, ['apple', 'banana', 'cherry'])

    def test_random(self):
        # Initialize SpecialWordFinder with the test file
        word_finder = SpecialWordFinder(self.test_file)
        # Ensure that the random method returns a word from the words list
        self.assertIn(word_finder.random(), ['apple', 'banana', 'cherry'])

if __name__ == '__main__':
    unittest.main()