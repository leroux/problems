"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        # insert copies after originals keeping copy.random pointed at originals
        cur = head
        while cur:
            copy = Node(cur.val, cur.next, cur.random)
            cur.next = copy
            cur = cur.next.next
        
        # update copy.random to next node
        cur = head
        while cur:
            copy = cur.next
            if copy.random:
                copy.random = copy.random.next
            cur = cur.next.next
        
        # separate into 2 lists: original and copy
        cur = dummy = Node(0, head, None)
        while cur:
            tmp = cur.next
            if cur.next:
                cur.next = cur.next.next
            else:
                break
            cur = tmp

        return dummy.next