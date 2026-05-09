"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Ethan White
Student ID: 130278197

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():

    explanation = """
- **Why a single shortest-path run from S is not enough:**
  A single-shortest path from S is not enough, as it only gives one piece of the entire path we need.
  Just because this one piece is optimal does not mean the remaining path will also be optimal (this is not greedy).

- **What decision remains after all inter-location costs are known:**
  After all inter-location costs are known, each path from S to T (that also visits each relic chamber) must be checked for the most
  optimal one (the one that minimizes the total torch fuel cost).

- **Why this requires a search over orders (one sentence):**
  In order to avoid having to check every single path, only the paths
  that lower the total torch fuel cost should be explored.
"""
    
    return explanation


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):

    sources = relics + [spawn] # |M| + 1

    return sources


def run_dijkstra(graph, source):

    distances = {} # set up table
    final = [] # list of finalized nodes

    for key in graph.keys():
        distances[key] = float('inf') # every node has INF distance
    distances[source] = 0 # change source node to 0 distance

    minheap = [(0, source)] # must push nodes into minheap by cost first

    while(len(minheap) > 0):
        
        min_node = heapq.heappop(minheap) # get current node path from minheap

        if(min_node[0] > distances[min_node[1]]): # skip if the current path to node is worse
            continue

        distances[min_node[1]] = min_node[0] # save the current path for node
        final.append(min_node[1]) # finalize node path when popped from minheap

        for (neighbor, cost) in graph[min_node[1]]: # for each neighbor of min_node in graph
            if neighbor not in final: # only add unfinalized node paths to minheap
                heapq.heappush(minheap, (min_node[0] + cost, neighbor)) # push neighbor's path

    return distances


def precompute_distances(graph, spawn, relics, exit_node):

    source_nodes = {}

    for source in select_sources(spawn, relics, exit_node):
        source_nodes[source] = run_dijkstra(graph, source) # run dijkstra's |M| + 1 times

    return source_nodes


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():

    check = """
- **For nodes already finalized (in S):**
dist[v] must represent the shortest path from vertex x to v since vertex v will never be revisited.

- **For nodes not yet finalized (not in S):**
dist[u] must represent the shortest path so far from vertex x to u where each vertex between
x and u is in S.
In other words, each vertex between x and u have already been finalized, thus dist[u] could
be the true shortest path (unless a shorter path is found with the same conditions).

- **Initialization : why the invariant holds before iteration 1:**
Before iteration 1, S is an empty set, dist[v] for the source node is 0, and dist[v] for all other nodes is inf.
The invariant holds since the distance from the source node to itself must be 0 and no other nodes have been finalized, so the distances must remain undetermined at inf.

- **Maintenance : why finalizing the min-dist node is always correct:**
Since all edge weights must be nonnegative, there will never be a future dist[u] for node u that is smaller than dist[v].
Thus, finalizing each min-dist node is guaranteed to be correct.

- **Termination : what the invariant guarantees when the algorithm ends:**
When the algorithm terminates, S is filled with every node, dist[v] for the source node is 0, and dist[v] for all other nodes is some nonnegative value.
The invariant guarantees that each dist[v] is the minimal distance from the source node to node v.

Knowing the true shortest path costs from any given vertex to another helps the route planner guarantee that the resulting route that it determines is also minimal. 
"""
    return check


# =============================================================================
# PART 4
# =============================================================================

def explain_search():

    explain = """
- **The failure mode:** Assume that greedy always moves to the next unvisited node with the smallest torch cost. 
- **Counter-example setup:** 
Assume the following dungeon layout:
      →---1---A---1---↓
S ---|      3↓ ↑1     T
      →---2---B---1---↑
- **What greedy picks:** 
Greedy would choose to go to node A first (A is unvisited and 1 < 2).
Then it would have to go to B, which costs 3. 
Then it would finish at T which costs 1. 
The total cost would be 5.
- **What optimal picks:** 
Optimal would chose to go to B first, which costs 2. 
Then it would have to go up to A, which costs 1. 
Then it would finish at T which costs 1. 
The total cost would be 4.
- **Why greedy loses:** 
Greedy fails to consider the possibility that choosing the current lightest weight could force the route to take a much heavier cost later on. 
In other words, always choosing the local minimum does not guarantee that the global result will also be minimum.
Therefore, the greedy strategy fails for the route construction phase of the engine.

The algorithm must explore every possible order that the relic chambers can be visited in and determine the order that results in the smallest total torch cost. 
"""
    return explain


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):

    best = [] # create list for best path
    best.append(float('inf')) # initialize total path cost as inf

    """
    NOTE: For reasons explained in Entry 4 of DEVLOG.md, the first index 
    of best is reserved to hold the total path cost for the best path so far.
    Everything after the first element is the actual best path so far.
    """

    _explore(dist_table, spawn, relics, [], 0, exit_node, best)

    # if the total path cost was never updated, that means no valid path exists
    if(best[0] == float('inf')):
        return (float('inf'), [])
    else:
        return (best[0], best[1:])
    



def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    
    if(len(relics_remaining) == 0): # base case: all relics have been obtained

        # calculate the total path cost by adding the cost from the last relic chamber to T
        total_cost = cost_so_far + dist_table[current_loc][exit_node] 
        
        # if total path cost is better than the best so far, make it the new best so far
        if(total_cost < best[0]):
            best[0] = total_cost
            best[1:] = relics_visited_order

        return
    
    # for each unvisited neighbor of the current room
    for neighbor in dist_table[current_loc]:

        if neighbor in relics_remaining:

            # calculate the lower bound estimate of each potential future path
            lower_bound = cost_so_far + dist_table[current_loc][neighbor]

            # if lower bound estimate is less than the best so far, visit the neighbor
            """
            NOTE: This pruning condition is safe because every potential path cost
            from the neighbor to T is guaranteed to be at least the cost from the
            current room to the neighbor. Since the Dijkstra's runs minimized each 
            of the costs and since all of the costs are nonnegative, no future path
            can reduce the total path cost from the neighbor, and thus the optimal 
            solution can never be pruned.
            """
            if(lower_bound < best[0]):

                # make and edit copies of both lists for backtracking
                visited_copy = relics_visited_order.copy() 
                remaining_copy = relics_remaining.copy()

                visited_copy.append(neighbor)
                remaining_copy.remove(neighbor)
                
                _explore(dist_table, neighbor, 
                         remaining_copy, 
                         visited_copy, 
                         lower_bound, exit_node, best)

# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):

    dist_table = precompute_distances(graph, spawn, relics, exit_node)

    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()