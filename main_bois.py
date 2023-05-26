import sys
import math
import numpy as np

cells_init = []


#christal
target_1 = 0
target_2 = 0

#eggs
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
    total_ants = 0
    cells = []
    for i in range(number_of_cells):

        

        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, opp_ants = [int(j) for j in input().split()]

        cells.append([resources, my_ants, opp_ants])

        if ants_base == 0 and my_ants !=0:
            ants_base = i

        total_ants += my_ants


    for i,cell in enumerate(cells):      


        if total_ants > 30:
            if i == target_1 and cell[0] == 0 :
                target_1 = 0
            if i == target_2 and cell[0] == 0 :
                target_2 = 0
         

            if cell[0] !=0 and target_1 == 0 and cells_init[i][0] == 2:
                target_1 = i

            if cell[0] != 0 and target_1 != i and target_2 == 0 and cells_init[i][0] == 2:
                target_2 = i

            result = "LINE " + str(ants_base) + " " + str(target_1) + " " + str(int(total_ants/2)) + ";" +\
                    "LINE " + str(ants_base) + " " + str(target_2) + " " + str(int(total_ants/2))

        else : 
            if i == target_3 and cell[0] == 0 :
                target_3 = 0

            if cell[0] !=0 and target_1 == 0 and cells_init[i][0] == 1:
                target_3 = i

            result = "LINE " + str(ants_base) + " " + str(target_3) + " " + str(int(total_ants))  




    # print("total_ants :", total_ants, file=sys.stderr, flush=True)
    # print("total_ants ratio 3 :", str(int(total_ants/3)), file=sys.stderr, flush=True)



    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
    
    print(result)