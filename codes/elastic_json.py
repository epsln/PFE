import json
import sys
import glob
import os
from utils.find import *
from utils.taxo import *

#create taxonomy tree
taxoTree = getTaxoTree()

def find_index (jsonFile) :
	with open (jsonFile, "r") as f :
		lines = f.readlines()
		if len (lines) < 2:
			return 0
		lastLine = json.loads (lines [-2])
		if "index" not in lastLine :
			return 0
		return lastLine ["index"] ["_id"] + 1

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
		_file.write ("\n")

def add_json (jsonArray, jsonFile) :
	#add the json_tab to end of _file
	with open (jsonFile, "a") as _file :
		_file.write (json.dumps (jsonArray))
		_file.write ("\n")

def add_field (jsonDoc) :
	#field "dates"
	if "fieds" not in jsonDoc :
		jsonDoc ["fields"] = dict ()

def  add_meta (jsonDoc, metaFile) :
	add_field (jsonDoc)
	dates = find_dates (metaFile)

	jsonDoc ["fields"] ["raa"] = find_raa (metaFile)
	jsonDoc ["fields"] ["publi"] = find_date_publi (dates)
	jsonDoc ["fields"] ["arretes"] = find_arretes (metaFile)
	jsonDoc ["fields"] ["dates"] = dates
	jsonDoc ["fields"] ["titres"] = clean_title (find_titles (metaFile))
	jsonDoc ["fields"] ["decrets"] = find_decrets (metaFile)
	jsonDoc ["fields"] ["lois"] = find_lois (metaFile)
	jsonDoc ["fields"] ["noms"] = find_names (metaFile)
	jsonDoc ["fields"] ["articles"] = find_articles (metaFile)
	jsonDoc ["fields"] ["taxo"] = get_taxo (metaFile, taxoTree)
	jsonDoc ["fields"] ["lieux"] = find_locs (metaFile)
	jsonDoc ["fields"] ["orgs"] = find_orgs (metaFile)

def add_doc_to_json (_id, jsonDoc, doc2analyze) :
	try :
		metaFile = open (doc2analyze).read ()
		metaFile = clean_doc (metaFile);

		index = {
			"index" : {
				"_index" : "raa",
				"_type" : "raa",
				"_id" : _id
				}
			}
		add_json (index, jsonDoc)
		
		jsonArray = dict ()

		add_meta (jsonArray, metaFile)
		add_json (jsonArray, jsonDoc)

	except Exception as e :
		print ("Error with ", doc2analyze, " : ", e)

jsonFile = "elastic.json"

if not os.path.exists(jsonFile):
	with open (jsonFile, "w+") as f :
		print ("Created json file")
	index = 0
else :
	remove_last_line (jsonFile)
	index = find_index (jsonFile)
	

for i, filename in enumerate (glob.glob (sys.argv [1] + "*.txt")) :
	print (i + index, " : ", filename)
	add_doc_to_json (i + index, jsonFile, filename)

with open (jsonFile, "a") as _file :
	_file.write ("\n")

