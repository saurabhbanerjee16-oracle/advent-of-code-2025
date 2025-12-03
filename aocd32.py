#!/usr/bin/env python3
import sys

def find_max_12_digits(bank_str):
    """
    Find largest 12-digit number by selecting 12 digits in order.
    Uses greedy algorithm: at each position, pick the largest digit
    while leaving enough digits for remaining positions.
    """
    digits = [int(d) for d in bank_str]
    n = len(digits)
    k = 12
    
    result = []
    start = 0
    
    for i in range(k):
        # We need to leave (k - i - 1) digits after current selection
        end = n - (k - i - 1)
        
        # Find max digit in window [start, end)
        max_digit = -1
        max_pos = -1
        
        for pos in range(start, end):
            if digits[pos] > max_digit:
                max_digit = digits[pos]
                max_pos = pos
        
        result.append(max_digit)
        start = max_pos + 1
    
    # Convert list of digits to integer
    return int(''.join(str(d) for d in result))

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <input_file>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        banks = [line.strip() for line in f if line.strip()]
    
    total = 0
    for bank in banks:
        total += find_max_12_digits(bank)
    
    print("Total output joltage (12 batteries): {:,}".format(total))
    
    with open("output3_part2.txt", 'w') as f:
        f.write(str(total))
    
    return total

if __name__ == "__main__":
    main()
