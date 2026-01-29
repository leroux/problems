# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    # iterative solution
    #
    # def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
    #     prev = None
    #     cur = head
    #     while cur:
    #         nextcur = cur.next
    #         cur.next = prev
    #         prev = cur
    #         cur = nextcur
    #     return prev

    # recursive solution
    #
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return None

        new_head = head
        if head.next:
            new_head = self.reverseList(head.next)
            head.next.next = head
        head.next = None

        return new_head