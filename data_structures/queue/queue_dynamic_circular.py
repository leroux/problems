class QueueDynamicCircular:
    def __init__(self, initial_capacity=8):
        # pick nearest square so we can use
        # bitwise math instead of modulus
        self.capacity = 1
        while self.capacity < initial_capacity:
            self.capacity <<= 1

        self.data = [None for _ in range(self.capacity)]
        self.head = self.tail = 0
        self.size_val = 0

    def _resize(self):
        old_capacity = self.capacity
        old_data = self.data
        self.capacity <<= 1
        self.data = [None for _ in range(self.capacity)]

        # Copy elements directly without intermediate list
        if self.head <= self.tail:
            # No wraparound case
            self.data[:self.size_val] = old_data[self.head:self.tail]
        else:
            # Wraparound case - copy in two parts
            first_part_size = old_capacity - self.head
            self.data[:first_part_size] = old_data[self.head:]
            self.data[first_part_size:self.size_val] = old_data[:self.tail]

        self.head = 0
        self.tail = self.size_val

    def enqueue(self, val):
        if self.size_val == self.capacity - 1:
            self._resize()
        self.data[self.tail] = val
        self.tail = (self.tail + 1) & (self.capacity - 1)
        self.size_val += 1

    def dequeue(self):
        if self.size_val == 0:
            raise IndexError
        val = self.data[self.head]
        self.data[self.head] = None
        self.head = (self.head + 1) & (self.capacity - 1)
        self.size_val -= 1
        return val

    def front(self):
        if self.size_val == 0:
            raise IndexError
        return self.data[self.head]

    def is_empty(self):
        return self.size_val == 0

    def size(self):
        return self.size_val

    def to_list(self):
        l = []
        if self.head <= self.tail:
            l.extend(self.data[self.head:self.tail])
        else:
            l.extend(self.data[self.head:])
            l.extend(self.data[:self.tail])
        return l
