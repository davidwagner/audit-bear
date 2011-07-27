# Makefile for latex paper

all: paper.pdf

paper.pdf: paper.tex paper.bib abstract.tex acknow.tex analyses.tex appendix.tex background.tex conclusion.tex introduction.tex related_work.tex date_time.tex hardware.tex miss_votes.tex pollingLocations.tex procedural.tex incomplete_data.tex appendix.sty authblk.sty usenix.sty
	pdflatex paper.tex
	bibtex paper
	pdflatex paper.tex
	pdflatex paper.tex

clean:
	rm -rf paper.aux paper.bbl paper.blg paper.log paper.pdf

