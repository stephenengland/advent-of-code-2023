import math

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()




def main():
    lines = list(read_lines("test_11.txt"))

    x = 0
    y = 0
    
    x_has_galaxy = {}
    y_has_galaxy = {}
    galaxies = []

    max_x = 0

    for line in lines:
        x = 0
        for i in line:
            if i == "#":
                galaxies.append((x, y))
                x_has_galaxy[x] = True
                y_has_galaxy[y] = True

            x += 1
            max_x = max(x, max_x)
        y += 1
    
    max_y = y
    add_amount = 999999

    def increase_row(increase_y):
        nonlocal galaxies
        nonlocal add_amount

        new_galaxies = []
        for galaxy in galaxies:
            (x, y) = galaxy
            if y > increase_y:
                new_galaxies.append((x, y+add_amount))
            else:
                new_galaxies.append((x, y))

        galaxies = new_galaxies

    def increase_col(increase_x):
        nonlocal galaxies
        nonlocal add_amount

        new_galaxies = []
        for galaxy in galaxies:
            (x, y) = galaxy
            if x > increase_x:
                new_galaxies.append((x+add_amount, y))
            else:
                new_galaxies.append((x, y))

        galaxies = new_galaxies


    for i in range(0, max_y + 1):
        y = max_y - i

        if y not in y_has_galaxy or not y_has_galaxy[y]:
           increase_row(y)
    

    for i in range(0, max_x + 1):
        x = max_x - i

        if x not in x_has_galaxy or not x_has_galaxy[x]:
            increase_col(x)

    sum_paths = 0

    visited = {}
    for index, galaxy in enumerate(galaxies):
        for other_index, other_galaxy in enumerate(galaxies):
            visited_key = frozenset([index, other_index])
            if index != other_index and visited_key not in visited:
                sum_paths += abs(galaxy[0] - other_galaxy[0])
                sum_paths += abs(galaxy[1] - other_galaxy[1])
                visited[visited_key] = True

    print(f"sum_paths:{sum_paths}")

if __name__ == "__main__":
    main()