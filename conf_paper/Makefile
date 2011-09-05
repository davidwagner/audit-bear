# Makefile for latex paper (conference)

all: paper2.pdf

paper2.pdf: paper2.tex paper2.bib abstract.tex latexA/introduction.tex latexA/background.tex latexA/analyses.tex latexA/implementation.tex latexA/results.tex latexA/fvss.tex latexA/related_work.tex latexA/conclusion.tex latexA/acknow.tex 
	pdflatex paper2.tex
	bibtex paper2
	pdflatex paper2.tex
	pdflatex paper2.tex

clean:
	rm -rf paper2.aux paper2.bbl paper2.blg paper2.log paper2.pdf

