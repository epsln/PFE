import sys
import find

txt = open (sys.argv [1]).read ()
txt = find.clean_doc (txt);
arretes = find.find_arretes (txt)
titles = find.clean_title (find.find_titles (txt))

dates = find.find_dates (txt)
raa = find.find_raa (txt)
articles = find.find_articles (txt)
decret = find.find_decrets (txt)
lois = find.find_lois (txt)



#print ("Arretes : ", len (arretes), arretes, "\n")
#print ("Dates : ", len (dates), dates, "\n")
#print ("RAA : ", len (raa), raa, "\n")
#print ("Articles : ", len (articles), articles, "\n")
#print ("decret : ", len (decret), decret, "\n")
#print ("Lois : ", len (lois), lois, "\n")

print ("Titres : ", len (titles))
for title in titles :
	print (title, "\n")

print ("Titres : ", len (titles))
