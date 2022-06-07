from settings import *
import pygame
from tkinter import *
import random
import webbrowser


def get_maze_source(screen):
    choice_img_size = HEIGHT/4

    mazes_img = pygame.transform.scale(pygame.image.load("assets/mazes_img.jpg"), (choice_img_size, choice_img_size))
    user_choice_img = pygame.transform.scale(pygame.image.load("assets/user_choice_img.jpg"), (choice_img_size, choice_img_size))
    mazes_rect = mazes_img.get_rect(topleft=(WIDTH*(4/5)-mazes_img.get_width(), HEIGHT/1.5))
    user_choice_rect = user_choice_img.get_rect(topleft=(WIDTH/5, HEIGHT/1.5))

    # Rect for each
    r1 = pygame.Rect([WIDTH/5, HEIGHT/1.5, choice_img_size, choice_img_size])
    r2 = pygame.Rect([WIDTH*(4/5)-mazes_img.get_width(), HEIGHT/1.5, choice_img_size, choice_img_size])

    # Functions
    def draw_choice():
        screen.fill(WHITE)

        font = pygame.font.SysFont("Corbel", 60)
        wlcm = font.render("WELCOME TO", True, BLACK)
        prjct_name = font.render(pygame.display.get_caption()[0], True, TURQUOISE)
        project = font.render("PROJECT", True, BLACK)

        for num, txt in enumerate([wlcm, prjct_name, project]):
            screen.blit(txt, ((WIDTH-txt.get_width())/2, (HEIGHT/4)*(num+1)))

        pygame.display.flip()


    def draw():
        screen.fill(WHITE)

        font = pygame.font.SysFont("Corbel", 60)
        txt = font.render("Select an option", True, BLACK)
        screen.blit(txt, ((WIDTH-txt.get_width())/2, HEIGHT/3))

        screen.blit(user_choice_img, user_choice_rect.topleft)
        screen.blit(mazes_img, mazes_rect.topleft)

        pygame.draw.rect(screen, BLACK, r1, width=1)
        pygame.draw.rect(screen, BLACK, r2, width=1)

        font = pygame.font.SysFont("Corbel", 20)
        user_txt = font.render("Select to draw your own maze.   ", True, BLACK)
        maze_txt = font.render("    Select to choose a maze already prepared for you.", True, BLACK)
        screen.blit(user_txt, (user_choice_rect.midtop[0]-user_txt.get_width()/2, (HEIGHT+user_choice_rect.midbottom[1])/2))
        screen.blit(maze_txt, (mazes_rect.midtop[0]-maze_txt.get_width()/2, (HEIGHT+mazes_rect.midbottom[1])/2))

        pygame.display.flip()


    running = True
    is_started = False
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and is_started:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if HEIGHT/1.5 < mouse_y < HEIGHT/1.5+choice_img_size:
                    if WIDTH/5 < mouse_x < WIDTH/5+choice_img_size:
                        return "user"
                    if WIDTH*(4/5)-mazes_img.get_width() < mouse_x < WIDTH*(4/5):
                        return "maze images"
            
            if event.type == pygame.MOUSEBUTTONDOWN and not is_started:
                is_started = True

        if not is_started:
            draw_choice()
            continue

        draw()


def get_dimensions(screen):
    global run
    window = Tk()
    window.title("Get lenght of maze's sides")

    def command():
        global run
        run = False

    Label(window, text="Enter a number which is the lenght of the sides of the square maze.").pack()
    Label(window, text="But remember, the bigger the size is the slower the pathfinding will be.").pack()
    Label(window, text="Enter a natural positive number that should be smaller than 100.").pack()

    ent = Entry(window)
    ent.pack()

    Button(window, text="Enter", command=command).pack()

    run = True
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        window.update()
        if not run:
            size = int(ent.get())
            window.destroy()
            return size


