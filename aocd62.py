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
        # Operator from last line
        op = None
        for c in range(cstart, cend + 1):
            ch = lines[num_rows - 1][c]
            if ch == '+' or ch == '*':
                op = ch
                break
        if op is None:
            continue

        # For each character column in slice, read top to bottom digits
        column_numbers = []
        for c in range(cstart, cend + 1):
            digits = []
            for r in range(num_rows - 1):  # exclude operator line
                ch = lines[r][c]
                if ch.isdigit():
                    digits.append(ch)
            # If there are digits, form number
            if digits:
                num_str = ''.join(digits)
                column_numbers.append(int(num_str))
            else:
                column_numbers.append(0)  # no digits means 0

        # Reverse for right-to-left
        column_numbers.reverse()

        # Compute result
        if op == '+':
            result = sum(column_numbers)
        else:  # '*'
            result = 1
            for n in column_numbers:
                result *= n

        grand_total += result

    print(grand_total)

if __name__ == "__main__":
    solve()
