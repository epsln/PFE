filename=main
pdfName=Cadrage_PFE

all : 
	mkdir build/
	xelatex -output-directory=build/ $(filename).tex
	mv build/$(filename).pdf ./$(pdfName).pdf

read:
	evince $(pdfName).pdf &
