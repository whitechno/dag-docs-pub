# OpenAI Astra: Ten Advances in Mathematics and Theoretical Computer Science

## The document

**OpenAI, August 1, 2026: “Ten advances in mathematics and theoretical computer
science”**

**Official announcement:**  
https://openai.com/index/ten-advances-in-mathematics/

**Full paper:**  
https://cdn.openai.com/pdf/ten-proofs-oai.pdf

**Reasoning/discovery walkthroughs:**  
https://cdn.openai.com/pdf/reasoning-walkthroughs.pdf

**Lean 4 formalizations:**  
https://github.com/openai/ten-proofs

One detail worth knowing: the current main paper is **253 pages and was updated
August 6**. OpenAI preserves the original August 1, **249-page** version here:

https://cdn.openai.com/pdf/ten-proofs-oai-original.pdf

OpenAI describes the system that produced the results as **“an internal version
of Astra, our next major model.”** Astra has not been released as a normal
ChatGPT/API model, and OpenAI has not said that “Astra” means GPT-6 or given a
normal public model card for it. A subsequent OpenAI post calls Astra “one of
our upcoming models.”

## What makes this announcement remarkable

This is not something like “Astra scored 98% on a graduate mathematics
benchmark.”

OpenAI is claiming that Astra generated **new mathematics**: ten results on
research problems that were genuinely open before the model worked on them.
Several are resolutions or disproofs of well-known long-standing conjectures.
OpenAI says the model generated the mathematical arguments; humans then helped
prepare them into manuscripts using the model, after which Astra formalized each
result as a Lean certificate.

The ten results are:

1. **High-dimensional sphere packing.**  
	 Determines the asymptotic strength of the Cohn–Elkies linear-programming
	 bound. In particular, it yields the first improvement since 1978 in the
	 general high-dimensional sphere-packing exponent: from the
	 Kabatianskii–Levenshtein exponent $0.599055\ldots$ to approximately $0.6044$.

2. **Binary and spherical codes.**  
	 Gives exponentially stronger upper bounds on code sizes across the parameter
	 range, with a corresponding spherical-code result.

3. **Existence of non-sofic groups.**  
	 This is particularly striking. The question of whether **every countable
	 group is sofic** had been open for decades. Astra constructs a non-sofic
	 group using property-$(T)$ expanders, previous work of Kun and Kun–Thom, a
	 combinatorial matching argument, the binary Leavitt algebra, and Thompson's
	 group $V$.

4. **Connes's rigidity conjecture.**  
	 Constructs infinitely many pairwise non-isomorphic property-$(T)$ groups
	 having the same group von Neumann algebra, thereby disproving the conjecture
	 and addressing a related question of Popa.

5. **Arithmetic circuit complexity of the permanent.**  
	 Establishes new lower bounds, including
	 $$
	 \Omega\!\left (\frac{n^4}{\log n}\right)
	 $$
	 for arithmetic formulas and $\Omega (n^2\log\log n)$ for division-free
	 circuits.

6. **Quantum parallel repetition.**  
	 Proves exponential parallel repetition for arbitrary finite two-player
	 entangled games — an analogue of a foundational classical
	 complexity-theoretic principle in the much harder quantum setting.

7. **Closest Vector Problem (CVP).**  
	 Gives a direct reduction from 3SAT establishing an $n^{1/400}$-factor
	 hardness of approximation for Euclidean CVP, with consequences for decoding
	 and other lattice problems. This connects directly with fundamental questions
	 in lattice algorithms and post-quantum cryptography.

8. **Ehrhart's volume conjecture.**  
	 Proves the sharp bound
	 $$
	 \operatorname{vol} (K)\leq \frac{ (n+1)^n}{n!}
	 $$
	 under the conjecture's lattice-point/barycenter conditions, in every
	 dimension.

9. **Multicolor Ramsey numbers.**  
	 Shows
	 $$
	 R_k (3)=k^{\Theta (k)},
	 $$
	 giving the sought superexponential lower bound and resolving Erdős problem
	 183 .

10. **Extremal graph theory.**  
		Produces counterexamples to two conjectures concerning extremal numbers —
		the Erdős–Simonovits compactness conjecture and an Erdős degeneracy
		conjecture — resolving Erdős problems 146 and 180.

## The Lean part is especially important

This changes how I would evaluate the announcement.

For every result OpenAI released a separate Lean 4 formalization —
`SpherePacking.lean`, `NonSoficGroup.lean`, `ConnesRigidity.lean`,
`Permanent.lean`, `QuantumParallelRepetition.lean`, etc. The repository can be
built with Lean 4.32.0 and mathlib, and OpenAI also provides a separate route
for independent checking using Comparator.

So the situation is much stronger than:

> “An LLM printed a convincing-looking proof.”

