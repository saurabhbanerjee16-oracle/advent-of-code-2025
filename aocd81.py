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
        self.size = [1] * n
    
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
            self.size[root_y] = self.size[root_y] + self.size[root_x]
            # Update all sizes in the component to maintain consistency
            self.size[root_x] = self.size[root_y]
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            self.size[root_x] = self.size[root_x] + self.size[root_y]
            self.size[root_y] = self.size[root_x]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] = self.size[root_x] + self.size[root_y]
            self.size[root_y] = self.size[root_x]
            self.rank[root_x] += 1
        
        return True  # Successfully merged

def main():
    # Read input from file
    with open('input8.txt', 'r') as f:
        lines = f.readlines()
    
    # Parse points
    points = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Handle comma-separated or space-separated coordinates
        if ',' in line:
            x, y, z = map(int, line.split(','))
        else:
            x, y, z = map(int, line.split())
        points.append((x, y, z))
    
    n = len(points)
    
    # Generate all pairs with distances
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(points[i], points[j])
            pairs.append((dist, i, j))
    
    # Sort pairs by distance
    pairs.sort(key=lambda x: x[0])
    
    # Initialize Union-Find
    uf = UnionFind(n)
    
    # Make 1000 connection attempts (the 1000 shortest distances)
    connections_to_make = 1000
    if len(pairs) < connections_to_make:
        connections_to_make = len(pairs)
    
    for i in range(connections_to_make):
        dist, idx1, idx2 = pairs[i]
        uf.union(idx1, idx2)  # Attempt to connect
    
    # Count sizes of all connected components
    component_sizes = defaultdict(int)
    for i in range(n):
        root = uf.find(i)
        component_sizes[root] += 1
    
    # Get sizes list and sort in descending order
    sizes = sorted(component_sizes.values(), reverse=True)
    
    # Multiply the three largest sizes
    if len(sizes) >= 3:
        result = sizes[0] * sizes[1] * sizes[2]
    else:
        result = 0
    
    print(f"Total junction boxes: {n}")
    print(f"Number of connection attempts made: {connections_to_make}")
    print(f"Number of circuits after connections: {len(sizes)}")
    print(f"Three largest circuit sizes: {sizes[:3]}")
    print(f"Product of three largest: {result}")
    
    return result

if __name__ == "__main__":
    main()
