from pprint import pprint


inp = open('7.input').read()
#inp = open('7.test.input').read()

inp = inp.split('\n')[:-1]
inp = [list(s) for s in inp]


# part 1

splits = 0

for r in range(0, len(inp)):
    for c in range(len(inp[r])):
        if inp[r][c] == '.':
            inp[r][c] = 0
        elif inp[r][c] == 'S':
            inp[r][c] = 1

for r in range(1, len(inp)):
    for c in range(len(inp[r])):
        if inp[r][c] == '^':
            # split to left and right
            # for part 1
            splits += 1
            inp[r][c-1] += inp[r-1][c]
            inp[r][c+1] += inp[r-1][c]
            inp[r][c] = 0
        else:
            inp[r][c] += inp[r-1][c]


print(splits)

print(sum(inp[-1]))
