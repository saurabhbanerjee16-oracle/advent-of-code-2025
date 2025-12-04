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
    
    # Create a working copy
    working_grid = [row[:] for row in grid]
    total_removed = 0
    iteration = 0
    
    while True:
        iteration += 1
        # Find all accessible rolls in current state
        accessible_positions = []
        
        for r in range(rows):
            for c in range(cols):
                if working_grid[r][c] == '@':
                    # Count adjacent rolls
                    adjacent_count = 0
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if working_grid[nr][nc] == '@':
                                adjacent_count += 1
                    
                    # Check if accessible (fewer than 4 adjacent rolls)
                    if adjacent_count < 4:
                        accessible_positions.append((r, c))
        
        # If no accessible rolls, we're done
        if not accessible_positions:
            break
        
        # Remove accessible rolls (mark them as '.')
        removed_this_iteration = len(accessible_positions)
        for r, c in accessible_positions:
            working_grid[r][c] = '.'
        
        total_removed += removed_this_iteration
        
        # Optional: print progress
        print(f"Iteration {iteration}: Removed {removed_this_iteration} rolls")
    
    # Final results
    print(f"\nTotal iterations: {iteration-1}")
    print(f"Total rolls in original grid: {sum(row.count('@') for row in grid)}")
    print(f"Total rolls removed: {total_removed}")
    print(f"Rolls remaining: {sum(row.count('@') for row in working_grid)}")
    
    # Show final state
    print("\nFinal state:")
    for row in working_grid:
        print(''.join(row))
    
    # Write results to file
    with open('output4.txt', 'w') as file:
        file.write(f"Total rolls in original grid: {sum(row.count('@') for row in grid)}\n")
        file.write(f"Total rolls removed: {total_removed}\n")
        file.write(f"Rolls remaining: {sum(row.count('@') for row in working_grid)}\n")
        file.write(f"Total iterations: {iteration-1}\n")
        file.write("\nFinal state:\n")
        for row in working_grid:
            file.write(''.join(row) + '\n')
    
    print("\nResults have been written to 'output4.txt'")

if __name__ == "__main__":
    main()
