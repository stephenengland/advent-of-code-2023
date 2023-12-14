import math
import collections

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()




def main():
    lines = list(read_lines("test_8.txt"))
    steps = 0

    line_number = 0
    sequence = ''

    current_nodes = []
    mapped_nodes = {}
    for line in lines:
        if line_number == 0:
            sequence = line.strip()

        if line_number > 1:
            [key, left_right] = line.strip().split(' = ')
            mapped_nodes[key] = tuple(left_right.replace('(', '').replace(')', '').strip().split(', '))

            if key.endswith('A'):
                current_nodes.append(key)

        line_number += 1
    
    sequence_memo = {}

    def get_sequence_change(starting_node, current_sequence):
        nonlocal sequence_memo
        nonlocal mapped_nodes

        memo_key = (starting_node, current_sequence)
        if memo_key in sequence_memo:
            return sequence_memo[memo_key]

        if current_sequence[0] == 'L':
            next_node = mapped_nodes[starting_node][0]
        else:
            next_node = mapped_nodes[starting_node][1]

        if len(current_sequence) == 1:
            sequence_memo[memo_key] = next_node
        else:
            result = get_sequence_change(next_node, current_sequence[1:])
            sequence_memo[memo_key] = result

        return sequence_memo[memo_key]

    num_sequences_required = []

    for node in current_nodes:
        new_node = node
        sequences_needed = 0
        while not new_node.endswith('Z'):
            new_node = get_sequence_change(new_node, sequence)
            sequences_needed += 1
        
        num_sequences_required.append(sequences_needed)
    
    num_sequences_needed_all = math.lcm(*num_sequences_required)

    print(f"steps:{num_sequences_needed_all * len(sequence)}")

if __name__ == "__main__":
    main()