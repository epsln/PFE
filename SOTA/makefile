filename=main
pdfName=SoTA

all: 
	xelatex -output-directory=build/ ${filename}.tex
	biber build/${filename}
	xelatex -output-directory=build/ ${filename}.tex
	mv build/${filename}.pdf ./${pdfName}.pdf
read: 
	evince ${pdfName}.pdf &
