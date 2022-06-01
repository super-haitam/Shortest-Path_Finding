# Just the sketch of logic before going into pygame
# I'd like to thank "Sebastian League" for his video about A* PathFinding Algorithm: https://www.youtube.com/watch?v=-L-WgKMFuhE
import colorama
colorama.init(autoreset=True)
from colorama import Fore
import math
from maze_dict_container import maze_dict
import os
import time

# Begin
print("Welcome to the normal version of my Shortest-Path-Finding project from point A to B.")
print("For better understanding, I strongly recommend you to watch Sebastian League's video on A* pathfinding:")
print("\t https://www.youtube.com/watch?v=-L-WgKMFuhE")
print(Fore.YELLOW + "YELLOW", end=''); print(" is for Walls or not walkable nodes.")
print(Fore.RED + "RED", end=''); print(" is for checked nodes.")
print(Fore.GREEN + "GREEN", end=''); print(" is for the checked nodes' neighbours.")
print(Fore.CYAN + "CYAN", end=''); print(" is for neighbour with the least f-cost.")
print(Fore.BLUE + "BLUE", end=''); print(" is for the least f-cost node's parent.")
print(Fore.WHITE + "WHITE", end=''), print(" is for the walkable nodes.")

time.sleep(5)

maze_lst = maze_dict["small"][3]

# Neighbours
class Node:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.value = 0
        self.h_cost: int
        self.g_cost: int
        self.f_cost: int
        self.is_walkable: bool
        self.parent: Node


nodes_lst = [[Node(i, j) for i in range(len(maze_lst[0]))] for j in range(len(maze_lst))]
for j in range(len(maze_lst)):
    for i in range(len(maze_lst[0])):
        if maze_lst[j][i] == 1:
            nodes_lst[j][i].is_walkable = False
        else:
            nodes_lst[j][i].is_walkable = True
start = nodes_lst[1][0]
end = nodes_lst[-2][-1]
start.value, end.value = 'A', 'B'


start.g_cost = 0
start.h_cost = math.sqrt((start.x - end.x)**2 + (start.y - end.y)**2)
start.f_cost = start.h_cost + start.g_cost

end.g_cost = start.h_cost
end.h_cost = 0
end.f_cost = end.g_cost + end.h_cost

# Main loop
t0 = time.time()
current = start
checked = [start]
neighbours = []
while True:
    for ch in checked:
        for j in range(ch.y - 1, ch.y + 2):
            for i in range(ch.x - 1, ch.x + 2):
                if 0 <= j < len(maze_lst) and 0 <= i < len(maze_lst[0]):
                    if nodes_lst[j][i] != ch and nodes_lst[j][i].is_walkable and nodes_lst[j][i] not in checked:
                        neighbours.append(nodes_lst[j][i])

    # Set Parent of neighbours
    for n in neighbours:
        # parent = NodeWithHighestG-cost
        parent = checked[0]
        for ch in checked:
            if ch.g_cost > parent.g_cost:
                parent = ch
        for i in range(n.x-1, n.x+2):
            for j in range(n.y-1, n.y+2):
                if 0 <= j < len(maze_lst) and 0 <= i < len(maze_lst[0]):
                    node = nodes_lst[j][i]
                    if node != n and node in checked:
                        parent = node if node.g_cost <= parent.g_cost else parent
        n.parent = parent
        n.g_cost = math.sqrt((n.x - n.parent.x)**2 + (n.y - n.parent.y)**2) + n.parent.g_cost
        n.h_cost = math.sqrt((n.x - end.x)**2 + (n.y - end.y)**2)
        n.f_cost = n.g_cost + n.h_cost

    # Neighbour with less f-cost will be added to checked and removed from neighbours so that it's no longer an option
    less_f_cost_node = neighbours[0]
    for neighbour in neighbours:
        if neighbour.f_cost < less_f_cost_node.f_cost and neighbour not in checked:
            less_f_cost_node = neighbour
    for n in neighbours: # Looking for a node with same f-cost and lower h-cost
        if n.f_cost == less_f_cost_node.f_cost and n.h_cost < less_f_cost_node.h_cost:
            less_f_cost_node = n

    checked.append(less_f_cost_node)
    neighbours = list(set(neighbours))  # The enigmatic line that saved the world. (Still don't know how nor why)
    for ch in checked:
        if ch in neighbours:
            neighbours.pop(neighbours.index(ch))

    os.system("cls")
    for j in range(len(maze_lst)):
        for i in range(len(maze_lst[0])):
            try:
                if j == less_f_cost_node.parent.y and i == less_f_cost_node.parent.x:
                    print(Fore.BLUE + str(less_f_cost_node.parent.value), end=' ')
                elif nodes_lst[j][i] == less_f_cost_node:
                    print(Fore.CYAN + str(nodes_lst[j][i].value), end=' ')
                elif not nodes_lst[j][i].is_walkable:
                    print(Fore.YELLOW + str(nodes_lst[j][i].value), end=' ')
                elif nodes_lst[j][i] not in checked:
                    if nodes_lst[j][i] in neighbours:
                        print(Fore.GREEN + str(nodes_lst[j][i].value), end=' ')
                    else:
                        print(Fore.WHITE + str(nodes_lst[j][i].value), end=' ')
                else:
                    print(Fore.RED + str(nodes_lst[j][i].value), end=' ')
            except:
                if nodes_lst[j][i] == less_f_cost_node:
                    print(Fore.CYAN + str(nodes_lst[j][i].value), end=' ')
                elif not nodes_lst[j][i].is_walkable:
                    print(Fore.YELLOW + str(nodes_lst[j][i].value), end=' ')
                elif nodes_lst[j][i] not in checked:
                    print(Fore.GREEN + str(nodes_lst[j][i].value) if nodes_lst[j][i] in neighbours else nodes_lst[j][i].value, end=' ')
                else:
                    print(Fore.RED + str(nodes_lst[j][i].value), end=' ')
        print()

    current = less_f_cost_node
    if current == end:
        break

# Show the shortest path from start to end
print("END")
print("It took", time.time()-t0, "seconds to complete.")
parents = [end]
while True:
    parents.append(parents[-1].parent)
    if parents[-1] == start:
        break

for j in range(len(maze_lst)):
    for i in range(len(maze_lst[0])):
        if nodes_lst[j][i] in parents:
            print(Fore.MAGENTA + str(nodes_lst[j][i].value), end=' ')
        elif not nodes_lst[j][i].is_walkable:
            print(Fore.YELLOW + str(nodes_lst[j][i].value), end=' ')
        else:
            print(Fore.WHITE + str(nodes_lst[j][i].value), end=' ')
    print()

# OHHHHHHHHHHHHHHHHHH YEAH BABYYYYYYYYYYYYY SO GOOOOOOOOOD
# I AM THE BIGGEST FAN OF CODING AND I'M GONNA BE THE BEST SOFTWARE ENGINEER IN THE WORLD!!!!!!!!
# Logic Done the 30/5/2022 at 11:09AM
# Oh.. Actually I had hard time doing this; too much struggle, I actually almost cried when it finally worked
#  today's morning, I love coding but it's kinda too hard. Gotta keep up! 1/6/2022 at 5:15PM
# Still needs some refactory to OOP to make it easier for pygame version
