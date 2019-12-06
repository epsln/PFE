import sys
import re

txt = open (sys.argv [1]).read ()

def remove_same (_list) :
	return list (dict.fromkeys (_list))
def remove_keep_nb (_list) :
	pattern = re.compile (r"[^0-9-]")
	_list = [pattern.sub ('', patt) for patt in _list]
	return _list

#2012348-0010
def find_arretes (txt) :
	ref_arretes = re.findall (r"\d{2,3}-\d{4}-\d{2}-\d{2}-\d{1,4}", txt)
	
	return remove_same (
				ref_arretes
			)

def find_dates (txt) :
	#find dates with format "13 janvier 2019", "1er février 97", ...
	dates = re.findall (r"\d{1,2}e?r?(?:\W)*\s\b[A-zÀ-ÿ]{3,9}\b\s\d{4}", txt) 
	#find dates with format "1/4/2013", "02/05/97", ...
	dates_slash = re.findall (r"[\s (,]\d{1,2}/\d{1,2}/\d{2,4}[\s ),]", txt)
	
	#remove special characters
	pattern = re.compile (r"er (?!\d)")	#remove "er" in "1er janvier"
	dates = [pattern.sub (' ', date.lower ()) for date in dates]
	pattern = re.compile (r"[^\s\w]")	#special caracters
	dates = [pattern.sub ('', date.lower ()) for date in dates]
	
	pattern = re.compile (r"[ (),]")
	dates += [pattern.sub ('', date) for date in dates_slash]

	return remove_same (dates)

def find_titles (txt, arretes) :
	titles = list ()
	for arrete in (arretes) :
		regex = r"(?i)((\barr[eê]t[ée]\b|" + arrete + r").{1,200}?(\ble [pP]r[ée]fet\b|\barr[eê]t[ée]|page|vu))"
		print (arrete, regex)
		titles += re.findall (regex, txt)
	#return re.findall (r"(?i)(\barr[eê]t[ée]\b(?:.){1,300}(?=(\ble [pP]r[ée]fet\b|\barr[eê]t[ée])))", txt)
	return titles

def find_raa (txt) :
	#find RAA names 12-9837-183
	raa = re.findall (r"\d{1,2}-\d{4}-\d{1,4} ", txt)
	return remove_same ([r.replace (" ", "") for r in raa])
	
def find_articles (txt) :
	#find "R. 3-827", "L16-98-893-1"
	articles = re.findall (r"[RADL](?:[. *])*\d{1,4}(?:[.-]\d{1,4}(?:[-.]\d{1,4})*)", txt)
	pattern = re.compile (r"[^0-9-RADL]") #all non element that are not numbers or - or R A D and L
	return remove_same ([pattern.sub ('', art) for art in articles])

def find_lois (txt) :
	return remove_same (remove_keep_nb (
				re.findall (r"[lL]ois?(?:.){0,4}\d{1,4}-\d{1,4}", txt)
				)
			)

def find_decrets (txt) :
	return remove_same (remove_keep_nb (
				re.findall (r"[dD][ée]crets?(?:.){0,5}\d{1,4}-\d{1,4}", txt)
					)
			)

txt = " ".join (txt.split ())

arretes = find_arretes (txt)
titles = find_titles (txt, arretes)

dates = find_dates (txt)
raa = find_raa (txt)
articles = find_articles (txt)
decret = find_decrets (txt)
lois = find_lois (txt)

#print ("Arretes : ", len (arretes), arretes, "\n")
#print ("Dates : ", len (dates), dates, "\n")
#print ("RAA : ", len (raa), raa, "\n")
#print ("Articles : ", len (articles), articles, "\n")
#print ("decret : ", len (decret), decret, "\n")
#print ("Lois : ", len (lois), lois, "\n")

print ("Titres : ", len (titles))
for title in titles :
	print (title)

