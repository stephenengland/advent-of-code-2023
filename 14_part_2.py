import math
from collections import defaultdict

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()

def shift_map(direction, old_map, height, length):
    new_map = []

    if direction == 'south':
        enumerated_map = enumerate(reversed(old_map))
    else:
        enumerated_map = enumerate(old_map)

    if direction in ['north', 'south']:
        block_in_direction = {}
        spaces_in_direction = defaultdict(int)

        for i in range(length):
            block_in_direction[i] = height

        current_height = height
        for (j, line) in enumerated_map:
            new_line = ''
            for (i, node) in enumerate(line):
                if node == '#':
                    spaces_in_direction[i] = 0
                    block_in_direction[i] = current_height
                    new_line += '#'
                elif node == '.':
                    spaces_in_direction[i] += 1
                    new_line += '.'
                else:
                    if spaces_in_direction[i] > 0:
                        row = height - (current_height + spaces_in_direction[i])
                        new_map[row] = new_map[row][:i] + 'O' + new_map[row][i + 1:]
                        new_line += '.'
                        block_in_direction[i] += 1
                    else:
                        block_in_direction[i] = current_height
                        new_line += 'O'

            new_map.append(new_line)
            current_height -= 1

        return (reversed(new_map) if direction == 'south' else new_map, None)
    else:
        full_map_for_hash = ''
        for (j, line) in enumerated_map:
            if direction == 'east':
                line = line[::-1]
            new_line = ''
            spaces = 0
            for (i, node) in enumerate(line):
                if node == '#':
                    if spaces > 0:
                        new_line += ('.' * spaces)
                    spaces = 0
                    new_line += '#'
                elif node == '.':
                    spaces += 1
                else:
                    new_line += 'O'

            if spaces > 0:
                new_line += ('.' * spaces)

            new_line = new_line if direction == 'west' else new_line[::-1]
            new_map.append(new_line)
            if direction == 'east':
                full_map_for_hash += new_line

        return (new_map, hash(full_map_for_hash))
            

def main():
    lines = list(read_lines("test_14.txt"))

    last_rock_in_column = defaultdict(int)
    spaces_in_column = defaultdict(int)

    current_load = 0
    height = len(lines)

    shifted_map = []

    length = len(lines[0])
    for line in lines:
        shifted_map.append(line.strip())

    hashes = {}
    current_cycle = 0
    max_cycles = 1000000000
    have_looped = False
    while current_cycle < max_cycles:
        (shifted_map, _) = shift_map('north', shifted_map, height, length)
        (shifted_map,_) = shift_map('west', shifted_map, height, length)
        (shifted_map,_) = shift_map('south', shifted_map, height, length)
        (shifted_map,new_hash) = shift_map('east', shifted_map, height, length)
        
        if not have_looped and new_hash and new_hash in hashes:
            looped_cycles = current_cycle - hashes[new_hash]
            max_cycles = (max_cycles - current_cycle) % looped_cycles
            current_cycle = 1
            have_looped = True
        else:
            hashes[new_hash] = current_cycle
            current_cycle += 1

    # for line in shifted_map:
    #     print(line)

    current_height = height
    for line in shifted_map:
        for node in line:
            if node == 'O':
                current_load += current_height
        current_height -= 1

    print(current_load)

if __name__ == "__main__":
    main()