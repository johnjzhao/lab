def countMax(upRight):
    rows, cols = 0, 0

    # Process each coordinate and determine the final size of the grid
    for coord in upRight:
        r, c = map(int, coord.split())
        rows = max(rows, r)
        cols = max(cols, c)

    # Create the grid and fill it with zeros
    grid = [[0] * (cols + 1) for _ in range(rows + 1)]
    print (grid)

    # Update the grid based on the coordinates
    for coord in upRight:
        r, c = map(int, coord.split())
        for i in range(1, r + 1):
            for j in range(1, c + 1):
                grid[i][j] += 1

    # Find the maximal element in the grid
    max_element = max(max(row) for row in grid)

    # Count occurrences of the maximal element
    count_max = sum(row.count(max_element) for row in grid)

    return count_max

# Sample Input
upRight = ["3 2", "3 7", "4 1"]

# Sample Output
result = countMax(upRight)
print(result)

