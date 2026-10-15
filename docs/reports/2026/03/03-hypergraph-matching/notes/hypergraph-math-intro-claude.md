# Hypergraphs: A Technical Mathematical Introduction

## 1. Basic Definitions

**Definition 1.1 (Hypergraph).** A *hypergraph* is a pair $H = (V, E)$
where:
- $V$ is a finite non-empty set of $n$ *vertices*
- $E = \{e_1, e_2, \ldots, e_m\} \subseteq 2^V \setminus \{\emptyset\}$
  is a family of *hyperedges*

There are $2^n - 1$ possible non-empty subsets of $V$, and it is the maximum
possible number of hyperedges that can be in a hypergraph with $n$ vertices.
$0 \leq m \leq 2^n - 1$.

The size of a hyperedge $e$ is denoted by $|e|$.
$1 \leq \left|e\right| \leq n$ for any $e \in E$. Note that hypergraphs allow
hyperedges of size $1$.

When every $|e_i| = 2$, $H$ reduces to an ordinary graph. Hyperedges of size $k$
are called *$k$-edges*.

The maximum size of a hyperedge, also called the _rank_ of a hypergraph, is
defined by $rank := \max_{e \in E}\left|e\right|$.

**Definition 1.2 ($k$-uniform Hypergraph).** $H$ is *$k$-uniform* if $|e_i| = k$
for all $i$. A 2-uniform hypergraph is precisely a simple graph.

The maximum possible number of hyperedges that can be in a $k$-uniform
hypergraph with $n$ vertices is $\binom{n}{k}$. (Note
that $\binom{n}{k} = \frac{n!}{k!\,(n-k)!}$.)

A $k$-uniform hypergraph with $n$ vertices is _complete_ when it has maximum
possible hyperedges ($m = \binom{n}{k}$) and denoted by $K_n^{(k)}$. Example:
Tetrahedron $K_4^{(3)}$ is a complete 3-uniform hypergraph on 4 vertices - it
has a vertex set $\{1,2,3,4\}$ and edges $\{123, 124, 134, 234\}$.

**Definition 1.3 (Incidence Matrix).** The *incidence
matrix* $M \in \{0,1\}^{|V| \times |E|}$ is defined by $M_{v,e} = 1$
iff $v \in e$.

---

## 2. Degree and Regularity

**Definition 2.1.** $E[v]$ is the set of all hyperedges incident
to $v$: $E[v] = \{e \in E : v \in e\}$. The *degree* of a vertex $v$
is $d(v) = |E[v]|$. The *degree sequence* of $H$ is the
multiset $\{d(v)\}_{v \in V}$. The maximum degree is denoted
by $\Delta := \max_{v \in V}d(v)$, and the minimum degree
is $\delta := \min_{v \in V}d(v)$.

Since $E \subseteq 2^V \setminus \{\emptyset\}$, there are $2^n - 1$
possible non-empty subsets of $V$, and a vertex $v$ belongs to exactly $2^{n-1}$
of them. So the maximum possible degree is $2^{n-1}$ achieved when $E$ contains
every non-empty subset of $V$ that includes $v$.
$0 \leq d(v) \leq 2^{n-1}$ for all $v \in V$.

For **$k$-uniform hypergraph**, every edge has size exactly $k$, and $v$ can
appear in at most $\binom{n-1}{k-1}$ edges (choose the remaining $k-1$ vertices
from the other $n-1$ vertices). So $d(v) \leq \binom{n-1}{k-1}$. This recovers
the graph case: for $k=2$, $\binom{n-1}{1} = n-1$. ✓

**Proposition 2.2 (Handshaking Lemma for Hypergraphs).**
$$\sum_{v \in V} d(v) = \sum_{e \in E} |e|$$

*Proof.* Count the incidence pairs $(v, e)$ with $v \in e$ in two
ways. $\square$

