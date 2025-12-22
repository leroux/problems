inp = open('1.input').read()

pos = 50
p1_lands_zero = 0
p2_lands_zero = 0

for line in inp.strip().split('\n'):
    d = line[0]
    steps = int(line[1:])

    # for debug
    old_pos = pos

    while steps:
        if d == 'L':
            pos -= 1
        elif d == 'R':
            pos += 1
        steps -= 1
        if pos % 100 == 0:
            p2_lands_zero += 1

    pos_before_mod = pos
    pos %= 100

    if pos == 0:
        p1_lands_zero += 1

    print(f'{d=} {steps=} {old_pos=} {pos_before_mod=} {pos=} {p1_lands_zero=} {p2_lands_zero=}')