import sys
import re

txt = open (sys.argv [1]).read ()

def remove_same (_list) :
	return list (dict.fromkeys (_list))


#2012348-0010
def find_arretes (txt) :
	return remove_same (re.findall (r"\d{4,8}(?:[-_ ])*[a-zA-Z]{2,10}(?:\d{1})*(?:-)*(?:\d{2})*(?:-)*(?:[A-Za-z])*(?:[-_ ]\d{1,3})", txt) + re.findall (r"\d{2,3}-\d{4}-\d{2}-\d{2}-\d{1,4}", txt))

def find_dates (txt) :
	_dates = re.findall (r"\d{1,2}e?r?\s\b\w{3,8}\b\s\d{4}", txt) 
	_dates_slash = re.findall (r"[\s (]\d{1,2}/\d{1,2}/\d{2,4}[\s )]", txt)
	dates = list ()
	for date in _dates:
		dates.append (date.lower ())
	for date in _dates_slash :
		dates.append (date.replace (" ", "").replace ("(", "").replace (")", ""))
	return remove_same (dates)

def find_raa (txt) :
	_raa = remove_same (re.findall (r"\d{1,2}-\d{4}-\d{1,4} ", txt))
	raa = list ()
	for ra in _raa :
		raa.append (ra.replace (" ", ""))
	return raa
	
def find_articles (txt) :
	_articles = re.findall (r"[RADL](?:[. *])*\d{1,4}(?:-\d{1,4}(?:-\d{1,4})*)", txt)
	articles = list ()
	for article in _articles :
		articles.append (article.replace (" ", "").replace (".", ""))
	return remove_same (articles)

def find_decrets_lois (txt) :
	return remove_same (re.findall (r"(?:°)\d{4}-\d{1,4}", txt))


txt = " ".join (txt.split ())

arretes = find_arretes (txt)
dates = find_dates (txt)
raa = find_raa (txt)
articles = find_articles (txt)
decret = find_decrets_lois (txt)

print ("Arretes : ", len (arretes), arretes, "\n")
print ("Dates : ", len (dates), dates, "\n")
print ("RAA : ", len (raa), raa, "\n")
print ("Articles : ", len (articles), articles, "\n")
print ("decret : ", len (decret), decret, "\n")
