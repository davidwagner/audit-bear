# Makefile for latex paper (conference)

all: paper2.pdf paper.pdf

paper2.pdf: *.tex
	pdflatex paper2.tex
	bibtex paper2
	pdflatex paper2.tex
	pdflatex paper2.tex

paper.pdf: paper.tex paper.bib abstract.tex introduction.tex background.tex analyses.tex implementation.tex results.tex related_work.tex conclusion.tex fvss.tex incomplete_data.tex pollingLocations.tex acknow.tex appendix.tex date_time.tex hardware.tex miss_votes.tex authblk.sty usenix.sty
	pdflatex paper.tex
	bibtex paper
	pdflatex paper.tex
	pdflatex paper.tex

clean:
	rm -rf paper2.aux paper2.bbl paper2.blg paper2.log paper2.pdf paper.aux paper.bbl paper.blg paper.log paper.pdf

