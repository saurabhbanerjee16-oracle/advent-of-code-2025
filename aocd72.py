def read_input(filename):
    """Read the manifold diagram from input file."""
    with open(filename, 'r') as f:
        return [list(line.rstrip('\n')) for line in f.readlines()]

def count_timelines(manifold):
    """
    Count all possible timelines for a single quantum tachyon particle.
    
    The particle starts below S and moves downward.
    When it hits a splitter ^, it creates two timelines:
      - In one, it moves left and continues downward
      - In the other, it moves right and continues downward
    We need to count all unique complete paths from start to exit.
    """
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
    
    # Memoization dictionary
    memo = {}
    
    def dfs(r, c, depth=0):
        """Return number of timelines starting from (r, c)."""
        # Base case: exited the grid
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return 1
        
        # Check memo
        if (r, c) in memo:
            return memo[(r, c)]
        
        # Check current cell
        cell = manifold[r][c]
        
        # If we're at a splitter
        if cell == '^':
            # The particle moves horizontally at the splitter row
            # Then continues downward from the new position
            
            # Left timeline: move left, then down
            left_count = dfs(r, c - 1, depth + 1)
            
            # Right timeline: move right, then down
            right_count = dfs(r, c + 1, depth + 1)
            
            result = left_count + right_count
            memo[(r, c)] = result
            return result
        
        # Not a splitter, continue downward
        result = dfs(r + 1, c, depth + 1)
        memo[(r, c)] = result
        return result
    
    # Start from position below S
    return dfs(start_row + 1, start_col)

def main():
    # Read input from input7.txt
    manifold = read_input('input7.txt')
    
    # Count timelines
    timeline_count = count_timelines(manifold)
    
    print(f"Total number of timelines: {timeline_count}")

if __name__ == "__main__":
    main()
