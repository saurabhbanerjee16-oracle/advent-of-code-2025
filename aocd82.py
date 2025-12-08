import math
from collections import defaultdict

def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two 3D points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

class UnionFind:
    """Union-Find (Disjoint Set Union) data structure."""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n  # Track number of components
    
    def find(self, x):
        """Find root of x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union two elements, return True if they were in different sets."""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same set
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        self.components -= 1  # One less component after merging
        return True  # Successfully merged
    
    def connected(self):
        """Check if all elements are in the same set."""
        return self.components == 1

def main():
    # Read input from file
    import sys
    
    # Get filename from command line argument or use default
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'input8.txt'
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Parse points
    points = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Handle comma-separated coordinates
        if ',' in line:
            x, y, z = map(int, line.split(','))
        else:
            x, y, z = map(int, line.split())
        points.append((x, y, z))
    
    n = len(points)
    
    # Generate all pairs with distances
    print(f"Calculating distances for {n} points...")
    pairs = []
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(points[i], points[j])
            pairs.append((dist, i, j))
    
    print(f"Sorting {len(pairs):,} pairs...")
    # Sort pairs by distance
    pairs.sort(key=lambda x: x[0])
    
    print("Initializing Union-Find...")
    # Initialize Union-Find
    uf = UnionFind(n)
    
    last_connection = None
    
    print("Connecting pairs until all are in one circuit...")
    # Connect pairs until all junction boxes are in one circuit
    for i, (dist, idx1, idx2) in enumerate(pairs):
        if uf.union(idx1, idx2):
            # This was a successful connection (merged two different components)
            last_connection = (idx1, idx2)
            
            # Check if we're done (all connected)
            if uf.connected():
                print(f"All connected after {i+1} connections")
                break
    
    if last_connection:
        idx1, idx2 = last_connection
        x1 = points[idx1][0]
        x2 = points[idx2][0]
        product = x1 * x2
        
        print(f"\nLast connection between:")
        print(f"  Box {idx1}: {points[idx1]} (X={x1})")
        print(f"  Box {idx2}: {points[idx2]} (X={x2})")
        print(f"\nProduct of X coordinates: {x1} * {x2} = {product}")
        return product
    else:
        print("No connections were made!")
        return 0

if __name__ == "__main__":
    main()