all:
	~/virtualenvs/thesis/bin/when-changed *.nw -c 'noweave -t4 -latex -delay *.nw | cpif out.tex'
