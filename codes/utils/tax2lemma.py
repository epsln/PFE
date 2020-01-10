import spacy
import re

#Simple script to lemmatize and delete stopwords from original taxonomy


outFile = open("test.txt", "w")
nlp = spacy.load('fr_core_news_md')
i = 0

with open("taxonomieUTF.txt") as taxo:
    for line in taxo:
        i+=1
        print(round(float(i)/6537*100, 3),"%")
        lineTreated = re.findall(r'".+?"', line)[0].replace('"',"")
        lineTreated = line.strip('"').strip(',').lower()
        tokens = nlp(lineTreated)
        outLine = line.lower()
        #If the string contains only one word, just replace by the lemma
        if len(outLine.split()) == 1:
            outLine = outLine.replace(str(word), str(word.lemma_))
            outFile.write(outLine)
            continue
        #Else delete stopwords and replace by lemma 
        for word in tokens:
            if word.is_stop:
                outLine = outLine.replace(str(word), "")
            if not word.is_stop:
                outLine = outLine.replace(str(word), str(word.lemma_))
        outLine = outLine.replace("  ", " ")
        outFile.write(outLine)
                
