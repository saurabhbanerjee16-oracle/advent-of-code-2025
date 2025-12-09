import sys
from typing import List, Tuple, Set

def read_input(filename: str) -> Set[Tuple[int, int]]:
    """Read input file and return set of red tile coordinates."""
    red_tiles = set()
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(','))
                red_tiles.add((x, y))
    return red_tiles

def find_largest_rectangle(red_tiles: Set[Tuple[int, int]]) -> int:
    """
    Find the largest rectangle that can be formed using two red tiles
    as opposite corners.
    """
    max_area = 0
    
    # Convert to list for easier iteration
    tiles_list = list(red_tiles)
    
    # Try all pairs of red tiles as potential opposite corners
    for i in range(len(tiles_list)):
        x1, y1 = tiles_list[i]
        for j in range(i + 1, len(tiles_list)):
            x2, y2 = tiles_list[j]
            
            # For a valid rectangle, the two points must be diagonal to each other
            # (not on the same horizontal or vertical line)
            # But actually, thin rectangles ARE allowed (same row or same column)
            
            # For any two red tiles, they can be opposite corners if:
            # 1. They define a rectangle (which any two points do if we allow 0 width/height)
            # 2. The rectangle is axis-aligned
            
            # Calculate the corners of the rectangle
            # The rectangle will have corners at:
            # (min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)
            
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            min_y = min(y1, y2)
            max_y = max(y1, y2)
            
            # Now check: are our two red tiles the opposite corners?
            # They are opposite corners if:
            # - One is (min_x, min_y) and the other is (max_x, max_y) OR
            # - One is (min_x, max_y) and the other is (max_x, min_y)
            
            if ((x1 == min_x and y1 == min_y and x2 == max_x and y2 == max_y) or
                (x1 == min_x and y1 == max_y and x2 == max_x and y2 == min_y) or
                (x1 == max_x and y1 == max_y and x2 == min_x and y2 == min_y) or
                (x1 == max_x and y1 == min_y and x2 == min_x and y2 == max_y)):
                
                # Calculate area
                width = max_x - min_x + 1
                height = max_y - min_y + 1
                area = width * height
                
                max_area = max(max_area, area)
    
    return max_area

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 aocd91.py input9.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        red_tiles = read_input(input_file)
        largest_area = find_largest_rectangle(red_tiles)
        print(f"Largest rectangle area: {largest_area}")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
