Pandoc-based build system
=========================
February 11, 2026

This directory contains examples of and experiments with using Pandoc to build
PDF documents from Markdown sources. It is based
on [pandoc-book-template](https://github.com/wikiti/pandoc-book-template).

Pandoc references:
- <https://pandoc.org/>
- <https://github.com/jgm/pandoc>
- <https://github.com/jgm/pandoc-templates>

We also borrow freely from the approach used by Nathan Lambert for his book
"Reinforcement Learning from Human Feedback"
in <https://github.com/natolambert/rlhf-book/tree/main/book>.

_As a side note, the "Reinforcement Learning from Human Feedback" by Nathan
Lambert <https://rlhfbook.com/> is an excellent book written by a top expert in
the field of RLHF. It is not just very informative but also a delight to read.
Read this book to get a sense of where the present cutting-edge AI research is
going._

Installation on Mac
-------------------

Please check [this pandoc page](http://pandoc.org/installing.html) for more
information.

```
brew install pandoc
brew install pandoc-crossref
brew install --cask mactex
brew install make
```

Pandoc can be run through GitHub Actions. For some examples,
see <https://github.com/pandoc/pandoc-action-example>. Or, fork a process from
the [github action](
https://github.com/natolambert/rlhf-book/blob/main/.github/workflows/static.yml)
that auto-builds new versions on macOS.

[MacTex docs](https://tug.org/mactex/)

Setup
-----

Edit the *book/metadata.yml* file to set configuration data:

```yml
---
title: My book title
author: Daniel Herzog
rights: MIT License
lang: en-US
tags: [ pandoc, book, my-book, etc ]
abstract: |
  Your summary.
mainfont: DejaVu Sans # not available on Mac

# Filter preferences:
# - pandoc-crossref
linkReferences: true
---
```

You can find the list of all available keys in
<http://pandoc.org/MANUAL.html#extension-yaml_metadata_block> and
<https://pandoc.org/MANUAL.html#variables-for-latex>.

To build a LaTeX math equation, you can use an online equation
editor <https://www.codecogs.com/latex/eqneditor.php>.

Run
---

Run this pandoc command in the `pandoc-x` directory:
```text
pandoc \
$(ls book/chapters/*.md) \
-o ./build/pdf/book.pdf \
--metadata-file book/metadata.yml \
--metadata date="$(date +'%d %B %Y')" \
--filter pandoc-crossref \
--toc --toc-depth 3 \
--resource-path book/images \
--pdf-engine pdflatex \
--template book/templates/pdf.tex \
--bibliography=book/chapters/bib.bib --citeproc --csl=book/templates/ieee.csl
```
Other pandoc options:
```text
./book/chapters/03-training-overview.md \
-V geometry:margin=1.25in \
-V mainfont="texgyrepagella-regular.otf" -V monofont="Menlo" \
--pdf-engine=xelatex \
--pdf-engine pdflatex \
--listings

awk 'FNR==1 && NR!=1 {print "\n\n"}{print}' $(ls book/chapters/*.md)
```
Makefile variables:
```text
METADATA = book/metadata.yml
METADATA_ARGS = --metadata-file $(METADATA)
CHAPTERS = $(filter-out book/chapters/README.md,$(wildcard book/chapters/*.md))
TOC = --toc --toc-depth 3
MATH_FORMULAS = --mathjax # --webtex, is default for PDF/ebook. Consider resetting if issues.

BIBLIOGRAPHY = --bibliography=book/chapters/bib.bib --citeproc --csl=book/templates/ieee.csl
DATE_ARG = --metadata date="$(shell date +'%d %B %Y')"
DEBUG_ARGS = --verbose
FILTER_ARGS = --filter pandoc-crossref

# Combined arguments
ARGS = $(TOC) $(MATH_FORMULAS) $(METADATA_ARGS) $(FILTER_ARGS) $(DEBUG_ARGS) $(BIBLIOGRAPHY) $(DATE_ARG)

# Per-format options
PDF_ARGS = --template book/templates/pdf.tex --pdf-engine pdflatex --listings

# Chapters content
CONTENT = awk 'FNR==1 && NR!=1 {print "\n\n"}{print}' $(CHAPTERS)
CONTENT_FILTERS = tee # Use this to add sed filters or other piped commands

$(CONTENT) | $(CONTENT_FILTERS) | $(PANDOC_COMMAND) $(ARGS) $(PDF_ARGS) --resource-path=book -o $@
```

Overall workflow
----------------

In git repo: `.md sources + .svg figures` — all text, all diffable.

Build step (local or CI): `.md → .tex (pandoc) → .pdf (xelatex)`,
`.svg → .pdf (rsvg-convert)`. You could write a small Makefile or script for
this.

Overleaf: It's its own git repo under the hood but with a different purpose —
collaborative LaTeX editing.

Two approaches:
1. Overleaf as the final stage: Convert your .md to .tex once, upload to
   Overleaf with the PDF figures, and do final polish there. Overleaf doesn't
   handle .md or .svg natively.
2. Keep them separate: Git repo is the source of truth (Markdown + SVG),
   Overleaf is just for the submission-ready LaTeX. You'd sync manually when
   ready.

Either way, Overleaf will need .tex and .pdf figures — it can't use .md or .svg
directly. So the conversion step happens regardless, it's just a question of
when.

