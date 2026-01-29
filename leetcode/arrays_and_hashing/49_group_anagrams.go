func groupAnagrams(strs []string) [][]string {
    grouped := make(map[string][]string)
    for _, s := range strs {
        bt := []byte(s)
        slices.Sort(bt)
        grouped[string(bt)] = append(grouped[string(bt)], s)
    }
    res := [][]string{}
    for _, group := range grouped {
        res = append(res, group)
    }
    return res
}
