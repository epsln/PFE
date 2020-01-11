import json
import sys
import glob
import os
import ntpath
from utils.find import *
from utils.taxo import *

#create taxonomy tree
taxoTree = getTaxoTree()

def path_leaf(path):
	head, tail = ntpath.split(path)
	return tail or ntpath.basename(head)


def remove_last_line (jsonFile) :
	#remove last line
	with open (jsonFile, "r+") as _file :
		_file.seek (0, os.SEEK_END)
		pos = _file.tell () - 1
		while pos > 0 and _file.read (1) != "\n":
			pos -= 1
			_file.seek (pos, os.SEEK_SET)
		if pos > 0:
			_file.seek (pos, os.SEEK_SET)
			_file.truncate ()

def add_json (jsonArray, jsonFile) :
	#add the json_tab to end of _file
	with open (jsonFile, "a") as _file :
		#add new text
		_file.write (json.dumps (jsonArray))

def  add_meta (jsonDoc, metaFile, filename) :
	dates = find_dates (metaFile)

	jsonDoc ["raa"] = find_raa (metaFile)
	jsonDoc ["publi"] = find_date_publi (dates)
	jsonDoc ["name"] = filename
	jsonDoc ["arretes"] = find_arretes (metaFile)
	jsonDoc ["dates"] = dates
	jsonDoc ["titres"] = clean_title (find_titles (metaFile))
	jsonDoc ["decrets"] = find_decrets (metaFile)
	jsonDoc ["lois"] = find_lois (metaFile)
	jsonDoc ["noms"] = find_names (metaFile)
	jsonDoc ["articles"] = find_articles (metaFile)
	jsonDoc ["taxo"] = get_taxo (metaFile, taxoTree)
	jsonDoc ["lieux"] = find_locs (metaFile)
	jsonDoc ["orgs"] = find_orgs (metaFile)

def add_doc_to_json (jsonDoc, doc2analyze) :
	try :
		metaFile = open (doc2analyze).read ()
		metaFile = clean_doc (metaFile);

		jsonArray = dict ()
		add_meta (jsonArray, metaFile, doc2analyze)
		add_json (jsonArray, jsonDoc)

	except Exception as e :
		print ("Error with ", doc2analyze, " : ", e)

jsonFile = "reactiv.json"

if not os.path.exists(jsonFile):
	with open (jsonFile, "w+") as f :
		print ("Created json file")
		f.write ("[\n")
else :
	remove_last_line (jsonFile)


for i, filename in enumerate(glob.glob (sys.argv [1] + "*.txt")) :
	if i > 0 :	#insert coma
		with open (jsonFile, "a") as _file :
			_file.write (",\n")
	print (i, " : ", path_leaf(filename))
	add_doc_to_json (jsonFile, filename)

with open (jsonFile, "a") as _file :
	_file.write ("\n]")
