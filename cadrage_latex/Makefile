filename=main
pdfName=Cadrage_PFE

all : 
	xelatex -output-directory=build/ $(filename).tex
	mv build/$(filename).pdf ./$(pdfName).pdf

read:
	evince $(pdfName).pdf &
