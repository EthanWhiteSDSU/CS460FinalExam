# Development Log – The Torchbearer

**Student Name:** Ethan White
**Student ID:** 130278197

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

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

## Entry 4 – [???]: [Short description]

_Your entry here._

---


## Entry 5 – [???]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._

---

## Final Entry – [???]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | |
| Part 2: Precomputation Design | |
| Part 3: Algorithm Correctness | |
| Part 4: Search Design | |
| Part 5: State and Search Space | |
| Part 6: Pruning | |
| Part 7: Implementation | |
| README and DEVLOG writing | |
| **Total** | |
