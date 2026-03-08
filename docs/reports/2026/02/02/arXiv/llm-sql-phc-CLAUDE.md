# Generate PDF from LaTeX

Folder `arXiv-2403.05821v2` contains the LaTeX source files.

Top level source file (the entry point) is `example_paper.tex`.

Generate PDF output from these sources. Place the output PDF in the `pub`
folder. Use `build` folder for intermediate files.

It runs on macOS 15.7.3, zshell. I have installed mactex with
`brew install --cask mactex` command.

## Build commands

Run from the `arXiv-2403.05821v2` directory:
```bash
# Create output directories
mkdir -p ../pub ../build

# First pdflatex pass (generates .aux files)
pdflatex -output-directory=../build example_paper.tex

# Run bibtex from build/ with BIBINPUTS and BSTINPUTS pointing back to the source directory
cd ../build && \
BIBINPUTS=../arXiv-2403.05821v2: BSTINPUTS=../arXiv-2403.05821v2: bibtex example_paper && \
cd ../arXiv-2403.05821v2

# Second and third pdflatex passes (resolve references)
pdflatex -output-directory=../build example_paper.tex
pdflatex -output-directory=../build example_paper.tex

# Copy final PDF to pub folder
cp ../build/example_paper.pdf ../pub/llm-sql-20250409.pdf

# Clean up
rm -rf ../build ../pub
```

Run from the `arXiv` directory:
```bash
# Create output directories
mkdir -p pub build

# First pdflatex pass (generates .aux files)
TEXINPUTS=arXiv-2403.05821v2: pdflatex -output-directory=build arXiv-2403.05821v2/example_paper.tex

# Run bibtex (openout_any=a allows writing .blg into build/)
BIBINPUTS=arXiv-2403.05821v2: BSTINPUTS=arXiv-2403.05821v2: openout_any=a bibtex build/example_paper

# Second and third pdflatex passes (resolve references)
TEXINPUTS=arXiv-2403.05821v2: pdflatex -output-directory=build arXiv-2403.05821v2/example_paper.tex
TEXINPUTS=arXiv-2403.05821v2: pdflatex -output-directory=build arXiv-2403.05821v2/example_paper.tex

# Copy final PDF to pub folder
cp build/example_paper.pdf pub/llm-sql-20250409.pdf

# Clean up
rm -rf build pub
```

All in one line:
```text
rm -rf build pub && \
mkdir -p pub build && \
TEXINPUTS=arXiv-2403.05821v2: pdflatex -output-directory=build arXiv-2403.05821v2/example_paper.tex && \
BIBINPUTS=arXiv-2403.05821v2: BSTINPUTS=arXiv-2403.05821v2: openout_any=a bibtex build/example_paper && \
TEXINPUTS=arXiv-2403.05821v2: pdflatex -output-directory=build arXiv-2403.05821v2/example_paper.tex && \
TEXINPUTS=arXiv-2403.05821v2: pdflatex -output-directory=build arXiv-2403.05821v2/example_paper.tex && \
cp build/example_paper.pdf pub/llm-sql-20250409.pdf && \
rm -rf build
```

## Run with Makefile

```text
make pdf
```

## Added page numbers for easier reference

In `arXiv-2403.05821v2/example_paper.tex` added after line 159:
```latex
\fancyfoot[C]{\raisebox{-20pt}{\thepage}} % to show page number at bottom center without affecting the text layout
```
