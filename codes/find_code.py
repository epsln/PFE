import sys
from utils.find import *

txt = open (sys.argv [1]).read ()
txt = clean_doc (txt);

arretes = find_arretes (txt)
titles = find_titles (txt)
clean_titles = clean_title (titles)
dates = find_dates (txt)
datePubli = find_date_publi (dates)
raa = find_raa (txt)
articles = find_articles (txt)
decret = find_decrets (txt)
lois = find_lois (txt)
names = find_names (txt)
orgs = find_orgs (txt)
locs = find_locs (txt)


print ("Arretes : ", len (arretes), arretes, "\n")
print ("Publi : ", datePubli, "\n")
print ("Dates : ", len (dates), dates, "\n")
print ("RAA : ", len (raa), raa, "\n")
print ("Articles : ", len (articles), articles, "\n")
print ("decret : ", len (decret), decret, "\n")
print ("Lois : ", len (lois), lois, "\n")

print ("Locs : ", len(locs), locs, "\n")
print ("Orgs : ", len(orgs), orgs, "\n")

#for title in clean_titles :
#	print (title, "\n")
print ("Raw titles : ", len (titles))
print ("Cleaned titles : ", len (clean_titles))
#print ("names : ", len (names), names, '\n')
