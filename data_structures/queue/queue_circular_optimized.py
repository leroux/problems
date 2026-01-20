class QueueCircularOptimized:
    def __init__(self, capacity):
        """Initialize circular queue with power-of-2 capacity for bitwise optimization"""
        # Round up to next power of 2
        self.capacity = 1
        while self.capacity < capacity:
            self.capacity <<= 1

        self.data = [None] * self.capacity
        self.mask = self.capacity - 1  # For bitwise AND operations
        self.head = 0
        self.tail = 0

    def enqueue(self, val):
        """Add item to back of queue. Raise exception if full."""
        # Use bitwise AND instead of modulo
        if (self.tail + 1) & self.mask == self.head & self.mask:
            raise IndexError("Queue is full")

        self.data[self.tail & self.mask] = val
        self.tail += 1

    def dequeue(self):
        """Remove and return item from front of queue. Raise exception if empty."""
        if self.head == self.tail:
            raise IndexError("Queue is empty")

        val = self.data[self.head & self.mask]
        self.data[self.head & self.mask] = None  # Clean up reference
        self.head += 1
        return val

    def front(self):
        """Return front item without removing. Raise exception if empty."""
        if self.head == self.tail:
            raise IndexError("Queue is empty")
        return self.data[self.head & self.mask]

    def is_empty(self):
        """Return True if queue is empty"""
        return self.head == self.tail

    def is_full(self):
        """Return True if queue is full"""
        return (self.tail + 1) & self.mask == self.head & self.mask

    def size(self):
        """Return number of items in queue"""
        return self.tail - self.head

    def capacity_actual(self):
        """Return actual capacity (power of 2)"""
        return self.capacity

    def capacity_effective(self):
        """Return effective capacity (actual - 1 due to waste one slot)"""
        return self.capacity - 1

    def to_list(self):
        """Convert to Python list (front to back)"""
        if self.head == self.tail:
            return []

        result = []
        current = self.head
        while current != self.tail:
            result.append(self.data[current & self.mask])
            current += 1
        return result