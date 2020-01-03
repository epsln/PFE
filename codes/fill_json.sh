#!/bin/sh

BPATH=$1  # Path to directory containing PDFs.
touch prefet_json.json

for FILEPATH in $BPATH*; do
	echo $FILEPATH
	python fill_json.py "$FILEPATH"
done

exit 0

