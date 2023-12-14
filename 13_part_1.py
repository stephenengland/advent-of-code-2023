import math
import pprint

pp = pprint.PrettyPrinter(indent=4)

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()




def main():
    lines = list(read_lines("test_13.txt"))


    current_map = {
        "columns": [],
        "rows": [],
    }

    sum_13 = 0
    def find_reflection(current_map):
        #print(current_map)

        columns = current_map["columns"]
        reflected_req = [columns[0]]

        for i in range(1, len(columns)):
            is_a_reflection = True
            for j in range(0, len(reflected_req)):
                if i + j < len(columns) and reflected_req[j] != columns[i + j]:
                    # Not a reflection yet, keep going in the outer loop
                    is_a_reflection = False
                    break

            if is_a_reflection:
                return i
            else:
                reflected_req.insert(0, columns[i])
        
        rows = current_map["rows"]
        reflected_req = [rows[0]]

        for i in range(1, len(rows)):
            is_a_reflection = True
            for j in range(0, len(reflected_req)):
                if i + j < len(rows) and reflected_req[j] != rows[i + j]:
                    # Not a reflection yet, keep going in the outer loop
                    is_a_reflection = False
                    break

            if is_a_reflection:
                return i * 100
            else:
                reflected_req.insert(0, rows[i])

    for line in lines:
        if len(line.strip()) == 0:
            sum_13 += find_reflection(current_map)
            current_map = {
                "columns": [],
                "rows": [],
            }
        else:
            first_run = not current_map["rows"]
            row = ""
            for (index, c) in enumerate(line.strip()):
                if first_run:
                    current_map["columns"].append(c)
                else:
                    current_map["columns"][index] += c
                row += c
            current_map["rows"].append(row)

    sum_13 += find_reflection(current_map)

    print(f"sum_13:{sum_13}")

if __name__ == "__main__":
    main()