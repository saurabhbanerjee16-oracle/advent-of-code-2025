import sys
from collections import defaultdict, deque
from typing import List, Set, Dict

def find_paths_with_constraints_optimized(
    graph: Dict[str, List[str]], 
    start: str, 
    end: str, 
    required_nodes: Set[str]
) -> List[List[str]]:
    """
    Find all paths from start to end that contain all required nodes.
    Uses several optimizations for large graphs.
    """
    # Optimization 1: Precompute reachability from each node to end and required nodes
    reachable_to_end = {}
    reachable_to_required = {}
    
    # Compute reachability using BFS backwards from end
    reverse_graph = defaultdict(list)
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            reverse_graph[neighbor].append(node)
    
    # BFS from end to find all nodes that can reach end
    queue = deque([end])
    visited = {end}
    while queue:
        node = queue.popleft()
        for pred in reverse_graph[node]:
            if pred not in visited:
                visited.add(pred)
                queue.append(pred)
    reachable_to_end = visited.copy()
    
    # Check if start can reach end
    if start not in reachable_to_end:
        return []
    
    # Optimization 2: Early pruning - remove unreachable nodes from graph
    pruned_graph = {}
    for node in reachable_to_end:
        pruned_graph[node] = [n for n in graph.get(node, []) if n in reachable_to_end]
    
    # Main DFS with optimizations
    def dfs(
        current: str, 
        path: List[str], 
        visited_set: Set[str],
        found_required: Set[str],
        remaining_required_count: int
    ) -> None:
        # Optimization 3: Early termination if we can't reach all required nodes
        # Check if current node can reach all remaining required nodes
        if remaining_required_count > 0:
            # Simple heuristic: check if any remaining required node is in neighbors
            # For more accuracy, we could precompute reachability between all nodes
            pass
        
        if current == end:
            if len(found_required) == len(required_nodes):
                paths.append(path.copy())
            return
        
        # Optimization 4: Sort neighbors for better cache locality
        neighbors = pruned_graph.get(current, [])
        for neighbor in neighbors:
            if neighbor not in visited_set:
                visited_set.add(neighbor)
                path.append(neighbor)
                
                # Track found required nodes
                new_found_count = len(found_required)
                if neighbor in required_nodes:
                    found_required.add(neighbor)
                    new_found_count = len(found_required)
                
                dfs(
                    neighbor, 
                    path, 
                    visited_set, 
                    found_required,
                    len(required_nodes) - new_found_count
                )
                
                # Backtrack
                path.pop()
                visited_set.remove(neighbor)
                if neighbor in required_nodes:
                    found_required.discard(neighbor)
    
    paths = []
    visited_set = {start}
    initial_found = set()
    if start in required_nodes:
        initial_found.add(start)
    
    # Start DFS
    dfs(
        start, 
        [start], 
        visited_set, 
        initial_found,
        len(required_nodes) - len(initial_found)
    )
    
    return paths

