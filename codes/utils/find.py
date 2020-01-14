from datetime import datetime
import unicodedata
import dateparser
import spacy
import re

#in clean doc, add ' between a simple character and upper case character


nlp = spacy.load('fr_core_news_md')

def strip_accent (doc) :
	return ''.join (c for c in unicodedata.normalize ('NFD', doc)
		if unicodedata.category (c) != 'Mn')

#remove all accents and special characters
def clean_doc (doc) :
	return strip_accent (" ".join (doc.split ()))	

#remove all similar entries
def remove_same (_list) :
	return list (dict.fromkeys (_list))

#remove everything except numbers and -
def remove_keep_nb (_list) :
	pattern = re.compile (r"[^0-9-]")
	return [pattern.sub ('', patt) for patt in _list]

#remove words of less than 1 or 2 char words, special chars, dates, ...
def clean_title (_list) :
	#remove "arretes", dates, pages, symboles spéciaux, nombres
	pattern = re.compile (r"(?i)(\d{1,2}\s\b\w{3,9}\b\s\d{2,4}|pages?|[\W\d_])")

	#remove mots < 3 lettres surrounded by spaces
	clean = re.compile (r"(?i)((?<= )\w{1,2}(?= ))")
	spaces = re.compile (r" {1,}")

	_list = remove_same ([spaces.sub (' ', clean.sub (' ', pattern.sub (' ', patt))) for patt in _list])
	#remove title that have less than 4 words
	return [patt for patt in _list if len(patt.split ()) > 4]


def find_arretes (txt) :
	#find arretes with format 53-...-...-....[...]
	refArretes = re.findall (r"\d{2,3}-\d{4}-\d{2}-\d{2}-\d{1,4}", txt)

	#find all arrete refs with format "arrete [...] AB/123.12-ABC/...
	arretes = re.findall(r"(?i)(?<=\barrete)(((?:[. *](?:prefectoral)?(?:ministeriel)?|n.)*?)(\w{2,8}(?:[\/_.-][a-z0-9]{1,5}){1,5})\b){1,2}", txt)

	#only take third capturing group
	arretes = [ref [2] for ref in arretes]

	return remove_same (
				refArretes + arretes
			)

def find_date_publi (dates) :
	if len (dates) <= 0 :
		return ""
	#first date is publication date
	return dates [0]
	

def find_dates (txt) :
	spaces = re.compile (r" {1,}")

	#find dates with format "13 janvier 2019", "1er février 97", ...
	dates = re.findall (r"\d{1,2}e?r?(?:\W)*\s\b[A-zÀ-ÿ]{3,9}\b\s\d{4}", txt) 
	#find dates with format "1/4/2013", "02/05/97", ...
	dates_slash = re.findall (r"[\s (,]\d{1,2}/\d{1,2}/\d{2,4}[\s ),]", txt)

	#remove "er" in "1er janvier"
	pattern = re.compile (r"er (?!\d)")
	dates = [pattern.sub (' ', date.lower ()) for date in dates]

	#remove special characters
	pattern = re.compile (r"[^\s\w]")
	dates = clean_dates_string (remove_same ([spaces.sub (" ", pattern.sub ('', date.lower ())) for date in dates]))	#remove_same allow a big gain in speed
	
	pattern = re.compile (r"[ (),]")
	dates += clean_dates_slash ([pattern.sub ('', date) for date in dates_slash])

	return remove_same (dates)

def clean_dates_string (dateList) :
	#return dates "DD month YYYY" as format "YYYY-MM-DD"
	returnList = []
	for dateString in dateList :
		try :
			val = dateparser.parse(dateString).date ()
			returnList.append (val.strftime ('%Y-%m-%d'))

		except Exception as e:
			#wrong date orthographe
			print ("Error in date parsing : ", dateString, " : ", e)
	return returnList

def clean_dates_slash (dateList) :
	#return dates "DD/MM/YYYY" as format "YYYY-MM-DD"
	returnList = []
	for dateString in dateList :
		try :
			val = datetime.strptime (dateString, "%d/%m/%Y")
			returnList.append (val.strftime ('%Y-%m-%d'))

		except :
			#wrong date orthographe : maybe year is 97 instead of 1997
			try :
				val = datetime.strptime (dateString, "%d/%m/%y")
				returnList.append (val.strftime ('%Y-%m-%d'))
			except Exception as e:
				#distance pour trouver orthographe correct ?
				print ("Error in date parsing : ", dateString, " : ", e)
	return returnList

