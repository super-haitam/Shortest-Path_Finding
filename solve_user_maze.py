import pygame
import math
import time
pygame.init()


# Colors
BLUE = (0, 0, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
CYAN = (0, 80, 255)
BLACK = (0, 0, 0)
MAJENTA = (255, 0, 255)

# Screen
WIDTH, HEIGHT = 800, 600  # H < W cuz we want place in the right of the window 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shortest-Path Finding")

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
        self.color: tuple

        self.rect = pygame.Rect([x*(HEIGHT/len(maze_lst[0])), y*(HEIGHT/len(maze_lst)), HEIGHT/len(maze_lst[0]), HEIGHT/len(maze_lst)])

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# HERE THE WORK BEGINS 

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
        screen.fill(WHITE)

        for j in range(len(maze_lst)):
            for i in range(len(maze_lst[0])):
                if nodes_lst[j][i] == self.less_f_cost_node:
                    nodes_lst[j][i].color = CYAN
                elif nodes_lst[j][i] == self.less_f_cost_node.parent:
                    nodes_lst[j][i].color = BLUE
                elif not nodes_lst[j][i].is_walkable:
                    nodes_lst[j][i].color = BLACK
                elif nodes_lst[j][i] not in self.checked:
                    if nodes_lst[j][i] in self.neighbours:
                        nodes_lst[j][i].color = GREEN
                    else:
                        nodes_lst[j][i].color = WHITE
                else:
                    nodes_lst[j][i].color = RED
                nodes_lst[j][i].draw()

        pygame.display.flip()

    def set_neighbour_parents(self):
        # Set Parent of self.neighbours
        for n in self.neighbours:
            # parent = NodeWithHighestG-cost
            parent = self.checked[0]
            for ch in self.checked:
                if ch.g_cost > parent.g_cost:
                    parent = ch
            for i in range(n.x-1, n.x+2):
                if 0 <= i < len(maze_lst[0]):
                    node = nodes_lst[n.y][i]
                    if node != n and node in self.checked:
                        parent = node if node.g_cost <= parent.g_cost else parent
            for j in range(n.y-1, n.y+2):
                if 0 <= j < len(maze_lst):
                    node = nodes_lst[j][n.x]
                    if node != n and node in self.checked:
                        parent = node if node.g_cost <= parent.g_cost else parent
            n.parent = parent
            n.g_cost = math.sqrt((n.x - n.parent.x)**2 + (n.y - n.parent.y)**2) + n.parent.g_cost
            n.h_cost = math.sqrt((n.x - end.x)**2 + (n.y - end.y)**2)
            n.f_cost = n.g_cost + n.h_cost

    def run(self):
        # Main loop
        self.less_f_cost_node = start
        self.checked = [start]
        self.neighbours = []
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False

            for j in range(self.less_f_cost_node.y - 1, self.less_f_cost_node.y + 2):  # Vertical
                if 0 <= j < len(maze_lst):
                    if nodes_lst[j][self.less_f_cost_node.x] != self.less_f_cost_node and nodes_lst[j][self.less_f_cost_node.x].is_walkable and nodes_lst[j][self.less_f_cost_node.x] not in self.checked:
                        self.neighbours.append(nodes_lst[j][self.less_f_cost_node.x])
            for i in range(self.less_f_cost_node.x - 1, self.less_f_cost_node.x + 2):  # Horizontal
                if 0 <= i < len(maze_lst[0]):
                    if nodes_lst[self.less_f_cost_node.y][i] != self.less_f_cost_node and nodes_lst[self.less_f_cost_node.y][i].is_walkable and nodes_lst[self.less_f_cost_node.y][i] not in self.checked:
                        self.neighbours.append(nodes_lst[self.less_f_cost_node.y][i])
            
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
            for n in self.neighbours:
                if n in self.checked:
                    self.neighbours.pop(self.neighbours.index(n))

            self.draw()

            current = self.less_f_cost_node
            if current == end:
                pygame.time.wait(3000)
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
                    nodes_lst[j][i].color = MAJENTA
                elif not nodes_lst[j][i].is_walkable:
                    nodes_lst[j][i].color = BLACK
                else:
                    nodes_lst[j][i].color = WHITE
                nodes_lst[j][i].draw()
        pygame.display.flip()
        pygame.time.wait(3000)

game = Game()
game.run()
game.end()
 
