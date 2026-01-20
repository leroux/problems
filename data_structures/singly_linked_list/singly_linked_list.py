class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = ListNode()

    def append(self, val):
        new_node = ListNode(val)

        node = self.head
        while node:
            if node.next is None:
                break
            node = node.next
        node.next = new_node

    def prepend(self, val):
        new_real_head = ListNode(val)
        new_real_head.next = self.head.next
        self.head.next = new_real_head

    def insert(self, index, val):
        new_node = ListNode(val)
        
        prev = self.head
        i = 0
        while prev:
            # get node before index to insert at
            if i == index:
                new_node.next = prev.next
                prev.next = new_node
                return
            prev = prev.next
            i += 1

        raise IndexError

    def delete(self, index):
        node = self.head
        i = 0
        while node:
            # get node before index to delete
            if i == index:
                if not node.next:
                    raise IndexError
                val = node.next.val
                node.next = node.next.next
                return val
            node = node.next
            i += 1

        raise IndexError


    def get(self, index):
        node = self.head.next
        i = 0
        while node:
            if i == index:
                return node.val
            node = node.next
            i += 1
        raise IndexError

    def find(self, val):
        node = self.head.next
        i = 0
        while node:
            if node.val == val:
                return i
            node = node.next
            i += 1
        return -1

    def size(self):
        node = self.head.next
        i = 0
        while node:
            node = node.next
            i += 1
        return i

    def is_empty(self):
        return not self.head.next

    def to_list(self):
        l = []
        node = self.head.next
        while node:
            l.append(node.val)
            node = node.next
        return l
