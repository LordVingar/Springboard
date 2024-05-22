def same_frequency(num1, num2):
    """Do these nums have same frequencies of digits?
    
        >>> same_frequency(551122, 221515)
        True
        
        >>> same_frequency(321142, 3212215)
        False
        
        >>> same_frequency(1212, 2211)
        True
    """
        # Convert numbers to strings
    str_num1 = str(num1)
    str_num2 = str(num2)
    
    # Create dictionaries to store digit frequencies
    freq1 = {}
    freq2 = {}
    
    # Count digit frequencies in num1
    for digit in str_num1:
        freq1[digit] = freq1.get(digit, 0) + 1
        
    # Count digit frequencies in num2
    for digit in str_num2:
        freq2[digit] = freq2.get(digit, 0) + 1
        
    # Compare the dictionaries
    return freq1 == freq2