from dataclasses import dataclass
from math import sqrt
from pprint import pprint
from itertools import islice
from collections import defaultdict


inp = open('8.input').read()
#inp = open('8.test.input').read()


@dataclass
class P:
    x: int
    y: int
    z: int

    def __repr__(p) -> str:
        return f'({p.x},{p.y},{p.z})'

    def __hash__(p) -> str:
        return hash((p.x, p.y, p.z))


def distance(p: P, t: P) -> int:
    '''
    https://en.wikipedia.org/wiki/Euclidean_distance
    '''
    a = (p.x - t.x)**2
    b = (p.y - t.y)**2
    c = (p.z - t.z)**2
    return sqrt(a + b + c)


t1 = distance(P(162,817,812), P(425,690,689))
assert round(t1, 3) == 316.902
print('ok: test distance')


def input_to_points(inp: str) -> list[P]:
    out = []
    for line in inp.splitlines():
        line2 = line.split(',')
        assert len(line2) == 3
        x, y, z = line2
        x, y, z = int(x), int(y), int(z)
        out.append(P(x, y, z))
    return out


points = input_to_points(inp)
print(f'{points=}')
assert len(points) > 0
print('ok: test input to points')


# compute distances between all points
distances = []
for i, p in enumerate(points):
    for j, t in enumerate(points[i+1:]):
        if i == j:
            continue
        d = distance(p, t)
        print(d)
        distances.append((p, t, d))


distances_ordered = sorted(distances, key=lambda t: t[2])
pprint(distances_ordered)


point_to_circuit: dict[P, int] = {}
for i, p in enumerate(points):
    point_to_circuit[p] = i 

max_conns = 1000


def take(n, iterable):
    "Return first n items of the iterable as a list."
    return list(islice(iterable, n))


connected = 0
last2 = None
for p, t, d in distances_ordered:
    #if connected == max_conns:
    #    break
    if len(point_to_circuit) == 1:
        break

    p_circuit = point_to_circuit[p]
    t_circuit = point_to_circuit[t]

    print(f'{p_circuit=} {t_circuit=} {d=}')

    if p_circuit == t_circuit:
        connected += 1
        continue

    for k, v in point_to_circuit.items():
        if v == t_circuit:
            point_to_circuit[k] = p_circuit

    connected += 1

    last2 = (p, t)


counts = defaultdict(lambda: 0)
for k, v in point_to_circuit.items():
    counts[v] += 1
print(len(counts))



circuits_by_size = sorted(((k, v) for (k, v) in counts.items()), key=lambda t: t[1], reverse=True)

ans1 = 1
for _, x in circuits_by_size[:3]:
    ans1 *= x

print(ans1)

ans2 = last2[0].x * last2[1].x
print(ans2)
