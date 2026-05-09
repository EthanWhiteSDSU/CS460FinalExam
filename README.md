# The Torchbearer

**Student Name:** Ethan White
**Student ID:** 130278197
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  A single-shortest path from S is not enough, as it only gives one piece of the entire path we need.
  Just because this one piece is optimal does not mean the remaining path will also be optimal (this is not greedy).

- **What decision remains after all inter-location costs are known:**
  After all inter-location costs are known, each path from S to T (that also visits each relic chamber) must be checked for the most
  optimal one (the one that minimizes the total torch fuel cost).

- **Why this requires a search over orders (one sentence):**
  In order to avoid having to check every single path, only the paths
  that lower the total torch fuel cost should be explored.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| S | The entrance, all paths must start from here |
| R_i | Any given relic chamber R in set M, we want to know the shortest path from each relic chamber to the next or to T |


### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | Dictionary (Hash Table) |
| What the keys represent | dict[source_node], the key is just the source node |
| What the values represent | dict[end_node], each source node's value is a second dictionary of the minimum distances to each other node. The key is the end node and the value is the minimal distance |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Since dictionaries use hashing, an O(1) lookup is expected |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** |M| + 1
- **Cost per run:** O((V + E)log V), where E is the number of edges and V is the number of vertices.
- **Total complexity:** (|M| + 1) * O((V + E)log V) = O(|M|(V + E)log V)
- **Justification (one line):** In order to fill out an entire shortest-path table, we need to run Dijkstra's with S and each R in M
as the source node.

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
dist[v] must represent the shortest path from vertex x to v since vertex v will never be revisited.

- **For nodes not yet finalized (not in S):**
dist[u] must represent the shortest path so far from vertex x to u where each vertex between
x and u is in S.
In other words, each vertex between x and u have already been finalized, thus dist[u] could
be the true shortest path (unless a shorter path is found with the same conditions).

### Part 3b: Why Each Phase Holds

- **Initialization : why the invariant holds before iteration 1:**
Before iteration 1, S is an empty set, dist[v] for the source node is 0, and dist[v] for all other nodes is inf.
The invariant holds since the distance from the source node to itself must be 0 and no other nodes have been finalized, so the distances must remain undetermined at inf.

- **Maintenance : why finalizing the min-dist node is always correct:**
Since all edge weights must be nonnegative, there will never be a future dist[u] for node u that is smaller than dist[v].
Thus, finalizing each min-dist node is guaranteed to be correct.

- **Termination : what the invariant guarantees when the algorithm ends:**
When the algorithm terminates, S is filled with every node, dist[v] for the source node is 0, and dist[v] for all other nodes is some nonnegative value.
The invariant guarantees that each dist[v] is the minimal distance from the source node to node v.
 

### Part 3c: Why This Matters for the Route Planner

Knowing the true shortest path costs from any given vertex to another helps the route planner guarantee that the resulting route that it determines is also minimal. 

---

## Part 4: Search Design

### Why Greedy Fails

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

### What the Algorithm Must Explore

The algorithm must explore every possible order that the relic chambers can be visited in and determine the order that results in the smallest total torch cost. 

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc | Node | Denotes the current room (node) that the Torchbearer is in |
| Relics already collected | relics_visited_order | List | Denotes the relics that the Torchbearer has currently collected |
| Fuel cost so far | cost_so_far | Int | Denotes the current amount of fuel that the Torchbearer has used |

### Part 5b: Data Structure for Visited Relics

| Property | Your answer |
|---|---|
| Data structure chosen | List |
| Operation: check if relic already collected | Time complexity: O(M) |
| Operation: mark a relic as collected | Time complexity: O(1) |
| Operation: unmark a relic (backtrack) | Time complexity: O(M) |
| Why this structure fits | Marking is done in constant time due to appending, but checking and unmarking have to be done in linear time. Using a dictionary would make them also constant, but since M is small here, a List is easier to write and should work fine |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** k!
- **Why:** There are a total of k! different order permutations that can be searched.

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- **What is tracked:** total torch cost of the overall best path found so far
- **When it is used:** check if the cost of travelling along the current path will exceed the best so far
- **What it allows the algorithm to skip:** path orders that are guaranteed to be less optimal than the overall best path so far

### Part 6b: Lower Bound Estimation

- **What information is available at the current state:** current path cost, relics collected so far, relics to be collected, and cost to travel to the next neighboring (and unvisited) room
- **What the lower bound accounts for:** the current path cost plus the lowest possible remaining total cost of travelling through the rest of the potential paths from the next room to T
- **Why it never overestimates:** Since the cost of moving to the next room is already minimal (thanks to Dijkstra's), it serves as a proper lower bound for the remaining potential paths from that next room to T (since the next room MUST be visited in order to travel along any of those potential paths from it)

### Part 6c: Pruning Correctness

- Since moving to the next room is guaranteed to have the minimal cost, if that cost plus the current path's cost is ever equal to or greater than the best so far cost, all the remaining paths from that next room are not worth checking and should be pruned
- This is also guaranteed by there being no nonnegative costs in the dungeon, thus no future path can ever reduce the current path cost plus the next room cost


---

## References

Lecture Notes