import sys
import math
import time
from operator import attrgetter
from  typing import List, Dict

sys.setrecursionlimit(100000)

def debug(*msg):
    """Logging fn"""
    print(*msg, file=sys.stderr, flush=True)

class Cell:
    """Pojo like to represent a cell."""

    def __init__(self, index, _type, resources, n0, n1, n2, n3, n4, n5) -> None:
        self.index = index
        self._type = _type
        self.resources = resources
        self.neighs = [x for x in [n0, n1, n2, n3, n4, n5] if x > -1]
        self.beacon = 0

    def compute_res_around(self):
        self.res_around = sum([n.resources for n in self.neighs])

    def __str__(self):
        return self.index

def shortest_path(cell_a, cell_b, board):
    """Compute the shortest path between 2 cells (Dijkkstra).

    Parameters
    ----------
    cell_a : Cell
        The cell to start from
    cell_b : Cell
        The target cell
    board : dict of Cell
        The grid to search into

    Returns
    -------
    A list of Cell representing the shortest path, cell a and b included
    """

    for cell in board.values():
        cell._ddist = 1000

    cell_a._ddist = 0
    
    path = [cell_a]
    path_found = False

    def add_to_path(cell):
        nonlocal path

        for i, c in enumerate(path):
            if cell._ddist < c._ddist:
                return path.insert(i, cell)

        path.append(cell)

    def step_search():
        nonlocal path, path_found

        if len(path) == 0:
            path_found = True
            return

        current = path.pop(0)

        # target found, compute path and leave
        if current is cell_b:
            path_found = True
            path = [current]
            while current is not cell_a:
                path.insert(0, current.path_to)
                current = current.path_to
            return

        c_ddist = current._ddist + 1

        for neigh in current.neighs:
            if neigh._ddist > c_ddist:
                weight = neigh.resources / 1000
                neigh._ddist = c_ddist - weight
                neigh.path_to = current
                if neigh in path:
                    path.sort(key=attrgetter("_ddist"), reverse=True)
                else:
                    add_to_path(neigh)

    while not path_found:
        step_search()

    return path


# ------------------
# Global vars & init

board: Dict[int, Cell] = {}
bases: List[Cell]
my_score: int
op_score: int

# build board
number_of_cells = int(input())  # amount of hexagonal cells in this map
for i in range(number_of_cells):
    # _type: 0 for empty, 1 for eggs, 2 for crystal
    # initial_resources: the initial amount of eggs/crystals on this cell
    # neigh_0: the index of the neighbouring cell for each direction
    # _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
    board[i] = Cell(i, *[int(j) for j in input().split()])

# update neighbors with cells references
for i, cell in board.items():
    cell.neighs = [board[ci] for ci in cell.neighs]

input() # flush (number of bases)

# store bases
bases = [board[int(i)] for i in  input().split()]

# unused now (op bases)
for i in input().split():
    opp_base_index = int(i)

# Game lopp inputs
def input_game_update():
    """Update board cells and global vars"""
    global my_score, op_score

    my_score, op_score = [int(i) for i in input().split()]

    for i in range(len(board)):
        # resources: amount of eggs/crystals on this cell
        # my_ants:  amount of my ants on this cell
        # opp_ants: amount of opponent ants on this cell
        resources, my_ants, op_ants = [int(j) for j in input().split()]

        cell = board[i]
        cell.resources = resources
        cell.my_ants = my_ants
        cell.op_ants = op_ants
        if resources == 0:
            cell._type = 0


# ---------
# Game loop

while True:

    # Update game state

    input_game_update()

    total_own_ants = 0
    total_res_ants = 0
    total_res_crys = 0
    total_res_eggs = 0

    # Compute total res and ants, not really optimized
    # (we could compute this in input_game_update)
    for cell in board.values():
        total_own_ants += cell.my_ants

        if cell._type == 1:
            total_res_ants += cell.resources
            total_res_eggs += 1
        else:
            total_res_crys += cell.resources

        # WIP: cache res ! mixed eggs / crystals
        cell.compute_res_around()

    debug("rez cristals: %d - rez ants: %d - rez eggs: %d - my ants: %d" % (total_res_crys, total_res_ants, total_res_eggs, total_own_ants))

    time_start = time.time()

    # Compute shortest paths between bases and resources
    # Sort them by shortest and egg first

    sh_paths = {}
    resource_cells = [c for c in board.values() if c.resources > 0]
    for base in bases:
        for target_cell in resource_cells:
            path = shortest_path(base, target_cell, board)
            # unique path per resource (ex. two bases can't target same rez)
            if target_cell in sh_paths and len(path) > len(sh_paths[target_cell]):
                continue

            sh_paths[target_cell] = path

    def path_score(path):
        """Base scoring used to do sorting"""
        return len(path) * path[-1]._type**2

    all_scores = sorted(sh_paths.values(), key=path_score, reverse=False)

    debug("Paths compute time: %.3fs " % (time.time() - time_start))

    # Build actions
    # (poor stop condition)

    beacons = set()
    actions = []

    # reset cell beacon state
    for cell in board.values():
        cell.beacon = 0

    for path in all_scores:
        l = len(path)
        for cell in path:
            b_s = 1
            actions.append("BEACON %d %d" % (cell.index, b_s))
            beacons.add(cell.index)
            cell.beacon = b_s

        rate = len(path) # magic number :s
        if len(beacons) > total_own_ants / rate:
            break

    # Fire !
    if not actions:
        actions = ["WAIT"]

    print(";".join(actions))


# TODO:
# Find what's to focus more: crystals or eggs
# If we have "enough" ants, maximize crystal collect
#
# "Weighted paths" by my ants / op ants
# Can it be a strategy ?
# - Checker si res est capturée par op et si ça vaut le coup de surcharger
# - Essayer de voir si on peut computer le nombre de resources gagnées: (simuler déplacement des ants)

"""
Game conf for testing

* Lasts (BOSS)
seed=-6349142426491180000
seed=5824882457295828000

* Lot of resources
seed=-2389445195019525600
Less cristals than eggs
seed=-6178656501653549000
seed=-6938736017656281000
seed=-4684031952316367000
seed=5375051818664580000
"""