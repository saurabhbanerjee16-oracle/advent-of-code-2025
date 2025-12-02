#program that reads from a file named input.txt

def is_invalid_id(num):
    """
    Check if a number is an invalid ID.
    Invalid IDs have an even number of digits and consist of
    the same digit sequence repeated twice.
    """
    s = str(num)
    length = len(s)
    if length % 2 != 0:
        return False
    half = length // 2
    return s[:half] == s[half:]

def main():
    # Read input from file
    try:
        with open('input.txt', 'r') as file:
            input_str = file.read().strip()
    except FileNotFoundError:
        print("Error: input.txt not found in the current directory.")
        return
    
    # Remove any whitespace or newlines and split by commas
    # Handle the case where the input might have newlines for wrapping
    input_str = input_str.replace('\n', '').replace('\r', '').strip()
    
    # Parse the ranges
    ranges = []
    for r in input_str.split(','):
        r = r.strip()
        if r and '-' in r:
            try:
                start, end = map(int, r.split('-'))
                ranges.append((start, end))
            except ValueError:
                print(f"Warning: Skipping invalid range '{r}'")
    
    if not ranges:
        print("No valid ranges found in input.")
        return
    
    total_sum = 0
    
    print("Invalid IDs found in each range:")
    print("=" * 60)
    
    # Process each range
    for idx, (start, end) in enumerate(ranges, 1):
        invalid_ids = []
        
        # Check every number in the range
        for num in range(start, end + 1):
            if is_invalid_id(num):
                invalid_ids.append(num)
                total_sum += num
        
        # Display results for this range
        if invalid_ids:
            print(f"Range {idx}: {start:,}-{end:,}")
            print(f"  Invalid IDs: {', '.join(f'{n:,}' for n in invalid_ids)}")
            print(f"  Count: {len(invalid_ids)}, Sum: {sum(invalid_ids):,}")
        else:
            print(f"Range {idx}: {start:,}-{end:,}")
            print(f"  No invalid IDs found")
        print()
    
    print("=" * 60)
    print(f"TOTAL SUM OF ALL INVALID IDs: {total_sum:,}")
    
    # Optional: Show all invalid IDs in one list
    print("\n" + "=" * 60)
    print("SUMMARY:")
    
    all_invalid = []
    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id(num):
                all_invalid.append(num)
    
    if all_invalid:
        print(f"Found {len(all_invalid)} invalid IDs total")
        print(f"All invalid IDs (sorted): {sorted(all_invalid)}")
    else:
        print("No invalid IDs found in any range")

if __name__ == "__main__":
    main()
