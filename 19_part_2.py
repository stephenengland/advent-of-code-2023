import math

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()


class Rule:
    
    def __init__(self, condition, value, xmas_type, direction):
        self.condition = condition
        self.value = value
        self.xmas_type = xmas_type
        self.direction = direction

    def is_instruction(self):
        return self.condition == None

    def __str__(self):
        return f"{self.condition}, {self.value}, {self.xmas_type}, {self.direction}"

    def __repr__(self):
        if self.is_instruction():
            return f"{self.direction} instruction;"
        return f"{self.condition}, {self.value}, {self.xmas_type}, {self.direction};"

def main():
    lines = list(read_lines("test_19.txt"))

    rules_dict = {}
    has_found_a_blank_line = False
    for line in lines:
        if not line.strip():
            has_found_a_blank_line = True

        if not has_found_a_blank_line:
            [label, rules] = line.strip().split('{')
            rules_list = []
            for rule_s in rules.replace('}', '').split(','):
                phrase = rule_s.split(':')
                if len(phrase) > 1:
                    [rest_1, direction] = phrase
                    xmas_type = rest_1[0]
                    condition = rest_1[1]
                    value = int(rest_1[2:])
                    rules_list.append(Rule(condition, value, xmas_type, direction))
                else:
                    [direction] = phrase
                    rules_list.append(Rule(None, None, None, direction))
            rules_dict[label] = rules_list

    ranges_to_consider = [{ "x": (1, 4000),  "m": (1, 4000),  "a": (1, 4000),  "s": (1, 4000), "direction": "in"}]
    ranges_accepted = []

    def apply_rules(rules, range_in):
        current_range = range_in.copy()
        new_ranges = []

        for rule in rules:
            if rule.is_instruction():
                new_ranges.append({
                    **current_range,
                    "direction": rule.direction
                })
                return new_ranges
            else:
                range_to_compare = current_range[rule.xmas_type]

                if rule.condition == '>':
                    if range_to_compare[0] > rule.value:
                        new_ranges.append({
                            **current_range,
                            "direction": rule.direction
                        })
                        return
                    if range_to_compare[1] > rule.value:
                        new_ranges.append({
                            **current_range,
                            "direction": rule.direction,
                            rule.xmas_type: (rule.value + 1, range_to_compare[1])
                        })
                        current_range[rule.xmas_type] = (range_to_compare[0], rule.value)
                    # Rule does not apply, carry on!
                elif rule.condition == '<':
                    if range_to_compare[1] < rule.value:
                        new_ranges.append({
                            **current_range,
                            "direction": rule.direction
                        })
                        return
                    if range_to_compare[0] < rule.value:
                        new_ranges.append({
                            **current_range,
                            "direction": rule.direction,
                            rule.xmas_type: (range_to_compare[0], rule.value - 1)
                        })
                        current_range[rule.xmas_type] = (rule.value, range_to_compare[1])
                    # Rule does not apply, carry on!
        return new_ranges

    while ranges_to_consider:
        range_to_consider = ranges_to_consider.pop()
        new_ranges = apply_rules(rules_dict[range_to_consider["direction"]], range_to_consider)

        if not new_ranges:
            continue

        for new_range in new_ranges:
            if new_range["direction"] == "A":
                ranges_accepted.append(new_range)
            elif new_range["direction"] != "R":
                ranges_to_consider.append(new_range)

    #print(ranges_accepted)

    sum_possibilities = 0
    for accepted_range in ranges_accepted:
        sum_possibilities += ((accepted_range["x"][1] - accepted_range["x"][0]) + 1) * ((accepted_range["m"][1] - accepted_range["m"][0]) + 1) * ((accepted_range["a"][1] - accepted_range["a"][0]) + 1) * ((accepted_range["s"][1] - accepted_range["s"][0]) + 1)
    
    print(sum_possibilities)

if __name__ == "__main__":
    main()
