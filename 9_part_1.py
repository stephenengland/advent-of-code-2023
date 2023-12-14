import math

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()


memo = {}

def get_sequence_next_value(sequence):
    if sequence in memo:
        return memo[sequence]

    last_sequence_amount = None
    non_zero = False
    new_sequence = []
    for seq in sequence:
        if last_sequence_amount is not None:
            diff = seq - last_sequence_amount

            if diff != 0:
                non_zero = True

            new_sequence.append(diff)
            last_sequence_amount = seq
        else:
            last_sequence_amount = seq

    if non_zero:
        memo[sequence] = get_sequence_next_value(tuple(new_sequence)) + sequence[-1]
    else:
        memo[sequence] = sequence[-1]

    return memo[sequence]


def main():
    lines = list(read_lines("test_9.txt"))
    sum_seqs = 0

    times = []
    distances = []
    for line in lines:
        sequence = tuple(map(int, line.strip().split(' ')))
        sum_seqs += get_sequence_next_value(sequence)

    print(f"sum_seqs:{sum_seqs}")

if __name__ == "__main__":
    main()