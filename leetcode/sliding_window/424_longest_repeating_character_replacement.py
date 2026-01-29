class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        longest = 0
        count = defaultdict(lambda: 0)
        l, r = 0, 0
        while r < len(s):
            count[s[r]] += 1
            while count and r - l + 1 > max(count.values()) + k:
                count[s[l]] -= 1
                l += 1
            longest = max(longest, r - l + 1)
            r += 1
        return longest