def find_titles (txt) :
	#find "arrete" and the all characters (limit is 600 char) until "prefet", "arrete", "page" or "vu"
	titles = list ()
	titles = re.findall (r"(?i)((?<=(?<!present )arrete).{1,300}?(?=(prefet\b|article\b|(?<!present )arrete|page|vu\b)))", txt)
	spaces = re.compile (r" {1,}")					#detect multiple following spaces
	titles = [spaces.sub(' ', title[0]) for title in titles]	#remove all double spaces
	return remove_same (titles)

def find_raa (txt) :
	#find RAA names 12-9837-183
	raa = re.findall (r"0?\d{1,2}-[1-3]\d{3}-\d{1,3}\s", txt)
	return remove_same ([r.replace (" ", "") for r in raa])

def find_articles (txt) :
	#find "R. 3-827", "L16-98-893-1"
	articles = re.findall (r"(?i)\b[radl](?:[. *])*\d{1,4}(?:[.-]\d{1,4}(?:[-.]\d{1,4})*)", txt)
	pattern = re.compile (r"(?i)[^0-9-radl]") 			#all element that are not numbers or - or R A D and L
	return remove_same ([pattern.sub ('', art) for art in articles])

def find_lois (txt) :
	#find "loi(s)" and the following numbers 
	return remove_same (remove_keep_nb (
				re.findall (r"(?i)lois?(?:.){0,4}\d{1,4}-\d{1,4}", txt)
				)
			)

def find_decrets (txt) :
	#find "decret(s) and the following numbers
	return remove_same (remove_keep_nb (
				re.findall (r"(?i)decrets?(?:.){0,5}\d{1,4}-\d{1,4}", txt)
					)
			)

analysedText = ""
def analyse_text (txt) :
	global analysedText
	analysedText = nlp (txt)


def find_names (txt) :
	if analysedText == "" :
		analyse_text (txt)
	
	names = []

	#remove everything except chars, spaces and -
	clean = re.compile (r"(?i)[^-a-z\s]")

	#remove monsieur/madame/m/mme/m./mme./
	remove = re.compile (r"(?i)(?<=\b)(monsieur |madame |m[ \.]+|mme[ \.]+|DDT\b ?)")
	
	#remove words shorter than 2 characters and words longer than 20 char
	short = re.compile (r"\W*\b\w{1,2}\b|\W*\b\w{20,}\b")

	#remove multiple spaces
	spaces = re.compile (r" {1,}")

	for ent in analysedText.ents : 
		if "PER" in ent.label_ :	#Personne
			name = clean. sub ('', ent.text.lower ())
			name = spaces.sub (' ', short.sub ('', remove.sub ('', name)))
			if len (name.split ()) >= 2 :
				names.append (name)

	return remove_same (names)

def find_orgs (txt) :
	if analysedText == "" :
		analyse_text (txt)

	orgs = []

	#remove everything except chars, spaces and -
	clean = re.compile (r"(?i)[^-a-z\s]")

	#remove words shorter than 2 characters and words longer than 20 char
	short = re.compile (r"\W*\b\w{1,2}\b")

	#remove multiple spaces
	spaces = re.compile (r" {1,}")

	for ent in analysedText.ents : 
		if "ORG" in ent.label_ :	#Personne
			org = clean. sub ('', short.sub('', ent.text))
			org = spaces.sub (' ', org)
			orgs.append (org)
	analysedText = ""
	return remove_same (orgs)


def find_locs (txt) :
	if analysedText == "" :
		analyse_text (txt)

	locs = []

	#remove everything except chars, spaces and -
	clean = re.compile (r"(?i)[^\w'\s]")

	#remove isolated numbers (keep only number with letters ahead)
	remove = r"(?i)\b[a-z]+\d+|\b[a-z -]+\b"

	#remove words longer than 12 char
	short = re.compile (r"\W*\b\w\b|\W*\b\w{15,}\b")

	#remove arrete, monsieur/madame, cedex, 
	removeSpecials = re.compile (r"(?i)(?<=\b)(monsieur|madame|arrete|cedex|)")
	
	
	#remove multiple spaces
	spaces = re.compile (r" {1,}")

	for ent in analysedText.ents : 
		if "LOC" in ent.label_ :	#Personne
			loc = "".join (re.findall (remove, ent.text.replace ("_", " ")))
			#insert space before every majuscules
			loc = re.sub(r"(?<=\w)([A-Z])", r" \1", clean.sub ('', loc))
			loc = spaces.sub (' ', short.sub("", removeSpecials.sub ("", loc)))

			if len (loc) > 3 :
				locs.append (loc)

	return remove_same (locs)

