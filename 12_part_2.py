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
    if not restrictions:
        return (1, "", ()) if not remaining or "#" not in remaining else (0, "", ())
    if not remaining:
        return (0, "", ())

    memo_key = restrictions + (remaining,)

    if memo_key in reduce_away_memo:
        return reduce_away_memo[memo_key]

    number_of_blocks = 0
    for (index, c) in enumerate(remaining):
        if c == '#':
            number_of_blocks += 1
            if number_of_blocks > restrictions[0]:
                return (0, "", ())
        elif c == '?':
            if number_of_blocks == restrictions[0]:
                end_slice = index + 1
                new_remaining = remaining[end_slice:]
                new_restrictions = restrictions[1:]

                reduce_away_memo[memo_key] = reduce_away(new_remaining, new_restrictions)
                return reduce_away_memo[memo_key]
            else:
                return (0, remaining, restrictions)
        else:
            if number_of_blocks == restrictions[0]:
                end_slice = index + 1

                new_remaining = remaining[end_slice:]
                new_restrictions = restrictions[1:]

                reduce_away_memo[memo_key] = reduce_away(new_remaining, new_restrictions)
                return reduce_away_memo[memo_key]
            elif number_of_blocks > 0:
                return (0, "", ())

    if number_of_blocks == restrictions[0]:
        end_str = len(remaining) - number_of_blocks

        new_remaining = remaining[:end_str]
        new_restrictions = restrictions[1:]

        reduce_away_memo[memo_key] = reduce_away(new_remaining, new_restrictions)
        return reduce_away_memo[memo_key]

    reduce_away_memo[memo_key] = (1, "", ()) if "#" not in remaining and not restrictions else (0, "", ())
    return reduce_away_memo[memo_key]

def main():
    lines = list(read_lines("test_12.txt"))

    memo = {}

    def get_number_of_arrangements(remaining, restrictions):
        memo_key = restrictions + (remaining,)

        if memo_key in memo:
            return memo[memo_key]

        (result, new_remaining, new_restrictions) = reduce_away(remaining, restrictions)
        # print(result, new_remaining, new_restrictions, remaining, restrictions)

        if not new_remaining or not new_restrictions:
            memo[memo_key] = result
            return memo[memo_key]

        if "?" not in new_remaining:
            memo[memo_key] = 0
            return 0

        for index, c in enumerate(new_remaining):
            if c == '?':
                result += get_number_of_arrangements((new_remaining[:index] + '.' + new_remaining[index + 1:]).replace('..', '.'), new_restrictions)
                result += get_number_of_arrangements(new_remaining[:index] + '#' + new_remaining[index + 1:], new_restrictions)
                break

        memo[memo_key] = result
        return memo[memo_key]

    sum_arrangements = 0
    for line in lines:
        [challenge, restriction] = line.strip().split(' ')

        challenge = ((challenge + "?") * 5)[:-1]

        restrictions = list(map(int, restriction.strip().split(','))) * 5
        #restrictions = list(map(int, restriction.strip().split(',')))

        while ".." in challenge:
            challenge = challenge.replace('..', '.')

        result = get_number_of_arrangements(challenge, tuple(restrictions))
        #pp.pprint(reduce_away_memo)
        #print(challenge, restrictions, result)
        sum_arrangements += result

    print(f"sum_arrangements:{sum_arrangements}")

if __name__ == "__main__":
    main()
