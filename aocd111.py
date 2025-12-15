import sys
from collections import defaultdict, deque

def find_all_paths(graph, start, end):
    """Find all paths from start to end using DFS."""
    def dfs(current, path, visited):
        if current == end:
            paths.append(path.copy())
            return
        
        # Visit each neighbor that hasn't been visited yet
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, path, visited)
                path.pop()
                visited.remove(neighbor)
    
    paths = []
    visited = {start}
    dfs(start, [start], visited)
    return paths

def parse_input(file_path):
    """Parse the input file into a graph."""
    graph = defaultdict(list)
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            parts = line.split(':')
            if len(parts) < 2:
                continue
                
            device = parts[0].strip()
            outputs = [out.strip() for out in parts[1].split()]
            
            for output in outputs:
                graph[device].append(output)
    
    return graph

def main():
    if len(sys.argv) != 2:
        print("Usage: python device_paths.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Parse the graph from input
    graph = parse_input(input_file)
    
    # Find all paths from "you" to "out"
    all_paths = find_all_paths(graph, "you", "out")
    
    # Print all paths
    print(f"Found {len(all_paths)} paths from 'you' to 'out':\n")
    for i, path in enumerate(all_paths, 1):
        print(f"Path {i}: {' -> '.join(path)}")
    
    print(f"\nTotal paths: {len(all_paths)}")

if __name__ == "__main__":
    main()
