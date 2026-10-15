SRC_DIR = arXiv-2002.05014
BUILD_DIR = build
PUB_DIR = pub
ENTRY = Results_on_hypergraphs_A_survey
OUTPUT = hypergraph-intro-20260311

pdf: clean
	mkdir -p $(PUB_DIR) $(BUILD_DIR)
	cd $(SRC_DIR) && pdflatex -output-directory=../$(BUILD_DIR) $(ENTRY).tex
	cd $(SRC_DIR) && pdflatex -output-directory=../$(BUILD_DIR) $(ENTRY).tex
	cp $(BUILD_DIR)/$(ENTRY).pdf $(PUB_DIR)/$(OUTPUT).pdf
	rm -rf $(BUILD_DIR)

clean:
	rm -rf $(BUILD_DIR) $(PUB_DIR)

.PHONY: pdf clean
