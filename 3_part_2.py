def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()




def main():
    lines = list(read_lines("test_3.txt"))
    sum_gear_ratios = 0

    numbers = {}
    matrix = {}
    gears = []

    y = 0
    number_id = 0
    current_number_characters = ''
    current_number_coords = []

    def save_current_number():
        nonlocal matrix
        nonlocal numbers
        nonlocal number_id
        nonlocal current_number_characters
        nonlocal current_number_coords

        num = int(current_number_characters)
        number_id += 1
        for coord in current_number_coords:
            matrix[coord] = number_id
            numbers[number_id] = num
        current_number_characters = ''
        current_number_coords = []

    for line in lines:
        x = 0

        if current_number_characters:
            save_current_number()

        for char in line.strip():
            if char.isnumeric():
                current_number_characters += char
                current_number_coords.append((x, y))
            else:
                if current_number_characters:
                    save_current_number()
                if char == '*':
                    gears.append((x, y))
            x += 1
        y += 1

    if current_number_characters:
        save_current_number()

    for gear in gears:
        (x, y) = gear
        adjacent_numbers = set()

        def visit(x, y):
            nonlocal matrix
            nonlocal adjacent_numbers

            if (x, y) in matrix:
                adjacent_numbers.add(matrix[(x, y)])

        visit(x, y - 1)
        visit(x, y + 1)
        visit(x - 1, y)
        visit(x + 1, y)
        visit(x - 1, y - 1)
        visit(x + 1, y - 1)
        visit(x - 1, y + 1)
        visit(x + 1, y + 1)

        if len(adjacent_numbers) == 2:
            gear_ratio = 1
            for adjacent_number in adjacent_numbers:
                gear_ratio *= numbers[adjacent_number]
            sum_gear_ratios += gear_ratio

    print(f"Sum:{sum_gear_ratios}")

if __name__ == "__main__":
    main()