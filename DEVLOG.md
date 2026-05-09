# Development Log – The Torchbearer

**Student Name:** Ethan White
**Student ID:** 130278197

---

## Entry 1 – [5/6/26]: Initial Plan

I plan to first implement Djikstra's algorithm to determine the individual
shortest paths from each important node (minus T) to each other node in the dungeon. 
This will allow me to form a shortest-path table between nodes. 
Using this table, I can then prune the unoptimal paths using a branch and bound search pattern.
Once this is done, I should be left with the most optimal path.
I expect the branch and bound portion to be the most difficult.
I plan to test using the given example with a few self-made examples
to test edge cases and other situations.

---

## Entry 2 – [5/6/26]: [Parts 1 & 2 Completed]

I initially pushed edges into the minheap in the order (node, cost) at first. 
I found that the incorrect edges were being popped.
I found out that it was ordering the minheap by the node letter, not the cost.
By reversing the order, I was able to properly write my implementation for Part 2.

---

## Entry 3 – [5/7/26]: [Parts 3 & 4 Completed, improved Dijkstra's]

I realized that I forgot to include a finalized/unfinalized check for my implementation of Dijkstra's
I went back to my Part 2 code and added a final list
Every time a node is popped from the minheap, it is added to the final list
Then, each time its neighbors are checked to be pushed into the minheap, the code filters out nodes already in final

---

## Entry 4 – [5/8/26]: [Parts 5 & 6 Completed]

In order to track the total cost of the best path so far, I initially went with the following helper function:

def cost_of_best(best, dist_table, exit_node):

    if(len(best) == 0):
        return float('inf')

    cost = 0
    first_node = 'S'

    for node in best:
        cost += dist_table[first_node][node]
        first_node = node
    cost += dist_table[first_node][exit_node]

    return cost

However, I realized that this approach made my code too messy and would be repeated a lot.
I needed a way to store the total cost of the best path so far without changing the function
parameters.
After experimenting with different options, I eventually decided to reserve the first index of the best list for the cost alone, then I could just use the rest of the list as normal.

---


## Entry 5 – [5/8/26]: Post-Implementation Reflection

If given more time, I would try to find a better way to manage the relics_visited and relics_remaining lists. 
Although my implementation for them works, it might be a better idea
to try using dictionaries (hash tables) instead in order to make every operation constant.
This would make my implementation more optimized for larger graph inputs.

---

## Final Entry – [5/8/26]: Time Estimate

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 0.5 hours |
| Part 2: Precomputation Design | 1 hour |
| Part 3: Algorithm Correctness | 0.5 hours |
| Part 4: Search Design | 1.5 hours |
| Part 5: State and Search Space | 1.5 hours |
| Part 6: Pruning | 1.5 hours |
| Part 7: Implementation | 0.2 hours |
| README and DEVLOG writing | 1 hour |
| **Total** | 7.7 hours |