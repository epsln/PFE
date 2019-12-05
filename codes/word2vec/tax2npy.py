import gensim
import io
import numpy as np
import re
from scipy import spatial
import spacy

nlp = spacy.load('fr_core_news_md')
model = gensim.models.Word2Vec.load("model/fr.bin")
out = np.empty(300,)
with open("taxonomieUTF.txt") as taxo: 
    for line in taxo:
        phrase = re.findall(r'".+?"', line)[0].replace('"',"")
        phraseArr = np.zeros(300,)
        i = 0
        phrase = nlp(phrase)
        for token in phrase:
            if token.is_stop == False:
                token = token.lemma_
                try:
                    i+=1
                    phraseArr += model[token]
                except KeyError:
                    pass
        phraseArr /= float(i)
        out = np.column_stack((out, phraseArr))

        print(out.shape)        
np.save("taxonomyVectors.npy", out)
