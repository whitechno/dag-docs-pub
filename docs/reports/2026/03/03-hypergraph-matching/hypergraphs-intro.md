Hypergraphs Introduction
========================
March 3, 2026

This brief introduction to hypergraphs is based on the following references:

- [Hypergraphs: an introduction and review](
  https://arxiv.org/abs/2002.05014)
```text
@misc{ouvrard2020hypergraphsintroductionreview,
      title={Hypergraphs: an introduction and review}, 
      author={Xavier Ouvrard},
      year={2020},
      eprint={2002.05014},
      archivePrefix={arXiv},
      primaryClass={cs.DM},
      url={https://arxiv.org/abs/2002.05014}, 
}
```

- [Efficient Parallel Algorithms for Hypergraph Matching](
  https://arxiv.org/abs/2602.22976)
```bibtex
@misc{reinstädtler2026efficientparallelalgorithmshypergraph,
      title={Efficient Parallel Algorithms for Hypergraph Matching}, 
      author={Henrik Reinstädtler and Christian Schulz and Nodari Sitchinava 
              and Fabian Walliser},
      year={2026},
      eprint={2602.22976},
      archivePrefix={arXiv},
      primaryClass={cs.DS},
      url={https://arxiv.org/abs/2602.22976}, 
}
```

- [wiki Matching in hypergraphs](
  https://en.wikipedia.org/wiki/Matching_in_hypergraphs)

- Valdivia, Paola; Buono, Paolo; Plaisant, Catherine; Dufournaud, Nicole;
  Fekete, Jean-Daniel (2020). "Analyzing Dynamic Hypergraphs with Parallel
  Aggregated Ordered Hypergraph Visualization"
  [(PDF)](https://hal.inria.fr/hal-02264960/file/Paohvis.pdf).

  IEEE Transactions on Visualization and Computer Graphics. 26 (1). IEEE: 12.
  doi:10.1109/TVCG.2019.2933196. eISSN 1941-0506. hdl:11586/518500. ISSN
  1077-2626. PMID 31398121. S2CID 199518871.
```text
Paola R Valdivia, Paolo Buono, Catherine Plaisant, Nicole Dufournaud, Jean-Daniel Fekete.
Analyzing Dynamic Hypergraphs with Parallel Aggregated Ordered Hypergraph Visualization.
IEEE Transactions on Visualization and Computer Graphics, 2021, 27 (1), pp.1-13.
10.1109/TVCG.2019.2933196. hal-02264960
https://hal.inria.fr/hal-02264960/file/Paohvis.pdf
```

- [On an Erdős--Lov'asz problem: 3-critical 3-graphs of minimum degree 7](
  https://arxiv.org/abs/2512.24850
  )
```text
@misc{li2025erdhoslovaszproblem3critical3graphs,
      title={On an Erd\H{o}s--Lov'asz problem: 3-critical 3-graphs of minimum degree 7}, 
      author={Ruiliang Li},
      year={2025},
      eprint={2512.24850},
      archivePrefix={arXiv},
      primaryClass={cs.DM},
      url={https://arxiv.org/abs/2512.24850}, 
}
```

Hypergraph Concepts
-------------------

A weighted undirected hypergraph $H=(V,E,\omega)$ consists of a set $V$ of $n$
vertices and a set $E$ of $m$ hyperedges. Each hyperedge $e \subseteq V$ is a
subset of vertices whose weight is defined by the weight
function $\omega: E\to \mathbb{R}_{> 0}$. Each hyperedge may contain _one_ or
more vertices.

The _size_ of a hyperedge is the number of vertices it contains and is denoted
by $\left|e\right|$. The maximum size of a hyperedge, also called the _rank_ of
a hypergraph, is defined by $d := \max_{e \in E}\left|e\right|$. If all
hyperedges have the same size $d$, the hypergraph is called $d$-uniform. Note
that $1 \leq \left|e\right| \leq n$. There could be only one hyperedge of
size $n$, and at most $n$ hyperedges of size $1$.

Two edges are considered disjoint if they do not share any common vertices and
are neighbors if they do share at least one vertex. An edge is considered
locally maximal if it has a greater weight than all of its neighbors.

The set of hyperedges that contain a vertex $v$ is defined by $E[v]$.
Thereby, $deg(v) = |E[v]|$ denotes the number of hyperedges a vertex $v$ is
contained in and is called the _degree_ of $v$. The maximum degree is denoted
by $\Delta := \max_{v \in V}deg(v)$. Note that $0 \leq deg(v) \leq 2^{n-1}$.
(For regular graphs, $0 \leq deg(v) \leq n-1$.)

Graph's _kappa_ $\kappa = \sum_{v \in V} deg(v) = \sum_{e \in E} \left|e\right|$
is defined as the sum over all vertex degrees, which is equal to the sum of all
edge sizes. (For regular graphs, $\left|e\right| = 2$, and we get the well-known
equation $\sum_{v \in V} deg(v) = 2 m$.) Note
that $\kappa \leq \min\{\Delta \times n, d \times m\}$.

### Line Graph

Given a hypergraph $H = (V, E)$, the line graph $L(H) = (V', E')$ is defined
by $V' := E$, and $\{e_1, e_2\} \in E'$
if $e_1 \cap e_2 \neq \emptyset$, i.e., there is an edge in $L(H)$ if the two
corresponding hyperedges share at least one vertex.

### Matching

We assume that vertices with degree $0$ have been removed during the
preprocessing phase. Therefore, $\Delta > 0$ or else the hypergraph is empty.

A subset of hyperedges $M \subseteq E$ is a matching if all hyperedges are
pairwise disjoint. The weight of a matching $M$ is defined
by $w(M):= \sum_{e\in M}w(e)$. A matching $M$ is called maximal if no hyperedge
can be added without violating the matching property. A maximum matching
possesses the largest possible weight of all matchings. If the weight of each
hyperedge is exactly the same, the problem is referred to as _maximum
cardinality~matching_, maximizing $|M|$. Finding a cardinality matching or the
more general weighted hypergraph matching is NP-hard~
\cite{approxresult}. This is in contrast to ordinary graphs, for which the
problem can be solved in polynomial time~\cite{edmonds_1965}.

