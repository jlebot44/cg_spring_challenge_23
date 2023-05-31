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

# Process firsts inputs

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


# Try to build matrix of the sortests paths between each cell
# (we have 1sec for the first run)

def shortest_path(cell_a, cell_b, board):

    for cell in board.values():
        cell._ddist = 1000

    cell_a._ddist = 0
    
    path = [cell_a]
    path_found = False

    def add_to_path(cell):
        nonlocal path
        
        for i, c in enumerate(path):
            if cell._ddist < c._ddist:
                path.insert(i, cell)

        path.append(cell)

    def compute():
        nonlocal path, path_found

        if len(path) == 0:
            path_found = True
            return

        current = path.pop(0)

        if current is cell_b:
            # debug("STOP", len(path))
            path_found = True
            path = [current]
            while current is not cell_a:
                # debug(cell_a.index, current.index)
                path.insert(0, current.path_to)
                current = current.path_to
            return


        c_ddist = current._ddist + 1
        # debug("CURR %d %d c_dist %d" % (current.index, current._ddist, c_ddist))
        
        for neigh in current.neighs:
            if neigh._ddist > c_ddist:
                # debug("> neigh %d dist %d" % (neigh.index, neigh._ddist))
                neigh._ddist = c_ddist
                neigh.path_to = current
                if neigh in path:
                    # debug('IN PATH')
                    path.sort(key=attrgetter("_ddist"), reverse=True)
                else:
                    add_to_path(neigh)
                # debug(list(map(attrgetter('index'), path)))
        #     else:
        #         debug("< neigh %d dist %d" % (neigh.index, neigh._ddist))
        # debug(list(map(attrgetter('index'), path)))


    while not path_found:
        compute()

    return path

# grid_path = []
# cells = board.values()

# cell_a = board[55]
# cell_b = board[0]
# test = shortest_path(cell_a, cell_b, board)
# debug("Shortest %d %d -> %d" % (cell_a.index, cell_b.index, len(test)))
# debug(list(map(attrgetter('index'), test)))
# for cell in cells:
#     shortest_path
# raise Exception("ARG !")



# game loop
while True:
    game_scores = input().split()
    actions = []
    total_ants = 0
    
    total_resources = 0
    total_res_ants = 0
    total_res_crys = 0


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

        if cell._type == 1:
            total_res_ants+= resources
        else:
            total_res_crys+= resources


    # debug("ANTS", total_ants)

    for cell in board.values():
        cell.compute_res_around()

    time_start = time.time()
    
    sh_paths = {}
    resource_cells = [c for c in board.values() if c.resources > 0]
    
    # Find shortest paths between bases and resources
    for base in bases:
        for target_cell in resource_cells:
            path = shortest_path(base, target_cell, board)
            # unique path per resource (ex. two bases can't target same rez)
            if target_cell in sh_paths and len(path) > len(sh_paths[target_cell]):
                continue

            sh_paths[target_cell] = path

    def path_score(path):
        # return len(path)
        return len(path) * path[-1]._type**2

    all_scores = sorted(sh_paths.values(), key=path_score, reverse=False)
    
    debug("Paths & scores compute time %.3fs " % (time.time() - time_start))
    debug(list(map(path_score, all_scores)))

    total_strength = 0

    strength = 1

    for path in all_scores:
        l = len(path)
        s_cell = path[0]
        e_cell = path[-1]

        for cell in path:
            # b_s = 2 if cell._type == 1 else 1
            b_s = 1
            actions.append("BEACON %d %d" % (cell.index, b_s))

        # actions.append("LINE %d %d %d" % (s_cell.index, e_cell.index, strength))
        total_strength+= l * .9

        if total_ants / 2 < total_strength:
            break

    if actions:
        print(";".join(actions))
    else:
        print("WAIT")
