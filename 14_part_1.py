import math
from collections import defaultdict

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()

def main():
    lines = list(read_lines("test_14.txt"))

    last_rock_in_column = defaultdict(int)
    spaces_in_column = defaultdict(int)

    current_load = 0
    height = len(lines)

    shifted_map = []
    
    for line in lines:
        for (i, node) in enumerate(line.strip()):
            if node == '#':
                last_rock_in_column[i] = height
                spaces_in_column[i] = 0
            elif node == '.':
                if last_rock_in_column[i] == 0:
                    last_rock_in_column[i] = height + 1
                spaces_in_column[i] += 1
            else:
                if spaces_in_column[i] > 0:
                    last_rock_in_column[i] -= 1
                    current_load += last_rock_in_column[i]
                else:
                    last_rock_in_column[i] = height
                    current_load += last_rock_in_column[i]

        height -= 1
    
    print(current_load)

if __name__ == "__main__":
    main()