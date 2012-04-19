ALL = evt2012.ps evt2012.pdf

all: $(ALL)

.SUFFIXES: .pic .tex .ps .dvi .bib .bbl .aux

%.ps: %.dvi
	dvips -Pcmz -t letter $< -o $@

%.dvi: %.tex
	latex $<
	@echo Checking whether we should rerun LaTeX or not...
	@(grep Rerun $(<:.tex=.log) >/dev/null && latex $<; exit 0)

%.pdf: %.dvi
	dvips -t letter -Ppdf -G0 -o temp.ps $<
	ps2pdf -dMaxSubsetPct=100 -dCompatibilityLevel=1.2 -dSubsetFonts=true -dEmbedAllFonts=true -dMonoImageResolution=600 temp.ps $@
	rm temp.ps

%.aux: %.tex
	latex $<

%.bbl: ../refs.bib %.aux
	@echo Building bibliography...
	bibtex $(@:.bbl=)



evt2012.dvi:: evt2012.bbl
evt2012.dvi:: $(wildcard *.tex)


clean:
	-rm -f *.{aux,dvi,log,bbl,blg}

veryclean: clean
	-rm -f *.ps


