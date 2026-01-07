class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        minimum = prices[0]
        max_profit = 0
        for p in prices:
            max_profit = max(max_profit, p - minimum)
            minimum = min(minimum, p)
        return max_profit
