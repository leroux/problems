class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        number_to_index = {}
        for i in range(len(numbers)):
            complement = target - numbers[i]
            if number_to_index[complement]:
                return [i+1, number_to_index[complement]+1]
            number_to_index[numbers[i]] = i
        return []
            
