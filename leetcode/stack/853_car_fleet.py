class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        pairs = [(p, s) for p, s in zip(position, speed)]
        # closest to target first
        pairs.sort(reverse=True)
        
        fleets = 1

        # target = p + s * t. solve for t
        # target - p = st
        # t = (target - p) / s

        p = pairs[0][0]
        s = pairs[0][1]
        prev_time = (target - p) / s
        for p, s in pairs[1:]:
            t = (target - p) / s
            if t > prev_time:
                # new fleet
                fleets += 1
                prev_time = t

        return fleets

