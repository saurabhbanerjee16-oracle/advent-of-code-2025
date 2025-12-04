def main():
    # Read input from file
    try:
        with open('input4.txt', 'r') as file:
            grid = [list(line.strip()) for line in file if line.strip()]
    except FileNotFoundError:
        print("Error: input4.txt not found in the current directory.")
        return
    
    if not grid:
        print("The input file is empty.")
        return
    
    rows = len(grid)
    cols = len(grid[0])
    
    # Directions for 8 adjacent positions
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    
    # Create a copy to mark accessible rolls
    result_grid = [row[:] for row in grid]
    accessible_count = 0
    
    # Check each position in the grid
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                # Count adjacent rolls
                adjacent_count = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == '@':
                            adjacent_count += 1
                
                # Check if accessible (fewer than 4 adjacent rolls)
                if adjacent_count < 4:
                    result_grid[r][c] = 'x'  # Mark as accessible
                    accessible_count += 1
                else:
                    result_grid[r][c] = '@'  # Keep as original
    
    # Print results
    print("Original grid:")
    for row in grid:
        print(''.join(row))
    
    print(f"\nGrid with accessible rolls marked (x):")
    for row in result_grid:
        print(''.join(row))
    
    print(f"\nTotal rolls of paper (@): {sum(row.count('@') for row in grid)}")
    print(f"Accessible rolls: {accessible_count}")
    
    # Show positions of accessible rolls
    print("\nPositions of accessible rolls (row, column, 0-indexed):")
    for r in range(rows):
        for c in range(cols):
            if result_grid[r][c] == 'x':
                print(f"({r}, {c})")
    
    # Write output to file
    with open('output4.txt', 'w') as file:
        file.write("Grid with accessible rolls marked (x):\n")
        for row in result_grid:
            file.write(''.join(row) + '\n')
        file.write(f"\nTotal rolls of paper (@): {sum(row.count('@') for row in grid)}\n")
        file.write(f"Accessible rolls: {accessible_count}\n")
    
    print("\nResults have also been written to 'output4.txt'")

if __name__ == "__main__":
    main()
