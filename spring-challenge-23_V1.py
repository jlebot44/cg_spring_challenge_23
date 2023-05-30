#  
# Lot of resources
# seed=-2389445195019525600
#
# Less cristals than eggs
# seed=-6178656501653549000
# seed=-6938736017656281000
# seed=-4684031952316367000
# seed=5375051818664580000

import sys
import math
import time
from operator import attrgetter

sys. setrecursionlimit(100000)

def debug(*msg):
    print(*msg, file=sys.stderr, flush=True)

class Cell:

    def __init__(self, index, _type, resources, n0, n1, n2, n3, n4, n5) -> None:
        self.index = index
        self._type = _type
        self.resources = resources
        self.neighs = [x for x in [n0, n1, n2, n3, n4, n5] if x > -1]
        self.closed = False
        self.visted = 0

    def compute_res_around(self):
        self.res_around = sum([n.resources for n in self.neighs])


board = {}

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

number_of_cells = int(input())  # amount of hexagonal cells in this map
for i in range(number_of_cells):
    # _type: 0 for empty, 1 for eggs, 2 for crystal
    # initial_resources: the initial amount of eggs/crystals on this cell
    # neigh_0: the index of the neighbouring cell for each direction
    # _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
    board[i] = Cell(i, *[int(j) for j in input().split()])

for i, cell in board.items():
    cell.neighs = [board[ci] for ci in cell.neighs]

number_of_bases = int(input())
bases = [board[int(i)] for i in  input().split()]

for i in input().split():
    opp_base_index = int(i)

scores = []

def compute_scores(cell, back_cell, path = None):

    if path is None:
        path = [cell]
    
    if len(path) > 14:
        return

    neighs = [neigh for neigh in cell.neighs if neigh not in path]
    cell.closed = True

    for neigh in neighs:
        if neigh.resources > 0:
            # we stop this path
            comp = path[:]
            comp.append(neigh)
            scores.append(comp)
        else:
            #
            path.append(neigh)
            compute_scores(neigh, cell, path[:])


# game loop
while True:
    actions = []
    total_ants = 0
    total_resources = 0
    for i in range(number_of_cells):
        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, op_ants = [int(j) for j in input().split()]
        cell = board[i]
        cell.resources = resources
        cell.my_ants = my_ants
        cell.op_ants = op_ants
        if resources == 0:
            cell._type = 0

        cell.closed = False
        cell.visited = 0

        total_ants+= my_ants
        total_resources+= resources

    # debug("ANTS", total_ants)

    # compute_scores(bases[0], bases[0])

    for cell in board.values():
        cell.compute_res_around()

    t = time.time()
    all_scores = []
    for base in bases:
        scores = []
        compute_scores(base, base)
        all_scores+= scores

    debug("Compute scores time", time.time() - t)

    filtered = {}
    for path in all_scores:
        key = (path[0], path[-1])
        cmp = filtered.get(key, None)
        if cmp is None or len(path) < len(cmp):
            filtered[key] = path

    all_scores = filtered.values()

    def path_score(path):
        return len(path) * path[-1]._type**2

    all_scores = sorted(all_scores, key=path_score, reverse=False)
    debug(list(map(path_score, all_scores)))

    total_strength = 0
    
    strength = 1

    for path in all_scores:
        l = len(path)
        s_cell = path[0]
        e_cell = path[-1]

        actions.append("LINE %d %d %d" % (s_cell.index, e_cell.index, strength))
        total_strength+= l * .9

        if total_ants / 2 < total_strength:
            break

    if actions:
        print(";".join(actions))
    else:
        print("WAIT")
