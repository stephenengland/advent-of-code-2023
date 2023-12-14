def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()




def main():
    lines = list(read_lines("test_3.txt"))
    sum_part_numbers = 0

    matrix = {}
    symbols = []

    y = 0
    for line in lines:
        x = 0

        for char in line.strip():
            if char.isnumeric():
                matrix[(x, y)] = char
            else:
                matrix[(x, y)] = "visited"

                if char != '.':
                    symbols.append((x, y))
            x += 1
        y += 1
    
    def visit(x, y):
        nonlocal sum_part_numbers
        coord = (x, y)
        if coord in matrix and matrix[coord] != "visited":
            
            num = matrix[coord]

            other_x = x - 1
            while (other_x, y) in matrix and matrix[(other_x, y)] != "visited":
                num = matrix[(other_x, y)] + num
                matrix[(other_x, y)] = "visited"
                other_x = other_x - 1
            
            other_x = x + 1
            while (other_x, y) in matrix and matrix[(other_x, y)] != "visited":
                num = num + matrix[(other_x, y)]
                matrix[(other_x, y)] = "visited"
                other_x = other_x + 1
            
            sum_part_numbers += int(num)
            matrix[coord] = "visited"

    for symbol in symbols:
        (x, y) = symbol

        visit(x, y - 1)
        visit(x, y + 1)
        visit(x - 1, y)
        visit(x + 1, y)
        visit(x - 1, y - 1)
        visit(x + 1, y - 1)
        visit(x - 1, y + 1)
        visit(x + 1, y + 1)

    print(f"Sum:{sum_part_numbers}")

if __name__ == "__main__":
    main()