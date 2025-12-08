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
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
            self.rank[root_x] += 1
        
        return True

def test_example():
    # Example data
    example_data = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
    
    # Parse points
    points = []
    for line in example_data.strip().split('\n'):
        x, y, z = map(int, line.split(','))
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
    
    # Print first 10 connections to debug
    print("First 10 connections:")
    for i in range(10):
        dist, idx1, idx2 = pairs[i]
        p1 = points[idx1]
        p2 = points[idx2]
        print(f"{i+1}. Distance {dist:.2f}: {p1} - {p2}")
        uf.union(idx1, idx2)
    
    # Count sizes of all connected components
    component_sizes = defaultdict(int)
    for i in range(n):
        root = uf.find(i)
        component_sizes[root] += 1
    
    # Get sizes list and sort in descending order
    sizes = sorted(component_sizes.values(), reverse=True)
    
    print(f"\nComponent sizes after 10 connections: {sizes}")
    print(f"Number of components: {len(sizes)}")
    
    # Multiply the three largest sizes
    if len(sizes) >= 3:
        result = sizes[0] * sizes[1] * sizes[2]
    else:
        result = 0
    
    print(f"Product of three largest: {result}")
    return result

if __name__ == "__main__":
    test_example()