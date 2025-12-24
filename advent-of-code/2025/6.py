from functools import reduce

#inp = open('6.test.input').read()
inp = open('6.input').read()

lines = inp.strip().split('\n')

numbers = lines[:-1]
ops = lines[-1].split()

# part 1

colcount = len(ops)
cols = [[] for _ in range(colcount)]

for line in numbers:
    nums_in_row = line.split()
    for i, num in enumerate(nums_in_row):
        print(i, num)
        cols[i].append(int(num))

total = 0
for i, op in enumerate(ops):
    if op == '+':
        colres = reduce(lambda x, y: x + y, cols[i])
    elif op == '*':
        colres = reduce(lambda x, y: x * y, cols[i])
    else:
        asdf
    total += colres
    print(f'{colres=} {total=}')

# part 2

# rotate numbers counter-clockwise

cols = ['' for _ in range(len(numbers[0]))]

for line in numbers:
    for i, c in enumerate(line):
        cols[i] += c

# first column is bottom, last column is top
cols = list(reversed(cols))

cols2 = [[]]
for part in cols:
    stripped = part.strip()
    if stripped == '':
        cols2.append([])
    else:
        cols2[-1].append(int(stripped))

print(cols2)

ops = list(reversed(ops))

total = 0
for i, op in enumerate(ops):
    if op == '+':
        colres = reduce(lambda x, y: x + y, cols2[i])
    elif op == '*':
        colres = reduce(lambda x, y: x * y, cols2[i])
    else:
        asdf
    total += colres
    print(f'{colres=} {total=}')
