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
queries by finding table re-arrangement that maximizes the LLM's KV cache prefix
hit count (PHC). Compared to the brute-force algorithm that requires `n!*(m!)^n`
potential orderings, GGR significantly reduces the search space by selecting the
highest-hit value and then reducing the dimensions of the table at each
recursive step with the maximum depth of recursion `O(min(n,m))`. GGR achieves
near-perfect PHC output with lightning-fast execution time.

Here we propose several improvements to the GGR algorithm that improve the
output (moving it closer to the optimal solution) and also further improve the
execution time.
