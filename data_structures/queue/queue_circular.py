class QueueCircular:
    def __init__(self, capacity):
        """Initialize circular queue with given capacity"""
        self.data = [None] * capacity
        self.head = 0
        self.tail = 0

    def enqueue(self, val):
        """Add item to back of queue. Raise exception if full."""
        cap = len(self.data)
        front_idx = self.head % len(self.data)
        if (self.tail + 1) % cap == front_idx:
            raise IndexError
        idx = self.tail % len(self.data)
        self.data[idx] = val
        self.tail += 1

    def dequeue(self):
        """Remove and return item from front of queue. Raise exception if empty."""
        if self.head == self.tail:
            raise IndexError
        idx = self.head % len(self.data)
        val = self.data[idx]
        self.data[idx] = None
        self.head += 1
        return val

    def front(self):
        """Return front item without removing. Raise exception if empty."""
        if self.head == self.tail:
            raise IndexError
        front_idx = self.head % len(self.data)
        return self.data[front_idx]

    def is_empty(self):
        """Return True if queue is empty"""
        return self.head == self.tail

    def is_full(self):
        """Return True if queue is full"""
        cap = len(self.data)
        front_idx = self.head % cap
        return (self.tail + 1) % cap == front_idx

    def size(self):
        """Return number of items in queue"""
        return self.tail - self.head

    def capacity(self):
        """Return maximum capacity of queue"""
        return len(self.data)

    def to_list(self):
        """Convert to Python list (front to back)"""
        front_idx = self.head % len(self.data)
        back_idx = self.tail % len(self.data)
        if self.head == self.tail:
            return []
        if back_idx > front_idx:
            return self.data[front_idx:back_idx]
        else:
            return self.data[front_idx:] + self.data[:back_idx]