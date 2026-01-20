class StackArray:
    """Stack implementation using Python list"""

    def __init__(self):
        self._data = []

    def push(self, val):
        """Add element to top of stack"""
        self._data.append(val)

    def pop(self):
        """Remove and return top element. Raise exception if empty."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        """Return top element without removing. Raise exception if empty."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self):
        """Return True if stack is empty"""
        return len(self._data) == 0

    def size(self):
        """Return number of elements in stack"""
        return len(self._data)

    def to_list(self):
        """Convert to Python list (top to bottom)"""
        return self._data[::-1]  # Reverse to show top-to-bottom