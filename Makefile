.PHONY: all run code doc

all: doc code

autobuild:
	~/virtualenvs/thesis/bin/when-changed turing_sds.nw -c 'make code doc'

turing_sds.tex: turing_sds.nw
	noweave -t4 -filter emptydefn -filter btdefn -delay -latex -index turing_sds.nw | cpif turing_sds.tex

turing_sds_original.tex: turing_sds_original.nw
	noweave -t4 -latex -index -filter btdefn -delay turing_sds_original.nw | cpif turing_sds_original.tex

turing_sds.pdf: turing_sds.tex
	latexmk -halt-on-error -pdf turing_sds.tex
	-pkill -hup mupdf

turing_sds_original.pdf: turing_sds_original.tex
	latexmk -halt-on-error -pdf turing_sds_original.tex
	-pkill -hup mupdf

doc: turing_sds.pdf

#turing_sds.py: turing_sds.nw
#	notangle turing_sds.nw -R"new script" | cpif turing_sds.py

turing_sds_original.py: turing_sds_original.nw
	notangle -t4 -filter btdefn turing_sds_original.nw | cpif turing_sds_original.py

%.py: turing_sds.nw
	notangle -t4 -R"$(subst _,-,$@)" -filter emptydefn -filter btdefn turing_sds.nw | cpif $@ && touch $@

code: two_agent_solution.py run_two_agent_solution.py multi_swarm_solution.py

run: turing_sds.py
	~/virtualenvs/thesis/bin/ipython turing_sds.py
