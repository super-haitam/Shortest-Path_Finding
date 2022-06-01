# Just the sketch of logic before going into pygame
# I'd like to thank "Sebastian League" for his video about A* PathFinding Algorithm: https://www.youtube.com/watch?v=-L-WgKMFuhE
from maze_dict_container import maze_dict
from colorama import Fore
import colorama
colorama.init(autoreset=True)
from generate_maze_dict import sizes_str
from maze_dict_container import maze_dict
import time
import math
import os


# Begin
print("Welcome to the normal version of my Shortest-Path-Finding project from point A to B.")
print("For better understanding, I strongly recommend you to watch Sebastian League's video on A* pathfinding:")
print("\t https://www.youtube.com/watch?v=-L-WgKMFuhE")
print(Fore.YELLOW + "YELLOW", end=''); print(" is for Walls or not walkable nodes.")
print(Fore.RED + "RED", end=''); print(" is for self.checked nodes.")
print(Fore.GREEN + "GREEN", end=''); print(" is for the self.checked nodes' self.neighbours.")
print(Fore.CYAN + "CYAN", end=''); print(" is for neighbour with the least f-cost.")
print(Fore.BLUE + "BLUE", end=''); print(" is for the least f-cost node's parent.")
print(Fore.WHITE + "WHITE", end=''), print(" is for the walkable nodes.")

time.sleep(5)

maze_size = input(f"\nDo you want my program to solve a {', '.join(sizes_str)} maze: ").lower()
if maze_size not in sizes_str:
    print(f"\nERROR: Choice not in possible answers {sizes_str}, got {maze_size} instead!")
    quit()
integer = int(input("Choose a number from 0 to 3: "))
if not 0 <= integer <= 4:
    print(f"\nERROR: The given number is either not valid, or not between 0 and 3!")
    quit()
maze_lst = maze_dict[maze_size][integer]

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
t0 = time.time()

class Game:
    def draw(self):
        os.system("cls")
        for j in range(len(maze_lst)):
            for i in range(len(maze_lst[0])):
                if nodes_lst[j][i] == self.less_f_cost_node:
                    print(Fore.CYAN + str(nodes_lst[j][i].value), end=' ')
                elif nodes_lst[j][i] == self.less_f_cost_node.parent:
                    print(Fore.BLUE + str(nodes_lst[j][i].value), end=' ')
                elif not nodes_lst[j][i].is_walkable:
                    print(Fore.YELLOW + str(nodes_lst[j][i].value), end=' ')
                elif nodes_lst[j][i] not in self.checked:
                    if nodes_lst[j][i] in self.neighbours:
                        print(Fore.GREEN + str(nodes_lst[j][i].value), end=' ')
                    else:
                        print(Fore.WHITE + str(nodes_lst[j][i].value), end=' ')
                else:
                    print(Fore.RED + str(nodes_lst[j][i].value), end=' ')
            print()

    def set_neighbour_parents(self):
        # Set Parent of self.neighbours
        for n in self.neighbours:
            # parent = NodeWithHighestG-cost
            parent = self.checked[0]
            for ch in self.checked:
                if ch.g_cost > parent.g_cost:
                    parent = ch
            for i in range(n.x-1, n.x+2):
                for j in range(n.y-1, n.y+2):
                    if 0 <= j < len(maze_lst) and 0 <= i < len(maze_lst[0]):
                        node = nodes_lst[j][i]
                        if node != n and node in self.checked:
                            parent = node if node.g_cost <= parent.g_cost else parent
            n.parent = parent
            n.g_cost = math.sqrt((n.x - n.parent.x)**2 + (n.y - n.parent.y)**2) + n.parent.g_cost
            n.h_cost = math.sqrt((n.x - end.x)**2 + (n.y - end.y)**2)
            n.f_cost = n.g_cost + n.h_cost

    def run(self):
        # Main loop
        self.checked = [start]
        self.neighbours = []
        while True:
            for ch in self.checked:
                for j in range(ch.y - 1, ch.y + 2):
                    for i in range(ch.x - 1, ch.x + 2):
                        if 0 <= j < len(maze_lst) and 0 <= i < len(maze_lst[0]):
                            if nodes_lst[j][i] != ch and nodes_lst[j][i].is_walkable and nodes_lst[j][i] not in self.checked:
                                self.neighbours.append(nodes_lst[j][i])

            self.set_neighbour_parents()    

            # Neighbour with less f-cost will be added to self.checked and removed from self.neighbours so that it's no longer an option
            self.less_f_cost_node = self.neighbours[0]
            for neighbour in self.neighbours:
                if neighbour.f_cost < self.less_f_cost_node.f_cost and neighbour not in self.checked:
                    self.less_f_cost_node = neighbour
            for n in self.neighbours: # Looking for a node with same f-cost and lower h-cost
                if n.f_cost == self.less_f_cost_node.f_cost and n.h_cost < self.less_f_cost_node.h_cost:
                    self.less_f_cost_node = n

            self.checked.append(self.less_f_cost_node)
            self.neighbours = list(set(self.neighbours))  # The enigmatic line that saved the world. (Still don't know how nor why)
            for ch in self.checked:
                if ch in self.neighbours:
                    self.neighbours.pop(self.neighbours.index(ch))

            self.draw()

            current = self.less_f_cost_node
            if current == end:
                break
    def end(self):
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

game = Game()
game.run()
game.end()

# OHHHHHHHHHHHHHHHHHH YEAH BABYYYYYYYYYYYYY SO GOOOOOOOOOD
# I AM THE BIGGEST FAN OF CODING AND I'M GONNA BE THE BEST SOFTWARE ENGINEER IN THE WORLD!!!!!!!!
# Logic Done the 30/5/2022 at 11:09AM
# Oh.. Actually I had hard time doing this; too much struggle, I actually almost cried when it finally worked
#  today's morning, I love coding but it's kinda too hard. Gotta keep up! 1/6/2022 at 5:15PM
# Still needs some refactory to OOP to make it easier for pygame version
