MD_dir = source
BUILD_dir = build

MD_list = $(shell find $(MD_dir) -type f -name '*.md')
HTML_list = $(patsubst $(MD_dir)/%.md, $(BUILD_dir)/html/%.html, $(MD_list))
LATEX_list = $(patsubst $(MD_dir)/%.md, $(BUILD_dir)/latex/%.tex, $(MD_list))
PDF_list = $(patsubst $(MD_dir)/%.md, $(BUILD_dir)/pdf/%.pdf, $(MD_list))

MD_HTML_template = $(wildcard $(MD_dir)/_template/html/*)
HTML_template = $(patsubst $(MD_dir)/_template/html/%, $(BUILD_dir)/html/template/%, $(MD_HTML_template))

FILTERS = ../filter/panviz/main.py pandoc-crossref

all :
	@ echo "Do something"

clean :
	rm -Rf build/*

$(BUILD_dir)/html/%.html : $(MD_dir)/%.md
	@ mkdir -p "$(@D)"
	@ echo "\033[36m$(notdir $@) \033[0m"
	pandoc -s --from=markdown+yaml_metadata_block+implicit_figures $(foreach filter,$(FILTERS), -F $(filter))  --katex -c template/css/skeleton.css -c template/css/custom.css -A source/_template/html/after.html --highlight-style tango $< -o $@

$(BUILD_dir)/html/template/% : $(MD_dir)/_template/html/%
	@ echo "\033[35mcopy $< to $@\033[0m"
	@ mkdir -p "$(@D)"
	@ cp -R $< $@

html : $(HTML_template) $(HTML_list)
	@ echo "\033[46m HTML done \033[0m"

$(BUILD_dir)/latex/%.tex : $(MD_dir)/%.md
	@ mkdir -p "$(@D)"
	@ echo "\033[36m$(notdir $@) \033[0m"
	pandoc -s --from=markdown+yaml_metadata_block+implicit_figures $(foreach filter,$(FILTERS), -F $(filter)) --highlight-style tango $< -o $@

latex : $(LATEX_list)
	@ echo "\033[46m LaTeX done \033[0m"

$(BUILD_dir)/pdf/%.pdf : $(BUILD_dir)/latex/%.tex
	@ mkdir -p "$(@D)"
	@ echo "\033[36m$(notdir $@) \033[0m"
	pdflatex -output-directory=./$(@D) $<

pdf : $(PDF_list)
	@ echo "\033[46m PDF done \033[0m"

PYTHON_V = $(shell python -c 'import sys; print(sys.version_info[0])')
ifeq "$(PYTHON_V)" "2"
	PYTHON_ws = python -m SimpleHTTPServer 8080
else
	PYTHON_ws = python -m http.server 8080
endif
http_start : html
	cd $(BUILD_dir)/html && $(PYTHON_ws)

