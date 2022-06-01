choice = input("Choose between the 'normal' or 'advanced' Shortest-Path Finding: ")

if choice == "normal":
    import normal
elif choice == "advanced":
    print("Do you want to")
    print("\t0: Choose an image already prepared for you")
    print("\t1: Design your own maze")

    choice = int(input())
    if choice == 0:
        import solve_maze_images
    elif choice == 1:
        import solve_user_maze
    else:
        print(f"ERROR: Invalid input, should be 0 or 1 got {choice} instead!")
