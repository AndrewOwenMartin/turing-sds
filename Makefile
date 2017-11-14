.PHONY: all run code doc

all: doc code

autobuild:
	~/virtualenvs/thesis/bin/when-changed turing_sds.nw -c 'make code doc'

turing_sds.tex: turing_sds.nw
	noweave -t4 -latex -index -delay turing_sds.nw | cpif turing_sds.tex

turing_sds.pdf: turing_sds.tex
	latexmk -pdf turing_sds.tex
	-pkill -hup mupdf

doc: turing_sds.pdf

turing_sds.py: turing_sds.nw
	notangle turing_sds.nw -R"new script" | cpif turing_sds.py

code: turing_sds.py

run: turing_sds.py
	~/virtualenvs/thesis/bin/ipython turing_sds.py
