# Create SVG figures of various hypergraphs

## figure_lncs.svg

Create SVG figure that matches exactly the PDF figure in
`arXiv/arXiv-2602.22976/figure_lncs.pdf`.

Save it in this directory as `figure_lncs.svg`.

## Figure description

The figure illustrates the tight lower bound construction for the 1/d
approximation guarantee (Lemma 2 in the paper). It shows a hypergraph with 2d
vertices arranged in d rows. Each row contains a pair of vertices xᵢ and yᵢ
connected by a weight-1 hyperedge (depicted as a light orange pill-shaped
region). A single additional hyperedge of weight 1+ε (depicted as a blue dashed
rounded rectangle) connects all x vertices x₁, xᵢ, ..., x_d.

The local-max algorithm selects the heavy hyperedge of weight 1+ε, yielding a
matching of weight 1+ε. The optimal matching instead picks all d weight-1 pairs,
yielding weight d. The ratio (1+ε)/d → 1/d as ε → 0, showing the approximation
bound is tight.
