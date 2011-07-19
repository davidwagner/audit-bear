# Makefile for latex paper

all: paper.pdf

paper.pdf: paper.tex paper.bib
	pdflatex paper.tex
	bibtex paper
	pdflatex paper.tex
	pdflatex paper.tex

clean:
	rm -rf paper.aux paper.bbl paper.blg paper.log paper.pdf

