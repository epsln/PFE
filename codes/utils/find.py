from datetime import datetime
import unicodedata
import dateparser
import spacy
import re

nlp = spacy.load('fr_core_news_sm')

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
	_list = [pattern.sub ('', patt) for patt in _list]
	return _list

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


#2012348-0010
def find_arretes (txt) :
#TODO : complete arrete names search
	ref_arretes = re.findall (r"\d{2,3}-\d{4}-\d{2}-\d{2}-\d{1,4}", txt)
	
	return remove_same (
				ref_arretes
			)
	

def find_dates (txt) :
	#find dates with format "13 janvier 2019", "1er février 97", ...
	dates = re.findall (r"\d{1,2}e?r?(?:\W)*\s\b[A-zÀ-ÿ]{3,9}\b\s\d{4}", txt) 
	#find dates with format "1/4/2013", "02/05/97", ...
	dates_slash = re.findall (r"[\s (,]\d{1,2}/\d{1,2}/\d{2,4}[\s ),]", txt)

	#remove "er" in "1er janvier"
	pattern = re.compile (r"er (?!\d)")
	dates = [pattern.sub (' ', date.lower ()) for date in dates]

	#remove special characters
	pattern = re.compile (r"[^\s\w]")	#special caracters
	dates = clean_dates_string ([pattern.sub ('', date.lower ()) for date in dates])
	
	pattern = re.compile (r"[ (),]")
	dates += clean_dates_slash ([pattern.sub ('', date) for date in dates_slash])

	return remove_same (dates)

def clean_dates_string (date_list) :
	#return dates "DD month YYYY" as format "YYYY-MM-DD"
	#return [dateparser.parse(date_string).date().strftime ('%Y-%m-%d') for date_string in date_list]
	return_list = []
	for date_string in date_list :
		try :
			val = dateparser.parse(date_string)
			val = val.date()
			return_list.append (val.strftime ('%Y-%m-%d'))

		except :
			#wrong date orthographe
			print ("Wrong date writing : ", date_string)
	return return_list

def clean_dates_slash (date_list) :
	#return dates "DD/MM/YYYY" as format "YYYY-MM-DD"
	#return [datetime.strptime (date_string, "%d/%m/%Y").strftime ('%Y-%m-%d') for date_string in date_list]
	return_list = []
	for date_string in date_list :
		try :
			val = datetime.strptime (date_string, "%d/%m/%Y")
			return_list.append (val.strftime ('%Y-%m-%d'))

		except :
			#wrong date orthographe
			try :
				val = datetime.strptime (date_string, "%d/%m/%y")
				return_list.append (val.strftime ('%Y-%m-%d'))
			except :
				print ("Wrong date writing : ", date_string)
	return return_list

def find_titles (txt) :
	#find "Arreté" and the all characters (limit is 600 char) until "préfet", "arrêté", "page" or "vu"
	titles = list ()
	titles = re.findall (r"(?i)((?<=(?<!présent )arr[eê]t[eé]).{1,300}?(?=(pr[ée]fet\b|article\b|(?<!présent )arr[eê]t[ée]|page|vu\b)))", txt)
	spaces = re.compile (r" {1,}")	#detect multiple following spaces
	titles = [spaces.sub(' ', title[0]) for title in titles]	#remove all double spaces
	return remove_same (titles)

def find_raa (txt) :
	#TODO Compose number with the first date is 

	#find RAA names 12-9837-183
	raa = re.findall (r"\d{1,2}-\d{4}-\d{1,4} ", txt)
	return remove_same ([r.replace (" ", "") for r in raa])
	
def find_articles (txt) :
	#find "R. 3-827", "L16-98-893-1"
	articles = re.findall (r"[RADL](?:[. *])*\d{1,4}(?:[.-]\d{1,4}(?:[-.]\d{1,4})*)", txt)
	pattern = re.compile (r"[^0-9-RADL]") #all element that are not numbers or - or R A D and L
	return remove_same ([pattern.sub ('', art) for art in articles])

def find_lois (txt) :
	#find "Loi(s)" and the following numbers 
	return remove_same (remove_keep_nb (
				re.findall (r"[lL]ois?(?:.){0,4}\d{1,4}-\d{1,4}", txt)
				)
			)

def find_decrets (txt) :
	#find "Décret(s) and the following numbers
	return remove_same (remove_keep_nb (
				re.findall (r"[dD][ée]crets?(?:.){0,5}\d{1,4}-\d{1,4}", txt)
					)
			)


def find_names (txt) :
	names = []

	#remove everything except chars, spaces and -
	clean = re.compile (r"(?i)[^-a-z\s]")

	#remove monsieur/madame/m/mme/m./mme./
	remove = re.compile (r"(?i)(?<=\b)(monsieur |madame |m[ \.]+|mme[ \.]+|DDT\b ?)")
	
	#remove words shorter than 2 caracs and words longer than 20 char
	short = re.compile (r"\W*\b\w{1,2}\b|\W*\b\w{20,}\b")

	#remove multiple spaces
	spaces = re.compile (r" {1,}")

	for ent in nlp (txt).ents: 
		if "PER" in ent.label_ :	#Personne
			name = clean. sub ('', ent.text.lower ())
			name = spaces.sub (' ', short.sub ('', remove.sub ('', name)))
			if len (name.split ()) >= 2 :
				names.append (name)

	return remove_same (names)
