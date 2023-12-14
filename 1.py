def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()

def seek_number_first(word):
    number = None
    for i in range(len(word) - 1):
        if word[i].isnumeric():
            number = int(word[i]) * 10
            break
    
    if number is not None:
        for i in range(len(word)):
            if word[len(word) - (i + 1)].isnumeric():
                number += int(word[len(word) - (i + 1)])
                break

    return number

# I know there are easier ways to do this- but I did this as part of the challenge.
numbers_as_letters = { "one", "two", "three", "four", "five", "six", "seven", "eight", "nine" }
numbers_mapping = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9
}

still_possible_to_be_a_number = {}
still_possible_to_be_a_number_backwards = {}
longest_number_length = 5
for i in range(longest_number_length + 1):
    for number in numbers_as_letters:
        if len(number) >= (i):
            still_possible_to_be_a_number[number[:i]] = True
            still_possible_to_be_a_number_backwards[number[i:]] = True

def seek_number(word):
    number = None

    start = 0
    for i in range(len(word) - 1):

        if word[i].isnumeric():
            number = int(word[i]) * 10
            break
        
        if i - start >= 2:
            if word[start:i+1] in numbers_mapping:
                number = numbers_mapping[word[start:i+1]] * 10
                break

        # Trim the start of the sliding window
        while i > start and word[start:i+1] not in still_possible_to_be_a_number:
            start += 1

    end = len(word) - 1
    if number is not None:
        for i in range(len(word)):
            index = len(word) - (i + 1)
            if word[index].isnumeric():
                number += int(word[index])
                break
            
            if end - index >= 2:
                if word[index:end] in numbers_mapping:
                    number += numbers_mapping[word[index:end]]
                    break

            # Trim the end of the sliding window
            while index < end and word[index:end] not in still_possible_to_be_a_number_backwards:
                end -= 1

    return number


def main():

    lines = list(read_lines("test.txt"))
    sum = 0
    for line in lines:
        number = seek_number(line)
        print(f"{line.strip()}:{number}")

        if number:
            sum += number
    
    print(f"Sum:{sum}")

if __name__ == "__main__":
    main()