**Definition 2.3.** $H$ is *$r$-regular* if $d(v) = r$ for all $v \in V$. For
a $k$-uniform $r$-regular hypergraph: $r|V| = k|E|$.

A complete $k$-uniform hypergrap $K_n^{(k)}$ is $\binom{n-1}{k-1}$-regular.

---

## 3. Walks, Connectivity, and Paths

**Definition 3.1.** A *walk* of length $\ell$ in $H$ is an alternating
sequence $v_0, e_1, v_1, e_2, \ldots, e_\ell, v_\ell$
where $\{v_{i-1}, v_i\} \subseteq e_i$. A *path* is a walk with no repeated
vertices or edges. A *cycle* is a closed path of length $\geq 2$.

**Definition 3.2.** $H$ is *connected* if for every pair $u, v \in V$ there
exists a walk from $u$ to $v$. The *connected components* partition $V$ in the
standard sense.

**Definition 3.3 (Girth).** The *girth* $g(H)$ is the length of the shortest
cycle in $H$. A hypergraph with girth $> 2$ (no two hyperedges share more than
one vertex) is called *linear*.

---

## 4. Duality

**Definition 4.1 (Dual Hypergraph).** The *dual* of $H = (V, E)$
is $H^* = (E, \mathcal{V}^*)$
where $\mathcal{V}^* = \{V_v : v \in V\}$
and $V_v = \{e \in E : v \in e\}$.

The incidence matrix of $H^*$ is $M^T$. Duality is an
involution: $(H^*)^* \cong H$.

**Proposition 4.2.** $H$ is $k$-uniform and $r$-regular iff $H^*$ is $r$-uniform
and $k$-regular.

---

## 5. Colorings and Chromatic Theory

**Definition 5.1 (Proper Coloring).** A *proper vertex $q$-coloring* is a
map $c: V \to [q]$ such that no hyperedge is monochromatic: for
all $e \in E$, $c$ is non-constant on $e$.

The *chromatic number* $\chi(H)$ is the smallest $q$ for which a proper coloring
exists.

**Definition 5.2 (Strong Coloring).** A *strong coloring* requires that every
hyperedge is *rainbow*: $|e|$ distinct colors on $e$. The *strong chromatic
number* $\chi_s(H) \geq \chi(H)$.

**Definition 5.3 (2-Colorability / Property B).** $H$ has *Property B* (due to
Bernstein) if $\chi(H) \leq 2$, i.e., $V$ can be 2-colored so no hyperedge is
monochromatic.

**Theorem 5.4 (Erdős, 1963).** If $H$ is $k$-uniform with $|E| < 2^{k-1}$,
then $H$ has Property B.

*Proof sketch.* Color each vertex independently and uniformly at random
in $\{0,1\}$. For each $k$-edge $e$, $\Pr[e \text{ monochromatic}] = 2^{1-k}$.
By union bound,
$\Pr[\exists \text{ monochromatic edge}] < |E| \cdot 2^{1-k} < 1$.
$\square$

**Theorem 5.5 (Erdős–Hajnal).** For every $k \geq 3$, there exist $k$-uniform
hypergraphs without Property B. The extremal number satisfies
$m(k) = \Theta(2^k \sqrt{k})$.

---

## 6. Transversals and Matchings

**Definition 6.1.** A *transversal* (or *hitting set*) of $H$ is a
set $T \subseteq V$ with $T \cap e \neq \emptyset$ for all $e \in E$. The
*transversal number* $\tau(H)$ is the minimum size of a transversal.

**Definition 6.2.** A *matching* is a set $\mathcal{M} \subseteq E$ of pairwise
disjoint edges. The *matching number* $\nu(H)$ is the maximum size of a
matching.

**Proposition 6.3 (Weak Duality).**
$$\nu(H) \leq \tau(H)$$

*Proof.* Any transversal must hit all edges of any matching, requiring at least
one vertex per edge. $\square$

**Edge and vertex removal.**

