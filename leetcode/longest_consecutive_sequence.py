class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        seen = set(nums)

        max_streak = 0

        for num in nums:
            if num-1 not in seen:
                cur_streak = 1
                while num+cur_streak not in seen:
                    cur_streak += 1
                max_streak = max(max_streak, cur_streak)
        return max_streak
            
