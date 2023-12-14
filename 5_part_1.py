import math

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()




def main():
    lines = list(read_lines("test_5.txt"))
    lowest_score = 0

    read_first_line = False
    seeds = []
    map_instructions = []

    def map_seeds():
        nonlocal seeds
        nonlocal map_instructions

        visited_seeds = set()
        new_seeds = []
        for map_instruction in map_instructions:
            [destination_start, source_start, map_range] = map_instruction.split(' ')

            for i, seed in enumerate(seeds):
                if seed >= int(source_start) and seed <= int(source_start) + int(map_range):
                    new_seeds.append(int(destination_start) - int(source_start) + seed)
                    visited_seeds.add(i)
        
        for i, seed in enumerate(seeds):
            if i not in visited_seeds:
                new_seeds.append(seed)
        seeds = new_seeds

    for line in lines:
        if not read_first_line:
            read_first_line = True
            [_, seed_contents] = line.strip().split(': ')
            for seed in seed_contents.split(' '):
                seeds.append(int(seed))
        elif line.strip():
            if ":" in line:
                if map_instructions:
                    print(seeds, map_instructions)
                    map_seeds()
                map_instructions = []
            else:
                map_instructions.append(line.strip())

    if map_instructions:
        map_seeds()
    
    lowest_score = min(seeds)

    print(f"Lowest:{lowest_score}")

if __name__ == "__main__":
    main()