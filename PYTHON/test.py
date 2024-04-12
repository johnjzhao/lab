def two_dimensions(coordinates, n):
    max_and_count = []
    grid = [[0 for _ in range(n)] for _ in range(n)]
    arr_length = len(coordinates)
    max_val = float('-inf')
    count = 1

    for i in range(arr_length):
        coors = coordinates[i].split()
        row = int(coors[0])
        column = int(coors[1])

        for j in range(row):
            for k in range(column):
                grid[j][k] += 1
                print(f"grid ({j},{k}): {grid[j][k]}")

                if not (j == 0 and k == 0) and grid[j][k] > max_val:
                    max_val = grid[j][k]
                    count = 1
                elif grid[j][k] == max_val:
                    count += 1

    max_and_count.append(max_val)
    max_and_count.append(count)

    return max_and_count

def main():
    coordinates = ["1 4", "2 3", "4 1"]
    print(f"The Max and count Are: {two_dimensions(coordinates, 8)}")

if __name__ == "__main__":
    main()

