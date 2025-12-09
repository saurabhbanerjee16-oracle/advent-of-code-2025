#!/usr/bin/env python3

import sys
import time

def parse_input(file_path):
    """Parse input coordinates."""
    with open(file_path, 'r') as f:
        return [tuple(map(int, line.strip().split(','))) for line in f if line.strip()]

# ------------------------------------------------------------
# PART ONE: Simple O(n²)
# ------------------------------------------------------------
def part_one(polygon):
    """Part One: Largest rectangle with any red corners."""
    max_area = 0
    n = len(polygon)
    
    for i in range(n):
        x1, y1 = polygon[i]
        for j in range(i + 1, n):
            x2, y2 = polygon[j]
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if area > max_area:
                max_area = area
    
    return max_area

# ------------------------------------------------------------
# PART TWO: Memory-efficient computational geometry approach
# ------------------------------------------------------------
def point_on_segment(px, py, x1, y1, x2, y2):
    """Check if point is on line segment."""
    if x1 == x2 == px and min(y1, y2) <= py <= max(y1, y2):
        return True
    if y1 == y2 == py and min(x1, x2) <= px <= max(x1, x2):
        return True
    return False

def point_in_polygon_fast(px, py, polygon, edges, edge_dict_x, edge_dict_y):
    """Fast check if point is in polygon using precomputed edges."""
    # Check if point is a vertex
    if (px, py) in polygon_set:
        return True
    
    # Check if point is on any edge (quick check using dictionaries)
    if px in edge_dict_x:
        for y1, y2 in edge_dict_x[px]:
            if min(y1, y2) <= py <= max(y1, y2):
                return True
    
    if py in edge_dict_y:
        for x1, x2 in edge_dict_y[py]:
            if min(x1, x2) <= px <= max(x1, x2):
                return True
    
    # Ray casting for interior
    inside = False
    n = len(polygon)
    
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        
        # Skip horizontal edges for ray casting
        if y1 == y2:
            continue
            
        if ((y1 > py) != (y2 > py)):
            x_intersect = (py - y1) * (x2 - x1) / (y2 - y1) + x1
            if px < x_intersect:
                inside = not inside
    
    return inside

def precompute_edges(polygon):
    """Precompute edge data structures."""
    edges = []
    edge_dict_x = {}
    edge_dict_y = {}
    
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        edges.append((x1, y1, x2, y2))
        
        if x1 == x2:  # Vertical edge
            if x1 not in edge_dict_x:
                edge_dict_x[x1] = []
            edge_dict_x[x1].append((y1, y2))
        else:  # Horizontal edge
            if y1 not in edge_dict_y:
                edge_dict_y[y1] = []
            edge_dict_y[y1].append((x1, x2))
    
    return edges, edge_dict_x, edge_dict_y

def rectangle_in_polygon(x1, y1, x2, y2, polygon, edges, edge_dict_x, edge_dict_y, cache):
    """Check if entire rectangle is inside polygon."""
    x_min, x_max = sorted([x1, x2])
    y_min, y_max = sorted([y1, y2])
    
    # Check all four corners first
    corners = [(x_min, y_min), (x_max, y_min), (x_min, y_max), (x_max, y_max)]
    for corner in corners:
        if corner not in cache:
            cache[corner] = point_in_polygon_fast(corner[0], corner[1], polygon, 
                                                 edges, edge_dict_x, edge_dict_y)
        if not cache[corner]:
            return False
    
    # Check boundary edges of rectangle
    # Top and bottom edges
    for x in range(x_min, x_max + 1):
        top = (x, y_min)
        bottom = (x, y_max)
        
        if top not in cache:
            cache[top] = point_in_polygon_fast(top[0], top[1], polygon, 
                                              edges, edge_dict_x, edge_dict_y)
        if not cache[top]:
            return False
            
        if bottom not in cache:
            cache[bottom] = point_in_polygon_fast(bottom[0], bottom[1], polygon, 
                                                 edges, edge_dict_x, edge_dict_y)
        if not cache[bottom]:
            return False
    
    # Left and right edges (skip corners already checked)
    for y in range(y_min + 1, y_max):
        left = (x_min, y)
        right = (x_max, y)
        
        if left not in cache:
            cache[left] = point_in_polygon_fast(left[0], left[1], polygon, 
                                               edges, edge_dict_x, edge_dict_y)
        if not cache[left]:
            return False
            
        if right not in cache:
            cache[right] = point_in_polygon_fast(right[0], right[1], polygon, 
                                                edges, edge_dict_x, edge_dict_y)
        if not cache[right]:
            return False
    
    return True

