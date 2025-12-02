#!/usr/bin/env python3

def is_invalid_id(num):
    s = str(num)
    length = len(s)
    for pattern_len in range(1, length // 2 + 1):
        if length % pattern_len != 0:
            continue
        repetitions = length // pattern_len
        if repetitions < 2:
            continue
        pattern = s[:pattern_len]
        if pattern * repetitions == s:
            return True
    return False

def main():
    try:
        with open('input.txt', 'r') as file:
            input_str = file.read().strip()
    except FileNotFoundError:
        print("Error: input.txt not found.")
        return
    
    input_str = input_str.replace('\n', '').replace('\r', '').strip()
    
    ranges = []
    for r in input_str.split(','):
        r = r.strip()
        if r and '-' in r:
            try:
                start, end = map(int, r.split('-'))
                ranges.append((start, end))
            except ValueError:
                continue
    
    total_sum = 0
    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id(num):
                total_sum += num
    
    print(f"Total sum: {total_sum}")

if __name__ == "__main__":
    main()
