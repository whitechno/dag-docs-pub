# Statistical models for (AI) ranking

2026-01-31

https://arena.ai/ had pioneered an Elo-style ranking system for AI models based
on human-sourced pairwise comparisons.

See their Leaderboard https://arena.ai/leaderboard

And profile on Built-In-SF: https://www.builtinsf.com/company/arena-1

Arena transitioned from the classic online Elo rating to the Bradley-Terry model
in 2023:

Chatbot Arena: New models & Elo system update by Wei-Lin Chiang, Tim Li, Joseph
E. Gonzalez, Ion Stoica (Dec 7, 2023)
https://www.lmsys.org/blog/2023-12-07-leaderboard/

The Bradley-Terry model is the most widely used method for the ranking of
individuals, teams, or objects, based on pairwise comparisons between them.
Estimates of rankings within this model are commonly made using a simple
iterative algorithm first introduced by Zermelo almost a century ago. (He is
also well known for creating, together with Fraenkel, the ZFC set theory.)

See lecture notes about the Bradley-Terry model
https://web.stanford.edu/class/archive/stats/stats200/stats200.1172/Lecture24.pdf
from Statistics 200: Introduction to Statistical Inference, Stanford University
https://web.stanford.edu/class/archive/stats/stats200/stats200.1172/lectures.html

In 2023, M. Newman found an alternative and similarly simple iteration that
provably returns identical results but does so much faster - over a hundred
times faster in some cases:

M. E. J. Newman. Efficient Computation of Rankings from Pairwise Comparisons.
Journal of Machine Learning Research 24 (238):1−25, 2023.
https://jmlr.org/papers/v24/22-1086.html
