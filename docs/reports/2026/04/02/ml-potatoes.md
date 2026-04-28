ML for Potatoes
================
April 2, 2026

Stumbled across this exploration of ML algorithms to predict the suitability of
Russet potato clones for advancement in breeding trials. This study addresses
the challenge of efficiently identifying high-yield, disease-resistant, and
climate-resilient potato varieties that meet processing industry standards.

It feels like a return to the origin of the ML - [the Iris dataset](
<https://archive.ics.uci.edu/dataset/53/iris) - a small classic dataset from
Fisher, 1936. (One of the earliest known datasets used for evaluating
classification methods.)

"Predictive analytics of selections of russet potatoes" in [wiley.com](
https://acsess.onlinelibrary.wiley.com/doi/full/10.1002/csc2.21432
) 28 December 2024

Code for the methods described in the article:
https://github.com/fabstat/burbank.

### Section 2.7

Simulation studies are essential for evaluating the performance of statistical
and machine learning models under various conditions. The ADEMP (Aims,
Data-generating mechanisms, Estimands, Methods, Perfomance measures)
framework, as outlined by Morris et al. (2019), provides a structured approach
to designing and reporting simulation studies. The present study leveraged the
ADEMP framework to evaluate the generalizability of the top performing
classification models (see Section 3.1) on simulated datasets that are
independent of the original potato trials dataset.

Morris, T. P., White, I. R., & Crowther, M. J. (2019). Using simulation studies
to evaluate statistical methods. *Statistics in Medicine*, 38(11),
2074–2102. https://doi.org/10.1002/sim.8086

PDF downloaded from PubMed Central (open access):
https://pmc.ncbi.nlm.nih.gov/articles/PMC6492164/
Local copy: `morris-white-crowther-2019-simulation-studies.pdf`
