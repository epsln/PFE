import json
import sys
from find import *

def find_index (json_file) :
	with open (json_file, "r") as f :
		lines = f.readlines()
		if len (lines) < 2:
			return 0
		last_line = json.loads (lines [-2])
		if "index" not in last_line :
			return 0
		return last_line ["index"] ["_id"] + 1


def add_json (json_tab, json_file) :
	#add the json_tab to end of _file
	with open (json_file, "a") as _file:
		_file.write (json.dumps (json_tab))
		_file.write ("\n")

def add_field (json_doc) :
	#field "dates"
	if "fieds" not in json_doc :
		json_doc ["fields"] = dict ()

def  add_meta (json_doc, meta_file) :
	add_field (json_doc)
	json_doc ["fields"] ["dates"] = find_dates (meta_file)
	json_doc ["fields"] ["arretes"] = find_arretes (meta_file)
	json_doc ["fields"] ["raa"] = find_raa (meta_file)
#	json_doc ["fields"] ["titres"] = clean_title (find_titles (meta_file))

#	json_doc ["fields"] ["noms"] = find_names (meta_file)

doc = "prefet_json.json"
index = {
	"index" : {
		"_index" : "raa",
		"_type" : "raa",
		"_id" : find_index (doc)
		}
	}
add_json (index, doc)

json_doc = dict ()

meta_file = open (sys.argv [1]).read ()
meta_file = clean_doc (meta_file);

add_meta (json_doc, meta_file)
add_json (json_doc, doc)

