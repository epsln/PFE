#!/bin/sh

BPATH=$1  # Path to directory containing PDFs.
OPATH=$2  # Path to output directory.
BUILD="./build/"
TEMPFILE=$BUILD"temp.tiff"
MIN_WORDS=5     # Number of words required to accept pdftotext result.
# If the output path does not exist, attempt to create it.
if [ ! -d "$OPATH" ]; then
    mkdir -p "$OPATH"
fi

rm $BUILD*

for FILEPATH in $BPATH*pdf; do
	echo "Processing" "$FILEPATH"

	# Path to text file to be created. E.g. ./myfile.txt
	OUTFILE="${FILEPATH##*/}"
	OUTFILE="$OPATH${OUTFILE%%.*}".txt
	
	touch "$OUTFILE"    # The text file will be created regardless of whether

	#try to unpack files
    	pdftk "$FILEPATH" unpack_files output "$BUILD"
	
	#count if created >0 files
	shopt -s nullglob
	numfiles=("$BUILD"*)
	numfiles=${#numfiles[@]}
	if [ $numfiles -gt 0 ]
	then
		echo "Unpacked"
		gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=.out.pdf "$BUILD"*.pdf
		rm "$BUILD"*
		FILEPATH="./.out.pdf"
	fi
	

	echo -n "Attempting text extraction..."
	echo "$OUTFILE"
	pdftotext "$FILEPATH" "$OUTFILE"
	FILESIZE=$(wc -w < "$OUTFILE")
	echo " extracted $FILESIZE words."

	continue

	# If that fails, try Tesseract.
	if [ $FILESIZE -lt $MIN_WORDS ]
	then
		echo "Attempting OCR extraction..."
		echo "Image transformation..."

		magick -density 500 "$FILEPATH" -blur 3x1 -antialias -alpha remove -depth 8 -strip -background white $BUILD"page_%04d.tif"
		
		#clean each pages
		for TEMP in $BUILD*.tif; do
			echo "Doc" $TEMP
			magick -density 500 "$TEMP" -morphology Open Ring:1,1.5 "$TEMP"
			./textcleaner -g -e none -f 15 -o 10 $TEMP $TEMP
			magick  $TEMP -morphology Erode Ring:1,1.5 -monochrome $TEMP
		done
		#rebuild the doc
		magick $BUILD*.tif  -bordercolor White -border 10x10 $TEMPFILE	
		rm $BUILD*.tif
		
		#Use Tesseract to perform OCR on the tiff.
		#tesseract --tessdata-dir ./tesseract_lang_ref/ $TEMPFILE "$OUTFILE\_1" --dpi 500 -l fra --psm 12 --oem 1 > /dev/null 
		tesseract $TEMPFILE "$OUTFILE" --dpi 500 -l fra --psm 12 --oem 2 > /dev/null 
		rm $TEMPFILE

		mv "$OUTFILE.txt" "$OUTFILE"
		FILESIZE=$(wc -w < "$OUTFILE")
		echo " extracted $FILESIZE words
		"
	fi
done

exit 0

