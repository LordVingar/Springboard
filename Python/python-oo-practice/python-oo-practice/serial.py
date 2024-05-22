"""Python serial number generator."""

class SerialGenerator:
    """Machine to create unique incrementing serial numbers.
    
    >>> serial = SerialGenerator(start=100)

    >>> serial.generate()
    100

    >>> serial.generate()
    101

    >>> serial.generate()
    102

    >>> serial.reset()

    >>> serial.generate()
    100
    """
    def __init__(self, start=0):
        """Initialize a new SerialGenerator with a starting value."""
        self.start = start
        self.next_serial = start
    
    def generate(self):
        """Return the next serial number."""
        serial = self.next_serial
        self.next_serial += 1
        return serial
    
    def reset(self):
        """Reset the serial number to the starting value."""
        self.next_serial = self.start
    def __repr__(self):
        """Return a string representation of the SerialGenerator."""
        return f"SerialGenerator(start={self.start})"

