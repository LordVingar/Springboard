def number_compare(a, b):
    """Report on whether a>b, b>a, or b==a
    
        >>> number_compare(1, 1)
        'Numbers are equal'
        
        >>> number_compare(-1, 1)
        'Second is greater'
        
        >>> number_compare(1, -2)
        'First is greater'
    """
    if a < b:
        print(f"{a} is less than {b}")
    elif a > b:
        print(f"{a} is greater than {b}")
    else:
        print("Numbers are equal")