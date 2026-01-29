func twoSum(nums []int, target int) []int {
    // target - x => index of x
    cache := make(map[int]int, len(nums))

    for i, x := range nums {
        cache[target - x] = i
    }

    for j, y := range nums {
        if ix, exists := cache[y]; exists {
            if ix == j {
                continue
            }
            return []int{j, ix}
        }
    }

    return []int{}
}
