from PIL import Image

maze_dict = {}
sizes_str = ["big", "medium", "small", "big+", "big++"]
size_num = [(n, nb) for n in sizes_str for nb in range(1, 5)]

for size, num in size_num:
	name = f"{size} ({num}).png"
	img = Image.open(f"maze images\\{name}")

	# Get each node
	px_lst = []
	for j in range(0, img.size[1], 10):
		l = []
		for i in range(0, img.size[0], 10):
			crop = img.crop([i, j, i+10, j+10])
			l.append(crop)
		px_lst.append(l)


	# Convert from img to 0 or 1
	maze = []
	for y in px_lst:
		l = []
		for x in y:
			load = x.load()
			color = load[5, 5][:-1]
			if color == (255, 255, 255):
				l.append(0)
			elif color == (0, 0, 0):
				l.append(1)
		maze.append(l)


	if maze_dict.get(size) is not None:
		maze_dict[size].append(maze)
	else:
		maze_dict[size] = [maze]


	with open("maze_dict_container.py", 'w') as f:
		f.write(f"maze_dict = {maze_dict}")

print("Maze dict generated.\n")
