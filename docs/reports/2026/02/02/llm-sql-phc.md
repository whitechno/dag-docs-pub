Optimizing LLM Queries: Comments and Suggestions
================================================
February 2, 2026

Main publication:  
[[LLM-SQL](https://arxiv.org/pdf/2403.05821)] "Optimizing LLM Queries in
Relational Data Analytics Workloads", 9 Apr 2025.

Followup publication with AI-driven algorithm improvement:  
[[AI-Sys](https://arxiv.org/pdf/2512.14806)] "Let the Barbarians In: How AI Can
Accelerate Systems Performance Research", Section 4.4, 22 Dec 2025.

[LLM-SQL] presents a "Greedy Group Recursion" (GGR) algorithm for optimizing LLM
queries by finding (a `n x m`) table re-arrangement that maximizes the LLM's KV
cache prefix hit count (PHC). Compared to the brute-force algorithm that
requires `n!*(m!)^n` potential orderings, GGR significantly reduces the search
space by selecting the highest-hit value and then reducing the dimensions of the
table at each recursive step with the maximum depth of recursion `O(min(n,m))`.
GGR achieves close-to-perfect PHC output with fast practical execution time.

Here we propose several adjustments to the GGR algorithm that improve the
output (moving it closer to the optimal solution) and also further improve the
execution time.

Algorithm improvements
----------------------

See code specification of Greedy Group Recursion (GGR) algorithm on page 5 of
the [LLM-SQL] paper.

At each recursive step, the GGR algorithm scans the table (lines 17–23) to find
all distinct values with corresponding hit counts (lines 3–8). It then selects
the highest-hit value `b_v` (with corresponding column `b_c`) and splits the
table into two sub-tables - one with all the rows `R_v` containing `b_v` value
in `b_c` column excluding the field where the value is located in, and another
sub-table with the remaining rows. It then recurses on the two sub-tables (lines
24-26) and calculates the total PHC as the sum of PHC of the sub-tables and
contributions of `b_v` (line 28).

### Recursion early termination when only distinct values are present

If table scan tells that all values in the table are distinct (each appearing in
exactly one row), the algorithm terminates early and returns the `PHC=0` of the
table together with unmodified table:
```text
return 0, T
```
In other words, if the table cannot be optimized for hit count, the recursion
stops and the original table is returned. The situation of a table with all
distinct values can occur at the later stages of the recursion when only
singleton values from the long tail are left. In this situation the recursion
ends in one step.

Like the other two termination conditions, this one outputs the optimal
solution.

Minor typos in equations
------------------------

### Typo 1

On page 3, the equation (2) should have `1<=c<=m` rather than `0<=c<m`, as it
appears that everywhere else in the paper both rows and columns are counted from
`1` (to `n` and `m` respectively).

### Typo 2

On page 5, in the "Algorithm 1 Greedy Group Recursion" code specification, line
6: the contribution of each inferred column `c'` should have its value length to
be squared too `len(v')^2`, where `v'` is the inferred column `c'` value derived
from value `v` of parent column `c` based on the table's Functional Dependency
(FD) rules. Line 6 should read:
```text
tot_len = len(v)^2 + SUM_c'[len(v')^2]
```
There is also no need to average `len(T[r,c'])` because values `v' = T[r,c']`
are the same for all `r` in `R_v`. 
