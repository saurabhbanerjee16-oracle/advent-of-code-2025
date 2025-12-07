def read_input(filename):
    """Read the manifold diagram from input file."""
    with open(filename, 'r') as f:
        return [list(line.rstrip('\n')) for line in f.readlines()]

def simulate_manifold(manifold):
    """Simulate the tachyon beam propagation through the manifold."""
    rows = len(manifold)
    cols = len(manifold[0])
    
    # Find starting position 'S'
    start_row, start_col = None, None
    for r in range(rows):
        for c in range(cols):
            if manifold[r][c] == 'S':
                start_row, start_col = r, c
                break
        if start_row is not None:
            break
    
    # Count splits
    split_count = 0
    # Active beams: (row, col) positions
    active_beams = [(start_row + 1, start_col)]  # Beams always move downward from S
    
    # Track positions that already have a beam to avoid counting duplicate splits
    has_beam = [[False] * cols for _ in range(rows)]
    has_beam[start_row + 1][start_col] = True
    
    # Process beams until none are active
    while active_beams:
        new_beams = []
        
        for row, col in active_beams:
            # Move beam downward
            if row < rows:
                if manifold[row][col] == '^':  # Splitter encountered
                    split_count += 1
                    
                    # Emit beams to left and right
                    left_col = col - 1
                    right_col = col + 1
                    
                    # Left beam
                    if left_col >= 0 and not has_beam[row][left_col]:
                        new_beams.append((row, left_col))
                        has_beam[row][left_col] = True
                    
                    # Right beam
                    if right_col < cols and not has_beam[row][right_col]:
                        new_beams.append((row, right_col))
                        has_beam[row][right_col] = True
                else:
                    # Continue moving downward
                    next_row = row + 1
                    if next_row < rows and not has_beam[next_row][col]:
                        new_beams.append((next_row, col))
                        has_beam[next_row][col] = True
        
        active_beams = new_beams
    
    return split_count

def visualize_manifold(manifold, has_beam):
    """Create a visualization of the beam propagation (optional)."""
    rows = len(manifold)
    cols = len(manifold[0])
    
    result = []
    for r in range(rows):
        row_str = []
        for c in range(cols):
            if has_beam[r][c]:
                # Show beam position
                if manifold[r][c] == '.':
                    row_str.append('|')
                elif manifold[r][c] == '^':
                    row_str.append('^')
                elif manifold[r][c] == 'S':
                    row_str.append('S')
            else:
                # Show original character
                row_str.append(manifold[r][c])
        result.append(''.join(row_str))
    return result

def main():
    # Read input from input7.txt
    manifold = read_input('input7.txt')
    
    # Count splits
    split_count = simulate_manifold(manifold)
    
    print(f"Total beam splits: {split_count}")
    
    # Optional: Print the final state visualization
    print("\nFinal beam propagation:")
    rows = len(manifold)
    cols = len(manifold[0])
    
    # Re-run to get visualization
    start_row, start_col = None, None
    for r in range(rows):
        for c in range(cols):
            if manifold[r][c] == 'S':
                start_row, start_col = r, c
                break
    
    has_beam = [[False] * cols for _ in range(rows)]
    has_beam[start_row + 1][start_col] = True
    active_beams = [(start_row + 1, start_col)]
    
    while active_beams:
        new_beams = []
        for row, col in active_beams:
            if row < rows:
                if manifold[row][col] == '^':
                    left_col = col - 1
                    right_col = col + 1
                    
                    if left_col >= 0 and not has_beam[row][left_col]:
                        new_beams.append((row, left_col))
                        has_beam[row][left_col] = True
                    
                    if right_col < cols and not has_beam[row][right_col]:
                        new_beams.append((row, right_col))
                        has_beam[row][right_col] = True
                else:
                    next_row = row + 1
                    if next_row < rows and not has_beam[next_row][col]:
                        new_beams.append((next_row, col))
                        has_beam[next_row][col] = True
        active_beams = new_beams
    
    # Print visualization
    visualization = visualize_manifold(manifold, has_beam)
    for line in visualization:
        print(line)

if __name__ == "__main__":
    main()
