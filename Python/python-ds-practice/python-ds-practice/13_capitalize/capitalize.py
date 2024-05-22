def capitalize(phrase):
    """Capitalize first letter of first word of phrase.

        >>> capitalize('python')
        'Python'

        >>> capitalize('only first word')
        'Only first word'
    """
    words = phrase.split()
    if len(words) > 0:
        first_word = words[0]
        capitalized = first_word.capitalize() + ' '.join(words[1:])
        return capitalized
    return phrase.capitalize()