import sys
import heapq


def max_joltage(seq: str, size: int) -> str:
    stack = []
    for i, digit in enumerate(seq):
        free_space = lambda: size - len(stack)
        digits_left = len(seq) - i 

        while stack and stack[-1] < digit and free_space() < digits_left:
            stack.pop()

        if free_space():
            stack.append(digit)

    return ''.join(stack)


def digits_str_to_list(digits_str: str) -> list[int]:
    return [int(c) for c in digits_str]


assert digits_str_to_list('12345') == [1,2,3,4,5]


testcases = [
    ('987654321111111', '987654321111'),
    ('811111111111119', '811111111119'),
    ('234234234234278', '434234234278'),
    ('818181911112111', '888911112111'),
    ('999999987654321', '999999987654'),
    ('188888888888889', '888888888889'),
]

for t, expected in testcases:
    actual = max_joltage(t, 12)
    assert actual == expected, f'{t=}, {expected=}, {actual=}'

print('ok 1')

inp = open('input').read()
total = 0
for line in inp.split('\n'):
    if line == '':
        continue
    j1 = int(max_joltage(line, 12))
    total += j1
    print(f'{j1=} {total=}')

print('ok 3')
