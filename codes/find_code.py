import sys
import time
startTime = time.time ()
endTime = time.time ()

from utils.find import *
from utils.taxo import *

def display_time (arg) :
	global endTime
	global startTime
	endTime = time.time ()
	print (arg, " ", endTime-startTime)
	startTime = time.time ()

display_time ("Loading models")

txt = open (sys.argv [1]).read ()
txt = clean_doc (txt)

taxoTree = getTaxoTree()
display_time ("Building taxo tree")

arretes = find_arretes (txt)
display_time ("finding arretes")

titles = find_titles (txt)
clean_titles = clean_title (titles)
display_time ("finding titles")

dates = find_dates (txt)
display_time ("finding dates")

datePubli = find_date_publi (dates)
raa = find_raa (txt)
articles = find_articles (txt)
decret = find_decrets (txt)
lois = find_lois (txt)
display_time ("Finding other infos")

names = find_names (txt)
display_time ("finding names")
locs = find_locs (txt)
display_time ("finding locs")
orgs = find_orgs (txt)
display_time ("finding orgs")


taxo = get_taxo(txt, taxoTree)
display_time ("finding taxonomie")


print ("Arretes : ", len (arretes), arretes, "\n")
print ("Publi : ", datePubli, "\n")
print ("Dates : ", len (dates), dates, "\n")
print ("RAA : ", len (raa), raa, "\n")
print ("Articles : ", len (articles), articles, "\n")
print ("decret : ", len (decret), decret, "\n")
print ("Lois : ", len (lois), lois, "\n")

print ("Locs : ", len(locs), locs, "\n")
print ("Orgs : ", len(orgs), orgs, "\n")

print ("Taxo : ", len(taxo), taxo, "\n")

for title in clean_titles :
	print (title, "\n")
print ("Raw titles : ", len (titles))
print ("Cleaned titles : ", len (clean_titles))
print ("names : ", len (names), names, '\n')
