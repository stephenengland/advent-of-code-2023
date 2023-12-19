import math

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()


def mutate_x_y(direction, x, y):
    amount = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, -1),
        "D": (0, 1),
    }[direction]

    return x + amount[0], y + amount[1]

def main():
    lines = list(read_lines("test_18.txt"))

    y = 0
    x = 0
    max_y = 0
    max_x = 0
    min_x = 0
    min_y = 0
    terrain = {}
    terrain[(x, y)] = True

    exterior = {}

    for line in lines:
        [direction, amount, color] = line.strip().split(' ')

        for i in range(int(amount)):
            new_x, new_y = mutate_x_y(direction, x, y)
            terrain[(new_x, new_y)] = True
            max_x = max(max_x, new_x)
            max_y = max(max_y, new_y)
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            x = new_x
            y = new_y
    
    if min_x < 0 or min_y < 0:
        new_terrain = {}
        for node in terrain.keys():
            new_terrain[(node[0] - min_x, node[1] - min_y)] = True
        terrain = new_terrain
        max_x = max_x - min_x
        max_y = max_y - min_y

    visited_exterior = set()
    for y in range(max_y+1):
        if (0, y) not in terrain:
            exterior[(0, y)] = True
            visited_exterior.add((0, y))
        if (max_x, y) not in terrain:
            exterior[(max_x, y)] = True
            visited_exterior.add((max_x, y))

    for x in range(max_x+1):
        if (x, 0) not in terrain:
            exterior[(x, 0)] = True
            visited_exterior.add((x, 0))
        if (x, max_y) not in terrain:
            exterior[(x, max_y)] = True
            visited_exterior.add((x, max_y))

    nodes_to_check = []

    for node in exterior.keys():
        nodes_to_check.append(mutate_x_y('L', node[0], node[1]))
        nodes_to_check.append(mutate_x_y('U', node[0], node[1]))
        nodes_to_check.append(mutate_x_y('R', node[0], node[1]))
        nodes_to_check.append(mutate_x_y('D', node[0], node[1]))

    while nodes_to_check:
        (x, y) = nodes_to_check.pop()

        if x < 0 or y < 0 or x > max_x or y > max_y or (x,y) in visited_exterior:
            continue
        
        visited_exterior.add((x, y))

        if (x, y) not in terrain and (x,y) not in exterior:
            exterior[(x, y)] = True
            nodes_to_check.append(mutate_x_y('L', x, y))
            nodes_to_check.append(mutate_x_y('U', x, y))
            nodes_to_check.append(mutate_x_y('R', x, y))
            nodes_to_check.append(mutate_x_y('D', x, y))

    # for y in range(max_y + 1):
    #     line = ''
    #     for x in range(max_x + 1):
    #         if (x,y) in exterior:
    #             line += '.'
    #         else:
    #             line += '#'
    #     print(line)

    print(((max_x + 1) * (max_y + 1)) - len(exterior.keys()))

if __name__ == "__main__":
    main()