If $e \in E$, we express removing $e$ from $H$ as:
$$
H-e := \bigl( V, E \setminus \{e\} \bigr).
$$

If $v\in V$, then $H-v$ denotes the induced subhypergraph obtained by
deleting $v$ and all $v$-incident edges:
$$
H-v := \bigl( V \setminus \{v\}, E \setminus E[v] \bigr).
$$

**Definition 6.4.** $H$ is (edge) *$\tau$-critical* if removing any edge
decreases $\tau$:

$$\tau(H-e) < \tau(H), \quad \forall e \in E$$

There is an alternative vertex-critical definition:
$$\tau(H-v) < \tau(H), \quad \forall v \in V$$

**Theorem 6.5 (König's Theorem — Bipartite case).** For bipartite graphs
(2-uniform): $\nu = \tau$. This equality *fails* in general for hypergraphs.

---

## 7. Fractional Relaxations and Linear Programming

The LP relaxation is central to hypergraph theory. Define:

$$\tau^*(H) = \min \left\{ \sum_{v} x_v : x_v \geq 0,\ \sum_{v \in e} x_v \geq 1 \ \forall e \right\}$$

$$\nu^*(H) = \max \left\{ \sum_{e} y_e : y_e \geq 0,\ \sum_{e \ni v} y_e \leq 1 \ \forall v \right\}$$

**Theorem 7.1 (LP Duality).** $\nu^*(H) = \tau^*(H)$ (strong duality of the
primal/dual LP pair).

**Proposition 7.2.** $\nu(H) \leq \nu^*(H) = \tau^*(H) \leq \tau(H)$, and all
inequalities can be strict.

---

## 8. Spectral Theory of Hypergraphs

**Definition 8.1 (Adjacency Tensor).** For a $k$-uniform hypergraph, define the
*adjacency tensor* $\mathcal{A} \in \mathbb{R}^{n^k}$ by:

$$
\mathcal{A}_{i_1 i_2 \cdots i_k} = \begin{cases}  
\frac{1}{(k-1)!} & \text{if } \{i_1,\ldots,i_k\} \in E \\ 0 & \text{otherwise}  
\end{cases}
$$

**Definition 8.2 ($\mathcal{A}$-eigenvalues).** A
scalar $\lambda \in \mathbb{C}$ and vector $\mathbf{x} \neq \mathbf{0}$ satisfy
the *eigenvalue equation* if:

$$(\mathcal{A}\mathbf{x}^{k-1})_i = \lambda x_i^{k-1}, \quad \forall i$$

where $(\mathcal{A}\mathbf{x}^{k-1})_i = \sum_{i_2,\ldots,i_k} \mathcal{A}_{i\, i_2 \cdots i_k} x_{i_2} \cdots x_{i_k}$.

**Definition 8.3 (Normalized Laplacian).** For a $k$-uniform hypergraph, the
*Laplacian tensor* is $\mathcal{L} = \mathcal{D} - \mathcal{A}$
where $\mathcal{D}$ is the diagonal degree tensor.

**Theorem 8.4 (Perron–Frobenius for Tensors, Qi 2005 / Lim 2005).**
If $\mathcal{A}$ is a nonnegative irreducible tensor, then its spectral
radius $\rho(\mathcal{A})$ is an eigenvalue with a unique positive eigenvector (
up to scaling).

**Theorem 8.5 (Spectral Gap and Expansion).** For a $k$-uniform $d$-regular
hypergraph, define the *spectral gap* $\lambda = \rho(\mathcal{A}) - \lambda_2$.
Then the *edge expansion* $h(H)$ (Cheeger constant) satisfies:

$$\frac{\lambda}{2} \leq h(H) \leq \sqrt{2d\lambda}$$

---

## 9. Ramsey Theory for Hypergraphs

**Definition 9.1.** The *Ramsey number* $R^{(k)}(s, t)$ is the minimum $n$ such
that every red/blue coloring of $\binom{[n]}{k}$ contains a red $K_s^{(k)}$ or
blue $K_t^{(k)}$, where $K_n^{(k)}$ is the complete $k$-uniform hypergraph.

**Theorem 9.2 (Erdős–Rado, 1952).** Ramsey numbers for $k$-uniform hypergraphs
exist for all $k, s, t$. The tower-type upper bound satisfies:

$$R^{(k)}(s,t) \leq \text{twr}_{k-1}(\text{poly}(s,t))$$

where $\text{twr}_j$ denotes a tower of exponentials of height $j$.

**Theorem 9.3 (Stepping-Up Lemma, Erdős–Hajnal).** Lower bounds for $k$-uniform
Ramsey can be bootstrapped from $(k-1)$-uniform ones: if $R^{(k-1)}(s,t) > 2^n$,
then $R^{(k)}(s+1, t+1) > 2^n$.

---

## 10. Turán-Type Problems

**Definition 10.1.** The *Turán number* $\text{ex}(n, F)$ for a $k$-uniform
hypergraph $F$ is the maximum number of edges in an $n$-vertex $k$-uniform
hypergraph containing no copy of $F$.

**Theorem 10.2 (Turán density).** The
limit $\pi(F) = \lim_{n\to\infty} \binom{n}{k}^{-1} \text{ex}(n, F)$ exists for
all $k$-uniform $F$ (by supersaturation/smoothing).

**Problem 10.3 (Turán's Tetrahedron Problem, open).** Determine $\pi(K_4^{(3)})$
for the complete 3-uniform hypergraph on 4 vertices. Turán
conjectured $\pi(K_4^{(3)}) = 2/9$; this remains one of the most famous open
problems in combinatorics.

---

## 11. Sunflowers

**Definition 11.1.** A *sunflower* (or $\Delta$-system) with $p$ petals is a
family $\{E_1,\ldots,E_p\} \subseteq E$ such that $E_i \cap E_j = Y$
for all $i \neq j$ (the *core* $Y$).

**Theorem 11.2 (Sunflower Lemma, Erdős–Ko–Rado 1960).** If $\mathcal{F}$ is a
family of sets each of size $k$ with $|\mathcal{F}| > k!(p-1)^k$,
then $\mathcal{F}$ contains a sunflower with $p$ petals.

**Conjecture 11.3 (Erdős–Ko–Rado).** The bound $k!(p-1)^k$ can be improved
to $(p-1)^k \cdot k^{O(1)}$, or even $O(p)^k$. The case $p=3$ and
achieving $c^k$ for $c < k$ is the basis of recent breakthrough results
(Alweiss–Lovett–Wu–Zhang, 2020), which proved:

$$
|\mathcal{F}| > (O(p \log k))^k \implies  
\mathcal{F} \text{ contains a } p\text{-sunflower}
$$

<https://en.wikipedia.org/wiki/Sunflower_(mathematics)>

[The Sunflower Lemma - Extremal Combinatorics](
https://extremalcombinatorics.com/notes/sec_sunflower.html)

[Institute for Advanced Study, PCMI lecture series: from sunflowers to thresholds](
https://www.ias.edu/sites/default/files/Sunflowers%20Lecture%20Notes_1.pdf
)

These are lecture notes for a mini-course given at PCMI in July 2025. The main
topics are the sunflower conjecture, threshold phenomena, their connection using
the notion of spreadness, and an application of these notions in **complexity
theory**.

History of the Erd˝os-Rado sunflower conjecture (below c denotes some global
constant):
- Sunflower lemma: SF(n, r) ≤ n! · (r − 1)^n ≈ (rn)^n
- Kostochka [Kos96] improved bound for constant r to n^(1−o(1))n.
- Fukuyama [Fuk18] improved bound for r = 3 to ≈ n^{(3/4)n}.
- Alweiss, Lovett, Wu, Zhang [ALWZ21] improved to
  `(cr log(rn))^n · (log log n)^O(n)`.
- Frankston, Kahn, Narayanan, Park [FKNP21] improved bound to (cr log(rn))^n;
  used technique to prove the “fractional Kahn-Kalai conjecture”.
- Proof re-cast in language of information theory by Rao [Rao20] and
  Tao [Tao20].
- Bell, Chueluecha, Warnke [BCW21] improved the bound to (cr log n)^n.
- Park and Pham [PP24] refined the technique and proved the full Kahn-Kalai
  conjecture.

[The sunflower lemma via Shannon entropy - Terence Tao](
https://terrytao.wordpress.com/2020/07/20/the-sunflower-lemma-via-shannon-entropy/
)

[Special cases of Shannon entropy - Terence Tao](
https://terrytao.wordpress.com/2017/03/01/special-cases-of-shannon-entropy/
)


[Improved bounds for the sunflower lemma](https://arxiv.org/abs/1908.08483)
Ryan Alweiss, Shachar Lovett, Kewen Wu, Jiapeng Zhang
```text
@misc{alweiss2021improvedboundssunflowerlemma,
      title={Improved bounds for the sunflower lemma}, 
      author={Ryan Alweiss and Shachar Lovett and Kewen Wu and Jiapeng Zhang},
      year={2021},
      eprint={1908.08483},
      archivePrefix={arXiv},
      primaryClass={math.CO},
      url={https://arxiv.org/abs/1908.08483}, 
}
```
[Kewen Wu Improved bounds for the sunflower lemma](
https://shlw.github.io/slides/Sunflower.pdf)

---

## 12. Summary of Key Parameters

| Parameter               | Notation            | Definition                           |
|-------------------------|---------------------|--------------------------------------|
| Chromatic number        | $\chi(H)$           | Min colors, no monochromatic edge    |
| Strong chromatic number | $\chi_s(H)$         | Min colors, all edges rainbow        |
| Transversal number      | $\tau(H)$           | Min hitting set                      |
| Matching number         | $\nu(H)$            | Max disjoint edges                   |
| Fractional transversal  | $\tau^*(H)$         | LP relaxation of $\tau$              |
| Fractional matching     | $\nu^*(H)$          | LP relaxation of $\nu$               |
| Turán density           | $\pi(F)$            | Asymptotic edge density avoiding $F$ |
| Spectral radius         | $\rho(\mathcal{A})$ | Largest tensor eigenvalue            |

---

## References

The theory of hypergraphs remains an extraordinarily active area, with deep
connections to combinatorics, algebra, theoretical computer science, and
information theory. Open problems — especially around Turán densities,
sunflowers, and property B thresholds — continue to drive fundamental research.

[Math 426/529: Extremal Combinatorics by Jonathan A. Noel](
https://extremalcombinatorics.com/notes/root-1-2.html)

---

## Side note about directed hypergraphs (hyperdigraphs)

Everything in the introduction is for **undirected hypergraphs**, where
hyperedges are unordered subsets of vertices — i.e., each $E_i \subseteq V$ is a
set, with no notion of source, target, or orientation.

For completeness, here's a quick sketch of what the directed variants look like,
so the contrast is clear:

- **Directed hypergraphs** (or *hyperdigraphs*) replace each hyperedge with an
  ordered pair $(T, H)$ where $T$ (tail) and $H$ (head) are disjoint subsets
  of $V$, generalizing directed graphs.
- **Oriented hypergraphs** assign a $\pm 1$ orientation to each vertex-edge
  incidence, enabling a signed incidence matrix $B$ with $B^T B$ and $BB^T$
  playing the role of Laplacians.
- **$B$-hypergraphs** fix a partition of each edge into "input" and "output"
  vertices, common in categorical and database settings.

None of those appeared in the introduction — all definitions (degrees,
colorings, transversals, matchings, spectra via the adjacency tensor, Turán
numbers, sunflowers, etc.) were stated for the standard undirected model where
hyperedges are plain subsets $E \subseteq V$.

---
