def reverse_vowels(s):
    """Reverse vowels in a string.

    Characters which re not vowels do not change position in string, but all
    vowels (y is not a vowel), should reverse their order.

    >>> reverse_vowels("Hello!")
    'Holle!'

    >>> reverse_vowels("Tomatoes")
    'Temotaos'

    >>> reverse_vowels("Reverse Vowels In A String")
    'RivArsI Vewols en e Streng'

    reverse_vowels("aeiou")
    'uoiea'

    reverse_vowels("why try, shy fly?")
    'why try, shy fly?''
    """
    vowels = set('aeiouAEIOU')
    s = list(s)
    start, end = 0, len(s) - 1
    while start < end:
        if s[start] in vowels and s[end] in vowels:
            s[start], s[end] = s[end], s[start]
            start += 1
            end -= 1
        elif s[start] not in vowels:
            start += 1
        elif s[end] not in vowels:
            end -= 1
    return ''.join(s)