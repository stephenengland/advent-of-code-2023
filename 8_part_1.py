import math

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()




def main():
    lines = list(read_lines("test_8.txt"))
    steps = 0

    line_number = 0
    sequence = []

    current_nodes = []
    mapped_nodes = {}
    for line in lines:
        if line_number == 0:
            for seq in line.strip():
                sequence.append(seq)

        if line_number > 1:
            [key, left_right] = line.strip().split(' = ')
            mapped_nodes[key] = tuple(left_right.replace('(', '').replace(')', '').strip().split(', '))

            if key.endswith('A'):
                current_nodes.append(key)

        line_number += 1

    while not all(n.endswith('Z') for n in current_nodes):
        for seq in sequence:
            steps += 1
            new_nodes = []
            for current_node in current_nodes:
                if seq == 'L':
                    new_nodes.append(mapped_nodes[current_node][0])
                else:
                    new_nodes.append(mapped_nodes[current_node][1])

    print(f"steps:{steps}")

if __name__ == "__main__":
    main()