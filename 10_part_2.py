import math
from collections import defaultdict

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

    pipes = {}
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
            pipes[(x, y)] = pipe

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

    new_nodes_to_paint = []
    for potential in potentials:
        new_nodes_to_paint.append((potential, potential, frozenset([potential])))
    
    while new_nodes_to_paint:
        (node, origin_node, visited) = new_nodes_to_paint.pop()

        for other_node in pipes_connections[node]:
            if other_node == starting_location or other_node in potentials_set:
                continue

            if other_node not in visited:
                painted_nodes[other_node][origin_node] = (len(visited) + 1 if origin_node not in painted_nodes[other_node] else max(painted_nodes[other_node][origin_node], len(visited) + 1), visited | frozenset([other_node]))
                new_nodes_to_paint.append((other_node, origin_node, visited | frozenset([other_node])))

    max_sum_length = -1
    max_best = None
    max_second_best = None
    for node in painted_nodes:
        if len(painted_nodes[node].values()) > 1:
            best_loop_values = list(painted_nodes[node].values())
            best_loop_values.sort(reverse=True)
            best_sum = best_loop_values[0][0] + best_loop_values[1][0]
            if best_sum > max_sum_length:
                max_best = best_loop_values[0][1]
                max_second_best = best_loop_values[1][1]
            max_sum_length = max(max_sum_length, best_sum)


    visited = frozenset().union(max_best, max_second_best, frozenset([starting_location]))

    # Find out what 'S' is, replace it

    has_left_connection = (starting_location[0] - 1, starting_location[1]) in visited
    has_right_connection = (starting_location[0] + 1, starting_location[1]) in visited
    has_top_connection = (starting_location[0], starting_location[1] - 1) in visited
    has_bottom_connection = (starting_location[0], starting_location[1] + 1) in visited
    
    if has_left_connection:
        if has_right_connection:
            pipes[starting_location] = '-'
        elif has_bottom_connection:
            pipes[starting_location] = '7'
        elif has_top_connection:
            pipes[starting_location] = 'J'
    else:
        if has_right_connection:
            if has_bottom_connection:
                pipes[starting_location] = 'F'
            else:
                pipes[starting_location] = 'L'
        else:
            pipes[starting_location] = '|'

    # Find a node starting from the top

    y = 0
    starting_node_from_top = None
    while not starting_node_from_top:
        for x in range(max_x):
            if (x, y) in visited:
                node_type = pipes[(x,y)]
                starting_node_from_top = (x,y, 'top', 'left' if node_type in ['-', '7'] else 'right')
                break

        y += 1

    # Walk the loop using the node, marking the outside

    visited_inner_quadrants = {}
    nodes_to_walk = [starting_node_from_top]
    unenclosed_nodes = set()

    while nodes_to_walk:
        (x, y, outside_dir, coming_from) = nodes_to_walk.pop()

        if x < 0 or y < 0 or x > max_x or y > max_y or (x, y) in visited_inner_quadrants:
            continue

        pipe_type = pipes[(x,y)]

        left = right = top = bottom = False
        if pipe_type == "F":
            left = (outside_dir == "left" and coming_from == "bottom") or (outside_dir == "top" and coming_from == "right")
            top = (outside_dir == "left" and coming_from == "bottom") or (outside_dir == "top" and coming_from == "right")
        elif pipe_type == "-":
            top = outside_dir == "top"
            bottom = outside_dir == "bottom"
        elif pipe_type == "L":
            left = (outside_dir == "left" and coming_from == "top") or (outside_dir == "bottom" and coming_from == "right")
            bottom = (outside_dir == "left" and coming_from == "top") or (outside_dir == "bottom" and coming_from == "right")
        elif pipe_type == "|":
            left = outside_dir == "left"
            right = outside_dir == "right"
        elif pipe_type == "7":
            top = (outside_dir == "top" and coming_from == "left") or (outside_dir == "right" and coming_from == "bottom")
            right = (outside_dir == "top" and coming_from == "left") or (outside_dir == "right" and coming_from == "bottom")
        elif pipe_type == "J":
            bottom = (outside_dir == "bottom" and coming_from == "left") or (outside_dir == "right" and coming_from == "top")
            right = (outside_dir == "bottom" and coming_from == "left") or (outside_dir == "right" and coming_from == "top")

        #print(f"({x}, {y}), type: {pipe_type}:, left: {left}, right:{right}, top:{top}, bottom:{bottom}, outside_dir:{outside_dir}, coming_from:{coming_from}")

        if left and (x-1,y) not in visited:
            unenclosed_nodes.add((x-1, y))
        if right and (x+1,y) not in visited:
            unenclosed_nodes.add((x+1, y))
        if top and (x,y-1) not in visited:
            unenclosed_nodes.add((x, y-1))
        if bottom and (x,y+1) not in visited:
            unenclosed_nodes.add((x, y+1))

        if pipe_type in ("F", "-", "L") and (x+1, y) in visited:
            if pipe_type == "F":
                new_direction = "bottom" if outside_dir == "right" else "top"
            elif pipe_type == "-":
                new_direction = "bottom" if outside_dir == "bottom"  else "top"
            else:
                new_direction = "bottom" if outside_dir == "left" else "top"

            nodes_to_walk.append((x+1, y, new_direction, "left"))
        
        if pipe_type in ("|", "F", "7") and (x, y+1) in visited:
            if pipe_type == "|":
                new_direction = "left" if outside_dir == "left" else "right"
            elif pipe_type == "F":
                new_direction = "left" if outside_dir == "top" else "right"
            else:
                new_direction = "left" if outside_dir == "bottom" else "right"

            nodes_to_walk.append((x, y+1, new_direction, "top"))
        
        if pipe_type in ("-", "J", "7") and (x-1, y) in visited:
            if pipe_type == "-":
                new_direction = "bottom" if outside_dir == "bottom" else "top"
            elif pipe_type == "J":
                new_direction = "bottom" if outside_dir == "right" else "top"
            else:
                new_direction = "bottom" if outside_dir == "left" else "top"

            nodes_to_walk.append((x-1, y, new_direction, "right"))

        if pipe_type in ("|", "L", "J") and (x, y-1) in visited:
            if pipe_type == "|":
                new_direction = "left" if outside_dir == "left" else "right"
            elif pipe_type == "L":
                new_direction = "left" if outside_dir == "bottom" else "right"
            else:
                new_direction = "left" if outside_dir == "top" else "right"

            nodes_to_walk.append((x, y-1, new_direction, "bottom"))

        visited_inner_quadrants[(x,y)] = True

    unenclosed_nodes_list = list(unenclosed_nodes)
    # For every node that was marked, find anything touching it and mark it, too.
    while unenclosed_nodes_list:
        node = unenclosed_nodes_list.pop()
        unenclosed_nodes.add(node)

        def check_unenclosed_node(node):
            nonlocal unenclosed_nodes_list
            (x,y) = node
            if node not in visited and x >= 0 and y >= 0 and x <= max_x and y <= max_y and node not in unenclosed_nodes:
                unenclosed_nodes_list.append(node)

        (x,y) = node
        check_unenclosed_node((x-1, y))
        check_unenclosed_node((x+1, y))
        check_unenclosed_node((x, y-1))
        check_unenclosed_node((x, y+1))

    sum_enclosed = 0

    for y in range(0, max_y):
        line = ""
        for x in range(0, max_x):
            coords = (x,y)
            if coords not in visited and coords not in unenclosed_nodes:
                sum_enclosed += 1
                line += "I"
            elif coords in visited:
                line += pipes[coords]
            else:
                line += "."
        #print(line)

    print(sum_enclosed)


if __name__ == "__main__":
    main()