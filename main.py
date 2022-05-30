# Just the sketch of logic before going into pygame
# I'd like to thank "Sebastian League" for his video about A* PathFinding Algorithm: https://www.youtube.com/watch?v=-L-WgKMFuhE
import colorama
colorama.init(autoreset=True)
from colorama import Fore
import math


maze_lst = [[0 for i in range(10)] for j in range(8)]
maze_lst[0][0] = 1
maze_lst[-1][-1] = 2

# Neighbours
class Node:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.value: int
        self.h_cost: int
        self.g_cost: int
        self.f_cost: int


nodes_lst = [[Node(i, j) for i in range(len(maze_lst))] for j in range(len(maze_lst[0]))]
for j in range(len(maze_lst)):
    for i in range(len(maze_lst[0])):
        print(j, i)
        nodes_lst[j][i].value = maze_lst[j][i]
start = nodes_lst[0][0]
end = nodes_lst[-1][-1]

# Neighbours
current = nodes_lst[5][2]
checked = []
while True:
    # TODO You have to handle the case where the current is in the border
    neighbours = []
    for j in range(current.y - 1, current.y + 2):
        for i in range(current.x - 1, current.x + 2):
            if 0 <= j < len(maze_lst) and 0 <= i < len(maze_lst[0]):
                node = nodes_lst[j][i]
                if node != current and node != start:
                    neighbours.append(node)

    # Setting Costs
    for neighbour in neighbours:
        neighbour.g_cost = math.sqrt((neighbour.x - start.x)**2 + (neighbour.y - start.y)**2)
        neighbour.h_cost = math.sqrt((neighbour.x - end.x)**2 + (neighbour.y - end.y)**2)
        neighbour.f_cost = neighbour.h_cost + neighbour.g_cost

    # Neighbour with less f-cost
    less_f_cost_node = neighbours[0]
    for neighbour in neighbours:
        if neighbour.f_cost < less_f_cost_node.f_cost and neighbour not in checked:
            less_f_cost_node = neighbour
    checked.append(less_f_cost_node)

    print("----------------------------------")
    for j in range(len(maze_lst)):
        for i in range(len(maze_lst[0])):
            if nodes_lst[j][i] not in checked:
                print(Fore.GREEN + str(nodes_lst[j][i].value) if nodes_lst[j][i] in neighbours else nodes_lst[j][i].value, end=' ')
            else:
                print(Fore.RED + str(nodes_lst[j][i].value), end=' ')
        print()
    current = less_f_cost_node
    if current == end:
        break
