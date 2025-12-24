from dataclasses import dataclass

#inp = open('5.test.input').read()
inp = open('5.input').read()

fresh_id_ranges_text, available_ids_text = inp.strip().split('\n\n')

fresh_id_ranges: list[tuple[int, int]] = []

for r in fresh_id_ranges_text.split('\n'):
    start, end = r.split('-')
    start, end = int(start), int(end)
    fresh_id_ranges.append((start, end))

avail_ids: set[int] = set()
for id_ in available_ids_text.split('\n'):
    avail_ids.add(int(id_))

fresh_id_ranges = sorted(fresh_id_ranges, key=lambda t: t[0])

rangeset = [] 
for r in fresh_id_ranges:
    # if next start < previous end, merge
    if rangeset and r[0] <= rangeset[-1][1]:
        print(f'merging {r=} and {rangeset[-1]}')
        rangeset[-1] = (rangeset[-1][0], max(rangeset[-1][1], r[1]))
    else:
        print(f'appending {r=}')
        rangeset.append(r)

print(rangeset)
print(len(rangeset))

# part 1
avail_and_fresh = 0
for id_ in avail_ids:
    for start, end in rangeset:
        if start <= id_ <= end:
            avail_and_fresh += 1
            break

# part 2
fresh = 0
for start, end in rangeset:
    fresh += end - start + 1

print(f'{avail_and_fresh=}')
print(f'{fresh=}')
