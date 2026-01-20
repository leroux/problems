class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, val):
        new_node = ListNode(val)

        if self.head is None:
            self.head = new_node
            return

        node = self.head
        while node:
            if node.next is None:
                break
            node = node.next
        node.next = new_node

    def prepend(self, val):
        new_head = ListNode(val)
        new_head.next = self.head
        self.head = new_head

    def insert(self, index, val):
        new_node = ListNode(val)
        
        if index == 0:
            new_node.next = self.head
            self.head = new_node
            return

        node = self.head
        i = 0
        while node:
            # get node before index to insert at
            if i == index - 1:
                new_node.next = node.next
                node.next = new_node
                return
            node = node.next
            i += 1

        raise IndexError

    def delete(self, index):
        if self.head is None:
            raise IndexError

        if index == 0:
            val = self.head.val
            self.head = self.head.next
            return val

        node = self.head
        i = 0
        while node:
            # get node before index to delete
            if i == index - 1:
                val = node.next.val
                node.next = node.next.next
                return val
            node = node.next
            i += 1

        raise IndexError


    def get(self, index):
        node = self.head
        i = 0
        while node:
            if i == index:
                return node.val
            node = node.next
            i += 1
        raise IndexError

    def find(self, val):
        node = self.head
        i = 0
        while node:
            if node.val == val:
                return i
            node = node.next
            i += 1
        return -1

    def size(self):
        node = self.head
        i = 0
        while node:
            node = node.next
            i += 1
        return i

    def is_empty(self):
        return not self.head

    def to_list(self):
        l = []
        node = self.head
        while node:
            l.append(node.val)
            node = node.next
        return l
