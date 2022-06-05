import pygame
from settings import *
import utils
import math
import time
pygame.init()


# TODO Add a timer

# Screen
# H < W cuz we want place in the right of the window 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shortest-Path Finding")

# Get the maze as list of lists of Nodes whether from images or user's painting lol
maze_source = utils.get_maze_source(screen)
if maze_source == "user":
    maze_size = utils.get_dimensions(screen)
    maze_lst = utils.get_user_maze(screen, maze_size)

    nodes_lst = [[Node(i, j, maze_lst) for i in range(len(maze_lst[0]))] for j in range(len(maze_lst))]
    for j in range(len(maze_lst)):
        for i in range(len(maze_lst[0])):
            if maze_lst[j][i] == 1:
                nodes_lst[j][i].is_walkable = False
            else:
                nodes_lst[j][i].is_walkable = True
            
            if maze_lst[j][i] == 2:
                start = nodes_lst[j][i]
            elif maze_lst[j][i] == 3:
                end = nodes_lst[j][i]
elif maze_source == "maze images":
    maze_lst = utils.get_maze_lst()
    # maze_lst = maze_dict["big++"][0]
    nodes_lst = [[Node(i, j, maze_lst) for i in range(len(maze_lst[0]))] for j in range(len(maze_lst))]
    for j in range(len(maze_lst)):
        for i in range(len(maze_lst[0])):
            if maze_lst[j][i] == 1:
                nodes_lst[j][i].is_walkable = False
            else:
                nodes_lst[j][i].is_walkable = True
    start = nodes_lst[1][0]
    end = nodes_lst[-2][-1]

start.g_cost = 0
start.h_cost = math.sqrt((start.x - end.x)**2 + (start.y - end.y)**2)
start.f_cost = start.h_cost + start.g_cost

end.g_cost = start.h_cost
end.h_cost = 0
end.f_cost = end.g_cost + end.h_cost
t0 = time.time()

class Game:
    def __init__(self):
        self.least_f_cost_node = start
        self.highest_g_cost_node = start
        self.checked = [start]
        self.neighbours = []

        self.timer_font = pygame.font.SysFont("Corbel", 50, bold=True)

    def draw(self):
        screen.fill(WHITE)

        for j in range(len(maze_lst)):
            for i in range(len(maze_lst[0])):
                if nodes_lst[j][i] == self.least_f_cost_node:
                    nodes_lst[j][i].color = CYAN
                elif nodes_lst[j][i] == self.least_f_cost_node.parent:
                    nodes_lst[j][i].color = BLUE
                elif nodes_lst[j][i] == start:
                    nodes_lst[j][i].color = TURQUOISE
                elif nodes_lst[j][i] == end:
                    nodes_lst[j][i].color = BROWN
                elif not nodes_lst[j][i].is_walkable:
                    nodes_lst[j][i].color = BLACK
                elif nodes_lst[j][i] not in self.checked:
                    if nodes_lst[j][i] in self.neighbours:
                        nodes_lst[j][i].color = GREEN
                    else:
                        nodes_lst[j][i].color = WHITE
                else:
                    nodes_lst[j][i].color = RED
                nodes_lst[j][i].draw(screen)

        seconds = time.time()-t0
        minutes = 0
        while 60 <= seconds:
            minutes += 1
            seconds -= 60

        timer_txt = self.timer_font.render(f"{minutes if 10<minutes else '0'+str(minutes)}:{int(seconds) if 10<seconds else '0'+str(int(seconds))}", True, BLACK)
        screen.blit(timer_txt, ((HEIGHT+WIDTH-timer_txt.get_width())/2, HEIGHT/10))

        pygame.display.flip()

    def set_neighbour_parents(self):
        # Set Parent of self.neighbours
        for n in self.neighbours:
            # parent = NodeWithHighestG-cost
            if self.highest_g_cost_node.g_cost < self.least_f_cost_node.g_cost:
                self.highest_g_cost_node = self.least_f_cost_node
            parent = self.highest_g_cost_node

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
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False

            for j in range(self.least_f_cost_node.y - 1, self.least_f_cost_node.y + 2):  # Vertical
                if 0 <= j < len(maze_lst):
                    if nodes_lst[j][self.least_f_cost_node.x] != self.least_f_cost_node and nodes_lst[j][self.least_f_cost_node.x].is_walkable and nodes_lst[j][self.least_f_cost_node.x] not in self.checked:
                        self.neighbours.append(nodes_lst[j][self.least_f_cost_node.x])
            for i in range(self.least_f_cost_node.x - 1, self.least_f_cost_node.x + 2):  # Horizontal
                if 0 <= i < len(maze_lst[0]):
                    if nodes_lst[self.least_f_cost_node.y][i] != self.least_f_cost_node and nodes_lst[self.least_f_cost_node.y][i].is_walkable and nodes_lst[self.least_f_cost_node.y][i] not in self.checked:
                        self.neighbours.append(nodes_lst[self.least_f_cost_node.y][i])
            
            self.set_neighbour_parents()

            # Neighbour with least f-cost will be added to self.checked and removed from self.neighbours so that it's no longer an option
            self.least_f_cost_node = self.neighbours[0]
            for neighbour in self.neighbours:
                if neighbour.f_cost < self.least_f_cost_node.f_cost and neighbour not in self.checked:
                    self.least_f_cost_node = neighbour
            # Looking for a node with same f-cost and lower h-cost
            for n in self.neighbours:
                if n.f_cost == self.least_f_cost_node.f_cost and n.h_cost < self.least_f_cost_node.h_cost:
                    self.least_f_cost_node = n

            self.checked.append(self.least_f_cost_node)
            self.neighbours = list(set(self.neighbours))  # The enigmatic line that saved the world. (Still don't know how nor why)
            for n in self.neighbours:
                if n in self.checked:
                    self.neighbours.pop(self.neighbours.index(n))

            self.draw()

            current = self.least_f_cost_node
            if current == end:
                pygame.time.wait(1000)
                break

    def end(self):
        # Show the shortest path from start to end
        print("END")
        print("It took", time.time()-t0, "seconds to complete.")
        parents = [end]
        while True:
            parents.append(parents[-1].parent)

            # Will draw each time we add a parent to parents to make great effect
            for j in range(len(maze_lst)):
                for i in range(len(maze_lst[0])):
                    if nodes_lst[j][i] in parents:
                        nodes_lst[j][i].color = MAJENTA
                    elif not nodes_lst[j][i].is_walkable:
                        nodes_lst[j][i].color = BLACK
                    else:
                        nodes_lst[j][i].color = WHITE
                    nodes_lst[j][i].draw(screen)
            pygame.display.flip()

            if parents[-1] == start:
                break
            
        pygame.time.wait(1200)

game = Game()
game.run()
game.end()
 
