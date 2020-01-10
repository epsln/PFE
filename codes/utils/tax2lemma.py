import spacy
import re

outFile = open("test.txt", "w")
nlp = spacy.load('fr_core_news_md')
i = 0
with open("taxonomieUTF.txt") as taxo:
    for line in taxo:
        i+=1
        #print(round(float(i)/len(taxo.read())*100, 3),"%")
        print(i)
        lineTreated = re.findall(r'".+?"', line)[0].replace('"',"")
        lineTreated = line.strip('"').strip(',').lower()
        tokens = nlp(lineTreated)
        outLine = line.lower()
        for word in tokens:
            if word.is_stop:
                outLine = outLine.replace(str(word), "")
            if not word.is_stop:
                outLine = outLine.replace(str(word), str(word.lemma_))
        outLine = outLine.replace("  ", " ")
        outFile.write(outLine)
                
