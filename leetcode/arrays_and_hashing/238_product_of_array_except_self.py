'''
maybe 2 passes? multiply going forward then back?
then can figure out how to remove self from the equation

[1,2,4,6]

0: _*2*4*6
1: 1*_*4*6
2: 1*2*_*6
3: 1*2*4*_
'''

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        products = [1 for _ in range(len(nums))]
        for i in range(1, len(nums)):
            products[i] = products[i-1] * nums[i-1]

        products2 = [1 for _ in range(len(nums))]
        for i in range(len(nums)-2, -1, -1):
            products2[i] = products2[i+1] * nums[i+1] 
     
        products = [products[i]*products2[i] for i in range(len(products))]

        return products

