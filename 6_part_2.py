import math

def read_lines(filename):
    file = open(filename, 'r')
    for line in file.readlines():
        yield line
    file.close()




def main():
    lines = list(read_lines("test_6.txt"))
    product = None

    times = []
    distances = []
    for line in lines:
        [label, contents] = line.strip().split(':')

        content = int(contents.strip().replace(' ', '').strip())
        if label.strip() == "Time":
            times.append(content)
        else:
            distances.append(content)
    
    for index, time in enumerate(times):
        distance = distances[index]

        methods = 0
        for t in range(1, time):
            remainder = time - t

            if remainder * t > distance:
                methods += 1
        
        if product is None:
            product = methods
        else:
            product *= methods
        

    print(f"product:{product}")

if __name__ == "__main__":
    main()