def get_user_maze(screen, size):
    def get_reseted_nodes_lst():
        nodes_lst = [[Node(i, j, maze_lst) for i in range(size)] for j in range(size)]
        for j in range(len(nodes_lst)):
            for i in range(len(nodes_lst[0])):
                nodes_lst[j][i].color = WHITE
        return nodes_lst

    maze_lst = [[0 for i in range(size)] for j in range(size)]
    nodes_lst = get_reseted_nodes_lst()

    # Pallette colors
    colors = [{"color": BLACK, "comment": "Walls"}, {"color": WHITE, "comment": "Path"}, 
            {"color": TURQUOISE, "comment": "Start Point"}, {"color": BROWN, "comment": "End Point"}]

    # Pallette rectangles
    pallette_rects = [pygame.Rect([HEIGHT, i*HEIGHT/6, WIDTH-HEIGHT, HEIGHT/8]) for i in range(len(colors))]
    color_rect = pygame.Rect([HEIGHT+(WIDTH-HEIGHT)/20, 0, (WIDTH-HEIGHT)/3, HEIGHT/8/1.5])

    font = pygame.font.SysFont("Corbel", 20)
    # Clear
    clear_rect = pygame.Rect([HEIGHT, HEIGHT*(3/4), WIDTH-HEIGHT, HEIGHT/16])
    clear_txt = font.render("Clear", True, BLACK)
    # Solve
    solve_rect = pygame.Rect([HEIGHT, HEIGHT*(6/7), WIDTH-HEIGHT, HEIGHT/16])
    solve_txt = font.render("Solve", True, BLACK)

    # Functions
    def draw():
        screen.fill(WHITE)

        # Draw Nodes
        for j in range(len(nodes_lst)):
            for i in range(len(nodes_lst[0])):
                nodes_lst[j][i].draw(screen)

        # Draw lines to see that there are really nodes not just white space
        for j in range(len(nodes_lst)+1):
            pygame.draw.line(screen, BLACK, (0, j*(HEIGHT/len(maze_lst))), (HEIGHT, j*(HEIGHT/len(maze_lst))))
        for i in range(len(nodes_lst[0])+1):
            pygame.draw.line(screen, BLACK, (i*(HEIGHT/len(maze_lst[0])), 0), (i*(HEIGHT/len(maze_lst[0])), HEIGHT))

        # Draw colors pallette at the right of the screen
        for i in range(len(colors)):
            pallette_rect = pallette_rects[i]
            color_rect.y = pallette_rect.y + (pallette_rect.h-color_rect.h)/2

            pygame.draw.rect(screen, BLACK, pallette_rect, width=2)
            pygame.draw.rect(screen, colors[i]["color"], color_rect)
            # For the border
            pygame.draw.rect(screen, BLACK, color_rect, width=1)

            txt = font.render(colors[i]["comment"], True, BLACK)
            screen.blit(txt, (HEIGHT + (WIDTH-HEIGHT)/2, pallette_rect.y+(pallette_rect.h-txt.get_height())/2))
        
        # Add clear button
        pygame.draw.rect(screen, BLACK, clear_rect, width=2)
        screen.blit(clear_txt, (clear_rect.x + (clear_rect.w-clear_txt.get_width())/2, clear_rect.y + (clear_rect.h-clear_txt.get_height())/2))
        # Add solve button
        pygame.draw.rect(screen, BLACK, solve_rect, width=2)
        screen.blit(solve_txt, (solve_rect.x + (solve_rect.w-solve_txt.get_width())/2, solve_rect.y + (solve_rect.h-solve_txt.get_height())/2))

        pygame.display.flip()


    running = True
    selected_color = WHITE
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if pygame.mouse.get_pressed()[0]:  # Allow continuous pressing
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Color the node based on the selected_color
                for j in range(len(nodes_lst)):
                    for i in range(len(nodes_lst[0])):
                        node = nodes_lst[j][i]
                        if node.rect.collidepoint(mouse_x, mouse_y):
                            node.color = selected_color
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Change the selected color based on the Color clicked on
                for i in range(len(pallette_rects)):
                    if pallette_rects[i].collidepoint(mouse_x, mouse_y):
                        selected_color = colors[i]["color"]

                # Clear
                if clear_rect.collidepoint(mouse_x, mouse_y):
                    nodes_lst = get_reseted_nodes_lst()

                # Solve
                if solve_rect.collidepoint(mouse_x, mouse_y):
                    for j in range(len(nodes_lst)):
                        for i in range(len(nodes_lst[0])):
                            node = nodes_lst[j][i]
                            if node.color == WHITE:
                                maze_lst[j][i] = 0
                            elif node.color == BLACK:
                                maze_lst[j][i] = 1
                            elif node.color == TURQUOISE:
                                maze_lst[j][i] = 2
                            elif node.color == BROWN:
                                maze_lst[j][i] = 3
                    return maze_lst

        draw()


def get_maze_lst():
    global run
    window = Tk()
    window.title("Get maze size")

    def command():
        global run
        run = False

    Label(window, text="Select the size of the maze.").pack()

    var = IntVar()
    for num, size in enumerate(sizes_str):
        Radiobutton(window, text=size, variable=var, value=num).pack()
    Button(window, text="Enter", command=command).pack()

    run = True
    while run:
        window.update()
    
    # Will return the index of the size in the list
    size_index = var.get()

    window.destroy()
    
    return maze_dict[sizes_str[size_index]][random.randrange(4)]


def end():
    global run
    window = Tk()

    def command():
        global run
        run = False

    def open_github():
        command()
        webbrowser.open("https://github.com/super-haitam")

    Label(window, text="Thank you for running my project; Hope you enjoyed!").pack()
    Label(window, text="There are many others in my Github account: https://github.com/super-haitam").pack()
    Button(window, text="Open Github", command=open_github).pack()
    Button(window, text="See you soon!", command=command).pack()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        window.update()
    window.destroy()
