Hypergraph Matching Review
==========================
March 3, 2026

[[Hypergraph Matching]](https://arxiv.org/abs/2602.22976)
"Efficient Parallel Algorithms for Hypergraph Matching"
By Henrik Reinstädtler, Christian Schulz, Nodari Sitchinava, Fabian Walliser
Submitted on 26 Feb 2026


Technical Summary
-----------------

### Problem

A hypergraph H = (V, E, ω) generalizes a graph by allowing hyperedges to connect
more than two vertices. A *matching* is a set of pairwise vertex-disjoint
hyperedges. The weighted hypergraph matching problem — finding a maximum-weight
matching — is NP-hard (in contrast to ordinary graph matching, which is
polynomial). The best achievable approximation in polynomial time is 1/d, where
d is the maximum hyperedge size (rank).

### Core Algorithm: Local-Max

The paper's central idea is a *local-max* strategy: iteratively identify
hyperedges that are locally maximal (weight exceeds all neighboring hyperedges
sharing at least one vertex) and add them to the matching, removing their
neighbors. Random weight perturbations are added each round to break ties and
prevent stagnation.

The correctness argument maps the algorithm to Luby's parallel MIS algorithm on
the line graph L(H), where each hyperedge becomes a vertex and adjacency encodes
shared vertices. This equivalence gives O(log m) rounds with high probability
(w.h.p.), where m is the number of hyperedges.

**Approximation guarantee:** Any maximal matching produced by the local-max
algorithm has weight at least 1/d of the optimum (tight lower bound).

### Terminology

In the PRAM model, **running time** and **work** are two separate complexity
measures:

**Running time** (also called *parallel time* or *span*) is the number of
sequential steps elapsed from start to finish, assuming you have as many
processors as you need. It measures how fast the algorithm runs in wall-clock
time on an ideal parallel machine. O(log m) running time means the algorithm
finishes in logarithmically many parallel steps — very fast regardless of input
size.

**Work** is the total number of operations performed across all processors
combined — i.e., running time × number of processors active at each step, summed
up. It measures the total computational effort, analogous to the runtime of a
sequential algorithm. O((κ+n) log m) work means that if you ran all those
operations sequentially, they would take that long.

The relationship between the two reveals parallelism's efficiency. For this
algorithm:
- Wall-clock time: O(log m) — logarithmic, very fast
- Total operations: O((κ+n) log m) — essentially linear in the input size (κ+n)
  times a log factor

An algorithm is called **work-optimal** when its total work matches the best
known sequential algorithm. That is the motivation for the third variant in the
paper: it reduces work to O(κ+n) (dropping the log m factor) at the cost of
slower parallel time O((log m + log n) log m).

**w.h.p.** stands for **with high probability**. In algorithm analysis it means
the bound holds with probability at least 1 − 1/n^c for some constant c > 1
(where n is the input size), so the failure probability becomes negligible as n
grows. Here it qualifies the O(log m) round count, which relies on random weight
assignments — the algorithm could theoretically take more rounds on an unlucky
random draw, but that probability shrinks polynomially fast.

### Parallel Algorithms and Complexity

Three PRAM variants are presented:

| Algorithm         | Time                     | Work           | Model               |
|-------------------|--------------------------|----------------|---------------------|
| CRCW (SUM-CRCW)   | O(log m)                 | O((κ+n) log m) | Combining CRCW PRAM |
| CREW              | O((log Δ + log d) log m) | O((κ+n) log m) | CREW PRAM           |
| Work-optimal CREW | O((log m + log n) log m) | O(κ+n)         | CREW PRAM           |

Here n = number of vertices, m = number of hyperedges, κ = sum of all vertex
degrees (= sum of all edge sizes), Δ = maximum vertex degree, d = rank.

The CRCW variant achieves O(1) time per round using atomic increments and
concurrent writes. The CREW variant replaces concurrent operations with
prefix-sum reductions (log-time), running 6 sub-phases per round. The
work-optimal CREW variant additionally compacts the hypergraph between rounds
using parallel prefix sums, reducing total work from O((κ+n) log m)
to O(κ+n).

The algorithm extends naturally to MapReduce and external memory models.

### Data Structure

The hypergraph is stored in a compressed sparse format using four arrays:
- Vid, Vp: vertex-to-incident-edge index
- Eid, Ep: edge-to-contained-vertex index

This bidirectional CSR-like structure supports efficient traversal in both
directions with O(κ) total memory.

### Implementation

Algorithms are implemented in both CUDA (HLM:C) and Kokkos (HLM:K), the latter
providing cross-architecture portability (GPU, multicore CPU via OpenMP). Random
weight noise is sampled uniformly from [0, 100] each round using XORWOW (CUDA)
or XORSHIFT (Kokkos) generators.

### Experimental Results

Hardware: NVIDIA RTX 4090 + 16-core Intel Xeon w5-3435X, 128 GB RAM. Benchmark:
90 large hypergraph instances (SAT competition 2014, SuiteSparse, DAC challenge)
and 42 graph instances (DIMACS 10th challenge).

**Hypergraphs (weighted matching, vs. single-core Greedy baseline):**
- HLM:C (GPU, CUDA): speedup 3.2–76.6×, matching quality 88–99.7% of Greedy
- HLM:K (GPU, Kokkos): speedup up to 32×
- HLM:K (16C, CPU): speedup ~13×
- Stack Streaming baseline [40]: 1.7–3.7× but lower quality (67–76% on some
  categories)

**Graphs (cardinality matching):**
- HLM:C (GPU) vs. LM/MPI (16-core CPU): faster on 3 of 6 categories (up to
  2.75×), slower on 3 (up to 1.61×)
- HLM:K (GPU) vs. SuMaC (GPU): up to 27.16× faster; matching size 87.6–98.2% of
  SuMaC

The Wiki hypergraph (non-uniform weights) required 16 rounds vs. 5–7 for others,
explaining its relatively lower GPU speedup (2.38×). The CUDA and Kokkos
implementations differ primarily in random number generator, which affects both
speed and quality marginally.
