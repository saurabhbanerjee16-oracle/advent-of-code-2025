def main():
    with open('input5.txt', 'r') as file:
        content = file.read().strip()
    
    # Split content into two parts
    parts = content.split('\n\n')
    
    # If file doesn't have a blank line separator
    if len(parts) < 2:
        lines = [line for line in content.split('\n') if line.strip()]
        # Find where ranges end and IDs begin
        separator_index = 0
        for i, line in enumerate(lines):
            if '-' not in line:
                separator_index = i
                break
        
        ranges = lines[:separator_index]
        ids = lines[separator_index:]
    else:
        ranges = parts[0].split('\n')
        ids = parts[1].split('\n')
    
    # Parse ranges
    parsed_ranges = []
    for r in ranges:
        if '-' in r:
            start, end = map(int, r.split('-'))
            parsed_ranges.append((start, end))
    
    # Count fresh ingredients
    fresh_count = 0
    for id_str in ids:
        if id_str:
            ingredient_id = int(id_str)
            if any(start <= ingredient_id <= end for start, end in parsed_ranges):
                fresh_count += 1
    
    print(f"Number of fresh ingredient IDs: {fresh_count}")

if __name__ == "__main__":
    main()
