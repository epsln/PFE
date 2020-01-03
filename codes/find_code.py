import sys
from find import *

txt = open (sys.argv [1]).read ()
txt = clean_doc (txt);
arretes = find_arretes (txt)
titles = find_titles (txt)
clean_titles = clean_title (titles)

dates = find_dates (txt)
raa = find_raa (txt)
articles = find_articles (txt)
decret = find_decrets (txt)
lois = find_lois (txt)
names = find_names (txt)



print ("Arretes : ", len (arretes), arretes, "\n")
print ("Dates : ", len (dates), dates, "\n")
print ("RAA : ", len (raa), raa, "\n")
print ("Articles : ", len (articles), articles, "\n")
print ("decret : ", len (decret), decret, "\n")
print ("Lois : ", len (lois), lois, "\n")

print ("Titres : ", len (titles))

for title in clean_titles :
	print (title, "\n")

print ("Titres : ", len (titles))
print ("Titres : ", len (clean_titles))
print ("names : ", len (names), names, '\n')
