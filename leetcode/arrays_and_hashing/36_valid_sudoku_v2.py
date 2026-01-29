class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # since domain is well-defined, we can have O(1) lookup
        # with direct addressing.
        # rs[row_index][seen_num_index]
        rs = [[False] * 9 for _ in range(9)]
        cs = [[False] * 9 for _ in range(9)]
        boxes = [[False] * 9 for _ in range(9)]

        for i in range(9):
            for j in range(9):
                val = board[i][j]
                if val == '.':
                    continue
                n = ord(val) - ord('1')
                box_idx = (i // 3) * 3 + (j // 3) 
                if rs[i][n] or cs[j][n] or boxes[box_idx][n]:
                    return False
                rs[i][n] = cs[j][n] = boxes[box_idx][n] = True
        return True
