import math

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()




def main():
    lines = list(read_lines("test_4.txt"))
    sum_score = 0

    for card in lines:

        [card_label, contents] = card.split(': ')
        [winning_numbers, scratch_off] = contents.strip().split(' | ')


        winners = set()
        for winning_number in winning_numbers.strip().split(' '):
            if winning_number.strip():
                winners.add(winning_number.strip())

        count_wins = 0
        for number in scratch_off.strip().split(' '):
            if number.strip() in winners:
                count_wins += 1

        if count_wins > 0:
            print(card_label, count_wins, winners, math.pow(2, count_wins - 1))
            sum_score += math.pow(2, count_wins - 1)

    print(f"Sum:{sum_score}")

if __name__ == "__main__":
    main()