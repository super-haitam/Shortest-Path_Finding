import pygame
from generate_maze_dict import sizes_str
from maze_dict_container import maze_dict


# Colors
BLUE = (0, 0, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
CYAN = (0, 80, 255)
BLACK = (0, 0, 0)
MAJENTA = (255, 0, 255)
TURQUOISE = (60, 158, 143)
BROWN = (165, 140, 130)

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Node Class
class Node:
    def __init__(self, x, y, maze_lst):
        self.x, self.y = x, y
        self.value = 0
        self.h_cost: int
        self.g_cost: int
        self.f_cost: int
        self.is_walkable: bool
        self.parent: Node
        self.color: tuple

        self.rect = pygame.Rect([self.x*(HEIGHT/len(maze_lst[0])), self.y*(HEIGHT/len(maze_lst)), HEIGHT/len(maze_lst[0]), HEIGHT/len(maze_lst)])

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
