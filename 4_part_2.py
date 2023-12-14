import math

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()




def main():
    lines = list(read_lines("test_4.txt"))
    sum_score = 0

    i = 0
    card_wins = {}
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

        card_wins[i] = count_wins
        i += 1

    i -= 1
    card_score = {}
    for x in reversed(range(0, i + 1)):
        print(x, i)
        card_score[x] = 1
        if x != i and card_wins[x] > 0:
            for y in range(1, card_wins[x] + 1):
                if x + y <= i:
                    card_score[x] += card_score[x + y]
        sum_score += card_score[x]
    print(card_score)

    print(f"Sum:{sum_score}")

if __name__ == "__main__":
    main()