def find_paths_with_constraints_count_only(
    graph: Dict[str, List[str]], 
    start: str, 
    end: str, 
    required_nodes: Set[str]
) -> int:
    """
    Count paths without storing them all (more memory efficient).
    """
    # Prune unreachable nodes first
    reverse_graph = defaultdict(list)
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            reverse_graph[neighbor].append(node)
    
    # Find nodes that can reach end
    queue = deque([end])
    reachable_to_end = {end}
    while queue:
        node = queue.popleft()
        for pred in reverse_graph[node]:
            if pred not in reachable_to_end:
                reachable_to_end.add(pred)
                queue.append(pred)
    
    if start not in reachable_to_end:
        return 0
    
    # Prune graph
    pruned_graph = {}
    for node in reachable_to_end:
        pruned_graph[node] = [n for n in graph.get(node, []) if n in reachable_to_end]
    
    # Use memoization for DP approach if the graph is DAG
    # First check if graph is a DAG (likely for this problem)
    def is_dag():
        in_degree = defaultdict(int)
        for node in pruned_graph:
            for neighbor in pruned_graph[node]:
                in_degree[neighbor] += 1
        
        # Kahn's algorithm
        queue = deque([node for node in pruned_graph if in_degree[node] == 0])
        count = 0
        
        while queue:
            node = queue.popleft()
            count += 1
            for neighbor in pruned_graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return count == len(pruned_graph)
    
    if is_dag():
        # Topological sort for DP
        in_degree = defaultdict(int)
        for node in pruned_graph:
            for neighbor in pruned_graph[node]:
                in_degree[neighbor] += 1
        
        # Initialize queue with nodes having 0 in-degree
        queue = deque([node for node in pruned_graph if in_degree[node] == 0])
        topo_order = []
        
        while queue:
            node = queue.popleft()
            topo_order.append(node)
            for neighbor in pruned_graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # DP[mask][node] = number of ways to reach node with visited required nodes mask
        # For 2 required nodes, mask: 00, 01, 10, 11
        mask_len = len(required_nodes)
        required_list = list(required_nodes)
        node_to_index = {node: i for i, node in enumerate(pruned_graph)}
        required_mask = {}
        for i, node in enumerate(required_list):
            required_mask[node] = 1 << i
        
        # Initialize DP
        dp = [defaultdict(int) for _ in range(1 << mask_len)]
        start_mask = 0
        if start in required_mask:
            start_mask = required_mask[start]
        dp[start_mask][start] = 1
        
        # Process in topological order
        for node in topo_order:
            for mask in range(1 << mask_len):
                if dp[mask][node] > 0:
                    for neighbor in pruned_graph[node]:
                        new_mask = mask
                        if neighbor in required_mask:
                            new_mask = mask | required_mask[neighbor]
                        dp[new_mask][neighbor] += dp[mask][node]
        
        # Count paths to end with all required nodes
        full_mask = (1 << mask_len) - 1
        return dp[full_mask].get(end, 0)
    else:
        # Fall back to DFS with counting only
        count = 0
        
        def dfs_count(current, visited_set, found_required):
            nonlocal count
            
            if current == end:
                if len(found_required) == len(required_nodes):
                    count += 1
                return
            
            for neighbor in pruned_graph.get(current, []):
                if neighbor not in visited_set:
                    visited_set.add(neighbor)
                    
                    new_found = found_required.copy()
                    if neighbor in required_nodes:
                        new_found.add(neighbor)
                    
                    dfs_count(neighbor, visited_set, new_found)
                    visited_set.remove(neighbor)
        
        initial_found = set()
        if start in required_nodes:
            initial_found.add(start)
        
        visited_set = {start}
        dfs_count(start, visited_set, initial_found)
        return count

def parse_input(file_path: str) -> Dict[str, List[str]]:
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
        print("Usage: python device_paths_optimized.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Parse the graph from input
    graph = parse_input(input_file)
    
    # Required nodes for Part 2
    required_nodes = {"dac", "fft"}
    
    # Use the counting-only version for efficiency
    print("Analyzing graph...")
    
    # First check if we have all required nodes
    missing_nodes = required_nodes - set(graph.keys())
    if missing_nodes:
        # Check if required nodes might be destinations (not sources)
        all_nodes = set(graph.keys())
        for neighbor_list in graph.values():
            all_nodes.update(neighbor_list)
        
        missing_nodes = required_nodes - all_nodes
        if missing_nodes:
            print(f"Warning: Required nodes {missing_nodes} not found in graph!")
    
    # Count paths using optimized algorithm
    path_count = find_paths_with_constraints_count_only(graph, "svr", "out", required_nodes)
    
    # If we want to see actual paths for smaller graphs (uncomment for debugging):
    # if path_count <= 100:  # Only show paths if count is small
    #     actual_paths = find_paths_with_constraints_optimized(graph, "svr", "out", required_nodes)
    #     print(f"\nFound {len(actual_paths)} paths from 'svr' to 'out' that visit both 'dac' and 'fft':")
    #     for i, path in enumerate(actual_paths, 1):
    #         print(f"Path {i}: {' -> '.join(path)}")
    
    print(f"\nTotal paths from 'svr' to 'out' that visit both 'dac' and 'fft': {path_count}")

if __name__ == "__main__":
    main()
