# Minimal makefile for Sphinx documentation
SHELL := /bin/bash

# Define the source files and destination directory
FILES := ../README_sphynx.md ../RELEASE_NOTES.md ./gen_ai_hub/examples/gen_ai_hub.ipynb \
         ./gen_ai_hub/examples/orchestration-service.ipynb ./gen_ai_hub/examples/orchestration-service2.ipynb ./gen_ai_hub/examples/streaming.ipynb \
         ./gen_ai_hub/examples/prompt-registry.ipynb ./gen_ai_hub/examples/document-grounding.ipynb ./gen_ai_hub/examples/async-examples.ipynb \
		 ./gen_ai_hub/examples/evaluations.ipynb
DESTINATION := ./source/_reference

# Define HTML
HTML_FILE := ./build/html/index.html

# Tell make these targets are not files
.PHONY: all check_files copy_files api_doc build comment_out_lines

# Default target
all: check_files copy_files api_doc build comment_out_lines

# Check if all files exist
check_files:
	@$(foreach file,$(FILES),\
		$(if $(wildcard $(file)),,@echo "File $(file) exists.";,@echo "File $(file) does not exist!" && exit 1;))

# Copy files to the destination directory
copy_files: check_files
	@mkdir -p $(DESTINATION)
	@$(foreach file,$(FILES),\
		cp -v $(file) $(DESTINATION);)

# Generate API documentation with depth 1, force overwrite and no module index
api_doc:
	python -m sphinx.ext.apidoc -o source/_api_doc ../gen_ai_hub -d 1 -T -f -M

# Build the documentation with Sphinx
build: copy_files
	python -m sphinx -b html ./source ./build/html

# Open generated documentation in browser
preview_html: all
	@echo "Opening $(HTML_FILE) in the default browser"
	@xdg-open $(HTML_FILE) || open $(HTML_FILE) || start $(HTML_FILE)

# Comment out checkmarx relevant lines
comment_out_lines:
	@if [ "$$(uname)" = "Darwin" ]; then \
		sed -i '' '/window\.location/s/^/\/\/ /' ./build/html/_static/doctools.js; \
	else \
		sed -i '/window\.location/s/^/\/\/ /' ./build/html/_static/doctools.js; \
	fi