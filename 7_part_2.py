import math
from collections import defaultdict

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()


def determine_hand_type(hand):
    frequencies = defaultdict(int)

    most_frequent = 0
    most_frequent_card = -1
    second_most_frequent = 0
    second_most_frequent_card = -1
    jokers = 0
    for card in hand:
        frequencies[card] += 1

        if card == 1:
            jokers += 1
            continue

        if frequencies[card] > most_frequent:
            if card != most_frequent_card:
                second_most_frequent = most_frequent
                second_most_frequent_card = most_frequent_card
            most_frequent = frequencies[card]
            most_frequent_card = card
        elif frequencies[card] == most_frequent:
            if card > most_frequent_card:
                second_most_frequent = most_frequent
                second_most_frequent_card = most_frequent_card
                most_frequent = frequencies[card]
                most_frequent_card = card
            elif card >= second_most_frequent_card or frequencies[card] > second_most_frequent:
                second_most_frequent = frequencies[card]
                second_most_frequent_card = card
        elif frequencies[card] > second_most_frequent:
            second_most_frequent = frequencies[card]
            second_most_frequent_card = card
        elif frequencies[card] == second_most_frequent and card >= second_most_frequent_card:
            second_most_frequent = frequencies[card]
            second_most_frequent_card = card

    if most_frequent >= (4 - jokers):
        if most_frequent >= (5 - jokers):
            return 9, most_frequent_card, second_most_frequent_card # 5 of kind
        return 8, most_frequent_card, second_most_frequent_card # 4 of kind
    elif (most_frequent == 3 and second_most_frequent == 2) or (jokers == 1 and (most_frequent == 3 or second_most_frequent == 2)):
        return 7, most_frequent_card, second_most_frequent_card # full house
    elif most_frequent == 3 or (jokers >= 2) or (jokers == 1 and most_frequent > 1):
        return 6, most_frequent_card, second_most_frequent_card # 3 of kind
    elif (most_frequent == 2 and second_most_frequent == 2):
        return 5, most_frequent_card, second_most_frequent_card # two pairs
    elif most_frequent == 2 or jokers == 1:
        return 4, most_frequent_card, second_most_frequent_card # one pair

    return 3, most_frequent_card, second_most_frequent_card # high card

def map_faces(card):
    mapped = {
        'A': 14,
        'K': 13,
        'Q': 12,
        'J': 1,
        'T': 10,
    }
    if card in mapped:
        return mapped[card]
    
    return int(card)


def main():
    lines = list(read_lines("test_7.txt"))


    hand_list = []
    for line in lines:
        [hand, bid] = line.strip().split(' ')

        hand_mapped = list(map(map_faces, hand))

        score = determine_hand_type(hand_mapped)
        print(score)
        hand_list.append((score, int(bid), hand_mapped))

    
    hand_list.sort(key=lambda x:(x[0][0], tuple(x[2])), reverse=True)

    sum_hands = 0
    for index, hand_data in enumerate(hand_list):
        sum_hands += (len(hand_list) - index) * hand_data[1]

    print(f"sum_hands:{sum_hands}")

if __name__ == "__main__":
    main()