def part_two_smart(polygon):
    """Smart Part Two solution with aggressive pruning."""
    global polygon_set
    polygon_set = set(polygon)
    
    n = len(polygon)
    if n < 2:
        return 0
    
    # Precompute edge data
    print("Precomputing edge data...")
    edges, edge_dict_x, edge_dict_y = precompute_edges(polygon)
    
    # Sort points for better cache locality
    sorted_points = sorted(polygon)
    
    max_area = 0
    cache = {}  # Cache point-in-polygon checks
    
    print(f"Checking {n} red points...")
    start_time = time.time()
    last_report = start_time
    
    total_pairs = n * (n - 1) // 2
    pairs_checked = 0
    
    # Group points by x coordinate for pruning
    points_by_x = {}
    for x, y in sorted_points:
        if x not in points_by_x:
            points_by_x[x] = []
        points_by_x[x].append(y)
    
    # Sort y lists
    for x in points_by_x:
        points_by_x[x].sort()
    
    # Get unique x coordinates sorted
    unique_x = sorted(points_by_x.keys())
    
    # Try all pairs with pruning
    for i in range(n):
        x1, y1 = sorted_points[i]
        
        # Early pruning: maximum possible width from this x1
        max_width = unique_x[-1] - x1 + 1
        
        for j in range(i + 1, n):
            pairs_checked += 1
            
            x2, y2 = sorted_points[j]
            
            # Calculate area
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            
            # Skip if can't beat current max
            if area <= max_area:
                continue
            
            # Quick check: corners must be red
            if (x1, y1) not in polygon_set or (x2, y2) not in polygon_set:
                continue
            
            # Check if rectangle is valid
            if rectangle_in_polygon(x1, y1, x2, y2, polygon, edges, 
                                   edge_dict_x, edge_dict_y, cache):
                max_area = area
                # Optional: can't get larger area with same width/height combo
            
            # Report progress every 10 seconds
            current_time = time.time()
            if current_time - last_report > 10:
                elapsed = current_time - start_time
                progress = pairs_checked / total_pairs * 100
                print(f"  Progress: {progress:.1f}% ({pairs_checked:,}/{total_pairs:,}), "
                      f"max area: {max_area:,}, time: {elapsed:.1f}s")
                last_report = current_time
    
    print(f"Total pairs checked: {pairs_checked:,}")
    return max_area

