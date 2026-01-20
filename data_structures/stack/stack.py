class StackNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None


class Stack:
    def __init__(self):
        # dummy head
        self.head = StackNode()

    def push(self, val):
        """Add element to top of stack"""
        new_head = StackNode(val)
        new_head.next = self.head.next
        self.head.next = new_head

    def pop(self):
        """Remove and return top element. Raise exception if empty."""
        if self.head.next is None:
            raise IndexError
        val = self.head.next.val
        self.head.next = self.head.next.next
        return val

    def peek(self):
        """Return top element without removing. Raise exception if empty."""
        if self.head.next is None:
            raise IndexError
        return self.head.next.val

    def is_empty(self):
        """Return True if stack is empty"""
        return self.head.next is None

    def size(self):
        """Return number of elements in stack"""
        i = 0
        node = self.head.next
        while node:
            i += 1
            node = node.next
        return i

    def to_list(self):
        """Convert to Python list (top to bottom)"""
        l = []
        node = self.head.next
        while node:
            l.append(node.val)
            node = node.next
        return l

