# class Solution:
#     def topKFrequent(self, nums: List[int], k: int) -> List[int]:
#         # count occurrences
#         counts: dict[int, int] = {}
#         for num in nums:
#             if num in counts:
#                 counts[num] += 1
#             else:
#                 counts[num] = 1

#         # make list of tuples sorted by count
#         counts_asc = sorted(counts.items(), key=lambda t: t[1])

#         top_k: List[int] = []
#         for i in range(1, k+1):
#             top_k.append(counts_asc[-i][0])

#         return top_k

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # count occurrences
        counts: dict[int, int] = {}
        for num in nums:
            counts[num] = 1 + counts.get(num, 0)

        heap: List[int] = []
        for num, count in counts.items():
            heapq.heappush(heap, (count, num))
            if len(heap) > k:
                heapq.heappop(heap)

        top_k = []
        for _ in range(k):
            top_k.append(heapq.heappop(heap)[1])
        return top_k
