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

        map_instructions_ints = []
        for map_instruction in map_instructions:
            [destination_start, source_start, map_range] = map_instruction.split(' ')
            map_instructions_ints.append((int(destination_start), int(source_start), int(map_range)))
        new_seeds = []

        for seed in seeds:
            seed_ranges_left = [seed]

            while seed_ranges_left:
                (seed_start, seed_range) = seed_ranges_left.pop()
                seed_end = seed_start + seed_range
                found_modification = False

                for map_instruction in map_instructions_ints:
                    (destination_start, source_start, map_range) = map_instruction
                    source_end = source_start + map_range

                    start_within_range = seed_start >= source_start and seed_start <= source_end
                    end_within_range = seed_end >= source_start and seed_end <= source_end

                    modifier = destination_start - source_start
                    if start_within_range and end_within_range:
                        new_seeds.append((seed_start + modifier, seed_range))
                        found_modification = True
                    elif start_within_range:
                        remainder = seed_end - source_end

                        new_seeds.append((seed_start + modifier, seed_range - remainder))
                        seed_ranges_left.append((source_end + 1, remainder))
                        found_modification = True
                    elif end_within_range:
                        split_range = (seed_end - source_start) + 1
                        new_seeds.append((source_start + modifier, split_range))
                        seed_ranges_left.append((seed_start, seed_range - split_range))
                        found_modification = True

                if not found_modification:
                    new_seeds.append((seed_start, seed_range))

        seeds = new_seeds

    for line in lines:
        if not read_first_line:
            read_first_line = True
            [_, seed_contents] = line.strip().split(': ')

            seed_start = None
            for seed in seed_contents.split(' '):
                if seed_start is None:
                    seed_start = int(seed)
                else:
                    seeds.append((seed_start, int(seed)))
                    seed_start = None
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
    
    def find_score_of_seed_range(s):
        return s[0]

    lowest_score = min(seeds, key=find_score_of_seed_range)

    print(f"Lowest:{lowest_score}")

if __name__ == "__main__":
    main()