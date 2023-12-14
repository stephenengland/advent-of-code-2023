def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()


def determine_success(game_line, upper_limit_cube_types):
    [game_id, game_moves] = game_line.split(': ')

    game_number = int(game_id.replace('Game ', '').strip())

    max_cube_types = {}

    for game_move in game_moves.split('; '):
        cubes = game_move.split(',')

        for cube in cubes:
            [amount, cube_type] = cube.strip().split(' ')
            if cube_type not in max_cube_types:
                max_cube_types[cube_type] = int(amount)
            else:
                max_cube_types[cube_type] = max(max_cube_types[cube_type], int(amount))
    
    for cube_type, limit in upper_limit_cube_types.items():
        if max_cube_types[cube_type] > limit:
            return (False, game_number, cube_type)
    
    return (True, game_number, None)

def get_cube_power(game_line):
    [game_id, game_moves] = game_line.split(': ')

    game_number = int(game_id.replace('Game ', '').strip())

    max_cube_types = {}

    for game_move in game_moves.split('; '):
        cubes = game_move.split(',')

        for cube in cubes:
            [amount, cube_type] = cube.strip().split(' ')
            if cube_type not in max_cube_types:
                max_cube_types[cube_type] = int(amount)
            else:
                max_cube_types[cube_type] = max(max_cube_types[cube_type], int(amount))
    
    power = 1
    for cube_type, max_type in max_cube_types.items():
        power *= max_type

    if len(max_cube_types.items()) < 3:
        raise Exception("There is a game line with none of a cube type")
    
    return power

def main():

    # For easy mode
    upper_limit_cube_types = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    lines = list(read_lines("test_2.txt"))
    sum_powers = 0
    for line in lines:
        power = get_cube_power(line)

        sum_powers += power
    
    print(f"Sum:{sum_powers}")

if __name__ == "__main__":
    main()