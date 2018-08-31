# Markdown sources
MD_dir = source
MD_list = $(shell find $(MD_dir) -type f -name '*.md')

# image list
IMG_list = $(shell find $(MD_dir)/img -type f -name '*.png')

# Build informations
BUILD_dir = build

FILTERS = ../filters/panviz2.py ../filters/panref.py ../filters/pancode.py ../filters/panabstract.py mermaid-filter pandoc-citeproc
#pandoc-citeproc
EXTENSIONS = markdown+yaml_metadata_block+implicit_figures+definition_lists+example_lists+pipe_tables+table_captions+smart+inline_notes
CSL = --csl=source/biblio/3d-research.csl
CSL = --csl=source/biblio/springer-socpsych-brackets.csl

# Options
OPTIONS = --wrap=preserve -s

all :
	@ echo "Do something"

# function to autogen rules about pandoc compilation for output type $(1)
# $(1) : name of rule and directory
# $(2) : extension of output format
# $(3) : output format in pandoc
# $(4) : spectial options for pandoc (before and after file, css, math renderer, etc.
# $(5) : list of rules which $(1) depends
define OUTPUT_format

list = $$(patsubst $(MD_dir)/%.md, $(BUILD_dir)/$(1)/%.$(2),$(MD_list))
imgs = $$(patsubst $(MD_dir)/img/%.png, $(BUILD_dir)/$(1)/img/%.png,$(IMG_list))

$(BUILD_dir)/$(1) :
	@ echo "\033[34m$$@\033[0m"
	mkdir -p $$@

