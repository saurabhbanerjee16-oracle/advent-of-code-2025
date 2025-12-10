import sys
import re
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpInteger, PULP_CBC_CMD

def parse_line(line):
    """Parse a line into button sets and target values."""
    # Remove brackets and split
    pattern_part = re.search(r'\[(.*?)\]', line)
    if pattern_part:
        line = line[line.find(']') + 1:].strip()
    
    # Split into buttons and targets
    parts = line.split('{')
    left_part = parts[0].strip()
    right_part = parts[1].rstrip('}').strip()
    
    # Parse buttons: (a,b,c)
    buttons = []
    for match in re.finditer(r'\(([^)]+)\)', left_part):
        indices = tuple(map(int, match.group(1).split(',')))
        buttons.append(indices)
    
    # Parse targets
    targets = list(map(int, right_part.split(',')))
    
    return buttons, targets

def solve_machine(buttons, targets):
    """Solve for minimal presses for one machine."""
    m = len(targets)  # number of counters
    n = len(buttons)  # number of buttons
    
    # Create problem
    prob = LpProblem("Machine", LpMinimize)
    
    # Variables: x[j] >= 0, integer
    x = [LpVariable(f"x{j}", lowBound=0, cat=LpInteger) for j in range(n)]
    
    # Objective: minimize total presses
    prob += lpSum(x)
    
    # Constraints: for each counter i, sum over buttons affecting i = target[i]
    for i in range(m):
        # Find all buttons j that affect counter i
        coeffs = []
        for j in range(n):
            if i in buttons[j]:
                coeffs.append(x[j])
        if coeffs:
            prob += lpSum(coeffs) == targets[i]
        else:
            # If no button affects this counter but target > 0, impossible
            if targets[i] > 0:
                # This machine can't be solved, return large penalty or handle
                return None
    
    # Solve
    solver = PULP_CBC_CMD(msg=False)
    prob.solve(solver)
    
    # Return total presses (objective value)
    return int(prob.objective.value())

def main():
    if len(sys.argv) != 2:
        print("Usage: python solution.py input10.txt")
        return
    
    filename = sys.argv[1]
    total_presses = 0
    
    with open(filename, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                buttons, targets = parse_line(line)
                min_presses = solve_machine(buttons, targets)
                if min_presses is None:
                    print(f"Warning: Machine {line_num} has no solution")
                else:
                    total_presses += min_presses
                    # Optional: print per-machine result
                    # print(f"Machine {line_num}: {min_presses}")
            except Exception as e:
                print(f"Error parsing line {line_num}: {e}")
                continue
    
    print(total_presses)

if __name__ == "__main__":
    main()
