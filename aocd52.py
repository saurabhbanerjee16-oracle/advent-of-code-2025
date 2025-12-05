def main():
    with open('input5.txt', 'r') as file:
        content = file.read().strip()
    
    # Get only the ranges part (before blank line)
    parts = content.split('\n\n')
    if len(parts) < 2:
        # If no blank line, take all lines with dashes as ranges
        ranges_text = content
    else:
        ranges_text = parts[0]
    
    # Parse ranges
    ranges = []
    for line in ranges_text.split('\n'):
        if '-' in line:
            start, end = map(int, line.strip().split('-'))
            ranges.append((start, end))
    
    # Sort ranges by start value
    ranges.sort(key=lambda x: x[0])
    
    # Merge overlapping ranges
    merged = []
    if ranges:
        current_start, current_end = ranges[0]
        
        for start, end in ranges[1:]:
            if start <= current_end + 1:  # Overlapping or adjacent
                current_end = max(current_end, end)
            else:
                merged.append((current_start, current_end))
                current_start, current_end = start, end
        
        merged.append((current_start, current_end))
    
    # Count total IDs
    total_fresh = sum(end - start + 1 for start, end in merged)
    
    print(f"Number of fresh ingredient IDs according to ranges: {total_fresh}")
    
    # Optional: Show merged ranges
    print(f"Merged ranges: {merged}")

if __name__ == "__main__":
    main()