$(BUILD_dir)/$(1)/%.$(2) : $(MD_dir)/%.md $(wildcard $(MD_dir)/_template/$(1)/*.$(2))
	@ echo "\033[95m$$(notdir $$@)\033[0m"
	pandoc $(OPTIONS) \
		--from=$(EXTENSIONS) \
		$(foreach filter,$(FILTERS),-F $(filter)) $(CSL) \
		$(4) \
		-t $(3) $$< -o $$@

$(BUILD_dir)/$(1)/img/%.png : $(MD_dir)/img/%.png
	@ echo "\033[36m$$@\033[0m"
	@ mkdir -p "$$(@D)"
	cp $$< $$(@D)

$(1) : | $$(imgs) $(BUILD_dir)/$(1) $$(list) $(5)
	@ echo "\033[46m $(1) done \033[0m"

$(1)_img : $$(imgs)
	@ echo "\033[44m $(1) images done \033[0m"

endef


# HTML ################################################################
# list of css files to add in pandoc command line    
#CSS_template = $(patsubst $(MD_dir)/_template/html/%, template/% , $(shell find $(MD_dir)/_template/html -type f -name '*.css' | sort -r))
CSS_template = $(patsubst $(MD_dir)/_template/html/style/%.css, template/style/%.css , $(shell find $(MD_dir)/_template/html/style -type f -name '*.css' | sort -r))
#MATH_render = --katex=https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.9.0/ 
MATH_render = --katex=https://cdn.jsdelivr.net/npm/katex@0.10.0-beta/dist/
#MATH_render = --katex
#MATH_render = --mathml
#MATH_render = --mathjax

# concatenate all HTML options
HTML_opt = $(MATH_render) $(foreach css,$(CSS_template),-c $(css)) -B source/_template/html/before.html -A source/_template/html/after.html --highlight-style tango

# HTML template data
HTML_template = $(patsubst $(MD_dir)/_template/html/%.js, $(BUILD_dir)/html/template/%.js, $(wildcard $(MD_dir)/_template/html/*.js))
$(BUILD_dir)/html/template/style/%.css : $(MD_dir)/_template/html/style/%.css
	@ echo "\033[36mtransform copy $< to $@\033[0m"
	@ mkdir -p "$(@D)"
	gsed -r ':a; s%(.*)/\*.*\*/%\1%; ta; /\/\*/ !b; N; ba' $< | sed '/^\s*$$/d' | gsed -r 's/^[[:blank:]]+//' | tr -d '\n' > $@
$(BUILD_dir)/html/template/% : $(MD_dir)/_template/html/%
	@ echo "\033[35mcopy $< to $@\033[0m"
	@ mkdir -p "$(@D)"
	cp -R $< $(@D)

#sed 's|/\*|\n&|g;s|*/|&\n|g' $< | sed '/\/\*/,/*\//d' | sed '/^\s*$$/d' | sed 's/^ *//' | tr -d '\n' > $@
#cp $< $(@D)

HTML_template_rules=$(HTML_template) $(patsubst %.css,$(BUILD_dir)/html/%.css,$(CSS_template))

$(eval $(call OUTPUT_format,html,html,html5,$$(HTML_opt),$$(HTML_template_rules)))

# LaTeX ###############################################################
LATEX_opt = -B source/_template/latex/before.tex -A source/_template/latex/after.tex --highlight-style tango
$(eval $(call OUTPUT_format,latex,tex,latex,$$(LATEX_opt)))

# PDF #################################################################
PDF_list = $(patsubst $(MD_dir)/%.md, $(BUILD_dir)/pdf/%.pdf,$(MD_list))

$(BUILD_dir)/pdf :
	mkdir -p $@

$(BUILD_dir)/pdf/img/%.png : $(MD_dir)/img/%.png
	@ echo "\033[36m$@\033[0m"
	@ mkdir -p "$(@D)"
	cp $< $(@D)

#	pdflatex -output-directory $(@D) $<
$(BUILD_dir)/pdf/%.pdf : $(BUILD_dir)/latex/%.tex
	@ echo "\033[35m$(notdir $@)\033[0m"
	cd $(dir $<) && pdflatex -interaction=batchmode -output-directory ../pdf  $(notdir $<)

#pdf : | latex_img $(patsubst $(MD_dir)/img/%.png, $(BUILD_dir)/pdf/img/%.png,$(IMG_list)) $(BUILD_dir)/pdf $(BUILD_dir)/latex $(PDF_list)
pdf : | latex_img  $(BUILD_dir)/pdf $(BUILD_dir)/latex $(PDF_list)
	@ echo "\033[46m PDF done \033[0m"

# native ##############################################################
$(eval $(call OUTPUT_format,native,pandoc,native))

# ODT #################################################################
ODT_opt = --resource-path=$(BUILD_dir)/odt
$(eval $(call OUTPUT_format,odt,odt,odt,$$(ODT_opt)))

clean :
	rm -Rf build/*

# how to launch web server in different version of python
2.ws : webserver = python -m SimpleHTTPServer 8080
3.ws : webserver = python -m http.server 8080
%.ws :
	cd $(BUILD_dir)/html && $(webserver)

PYTHON_V = $(shell python -c 'import sys; print(sys.version_info[0])')
http_start : | html $(PYTHON_V).ws
	@ echo "end"

# for gnuplot with maths export in png
# first set terminal in gnuplot :
# ```
# 	set terminal epslatex color font 'Helvetica,10'
# ```
# plot your graph
# insert your gnuplot's output tex file in a minimal document with standalone document class
# ```
#	\documentclass[preview]{standalone}
#	\usepackage{graphicx}
#	\begin{document}
#	\input{YOURGNUPLOT.tex}
#	\end{document}
# ```
# compile it and use ImageMagick to convert it as base64 png :
# ```
#	convert -density 300 file.pdf -quality 90 png:- | base64
# ```
#
# Ce qui reste à améliorer dans cette procédure : trop de fichiers intermédiaire (il est possible d'avoir directement la sortie en png avec pdflatex mais il génère quoiqu'il arrive le pdf, et on a pas notre png en base64).

% : %.bd 
	mkdir -p $@_
	pandoc $(OPTIONS) \
		--from=$(EXTENSIONS) \
		$(foreach filter,$(FILTERS),-F $(filter)) \
		$(HTML_opt) \
		-t html5 $(foreach file,$(shell cat $<),$(file)) -o $@_/$@.html



