def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def p1_invalid_ids(inp: str):
    inp = inp.split(',')

    invalids = 0
    invalids_sum = 0

    for line in inp:
        start, end = line.split('-')
        start, end = int(start), int(end)
        print(start, end)

        for i in range(start, end+1):
            s = str(i)
            # odd length can't have a pattern repeating twice
            if len(s) % 2 == 1:
                continue

            midpoint = int(len(s) / 2)
            if s[:midpoint] == s[midpoint:]:
                print(f'invalid id: {s}')
                invalids += 1
                invalids_sum += i

    print(f'{invalids=} {invalids_sum=}')


def p2_invalid_ids(inp: str):
    inp = inp.split(',')

    invalids = 0
    invalids_sum = 0

    for line in inp:
        start, end = line.split('-')
        start, end = int(start), int(end)
        print(start, end)

        for i in range(start, end+1):
            s = str(i)

            midpoint = int(len(s) / 2)

            for j in range(1, midpoint+1):
                if len(s) % j == 0: 
                    chnks = set(chunks(s, j))
                    if len(chnks) == 1:
                        print(f'invalid id: {s}')
                        invalids += 1
                        invalids_sum += i
                        break

    print(f'{invalids=} {invalids_sum=}')


testinp = '''
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
'''.strip()


p1_invalid_ids(testinp)
p2_invalid_ids(testinp)
print('ok 1')

inp = open('2.input').read()
inp = inp.strip()
p1_invalid_ids(inp)
p2_invalid_ids(inp)
print('ok 2')