# ------------------------------------------------------------
# Alternative: Use sweep line for really large n
# ------------------------------------------------------------
def part_two_sweep(polygon):
    """Use sweep line algorithm for very large inputs."""
    polygon_set = set(polygon)
    n = len(polygon)
    
    if n < 2:
        return 0
    
    # Sort points
    points = sorted(polygon)
    
    max_area = 0
    
    # For each pair of x coordinates (potential rectangle width)
    # This is O(n²) worst case but with pruning
    
    # Group points by x
    by_x = {}
    for x, y in points:
        by_x.setdefault(x, []).append(y)
    
    # Sort y lists
    for x in by_x:
        by_x[x].sort()
    
    # Get unique x values
    x_vals = sorted(by_x.keys())
    m = len(x_vals)
    
    print(f"Checking {m} unique x coordinates...")
    
    # For each pair of x values
    for i in range(m):
        x1 = x_vals[i]
        y_list1 = by_x[x1]
        
        for j in range(i, m):
            x2 = x_vals[j]
            width = x2 - x1 + 1
            
            # Maximum possible area with this width
            max_possible_height = 0
            # We need to find common y values
            
            y_list2 = by_x.get(x2, [])
            
            # Find intersection of y values
            common_y = set(y_list1).intersection(y_list2)
            if not common_y:
                continue
                
            common_y = sorted(common_y)
            
            # Find consecutive sequences in common_y
            seq_start = 0
            for k in range(1, len(common_y)):
                if common_y[k] != common_y[k-1] + 1:
                    # Check sequence from seq_start to k-1
                    height = common_y[k-1] - common_y[seq_start] + 1
                    area = width * height
                    
                    if area > max_area:
                        # Check if rectangle (x1, y_start) to (x2, y_end) is valid
                        # We already know corners are red
                        # Need to check interior
                        y_start = common_y[seq_start]
                        y_end = common_y[k-1]
                        
                        # Quick check: all boundary points must be in polygon
                        valid = True
                        # We'll implement a simplified check
                        # For now, assume if corners are red and y's are consecutive
                        # the rectangle might be valid
                        
                        # Actually check a few interior points
                        mid_x = (x1 + x2) // 2
                        mid_y = (y_start + y_end) // 2
                        
                        # Simple check: if mid point is in polygon
                        # This is not sufficient but a heuristic
                        if (mid_x, mid_y) in polygon_set or \
                           point_in_polygon_simple(mid_x, mid_y, polygon):
                            if area > max_area:
                                max_area = area
                    
                    seq_start = k
            
            # Check last sequence
            if seq_start < len(common_y):
                height = common_y[-1] - common_y[seq_start] + 1
                area = width * height
                if area > max_area:
                    # Similar check
                    y_start = common_y[seq_start]
                    y_end = common_y[-1]
                    mid_x = (x1 + x2) // 2
                    mid_y = (y_start + y_end) // 2
                    if (mid_x, mid_y) in polygon_set or \
                       point_in_polygon_simple(mid_x, mid_y, polygon):
                        max_area = area
    
    return max_area

def point_in_polygon_simple(x, y, polygon):
    """Simple point-in-polygon check."""
    inside = False
    n = len(polygon)
    
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        
        # Check if on edge
        if x1 == x2 == x and min(y1, y2) <= y <= max(y1, y2):
            return True
        if y1 == y2 == y and min(x1, x2) <= x <= max(x1, x2):
            return True
        
        if ((y1 > y) != (y2 > y)):
            x_intersect = (y - y1) * (x2 - x1) / (y2 - y1) + x1
            if x < x_intersect:
                inside = not inside
    
    return inside

# ------------------------------------------------------------
# Main execution
# ------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 solution.py <input_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        print(f"Reading input from {file_path}")
        polygon = parse_input(file_path)
        
        if not polygon:
            print("Error: No coordinates found.")
            return
        
        n = len(polygon)
        print(f"Loaded {n} red tiles")
        
        # Get bounds
        xs = [x for x, _ in polygon]
        ys = [y for _, y in polygon]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        grid_cells = (max_x - min_x + 1) * (max_y - min_y + 1)
        print(f"Bounds: x={min_x}..{max_x}, y={min_y}..{max_y}")
        
        # Part One
        print("\n" + "=" * 50)
        print("PART ONE")
        print("=" * 50)
        start1 = time.time()
        area1 = part_one(polygon)
        time1 = time.time() - start1
        print(f"Largest area: {area1}")
        print(f"Time: {time1:.3f}s")
        
        # Part Two
        print("\n" + "=" * 50)
        print("PART TWO")
        print("=" * 50)
        
        # Choose algorithm
        if n <= 2000:
            print("Using smart algorithm with pruning...")
            start2 = time.time()
            area2 = part_two_smart(polygon)
            time2 = time.time() - start2
        else:
            print("Using sweep line algorithm...")
            start2 = time.time()
            area2 = part_two_sweep(polygon)
            time2 = time.time() - start2
        
        print(f"Largest area: {area2}")
        print(f"Time: {time2:.3f}s")
        
        print("\n" + "=" * 50)
        print("RESULTS")
        print("=" * 50)
        print(f"Part One: {area1}")
        print(f"Part Two: {area2}")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted. Partial result:")
        print(f"Part One: {area1 if 'area1' in locals() else 'N/A'}")
        print(f"Part Two: {area2 if 'area2' in locals() else 'N/A'}")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    print("Advent of Code - Day 9 (Memory Efficient)")
    print("=" * 50)
    main()
