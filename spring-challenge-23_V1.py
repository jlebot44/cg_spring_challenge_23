import sys
import math

def debug(*msg):
    print(*msg, file=sys.stderr, flush=True)

board = {}

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

number_of_cells = int(input())  # amount of hexagonal cells in this map
for i in range(number_of_cells):
    # _type: 0 for empty, 1 for eggs, 2 for crystal
    # initial_resources: the initial amount of eggs/crystals on this cell
    # neigh_0: the index of the neighbouring cell for each direction
    _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
    board[i] = [_type, initial_resources]

number_of_bases = int(input())

for i in input().split():
    my_base_index = int(i)

for i in input().split():
    opp_base_index = int(i)

# game loop
while True:
    actions = []
    total_ants = 0
    for i in range(number_of_cells):
        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, opp_ants = [int(j) for j in input().split()]

        board[i][1] = resources
        if resources == 0:
            board[i][0] = 0

        total_ants+= my_ants

        if resources > 0:
            actions.append("LINE %d %d %d" % (my_base_index, i, 2))
        #     debug("resources %d" % int(resources / (my_ants + 1)))

    resources = [x for x in [*board.items()] if x[1][0] > 0]
    resources = sorted(resources, key=lambda x: x[1][1] / x[1][0]**2, reverse=True)
    l = len(resources)

    for i, res in resources:
        actions.append("LINE %d %d %d" % (my_base_index, i, i))
        # l -= 1

    # debug(res)
    # eggs = sum([r for t, r in board.items() if t == 1])
    
    # if ()
    # for i, res in board.items():


    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    if actions:
        print(";".join(actions))
    else:
        # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
        print("WAIT")
