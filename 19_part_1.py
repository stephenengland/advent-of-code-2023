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

def apply_rules(rules, item):
    for rule in rules:
        if rule.is_instruction():
            return rule.direction
        val_to_compare = item[rule.xmas_type]

        if rule.condition == '>':
            if val_to_compare > rule.value:
                return rule.direction
        elif rule.condition == '<':
            if val_to_compare < rule.value:
                return rule.direction

def main():
    lines = list(read_lines("test_19.txt"))

    rules_dict = {}
    items = []
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

        elif line.strip():
            types = line.strip().replace('{', '').replace('}', '').split(',')
            xmas_types = {}
            for t in types:
                [name, val] = t.strip().split('=')
                xmas_types[name] = int(val)

            items.append((xmas_types, 'in'))

    sum_ratings = 0
    current_item_list = items
    while current_item_list:
        (next_item, rule) = current_item_list.pop()

        new_rule = apply_rules(rules_dict[rule], next_item)

        if new_rule == 'A':
            for val in next_item.values():
                sum_ratings += val
        elif new_rule != 'R':
            current_item_list.append((next_item, new_rule))
    
    print(sum_ratings)



if __name__ == "__main__":
    main()