A Lean kernel can mechanically check that a formal theorem follows from the
definitions, lemmas, and axioms used in the formal development.

There is nevertheless an important distinction. **Lean verification establishes
the formal theorem encoded in Lean.** Human mathematicians still need to check
that the formal statement precisely represents the intended classical open
problem, that all definitions and hypotheses have the intended interpretation,
that there isn't an inappropriate assumption hidden in the formalization, and —
separately — understand the mathematical ideas and their significance.

That is why the informal 253-page manuscript remains important even though there
are Lean certificates.

## Did Astra really *discover* these results?

According to OpenAI's description, yes, in a stronger sense than most previous
“AI-assisted mathematics” work.

OpenAI says the **mathematical arguments themselves were generated by the
system**, rather than human mathematicians finding the central argument and
asking the model to fill in routine proof steps. OpenAI explicitly says it does
not want to attribute human authorship to arguments generated entirely by the
AI.

The separate 62-page **reasoning walkthroughs** are interesting for exactly this
reason. They describe, problem by problem, failed approaches, intermediate
ideas, changes of viewpoint, and the path to the final argument. The document
says these narratives were themselves produced by an AI model after reading the
original reasoning traces together with the resulting manuscripts. So I would
regard them as **post-hoc reconstructions of the discovery process**, not
literal unedited internal chain-of-thought transcripts.

That distinction matters.

## There's already independent mathematical follow-up

This is one of the strongest reasons not to dismiss the release as publicity.

On August 6, **Gábor Kun and Andreas Thom** posted *Nonsofic wreath products of
residually finite groups*. Their abstract explicitly says that their paper *
*builds on OpenAI's breakthrough in finding the first non-sofic group**,
extracts the underlying proof mechanism, and obtains additional non-sofic
constructions.

There is also interesting independent/concurrent work on the Connes rigidity
result. A separate August preprint reports that its authors had independently
developed a construction, with a preliminary manuscript assembled by July 27,
before OpenAI's August 1 announcement. The paper explicitly describes the two
pieces of work as independent and concurrent.

And work is already extending the Ehrhart result: another August preprint proves
the equality case as a counterpart to the inequality established in the OpenAI
work.

So only eight days after the announcement, at least parts of the package are
already interacting with ordinary mathematical research rather than existing
solely as an OpenAI claim.

## The "$2,000" claim needs careful interpretation

OpenAI says the total number of tokens needed to find solutions to these
problems would cost roughly **$2,000 at Sol API rates**.

That is striking, but it should **not** be interpreted as “OpenAI spent $2,000
and solved ten famous open problems.”

It is an estimate of the token/inference cost for the successful searches at
GPT-5.6 Sol API pricing. It does not account for training Astra,
model-development compute, researcher salaries, selecting and preparing the
problems, unsuccessful preliminary experiments, verification, manuscript
preparation, or formalization infrastructure. OpenAI also doesn't give us a
denominator such as “we tried exactly 12 open problems and solved 10”;
consequently, it isn't yet possible to infer Astra's probability of solving an
arbitrary research problem from these ten successes.

That last question — **selection effects** — is one of the most important things
I would like OpenAI to publish next.

## How significant is this?

Assuming the formalizations and correspondence with the intended theorems
survive specialist scrutiny, I think the significance is not primarily that
**ten particular problems were solved**.

It is that the same general-purpose model apparently moved across

$$
\text{harmonic analysis} \to \text{coding theory} \to \text{group theory} \to \text{operator algebras} \to \text{algebraic complexity} \to \text{quantum information} \to \text{lattices} \to \text{convex geometry} \to \text{Ramsey theory} \to \text{extremal combinatorics},
$$

and produced research-level arguments in all of them.

That is qualitatively different from an AI becoming extraordinarily good at IMO
problems. Olympiad problems are deliberately constructed to have short,
accessible solutions and are known to be solvable. Here the system has to decide
**what might be true, which existing ideas matter, how apparently unrelated
techniques might fit together, and whether a promising line of attack is
actually new**.

That is much closer to research.

There is one additional indication that Astra is a fairly broad capability jump
rather than a specialized mathematics model. On August 7, OpenAI reported that
its latest internal Astra evaluations showed large advances in **agentic coding
and cybersecurity**, enough that OpenAI said it could no longer rule out its
highest “Critical” cyber-capability category under its Preparedness Framework.

So at present Astra appears to be OpenAI's **next general frontier model**, with
scientific reasoning being one particularly dramatic manifestation of its
capabilities.

## What I would read first

Rather than reading all 253 pages sequentially, I'd start with **Chapter 3,
“Nonsofic groups exist”** and then **Chapter 1, sphere packing**. The former is
conceptually extraordinary because it answers an old yes/no existence question
in group theory; the latter is a good example where the numerical improvement
looks modest but actually ends a high-dimensional exponent barrier dating to
1978 .

