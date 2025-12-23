inp = open('4.input').read()
testinp = open('4.test.input').read()


def p1(inp: str) -> int:
    inp = inp.strip().split('\n')
    print(inp)

    xlen = len(inp[0])
    ylen = len(inp)
    print(f'{xlen=} {ylen=}')

    accessible_rolls = 0

    for x in range(0, xlen):
        for y in range(0, ylen):
            print(f'{x=} {y=} {inp[y][x]=} {adjacent(x, y, xlen, ylen)=}')

            # only check adjacent for spots with a roll
            if inp[y][x] != '@':
                continue

            adjs = adjacent(x, y, xlen, ylen)

            # if we're at the edge there are default free spots
            free_spots = 8 - len(adjs) 

            for x2, y2 in adjs:
                print(f'{x2=} {y2=} {inp[y2][x2]=}')
                if inp[y2][x2] == '.':
                    free_spots += 1

            if free_spots >= 5:
                accessible_rolls += 1

    return accessible_rolls


def p2(inp: str) -> int:
    inp = inp.strip().split('\n')
    inp = [list(inner) for inner in inp]
    print(inp)

    xlen = len(inp[0])
    ylen = len(inp)
    print(f'{xlen=} {ylen=}')

    previous_accessible_rolls = None
    accessible_rolls = 0

    while previous_accessible_rolls != accessible_rolls:
        previous_accessible_rolls = accessible_rolls

        for x in range(0, xlen):
            for y in range(0, ylen):
                print(f'{x=} {y=} {inp[y][x]=} {adjacent(x, y, xlen, ylen)=}')

                # only check adjacent for spots with a roll
                if inp[y][x] not in '@x':
                    continue

                adjs = adjacent(x, y, xlen, ylen)

                # if we're at the edge there are default free spots
                free_spots = 8 - len(adjs) 

                for x2, y2 in adjs:
                    print(f'{x2=} {y2=} {inp[y2][x2]=}')
                    if inp[y2][x2] == '.':
                        free_spots += 1

                if free_spots >= 5:
                    accessible_rolls += 1
                    inp[y][x] = 'x'

        # remove all x
        for x in range(0, xlen):
            for y in range(0, ylen):
                if inp[y][x] == 'x':
                    inp[y][x] = '.'


    return accessible_rolls

    
def adjacent(x, y, xlen, ylen):
    coords = [
        (x-1, y-1),
        (x  , y-1),
        (x+1, y-1),
        (x-1, y),
        (x+1, y),
        (x-1, y+1),
        (x  , y+1),
        (x+1, y+1),
    ]
    coords = [(x, y) for (x, y) in coords if x >= 0 and x < xlen and y >= 0 and y < ylen]
    return coords


testinp_p1 = p1(testinp)
print(f'{testinp_p1=}')
assert testinp_p1 == 13
testinp_p2 = p2(testinp)
print(f'{testinp_p2=}')
assert testinp_p2 == 43

inp_p1 = p1(inp)
print(f'{inp_p1=}')
inp_p2 = p2(inp)
print(f'{inp_p2=}')
