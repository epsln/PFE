import gensim
import io
import numpy as np
import re
from scipy import spatial
import spacy

nlp = spacy.load('fr_core_news_md')
model = gensim.models.Word2Vec.load("model/fr.bin")
#print(model['am;nagement'])
ff = io.open("docs/Lettre_Enquete.txt")
doc = nlp(ff.read())
fp = open("taxonomieUTF.txt")

taxo = np.load("taxonomyVectors.npy")
def tax2vec(keyword):
    try:
        vecIn = model[keyword.lower().strip("\n")]
    except KeyError:
        return "NONE", 10000

    mini = 100000
    bestWord = ""
    for i in range(taxo.shape[1]):
        vecTax = taxo[:,i]
        dist = spatial.distance.cosine(vecIn, vecTax ) 
        if dist > 0 and mini > dist:
            mini = dist
            for j, line in enumerate(fp):
                if j == i:
                    bestWord = line 
    return bestWord, mini 


def findWordInTax(originalDoc):
    with open("taxonomieUTF.txt") as taxo:
        for word in originalDoc:
            if taxo.countains(word):
                print(word)

minDist = 1000
dist    = 10000

keyList = []
for token in doc:
    if token.is_stop == False:
        (bWord, dist) = tax2vec(token.lemma_)
        keyList.append((bWord, dist))

keyList = set(keyList.sort(key=lambda tup: tup[1]))
print(keyList)
    
