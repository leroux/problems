class Solution:
    def trap(self, height: List[int]) -> int:
        max_forwards = []
        max_ = 0
        for h in height:
            max_ = max(max_, h)
            max_forwards.append(max_)

        max_backwards = []
        max_ = 0
        for h in reversed(height):
            max_ = max(max_, h)
            max_backwards.append(max_)
        max_backwards = list(reversed(max_backwards))

        mins = []
        for i in range(len(height)):
            mins.append(min(max_forwards[i], max_backwards[i]))

        sub = [m - h for (m, h) in zip(mins, height)]

        return sum(sub)
