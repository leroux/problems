class QueueNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None


class QueueLinked:
    def __init__(self):
        self.dummy_head = QueueNode()
        self.tail = self.dummy_head

    def enqueue(self, val):
        """Add item to back of queue"""
        new_node = QueueNode(val)
        self.tail.next = new_node
        self.tail = new_node

    def dequeue(self):
        """Remove and return item from front of queue. Raise exception if empty."""
        head = self.dummy_head.next
        if head is None:
            raise IndexError
        val = head.val
        self.dummy_head.next = head.next
        if self.dummy_head.next is None:
            self.tail = self.dummy_head
        return val

    def front(self):
        """Return front item without removing. Raise exception if empty."""
        head = self.dummy_head.next
        if head is None:
            raise IndexError
        return head.val

    def is_empty(self):
        """Return True if queue is empty"""
        head = self.dummy_head.next
        return head is None

    def size(self):
        """Return number of items in queue"""
        i = 0
        node = self.dummy_head.next
        while node:
            node = node.next
            i += 1
        return i

    def to_list(self):
        """Convert to Python list (front to back)"""
        l = []
        node = self.dummy_head.next
        while node:
            l.append(node.val)
            node = node.next
        return l

