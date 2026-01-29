# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        slow, fast = head, head.next

        # find midpoint to split list
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # 2nd half is after slow
        l2 = slow.next
        # disconnect the halves
        slow.next = None

        # reverse 2nd half in place
        prev = None
        while l2:
            l2.next, prev, l2 = prev, l2, l2.next

        # merge the halves
        l1, l2 = head, prev
        while l2:
            tmp1, tmp2 = l1.next, l2.next
            l1.next = l2
            l2.next = tmp1
            l1 = tmp1
            l2 = tmp2