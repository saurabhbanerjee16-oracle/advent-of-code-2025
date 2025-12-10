import sys
import re
import numpy as np

def parse_line(line):
    # Extract parts
    pattern = r'\[([.#]+)\]|\(([\d,]+)\)|{([\d,]+)}'
    matches = re.findall(pattern, line)
    
    diagram = ''
    buttons = []
    joltages = []
    
    for m in matches:
        if m[0]:  # diagram
            diagram = m[0]
        elif m[1]:  # button
            nums = tuple(map(int, m[1].split(',')))
            buttons.append(nums)
        elif m[2]:  # joltages
            joltages = list(map(int, m[2].split(',')))
    
    return diagram, buttons, joltages

def solve_machine(diagram, buttons):
    n_lights = len(diagram)
    n_buttons = len(buttons)
    
    # Target vector from diagram: 1 for # (on), 0 for . (off)
    target = [1 if c == '#' else 0 for c in diagram]
    
    # Build coefficient matrix A: A[i][j] = 1 if button j toggles light i
    A = [[0] * n_buttons for _ in range(n_lights)]
    for j, btn in enumerate(buttons):
        for idx in btn:
            if idx < n_lights:
                A[idx][j] = 1
    
    # Convert to numpy for Gaussian elimination over GF(2)
    A_mat = np.array(A, dtype=int)
    b_vec = np.array(target, dtype=int)
    
    # Gaussian elimination over GF(2)
    # We'll solve for x where A*x ≡ b (mod 2)
    # and find solution with minimal number of 1's (button presses)
    
    # Augmented matrix
    aug = np.column_stack((A_mat, b_vec))
    rows, cols = aug.shape
    
    # Forward elimination
    row = 0
    for col in range(n_buttons):
        # Find pivot
        pivot = None
        for r in range(row, n_lights):
            if aug[r, col] == 1:
                pivot = r
                break
        if pivot is None:
            continue
        
        # Swap rows
        aug[[row, pivot]] = aug[[pivot, row]]
        
        # Eliminate other rows
        for r in range(n_lights):
            if r != row and aug[r, col] == 1:
                aug[r] ^= aug[row]
        
        row += 1
        if row == n_lights:
            break
    
    # Check for consistency
    for r in range(row, n_lights):
        if aug[r, -1] != 0:
            # No solution
            return None
    
    # Back substitution to find a solution
    # We'll find the solution with minimum weight (number of 1's)
    # by trying to set free variables to 0 first
    
    solution = [0] * n_buttons
    used_rows = []
    
    for col in range(n_buttons):
        # Find row with this as pivot
        pivot_row = None
        for r in range(n_lights):
            if aug[r, col] == 1:
                pivot_row = r
                used_rows.append(r)
                break
        
        if pivot_row is not None:
            # This is a pivot column
            # The value is determined by augmented column
            solution[col] = aug[pivot_row, -1]
    
    # Verify solution works (optional)
    # Verify by multiplying A * solution mod 2
    verify = [sum(A_mat[i, j] * solution[j] for j in range(n_buttons)) % 2
              for i in range(n_lights)]
    if verify != target:
        # Try to find solution via brute force for small cases
        # This handles cases where Gaussian elimination alone doesn't give minimal weight
        return solve_small_brute(diagram, buttons)
    
    # Count presses (sum of solution)
    presses = sum(solution)
    
    # Try to reduce further by combining with nullspace vectors
    # For small n_buttons, we can brute force minimal solution
    if n_buttons <= 20:
        presses = min(presses, brute_force_min(diagram, buttons))
    
    return presses

def brute_force_min(diagram, buttons):
    n_lights = len(diagram)
    n_buttons = len(buttons)
    target = [1 if c == '#' else 0 for c in diagram]
    
    min_presses = float('inf')
    
    # Try all button press combinations (0 or 1 presses each)
    for mask in range(1 << n_buttons):
        presses = bin(mask).count('1')
        if presses >= min_presses:
            continue
        
        # Simulate lights
        lights = [0] * n_lights
        for btn_idx in range(n_buttons):
            if mask >> btn_idx & 1:
                for light_idx in buttons[btn_idx]:
                    if light_idx < n_lights:
                        lights[light_idx] ^= 1
        
        if lights == target:
            min_presses = presses
    
    return min_presses if min_presses != float('inf') else None

def solve_small_brute(diagram, buttons):
    # Brute force for when Gaussian elimination fails
    return brute_force_min(diagram, buttons)

def solve_file(filename):
    total = 0
    with open(filename, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            diagram, buttons, _ = parse_line(line)
            presses = solve_machine(diagram, buttons)
            
            if presses is None:
                print(f"Line {line_num}: No solution found")
                continue
            
            total += presses
            print(f"Line {line_num}: {presses} presses")
    
    print(f"\nTotal: {total}")
    return total

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python solution.py input10.txt")
        sys.exit(1)
    
    solve_file(sys.argv[1])
