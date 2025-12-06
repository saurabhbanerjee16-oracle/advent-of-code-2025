def solve():
    with open('input6.txt', 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    # Pad lines to equal length
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    num_rows = len(lines)
    num_cols = max_len

    # Find columns that are all spaces (separators)
    separator_cols = []
    for c in range(num_cols):
        if all(lines[r][c] == ' ' for r in range(num_rows)):
            separator_cols.append(c)

    # Problems are between separator columns
    # We need to slice from start to end, where start is 0 or separator+1
    problem_slices = []
    start = 0
    for c in separator_cols:
        if start < c:
            problem_slices.append((start, c - 1))
        start = c + 1
    if start < num_cols:
        problem_slices.append((start, num_cols - 1))

    grand_total = 0

    for cstart, cend in problem_slices:
        numbers = []
        # Last line is operator line
        for r in range(num_rows - 1):
            digits = []
            for c in range(cstart, cend + 1):
                ch = lines[r][c]
                if ch.isdigit():
                    digits.append(ch)
            if digits:
                num_str = ''.join(digits)
                numbers.append(int(num_str))
            else:
                # In case a number is missing? Should not happen
                numbers.append(0)

        # Operator from last line
        op = None
        for c in range(cstart, cend + 1):
            ch = lines[num_rows - 1][c]
            if ch == '+' or ch == '*':
                op = ch
                break

        if op is None:
            continue  # no operator found

        # Compute problem result
        if op == '+':
            result = sum(numbers)
        else:  # '*'
            result = 1
            for n in numbers:
                result *= n

        grand_total += result

    print(grand_total)

if __name__ == "__main__":
    solve()
