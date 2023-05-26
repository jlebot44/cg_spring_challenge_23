import sys
import math
import numpy as np

cells_init = []
cells = []

target_1 = 0
target_2 = 0
target_3 = 0

result = ""
ants_base = 0


number_of_cells = int(input())  # amount of hexagonal cells in this map
for i in range(number_of_cells):
    
    # _type: 0 for empty, 1 for eggs, 2 for crystal
    # initial_resources: the initial amount of eggs/crystals on this cell
    # neigh_0: the index of the neighbouring cell for each direction
    _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
    cells_init.append([_type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5])

number_of_bases = int(input())

for i in input().split():
    my_base_index = int(i)

for i in input().split():
    opp_base_index = int(i)

# game loop
while True:
    for i in range(number_of_cells):

        total_ants = 0

        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, opp_ants = [int(j) for j in input().split()]

        if ants_base == 0 and my_ants !=0:
            ants_base = i

        if i == target_1 and resources == 0:
            target_1 = 0
        if i == target_2 and resources == 0:
            target_2 = 0        
        
        if resources !=0 and target_1 == 0:
            target_1 = i

        if resources != 0 and target_1 != i and target_2 == 0:
            target_2 = i



        total_ants += my_ants

        cells.append([resources, my_ants, opp_ants])


    for index,cell in enumerate(cells_init):
        print("init_cell : ", index, cell, file=sys.stderr, flush=True)

    for index,cell in enumerate(cells):
        print("cell : ", index, cell, file=sys.stderr, flush=True)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    result = "LINE " + str(ants_base) + " " + str(target_1) + " " + str(int(my_ants/2)) + ";" +\
             "LINE " + str(ants_base) + " " + str(target_2) + " " + str(int(my_ants/2))



    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
    
    print(result)