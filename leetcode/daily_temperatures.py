class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        stack = []
        res = [0 for _ in temperatures]
        for i, t in enumerate(temperatures):
            while stack and t > stack[-1][0]:
                _, prev_idx = stack.pop()
                res[prev_idx] = i - prev_idx
            stack.append((t, i))
        return res
