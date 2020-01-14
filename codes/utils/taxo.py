import io
import numpy as np
import re
import spacy
import unidecode
from treelib import Node, Tree
from utils import find 

nlp = spacy.load('fr_core_news_md')

def tax2vec(vecIn):
    mini = 100000
    bestWord = ""
    idx = 0
    for i in range(taxo.shape[1]):
        vecTax = taxo[:,i]
        dist = spatial.distance.cosine(vecIn, vecTax ) 
        if dist > 0 and mini > dist:
            mini = dist
            idx = i
    bestWord = re.findall(r'".+?"', fp[idx])[0].replace('"',"")
    return bestWord, mini 

#Helper function to get the un-normalized taxonomy
def getNormalWord(lineNum):
    fp = open("utils/taxonomieUTF.txt")
    for i, line in enumerate(fp):
        if i == lineNum:
            return line 
           
def getTaxoTree():
    parentArr = []
    taxoTree = Tree()
    taxoTree.create_node("Taxo", str(-1)) #Root
    with open("utils/taxonomieUTF.txt") as fic:
        for i, line in enumerate(fic):
            currName = re.search(r'(?<=").+?(?=")', line)
            if currName :
                currName = find.strip_accent (currName.group())
            else :
                continue
            currName = currName.strip('"').strip(',')
            line = line.split('"')[0]
            virCount = line.count(',') - 2
            try:
                parentArr = parentArr[:virCount]
                parentArr[virCount] = str(i) 
            except IndexError:
                parentArr.append(str(i))
            if len(parentArr) > 1:
                taxoTree.create_node(currName, str(i), parent=parentArr[virCount-1])
            else:
                taxoTree.create_node(currName, str(i), parent="-1")

    return taxoTree

def getPathFromNode(idNode, taxoTree):
    pathArr = []
    node = taxoTree.get_node(idNode)
    while True:
        if type(node) != type(None):
            pathArr.append(node.tag) 
            node = taxoTree.parent(node.identifier)
        else:
            return pathArr[:-1] 

def findWordInTax(title, taxoTree):
    taxoOutput = []
    lineOutput = []
    title = title.lower()
    title = nlp(title)
    titleTreated = ""
    for word in title:
        if not word.is_stop:
            titleTreated += word.lemma_+" "
    titleTreated = titleTreated[:-1]
    with open("utils/taxonomieLemma.txt") as taxo:
        for i, line in enumerate(taxo):
            line = re.search(r'(?<=").+?(?=")', line)
            if line :
                line = line.group()
            else :
                continue
            line = line.strip('"').strip(',')
            line = " " + line + " "
            if line in titleTreated:
                outputLine = re.search(r'(?<=").+?(?=")', getNormalWord (i))
                if outputLine :
                    outputLine = find.strip_accent (outputLine.group())
                else :
                    continue
                path = getPathFromNode(str(i), taxoTree)
                taxoOutput += path
                #favorise les termes taxo détectés dans les titres
                for j in range (100) :
                    taxoOutput.append(outputLine)

    return taxoOutput


def get_taxo(text, taxoTree):
    out = list()
    outList = list()

    #Get their titles
    title = find.clean_title (find.find_titles(text))

    for t in title:
        out += findWordInTax(t, taxoTree)

    dictDuplicates = {i:out.count(i) for i in out}
    dictDuplicates = sorted(dictDuplicates.items(), key=lambda x: x[1], reverse=True)
    for elem in dictDuplicates:
        outList.append(elem[0])
    return outList
     
