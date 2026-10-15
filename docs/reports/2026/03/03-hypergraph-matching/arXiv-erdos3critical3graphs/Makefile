SRC_DIR = arXiv-2512.24850
BUILD_DIR = build
PUB_DIR = pub
ENTRY = 3_critical_3_graphs_of_minimum_degree_7
OUTPUT = erdos3critical3graphs-20260313

pdf: clean
	mkdir -p $(PUB_DIR) $(BUILD_DIR)
	TEXINPUTS=$(SRC_DIR): pdflatex -output-directory=$(BUILD_DIR) $(SRC_DIR)/$(ENTRY).tex
	TEXINPUTS=$(SRC_DIR): pdflatex -output-directory=$(BUILD_DIR) $(SRC_DIR)/$(ENTRY).tex
	cp $(BUILD_DIR)/$(ENTRY).pdf $(PUB_DIR)/$(OUTPUT).pdf
	rm -rf $(BUILD_DIR)

clean:
	rm -rf $(BUILD_DIR) $(PUB_DIR)

.PHONY: pdf clean
