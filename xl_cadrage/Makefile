filename=main
pdfName=XL_description_projet

all : 
	xelatex -output-directory=build/ $(filename).tex
	mv build/$(filename).pdf ./$(pdfName).pdf

read:
	evince $(pdfName).pdf &
