import math
import pprint

pp = pprint.PrettyPrinter(indent=4)

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()


reduce_away_memo = {}
def reduce_away(remaining, restrictions):
    if not remaining:
        return 0
    if not restrictions:
        return 1 if "#" not in remaining else 0

    memo_key = restrictions + (remaining,)

    if memo_key in reduce_away_memo:
        return reduce_away_memo[memo_key]

    number_of_blocks = 0
    number_of_question_marks_behind = 0
    number_of_question_marks_in_front = 0
    for (index, c) in enumerate(remaining):
        if c == '#':
            number_of_blocks += 1
        else:
            if number_of_blocks == restrictions[0]:
                start_slice = index - number_of_blocks
                end_slice = index

                new_remaining = remaining[:start_slice] + remaining[end_slice:]
                new_restrictions = restrictions[1:]

                other_combos = reduce_away(new_remaining, new_restrictions)
                if other_combos > 0:
                    reduce_away_memo[memo_key] = 1
                else:
                    reduce_away_memo[memo_key] = 0
                return reduce_away_memo[memo_key]
            elif number_of_blocks > 0:
                    return 0

    if number_of_blocks == restrictions[0]:
        end_str = len(remaining) - number_of_blocks
        if number_of_question_marks_behind > 0:
            end_str -= 1

        new_remaining = remaining[:end_str]
        new_restrictions = restrictions[1:]

        other_combos = reduce_away(new_remaining, new_restrictions)
        if other_combos > 0:
            reduce_away_memo[memo_key] = 1
        else:
            reduce_away_memo[memo_key] = 0
        return reduce_away_memo[memo_key]

    reduce_away_memo[memo_key] = 1 if "#" not in remaining and not restrictions else 0
    return reduce_away_memo[memo_key]

def main():
    lines = list(read_lines("test_12.txt"))

    memo = {}

    def get_number_of_arrangements(remaining, restrictions):
        memo_key = restrictions + (remaining,)

        if memo_key in memo:
            return memo[memo_key]

        if "?" not in remaining:
            memo[memo_key] = reduce_away(remaining, restrictions)
            return memo[memo_key] 

        result = 0
        for index, c in enumerate(remaining):
            if c == '?':
                result += get_number_of_arrangements((remaining[:index] + '.' + remaining[index + 1:]).replace('..', '.'), restrictions)
                result += get_number_of_arrangements(remaining[:index] + '#' + remaining[index + 1:], restrictions)
                break

        memo[memo_key] = result
        return memo[memo_key]

    sum_arrangements = 0
    for line in lines:
        [challenge, restriction] = line.strip().split(' ')

        # challenge = (challenge + "?") * 5

        restrictions = list(map(int, restriction.strip().split(',')))

        while ".." in challenge:
            challenge = challenge.replace('..', '.')

        result = get_number_of_arrangements(challenge, tuple(restrictions))
        #pp.pprint(reduce_away_memo)
        print(challenge, restrictions, result)
        sum_arrangements += result

    print(f"sum_arrangements:{sum_arrangements}")

if __name__ == "__main__":
    main()
