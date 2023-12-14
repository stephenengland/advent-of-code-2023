import math

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()


def get_connections(pipe_type, x, y, max_x, max_y):
    if pipe_type == '|':
        if y > 0:
            yield (x, y-1)
        if y < max_y:
            yield (x, y + 1)
    elif pipe_type == 'L':
        if y > 0:
            yield (x, y-1)
        if x < max_x:
            yield (x+1, y)
    elif pipe_type == 'J':
        if y > 0:
            yield (x, y-1)
        if x > 0:
            yield (x-1, y)
    elif pipe_type == '7':
        if y < max_y:
            yield (x, y + 1)
        if x > 0:
            yield (x-1, y)
    elif pipe_type == 'F':
        if y < max_y:
            yield (x, y + 1)
        if x < max_x:
            yield (x+1, y)
    elif pipe_type == '-':
        if x > 0:
            yield (x-1, y)
        if x < max_x:
            yield (x+1, y)

def main():
    lines = list(read_lines("test_10.txt"))
    product = None

    pipes = []
    pipes_connections = {}
    starting_location = (-1, -1)
    potentials = []


    max_y = 0
    max_x = 0
    for line in lines:
        x = 0
        for pipe in line.strip():
            if pipe == 'S':
                starting_location = (x, max_y)
            x += 1
        max_x = max(max_x, x)
        max_y += 1

    y = 0
    for line in lines:
        x = 0
        for pipe in line.strip():
            if pipe != ".":
                if pipe != 'S':
                    pipes_connections[(x, y)] = list(get_connections(pipe, x, y, max_x, max_y))
                    if starting_location in pipes_connections[(x, y)]:
                        potentials.append((x, y))

                
            x += 1

        y += 1

    potentials_set = set(potentials)
    painted_nodes = {}
    
    for node in pipes_connections:
        painted_nodes[node] = {}

    # def paint_potential_paths(node, origin_node, visited):
    #     nonlocal painted_nodes
    #     nonlocal pipes_connections
    #     nonlocal starting_location
    #     nonlocal potentials_set

    #     for other_node in pipes_connections[node]:
    #         if other_node == starting_location or other_node in potentials_set:
    #             continue

    #         if other_node not in visited:
    #             painted_nodes[other_node][origin_node] = len(visited) + 1 if origin_node not in painted_nodes[other_node] else max(painted_nodes[other_node][origin_node], len(visited) + 1)
    #             paint_potential_paths(other_node, origin_node, visited | frozenset([other_node]))

    new_nodes_to_paint = []
    for potential in potentials:
        new_nodes_to_paint.append((potential, potential, frozenset([potential])))
    
    while new_nodes_to_paint:
        (node, origin_node, visited) = new_nodes_to_paint.pop()

        for other_node in pipes_connections[node]:
            if other_node == starting_location or other_node in potentials_set:
                continue

            if other_node not in visited:
                painted_nodes[other_node][origin_node] = len(visited) + 1 if origin_node not in painted_nodes[other_node] else max(painted_nodes[other_node][origin_node], len(visited) + 1)
                new_nodes_to_paint.append((other_node, origin_node, visited | frozenset([other_node])))

    max_sum_length = -1
    for node in painted_nodes:
        if len(painted_nodes[node].values()) > 1:
            best_loop_values = list(painted_nodes[node].values())
            best_loop_values.sort(reverse=True)
            max_sum_length = max(max_sum_length, best_loop_values[0] + best_loop_values[1])
            

    print(f"longest_loop:{max_sum_length/2}")

if __name__ == "__main__":
    main()