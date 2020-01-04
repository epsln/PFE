import spacy
import re

outFile = open("taxonomieLemma.txt", "w")
nlp = spacy.load('fr_core_news_md')
with open("taxonomieUTF.txt") as taxo:
    for line in taxo:
        lineTreated = re.findall(r'".+?"', line)[0].replace('"',"")
        lineTreated = line.strip('"').strip(',')
        tokens = nlp(lineTreated)
        outLine = line
        for word in tokens:
            if word.is_stop:
                outLine = outLine.strip(str(word))
            if not word.is_stop:
                outLine = outLine.replace(str(word), str(word.lemma_))
        outFile.write(outLine)
                
