class Solution:
    def isValid(self, s: str) -> bool:
        mp = {')': '(', '}': '{', ']': '['}
        st = []
        for c in s:
            # push if opener
            if c in '({[':
                st.append(c)
            # if closer, check if associated opener on stack
            # and pop opener off
            elif c in ')}]':
                if not st or st.pop() != mp[c]:
                    return False
            # should never hit
            else:
                raise ValueException
        # check no unclosed openers left
        if st:
            return False
        return True
