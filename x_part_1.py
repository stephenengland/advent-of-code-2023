import math

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()




def main():
    lines = list(read_lines("test_x.txt"))

    for line in lines:
        [label, contents] = line.strip().split(':')

if __name__ == "__main__":
    main()