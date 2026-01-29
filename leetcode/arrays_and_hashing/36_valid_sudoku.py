class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        for row in board:
            if not check_valid(row):
                return False

        for col in columns(board):
            if not check_valid(col):
                return False

        for square in squares(board):
            if not check_valid(square):
                return False

        return True

def check_valid(xs: List[str]) -> bool:
    '''returns True if no repeats'''
    counts = {}
    for x in xs:
        if x == '.':
            continue
        if x in counts:
            return False
        counts[x] = 1
    return True

def columns(board: List[List[str]]) -> List[List[str]]:
    cols = []
    for col_ix in range(len(board[0])):
        col = [r[col_ix] for r in board]
        cols.append(col)
    return cols

def squares(board: List[List[str]]) -> List[List[str]]:
    squares = [
        square_centering_on(board, row_ix, col_ix)
        for row_ix, col_ix
        in [
            (1, 1),
            (1, 4),
            (1, 7),
            (4, 1),
            (4, 4),
            (4, 7),
            (7, 1),
            (7, 4),
            (7, 7),
        ]
    ]
    return squares


def square_centering_on(board: List[List[str]], row_ix, col_ix):
    return [
        board[row_ix+row_offset][col_ix+col_offset]
        for row_offset, col_offset in
        [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 0),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
    ]
