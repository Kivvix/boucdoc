# Markdown sources
MD_dir = source
MD_list = $(shell find $(MD_dir) -type f -name '*.md')
MD_HTML_template = $(wildcard $(MD_dir)/_template/html/*)

# Build informations
BUILD_dir = build

# HTML info
# HTML_bdir : directory where build HTML version, this could be www dir of Apache or something else
HTML_bdir = $(BUILD_dir)/html

# autogen list of html files from MD_list
HTML_list  = $(patsubst $(MD_dir)/%.md, $(HTML_bdir)/%.html, $(MD_list))
# list of files in _template/html directory (to copy in HTML_bdir
HTML_template = $(patsubst $(MD_dir)/_template/html/%, $(HTML_bdir)/template/%, $(MD_HTML_template))
# list of css files to add in pandoc command line
CSS_template = $(patsubst $(MD_dir)/_template/html/%, template/% , $(shell find $(MD_dir)/_template/html -type f -name '*.css'))
MATH_render = --katex=https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.9.0/ 
#MATH_render = --katex
#MATH_render = --mathml
#MATH_render = --mathjax

# LaTeX/pdf info
LATEX_list = $(patsubst $(MD_dir)/%.md, $(BUILD_dir)/latex/%.tex, $(MD_list))
PDF_list = $(patsubst $(MD_dir)/%.md, $(BUILD_dir)/pdf/%.pdf, $(MD_list))

NATIVE_list = $(patsubst $(MD_dir)/%.md, $(BUILD_dir)/native/%.pandoc, $(MD_list))

#FILTERS = ../filters/panviz.py pandoc-crossref
FILTERS = ../filters/panviz2.py ../filters/panref.py ../filters/pancode.py ../filters/panabstract.py mermaid-filter 
EXTENSIONS = markdown+yaml_metadata_block+implicit_figures+definition_lists+example_lists+pipe_tables+table_captions

all :
	@ echo "Do something"

clean :
	rm -Rf build/*

$(BUILD_dir)/native/%.pandoc : $(MD_dir)/%.md
	@ mkdir -p "$(@D)"
	@ echo "\033[95m$(notdir $@) \033[0m"
	pandoc -s --from=$(EXTENSIONS) $(foreach filter,$(FILTERS), -F $(filter)) -t native $< -o $@

native : $(NATIVE_list)
	@ echo "\033[105m HTML done \033[0m"

$(HTML_bdir)/%.html : $(MD_dir)/%.md
	@ [[ -d $(@D) ]] && mkdir -p "$(@D)"
	@ echo "\033[36m$(notdir $@) \033[0m"
	pandoc --wrap=preserve -s --from=$(EXTENSIONS) $(foreach filter,$(FILTERS), -F $(filter)) $(MATH_render) $(foreach css,$(CSS_template), -c $(css)) -B source/_template/html/before.html -A source/_template/html/after.html --highlight-style tango -t html5 $< -o $@

$(BUILD_dir)/html/template/% : $(MD_dir)/_template/html/%
	@ echo "\033[35mcopy $< to $@\033[0m"
	@ mkdir -p "$(@D)"
	@ cp -R $< $(@D)

html : $(HTML_template) $(HTML_list)
	@ echo "\033[46m HTML done \033[0m"

$(BUILD_dir)/latex/%.tex : $(MD_dir)/%.md
	@ mkdir -p "$(@D)"
	@ echo "\033[36m$(notdir $@) \033[0m"
	pandoc --wrap=preserve -s --from=markdown+yaml_metadata_block+implicit_figures $(foreach filter,$(FILTERS), -F $(filter)) -B source/_template/latex/before.tex -A source/_template/latex/after.tex --highlight-style tango $< -o $@

latex : $(LATEX_list)
	@ echo "\033[46m LaTeX done \033[0m"

$(BUILD_dir)/pdf/%.pdf : $(BUILD_dir)/latex/%.tex
	@ [[ -d $(@D) ]] && mkdir -p "$(@D)"
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

